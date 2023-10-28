import csv
import datetime;


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
            "track_number": rowTF["track_number"] if rowTF is not None else "",
            "disc_number": rowTF["disc_number"] if rowTF is not None else "",
            "explicit": rowTF["explicit"] if rowTF is not None else "",
            "release_date": rowTF["release_date"] if rowTF is not None else "",
            "album_id": rowTF["album_id"] if rowTF is not None else "",
        }
    )


print("Starting...")

# Open and read the csv files
with open(
    "Datasets/Computed/Spotify_Youtube_with_id_sorted.csv", "r", encoding="utf8"
) as fileSY:
    readerSY = csv.DictReader(fileSY)
    with open(
        "Datasets/Computed/tracks_features_edited_sorted.csv", "r", encoding="utf8"
    ) as fileTF:
        readerTF = csv.DictReader(fileTF)

        trackIdSY = ""
        with open("Datasets/Computed/complete_dataset.csv", "w", encoding="utf8") as fileCD:
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
            totalrows = 20718
            countRows = 0
            
            # convert dictReader to dict ('id' as key, full row as value)
            TFdict = {}
            for rowTF in readerTF:
                TFdict[rowTF["id"]] = rowTF
            
            for rowSY in readerSY:
                if countRows % 5000 == 0:
                    ct = datetime.datetime.now()
                    print("Time:", ct)
                    print("Progress:", str((countRows*100)/totalrows)[:4]+"%")
                    print("Match over total:", str(matchCount)+"/"+str(countRows))
                    print()
                countRows += 1
                
                trackIdSY = rowSY["Uri"].split(":")[2]
                # print(trackIdSY)
                foundMatch = False
                # for each row of the tracks_features.csv
                trackIdTF = ""
                
                if trackIdSY in TFdict:
                    matchCount += 1
                    # print("match")
                    foundMatch = True
                    # write all the fields of youtube_spotify_with_id_sorted.csv plus the chosen
                    # fields of tracks_features_sorted.csv
                    writeLine(writerCD, rowSY, rowTF)
                
                # reset the readerTF
                fileTF.seek(0)
                # if we didn't find a match and the song is a single we can keep it with no album, else we discard it
                if not foundMatch:
                    # print("no match")
                    if rowSY["Album_type"] == "single":
                        # print("no match with single")
                        writeLine(writerCD, rowSY, None)
                    else:
                        # print("no match with an album")
                        pass

    print("matchCount: ", matchCount)
