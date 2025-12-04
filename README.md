# 02807FinalProject
Spotify million playlist dataset

## Python version
Python 3.8 or newer



### Required Packages
pandas
numpy
matplotlib
scikit-learn
seaborn
scipy
umap-learn
faiss
sentence_transformers
openai


### Install required packages:
pip install pandas numpy faiss-cpu sentence-transformers openai matplotlib seaborn scikit-learn scipy umap-learn


## Data processing and clustering
- Clone or download this repository.
- Open the Jupyter Notebook clustering.ipynb
- Ensure the directory structure with the following files:
  data/_raw/
   data/                     -> 1000 MPD JSON files
   scraped/                  -> scraped playlist dataset
   spotify_data.csv          -> audio features (Million Songs Dataset)
- Run all cells sequentially
- The notebook will automatically write output files to ./data/.




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
- Open the main.py file in Visual Studio Code or another editor.
- Make sure that the file is in the same folder as the .env file, with valid spotify API key information
- Make sure the environment you are using has the right packages installed through conda or pip
- Press run and the script will:
    Look for public playlists with specific keywords
    Scrape the playlist name, song name, song ID and artist name
    Save it all in a new CSV file called spotify_data.csv


### How ot run data_splitter.py
- Clone or download this repository
- Open the data_splitter.py file in Visual Studio Code or another editor
- Make sure that the file is in the same folder as the merged_with_features.csv file
- Make sure the environment you are using has the right packages installed through conda or pip
- Press run and the script will:
    Split the merged_with_features.csv data into a 20/80 split with 80% training and 20% test


## BERT and FAISS for Playlist Recommendation

### How to run
- Clone or download this repository.
- Open the Jupyter Notebook (bert_prompt_to_playlist.ipynb)
- Ensure the dataset data.csv and embeddings are placed in the correct directory, as well as the llm_judge files.
- Run all cells sequentially.
- The script will:
    Create or import tracks and playlist BERT embeddings  
    Build a FAISS index for fast similarity search  
    Generate a playlist based on the prompt and tracks+playlist embeddings similarity  
    Evaluate performance using ranking metrics (Precision@10, Recall@10, MAP@10, NDCG@10)  
    Evaluate performance using an LLM-as-a-judge method  
    /!\ To run the LLM-as-a-judge part, you need an OpenAI API key, which you can create here: https://platform.openai.com/api-keys, as well as **credit** on your account (gpt-4o-mini is almost, but **not**, free). If this is unfeasible, you can find the results of our run in the outputs.pdf file. 
