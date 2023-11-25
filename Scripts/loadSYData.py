# required libraries
import pandas as pd
import os
from pathlib import Path

# parameters and URLs
path = str(Path(os.path.abspath(os.getcwd())).parent.absolute())
print(path)
syUrls = path + "/Desktop/Datasets/Computed/complete_dataset.csv"

# saving folder
savePath = path + "/Desktop/Datasets/rdf/"

# Load the CSV files in memory
names = ["Url_spotify", "Artist"]
artists = pd.read_csv(syUrls, sep=",", index_col="Url_spotify", usecols=names)

artists.info()

# Load the required libraries
from rdflib import Graph, Literal, RDF, URIRef, Namespace

# rdflib knows about some namespaces, like FOAF
from rdflib.namespace import FOAF, XSD, SKOS

# Construct the SpotifyYoutubeStatistics ontology namespaces not known by RDFlib
SY = Namespace("http://www.dei.unipd.it/Database2/FRANGI/spotifyYoutubeStatistics/")

# create the graph
g = Graph()

# iterate over the artists dataframe
for index, row in artists.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the artist id as URI
    Artist = URIRef(SY[index])
    # Add triples using store's add() method.
    g.add((Artist, RDF.type, SY.Artist))
    g.add((Artist, SY["personName"], Literal(row["Artist"], datatype=XSD.string)))

names = [
    "Uri",
    "Track",
    "Danceability",
    "Energy",
    "Key",
    "Loudness",
    "Speechiness",
    "Acousticness",
    "Instrumentalness",
    "Liveness",
    "Valence",
    "Tempo",
    "Duration_ms",
    "Stream",
    "uStream"
]
songs = pd.read_csv(syUrls, sep=",", index_col="Uri", usecols=names)

songs.info()

songsDict = {}

names1 = {
    "Instrumentalness": "instrumentalness",
    "Danceability": "danceability",
    "Energy": "energy",
    "Loudness": "loudness",
    "Speechiness": "speechiness",
    "Acousticness": "acousticness",
    "Liveness": "liveness",
    "Valence": "valence",
}
names2 = {"Key": "key", "Duration_ms": "duration", "uStream": "stream"}

# iterate over the songs dataframe
for index, row in songs.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the movie id as URI
    Song = URIRef(SY[index])
    # Add triples using store's add() method.
    g.add((Song, RDF.type, SY.SpotifySong))
    g.add((Song, SY["trackName"], Literal(row["Track"], datatype=XSD.string)))

    for id in names1:
        if pd.isnull(row[id]) == False:
            g.add((Song, SY[names1[id]], Literal(float(row[id]), datatype=XSD.float)))

    for id in names2:
        if pd.isnull(row[id]) == False:
            g.add((Song, SY[names2[id]], Literal(int(row[id]), datatype=XSD.integer)))

"""

    # Add elements to the songsDict dictionary
    # the key is the song uri
    # the value is the greates stream value for the song.
    if pd.isnull(row["Stream"]) == False:
        if (index not in songsDict) or (
            (index in songsDict) and (int(row["Stream"]) > songsDict[index])
        ):
            songsDict[index] = int(row["Stream"])

# Add triples for song-stream join with add() method.
for index in songsDict:
    Song = URIRef(SY[index])

    g.add((Song, SY["stream"], Literal(songsDict[index], datatype=XSD.integer)))

"""

#names = ["track_album_id", "Album"]
#albums = pd.read_csv(syUrls, sep=",", index_col="track_album_id", usecols=names)

names = ["albumId", "Album"]
albums = pd.read_csv(syUrls, sep=",", index_col="albumId", usecols=names)

albums.info()

# iterate over the albums dataframe
for index, row in albums.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the album id as URI
    Album = URIRef(SY[index])
    # Add triples using store's add() method.

    if pd.isnull(index) == False:
        g.add((Album, RDF.type, SY.Album))
        g.add((Album, SY["albumName"], Literal(row["Album"], datatype=XSD.string)))

