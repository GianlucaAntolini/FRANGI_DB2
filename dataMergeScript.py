import csv


def writeLine(writerCD, rowSY, rowTF):
    writerCD.writerow(
        {
            "id": rowSY["id"],
            "row_id": rowSY["row_id"],
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
            "track_number": rowTF["track_number"]
            if rowTF["track_number"] is not None
            else "",
            "disc_number": rowTF["disc_number"]
            if rowTF["disc_number"] is not None
            else "",
            "explicit": rowTF["explicit"] if rowTF["explicit"] is not None else "",
            "release_date": rowTF["release_date"]
            if rowTF["release_date"] is not None
            else "",
            "album_id": rowTF["album_id"] if rowTF["album_id"] is not None else "",
        }
    )


# Open and read the csv files
with open(
    "Datasets/Computed/Spotify_Youtube_with_id_sorted.csv", "r", newline=""
) as fileSY:
    readerSY = csv.DictReader(fileSY)
    with open(
        "Datasets/Computed/tracks_features_sorted.csv", "r", newline=""
    ) as fileTF:
        readerTF = csv.DictReader(fileTF)

        trackIdSY = ""
        with open("Datasets/Computed/complete_dataset.csv", "w", newline="") as fileCD:
            fieldNamesCD = [
                # added id field from spotify_youtube.csv (maybe not needed)
                "id",
                # here start all the fields from the spotify_youtube_with_id_sorted.csv
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
                # here start the chosen fields from the tracks_features_sorted.csv
                "track_number",
                "disc_number",
                "explicit",
                "release_date",
                "album_id",
            ]
            writerCD = csv.DictWriter(fileCD, fieldnames=fieldNamesCD)

            # Write the header row to the output CSV file
            writerCD.writeheader()

            matchCount = 0

            for rowSY in readerSY:
                trackIdSY = rowSY["Uri"].split(":")[2]
                print(trackIdSY)
                foundMatch = False
                # for each row of the tracks_features.csv
                trackIdTF = ""
                for rowTF in readerTF:
                    trackIdTF = rowTF["id"]

                    # if the track id of the spotify_youtube.csv is equal to the track id of the tracks_features.csv
                    if trackIdSY == trackIdTF:
                        matchCount += 1
                        print("match")
                        foundMatch = True
                        rowTFAlbum = rowTF["album"]
                        # write all the fields of youtube_spotify_with_id_sorted.csv plus the chosen
                        # fields of tracks_features_sorted.csv
                        writeLine(writerCD, rowSY, rowTF)

                        # break inner loop
                        break
                # reset the readerTF
                fileTF.seek(0)
                # if we didn't find a match and the song is a single we can keep it with no album, else we discard it
                if not foundMatch:
                    print("no match")
                    if rowSY["Album_type"] == "single":
                        print("no match with single")
                        writeLine(writerCD, rowSY, None)
                    else:
                        print("no match with an album")

    print("matchCount: ", matchCount)
