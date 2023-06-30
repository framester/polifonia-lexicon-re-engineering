# This script takes as input a csv file (corresponding to Polifonia Lexicon in a given language) and creates an RDF file in Turtle format.

# The csv file must contain the following columns:
# 1. BabelNet ID (e.g. bn:00000001n)
# 3. POS (e.g. n)
# 4. Gloss (e.g. the gloss of the lexicon entry)
# 5. Label (e.g. the lemma of the lexicon entry))

# The script takes also as input the language of the csv file (ITA, EN, ES, FR, DE, NL) and the nature of the lexicon entry
# (automatically inheritated from babelnet or manually added by Polifonia Internships).

# The script creates a RDF file in Turtle format, where each entry in the csv file is a sense of a
# lexical unit (i.e. a word). The sense is associated to the BabelNet ID, the lexical unit is associated
# to the WordNet ID. The sense and the lexical unit are connected through the property fs:isExpressedByLexicalUnit.

# The script uses the following namespaces:
# - BabelNet: http://babelnet.org/rdf/
# - Framester: https://w3id.org/framester/resource/polifonia/
# - Framester Schema: https://w3id.org/framester/schema/
# - RDF: http://www.w3.org/1999/02/22-rdf-syntax-ns#
# - RDFS: http://www.w3.org/2000/01/rdf-schema#

# The script uses the following classes and properties from the Framester Schema:
# - fs:Sense
# - fs:LexicalUnit
# - fs:containsSense
# - fs:isExpressedByLexicalUnit

# The script uses the following classes and properties from the RDF and RDFS namespaces:
# - rdf:type
# - rdfs:label
# - rdfs:comment

# The script uses the following classes and properties from the BabelNet namespace:
# - bn: (prefix for BabelNet IDs)

from rdflib import Graph, Literal, Namespace, RDF, URIRef
import pandas as pd
from tqdm import tqdm
import urllib

def create_rdf(input_file, output_file, lang, logic):
    # create namespaces for URIs
    n_babel = Namespace("http://babelnet.org/rdf/")
    n_polifonia = Namespace("https://w3id.org/framester/resource/polifonia/")

    # initialize an RDF Graph
    g = Graph()

    # define RDF and RDFS namespaces
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

    # define framester schema namespace
    fs = Namespace("https://w3id.org/framester/schema/")

    # Bind the namespace to a prefix
    g.bind("bn", n_babel)
    g.bind("fschema", fs)
    g.bind("rdf", rdf)
    g.bind("rdfs", rdfs)
    g.bind("polifonia", n_polifonia)  # Added this line

    # read the csv using pandas
    df = pd.read_csv(input_file, sep=',', header=0)

    # Create a progress bar with tqdm
    progress_bar = tqdm(total=len(df), desc='Processing rows', ncols=100)

    for index, row in df.iterrows():
        id = str(row['bn:id']).replace("bn:", "s")
        pos = str(row['pos'])
        description = str(row['definition'])
        label = str(row[f'lemmata {lang}'])

        # URL encode the label
        encoded_label = urllib.parse.quote(label)
        pos_encoded = urllib.parse.quote(pos)
        lang_encoded = urllib.parse.quote(lang)

        # create your resources and add them to the graph
        synset = URIRef(n_babel[id])

        if logic == 'automatic':
            sense = URIRef(n_babel[encoded_label + "_" + lang_encoded + "/" + id])
            lexical_unit = URIRef(n_babel[encoded_label + "_n_" + lang_encoded])
        elif logic == 'manual':
            sense = URIRef(n_polifonia[encoded_label + '_' + lang_encoded])
            lexical_unit = URIRef(n_polifonia[encoded_label + "_" + pos_encoded + "_" + lang_encoded])
        else:
            raise ValueError('Invalid logic. Choose either "automatic" or "manual".')

        g.add((synset, RDF.type, fs['Synset']))
        g.add((synset, rdfs.comment, Literal(description)))
        g.add((synset, fs['containsSense'], sense))

        g.add((sense, RDF.type, fs['Sense']))
        g.add((sense, rdfs.label, Literal(label)))
        g.add((sense, fs['isExpressedByLexicalUnit'], lexical_unit))

        g.add((lexical_unit, RDF.type, fs['LexicalUnit']))
        g.add((lexical_unit, rdfs.label, Literal(label)))

        # Update the progress bar
        progress_bar.update(1)

    # Save to an N-Triples file
    g.serialize(destination=output_file, format='turtle')

    # Close the progress bar
    progress_bar.close()


# define your list of tuples
rdf_args = [
    ('input/csv_for_rdf/manual_IT_filtered.csv', 'output/release_v0.2/output_IT_manual_turtle.ttl', 'IT', 'manual'),
    ('input/csv_for_rdf/manual_ES_filtered.csv', 'output/release_v0.2/output_ES_manual_turtle.ttl', 'ES', 'manual'),
    ('input/csv_for_rdf/manual_FR_filtered.csv', 'output/release_v0.2/output_FR_manual_turtle.ttl', 'FR', 'manual'),
    ('input/csv_for_rdf/manual_NL_filtered.csv', 'output/release_v0.2/output_NL_manual_turtle.ttl', 'NL', 'manual'),
    ('input/csv_for_rdf/automatic_IT_filtered.csv', 'output/release_v0.2/output_IT_automatic_turtle.ttl', 'IT', 'automatic'),
    ('input/csv_for_rdf/automatic_EN_filtered.csv', 'output/release_v0.2/output_EN_automatic_turtle.ttl', 'EN', 'automatic'),
    ('input/csv_for_rdf/automatic_ES_filtered.csv', 'output/release_v0.2/output_ES_automatic_turtle.ttl', 'ES', 'automatic'),
    ('input/csv_for_rdf/automatic_FR_filtered.csv', 'output/release_v0.2/output_FR_automatic_turtle.ttl', 'FR', 'automatic'),
    ('input/csv_for_rdf/automatic_DE_filtered_fixed.csv', 'output/release_v0.2/output_DE_automatic_turtle.ttl', 'DE', 'automatic'),
    ('input/csv_for_rdf/automatic_NL_filtered.csv', 'output/release_v0.2/output_NL_automatic_turtle.ttl', 'NL', 'automatic')
]

# iterate over the list of tuples, calling create_rdf() for each one
for args in rdf_args:
    create_rdf(*args)
