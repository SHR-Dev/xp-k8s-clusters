#!/bin/bash
kind delete cluster
kind create cluster --config=kind.yml

helm upgrade --install --wait --namespace management --create-namespace argocd argo-cd --repo=https://argoproj.github.io/argo-helm --set configs.secret.argocdServerAdminPassword='$2y$10$ZgBRKmHYy4tPe5.iEHvX2u.oEZ4.Tnc4LfQPT25IU02Cstma8zcEy'
kubectl -n management apply -f mgmt-cluster/templates/vault_init.sh

kubectl -n management apply -f Argo-Apps/

kubectl -n management wait --for=jsonpath='{.status.health.status}'=Healthy Application -l management-app=Workflows --timeout=5m
kubectl -n management wait --for condition=established --timeout=5m crd/workflows.argoproj.io



kubectl -n management apply -f mgmt-cluster/templates/configure-workflow.yaml

kubectl -n management wait --for=jsonpath='{.status.phase}'=Completed Workflow -l configures=crossplane  --timeout=10m



# helm uninstall --namespace management argocd
