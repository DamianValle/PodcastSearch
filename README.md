<p align="left"><img src="/img/logo.png" width="150"/></p>

# Spotify Podcast Search Engine

Podcast Search Engine powered by ElasticSearch implemented using python indexing the Spotify Podcast Dataset.

## System architecture

<p align="center"><img src="/img/overview.png" width="700"/></p>

## Podcast data:

- Available at: [Spotify Podcast Dataset](https://podcastsdataset.byspotify.com/)
- Structure of the data:
  - JSON file divided into pieces (transcripts) with the following structure
    - Transcript: all the words as a text file
    - Confidence: float number between 0 and 1
    - Words: each word individually with start and end time
  - Metadata file:
    - Contains podcast name, URI, description, publisher, language, episode name and duration.
- There is a smaller (1.2 GB) test sample with the same structure as the other files: spotify-podcasts-2020-summarization-testset

The dataset should extracted into the ```/podcasts-no-audio13GB``` folder.

## Needed for GUI and Spotify Web API

```
pip install requirements.txt
```

```
sudo apt-get install python3-tk
sudo apt install tkinter
```

```
export SPOTIPY_CLIENT_ID='your-client-id'
export SPOTIPY_CLIENT_SECRET='your-client-secret'
```

## Elasticsearch setup:

- download elasticsearch: https://www.elastic.co/start
- unzip downloaded file
- go to unzipped folder and run bin/elasticsearch
- To see if it's working: open browser and go to http://localhost:9200/

## Kibana setup:

- download kibana: https://www.elastic.co/start
- unzip downloaded file
- go to unzipped folder and run bin/kibana
- To see if it's working: open browser and go to http://localhost:5601/app/management/data/index_management/indices This should show your local indices
