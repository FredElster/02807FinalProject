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