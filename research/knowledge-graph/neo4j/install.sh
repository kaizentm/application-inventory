#!/bin/bash

helm repo add neo4j https://helm.neo4j.com/neo4j
helm repo update

helm upgrade --install neo4j neo4j/neo4j --namespace neo4j -f neo4j-helm-values.yaml --create-namespace  
