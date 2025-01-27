# Workshop: Introduksjon til Snowflake ❄️

Velkommen til Snowflake-workshop! De neste to timene skal vi bryne oss på innhenting, transformering og plotting av [tilsynsdata](https://hotell.difi.no/?dataset=mattilsynet/smilefjes/tilsyn) fra Digitaliseringsdirektoratet. Dette er en vurdering av over 3500 restauranter i Norge på parametre som lokaler, mathåndtering, merking og lignende. Vårt mål er å ta i bruk geodata fra Kartverket for å visualisere hvilke kommuner i Norge som har - og eventuelt _ikke_ har - restaurantene sine helt på stell 😀 🤔 😩

## DEL 1: Kobling mot Google Cloud Storage 💾

Logg inn i [Snowflake](https://sc96841.europe-west4.gcp.snowflakecomputing.com/console/login#/) med brukernavn og passord du har blitt tildelt og naviger deg til **Projects -> Worksheets** og lag et nytt worksheet i høyre hjørne. Nå er du klar til å utvikle i ditt eget arbeidsområde!

> **Tips 💡** Når vi jobber i en Snowflake Worksheet er det ikke nødvendig å slette cellene etter de er kjørt. Du kan heller markere de linjene du ønsker skal kjøre, så har du også historikken med deg til senere oppgaver.  

### Oppgave 1.1: Lag database og skjema 
Det første du må gjøre er å lage en egen database og et skjema (datasett) på formatet `ditt_navn`_database/schema slik som i kodesnutten under. Bytt med ditt eget navn og kjør cellene i Snowflake. 

```sql
CREATE DATABASE ditt_navn_database; 
CREATE SCHEMA ditt_navn_schema;
```

Naviger deg til **Database** i panelet til venstre og kjør refresh. Nå vil du forhåpentligvis se at din nye database og skjema er opprettet.

<img src=https://github.com/bekk/snowflake-workshop/assets/29883261/6f4f1fac-94f7-43f5-94c0-6bd47b4e4a25 width=250 />

Det er slitsomt å måtte spesifisere hele stien hver gang vi oppretter en tabell. Heldigvis kan du slippe dette ved å sette hvilken kontekst du ønsker å være i (altså, hvilken database og hvilket skjema du vil bruke). I filen kan du navigere deg i venstre hjørne og sette database og skjema som vi akkurat lagde.

<img src=https://github.com/bekk/snowflake-workshop/assets/29883261/baac22e4-51e6-415c-98fb-02cf5ba46c44 width=400 />


Nok snikksnakk, la oss hente data fra GCP!

### Oppgave 1.2: Last inn data fra GCS-bøtte 🪣

Nå skal vi hente data fra `snowflake-ws-raw-data`-bøtta som ligger i [GCP](https://console.cloud.google.com/storage/browser?project=snowflake-workshop&prefix=&forceOnBucketsSortingFiltering=true). For å gjøre dette er vi nødt til å opprette en konfigurasjonsenhet som brukes for å integrere Snowflake med eksterne lagringstjenester (som Google Cloud Storage). Denne enheten kalles for `storage integration object` og oppretter blant annet en egen service account (maskinbruker) som vi kan gi tilgang til i bøtta vår. Kodesnutten under sier at vi ønsker å lage et eksternt volum i GCS som har tilgang til en gitt sti. 

> **NB:** Det går bare an å sette opp én integrasjon per bøtte. Denne er allerede satt opp for dere, så dere trenger ikke kjøre kodesnutten under!

```sql
CREATE STORAGE INTEGRATION august_gcp_integration
    type = external_stage
    storage_provider = GCS 
    enabled = true 
    storage_allowed_locations = ('gcs://snowflake-ws-raw-data/');
```

Nå kan vi hente ut den genererte maskinbrukeren ved å kjøre:

```sql
DESC STORAGE INTEGRATION august_gcp_integration;
```

Her ser vi at vi har fått en maskinbruker, `STORAGE_GCP_SERVICE_ACCOUNT`, som vi kan gi tilgang til i bøtta. Dette er også allerede gjort, men du kan verifisere det ved å navigere deg til [**Permissions**](https://console.cloud.google.com/storage/browser/snowflake-ws-raw-data;tab=permissions?forceOnBucketsSortingFiltering=true&project=snowflake-workshop&prefix=&forceOnObjectsSortingFiltering=false)-fanen i bøtta og se at maskinbrukeren har rettigheten `Storage Admin`.

Så lett var det - nå har vi muligheten til å autentisere oss mot bøtta og hente ut dataen 🚀

### Oppgave 1.3: Lag mellomledd for kildedata og datavarehus

Det siste vi trenger å lage for å hente data er et `stage object`. Dette er et område som brukes til midlertidig lagring av rådatafiler før de lastes inn i Snowflake-databaser. Det fungerer som et mellomledd mellom kildedataene og datavarehuset vårt. For å hente dataen må vi ta i bruk `storage integration`-objektet vi nettopp lagde ved å kopiere og kjøre kodesnutten under:

```sql
CREATE STAGE gcp_data
    storage_integration = august_gcp_integration
    url = 'gcs://snowflake-ws-raw-data/';
```

Verifiser at dette funket ved å kjøre `list @gcp_data;`. Får du opp fire filer, er vi _endelig_ klare til å kopiere data inn i Snowflake. 


## DEL 2: Hent CSV-data for tilsyn og postnummer 📫

### Oppgave 2.1: Kopier data fra stage til tabell
Nå skal vi gjøre oss klare for å laste inn data. Først er vi nødt til å lage et fil-format som matcher CSV-formatet. 
Åpne `postnummer.csv` og `tilsyn.csv` i [bøtta](https://console.cloud.google.com/storage/browser/snowflake-ws-raw-data;tab=objects?forceOnBucketsSortingFiltering=true&project=snowflake-workshop&prefix=&forceOnObjectsSortingFiltering=false) for å se hvilke verdier du må erstatte i kodesnutten under: 

```sql
CREATE FILE FORMAT csv_format
    type = csv 
    field_delimiter = <sett_inn_separasjonstegn>
    skip_header = <sett_inn_antall_rader_som_må_hoppes_over>;
```

I tillegg må vi initiere tabellen vår, `tilsyn`, med riktig antall kolonner og type. Dette er en døll prosess å gjøre for hånd (ChatGPT fikset det for meg), så bare kopier og kjør snutten under:

```sql
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
```

Til slutt kopierer vi dataen _fra_ stage-objektet vårt _til_ den nylig opprettede tabellen vår. Merk at når vi tar i bruk stage-objektet vårt, så slipper vi også å fore inn hele URL-en. Siden dataen også (muligens) inneholder noen korrupte rader, slenger vi på `on_error=continue` for at opplastingen skal hoppe over disse radene og fortsette innlastningen. Kjør og kopier:

```sql
COPY INTO tilsyn 
FROM @gcp_data/csv/tilsyn.csv
file_format=csv_format
on_error=continue;
```

Når snutten er ferdigkjørt kan vi se at det var seks rader som var feilformatert. Det bryr vi oss ikke så mye om i denne workshopen. 

Kjør en spørring på tabellen for å sjekke at dataen er korrekt lastet inn. 

### Oppgave 2.2: Transformer tilsynstabellen

Det er et par ting med den opprinnelige rådataen som ikke passer vårt formål. Lag derfor en spørring og skriv den til en ny tabell, `tilsyn_transformert`, som inneholder følgende:
1. `navn, orgnummer, postnr, poststed, total_karakter`-kolonnene på vanlig format
2. Sette verdier fra `karakter1` til kolonne `rutiner_og_ledelse`, `karakter2` til `lokaler_og_utstyr`, `karakter3` til `mathandtering_og_tilberedning` og `karakter4` til `merking_og_sporbarhet`
3. Omgjøre dato-strengen på formatet 'DDMMYYYY' til dato 
4. Kjør en spørring som verifiserer at dataen ser korrekt ut.

<details>
  <summary>🚨 Løsningsforslag</summary>
  
  ```sql
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
  ```

</details>


### Oppgave 2.3: Hent inn postnummer-data

I neste del av workshopen skal vi få inn geodata for kommuner. Problemet vårt er at det eneste vi har å gå på i tilsynstabellen er `postnr`, mens kommune-dataen vår bare har info om kommunenavn og kommunenummer. Heldigvis har vi en fil i GCS, `postnummer`, som kan hjelpe oss med å knytte de to tabellene sammen!

Vi ønsker å gjøre akkurat det samme for `postnummer` som vi gjorde for tilsyn: 
1. Initiere tabellen med riktige antall kolonner og typer
2. Kopier fra stage-objekt til tabell
3. Verifiser resultatet

<details>
  <summary>🚨 Løsningsforslag</summary>

```sql
-- Initier postnummer-tabell 
CREATE TABLE postnummer (
    postnummer VARCHAR,
    poststed VARCHAR,
    kommunenummer VARCHAR,
    kommunenavn VARCHAR
);

-- Kopier postnummer fra stage til Snowflake-tabell
COPY INTO postnummer 
FROM @gcp_data/csv/postnummer.csv
file_format=csv_format
on_error=continue;
```
  
</details>


## DEL 3: Hent og transformer JSON-data for kommuner 🗺️

CSV-filene vi har jobbet med hittil har vært enkel, tabulær data. Men hvordan håndterer man semi-strukturert data som JSON?

### Oppgave 3.1: Last opp data fra stage til kommuner-tabell

Som i tidligere oppgaver må vi starte med å initiere tabellen vår. I kodesnutten under lager vi tabellen `kommuner` med all data i én kolonne av typen `VARIANT`. Det er en fleksibel datatype som kan holde en hvilken som helst type av semi-strukturerte data som JSON, Avro, XML eller lignende. Kjør kodesnutten under:

```sql
CREATE TABLE kommuner (
    json_data variant
);
```

Deretter må vi kopiere inn dataen fra GCS på samme måte som før. Det eneste vi dropper å gjøre er å lage et filformat slik som for CSV, da det eneste vi trenger å sette er typen:

```sql
COPY INTO kommuner
from @gcp_data/json/kommuner.json
file_format = (type = JSON);
```

Ta en titt på tabellen vi nå har opprettet. Her er vi nødt til å nøste opp i et par ting 🧹

### Oppgave 3.2: Pakk ut JSON-data

La oss starte med å pakke ut dataen slik at vi får én kommune per rad. Vi bruker en noe mystisk funksjon, `LATERAL FLATTEN`, for å pakke ut features-objektet. Det er den mest effektive måte å pakke ut nøstede arrays i en JSON-kolonne, slik vi har her:

```sql
CREATE TABLE kommuner_unwrapped as 
    select f.value as feature
    from kommuner,
    lateral flatten(input => kommuner.json_data[0]:features) f;
```

Se på den nye tabellen vår. Nå har vi i alle fall én rad per feature (kommuner med data), men vi ønsker å pakke ut dataen enda mer fra JSON-formatet til kolonner. 

Det vi trenger fra kommuner er kommunenavn, kommunenummer og geometri slik at vi kan slå det sammen med de andre tabellene og plotte tilsynskarakterene i et kart per kommune. Vi ønsker i samme slengen å transformere geometry-objektet til binær-format, og det kan du gjøre ved å bruke `ST_ASWKB(TRY_TO_GEOMETRY(feature:geometry))`. 

Finn ut av hvordan vi kan få transformert JSON-objektet til de ønskede kolonnene og prøv selv!

<details>
  <summary>🚨 Løsningsforslag</summary>


  I Snowflake aksesserer du JSON-objekter med kolon, `:`. Hvis du for eksempel har `{"key": "value"}` i en kolonne, `json_column`, så kan du hente ut verdien med `json_column:key::<TYPE>`, der `TYPE` er typen du ønsker å konvertere til (eksempelvis `STRING`). For nøstede objekter kan du bare fortsette med den samme annotasjonen (eksempelvis `{ "outer": { "inner": "value" } }` blir `json_column:outer:inner::<TYPE>`). 

```sql
CREATE TABLE kommuner_transformert as
    select  
        feature:properties:kommunenavn::STRING as kommunenavn,
        feature:properties:kommunenummer::STRING as kommunenummer,
        ST_ASWKB(TRY_TO_GEOMETRY(feature:geometry)) AS geometry
    from kommuner_unwrapped;
```
  
</details>

### Oppgave 3.3: Slå sammen datasettene

Nå har vi all dataen vi trenger på formatet vi ønsker! Det siste vi da må gjøre er å slå sammen datasettene. 
Som nevnt tidligere trenger vi postnummer-tabellen til å knytte tilsynsdata og kommuner sammen. For å oppnå målet vårt trenger vi følgende kolonner: 

1. `navn`, `dato` og `total_karakter` fra `tilsyn_transformert`-tabellen
3. `kommunenavn`, `kommunenummer` og `geometry` fra `kommuner_transformert`-tabellen

Gjør et forsøk selv!

> **Tips 💡** Dette kan fort bli en lang spørring, så det kan være lurt å dele opp joins i hver sin delspørring ved bruk av `WITH <navn_på_delspørring> AS ...` og deretter bruke `<navn_på_delspørring>` i neste join. Du kan lese mer om `WITH`-clauses [her](https://www.geeksforgeeks.org/sql-with-clause/).

<details>
  <summary>🚨 Løsningsforslag</summary>
    
```sql
CREATE TABLE tilsyn_med_kommune as (
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
```

</details>


Ta en titt på dataen nå. Nå har vi egentlig all data vi trenger til å plotte tilgjengelig!

## DEL 4: Grupper data på kommuner og plott resultatet 📊

### Oppgave 4.1: Karaktersnitt per kommune

Tabellen vår `tilsyn_med_kommune` har nå én rad per tilsyn. Det vi nå trenger å gjøre er å gruppere dataen slik at vi har en gjennomsnittskarakter på hver kommune. Lag en spørring som tar med `kommunenavn`, `geometry`, og gjennomsnittskarakteren av `total_karakter` (avrundet med tre desimaler). Kall den nye tabellen `tilsynskarakter_per_kommune`. 

<details>
  <summary>🚨 Løsningsforslag</summary>

```sql
CREATE TABLE tilsynskarakter_per_kommune as 
    SELECT 
        kommunenavn,
        kommunenummer,
        geometry,
        round(avg(total_karakter), 3) as gjennomsnittlig_karakter
    FROM tilsyn_med_kommune
    GROUP BY kommunenavn, kommunenummer, geometry;
```
  
</details>

Kjør en `SELECT` på den nye tabellen din og naviger deg til høyre kolonne i resultatet. Scroller du nedover finner du mer detaljert info om `gjennomsnittlig_karakter`-kolonnen, som gjennomsnittlig karakter for alle kommuner, distribusjonen av karakterer og prosentvis null-verdier. Vi ser at kolonneverdiene er relativt normaldistribuert, så her blir det kult å plotte!  


### Oppgave 4.2: Plott tilsynskarakter per kommune 
Nå skal vi ta i bruk dataene vi har laget via en snowflake-connector. En connector lar deg koble til Snowflake utenfor plattformen via f.eks en Python-applikasjon. Vi har allerede laget et Python-script for å visualisere dataene i `tilsynskarakter_per_kommune`-tabellen. Scriptet konverterer geometrikolonnen tilbake til GeoJSON fra binærformat. Dette må til for å kunne visualisere dataene i rammeverket `Folium`. Slik gjør du det:

1. For å kunne kjøre scriptet må du først klone repoet
```sh
git clone git@github.com:bekk/snowflake-workshop.git
```

2. Av erfaring varierer Python noe fra maskin til maskin, så jeg anbefaler at dere lager et _virtual environment_ i repoet du nettopp klonet:
```sh
python3 -m venv .venv && source .venv/bin/activate
```

3. Deretter må du installere avhengighetene som trengs. Dette gjør du ved å navigere deg inn i `/visualisering` og kjøre
```sh
pip install -r requirements.txt
```

4. Etter å ha installert avhengighetene må du sette inn de nødvendige parameterene i `main.py`. Finn frem brukernavnet, passordet, database- og skjema-navnet. Fyll disse inn i `connector.connect`-funksjonen.

Når parametererne er ferdig utfylt kjører du følgende kommando i `/visualisering`-mappen

```sh
python main.py
```

Etter kommandoen er ferdigkjørt vil det bli laget en fil `map.html`. Åpne opp filen i en nettleser og du vil se dataene dine plottet på et kart.

Gratulerer - nå kan du vite hvilke kommuner du bør - og absolutt _ikke_ bør - besøke om du er på jakt etter en kulinarisk opplevelse 🍔

## DEL 5: Transformasjoner i dbt

Frem til nå har vi kjørt transformasjonene våre manuelt i et worksheet. Dette er ikke særlig skalerbart når man jobber på prosjekt. Derfor ønsker vi å ta i bruk **dbt**!

**dbt** (data build tool)
