# 4 - Visualisering
I denne delen skal vi se på hvordan man kan konsummere data fra en applikasjon utenfra Snowflake

## 4.1 Oppsett
For å komme deg videre må du installere avhengighetene som trengs for å konsumere data fra Snowflake og visualisere dem ved bruk av Folium. Dette gjør du ved å kjøre
```sh
pip install -r requirements.txt
```

## 4.2 Legg inn dine credentials i main.py 
Etter å ha installert avhengighetene må du sette inn de nødvendige parameterene i main.py. Finn frem brukernavnet, passordet, database- og schemanavnet. Fyll disse inn i `connector.connect`-funksjonen.


## 4.3 Generere kart
Åpne opp terminalen og naviger til denne mappen. Kjør så

```sh
python main.py
```

Etter kommandoen er ferdigkjørt vil det bli laget en map.html. Åpne opp filen i en nettleser og du vil se dataene dine plottet på et kart.
