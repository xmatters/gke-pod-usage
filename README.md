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

## Results
```
> python3.6 pod_usage.py namespace
NAME                                                             MEMORY LIMIT     MEMORY REQUEST   MEMORY USED      DIFFERENCE
namespace-podname-5c559b96df-g2c6b                               6.8 G            2.4 G            851.0 M          -1.5 G
namespace-podname-7978ff7bbb-phds8                               6.8 G            2.4 G            1.3 G            -1.1 G
namespace-podname-7d6b6d4b9c-tgtjk                               6.8 G            2.4 G            982.0 M          -1.4 G
namespace-podname-f7d65545f-8mbqk                                6.8 G            2.4 G            929.0 M          -1.5 G
namespace-podname-8bc6f6946-cjbqz                                6.8 G            2.4 G            958.0 M          -1.4 G
namespace-podname-5f75b4878c-ddhgb                               4.8 G            2.4 G            1.0 G            -1.3 G
namespace-podname-d9c8f8596-qc428                                6.8 G            2.4 G            4.2 G            1.8 G
namespace-podname-58b78d865-zfjq9                                6.8 G            2.4 G            923.0 M          -1.5 G
namespace-podname-54cd84fc4-5lv9z                                6.8 G            2.4 G            779.0 M          -1.6 G
namespace-podname-9b548957-ljjh9                                 6.8 G            2.4 G            909.0 M          -1.5 G
namespace-podname-676974b948-fj9n9                               4.8 G            2.4 G            979.0 M          -1.4 G
namespace-podname-d69c4db89-77tj8                                4.8 G            2.4 G            1.0 G            -1.3 G
namespace-podname-579f9d8848-fj5vp                               2.2 G            228.0 M          34.0 M           -194.0 M
namespace-podname-668b4b54-lfp6z                                 2.2 G            228.0 M          1.1 G            899.0 M
TOTAL                                                            79.5 G           28.9 G           15.8 G           -13.2 G

```

## Disclaimer
pod_usage is not an officially supported xMatters product.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.