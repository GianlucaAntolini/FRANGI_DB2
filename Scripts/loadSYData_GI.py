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

addedChannels = []

# iterate over the csv data
for index, row in csvData.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the id as URI
    video = URIRef(SY[row["Url_youtube"]])
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
        g.add(
            (
                video,
                SY["views"],
                Literal(row["Views"], datatype=XSD.integer),
            )
        )
        g.add(
            (
                video,
                SY["likes"],
                Literal(row["Likes"], datatype=XSD.integer),
            )
        )
        g.add(
            (
                video,
                SY["comments"],
                Literal(row["Comments"], datatype=XSD.integer),
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

    if (channel, RDF.type, SY.Channel) not in g:
        g.add((channel, RDF.type, SY.Channel))
        # if the channel isn't already in the addedChannels list add it
        if channel is not None and channel not in addedChannels:
            addedChannels.append(channel)

            g.add(
                (
                    channel,
                    SY["channelName"],
                    Literal(row["Channel"], datatype=XSD.string),
                )
            )

    # add edges triples (links between nodes)
    if (song, RDF.type, SY.SpotifySong) in g:
        g.add((video, SY["isVideoOf"], song))
    if channel is not None:
        g.add((video, SY["isUploadedBy"], channel))


# Bind the namespaces to a prefix for more readable output
g.bind("xsd", XSD)
g.bind("sy", SY)

# print all the data in the Turtle format
print("--- saving serialization ---")
with open(
    savePath + "Videos_Channels_Albums_AlbumTypes.ttl", "w+", encoding="utf-8"
) as file:
    file.write(g.serialize(format="turtle"))
