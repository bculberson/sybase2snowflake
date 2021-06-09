Prerequisites:

* Needs ODBC Driver for ASE 3.0 DEB x64 from https://www.devart.com/odbc/ase/
* Python 3
* Requirements installed from requirements.txt
* ODBC Driver installed on host with DSN to the source db

# CREATE A TEST DB
```sh
mkdir ~/.dksybase
mkdir ~/extract
docker-compose up
```

# HOW TO EXTRACT AND UPLOAD DATA TO SNOWFLAKE WITH DELETE AFTER PUT
```sh
docker-compose run test python extract.py <DSN> <DATABASE> <TABLE> <TEMP_DIR> | python load.py <SNOWFLAKE_ACCT> <SNOWFLAKE_USER> <SNOWFLAKE_PASSWORD> DELETE
```


# SNOWFLAKE IMPORT FROM STAGE
```sql
create database S2S;
use database S2S;
create schema TEST;
use schema TEST;

CREATE TABLE TEST (id INT, "data" VARCHAR(255));

CREATE file format JSON
  TYPE = JSON
  COMPRESSION = GZIP
  STRIP_OUTER_ARRAY = TRUE;

INSERT INTO TEST
select t.$1[0],t.$1[1] from @~ (file_format => 'JSON', pattern=>'.*\.TEST_.*\.json\.gz') t;

select * from test limit 100;
```