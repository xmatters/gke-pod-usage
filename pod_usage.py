#!/usr/bin/env python3
"""This utility compares pod resource requests and limits against actual usage"""

import subprocess
import argparse

from kubernetes import client, config

from bytes2human import human2bytes, bytes2human


def get_pods(kube, namespace):
    """Return a list of pods in a namespace"""

    return kube.list_pod_for_all_namespaces(field_selector='metadata.namespace=%s' % namespace,
                                            include_uninitialized=False,
                                            watch=False)


def get_usage(namespace):
    """Return usage for a namespace, uses heapster"""

    return subprocess.run(['kubectl', 'top', 'pod', '--namespace=%s' % namespace],
                          stdout=subprocess.PIPE).stdout.decode('utf-8')


def formatted_pods(pods):
    """Create a dictionary of pods with their resource information"""

    pod_map = {}
    for pod in pods.items:
        podname = pod.metadata.name
        pod_namespace = pod.metadata.namespace
        memory_request = 0
        memory_limit = 0

        for container in pod.spec.containers:
            try:
                # Convert human readable IEC values to an integer
                memory_request += human2bytes(container.resources.requests['memory'])
                memory_limit += human2bytes(container.resources.limits['memory'])
            except (KeyError, TypeError): # Skip containers without defined requests or limits
                pass

        pod_map[podname] = {'namespace': pod_namespace,
                            'resources': {'requests': {'memory': memory_request},
                                          'limits':   {'memory': memory_limit}}}

    return pod_map


def main(namespace):
    """Compare pod usage to its requests and limits"""

    # Load kubernetes config from environment, and connect
    config.load_kube_config()
    kube = client.CoreV1Api()

    # Get a dictionary of pods and their resources
    pods = formatted_pods(get_pods(kube, namespace))

    # Get pod usage from the namespace
    usage = get_usage(namespace)

    # Convert multiline usage output, skip the first row which is a header row
    for row in usage.splitlines()[1:]:
        podname = row.split()[0]
        memory_usage = human2bytes(row.split()[2])

        pods[podname]['resources']['usage'] = {'memory': memory_usage}

    # A namespaces may not exist, and may not contain pods
    if not pods:
        print('No resources found.')
        exit(1)
    else:
        total_limits = 0
        total_requests = 0
        total_usage = 0
        total_diff = 0

        # Print header row
        print(f'{"NAME":64} {"MEMORY LIMIT":16} {"MEMORY REQUEST":16} {"MEMORY USED":16} {"DIFFERENCE"}')

        # Print details for each pod in the namespace
        for pod, state in pods.items():
            requests = state['resources']['requests']['memory']
            limits = state['resources']['limits']['memory']

            try:
                usage = state['resources']['usage']['memory']
            except KeyError: # Skip non-running pods
                usage = 0

            # Add it all up
            difference = usage - requests
            total_limits += limits
            total_requests += requests
            total_usage += usage
            total_diff += difference

            # Print pod specific details
            print(f'{pod:64} {bytes2human(limits):16} {bytes2human(requests):16} {bytes2human(usage):16} {bytes2human(difference)}')

        # Print totals
        print(f'{"TOTAL":64} {bytes2human(total_limits):16} {bytes2human(total_requests):16} {bytes2human(total_usage):16} {bytes2human(total_diff)}')


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    PARSER.add_argument("namespace", help="Kubernetes namespace.")
    ARGS = PARSER.parse_args()

    main(ARGS.namespace)
