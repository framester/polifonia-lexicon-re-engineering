from SPARQLWrapper import SPARQLWrapper, JSON
from nltk.corpus import wordnet as wn


sparql_endpoint = "http://etna.istc.cnr.it/framester2/sparql"
sparql = SPARQLWrapper(sparql_endpoint)
sparql.setReturnFormat(JSON)

# Prepared SPARQL query with placeholders for parameters
sparql_query_template = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX fschema: <https://w3id.org/framester/schema/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT DISTINCT ?Synset
    WHERE {{
        {{
            ?Synset a <https://w3id.org/framester/wn/wn30/schema/NounSynset> .
            ?Synset rdfs:label ?label .
        }} UNION {{
            ?Synset a <https://w3id.org/framester/wn/wn30/schema/VerbSynset> .
            ?Synset rdfs:label ?label .
        }} UNION {{
            ?Synset a <https://w3id.org/framester/wn/wn30/schema/AdjectiveSynset> .
            ?Synset rdfs:label ?label .
        }} UNION {{
            ?Synset a <https://w3id.org/framester/wn/wn30/schema/AdverbSynset> .
            ?Synset rdfs:label ?label .
        }}
        FILTER(regex(?Synset, "(?i){name}") && regex(?Synset, "{pos}") && regex(?Synset, "{sense_number}") )
    }}
"""


def get_framester_uri_from_wn_synset_id(wn_synset_id):
    name, pos, sense_number = get_synset_from_wn_id(wn_synset_id)

    sparql_query = sparql_query_template.format(name=name, pos=pos, sense_number=sense_number)
    sparql.setQuery(sparql_query)

    results = sparql.query().convert()

    try:
        return results["results"]["bindings"][0]["Synset"].get("value", None)
    except (KeyError, IndexError):
        print(f"\nNo matching URI found for WordNet synset ID in Framester: {wn_synset_id} ({name=}, {pos=}, {sense_number=})")
        return None
    

def get_synset_from_wn_id(wn_synset_id):
    pos = wn_synset_id[-1]
    synset = wn.synset_from_pos_and_offset(wn_synset_id[-1], int(wn_synset_id[3:-1]))
    name = synset.name().split(".")[0]
    sense_number = synset.name().split(".")[-1]
    pos = resolve_pos_full_from_short(pos)
    return name, pos, int(sense_number)


def resolve_pos_full_from_short(pos_short):
    pos_short_to_pos_full = {
        "n": "noun",
        "v": "verb",
        "a": "adjective",
        "r": "adverb"
    }
    
    return pos_short_to_pos_full.get(pos_short, None)
