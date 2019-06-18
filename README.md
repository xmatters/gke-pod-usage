# pod_usage

pod_usage queries a k8s cluster and compares pod usage versus the pod requests and limits. It provides output that can then be analyzed to determine if optimizations can be made, and helps you find out if your oversubscribed or undersubcribed.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. It will use the GKE credentials from your environment.

### Prerequisites

```
Python 3.6+
A GKE Kubernetes Cluster with Heapster enabled (this is default.)
Python kubernetes-client
```

### Installing

```
python3 -m venv /path/to/new/virtual/env
git clone ssh://git@github.com:xmatters/gke-pod-usage.git
cd gke-pod-usage
pip install -r requirements.txt
```

## Running

```
gcloud config set project <project>
gcloud container clusters get-credentials <cluster> --zone <zone> --project <project>
python3 pod_usage.py <namespace>
```