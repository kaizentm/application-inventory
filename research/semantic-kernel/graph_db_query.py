import os
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Annotated
from semantic_kernel.functions import kernel_function


graphdb_repository = os.getenv("GRAPHDB_REPOSITORY")
sparql = SPARQLWrapper(graphdb_repository)


class GraphDBPlugin:

    @kernel_function(
        name="query_graphdb"
    )
    def query_graphdb(
        self,
        query: str,
    ) -> Annotated[str, "the output is a string"]:
        """Queries the graph database."""

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        ret = sparql.queryAndConvert()
        print(query)

        results = ret["results"]["bindings"] 
        # for r in results:
        #     print(r)
        return results    
