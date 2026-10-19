# Kubernetes AI Cluster Triage with K8sGPT and Ollama

An original local-first cluster-triage lab. It deploys Ollama inside a dedicated namespace and
configures K8sGPT to send anonymised Kubernetes diagnostic prompts to the local model endpoint.
It is intended for Kind, Minikube, or a non-production test cluster—not a production incident
response system.

## Prerequisites

- Kubernetes cluster and `kubectl`
- Helm 3
- At least 8 GB RAM available for the local model

## Deploy

```bash
kubectl apply -k k8s
kubectl -n ai-triage rollout status deployment/ollama
helm repo add k8sgpt https://charts.k8sgpt.ai/
helm upgrade --install k8sgpt k8sgpt/k8sgpt -n ai-triage -f helm/k8sgpt-values.yaml
```

## Run an analysis

```bash
kubectl -n ai-triage exec deploy/k8sgpt -- k8sgpt analyze --explain
```

Review generated output before applying any suggested remediation. This repository contains no
cluster credentials, model tokens, or production manifests.
Local AI-assisted Kubernetes diagnostics with K8sGPT and Ollama.
