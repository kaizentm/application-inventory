FROM neo4j:5.17.0

# copy my-plugins into the Docker image
COPY neosemantics-5.17.0.jar /var/lib/neo4j/plugins/

# # install the apoc core plugin that is shipped with Neo4j
# RUN cp /var/lib/neo4j/labs/apoc-* /var/lib/neo4j/plugins