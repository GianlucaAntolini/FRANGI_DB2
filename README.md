# FRANGI_DB2

Datasets:

https://www.kaggle.com/datasets/salvatorerastelli/spotify-and-youtube

https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs

The datasets have been merged in a single file called complete_dataset.csv. To create this file one must place the 3 Python scripts in a folder in which there should be another folder called Datasets, that contains inside other two folders: Original (where the original datasets should be placed) and Computed. The scripts have to be run in the following order

1: addIdColumnToDataset.py

2: sortDatasetsScript.py (optional, but it makes merging faster)

3: dataMergeScript.py
