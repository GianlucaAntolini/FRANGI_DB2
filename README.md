# FRANGI_DB2

This project consists of creating a RDF graph that stores informations about viral Spotify songs and their Youtube Video (if it exists). We include also informations about the artists, the albums and the generes of the songs and also other useful informations.

We first designed and created the ontology for the data using Protegè, then we created the RDF graph using RDFlib library for Python and we eventually wrote some queries that retrieve some useful/interesting data and statistics from the database.

The following are the queries that we decided to create:
...
TODO
...



Datasets:

https://www.kaggle.com/datasets/salvatorerastelli/spotify-and-youtube

https://www.kaggle.com/datasets/sujaykapadnis/spotify-songs

The datasets (in the Datasets/Original folder) have been merged in a single file called complete_dataset.csv (in the Datasets/Computed folder). To create this file we created a python script called dataMergeScript.py in which we match the Spotify track ids of the songs and keep the information from both files.



