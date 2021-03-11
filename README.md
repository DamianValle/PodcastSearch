# PodcastSearch

Planning, organization & ideas:
https://docs.google.com/document/d/17JKpFqKf7zWBIn_4Hav5L_UU5DdRN2hHe4deIsgkfBo/edit?usp=sharing



# Setting up (local) Elasticsearch and Kibana

Elasticsearch:
  download elasticsearch: https://www.elastic.co/start
  unzip downloaded file
  go to unzipped folder and run bin/elasticsearch
  To see if it's working: open browser and go to http://localhost:9200/
  
Kibana:
  download kibana: https://www.elastic.co/start
  unzip downloaded file
  go to unzipped folder and run bin/kibana
  To see if it's working: open browser and go to http://localhost:5601/app/management/data/index_management/indices This should show your local indices
 
Adding and retrieving indices:
  This happens with https requests
  see readme of https://github.com/elastic/elasticsearch for examples using curl



