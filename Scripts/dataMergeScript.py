import csv


# map of string:string called channelNamesIds
channelNamesIds = {}


def writeLine(writerCD, rowSY, rowTF):
    channelId = ""
    if rowSY["Channel"] != "" and rowSY["Channel"] is not None:
        if rowSY["Channel"] in channelNamesIds:
            channelId = channelNamesIds[rowSY["Channel"]]
        else:
            # create a new channel id : "channel" + len(channelNamesIds)
            channelId = "channel" + str(len(channelNamesIds))
            # add the channel id to the map
            channelNamesIds[rowSY["Channel"]] = channelId
    writerCD.writerow(
        {
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
            # we check if the part of the other file is not None but it shouldn't be because we do a full join
            "track_album_release_date": rowTF["track_album_release_date"]
            if rowTF is not None
            else "",
            "track_album_id": rowTF["track_album_id"] if rowTF is not None else "",
            "playlist_name": rowTF["playlist_name"] if rowTF is not None else "",
            "playlist_id": rowTF["playlist_id"] if rowTF is not None else "",
            "playlist_genre": rowTF["playlist_genre"] if rowTF is not None else "",
            "playlist_subgenre": rowTF["playlist_subgenre"]
            if rowTF is not None
            else "",
            # generated channel id
            "channelId": channelId,
        }
    )


# Open and read the csv files
with open("../Datasets/Original/Spotify_Youtube.csv", "r", newline="") as fileSY:
    readerSY = csv.DictReader(fileSY)
    with open("../Datasets/Original/spotify_songs.csv", "r", newline="") as fileTF:
        readerTF = csv.DictReader(fileTF)

        trackIdSY = ""
        with open(
            "../Datasets/Computed/complete_dataset.csv", "w", newline=""
        ) as fileCD:
            fieldNamesCD = [
                # here start all the fields from the spotify_youtube_with_id_sorted.csv
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
                # here start the chosen fields from the tracks_features_sorted.csv
                "track_album_release_date",
                "track_album_id",
                "playlist_name",
                "playlist_id",
                "playlist_genre",
                "playlist_subgenre",
                # additional channel id
                "channelId",
            ]
            writerCD = csv.DictWriter(fileCD, fieldnames=fieldNamesCD)

            # Write the header row to the output CSV file
            writerCD.writeheader()

            TFDict = {}
            for rowTF in readerTF:
                TFDict[rowTF["track_id"]] = rowTF
            count = 0
            for rowSY in readerSY:
                trackIdSY = rowSY["Uri"].split(":")[2]
                # for each row of the tracks_features.csv
                if trackIdSY in TFDict:
                    count += 1
                    print("Found: " + trackIdSY)
                    print(TFDict[trackIdSY])
                    writeLine(writerCD, rowSY, TFDict[trackIdSY])
