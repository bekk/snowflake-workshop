# Oppgave 7: Last inn data i schemaet ditt

## Åpne opp et nytt prosjekt/notebook i Snowflake og rediger og kjør alle statementene under
```sql
USE DATABASE <NAVNET PÅ DATABASEN DU OPPRETTET>;
USE SCHEMA <NAVNET PÅ SCHEMAET DU OPPRETTET>;

CREATE STAGE gcp_data
    storage_integration = storage
    url = '<gcs://<navnet_på_bøtta_du_opprettet>/>';

CREATE FILE FORMAT csv_format
    type = csv 
    field_delimiter = ";"
    skip_header = 1;

CREATE TABLE tilsyn (
    tilsynsobjektid VARCHAR,
    orgnummer VARCHAR,
    navn VARCHAR,
    adrlinje1 VARCHAR,
    adrlinje2 VARCHAR,
    postnr VARCHAR,
    poststed VARCHAR,
    tilsynid VARCHAR,
    sakref VARCHAR,
    status INT,
    dato VARCHAR,
    total_karakter INT,
    tilsynsbesoektype INT,
    tema1 VARCHAR,
    tema1_nn VARCHAR,
    karakter1 INT,
    tema2_no VARCHAR,
    tema2_nn VARCHAR,
    karakter2 INT,
    tema3_no VARCHAR,
    tema3_nn VARCHAR,
    karakter3 INT,
    tema4_no VARCHAR,
    tema4_nn VARCHAR,
    karakter4 INT
);

COPY INTO tilsyn 
FROM @gcp_data/tilsyn/smilefjes-tilsyn.csv
file_format=csv_format
on_error=continue;

CREATE TABLE tilsyn_transformert as 
    select 
        navn, 
        orgnummer,
        postnr, 
        poststed,
        total_karakter,
        karakter1 as rutiner_og_ledelse,
        karakter2 as lokaler_og_utstyr,
        karakter3 as mathandtering_og_tilberedning,
        karakter4 as merking_og_sporbarhet,
        TO_DATE(dato, 'DDMMYYYY') as dato
    from tilsyn;

CREATE TABLE postnummer (
    postnummer VARCHAR,
    poststed VARCHAR,
    kommunenummer VARCHAR,
    kommunenavn VARCHAR
);

COPY INTO postnummer 
FROM @gcp_data/postnummer/postnummer_raw.csv
file_format=csv_format
on_error=continue;


CREATE TABLE kommuner (
    json_data variant
);

COPY INTO kommuner
from @gcp_data/kommuner/kommuner_raw.json
file_format = (type = JSON, STRIP_OUTER_ARRAY = TRUE);

CREATE OR REPLACE TABLE kommuner_unwrapped as 
    select f.value[1] as feature, kommuner.json_data:kommunenummer:kodeverdi::STRING AS kommunenummer, kommuner.json_data:administrativenhetnavn[0]:navn::STRING as kommunenavn
    from kommuner,
    lateral flatten(input => kommuner.json_data:features) f
    WHERE feature is not NULL;

SELECT * FROM kommuner_unwrapped LIMIT 1;
    
CREATE OR REPLACE TABLE kommuner_transformert as
    select  
        kommunenavn,
        kommunenummer,
        ST_ASWKB(TRY_TO_GEOMETRY(feature:geometry)) AS geometry
    from kommuner_unwrapped;

SELECT * FROM kommuner_transformert LIMIT 1;
    
CREATE OR REPLACE TABLE tilsyn_med_kommune as (
  WITH tilsyn_med_postnummer as (
    SELECT 
      t.navn,
      t.dato,
      t.total_karakter,
      p.*
    FROM postnummer as p 
    JOIN tilsyn_transformert as t
    ON t.postnr = p.postnummer
  )
  SELECT 
    t.navn,
    t.dato,
    t.total_karakter, 
    t.postnummer,
    t.poststed,
    k.*
  FROM kommuner_transformert as k 
  LEFT JOIN tilsyn_med_postnummer as t
  ON k.kommunenummer = t.kommunenummer
);


CREATE OR REPLACE TABLE tilsynskarakter_per_kommune as 
    SELECT 
        kommunenavn,
        kommunenummer,
        geometry,
        round(avg(total_karakter), 3) as gjennomsnittlig_karakter
    FROM tilsyn_med_kommune
    GROUP BY kommunenavn, kommunenummer, geometry;

SELECT * FROM tilsynskarakter_per_kommune LIMIT 10;
```

## Apply og logg inn
Kjør sql statementene i terraform, og se at tabellene blir korrekt opprettet