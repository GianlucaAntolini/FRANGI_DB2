import csv


# map of string:string called channelNamesIds
channelNamesIds = {}

albumNamesIds = {}

songsDict = {}

videosDict = {}

def updateLine(rowSY):
    if rowSY["Stream"] != "" and rowSY["Stream"] is not None:
        if (rowSY["Uri"] not in songsDict) or (
            (rowSY["Uri"] in songsDict) and (int(rowSY["Stream"]) > songsDict[rowSY["Uri"]])
        ):
            songsDict[rowSY["Uri"]] = int(rowSY["Stream"])
    if rowSY["official_video"] not in videosDict:
        videosDict[rowSY["Url_youtube"]] = [rowSY["Comments"], rowSY["Likes"], rowSY["Views"], rowSY["official_video"]]
    else:
        if rowSY["Comments"] != "" and rowSY["Comments"] is not None:
            videosDict[rowSY["Url_youtube"]][0] = rowSY["Comments"]
        if rowSY["Likes"] != "" and rowSY["Likes"] is not None:
            videosDict[rowSY["Url_youtube"]][1] = rowSY["Likes"]
        if rowSY["Views"] != "" and rowSY["Views"] is not None:
            videosDict[rowSY["Url_youtube"]][2] = rowSY["Views"]
        if rowSY["official_video"] != "" and rowSY["official_video"] is not None:
            videosDict[rowSY["Url_youtube"]][3] = rowSY["official_video"]

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

    albumId = ""
    if rowSY["Album"] != "" and rowSY["Album"] is not None:
        if rowSY["Album_type"] != "" and rowSY["Album_type"] is not None:
            if (rowSY["Album"], rowSY["Album_type"]) in albumNamesIds:
                albumId = albumNamesIds[(rowSY["Album"], rowSY["Album_type"])]
            else:
                # create a new album id : "album" + len(albumNamesIds)
                albumId = "album" + str(len(albumNamesIds))
                # add the album id to the map
                albumNamesIds[(rowSY["Album"], rowSY["Album_type"])] = albumId
        else:
            if (rowSY["Album"], "") in albumNamesIds:
                albumId = albumNamesIds[(rowSY["Album"], "")]
            else:
                # create a new album id : "album" + len(albumNamesIds)
                albumId = "album" + str(len(albumNamesIds))
                # add the album id to the map
                albumNamesIds[(rowSY["Album"], "")] = albumId

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
            # other file part
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
            #generate album id
            "albumId": albumId,
            # updated stream values
            "uStream": songsDict[rowSY["Uri"]] if rowSY["Uri"] in songsDict
            else "",
            # updated comments values
            "uComments": videosDict[rowSY["Url_youtube"]][0] if rowSY["Url_youtube"] in videosDict
            else "",
            # updated likes values
            "uLikes": videosDict[rowSY["Url_youtube"]][1] if rowSY["Url_youtube"] in videosDict
            else "",
            # updated views values
            "uViews": videosDict[rowSY["Url_youtube"]][2] if rowSY["Url_youtube"] in videosDict
            else "",
            # updated official_video values
            "uOfficial_video": videosDict[rowSY["Url_youtube"]][3] if rowSY["Url_youtube"] in videosDict
            else "",
        }
    )

# open file to save stream values
with open("Datasets/Original/Spotify_Youtube.csv", "r", newline="", encoding = "utf-8") as fileSY:
    readerSY = csv.DictReader(fileSY)
    for rowSY in readerSY:
        updateLine(rowSY)

# Open and read the csv files
with open("Datasets/Original/Spotify_Youtube.csv", "r", newline="", encoding = "utf-8") as fileSY:
    readerSY = csv.DictReader(fileSY)
    with open("Datasets/Original/spotify_songs.csv", "r", newline="", encoding = "utf-8") as fileTF:
        readerTF = csv.DictReader(fileTF)

        trackIdSY = ""
        with open(
            "Datasets/Computed/complete_dataset.csv", "w", newline="", encoding = "utf-8"
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
                #additional album id,
                "albumId",
                "uStream",
                "uComments",
                "uLikes",
                "uViews",
                "uOfficial_video"
            ]
            writerCD = csv.DictWriter(fileCD, fieldnames=fieldNamesCD)

            # Write the header row to the output CSV file
            writerCD.writeheader()

            TFDict = {}
            for rowTF in readerTF:
                TFDict[rowTF["track_id"]] = rowTF
            for rowSY in readerSY:
                trackIdSY = rowSY["Uri"].split(":")[2]
                # for each row of the tracks_features.csv
                if trackIdSY in TFDict:
                    writeLine(writerCD, rowSY, TFDict[trackIdSY])
                else:
                    writeLine(writerCD, rowSY, None)