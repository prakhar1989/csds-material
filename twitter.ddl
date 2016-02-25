
DROP TABLE IF EXISTS tweets;

CREATE TABLE tweets (
 is_delete bool,
 id bigint,
 uid bigint,
 truncated bool,
 text text,
 reply_to bigint,
 reply_to_name text,
 favorite_count int,
 source text,
 retweeted bool,
 possibly_sensitive bool,
 lang text,
 created_at varchar(64),
 filter_level text
);

DROP TABLE IF EXISTS coords;
CREATE TABLE coords (
 tid bigint, -- The ID of the tweet being geolocated
 lat float,
 lon float
);


DROP TABLE IF EXISTS places;
CREATE TABLE places (
 tid bigint, -- The ID of the tweet the place is mentioned in
 url text,
 country text,
 country_code text,
 place_type text,
 id text,
 name text
);

DROP TABLE IF EXISTS place_coords;
CREATE TABLE place_coords (
 pid text, -- The ID of the place being geolocated
 lat float,
 lon float
);

