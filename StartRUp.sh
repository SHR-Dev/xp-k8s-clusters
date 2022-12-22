#!/bin/bash
kind delete cluster
kind create cluster # --config=kind.yml

k="kubectl -n management "

helm upgrade --install --wait \
    --namespace management --create-namespace \
    argocd argo-cd \
    --repo=https://argoproj.github.io/argo-helm \
    --set configs.secret.argocdServerAdminPassword='$2y$10$ZgBRKmHYy4tPe5.iEHvX2u.oEZ4.Tnc4LfQPT25IU02Cstma8zcEy'

${k} apply -f resources/vault_init.sh

${k} apply -f Argo-Apps/

${k} wait --timeout=5m \
    --for=jsonpath='{.status.health.status}'=Healthy \
    Application -l management-app=Workflows 
${k} wait --timeout=5m\
    --for condition=established  \
    crd/workflows.argoproj.io



${k} apply \
    -f resources/configure-workflow.yaml

${k} wait --timeout=5m \
    --for=jsonpath='{.status.phase}'=Succeeded \
    Workflow -l configures=crossplane  


${k} apply -f resources/provider-config.yml
# helm uninstall --namespace management argocd
