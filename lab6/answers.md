# Checkpoint Questions

**Q1. In your own words, explain the difference between the control plane and a worker node.**
The Control Plane is the orchestration layer that manages the cluster, maintains desired states, schedules deployments, and provides the API. The Worker Nodes are the physical or virtual machines that actually run the containerized application workloads inside Pods.

**Q2. Delete the pod, then recreate it... Has the IP changed? Explain why.**
Yes, the IP address changed. Pods in Kubernetes are "ephemeral" (temporary). When a pod is deleted, its network namespace is destroyed. When a new pod is created to replace it, Kubernetes assigns it a brand new, dynamically generated IP address from the internal cluster network pool.

**Q3. Using the lecture's control-loop model, describe exactly what Kubernetes did when you deleted the pod.**
1. **Desired State:** The Deployment's manifest dictates there must be exactly 3 replicas running at all times.
2. **Gap Detected:** When a pod was manually deleted, the actual state dropped to 2 running replicas. The Controller Manager observed this mismatch between the actual state and desired state.
3. **Reconcile:** The cluster automatically reconciled the state by scheduling and creating 1 brand new pod to bring the actual state back up to the desired state of 3 replicas.

**Q4. Why will you be able to scale the frontend without touching the database tier?**
Kubernetes applications use a decoupled, microservices architecture. Tiers communicate with each other through Services, which act as internal load balancers. Scaling the frontend merely adds more frontend Pods that utilize the same database Service. The database tier's configuration, storage, and operations remain completely independent.

**Q5. What is the difference between accessing a Pod directly via port-forward and accessing it through a Service? Why do Services matter?**
Using `port-forward` maps a local port directly to one specific pod, which is only useful for temporary debugging. Because pods are ephemeral and receive new IP addresses when recreated, direct connections will break. A Service provides a stable, persistent internal IP and DNS name that reliably routes traffic to the underlying pods, ensuring constant connectivity even as pods are destroyed and recreated.

**Q6. Explain why this same update-and-rollback would be much harder to do safely with Docker Compose alone.**
Docker Compose does not natively support zero-downtime rolling updates; updating an image typically requires stopping the old container before starting the new one, resulting in downtime. Kubernetes automates this by spinning up new Pods and gracefully terminating old ones one-by-one. Additionally, Kubernetes maintains a history of ReplicaSets, allowing for instant rollbacks to a previous healthy state with a single command.

**Q7. Explain why the frontend and API tiers use a Deployment while the database tier uses a StatefulSet.**
The frontend and API tiers are completely stateless; they don't store persistent local data, and any pod can be swapped for another instantly. Deployments are perfect for managing stateless replicas. The database tier is stateful; it requires persistent data storage (via a PersistentVolumeClaim), stable network identities, and strictly ordered startup/teardown processes. StatefulSets are specifically designed to provide these strict guarantees.

**Q8. Would this data have survived if postgres had instead been deployed as a plain Deployment without a PersistentVolumeClaim? Explain your reasoning.**
No, the data would have been permanently lost. A plain Deployment without a PersistentVolumeClaim writes data directly to the container's temporary internal filesystem. When the pod is deleted, the container and its ephemeral storage are completely destroyed. The PersistentVolumeClaim ensures data is written to an independent, persistent storage volume that outlives the lifecycle of any individual pod.

**Q9. What status did the broken pod show? Compare it against the lecture's Pod Status table - does it match one exactly, or is it related? Explain what it means.**
The status showed `ImagePullBackOff` (and `ErrImagePull` in the events). This is a sub-state directly related to the `Pending` status. It indicates that the `kubelet` failed to pull the requested container image from the registry (because the fake tag does not exist). Kubernetes places the pod in a "BackOff" state, meaning it will repeatedly delay and retry pulling the image, increasing the wait time between each failed attempt.