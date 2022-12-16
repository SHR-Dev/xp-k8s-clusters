#!/bin/bash
kind delete cluster
kind create cluster --config=kind.yml

helm upgrade --install --wait --namespace management --create-namespace argocd argo-cd --repo=https://argoproj.github.io/argo-helm --set configs.secret.argocdServerAdminPassword='$2y$10$ZgBRKmHYy4tPe5.iEHvX2u.oEZ4.Tnc4LfQPT25IU02Cstma8zcEy'
kubectl -n management apply -f mgmt-cluster/templates/vault_init.sh

kubectl -n management apply -f Argo-Apps/

# helm uninstall --namespace management argocd
