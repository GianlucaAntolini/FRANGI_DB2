# FRANGI_DB2

This project consists of creating a RDF graph that stores informations about viral Spotify songs and their Youtube Video (if it exists). We include also informations about the artists, the albums and the generes of the songs and also other useful informations.

We first designed and created the ontology for the data using Protegè, then we created the RDF graph using RDFlib library for Python and we eventually wrote some queries that retrieve some useful/interesting data and statistics from the database.

**Datasets**:

https://www.kaggle.com/datasets/salvatorerastelli/spotify-and-youtube

https://www.kaggle.com/datasets/sujaykapadnis/spotify-songs


**Info**

 - Steps/order to generate the data to be imported in GraphDB:  
      - run dataMergeScript.ipynb  
      - run loadSYData.ipynb  
 - As number of streams we took the maximum value when there were multiple values for the same video. We generated top level genres and subgenres by looking at the names of all the genres.  
 - The datasets (in the Datasets/Original folder) have been merged in a single file called complete_dataset.csv (in the Datasets/Computed folder). To create this file we created a script called dataMergeScript.ipynb in which we match the Spotify track ids of the songs and keep the information from both files.
 - Here are the paths of the main files:
      - The base ontology is under "Ontology/syOntololgy.ttl"
      - The computed turtle file with the data is under "Datasets/rdf/syOn.ttl"
      - The queries (with description and code) are under "Queries/SPARQL_queries.pdf"


**Diagram**

![alt text](https://github.com/GianlucaAntolini/FRANGI_DB2/blob/main/Ontology/syOntology.png)
   
 
**Queries**

The following are the queries that we decided to create:  
   1 - Top 10 songs by number of streams  
   2 - Song with max duration for each playlist, ordered by duration   
   3 - How many artists published n songs  
   4 - Artist that produced the most streams  
   5 - Top 10 channels by number of views, with also likes and comments    
   6 - Is the playlist with most songs the one with most streams?  
   /7 - Most common 5 genres among playlists  
   8 - Genre of top 5 playlists with most played songs      
   9 - Random pair of songs that have similar tempo and key (useful for djs)  
   /10 - Average number of views of songs for the 3 types of album types (single, compilation and album)  
   11 - Are number of streams of a song higher than the number of views of their related youtube video (in general)?  
   /12 - Average ratios of views/likes and views/comments of videos that are the official video of the songs and the ones that are not  
   13 - Top 10 artists by number of albums published  
   14 - Relation between YouTube video views and corresponding song  
   
   
   
**Validation**

In the Validation folder we created a text file of some SHACL shapes to validate the data and test that it is actually correctly uploaded.

