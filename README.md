# PodcastSearch

Planning, organization & ideas:
 * https://docs.google.com/document/d/17JKpFqKf7zWBIn_4Hav5L_UU5DdRN2hHe4deIsgkfBo/edit?usp=sharing



# Setting up (local) Elasticsearch and Kibana

Elasticsearch:
  * download elasticsearch: https://www.elastic.co/start
  * unzip downloaded file
  * go to unzipped folder and run bin/elasticsearch
  * To see if it's working: open browser and go to http://localhost:9200/
  
Kibana:
  * download kibana: https://www.elastic.co/start
  * unzip downloaded file
  * go to unzipped folder and run bin/kibana
  * To see if it's working: open browser and go to http://localhost:5601/app/management/data/index_management/indices This should show your local indices
 
Adding and retrieving indices:
  * This happens with https requests
  * see readme of https://github.com/elastic/elasticsearch for examples using curl

Podcast data:
  * download at: [Spotify Podcast Dataset](https://podcastsdataset.byspotify.com/)
  * Structure of the data: 
    * each podcast is a Json file divided into pieces (transcripts) with the following structure
      * transcript: all the words as a text file
      * confidence: float number between 0 and 1
      * words: each word individually with start and end time
    * There is also a metadata file:
      * contains name, uri, description, publisher, language, episode name, duration and links to uri's and files in table form
  * There is a smaller (1.2 GB) test sample with the same structure as the other files: spotify-podcasts-2020-summarization-testset
  
  
  
  needed for GUI:
  sudo apt-get install python3-tk
  sudo apt install tkinter

