curl -L https://github.com/neo4j-labs/neosemantics/releases/download/5.17.0/neosemantics-5.17.0.jar > neosemantics-5.17.0.jar

docker build -t kaizentm/neo4j-neosemantics:5.17.0-2 . --platform=linux/amd64

docker push kaizentm/neo4j-neosemantics:5.17.0-2