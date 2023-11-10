# required libraries
import pandas as pd
import os
from pathlib import Path

# parameters and URLs
path = str(Path(os.path.abspath(os.getcwd())).parent.absolute())
syUrls = path + '/Desktop/Datasets/Computed/complete_dataset.csv'

# saving folder
savePath =  path + '/Desktop/Datasets/rdf/'

# Load the CSV files in memory
names = ['Url_spotify','Artist']
artists = pd.read_csv(syUrls, sep=',', index_col='Url_spotify', usecols=names)

artists.info()

# Load the required libraries
from rdflib import Graph, Literal, RDF, URIRef, Namespace
# rdflib knows about some namespaces, like FOAF
from rdflib.namespace import FOAF, XSD

# Construct the SpotifyYoutubeStatistics ontology namespaces not known by RDFlib
SY = Namespace("http://www.dei.unipd.it/Database2/FRANGI/spotifyYoutubeStatistics/")

# create the graph
g = Graph()

#iterate over the artists dataframe
for index, row in artists.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the artist id as URI
    Artist = URIRef(SY[index])
    # Add triples using store's add() method.
    g.add((Artist, RDF.type, SY.Artist))
    g.add((Artist, SY['personName'], Literal(row['Artist'], datatype=XSD.string)))

names = ['Uri','Track','Danceability','Energy','Key','Loudness','Speechiness','Acousticness','Instrumentalness','Liveness','Valence','Tempo','Duration_ms','Stream']
songs = pd.read_csv(syUrls, sep=',', index_col='Uri', usecols=names)

songs.info()

songsDict = {}

names1 = {'Instrumentalness':'instrumentalness','Danceability':'danceability','Energy':'energy','Loudness':'loudness','Speechiness':'speechiness','Acousticness':'acousticness','Liveness':'liveness','Valence':'valence'}
names2 = {'Key':'key','Duration_ms':'duration'}

#iterate over the songs dataframe
for index, row in songs.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the movie id as URI
    Song = URIRef(SY[index])
    # Add triples using store's add() method.
    g.add((Song, RDF.type, SY.SpotifySong))
    g.add((Song, SY['trackName'], Literal(row['Track'], datatype=XSD.string)))

    for id in names1:
        if pd.isnull(row[id]) == False:
            g.add((Song, SY[names1[id]], Literal(float(row[id]), datatype=XSD.float)))

    for id in names2:
        if pd.isnull(row[id]) == False:
            g.add((Song, SY[names2[id]], Literal(int(row[id]), datatype=XSD.integer)))

    # Add elements to the songsDict dictionary
    # the key is the song uri
    # the value is the greates stream value for the song.
    if pd.isnull(row['Stream']) == False:
        if (index not in songsDict) or ((index in songsDict) and (int(row['Stream']) > songsDict[index])):
            songsDict[index] = int(row['Stream'])

# Add triples for song-stream join with add() method.
for index in songsDict:
    Song = URIRef(SY[index])

    g.add((Song, SY['stream'], Literal(songsDict[index], datatype=XSD.integer)))

names = ['track_album_id','Album']
albums = pd.read_csv(syUrls, sep=',', index_col='track_album_id', usecols=names)

albums.info()

#iterate over the albums dataframe
for index, row in albums.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the album id as URI
    Album = URIRef(SY[index])
    # Add triples using store's add() method.

    if pd.isnull(index) == False:
        g.add((Album, RDF.type, SY.Album))
        g.add((Album, SY['albumName'], Literal(row['Album'], datatype=XSD.string)))

names = ['Uri','Url_spotify']
joinArtistSong = pd.read_csv(syUrls, sep=',', index_col='Uri', keep_default_na=False, na_values=['_'], usecols=names)

for index, row in joinArtistSong.iterrows():
    # Create the node about the song
    # note that we do not add this resource to the database (created before)
    Song = URIRef(SY[index])
    
    # Create the node about the artist
    # note that we do not add this resource to the database (created before)
    Artist = URIRef(SY[row['Url_spotify']])

    g.add((Artist, SY['published'], Song))
    g.add((Song, SY['isPublishedBy'], Artist))

names = ['track_album_id','Album_type']
joinAlbumAlbumtype = pd.read_csv(syUrls, sep=',', index_col='track_album_id', usecols=names)

for index, row in joinAlbumAlbumtype.iterrows():
    # Create the node about the song
    # note that we do not add this resource to the database (created before)
    Album = URIRef(SY[index])
    
    # Create the node about the artist
    # note that we do not add this resource to the database (created before)
    Albumtype = URIRef(SY[row['Album_type']])

    if pd.isnull(index) == False:
        g.add((Album, SY['hasType'], Albumtype))


# Bind the namespaces to a prefix for more readable output
g.bind("xsd", XSD)
g.bind("sy", SY)

# print all the data in the Turtle format
print("--- saving serialization ---")
with open(savePath + 'syOn.ttl', 'w', encoding= 'utf-8') as file:
    file.write(g.serialize(format='turtle'))