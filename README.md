# 02807FinalProject
Spotify million playlist dataset

## Python version
Python 3.8 or newer



### Required Packages
pandas
numpy


### Install required packages:
pip install pandas numpy


## Locality-Sensitive Hashing for Playlist Recommendation

### How to run
- Clone or download this repository.
- Open the Jupyter Notebook (LSH.ipynb)
- Ensure the dataset files train.csv, test.csv are placed in the correct directory.
- Run all cells sequentially.
- The script will:
    Construct MinHash signatures for all playlists
    Build an LSH index for efficient similarity search
    Generate playlist continuation recommendations
    Evaluate performance using ranking metrics (Precision@10, Recall@10, MAP@10, NDCG@10



### How to run main.py (Used for Data scraping)
- Clone or download this repository
- Open the main.py file in visual studio code or another editor.
- Make sure that the file is in the same folder as the .env file, with valid spotify API key information
- Make sure the environment you are using has the right packages installed through conda or pip
- Press run and the script will:
    Look for public playlists with specific keywords
    Scrape the playlist name, song name, song ID and artist name
    Save it all in a new CSV file called spotify_data.csv


### How ot run data_splitter.py
- Clone or download this repository
- Open the data_splitter.py file in visual studio code or another editor
- Make sure that the file is in the same folder as the merged_with_features.csv file
- Make sure the environment you are using has the right packages installed through conda or pip
- Press run adn the script will:
    Split the merged_with_features.csv data into a 20/80 split with 80% training and 20% test