import os

from twitter_pb2 import *
from sqlalchemy import *
from json import loads

tweets = Tweets()
with file('twitter.pb', 'r') as f:
  tweets.ParseFromString(f.read())


# recreate the sqlite db
os.system("cat twitter.ddl | sqlite3 twitter.db")

db = create_engine("sqlite:///%s" % "./twitter.db")
DELETE = "insert into tweets(is_delete, id, uid) values(?, ?, ?);"
INSERT = "insert into tweets values (?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
INSERTCOORD = "insert into coords values(?,?,?)"
INSERTPLACE = "insert into places values(?,?,?,?,?,?,?)"
INSERTPLACECOORD = "insert into place_coords values(?,?,?)"
for tweet in tweets.tweets:
  if tweet.is_delete:
    delete = tweet.delete
    db.execute(DELETE, tweet.is_delete, delete.id, delete.uid)
  else:
    insert = tweet.insert
    db.execute(INSERT,
      tweet.is_delete,
      insert.id,
      insert.uid,
      insert.truncated,
      insert.text,
      insert.reply_to,
      insert.reply_to_name,
      insert.favorite_count,
      insert.source,
      insert.retweeted,
      insert.possibly_sensitive,
      insert.lang,
      insert.created_at,
      insert.filter_level)

    coord = insert.coord
    if coord.lat:
      db.execute(INSERTCOORD,
        insert.id,
        coord.lat,
        coord.lon)

    place = insert.place
    if place.url:
      db.execute(INSERTPLACE,
        insert.id,
        place.url,
        place.country,
        place.country_code,
        place.place_type,
        place.id,
        place.name)
      for coord in place.bounding_box:
        db.execute(INSERTPLACECOORD,
          place.id,
          coord.lat,
          coord.lon)

