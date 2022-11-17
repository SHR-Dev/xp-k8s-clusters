#!/bin/bash
kind delete cluster

kind create cluster

helm upgrade --install --wait mgmt mgmt-cluster/ 
python3 forward_ports.py &

# kubectl wait --for=condition=ready pod -l app=gitea
kubectl apply -f pipeline/Webhook_Listen.yaml
python3 preloader/app.py
