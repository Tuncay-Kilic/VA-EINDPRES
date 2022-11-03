#!/usr/bin/env python
# coding: utf-8

# ### Eindpresentatie, Serhat_Kokcu-500858425-Tuncay-Kilic-500827104,Umut-Demirtas-500837354

# In[1]:


import pandas as pd
import requests
import json
import datetime
import numpy as np
from shapely.geometry import Point, Polygon
from matplotlib import pyplot
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import branca
import branca.colormap as cm
import streamlit as st
import streamlit_folium
from streamlit_folium import folium_static


# In[2]:


color_map = ["cyan", "darkcyan", "cornflowerblue"] 
st.title('2022-2023 sem-1 Eind presentatie: aardbevingen')
st.header('Eindpresentatie')
st.subheader(' Team 27?: Tuncay, Umut, Serhat,bob') 


# In[3]:


dataframe = pd.read_csv("earthquakes.csv")


# In[4]:


dataframe['place'] = dataframe['place'].astype(str)


# In[5]:


dataframe['placenew'] = dataframe['place'].str.split(',').str[1]
dataframe.head()


# In[6]:


#Vervang NaN met unkown zodat het duidelijk is hoe groot het aandel aan verloren data is.
dataframe.placenew = dataframe.placenew.fillna('unknown')

top10 = dataframe[dataframe["placenew"].str.contains("Papua New Guinea|Indonesia|Chile|Aleutian Islands|Philippines|Japan region|Mexico|Russia|China")]



# In[7]:

st.subheader('In deze blog wordt er geinspecteerd hoeveel aardbevingen er zijn voorgekomen in de afgelopen 100 jaar, ook wordt er bestudeerd hoe aardbevingen en de frequentie ervan veranderd is')
st.subheader('hieronder een boxplot met de magnitude per land') 


# In[8]:


fig_box1 = px.box(top10, x="placenew", y="mag",
                 labels={
                     "mag": "Magnitude",
                     "placenew": "Landen",
                 },
                title="Magnitude t.o.v. land")
fig_box1.show()
st.plotly_chart(fig_box1)


# In[9]:


st.subheader('hieronder een boxplot met de diepte van aardbevingen t.o.v. land') 


# In[10]:


fig_box2 = px.box(top10, x="placenew", y="depth",
                 labels={
                     "depth": "diepte",
                     "placenew": "Land",
                 },
                title="Diepte van aardbeving t.o.v. land")
fig_box2.show()
st.plotly_chart(fig_box2)


# In[11]:


st.subheader('hieronder een boxplot met de datum per aardsbeving verdeeld in landen') 


# In[12]:


fig_box3 = px.box(top10, x="placenew", y="Date",
                 labels={
                     "Date": "Datum",
                     "placenew": "Land",
                 },
                title="Datum per aardsbeving verdeeld in landen")
fig_box3.show()
st.plotly_chart(fig_box3)


# In[13]:


top10x = top10.dropna()


# In[14]:


top10x['year'] = pd.DatetimeIndex(top10x['Date']).year
top10x.head()


# In[15]:


st.subheader('hieronder een scatterplot') 


# In[16]:


fig_scatter = px.scatter(top10x, x="depth", y="mag", animation_frame="year", #animation_group="placenew",
           size="mag", color="placenew", hover_name="placenew",
           log_x=False, size_max=55, range_x=[0,100], range_y=[0,20])

fig_scatter["layout"].pop("updatemenus") # optional, drop animation buttons
fig_scatter.show()
st.plotly_chart(fig_scatter)


# In[17]:


st.subheader('hieronder een histogram') 


# In[18]:


fig_hist = px.histogram(dataframe, x="mag", color="placenew").update_xaxes(categoryorder='total descending',
                title="Aandel van landen in aardbevingen beoordeeld op magnitude")
fig_hist.show()
st.plotly_chart(fig_hist)


# In[19]:


st.subheader('hieronder een histogram met dichtheid')


# In[20]:


figT = px.histogram(dataframe, x="depth", color="placenew", marginal="rug", # can be `box`, `violin`
                         hover_data=dataframe)
figT.show()
st.plotly_chart(figT)


# In[21]:


st.subheader('hieronder een scatterplot met het verband tussen magnitude en diepte van een aardbeving. van de aardbevingen')


# In[22]:


fig_scatter2 = px.scatter(dataframe, x="mag", y="depth",
                 labels={
                     "depth": "Diepte",
                     "mag": "Magnitude"},
                title="Verband tussen magnitude en diepte van een aardbeving. van de aardbevingen")
fig_scatter2.show()
st.plotly_chart(fig_scatter2)


# In[23]:


st.subheader('hieronder een scatterplot met het verband tussen de magnitude en de locatie (longitude) van de aardbevingen')


# In[24]:


fig_scatter3 = px.scatter(top10, x="mag", y="longitude",
                 labels={
                     "depth": "Diepte",
                     "mag": "Magnitude"},
                title="Verband tussen de magnitude en de locatie (longitude) van de aardbevingen")
fig_scatter3.show()
st.plotly_chart(fig_scatter3)


# In[25]:


top10.head()


# In[26]:


