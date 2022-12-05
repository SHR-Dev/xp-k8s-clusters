#!/bin/bash
kind delete cluster

kind create cluster --config=kind.yml

kubectl create ns nginx-system
kubectl kustomize --enable-helm kustomization/ | kubectl apply -f -

helm upgrade --install --wait mgmt mgmt-cluster/ --timeout 15m0s