# Load video
names = [
    "Url_youtube",
    "Title",
    "Channel",
    "Views",
    "Likes",
    "Comments",
    "Description",
    "Licensed",
    "official_video",
    "channelId",
    "uViews",
    "uComments",
    "uLikes",
    "uOfficial_video"
]
videos = pd.read_csv(syUrls, sep=",", index_col="Url_youtube", usecols=names)

videos.info()

# iterate over the videos dataframe
for index, row in videos.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the album id as URI
    Video = URIRef(SY[str(index).split("=")[-1]])
    # Add triples using store's add() method.

    if pd.isnull(index) == False:
        g.add((Video, RDF.type, SY.YoutubeVideo))
        g.add((Video, SY["videoTitle"], Literal(row["Title"], datatype=XSD.string)))
#        if not pd.isnull(row["Views"]):
#            g.add((Video, SY["views"], Literal(int(row["Views"]), datatype=XSD.integer)))
        if not pd.isnull(row["uViews"]):
            g.add((Video, SY["views"], Literal(int(row["uViews"]), datatype=XSD.integer)))
#        if not pd.isnull(row["Likes"]):
#            g.add((Video, SY["likes"], Literal(int(row["Likes"]), datatype=XSD.integer)))
        if not pd.isnull(row["uLikes"]):
            g.add((Video, SY["likes"], Literal(int(row["uLikes"]), datatype=XSD.integer)))
#        if not pd.isnull(row["Comments"]):
#            g.add((Video, SY["comments"], Literal(int(row["Comments"]), datatype=XSD.integer)))
        if not pd.isnull(row["uComments"]):
            g.add((Video, SY["comments"], Literal(int(row["uComments"]), datatype=XSD.integer)))
        g.add((Video, SY["description"], Literal(row["Description"], datatype=XSD.string)))
        g.add((Video, SY["licensed"], Literal(row["Licensed"], datatype=XSD.boolean)))
#        g.add((Video, SY["officialVideo"], Literal(row["official_video"], datatype=XSD.boolean)))
        if not pd.isnull(row["uOfficial_video"]):
            g.add((Video, SY["officialVideo"], Literal(row["uOfficial_video"], datatype=XSD.boolean)))

# Load channels
names = [
    "Channel",
    "channelId"
]
channels = pd.read_csv(syUrls, sep=",", index_col="channelId", usecols=names)

channels.info()

# iterate over the videos dataframe
for index, row in channels.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the album id as URI
    Channel = URIRef(SY[index])
    # Add triples using store's add() method.

    if pd.isnull(index) == False:
        g.add((Channel, RDF.type, SY.YoutubeChannel))
        g.add((Channel, SY["channelName"], Literal(row["Channel"], datatype=XSD.string)))


names = ["Uri", "Url_spotify"]
joinArtistSong = pd.read_csv(
    syUrls,
    sep=",",
    index_col="Uri",
    keep_default_na=False,
    na_values=["_"],
    usecols=names,
)

for index, row in joinArtistSong.iterrows():
    # Create the node about the song
    # note that we do not add this resource to the database (created before)
    Song = URIRef(SY[index])

    # Create the node about the artist
    # note that we do not add this resource to the database (created before)
    Artist = URIRef(SY[row["Url_spotify"]])

    g.add((Artist, SY["published"], Song))
    g.add((Song, SY["isPublishedBy"], Artist))

#names = ["track_album_id", "Album_type"]
#joinAlbumAlbumtype = pd.read_csv(
#    syUrls, sep=",", index_col="track_album_id", usecols=names
#)

names = ["albumId", "Album_type"]
joinAlbumAlbumtype = pd.read_csv(
    syUrls, sep=",", index_col="albumId", usecols=names
)

