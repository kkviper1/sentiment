import MySQLdb
import pandas.io.sql as psql
import folium
from folium.plugins import HeatMap

class heatmap:
        def heatmap(df):
                m = folium.Map([26.560000, 75.490000], zoom_start=1)
                heat = df[['Latitude', 'Longitude']].as_matrix()
                HeatMap(heat).add_to(m)
                m.save('map.html')
