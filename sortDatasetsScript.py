# TO SORT THE TWO DATASETS BY ID:
# makes the matching between ids for merging easier and faster


import pandas as pd

# tracks_features file
# Load the CSV file into a DataFrame
df = pd.read_csv("Datasets/Computed/tracks_features_edited.csv")

# Sort the DataFrame by the "Id" column
df_sorted = df.sort_values(by="id")

# Save the sorted DataFrame to a new CSV file
df_sorted.to_csv("Datasets/Computed/tracks_features_edited_sorted.csv", index=False)


# Spotify_Youtube_with_id file
# Load the CSV file into a DataFrame
df = pd.read_csv("Datasets/Computed/Spotify_Youtube_with_id.csv")

# Sort the DataFrame by the "Id" column
df_sorted = df.sort_values(by="id")

# Save the sorted DataFrame to a new CSV file
df_sorted.to_csv("Datasets/Computed/Spotify_Youtube_with_id_sorted.csv", index=False)
