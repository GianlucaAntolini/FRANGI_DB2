import pandas as pd
import os
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD, SKOS

# path to csv and path of saving folder
path = str(Path(os.path.abspath(os.getcwd())).parent.absolute())
syUrls = path + "/Datasets/Computed/complete_dataset.csv"
savePath = path + "/Datasets/rdf/"

# Construct the SpotifyYoutubeStatistics ontology namespaces not known by RDFlib
SY = Namespace("http://www.dei.unipd.it/Database2/FRANGI/spotifyYoutubeStatistics/")

# create the graph
g = Graph()

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

# Bind the namespaces to a prefix for more readable output
g.bind("xsd", XSD)
g.bind("sy", SY)

# print all the data in the Turtle format
print("--- saving serialization ---")
with open(savePath + "Playlists_Genres.ttl", "w+", encoding="utf-8") as file:
    file.write(g.serialize(format="turtle"))