newdf = dataframe["placenew"].value_counts()
newdf.head(15)


# In[71]:


stad = st.text_input('stad', 'kayseri')
api_key = "885ad48647fcd8f54a243936ff054f13"
## bron API dataset : https://openweathermap.org
city_name = stad 
                    #bron: https://www.worldatlas.com/articles/cities-most-likely-to-be-hit-by-an-earthquake.html
        

#Let's get the city's coordinates (lat and lon)
url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
print(url)

#Let's parse the Json
req = requests.get(url)
data = req.json()

#Let's get the name, the longitude and latitude
name = data['name']
lon = data['coord']['lon']
lat = data['coord']['lat']
temp = data['main']['temp']
print(name, lon, lat, temp)


# In[72]:


map = folium.Map(location=[lat, lon],zoom_start=10)

clustermod = MarkerCluster().add_to(map)

for row in dataframe.iterrows():
    row_values = row[1]
    popup1 = row_values["place"]
    prefer_canvas=True
    location = [row_values['latitude'], row_values['longitude']]
    marker = folium.Marker(location = location, popup =  row_values['mag'])
    marker.add_to(clustermod)


    #prefer_canvas=True, per locatie zien duurt heel lang om te laden.
    #
    
    
colormap = cm.LinearColormap(colors=['green', 'yellow','darkorange'], index=[0, 50, 100],vmin=0,vmax=220)
colormap.caption = 'Hoeveelheid aardbevingen per sector'
colormap
colormap.add_to(map)

folium_static(map)


# In[29]:


data = newdf = dataframe["placenew"].value_counts()

df1 = pd.DataFrame(data)


# In[30]:


df1.head()


# In[31]:


df1.columns


# In[32]:


df1.reset_index()


# In[58]:


#relevant = df1["placenew"] > 20

relevant = df1[df1['placenew'] >= 20]


# In[59]:



relevant


# In[55]:


st.subheader('barplot met aantal aardbevingen per land')


# In[66]:


#Boxplot om outliers te bepalen.
fig_bar = px.bar(relevant, y="placenew",
                labels={ # replaces default labels by column name
                "placenew": "aantal aardbevingen",  "index": "land",
            }, title= "aantal aardbevingen per land")
fig_bar.show()
st.plotly_chart(fig_bar)


# In[37]:


dataframe['Date'] = pd.to_datetime(dataframe['Date'])


# In[38]:


jaar=dataframe.groupby(dataframe['Date'].dt.year)['mag'].agg(['sum', 'mean', 'max']).reset_index()
jaar


# In[39]:


fig_reg = plt.figure(figsize=(10, 4))
ax=sns.regplot(data=jaar, x='Date', y='sum',
            fit_reg=True,scatter=True,
           color= 'green')

ax.set(title="Lineaire regressie, aantal aardbevingen per jaar",
      xlabel= "jaar", ylabel='Aantal aardbevingen')

st.pyplot(fig_reg)


# In[ ]:





# ### wat zien we hier?

# In[40]:


st.subheader('er is een positieve correlatie met stijging in jaar en aantal aardbevingen.')


# In[41]:


fig_ = go.Figure()

fig_.add_trace(
    go.Scatter(x=jaar['Date'],
               y=jaar['sum'],
               name="sum",
               mode='markers',
               showlegend = True,
               marker_symbol='circle',
               marker_color= 'red'))

fig_.add_trace(
    go.Scatter(x=jaar['Date'],
               y=jaar['mean'],
               name="mean",
               mode='markers',
               visible=False,
               showlegend = True,
               marker_color= 'black',
               marker_symbol='triangle-left-open-dot',))

fig_.add_trace(
    go.Scatter(x=jaar['Date'],
               y=jaar['max'],
               name="max",
               mode='markers',
               showlegend = True,
               visible=False,
               marker_color= 'purple',
               marker_symbol='x-open-dot',))


fig_.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="sum",
                     method="update",
                     args=[{"visible": [True, False, False,]},
                           {"title": "sum"}]),
                dict(label="mean",
                     method="update",
                     args=[{"visible": [False, True, False,]},
                           {"title": "mean"}]),
                dict(label="max",
                     method="update",
                     args=[{"visible": [False, False, True,]},
                           {"title": "max"}]),
                    ]),
        )
    ])

fig_.update_xaxes(range=[1900, 2020])
# Add annotation
fig_.update_layout(
    annotations=[
        dict(text=":", showarrow=False,
        x=0, y=1.085, yref="paper", align="left")
    ]
)

fig_.show()
st.plotly_chart(fig_)


# In[68]:


import plotly.express as px

df = px.data.tips()
fig_tren = px.scatter(jaar, x="Date", y="sum", trendline="ols")
fig_tren.show()

results = px.get_trendline_results(fig_tren)
RSQ = px.get_trendline_results(fig_tren).px_fit_results.iloc[0].rsquared
print(results)

resultsF = results.iloc[0]["px_fit_results"].summary()


# In[69]:


st.write("The R-Squared value is ",RSQ)
print("The R-Squared value is ",RSQ)


# In[70]:


st.write(resultsF)
print(resultsF)

