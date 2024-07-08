from snowflake import connector
import pandas as pd

from map_utils import generate_map

conn = connector.connect(
    user="<<snowflake_brukernavn>>",
    password="<<snowflake_passord>>",
    account="so28625.europe-west4.gcp",
    warehouse="COMPUTE_WH",
    database="<<din_database>>",
    schema="<<ditt_schema>>"
)

def perform_snowflake_query(sql_query: str) -> pd.DataFrame:
    with conn.cursor() as cur:
        return cur.execute(sql_query).fetch_pandas_all()


dataframe = perform_snowflake_query("""
SELECT * EXCLUDE(GEOMETRY), ST_ASGEOJSON(ST_GEOMETRYFROMWKB(GEOMETRY)) AS GEOMETRY
FROM TILSYNSKARAKTER_PER_KOMMUNE;
""")

m = generate_map(dataframe)
m.save('map.html')
