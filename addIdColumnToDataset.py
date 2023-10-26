# FILE TO ADD THE ID COLUMN TO THE SPOTIFY_YOUTUBE.CSV FILE:
# it is basically the spotify uri split by ":" and taking the third element

import csv


# Open and read the csv files
with open("Datasets/Original/Spotify_Youtube.csv", "r", newline="") as fileSY:
    readerSY = csv.DictReader(fileSY)
    with open(
        "Datasets/Computed/Spotify_Youtube_with_id.csv", "w", newline=""
    ) as fileSYWI:
        # the same fields as the Spotify_Youtube.csv plus the id field
        fieldNamesSYWI = [
            "id",
            "row_id",
            "Track",
            "Artist",
            "Url_spotify",
            "Album",
            "Album_type",
            "Uri",
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
            "Url_youtube",
            "Title",
            "Channel",
            "Views",
            "Likes",
            "Comments",
            "Description",
            "Licensed",
            "official_video",
        ]
        writerSYWI = csv.DictWriter(fileSYWI, fieldnames=fieldNamesSYWI)

        # Write the header row to the output CSV file
        writerSYWI.writeheader()

        for rowSY in readerSY:
            trackIdSY = rowSY["Uri"].split(":")[2]
            # Write the data row to the output CSV file
            writerSYWI.writerow(
                {
                    "id": trackIdSY,
                    "row_id": rowSY[""],
                    "Track": rowSY["Track"],
                    "Artist": rowSY["Artist"],
                    "Url_spotify": rowSY["Url_spotify"],
                    "Album": rowSY["Album"],
                    "Album_type": rowSY["Album_type"],
                    "Uri": rowSY["Uri"],
                    "Danceability": rowSY["Danceability"],
                    "Energy": rowSY["Energy"],
                    "Key": rowSY["Key"],
                    "Loudness": rowSY["Loudness"],
                    "Speechiness": rowSY["Speechiness"],
                    "Acousticness": rowSY["Acousticness"],
                    "Instrumentalness": rowSY["Instrumentalness"],
                    "Liveness": rowSY["Liveness"],
                    "Valence": rowSY["Valence"],
                    "Tempo": rowSY["Tempo"],
                    "Duration_ms": rowSY["Duration_ms"],
                    "Stream": rowSY["Stream"],
                    "Url_youtube": rowSY["Url_youtube"],
                    "Title": rowSY["Title"],
                    "Channel": rowSY["Channel"],
                    "Views": rowSY["Views"],
                    "Likes": rowSY["Likes"],
                    "Comments": rowSY["Comments"],
                    "Description": rowSY["Description"],
                    "Licensed": rowSY["Licensed"],
                    "official_video": rowSY["official_video"],
                }
            )
