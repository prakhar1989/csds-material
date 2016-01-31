DROP TABLE purchases;

CREATE TABLE purchases (
    `sales_date` TIMESTAMP,
    `store_location` STRING, 
    `category` STRING, 
    `price` FLOAT,
    `card` STRING
) row format delimited fields 
terminated by ',' stored as textfile;

LOAD DATA INPATH '/user/csds/input/purchases.txt' INTO TABLE purchases;
