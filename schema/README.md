# Schema of polifonia-lexicon-re-engineering

# OWL version

This OWL ontology is derived from the re-engineered Polifonia Lexicon's triples stored in the dedicated RDF files (releases [here](https://github.com/framester/polifonia-lexicon-re-engineering/blob/main/schema/pl_EN_ont.owl)). Below, the prefixes used:

- `bn:`: BabelNet (http://babelnet.org/rdf/)
- `fschema:`: Framester schema (https://w3id.org/framester/schema/)
- `rdfs:`: RDF Schema (http://www.w3.org/2000/01/rdf-schema#)
- `polifonia:`: Polifonia (https://w3id.org/framester/resource/polifonia/)
- `wn:`: WordNet Framester (https://w3id.org/framester/wn/wn30/)

## Classes

The ontology includes the following classes:

- `fschema:Synset`: A set of synonymous words or phrases.
- `fschema:Sense`: A specific meaning for a word or phrase.
- `fschema:LexicalUnit`: A unit of lexical meaning.

## Properties

The ontology includes the following properties:

- `rdfs:comment`: A description of the resource.
- `rdfs:label`: A human-readable label for the resource.
- `fschema:containsSense`: Relates a Synset to a Sense it contains. It is an object property.
- `fschema:isExpressedByLexicalUnit`: Relates a Sense to a LexicalUnit that expresses it. It is an object property.

Inverse properties:

- `fschema:senseContainedIn`: Inverse of `fschema:containsSense`.
- `fschema:expressesSense`: Inverse of `fschema:isExpressedByLexicalUnit`.

The ontology is serialized in the RDF/XML format, which can be loaded into ontology editors like Protégé for further manipulation or visualization.

# Diagram Version
- This section contains the schema of the re-engineered Polifonia Lexicon.
  

    - Below is the schema that reports classes and properties only. Inverse properties are explicited.
![schemaUltraAbstract](https://github.com/framester/polifonia-lexicon-re-engineering/blob/main/schema/polifonia_lexicon_reengineering_ultraAbstractSchema.png)

    - Below is the schema that reports classes, properties and examples of automatically imported individuals. Inverse properties are not reported.

![schemaWithExampleIndividualsAutomatic](https://github.com/framester/polifonia-lexicon-re-engineering/blob/main/schema/polifonia_lexicon_reengineering_Schema_wExampleIndividuals_AutomaticConcepts.jpg)

  - Below is the schema that reports classes, properties and examples of manually added individuals (lexicalizations/translations added by Polifonia internships). Inverse properties are not reported.

![schemaWithExampleIndividualsManual](https://github.com/framester/polifonia-lexicon-re-engineering/blob/main/schema/polifonia_lexicon_reengineering_Schema_wExamples_ManualConcepts.jpg)
