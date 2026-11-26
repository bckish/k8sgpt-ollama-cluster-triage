# Kubernetes AI Cluster Triage with K8sGPT and Ollama

An original local-first cluster-triage lab. It deploys Ollama inside a dedicated namespace and
configures K8sGPT to send anonymised Kubernetes diagnostic prompts to the local model endpoint.
It is intended for Kind, Minikube, or a non-production test cluster—not a production incident
response system.

## Prerequisites

- Kubernetes cluster and `kubectl`
- Helm 3
- At least 8 GB RAM available for the local model

## Verified read-only baseline

The deterministic baseline consumes Kubernetes EventList JSON and produces a categorized report without executing any commands or remediation. Unknown reasons are generalized; messages and object identifiers are not copied into the report. This baseline is not an LLM.

```bash
python3 -W error -m unittest -v
python3 triage.py fixtures/events.json
```

For an isolated local Kind namespace only, a read-only event export can be supplied as input:

```bash
kubectl --kubeconfig ./triage-local.kubeconfig -n YOUR_LOCAL_NAMESPACE get events -o json > local-events.json
python3 triage.py local-events.json
```

Do not commit raw event exports. Review all recommendations; no automatic cluster mutations are implemented.

Verified 26 November 2026: three strict unit tests passed, the synthetic fixture categorized three warnings correctly, and a read-only EventList from the disposable Java lab categorized two startup health warnings without exposing raw event text. Kustomize rendering passed.

## Optional K8sGPT/Ollama integration (not yet end-to-end verified)

```bash
kind create cluster --name triage-local --image kindest/node:v1.34.3 --kubeconfig ./triage-local.kubeconfig
kubectl --kubeconfig ./triage-local.kubeconfig apply -k k8s
kubectl --kubeconfig ./triage-local.kubeconfig -n ai-triage rollout status deployment/ollama
```

The inherited Helm values are an integration starting point, not a validated release. Review the official K8sGPT chart schema and least-privilege RBAC before installing it, and verify local model availability separately. This repository contains no cluster credentials, model tokens, or production manifests. Delete only the disposable cluster when done.