for index, row in joinAlbumAlbumtype.iterrows():
    # Create the node about the song
    # note that we do not add this resource to the database (created before)
    Album = URIRef(SY[index])

    # Create the node about the artist
    # note that we do not add this resource to the database (created before)
    Albumtype = URIRef(SY[row["Album_type"]])

    if pd.isnull(index) == False:
        g.add((Album, SY["hasType"], Albumtype))

names = ["Url_youtube", "Uri"]
joinVideoSong = pd.read_csv(
    syUrls,
    sep=",",
    index_col="Url_youtube",
    keep_default_na=False,
    na_values=["_"],
    usecols=names,
)

for index, row in joinVideoSong.iterrows():
    
    if index == '':
        continue

    # Create the node about the video
    # note that we do not add this resource to the database (created before)
    Video = URIRef(SY[str(index).split("=")[-1]])

    # Create the node about the song
    # note that we do not add this resource to the database (created before)
    Song = URIRef(SY[row["Uri"]])

    g.add((Video, SY["isVideoOf"], Song))

names = ["Url_youtube", "channelId"]
joinVideoChannel = pd.read_csv(
    syUrls,
    sep=",",
    index_col="Url_youtube",
    keep_default_na=False,
    na_values=["_"],
    usecols=names,
)

for index, row in joinVideoChannel.iterrows():
    
    if index == '':
        continue

    # Create the node about the video
    # note that we do not add this resource to the database (created before)
    Video = URIRef(SY[str(index).split("=")[-1]])

    # Create the node about the channel
    # note that we do not add this resource to the database (created before)
    Channel = URIRef(SY[row["channelId"]])

    g.add((Video, SY["isUploadedBy"], Channel))

# ANDREA
# Load playlists and genres
names = ["playlist_id", "playlist_name", "playlist_id", "playlist_genre", "playlist_subgenre", "Uri"]
csvData = pd.read_csv(syUrls, sep=",", index_col="playlist_id" , usecols=names)
csvData.info()

# iterate over the csv data
for index, row in csvData.iterrows():

    if pd.isnull(index):
        continue

    # Create the node to add to the Graph
    # the node has the namespace + the id as URI
    playlist = URIRef(SY[index])
    genre = URIRef(SY[row["playlist_genre"]])
    Song = URIRef(SY[row["Uri"]])

    # remove spaces from subgenres
    formattedSubgenre = float("nan")
    if str(row["playlist_subgenre"]) != "nan":
        formattedSubgenre = row["playlist_subgenre"].replace(" ", "_")
    subgenre = URIRef(SY[formattedSubgenre])

    # Add nodes triples
    if (playlist, RDF.type, SY.SpotifyPlaylist) not in g:
        g.add((playlist, RDF.type, SY.SpotifyPlaylist))
        g.add(
            (
                playlist,
                SY["playlistName"],
                Literal(row["playlist_name"], datatype=XSD.string),
            )
        )

    if (genre, RDF.type, SY.Genre) not in g:
        g.add((genre, RDF.type, SY.Genre))
        g.add((genre, RDF.type, SKOS.Concept))

    if (subgenre, RDF.type, SY.Genre) not in g:
        g.add((subgenre, RDF.type, SY.Genre))
        g.add((subgenre, RDF.type, SKOS.Concept))

    # add edges triples (links between nodes)
    g.add((playlist, SY["hasGenre"], genre))
    g.add((playlist, SY["hasGenre"], subgenre))
    g.add((genre, SKOS.narrower, subgenre))  # SY['narrower']
    g.add((subgenre, SKOS.broader, genre))
    g.add((Song, SY["isPartOf"], playlist))

# Bind the namespaces to a prefix for more readable output
g.bind("xsd", XSD)
g.bind("sy", SY)

# print all the data in the Turtle format
print("--- saving serialization ---")
with open(savePath + "syOn.ttl", "w", encoding="utf-8") as file:
    file.write(g.serialize(format="turtle"))
