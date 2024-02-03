# Spike on evaluating GraphDB as a knowledge graph

## Install GraphDB

```sh
git clone https://github.com/Ontotext-AD/graphdb-helm && cd graphdb-helm
helm upgrade --install graphdb . --namespace graphdb --create-namespace  --set global.storageClass=default
```

In order to install GraphQL capabilities, you need to install `Semantic Objects` service:
```sh
kubectl apply -f ./install/SemanticObjects.yaml -n graphdb
``` 

and `WorkBench` service to play with GraphQL queries:

```sh
kubectl apply -f ./install/WorkBench.yaml -n graphdb
``` 


## Access to GraphDB
```sh
kubectl port-forward svc/graphdb-node 7200:7200 -n graphdb

# http://localhost:7200/
```

## Access to WorkBench
```sh
kubectl port-forward svc/workbench 3000:3000 -n graphdb

# http://localhost:3000/
```


