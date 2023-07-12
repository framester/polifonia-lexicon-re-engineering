from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, OWL
from glob import glob
from tqdm import tqdm

# Define namespaces
bn = Namespace("http://babelnet.org/rdf/")
fschema = Namespace("https://w3id.org/framester/schema/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
polifonia = Namespace("https://w3id.org/framester/resource/polifonia/")
wn = Namespace("https://w3id.org/framester/wn/wn30/")

# Create a graph
g = Graph()

# Bind the namespaces to the graph
g.bind("bn", bn)
g.bind("fschema", fschema)
g.bind("rdfs", rdfs)
g.bind("polifonia", polifonia)
g.bind("wn", wn)

ontology_iri = URIRef("https://w3id.org/framester/PolifoniaLexicon/schema/")
#version_iri = URIRef("http://example.com/myOntology/1.0")

g.add((ontology_iri, RDF.type, OWL.Ontology))
g.add((ontology_iri, OWL.versionIRI, version_iri))

# Declare 'containsSense' and 'isExpressedByLexicalUnit' as object properties
g.add((fschema.containsSense, RDF.type, OWL.ObjectProperty))
g.add((fschema.isExpressedByLexicalUnit, RDF.type, OWL.ObjectProperty))

# Declare inverse properties
g.add((fschema.containsSense, OWL.inverseOf, fschema.senseContainedIn))
g.add((fschema.isExpressedByLexicalUnit, OWL.inverseOf, fschema.expressesSense))

# List of Turtle files
all_turtle_files = glob("output/release_v0.3/*.ttl")

# Filter the list to include only files with '_EN_' in the filename
turtle_files = [file for file in all_turtle_files if '_EN_' in file]
#turtle_files = [file for file in all_turtle_files if ('_IT_' in file) or ('_EN_' in file) or ('_DE_' in file)]

# Load the triples from the Turtle files
for file in tqdm(turtle_files, desc="Loading files"):
    g.parse(file, format='turtle')

# Serialize the graph in the OWL (RDF/XML) format
owl_data = g.serialize(format='pretty-xml')

# Save the OWL data to a file
with open('schema/pl_EN_ont.owl', 'w') as f:
    f.write(owl_data)
