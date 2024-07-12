# --------------------LIBRERÍAS-----------------------------------------------#

import streamlit as st
from streamlit_option_menu import option_menu
import base64
import numpy as np
import pandas as pd
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import os
import json
from PIL import Image
import requests

# interactive maps
import folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium
from branca.colormap import LinearColormap
from folium.plugins import HeatMap
from folium.features import GeoJsonTooltip
import streamlit.components.v1 as components

# Plotly graphs
import plotly.graph_objs as go
import plotly_express as px

# AB testing
from scipy import stats
from scipy.stats import shapiro
from scipy.stats import normaltest
from scipy.stats import mannwhitneyu

# KNN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


# --------------------SITE CONFIGURATION-------------------------------------#

st.set_page_config(page_title='Best cities to live',
                   layout='wide',
                   page_icon='🌎')

# ---------------------BACKGROUND IMAGE---------------------------------------#


# def change_opacity(input_image_path, output_image_path, opacity):

    #img = Image.open(input_image_path).convert("RGBA")
    
    #datas = img.getdata()
    
    #new_data = []
    #for item in datas:
        #new_data.append((item[0], item[1], item[2], int(item[3] * opacity)))
    
    #img.putdata(new_data)
    
    #img.save(output_image_path, "PNG")

input_image_path = "img\img.png"
output_image_path = "img\img_2.png"
opacity = 0.3  # 50% de opacidad

#change_opacity(input_image_path, output_image_path, opacity)


def add_bg_from_local(image_file, position):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
            .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
            background-position: {position};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("img/img_2.png", position="top")
 
# ----------------------TITLE-----------------------------------------------#

logo = 'img/mapa_logo.png'

