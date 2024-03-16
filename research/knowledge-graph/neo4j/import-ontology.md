CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource)
REQUIRE r.uri IS UNIQUE


CALL n10s.graphconfig.init({handleVocabUris: 'MAP', handleRDFTypes: "LABELS_AND_NODES" , keepLangTag: true})



CALL n10s.onto.import.inline(
  '
@prefix : <http://application-inventory/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://application-inventory/> .
@prefix prov: <http://www.w3.org/ns/prov#> .

<http://application-inventory> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://application-inventory#exposedTo
:exposedTo rdf:type owl:ObjectProperty ;
           owl:inverseOf :exposedIn ;
           rdfs:domain :Package ;
           rdfs:range :Vulnerability .


###  http://application-inventory/deployedTo
:deployedTo rdf:type owl:ObjectProperty ;
            rdfs:domain :Application ;
            rdfs:range :Host .

###  http://application-inventory/exposedIn
:exposedIn rdf:type owl:ObjectProperty ;
           rdfs:domain :Vulnerability ;
           rdfs:range :Package .


###  http://application-inventory/includedIn
:includedIn rdf:type owl:ObjectProperty ;
            owl:inverseOf :includes ;
            rdfs:domain :Package ;
            rdfs:range :Application .


###  http://application-inventory/includes
:includes rdf:type owl:ObjectProperty ;
          rdfs:domain :Application ;
          rdfs:range :Package .


#################################################################
#    Data properties
#################################################################

###  http://application-inventory/deployedOn
:deployedOn rdf:type owl:DatatypeProperty ,
                     owl:FunctionalProperty ;            
            rdfs:range xsd:dateTime .


###  http://application-inventory/description
:description rdf:type owl:DatatypeProperty ,
                      owl:FunctionalProperty ;
             rdfs:domain :Thing ; 
             rdfs:range xsd:string .

###  http://application-inventory/version
:version rdf:type owl:DatatypeProperty ,
                  owl:FunctionalProperty ;
          rdfs:domain :Package ;
          rdfs:range xsd:string .

###  http://application-inventory/name
:name rdf:type owl:DatatypeProperty ,
               owl:FunctionalProperty ;
      rdfs:domain :Thing ;                                    
      rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://application-inventory/Vulnerable
:Vulnerable owl:equivalentClass [
    owl:unionOf  ( 
                  [rdf:type owl:Restriction ;
                  owl:onProperty :exposedTo ;
                  owl:someValuesFrom :Vulnerability]

                  [rdf:type owl:Restriction ;
                  owl:onProperty :includes ;
                  owl:someValuesFrom :Vulnerable]
    ) 
];
rdfs:subClassOf :Thing .


###  http://application-inventory/Application
:Application rdf:type owl:Class;
             rdfs:subClassOf :Thing .


###  http://application-inventory/Host
:Host rdf:type owl:Class;
      rdfs:subClassOf :Thing .


###  http://application-inventory/Package
:Package rdf:type owl:Class;
         rdfs:subClassOf :Thing .


###  http://application-inventory/Vulnerability
:Vulnerability rdf:type owl:Class ;
               rdfs:subClassOf prov:Entity ;
               prov:wasGeneratedBy  :VulnerabilityReportingActivity .

:VulnerabilityReportingActivity rdf:type owl:Class ;
                                rdfs:subClassOf prov:Activity; 
                                prov:wasAssociatedWith :SecurityAgent;
                                prov:used  :VulnerabilityScanningResults .

:SecurityAgent rdf:type owl:Class ;                            
               rdfs:subClassOf prov:Agent .      

:VulnerabilityScanningResults rdf:type owl:Class ;                            
                              rdfs:subClassOf prov:Entity .

:Thing rdf:type owl:Class .

',
  'Turtle'
)                              

# ^ Lost information about what Vulnerable is 
# Looks like inferencing should be implemented manually (e.g. invoke a list of predefined or custom procedures, or use procedures in Cypher queries) -> research
    So the inference logic goes back from the graph to the code