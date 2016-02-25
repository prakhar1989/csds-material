#
# 
# Script to encode twitter.data as protocol buffers
# Extracts _most_ of the fields.  
# 
# See twitter.proto for the protocol buffer description
#
# @author eugene wu 2013
#


from pdb import set_trace
from json import loads
from itertools import imap
from twitter_pb2 import *

tweets = Tweets()
with file('twitter.json', 'r') as f:
  for line in imap(loads, f):
    tweet = tweets.tweets.add()
    tweet.is_delete = ('delete' in line)
    if 'delete' in line:
      status = line['delete']['status']
      tweet.delete.id = status['id']
      tweet.delete.uid = status['user_id']
    else:
      insert = tweet.insert
      insert.uid = line['user']['id']
      insert.truncated = line['truncated']
      insert.text = line['text']
      if line.get('in_reply_to_status_id', None):
        insert.reply_to = line['in_reply_to_status_id']
        insert.reply_to_name = line['in_reply_to_screen_name']
      insert.id = line['id']
      insert.favorite_count = line['favorite_count']
      insert.source = line['source']
      insert.retweeted = line['retweeted']
      if line.get('possibly_sensitive', None):
        insert.possibly_sensitive = line['possibly_sensitive']
      insert.lang = line['lang']
      insert.created_at = line['created_at']
      if line.get('coordinates', None):
        coords = line['coordinates']
        insert.coord.lat = coords['coordinates'][0]
        insert.coord.lon = coords['coordinates'][1]
      insert.filter_level = line['filter_level']

      if line.get('place', None):
        place = line['place']
        insert.place.url = place['url']
        insert.place.country = place['country']
        insert.place.country_code = place['country_code']
        insert.place.place_type = place['place_type']
        insert.place.id = place['id']
        insert.place.name = place['name']
        if place.get('bounding_box', None):
          def add(pair):
            coord = insert.place.bounding_box.add()
            coord.lat = pair[0]
            coord.lon = pair[1]
          map(add, place['bounding_box']['coordinates'][0])



with file('twitter.pb', 'w') as f:
  f.write(tweets.SerializeToString())

