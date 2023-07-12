# polifonia-lexicon-re-engineering
This repository collects the outcomes of the effort for re-engineering Polifonia Lexicon and adding it to Framester.

# Polifonia Lexicon Re-engineering for enriching Framester

This repository contains the code and output produced to re-engineer the Polifonia Lexicon and prepare it for import into Framester in RDF format.

## Repository Structure

The repository is structured as follows:

- `input/`: This folder contains the input data required for the lexicon re-engineering process. It includes the following subfolders:
  - `excel/`: Contains the lexicon excel files on which the annotators worked. The 'initial' ones are the ones before the work of the annotators began. The 'final' ones are the ones after the work of annotators ended.
  - `csv_to_compare/`: Contains the CSV files extrapolated from the excel and used for comparing the initial and final versions of the lexicon, to separate the lexicon entries. They are created using 'data_preparation.py'.
  - `csv_for_rdf/`: Contains the CSV files generated from the Polifonia Lexicon, which are then transformed into RDF following Framester's schema. They are created using 'data_preparation.py'.

- `output/`: This folder contains the output generated by the re-engineering process. It includes the following subfolder:
  - `rdf/`: Contains the RDF files generated from the CSVs using the `lexicon_to_framester.py` script.

- `schema/`: This folder contains the project (.drawio file) for manipulating the graphical diagrams of the re-engineered Polifonia Lexicon's schema and the OWL ontology file(s) derived from the re-engineered Polifonia Lexicon's RDFs.

- `script/`: This folder contains the scripts required for the re-engineering process. It includes the following files:
  - `data_preparation.py`: A script for transforming the Polifonia Lexicon files into CSV format.
  - `lexicon_to_framester.py`: A script for converting the CSVs created from the Polifonia Lexicon into RDF data according to the Framester schema.
  - `lexicon_kg_to_onto.py`: A script for converting Polifonia Lexicon's RDF files into an OWL ontology ready to be imported in Protegé for further elaboration.
