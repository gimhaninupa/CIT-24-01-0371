# Lab 6: Kubernetes Fundamentals

## Task 1.2: Cluster Components

| Component | Pod Name (Example) | Role in Cluster |
| :--- | :--- | :--- |
| API Server | kube-apiserver-minikube | Control Plane |
| etcd | etcd-minikube | Control Plane |
| Scheduler | kube-scheduler-minikube | Control Plane |
| Controller Manager | kube-controller-manager-minikube | Control Plane |
| kube-proxy | kube-proxy-minikube | Worker Node |

**Missing Components:**
The `kubelet` and the container runtime (e.g., Docker) do not appear in the list of pods. This is because they are not deployed as containers managed by Kubernetes. Instead, they run as background system services (daemons) directly on the host operating system of every node in order to manage the pods themselves.