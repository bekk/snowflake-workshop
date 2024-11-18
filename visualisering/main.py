from snowflake import connector
import pandas as pd

from map_utils import generate_map

conn = connector.connect(
    user="<<snowflake_brukernavn>>",
    password="<<snowflake_passord>>",
    account="urcgqra-gu27095",
    warehouse="<ditt_warehouse>",
    database="<din_database>",
    schema="<ditt_schem>"
)

def perform_snowflake_query(sql_query: str) -> pd.DataFrame:
    with conn.cursor() as cur:
        return cur.execute(sql_query).fetch_pandas_all()


dataframe:pd.DataFrame = perform_snowflake_query("""
SELECT * EXCLUDE(GEOMETRY), ST_ASGEOJSON(ST_TRANSFORM(ST_GEOMETRYFROMWKB(GEOMETRY, 25833), 4326)) AS GEOMETRY
FROM TILSYNSKARAKTER_PER_KOMMUNE;
""")

m = generate_map(dataframe)
m.save('map.html')
