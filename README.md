# FRANGI_DB2

This project consists of creating a RDF graph that stores informations about viral Spotify songs and their Youtube Video (if it exists). We include also informations about the artists, the albums and the generes of the songs and also other useful informations.

We first designed and created the ontology for the data using Protegè, then we created the RDF graph using RDFlib library for Python and we eventually wrote some queries that retrieve some useful/interesting data and statistics from the database.

The following are the queries that we decided to create:
...
Francesco:
 1 - Top 10 song by number of streams
 2 - Song with max duration for each playlist, ordered by duration
 3 - Artist that wrote more songs
 4 - Artist that produced the most streams

Andrea:
 1 - First 10 channels by number of views, with also likes and comments
 2 - The playlist with most song is the one with most streams?
 3 - Correspondence between artist and genre (by number of songs in a playlist of such genre)
 4 - Top genre based on something (genres of playlists with most played songs or most common genre among playlists)

Gianluca:
 1 - Random pair of songs that have similar tempo and key (useful for djs)
 2 - Average number of views of songs for the 3 types of Album types
 3 - Are n of streams of a song higher than the n of views of their related yt video (in general)?
 4 - Average ratios of Views/Likes and Views/Comments of licensed and unlicensed YoutubeVideos
 5 - Top 10 YoutubeChannel by average of views on the YoutubeVideos they uploaded, with total n of views, likes, comments, and streams of the corresponding SpotifySongs

Insieme:
 1 - Relazione tra visualizzazioni di un video e ascolti della corrispondente canzone su Spotify
...



Datasets:

https://www.kaggle.com/datasets/salvatorerastelli/spotify-and-youtube

https://www.kaggle.com/datasets/sujaykapadnis/spotify-songs

The datasets (in the Datasets/Original folder) have been merged in a single file called complete_dataset.csv (in the Datasets/Computed folder). To create this file we created a python script called dataMergeScript.py in which we match the Spotify track ids of the songs and keep the information from both files.



Info:

 - As number of streams we took the maximum value when there were multiple values for the same video
 - We still have to choose if we will take the union or the intersection of the datasets (probably union)
