#!/bin/bash

kubectl apply -f k8s/firewall-deployment.yaml
kubectl apply -f k8s/monitor-deployment.yaml
kubectl apply -f k8s/switch-deployment.yaml
