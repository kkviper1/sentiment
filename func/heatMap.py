import MySQLdb
import pandas.io.sql as psql
import folium
from folium.plugins import HeatMap

# setup the database connection.  There's no need to setup cursors with pandas psql.
db=MySQLdb.connect( user='roger', passwd='roger', db='test')

# create the query
query = "select * from Message_Table"

# execute the query and assign it to a pandas dataframe
df = psql.read_sql(query, con=db)

# close the database connection
db.close()

m = folium.Map([26.560000, 75.490000], zoom_start=1)
heat = df[['Latitude', 'Longitude']].as_matrix()
HeatMap(heat).add_to(m)
m.save('map.html')