st.markdown(
    f"""
    <div style="display: flex; justify-content: center; align-items: center; text-align: center; margin-bottom: 50px;">
        <img src="data:image/png;base64,{base64.b64encode(open(logo, 'rb').read()).decode()}" style="width: 100px; height: auto; margin-right: 20px;">
        <h1 style='font-family: Lato; font-size: 50px;'>Analysis of the best cities to live</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Configuración del menú
page = option_menu(None, 
    ["Introduction", "Top10", "Environment", "Economy", "Rating", "Your best place", "Conclusions"], 
    icons=["info-circle", "trophy", "tree", "coin", "star", "heart", "clipboard-check"], 
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"}, 
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "0px", "--hover-color": "#FFD580","padding": "0px",
                     #"font-weight": "bold", #"display": "flex",
                     "align-items": "center","justify-content": "center", "height": "100px"},
        "nav-link-selected": {"background-color": "#FFD580"},
        "icon": {"color": "#9bc27e", "font-size": "30px", "margin": "auto", "display": "block"}})

# --------------------DATA LOADING-----------------------------------------------#

city_df = pd.read_csv("clean_data/city_df.csv")
city_world_AQI = pd.read_csv("clean_data/city_world_AQI.csv")
countries_df = pd.read_csv("clean_data/countries_df.csv")

####################################  PAGE 1  ######################################

if page == "Introduction":

    st.write("")

    st.markdown("""
    <h1 style='text-align: center;'>Introduction</h1>
""", unsafe_allow_html=True)
    
    st.markdown("""
            <p style='font-size:35px; text-align: center; color:green; font-style:italic; margin:0;'>
            <strong>Have you ever wondered which is the best city to live in?</strong></p>
            
            <p style='font-size:25px; text-align: center; color:black; font-style:italic; margin:0;'>
            <strong>We know that this decision can be overwhelming, with so many options and factors to consider.</strong></p>
                
            <p style='font-size:25px; text-align: center; color:black; font-style:italic; margin:0;'>
            <strong>That’s why we’ve created this app specifically designed to help you find your ideal city, whether for living or traveling.</strong></p>
                
            <p style='font-size:25px; text-align: center; color:black; font-style:italic; margin:0;'>
            <strong>Our tool is designed to make your search easy and effective, providing you with all the information you need to
            make an informed and personalized decision.</strong></p>
            """, 
            unsafe_allow_html=True)

    st.markdown("""
            <p style='font-size:50px; color:black; text-align: center;'>
            🌎
            </p>
            """,
            unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])

    with col2:

    # Random imagenes 

    # Unsplash API access key
        access_key = '62QWPpkPYOpWWKoUjSAPIvLqe_myc3HddfM3EjlI724'

        def get_random_photo(country="city"):
            try:
                response = requests.get(f"https://api.unsplash.com/photos/random?query={country}+city&client_id={access_key}")
            
                # Check if the request was successful
                if response.status_code == 200:
                    # Get JSON data from the response
                    data = response.json()
                    # Return the photo URL
                    return data["urls"]["regular"]
                else:
                    st.error(f"Failed to fetch an image. Error: {response.text}")
                    return None
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to fetch an image. Error: {str(e)}")
                return None

        def main():
            st.markdown("""
                <p style='font-size:25px; text-align: center; color:green; margin:0;'>
                <strong>Random Photos of Countries Around the World</strong></p>""", unsafe_allow_html=True)

            st.markdown("""
                <p style='font-size:20px; text-align: center; color:black; margin-bottom:0px;'>
                Enter the name of a country:</p>""", unsafe_allow_html=True)

            #Input for user to enter a city name
            country = st.text_input("", "")

            # Botón para activar la búsqueda
                
            # Estilos CSS para el botón y el input
            st.markdown("""
    <style>
        .st-0 {
            height: 40px !important;
            font-size: 20px !important;
            padding: 10px !important;
            background-color: #E6F0E8 !important;
            border-color: #5CB85C !important;
            color: #3C763D !important;
        }
        .stButton > button {
            background-color: #5CB85C !important;
            color: white !important;
            font-size: 20px !important;
            font-weight: bold !important;
            margin-top : -10px;
        }
        .stButton > button:hover {
            background-color: #449D44 !important;
        }
        .stButton {
            display: flex;
            justify-content: center;
        }
    </style>
    """, unsafe_allow_html=True)
            

            if st.button('Search'):
                if country.strip() == "":
                    st.warning("Please select a country")
                else:
                    #Create the variable photo_url and assign it the result of the get_random_photo() function
                    photo_url = get_random_photo(country)
        
                    #Check if a valid photo URL was obtained
                    if photo_url:

                        col1, col2, col3 = st.columns(3)
                        
                        st.image(photo_url, width=600, use_column_width=True)
                        st.write(
                                "<div style='text-align:right;color:red;font-size:14px'>Generated using Unsplash API</div>",
                        unsafe_allow_html=True)

        if __name__ == "__main__":
                            main()
   

####################################  PAGE 2  ######################################

elif page == "Top10":

        tab1, tab2, tab3 = st.tabs([
        "Cities under evaluation",
        "Top 10 best cities",
        "Happiness evolution"])
        
        with tab1:

            st.title('Cities under analysis')
            col1, col2 = st.columns(2)

            with col1:
                st.write('***Cities under the analysis***')             
                with open('HTML/cities_per_continent.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    st.components.v1.html(html_content, height=500)
            

            with col2:
                st.markdown('***You can zoom in/out and move it around:***')
                with open('HTML/cities_worldmap.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    st.components.v1.html(html_content, height=500)

            st.write('----')

            # Para que el usuario chequee si una ciudad especifica se analizo

            st.title('Check if a specific city was considered in the analysis:')

            # Botón para activar la búsqueda
            
            # Estilos CSS para el botón y el input
            st.markdown("""<style>.st-0 {
         height: 40px !important;
         font-size: 20px !important;
         padding: 10px !important;
         background-color: #E6F0E8 !important;
         border-color: #5CB85C !important;
         color: #3C763D !important;}
     .stButton > button {
         background-color: #5CB85C !important;
         color: white !important;
         font-size: 20px !important;
         font-weight: bold !important;}
     .stButton > button:hover {
         # background-color: #449D44 !important;}
     </style>""", unsafe_allow_html=True)
            
            city_name = st.text_input("Enter the city name to check if it was evaluated:")

            if st.button('Search'):
                # Convertir todos los nombres de ciudades en el dataset a minúsculas
                city_df['City_lower'] = city_df['City'].str.lower()

                # Función para verificar si la ciudad está en el dataset (ignorando mayúsculas/minúsculas)
                def check_city_exists(city_name):
                    if city_name:
                        city_name_lower = city_name.strip().lower()
                        if city_name_lower in city_df['City_lower'].values:
                            return True
                    return False

                # Verificar si la ciudad está en el dataset
                if check_city_exists(city_name):
                    st.success(f"The city '{city_name}' is part of the evaluated cities \U00002714")
                    city_data = city_df[city_df['City_lower'] == city_name.strip().lower()]
                    st.dataframe(city_data.drop(columns=['City_lower', 'lat', 'lng', 'AQI Value', 'Internet Access', 'Venture Capital', 'Taxation']).reset_index(drop=True))
                    
                    st.markdown('<u><i>Definition:</i></u>', unsafe_allow_html=True)
                    st.write('**Range from 0 to 10, with the larger numbers indicating higher desirability to live.**')
                    st.markdown("""
                                - `Housing`: Rating about affordability of houses in the city.
                                - `Cost of Living`: The expense of living in the city.
                                - `Startups`: The presence or number of startup companies in the city.
                                - `Travel Connectivity`: The ease of travel to and from the city, including transportation infrastructure and connectivity.
                                - `Commute`: The average time and ease of commuting within the city.
                                - `Business Freedom`: The level of freedom to conduct business activities in the city.
                                - `Safety`: The safety and security level in the city.
                                - `Healthcare`: The quality and availability of healthcare services in the city.
                                - `Education`: The quality and availability of educational institutions and services in the city.
                                - `Environmental Quality`: The quality of the environment in the city, including pollution levels and green spaces.
                                - `Economy`: The economic strength and stability of the city, including job opportunities and economic growth.
                                - `Leisure & Culture`: The availability and quality of leisure and cultural activities in the city.
                                - `Tolerance`: The level of tolerance and acceptance of diversity in the city.
                                - `Outdoors`: The availability and quality of outdoor activities and natural environments in and around the city.
                                - `AQI Category`: The category or classification of the air quality based on the AQI value, such as Good, Moderate, Unhealthy, etc.
                                """, unsafe_allow_html=True)

                elif city_name:
                    st.warning(f"The city '{city_name}' is NOT part of the analysis.")

        #------------- TAB 2 ---------------#

        with tab2:

            st.title('Top 10 rankings')

            col1, col2= st.columns(2)

            with col1:

                # Graph 1

                top_10_safest_cities = city_df.nlargest(10, 'Safety')
                colors = ['#4e6f43','#668f4f','#7fa465','#9bc27e','#b2cb91', '#c5e384', '#b3e1a7', '#a7e58e', '#d9f08c', '#e6f2b2', '#bbf1b1']
                fig = px.bar(top_10_safest_cities, 
                            x='Safety', 
                            y='City', 
                            color='Country', 
                            color_discrete_sequence=colors,
                            orientation='h',
                            title='Top 10 Safety',
                            labels={'Safety': 'Safety Score', 'City': 'City'},
                            height=400, 
                            width=650)
                fig.update_layout(xaxis_title='',
                                yaxis_title='City',
                                yaxis_categoryorder='total ascending',
                                xaxis_showgrid=False,
                                yaxis_showgrid=False,
                                template='plotly_white',
                                xaxis_tickvals=[])
                st.plotly_chart(fig)

                # Graph 2

                top_10_education = city_df.nlargest(10, 'Education')
                colors = ['#aec6cf', '#a3c1da', '#a1c4f2', '#9fdaf6', '#a4d8e5', '#92d6e9', '#99e2f2', '#b3e5f5', '#b1e4f7', '#c0f7ff']
                fig = px.bar(top_10_education,
                            x='Education',
                            y='City', 
                            color='Country', 
                            color_discrete_sequence=colors,
                            orientation='h',
                            title='Top 10 Education',
                            labels={'Education': 'Eduation Score', 'City': 'City'},
                            height=400,
                            width=650) 

                fig.update_layout(xaxis_title='',
                                yaxis_title='City',
                                yaxis_categoryorder='total ascending',
                                xaxis_showgrid=False,
                                yaxis_showgrid=False,
                                template='plotly_white',
                                xaxis_tickvals=[])
                st.plotly_chart(fig)

                # Graph 3

                top_10_economy = city_df.nlargest(10, 'Economy')
                colors = ['#ff6961', '#ffb3b3', '#ffbdbd', '#ff9aa2', '#ffacb7', '#ffafb0', '#ffada5', '#ffcccb', '#ffb7c5', '#ffccd5']
                fig = px.bar(top_10_economy,
                            x='Economy',
                            y='City',
                            color='Country',
                            color_discrete_sequence=colors,
                            orientation='h',
                            title='Top 10 Economy',
                            labels={'Economy': 'Economy Score', 'City': 'City'},
                            height=400,
                            width=650) 
                fig.update_layout(xaxis_title='',
                                yaxis_title='City',
                                yaxis_categoryorder='total ascending',
                                xaxis_showgrid=False,
                                yaxis_showgrid=False,
                                template='plotly_white',
                                xaxis_tickvals=[] )
                st.plotly_chart(fig)

                 # Graph 4

                top_10_costliving = city_df.nlargest(10, 'Cost of Living')
                colors = ['#cba3d8', '#dab4de', '#e1c3e8', '#e0bfe9', '#e6c9f2', '#d9a7e3', '#ddc1ef', '#e6c2f7', '#e3a8ff', '#ddb5e7']
                fig = px.bar(top_10_costliving,
                            x='Cost of Living',
                            y='City',
                            color='Country',
                            color_discrete_sequence=colors,
                            orientation='h',
                            title='Top 10 Cost of Living',
                            labels={'Cost of Living': 'Cost of Living Score', 'City': 'City'},
                            height=400,
                            width=650) 
                fig.update_layout(xaxis_title='',
                                yaxis_title='City',
                                yaxis_categoryorder='total ascending',
                                xaxis_showgrid=False,
                                yaxis_showgrid=False,
                                template='plotly_white',
                                xaxis_tickvals=[])
                st.plotly_chart(fig)

            with col2:

                 # Graph 5

                top_10_environment = city_df.nlargest(10, 'Environmental Quality')

                colors = ['#ffb347', '#ffd1b2', '#ffd1a3', '#ffb994', '#ffcc99', '#ffdab3', '#ffddb1', '#ffd9c2', '#ffe0a1', '#ffd2b2']
                fig = px.bar(top_10_environment,
                            x='Environmental Quality',
                            y='City', 
                            color='Country',
                            color_discrete_sequence=colors,
                            orientation='h',
                            title='Top 10 Environmental Quality',
                            labels={'Environmental Quality': 'Environmental Quality Score', 'City': 'City'},
                            height=400,
                            width=650) 
                fig.update_layout(xaxis_title='',
                                yaxis_title='City',
                                yaxis_categoryorder='total ascending',
                                xaxis_showgrid=False,
                                yaxis_showgrid=False,
                                template='plotly_white',
                                xaxis_tickvals=[])
                st.plotly_chart(fig)

                # Graph 6

                top_10_leisure = city_df.nlargest(10, 'Leisure & Culture')
                colors = ['#ffb3ba', '#ffccd5', '#ffc9de', '#ff9aa2', '#ffacb7', '#ffb6c1', '#ffd1d9', '#ffc9cb', '#ffb0c7', '#ffc0cb']
                fig = px.bar(top_10_leisure,
                            x='Leisure & Culture',
                            y='City',
                            color='Country',
                            color_discrete_sequence=colors,
                            orientation='h',
                            title='Top 10 of Leisure & Culture',
                            labels={'Leisure & Culture': 'Leisure & Culture Score', 'City': 'City'},
                            height=400,
                            width=650) 
                fig.update_layout(xaxis_title='',
                                yaxis_title='City',
                                yaxis_categoryorder='total ascending',
                                xaxis_showgrid=False,
                                yaxis_showgrid=False,
                                template='plotly_white',
                                xaxis_tickvals=[])
                st.plotly_chart(fig)

                # Graph 7

                top_10_connectivity = city_df.nlargest(10, 'Travel Connectivity')
                colors = ['#77ddcc', '#a0e6d9', '#adeeee', '#b2f4e8', '#99ffcc', '#a3f7e8', '#b1e5e9', '#c8ffff', '#bbf6f6', '#ace7e7']
                fig = px.bar(top_10_connectivity,
                            x='Travel Connectivity',
                            y='City',
                            color='Country',
                            color_discrete_sequence=colors,
                            orientation='h',
                            title='Top 10 of Travel Connectivity',
                            labels={'Travel Connectivity': 'Travel Connectivity Score', 'City': 'City'},
                            height=400,
                            width=650)
                fig.update_layout(xaxis_title='',
                                yaxis_title='City',
                                yaxis_categoryorder='total ascending',
                                xaxis_showgrid=False,
                                yaxis_showgrid=False,
                                template='plotly_white',
                                xaxis_tickvals=[])
                st.plotly_chart(fig)

                 # Graph 8

                top_10_connectivity = city_df.nlargest(10, 'Healthcare')

                colors = '#bf9000','#ffe599','#ffd966', '#FFD580'
                fig = px.bar(top_10_connectivity,
                            x='Healthcare',
                            y='City',
                            color='Country',
                            color_discrete_sequence=colors,
                            orientation='h',
                            title='Top 10 of Healthcare',
                            labels={'Healthcare': 'Healthcare Score', 'City': 'City'},
                            height=400,
                            width=650) 
                fig.update_layout(xaxis_title='',
                                yaxis_title='City',
                                yaxis_categoryorder='total ascending',
                                xaxis_showgrid=False,
                                yaxis_showgrid=False,
                                template='plotly_white',
                                xaxis_tickvals=[])
                st.plotly_chart(fig)

        #------------- TAB 3 ---------------#
        
        with tab3:

            st.title('Happiness evolution')

            country_options = ['All'] + list(countries_df['Country'].unique())
            selected_countries = st.multiselect("🌍 Select one or more countries", options=country_options, default=['Argentina'])

            # Filtrar los datos según la selección del usuario
            if 'All' in selected_countries:
                filtered_df = countries_df
            else:
                filtered_df = countries_df[countries_df['Country'].isin(selected_countries)]

            col1, col2 = st.columns(2)

            with col1:

                fig = px.line(filtered_df,
                                        x='year',
                                        y='Life Ladder',
                                        color='Country',
                                        title=f'Evolution of Life Ladder by Year')
                                    
                fig.update_layout(
                                xaxis=dict(
                                    tickmode='linear',
                                    dtick=1,  # Asegura que cada año esté etiquetado
                                    showgrid=False),
                                    yaxis=dict(showgrid=False),
                                    width=800)
                            
                st.plotly_chart(fig)

            with col2:

                st.write('')
                st.write('')
                
                st.markdown("""
            <p style='font-size:25px; color:black; text-align: justify;'>
            <strong>Life Ladder score:</strong><br>
            A measure of subjective well-being, reflecting individuals' overall satisfaction with life. <br>""",
            unsafe_allow_html=True)
                
                st.markdown("""
            <p style='font-size:25px; color:black; text-align: justify;'>
            The <strong>best possible life</strong> being a 10, and the <strong>worst possible life</strong> being a 0.
            </p>
            """,unsafe_allow_html=True)
                


####################################  PAGE 3  ######################################

elif page == "Environment":

    st.title('Air Quality worldwide comparison')

    col1, col2, col3 = st.columns(3)

    with col1:
        with open('HTML/AQI_worldmap.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
            st.components.v1.html(html_content, height=500, width=1000)

    with col3:
        st.image('img/AQI_std.png', width=400)

        # Para que el usuario busque por pais que le interese:
        
        st.write('')
        st.write('')
        st.write('')
            
        # Entrada de texto para que el usuario ingrese el nombre del país
        country_name = st.text_input('Check the AQI for a specific country:', '')

        # Estilos CSS para el botón y el input
        st.markdown("""<style>.st-0 {
            eight: 40px !important;
            font-size: 20px !important;
            padding: 10px !important;
            background-color: #E6F0E8 !important;
            border-color: #5CB85C !important;
            color: #3C763D !important;}
        .stButton > button {
            background-color: #5CB85C !important;
            color: white !important;
            font-size: 20px !important;
            font-weight: bold !important;}
        .stButton > button:hover {
            # background-color: #449D44 !important;}
        </style>""", unsafe_allow_html=True)

        # Botón para activar la búsqueda
        if st.button('Search'):
            # Convertir el nombre del país ingresado por el usuario a minúsculas para evitar problemas de mayúsculas/minúsculas
            country_name_lower = country_name.strip().lower()
        
            # Buscar el valor de AQI correspondiente al país ingresado por el usuario
            aqi_value = city_world_AQI.loc[city_world_AQI['Country'].str.lower() == country_name_lower, 'AQI Value'].values
        
            if len(aqi_value) > 0:
                st.success(f"The AQI value for '{country_name.capitalize()}' is {aqi_value[0]}")
            else:
                st.warning(f"Country '{country_name.capitalize()}' not found or no AQI value available.")

    st.write('----')

    st.markdown("### City comparison on Air Quality:")

    selected_continents = st.multiselect('🌍 Select continent(s):', ['All Continents'] + list(set(city_df['Continent'].unique())), default='All Continents')
    
    if 'All Continents' in selected_continents:
        country_options = ['All countries'] + list(set(city_df['Country'].unique()))
    else:
        country_options = ['All countries'] + list(set(city_df[city_df['Continent'].isin(selected_continents)]['Country'].unique()))

    selected_countries = st.multiselect('🌍 Select countries:', options=country_options, default='All countries')

    if 'All Continents' in selected_continents and 'All countries' in selected_countries:
        df_filtered = city_df
    elif 'All Continents' not in selected_continents and 'All countries' in selected_countries:
        df_filtered = city_df[city_df['Continent'].isin(selected_continents)]
    elif 'All Continents' in selected_continents and 'All countries' not in selected_countries:
        df_filtered = city_df[city_df['Country'].isin(selected_countries)]
    else:
        df_filtered = city_df[(city_df['Continent'].isin(selected_continents)) & (city_df['Country'].isin(selected_countries))]

    selected_cities = st.multiselect('🌍 Select cities:', options=['All cities'] + list(set(df_filtered['City'].unique())), default='All cities')

    if 'All cities' in selected_cities:
        df_final = df_filtered
    else:
        df_final = df_filtered[df_filtered['City'].isin(selected_cities)]


    # AQI value per city
    city_df_sorted_AQI = df_final.sort_values(by='AQI Value', ascending=False)

    fig = px.bar(city_df_sorted_AQI,
                    x='City',
                    y='AQI Value',
                    color='Country',
                    title='AQI Value per city',
                    labels={'AQI Value': 'AQI Value', 'City': 'City'},
                    height=600, 
                    width=1500) 

    fig.update_layout(xaxis_showgrid=False,
                        yaxis_showgrid=False,
                        template='plotly_white')  
        
    st.plotly_chart(fig)

####################################  PAGE 4  ######################################

elif page == "Economy":
    st.title("Business comparison")

    selected_continents = st.multiselect('🌍 Select continent(s):', ['All Continents'] + list(city_df['Continent'].unique()), default='All Continents')

    if 'All Continents' in selected_continents:
        country_options = ['All countries'] + list(city_df['Country'].unique())
    else:
        country_options = ['All countries'] + list(city_df[city_df['Continent'].isin(selected_continents)]['Country'].unique())

    selected_countries = st.multiselect('🌍 Select countries:', options=country_options, default='All countries')

    # Filtrar el DataFrame según las selecciones de continentes y países
    if 'All Continents' in selected_continents and 'All countries' in selected_countries:
        df_economy = city_df
    elif 'All Continents' not in selected_continents and 'All countries' in selected_countries:
        df_economy = city_df[city_df['Continent'].isin(selected_continents)]
    elif 'All Continents' in selected_continents and 'All countries' not in selected_countries:
        df_economy = city_df[city_df['Country'].isin(selected_countries)]
    else:
        df_economy = city_df[(city_df['Continent'].isin(selected_continents)) & (city_df['Country'].isin(selected_countries))]

    selected_cities = st.multiselect('🏙️ Select cities:', options=['All cities'] + list(df_economy['City'].unique()), default='All cities')

    if 'All cities' in selected_cities:
        df_final = df_economy
    else:
        df_final = df_economy[df_economy['City'].isin(selected_cities)]

    # Ordenar el DataFrame por AQI Value en orden descendente
    df_final = df_final.sort_values(by='AQI Value', ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        
        # Startups per city 

        city_df_sorted_startups = df_final.sort_values(by='Startups', ascending=False)

        fig = px.bar(
            city_df_sorted_startups,
            x='City',
            y='Startups',
            color='Country',
            title='Startups per city',
            labels={'Startups': 'Startups', 'City': 'City'},
            height=400, 
            width=800)

        fig.update_layout(
            xaxis_title='',
            yaxis_title='',
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            template='plotly_white')

        st.plotly_chart(fig)

    with col2:
        
        # Business Freedom per city 
        city_df_sorted_business = df_final.sort_values(by='Business Freedom', ascending=False)

        fig = px.bar(
            city_df_sorted_business,
            x='City',
            y='Business Freedom',
            color='Country',
            title='Business Freedom per city',
            labels={'Business Freedom': 'Business Freedom', 'City': 'City'},
            height=400, 
            width=800)

        fig.update_layout(
            xaxis_title='',
            yaxis_title='',
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            template='plotly_white')

        st.plotly_chart(fig)

    st.markdown("""<p style='font-size:40px; text-align: left; color:black; margin:0;'>
                    <strong>Correlation between "Business Freedom" and "Startups"</strong></p>""",
                    unsafe_allow_html=True)
                
    st.markdown("""<p style='font-size:25px; text-align: left; color:black; font-style:italic; margin:0;'>
                    After the assessment using Spearman's test I can confirm that both variables
                    are dependant which confirms that <strong>the number of startups in a city depends on the business freedom.</p>""",
                    unsafe_allow_html=True)
    
    st.write('')

    #--------------------- AB TESTING-------------------------------#

    st.markdown("""
                <p style='font-size:40px; text-align: left; color:black; margin:0;'>
                <strong>Applying A/B Testing: check if there's a significant difference between the mean values of Business Freedom:</strong></p>""",
                unsafe_allow_html=True)
    
    st.markdown("""
                <p style='font-size:20px; text-align: left; color:black; margin:0;'>
                Select <strong>only 2 continents</strong> to do the A/B testing for Business Freedom:.</p>""",
                unsafe_allow_html=True)
        
    selected_continents = {
        'North America': st.checkbox('North America'),
        'Central America': st.checkbox('Central America'),
        'South America': st.checkbox('South America'),
        'Europe': st.checkbox('Europe'),
        'Oceania': st.checkbox('Oceania'),
        'Asia': st.checkbox('Asia'),
        'Africa': st.checkbox('Africa')
    }

    # Filtrar continentes seleccionados
    selected = [continent for continent, is_selected in selected_continents.items() if is_selected]

    # Validar la selección
    if len(selected) == 2:
        df_final = city_df[city_df['Continent'].isin(selected)]
        st.success(f'You selected: {", ".join(selected)}')
        
        # Creo los grupos basados en la selección del usuario
        grupo1 = city_df[city_df['Continent'] == selected[0]]['Business Freedom']
        grupo2 = city_df[city_df['Continent'] == selected[1]]['Business Freedom']
        
        def analisis_preliminar(grupo1, grupo2, alpha=0.05):
            # Prueba de Shapiro-Wilk para normalidad
            stat, p_norm1 = stats.shapiro(grupo1)
            stat, p_norm2 = stats.shapiro(grupo2)
            
            # Prueba de Levene para igualdad de varianzas
            stat, p_levene = stats.levene(grupo1, grupo2)
            
            # Prueba de Mann-Whitney
            u_stat, p_utest = stats.mannwhitneyu(grupo1, grupo2)
            st.write(f"Test of Mann-Whitney: p-value = {p_utest}")
            
            # Evaluar el resultado de Mann-Whitney
            if p_utest > 0.05:
                st.markdown(f"""
                    <p style='font-size:20px; text-align: left; color:black; margin:0;'>
                    Considering that the <b>p-value is >0.05:</b> there is <b>NO significant difference</b> between the averages on Business Freedom for {selected[0]} and {selected[1]}.</p>""",
                    unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <p style='font-size:20px; text-align: left; color:black; margin:0;'>
                    Considering that the <b>p-value is <0.05:</b> there is a significant difference between the averages on Business Freedom for {selected[0]} and {selected[1]}.</p>""",
                    unsafe_allow_html=True)

        # Realizar el análisis preliminar
        analisis_preliminar(grupo1, grupo2)

    elif len(selected) > 2:
        st.error('Please, select only 2 continents.')
    else:
        st.warning('Please, select exactly 2 continents.')

            
####################################  PAGE 5  ######################################

elif page == "Rating":

        st.title('City rating')
        st.subheader('From 0 to 10 with the larger numbers indicating higher desirability to live.')

        # --------------------SIDEBAR-------------------------------------#

        st.sidebar.image('img/img_world.jpg', use_column_width=True)
        st.sidebar.title("Filters")
        st.sidebar.write('-------')

        continent_options = ['All'] + list(city_df['Continent'].unique())
        selected_continents = st.sidebar.multiselect("Select Continents", options=continent_options, default=["Europe"])

        # Se filtran los países según los continentes seleccionados o mostrar todos los países si se selecciona "All"
        if 'All' in selected_continents:
            country_options = ['All'] + list(city_df['Country'].unique())
        else:
            country_options = ['All'] + list(city_df[city_df['Continent'].isin(selected_continents)]['Country'].unique())

        selected_countries = st.sidebar.multiselect("Select Countries", options=country_options, default="All")

        # Filtrar ciudades según países seleccionados
        if 'All' in selected_countries:
            city_options = ['All'] + list(city_df['City'].unique())
        else:
            city_options = ['All'] + list(city_df[city_df['Country'].isin(selected_countries)]['City'].unique())

        selected_cities = st.sidebar.multiselect("Select Cities", options=city_options, default="All")


        # Se filtra los datos según la selección del usuario
        if 'All' in selected_continents and 'All' in selected_countries and 'All' in selected_cities:
            filtered_df = city_df
        elif 'All' not in selected_continents and 'All' in selected_countries and 'All' in selected_cities:
            filtered_df = city_df[city_df['Continent'].isin(selected_continents)]
        elif 'All' in selected_continents and 'All' not in selected_countries and 'All' in selected_cities:
            filtered_df = city_df[city_df['Country'].isin(selected_countries)]
        elif 'All' in selected_continents and 'All' in selected_countries and 'All' not in selected_cities:
            filtered_df = city_df[city_df['City'].isin(selected_cities)]
        elif 'All' not in selected_continents and 'All' not in selected_countries and 'All' in selected_cities:
            filtered_df = city_df[(city_df['Continent'].isin(selected_continents)) & (city_df['Country'].isin(selected_countries))]
        elif 'All' not in selected_continents and 'All' in selected_countries and 'All' not in selected_cities:
            filtered_df = city_df[(city_df['Continent'].isin(selected_continents)) & (city_df['City'].isin(selected_cities))]
        elif 'All' in selected_continents and 'All' not in selected_countries and 'All' not in selected_cities:
            filtered_df = city_df[(city_df['Country'].isin(selected_countries)) & (city_df['City'].isin(selected_cities))]
        else:
            filtered_df = city_df[(city_df['Continent'].isin(selected_continents)) & (city_df['Country'].isin(selected_countries)) & (city_df['City'].isin(selected_cities))]

    # --------------------GRAFICOS-------------------------------------#

        col1, col2 = st.columns(2)
        
        with col1:

            variables = ['Education', 'Cost of Living', 'Safety', 'Tolerance']
            for variable in variables:
                if not filtered_df.empty:
                    fig = px.bar(filtered_df,
                                x='City',
                                y=variable,
                                color='City',
                                title=f'{variable}')
                    fig.update_layout(xaxis=dict(showgrid=False),
                                    yaxis=dict(showgrid=False),
                                    width=600)
                    st.plotly_chart(fig)
                else:
                    st.warning(f"No data available for the selected filters for {variable}.")

        with col2:

            variables = ['Healthcare', 'Leisure & Culture', 'Outdoors', 'Travel Connectivity']
            for variable in variables:
                if not filtered_df.empty:
                    fig = px.bar(filtered_df,
                                x='City',
                                y=variable,
                                color='City',
                                title=f'{variable}')
                    fig.update_layout(xaxis=dict(showgrid=False),
                                    yaxis=dict(showgrid=False),
                                    width=600)
                    st.plotly_chart(fig)
                else:
                    st.warning(f"No data available for the selected filters for {variable}.")

       
    ####################################  PAGE 6  ######################################

elif page == "Your best place":
    
    st.title("Find your best place to live 🌎")

    st.markdown("""<p style='font-size:30px; text-align: left; color:green; font-style:italic; margin:0;'>
            <strong>What is more important for you when choosing a city to live?</strong></p>""", 
            unsafe_allow_html=True)
    
    st.write('')
    st.write('')
    st.write('')

    # Defino las variables
    variables = ['Cost of Living', 'Travel Connectivity', 'Safety', 'Healthcare', 'Education', 'Environmental Quality', 'Economy', 'Leisure & Culture', 'Business Freedom', 'Outdoors']

    # Mostrar las variables y permitir al usuario seleccionar tres
    selected_variables = st.multiselect("Select only 3 according to your preferences:", variables)

    if selected_variables:

        if len(selected_variables) != 3:
            st.error('Please select only 3 variables.')
        else:
            st.success(f"You selected: {', '.join(selected_variables)}")

        # Normalizar los datos seleccionados
        scaler = StandardScaler()
        normalized_data = scaler.fit_transform(city_df[selected_variables])
        normalized_df = pd.DataFrame(normalized_data, columns=selected_variables)
        normalized_df['City'] = city_df['City']

        # Entrenar el modelo KNN
        knn = NearestNeighbors(n_neighbors=3)
        knn.fit(normalized_df[selected_variables])

        # Obtener los valores más altos para las variables seleccionadas
        user_input = normalized_df[selected_variables].max().values

        # Encontrar los vecinos más cercanos
        distances, indices = knn.kneighbors([user_input])

        # Mostrar los resultados
        st.markdown("""
                <p style='font-size:30px; text-align: left; color:black; margin:0;'>
                The best cities to live according to your preferences are:</p>""",
                unsafe_allow_html=True)
        
        for idx in indices[0]:
            city_name = normalized_df.iloc[idx]['City']
            st.markdown(f"""
                    <p style='font-size:20px; text-align: left; color:black; margin:0;'>
                    &#9733; {city_name}</p>""",
                    unsafe_allow_html=True)


####################################  PAGE 7  ##########################################

elif page == "Conclusions":
    
    col1, col2, col3 =st.columns([1,2,1])
    
    with col2:

        st.markdown("<h1 style='text-align: center; font-size:45px;'>...Which is the best city to live?</h1>", unsafe_allow_html=True)
        
        st.markdown("""<p style='font-size:30px; text-align: center; color:black; font-style:italic; margin:0;'>
            <strong>It depends on you and your preferences! With this app we will help you to discover <strong>your best place:</strong></p>""", unsafe_allow_html=True)

        st.write('')
        st.write('')
        st.write('') 
        
        st.markdown("""
    <p style="font-size: 18px; line-height: 1.6;">
    1. <strong>Top cities rankings</strong> in terms of safety, healthcare, education, and more.
    </p>
                    
    <p style="font-size: 18px; line-height: 1.6;">
    2. <strong>Air Quality Comparison</strong> between countries and cities.
    </p>
                    
    <p style="font-size: 18px; line-height: 1.6;">
    3. <strong>Business Freedom Impact</strong> between cities.
    </p>
    
    <p style="font-size: 18px; line-height: 1.6;">
    4. <strong>Explore and compare cities</strong> across diverse factors.
    </p>

    <p style="font-size: 18px; line-height: 1.6;">
    5. <strong>Get the top 3 best cities</strong> according to your preferences and lifestyle.
    </p>
    """, unsafe_allow_html=True)
        
        st.markdown("""<h1 style='text-align: center; font-size:30px;'>Explore, compare, and decide where you'd like to live.<br>
                    Your next adventure starts here!</h1>""", unsafe_allow_html=True)
        st.markdown("""
                <p style='font-size:50px; color:black; text-align: center;'>
                🌎
                </p>
                """,
                unsafe_allow_html=True)
        
