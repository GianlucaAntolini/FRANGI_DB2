# required libraries
import pandas as pd
import os
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD, SKOS

# paths
path = str(Path(os.path.abspath(os.getcwd())).parent.absolute())
datasetCSV = path + "/Datasets/Computed/complete_dataset.csv"
savePath = path + "/Datasets/rdf/"

# Construct the SpotifyYoutubeStatistics ontology namespaces not known by RDFlib
SY = Namespace("http://www.dei.unipd.it/Database2/FRANGI/spotifyYoutubeStatistics/")

# create the graph
g = Graph()

# Load artists
data = pd.read_csv(datasetCSV, sep=",")

floatProps = {"Instrumentalness": "instrumentalness", "Danceability": "danceability", "Energy": "energy",
              "Loudness": "loudness", "Speechiness": "speechiness", "Acousticness": "acousticness",
              "Liveness": "liveness", "Tempo": "tempo", "Valence": "valence"}
intProps = {"Key": "key", "Duration_ms": "duration", "uStream": "stream"}

for index, row in data.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the artist id as URI
    Artist = None if pd.isnull(row["Url_spotify"]) else URIRef(SY[row["Url_spotify"]])
    Song = None if pd.isnull(row["Uri"]) else URIRef(SY[row["Uri"]])
    Album = None if pd.isnull(row["albumId"]) else URIRef(SY[row["albumId"]])
    Video = None if pd.isnull(row["Url_youtube"]) else URIRef(SY[str(row["Url_youtube"]).split("=")[-1]])
    Channel = None if pd.isnull(row["channelId"]) else URIRef(SY[row["channelId"]])
    Playlist = None if pd.isnull(row["playlist_id"]) else URIRef(row["playlist_id"])
    Genre = None if pd.isnull(row["playlist_genre"]) else URIRef(SY[row["playlist_genre"]])

    # remove spaces from subgenres
    formattedSubgenre = float("nan")
    if str(row["playlist_subgenre"]) != "nan":
        formattedSubgenre = row["playlist_subgenre"].replace(" ", "_")
    Subgenre = None if pd.isnull(row["playlist_subgenre"]) else URIRef(SY[formattedSubgenre])

    # add Artist
    if (Artist, RDF.type, SY.Artist) not in g and not pd.isnull(row["Url_spotify"]):
        g.add((Artist, RDF.type, SY.Artist))
        g.add((Artist, SY["personName"], Literal(row["Artist"], datatype=XSD.string)))

    # add Song
    if (Song, RDF.type, SY.SpotifySong) not in g and not pd.isnull(row["Uri"]):
        g.add((Song, RDF.type, SY.SpotifySong))
        g.add((Song, SY["trackName"], Literal(row["Track"], datatype=XSD.string)))

        for n in floatProps:
            if not pd.isnull(row[n]):
                g.add((Song, SY[floatProps[n]], Literal(float(row[n]), datatype=XSD.float)))

        for n in intProps:
            if not pd.isnull(row[n]):
                g.add((Song, SY[intProps[n]], Literal(int(row[n]), datatype=XSD.integer)))

    # add Album
    if (Album, RDF.type, SY.Album) not in g and not pd.isnull(row["albumId"]):
        g.add((Album, RDF.type, SY.Album))
        g.add((Album, SY["albumName"], Literal(row["Album"], datatype=XSD.string)))
        g.add((Album, SY["albumType"], Literal(row["Album_type"], datatype=XSD.string)))

    # add Video
    if (Video, RDF.type, SY.YoutubeVideo) not in g and not pd.isnull(row["Url_youtube"]):
        g.add((Video, RDF.type, SY.YoutubeVideo))
        g.add((Video, SY["videoTitle"], Literal(row["Title"], datatype=XSD.string)))

        if not pd.isnull(row["uViews"]):
            g.add((Video, SY["views"], Literal(int(row["uViews"]), datatype=XSD.integer)))

        if not pd.isnull(row["uLikes"]):
            g.add((Video, SY["likes"], Literal(int(row["uLikes"]), datatype=XSD.integer)))

        if not pd.isnull(row["uComments"]):
            g.add((Video, SY["comments"], Literal(int(row["uComments"]), datatype=XSD.integer)))

        g.add((Video, SY["description"], Literal(row["Description"], datatype=XSD.string)))
        g.add((Video, SY["licensed"], Literal(row["Licensed"], datatype=XSD.boolean)))

        if not pd.isnull(row["uOfficial_video"]):
            g.add((Video, SY["officialVideo"], Literal(row["uOfficial_video"], datatype=XSD.boolean)))

    # add Channel
    if (Channel, RDF.type, SY.YoutubeChannel) not in g and not pd.isnull(index):
        g.add((Channel, RDF.type, SY.YoutubeChannel))
        g.add((Channel, SY["channelName"], Literal(row["Channel"], datatype=XSD.string)))

    # add Album-Song edges
    if (Album, SY["isComposed"], Song) not in g and not pd.isnull(row["albumId"]) and not pd.isnull(row["Uri"]):
        g.add((Album, SY["isComposed"], Song))
        g.add((Song, SY["belongsTo"], Album))

    # add Song-Artist edges
    if (Artist, SY["published"], Song) not in g and not pd.isnull(row["Uri"]) and not pd.isnull(row["Url_spotify"]):
        g.add((Artist, SY["published"], Song))
        g.add((Song, SY["isPublishedBy"], Artist))

    # add Video-Song edges
    if (Video, SY["isVideoOf"], Song) not in g and not pd.isnull(row["Uri"]) and not pd.isnull(row["Url_youtube"]):
        g.add((Video, SY["isVideoOf"], Song))

    # add Video-Channel edges
    if (Video, SY["isUploadedBy"], Channel) not in g \
            and not pd.isnull(row["channelId"]) and not pd.isnull(row["Url_youtube"]):
        g.add((Video, SY["isUploadedBy"], Channel))
        g.add((Channel, SY["upload"], Video))

    # add Playlists
    if (Playlist, RDF.type, SY.SpotifyPlaylist) not in g and not pd.isnull(row["playlist_id"]):
        g.add((Playlist, RDF.type, SY.SpotifyPlaylist))
        g.add((Playlist, SY["playlistName"], Literal(row["playlist_name"], datatype=XSD.string)))

    # add Genres
    if (Genre, RDF.type, SY.Genre) not in g and not pd.isnull(row["playlist_genre"]):
        g.add((Genre, RDF.type, SY.Genre))
        g.add((Genre, RDF.type, SKOS.Concept))
        g.add((Genre, SY["genreName"], Literal(row["playlist_genre"], datatype=XSD.string)))

    # add Subgenres
    if (Subgenre, RDF.type, SY.Genre) not in g and not pd.isnull(row["playlist_subgenre"]):
        g.add((Subgenre, RDF.type, SY.Genre))
        g.add((Subgenre, RDF.type, SKOS.Concept))
        g.add((Subgenre, SY["genreName"], Literal(formattedSubgenre, datatype=XSD.string)))

    # add Playlist-Genre edges
    if (Playlist, SY["hasGenre"], Genre) not in g \
            and not pd.isnull(row["playlist_id"]) and not pd.isnull(row["playlist_genre"]):
        g.add((Playlist, SY["hasGenre"], Genre))

    # add Playlist-Subgenre edges
    if (Playlist, SY["hasGenre"], Subgenre) not in g \
            and not pd.isnull(row["playlist_id"]) and not pd.isnull(row["playlist_subgenre"]):
        g.add((Playlist, SY["hasGenre"], Subgenre))

    # add Genre-Subgenre edges
    if (Genre, SKOS.narrower, Subgenre) not in g \
            and not pd.isnull(row["playlist_subgenre"]) and not pd.isnull(row["playlist_genre"]):
        g.add((Genre, SKOS.narrower, Subgenre))
        g.add((Subgenre, SKOS.broader, Genre))

    # add Song-Playlist edges
    if (Song, SY["isPartOf"], Playlist) not in g and not pd.isnull(row["playlist_id"]) and not pd.isnull(row["Uri"]):
        g.add((Song, SY["isPartOf"], Playlist))

# Bind the namespaces to a prefix for more readable output
g.bind("xsd", XSD)
g.bind("sy", SY)

# print all the data in the Turtle format
print("--- saving serialization ---")
with open(savePath + "syOn1.ttl", "w", encoding="utf-8") as file:
    file.write(g.serialize(format="turtle"))
