import pandas as pd
import os
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD, SKOS

# parameters and URLs
path = str(Path(os.path.abspath(os.getcwd())).parent.absolute())
print(path)
syUrls = path + "/Datasets/Computed/complete_dataset.csv"

# saving folder
savePath = path + "/Datasets/rdf/"


# Construct the SpotifyYoutubeStatistics ontology namespaces not known by RDFlib
SY = Namespace("http://www.dei.unipd.it/Database2/FRANGI/spotifyYoutubeStatistics/")

# create the graph
g = Graph()


# FRANCESCO
# Load the CSV files in memory
names = ["Url_spotify", "Artist"]
artists = pd.read_csv(syUrls, sep=",", index_col="Url_spotify", usecols=names)

artists.info()
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
names2 = {"Key": "key", "Duration_ms": "duration"}

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

names = ["track_album_id", "Album"]
albums = pd.read_csv(syUrls, sep=",", index_col="track_album_id", usecols=names)

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

names = ["track_album_id", "Album_type"]
joinAlbumAlbumtype = pd.read_csv(
    syUrls, sep=",", index_col="track_album_id", usecols=names
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


# ANDREA
# Load playlists and genres
names = ["playlist_name", "playlist_id", "playlist_genre", "playlist_subgenre", "Uri"]
csvData = pd.read_csv(syUrls, sep=",", usecols=names)
csvData.info()

# iterate over the csv data
for index, row in csvData.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the id as URI
    playlist = URIRef(SY[row["playlist_id"]])
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
                SY["playlist_id"],
                Literal(row["playlist_name"], datatype=XSD.string),
            )
        )

    if (genre, RDF.type, SY.Genre) not in g:
        g.add((genre, RDF.type, SY.Genre))
        g.add(
            (
                genre,
                SY["playlist_genre"],
                Literal(row["playlist_genre"], datatype=XSD.string),
            )
        )

    if (subgenre, RDF.type, SY.Genre) not in g:
        g.add((subgenre, RDF.type, SY.Genre))
        g.add(
            (
                subgenre,
                SY["playlist_subgenre"],
                Literal(row["playlist_subgenre"], datatype=XSD.string),
            )
        )

    # add edges triples (links between nodes)
    g.add((playlist, SY["hasGenre"], genre))
    g.add((playlist, SY["hasGenre"], subgenre))
    g.add((genre, SKOS.narrower, subgenre))  # SY['narrower']
    g.add((Song, SY["isPartOf"], playlist))


# GIANLUCA
# Load playlists and genres
names = [
    "Uri",
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
]


csvData = pd.read_csv(syUrls, sep=",", usecols=names)
csvData.info()


# iterate over the csv data
for index, row in csvData.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the id as URI
    if pd.isnull(row["Url_youtube"]):
        continue

    video = URIRef(SY[row["Url_youtube"].split("=")[-1]])
    channel = (
        URIRef(SY[str(row["channelId"])])
        if str(row["channelId"]) != ""
        and str(row["channelId"]) != "nan"
        and str(row["channelId"]) is not None
        else None
    )
    song = URIRef(SY[row["Uri"]])

    if (video, RDF.type, SY.Video) not in g:
        g.add((video, RDF.type, SY.YoutubeVideo))
        g.add(
            (
                video,
                SY["videoTitle"],
                Literal(row["Title"], datatype=XSD.string),
            )
        )
        if not pd.isnull(row["Views"]):
            g.add(
                (
                    video,
                    SY["views"],
                    Literal(int(row["Views"]), datatype=XSD.integer),
                )
            )
        if not pd.isnull(row["Likes"]):
            g.add(
                (
                    video,
                    SY["likes"],
                    Literal(int(row["Likes"]), datatype=XSD.integer),
                )
            )
        if not pd.isnull(row["Comments"]):
            g.add(
                (
                    video,
                    SY["comments"],
                    Literal(int(row["Comments"]), datatype=XSD.integer),
                )
            )
        g.add(
            (
                video,
                SY["description"],
                Literal(row["Description"], datatype=XSD.string),
            )
        )
        g.add(
            (
                video,
                SY["licensed"],
                Literal(row["Licensed"], datatype=XSD.boolean),
            )
        )
        g.add(
            (
                video,
                SY["officialVideo"],
                Literal(row["official_video"], datatype=XSD.boolean),
            )
        )

    # if the channel isn't already in the addedChannels list add it
    if channel is not None:
        if (channel, RDF.type, SY.YoutubeChannel) not in g:
            g.add((channel, RDF.type, SY.YoutubeChannel))

        g.add(
            (
                channel,
                SY["channelName"],
                Literal(row["Channel"], datatype=XSD.string),
            )
        )

    # add edges triples (links between nodes)
    g.add((video, SY["isVideoOf"], song))
    if channel is not None:
        g.add((video, SY["isUploadedBy"], channel))


# Bind the namespaces to a prefix for more readable output
g.bind("xsd", XSD)
g.bind("sy", SY)

# print all the data in the Turtle format
print("--- saving serialization ---")
with open(savePath + "syOn.ttl", "w", encoding="utf-8") as file:
    file.write(g.serialize(format="turtle"))
