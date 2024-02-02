# Spike on evaluating GraphDB as a knowledge graph

## Install GraphDB

```sh
git clone https://github.com/Ontotext-AD/graphdb-helm && cd graphdb-helm
helm upgrade --install graphdb . --namespace graphdb --create-namespace  --set global.storageClass=default
```

## Access to the workbench
```sh
kubectl port-forward svc/graphdb-node 7200:7200 -n graphdb

# http://localhost:7200/
```

