# A module used to create a heatmap of the users belonging to various regions of the world using latitude and longitude
import folium
from folium.plugins import HeatMap
import pandas as pd

class heatmap:
    def heatmap(df):
        posLat=[]
        posLong=[]
        negLat=[]
        negLong=[]
        neuLat=[]
        negLong=[]
        m = folium.Map([26.560000, 75.490000], zoom_start=1)  # The coordinates that are used to map the various users within certain latitudes and longitudes
        heat1 = df[['Latitude', 'Longitude']].as_matrix()

        HeatMap(heat1).add_to(m)
        m.save('map.html') # Saving the heatmap created as a html file
        for row,i in enumerate(df["Category"]):
            if df.loc[row,'Category'] == 'Neutral':
                neuLat.append(df.loc[row,"Latitude"])
                neuLong.append(df.loc[row, "Longitude"])
            elif df.loc[row,'Category']== 'Positive':
                posLat.append(df.loc[row,"Latitude"])
                posLong.append(df.loc[row,"Longitude"])
            elif df.loc[row,'Category'] == 'Negative':
                neuLat.append(df.loc[row, "Latitude"])
                neuLong.append(df.loc[row, "Longitude"])
        df1 = pd.DataFrame(list(zip(posLat,posLong)),columns =['Latitude', 'Longitude'])
        df2 = pd.DataFrame(list(zip(negLat, negLong)), columns=['Latitude', 'Longitude'])
        df3 = pd.DataFrame(list(zip(neuLat, neuLong)), columns=['Latitude', 'Longitude'])

for row,i in enumerate(df1):
    folium.Marker(location=[45.3288, -121.6625],icon=folium.Icon(color='green')).add_to(m)
for row,i in enumerate(df2):
    folium.Marker(location=[45.3288, -121.6625], icon=folium.Icon(color='red')).add_to(m)
for row,i in enumerate(df3):
    folium.Marker(location=[45.3288, -121.6625], icon=folium.Icon(color='yellow')).add_to(m)




