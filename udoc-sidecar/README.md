# UDOC Sidecar
Container deployed alongside an AI/inference service in Kubernetes. Same governance call as
the agent, plus local mTLS termination + local queue buffering (replays to core on reconnect).
Spec §7: 2–4 vCPU, 4–8 GB per node. See k8s template in infra/k8s/.
