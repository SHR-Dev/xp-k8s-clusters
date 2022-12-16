#!/bin/bash
kind delete cluster
kind create cluster #--config=kind.yml

helm install --wait --namespace management --create-namespace argocd argo-cd --repo=https://argoproj.github.io/argo-helm
kubectl -n management apply -f mgmt-cluster/templates/vault_init.sh

kubectl -n management apply -f Argo-Apps/
