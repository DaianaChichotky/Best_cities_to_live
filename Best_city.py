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
        <h1 style='font-family: Lato; font-size: 45px;'>Analysis of the best cities to live</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Configuración del menú
page = option_menu(None, 
    ["Introduction", "Top10", "Environment", "Economy", "City Rating", "Country Evolution", "Your best place", "Conclusions"], 
    icons=["info-circle", "trophy", "tree", "coin", "star", "arrow-up-right", "heart", "clipboard-check"], 
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
            <p style='font-size:25px; text-align: center; color:green; font-style:italic; margin:0;'>
            <strong>What impact does quality of life have on the choice of a city?</strong></p>
            
            <p style='font-size:25px; text-align: center; color:green; font-style:italic; margin:0;'>
            <strong>How does safety influence the perception of a place as home?</strong></p>
            
            <p style='font-size:25px; text-align: center; color:green; font-style:italic; margin:0;'>
            <strong>What role does the economy play in our daily experience?</strong></p>
            """, 
            unsafe_allow_html=True)

    st.markdown("""
            <p style='font-size:50px; color:black; text-align: center;'>
            🌎
            </p>
            """,
            unsafe_allow_html=True)

    st.markdown("""
            <p style='font-size:20px; color:black; text-align: justify;'>
            These and more questions come to our minds when searching for the perfect place to live.
            Factors such as quality of life, safety, economy, and environmental surroundings play crucial roles.
            As we explore various cities around the world, understanding how these variables impact our daily lives and overall quality of life is essential.
            This analysis focuses on evaluating multiple key aspects that influence the decision to choose a place to live, using data from diverse global cities.
            From safety to air quality, and from business freedom to cultural accessibility, each factor uniquely contributes to the perception and experience of a city as a residential destination.
            </p>
            """,
            unsafe_allow_html=True)

# Random imagenes 

    import requests

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
        st.markdown('#### Random Photos of Countries Around the World')

        #Input for user to enter a city name
        country = st.text_input("Enter the name of a country:", "Argentina")

        #Create the variable photo_url and assign it the result of the get_random_photo() function
        photo_url = get_random_photo(country)
    
        #Check if a valid photo URL was obtained
        if photo_url:

            col1, col2, col3 = st.columns(3)

            with col2:
                    #Display image and caption
                    st.image(photo_url, width=600, use_column_width=True)
                    st.write(
                        "<div style='text-align:right;color:red;font-size:14px'>Generated using Unsplash API</div>",
                        unsafe_allow_html=True)
                
                    #Display "Generate another image" button
                    if st.button(f"Generate another random image of {country}"):
                        #Get a new random photo
                        photo_url = get_random_photo(country)
                    
                        # Check if a valid photo URL was obtained
                        if photo_url:
                            # Replace the image with the new one
                            st.image(photo_url, width=600, use_column_width=True)
                            st.write(
                                "<div style='text-align:right;color:red;font-size:14px'>Generated using Unsplash API</div>",
                                unsafe_allow_html=True
                            )

    if __name__ == "__main__":
                main()
   

####################################  PAGE 2  ######################################

elif page == "Top10":

        tab1, tab2 = st.tabs([
        "Cities under evaluation",
        "Top 10 best cities"])
        
        with tab1:

            st.title('Cities under analysis')
            col1, col2 = st.columns(2)

            with col1:
                st.write('***Cities under the analysis***')             
                with open('HTML/cities_per_continent.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    st.components.v1.html(html_content, height=600)
            

            with col2:
                st.markdown('***You can zoom in/out and move it around:***')
                with open('HTML/cities_worldmap.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    st.components.v1.html(html_content, height=600)

            st.write('----')

            # Para que el usuario chequee si una ciudad especifica se analizo

            st.title('Check if a specific city was considered in the analysis:')

            # Botón para activar la búsqueda
            
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
                    st.write('**The range is from 0 to 10, with the larger numbers indicating higher desirability to live.**')
                elif city_name:
                    st.warning(f"The city '{city_name}' is NOT part of the analysis.")

        
        with tab2:

            st.title('Top 10 rankings')

            col1, col2= st.columns(2)

            with col1:

                with open('HTML/top10_education.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    st.components.v1.html(html_content, height=350)

                with open('HTML/top10_cost_living.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    st.components.v1.html(html_content, height=350)

                with open('HTML/top10_safety.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    st.components.v1.html(html_content, height=350)

                with open('HTML/top10_environment.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    st.components.v1.html(html_content, height=350)

                    

            with col2:
                
                with open('HTML/top10_healthcare.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    st.components.v1.html(html_content, height=350)

                with open('HTML/top10_leisure.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    st.components.v1.html(html_content, height=350)

                with open('HTML/top10_connectivity.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    st.components.v1.html(html_content, height=350)

                with open('HTML/top10_economy.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    st.components.v1.html(html_content, height=350)


####################################  PAGE 3  ######################################

elif page == "Environment":

    st.title('Air Quality worldwide comparison')

    col1, col2, col3 = st.columns(3)

    with col1:
        with open('HTML/AQI_worldmap.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
            st.components.v1.html(html_content, height=600, width=1200)

    with col3:
        st.image('img/AQI_std.png', width=500)

        # Para que el usuario busque por pais que le interese:
        
        st.write('')
        st.write('')
        st.write('')
            
        # Entrada de texto para que el usuario ingrese el nombre del país
        city_name = st.text_input('Check the AQI for a specific city:', '')

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
            city_name_lower = city_name.strip().lower()
        
            # Buscar el valor de AQI correspondiente al país ingresado por el usuario
            aqi_value = city_world_AQI.loc[city_world_AQI['City'].str.lower() == city_name_lower, 'AQI Value'].values
        
            if len(aqi_value) > 0:
                st.success(f"The AQI value for '{city_name.capitalize()}' is {aqi_value[0]}")
            else:
                st.warning(f"Country '{city_name.capitalize()}' not found or no AQI value available.")

    st.write('----') 

    st.markdown("### City comparison:")

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

    selected_cities = st.multiselect('🏙️ Select cities:', options=['All cities'] + list(set(df_filtered['City'].unique())), default='All cities')

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

        # Relation between Startups and Economy
        fig = px.scatter(df_final,
                         x='Startups',
                         y='Economy',
                         color='City',
                         size='Economy',
                         hover_name='City',
                         title='Startups Vs Economy',
                         height=400,
                         width=800)
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

        # Relation between Business Freedom and Economy
        fig = px.scatter(df_final,
                         x='Business Freedom',
                         y='Economy',
                         color='City',
                         size='Economy',
                         hover_name='City',
                         title='Business Freedom Vs Economy',
                         height=400,
                         width=800)
        st.plotly_chart(fig)

    st.markdown("""
                <p style='font-size:40px; text-align: left; color:black; margin:0;'>
                <strong>Is there a significant correlation between "Business Freedom" and "Startups"?</strong></p>""",
                unsafe_allow_html=True)
        
    st.markdown("""
                <p style='font-size:25px; text-align: left; color:black; font-style:italic; margin:0;'>
                After the assessment using Spearman's test I can confirm that both variables
                are dependant which confirms that <strong>the number of startups in a city depends on the business freedom.</p>""",
                unsafe_allow_html=True)
        
    st.write("")
    st.write("")


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

elif page == "City Rating":

    st.title('City rating')
    st.subheader('From 0 to 10 with the larger numbers indicating higher desirability to live.')

    # --------------------SIDEBAR-------------------------------------#

    st.sidebar.image('img\img_world.jpg', use_column_width=True)
    st.sidebar.title("Filters")
    st.sidebar.write('-------')

    continent_options = ['All'] + list(city_df['Continent'].unique())
    selected_continents = st.sidebar.multiselect("Select Continents", options=continent_options, default=['Europe'])

    # Se filtran los países según los continentes seleccionados o mostrar todos los países si se selecciona "All"
    if 'All' in selected_continents:
        country_options = ['All'] + list(city_df['Country'].unique())
    else:
        country_options = ['All'] + list(city_df[city_df['Continent'].isin(selected_continents)]['Country'].unique())

    selected_countries = st.sidebar.multiselect("Select Countries", options=country_options, default=['Germany'])

    # Filtrar ciudades según países seleccionados
    if 'All' in selected_countries:
        city_options = ['All'] + list(city_df['City'].unique())
    else:
        city_options = ['All'] + list(city_df[city_df['Country'].isin(selected_countries)]['City'].unique())

    selected_cities = st.sidebar.multiselect("Select Cities", options=city_options, default=['All'])


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
                fig = px.bar(filtered_df, x='City', y=variable, color='City', title=f'{variable}')
                fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                st.plotly_chart(fig)
            else:
                st.warning(f"No data available for the selected filters for {variable}.")

    with col2:

        variables = ['Healthcare', 'Leisure & Culture', 'Outdoors', 'Travel Connectivity']
    
        for variable in variables:
            if not filtered_df.empty:
                fig = px.bar(filtered_df, x='City', y=variable, color='City', title=f'{variable}')
                fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                st.plotly_chart(fig)
            else:
                st.warning(f"No data available for the selected filters for {variable}.")

####################################  PAGE 6  ######################################

elif page == "Country Evolution":

    st.title('Country evolution')

    # --------------------SIDEBAR-------------------------------------#

    st.sidebar.image('img\img_world.jpg', use_column_width=True)
    st.sidebar.title("Filters")
    st.sidebar.write('-------')

    country_options = ['All'] + list(countries_df['Country'].unique())
    selected_countries = st.sidebar.multiselect("Select Countries", options=country_options, default=['Germany', 'Denmark'])

    # Filtrar los datos según la selección del usuario
    if 'All' in selected_countries:
        filtered_df = countries_df
    else:
        filtered_df = countries_df[countries_df['Country'].isin(selected_countries)]

    # --------------------GRAFICOS-------------------------------------#

    col1, col2 = st.columns(2)
    
    with col1:

        variables = ['Life Ladder', 'Social support', 'Healthy life expectancy at birth']
    
        for variable in variables:
            if not filtered_df.empty:
                fig = px.line(filtered_df, x='year', y=variable, color='Country', 
                          title=f'Evolution of {variable} by Year')
                          
                fig.update_layout(
                    xaxis=dict(
                        tickmode='linear',
                        dtick=1,  # Asegura que cada año esté etiquetado
                        showgrid=False),
                        yaxis=dict(showgrid=False))
                st.plotly_chart(fig)
            else:
                st.warning(f"No data available for the selected filters for {variable}.")

    with col2:

        variables = ['Freedom to make life choices', 'Generosity', 'Perceptions of corruption']
    
        for variable in variables:
            if not filtered_df.empty:
                fig = px.line(filtered_df, x='year', y=variable, color='Country', 
                          title=f'Evolution of {variable} by Year')
                fig.update_layout(
                    xaxis=dict(
                        tickmode='linear',
                        dtick=1,  # Asegura que cada año esté etiquetado
                        showgrid=False),
                        yaxis=dict(showgrid=False))
                st.plotly_chart(fig)
            else:
                st.warning(f"No data available for the selected filters for {variable}.")
   
    ####################################  PAGE 7  ######################################

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

        


####################################  PAGE 9  ##########################################

elif page == "Conclusions":
    
    col1, col2, col3 =st.columns([1,2,1])
    
    with col2:

        st.markdown("<h1 style='text-align: center; font-size:45px;'>Key Takeaways</h1>", unsafe_allow_html=True)
        st.write('')
        st.write('')

        st.subheader("🌍 Insightful Analysis")
        st.write("Identifying cities that stand out for their quality of life.")
    
        st.subheader("🌍 Comparative Analysis")
        st.write("Comparison on air quality and business freedom, highlighting those with higher desirability to live.")

        st.subheader("🌍 Personalized Recommendations")
        st.write("Users can discover cities align with their preferences, ensuring informed decision-making when considering relocation.")
        
        st.subheader("🌍 Future Directions")
        st.write("Future research should consider expanding the dataset to include more cities and diverse socio-economic factors.")

        st.subheader("🌍 Practical Applications")
        st.write("These insights serve individuals seeking new living environments.")