import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

### Making all text white 
st.markdown("""
    <style>
    /* Make all paragraph text white */
    .stApp {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
### Getting a background
import base64

# Function to load and encode image
def load_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

# Function to apply image as background
def background_image_style(path):
    encoded = load_image(path)
    return f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)),
                          url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """

# Apply background image
st.markdown(background_image_style("climbing everest.jpg"), unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.empty()
with col2:
    st.image("TrailError_logo_white.png", width=300)
with col3:
    st.empty()

# Add text as title with specific features
st.markdown("""
    <h2 style='text-align: center; color: #FFFFFF; font-family: Georgia;'>
        Welcome to your expedition to the Himalayas! 🏔️
    </h2>
""", unsafe_allow_html=True)

st.markdown("<h3 style='color: white; font-family: Georgia;'>Tell us a bit about yourself and we'll recommend the perfect mountain for you to climb according to your profile.</h3>", unsafe_allow_html=True)

#st.image('climbing everest.jpg', caption="This could be you", use_container_width=True)

## Change color to text input 
st.markdown("""
    <style>
    label {
        color: white !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

age = st.text_input("How old are you?")
try:
    age = int(age)
except:
    #st.error("Please make sure that you only enter a number")
    st.stop()

nb_members = st.text_input("How many people will join the expedition?")
try:
    nb_members = int(nb_members)
except:
    st.stop()

nb_hired = st.text_input("How many of those are hired staff?")
try:
    nb_hired = int(nb_hired)
except:
    st.stop()

pct_hired= int(nb_hired)/int(nb_members)

season_list = ["Spring", "Summer", "Autumn", "Winter"]
with st.container(border=True):
    season = st.selectbox("In which season would you like to hike?", season_list)
    
sex_list = ["M", "F"]
with st.container(border=True):
    sex = st.selectbox("Sex", sex_list)
o2_list = ["Yes", "No"]
with st.container(border=True):
    o2 = st.selectbox("Will you bring oxygen?", o2_list)
if o2 == "Yes":
    o2used = 1
if o2 == "No":
    o2used = 0

difficulty_list = ["Easy","Medium", "Hard" ]
with st.container(border=True):
    difficulty = st.selectbox ("Difficulty level", difficulty_list)
# Here we need to define the categories with the ranges defined by Diogo

Country = ['Other',
 'Afghanistan',
 'Albania',
 'Algeria',
 'Andorra',
 'Argentina',
 'Armenia',
 'Australia',
 'Austria',
 'Azerbaijan',
 'Bahrain',
 'Bangladesh',
 'Belarus',
 'Belgium',
 'Bhutan',
 'Bolivia',
 'Bosnia-Herzegovina',
 'Botswana',
 'Brazil',
 'Bulgaria',
 'Canada',
 'Chile',
 'China',
 'Colombia',
 'Costa Rica',
 'Croatia',
 'Cuba',
 'Cyprus',
 'Czech Republic',
 'Czechoslovakia',
 'Denmark',
 'Dominica',
 'Dominican Republic',
 'Ecuador',
 'Egypt',
 'El Salvador',
 'Estonia',
 'Finland',
 'France',
 'Georgia',
 'Germany',
 'Greece',
 'Guatemala',
 'Honduras',
 'Hungary',
 'Iceland',
 'India',
 'Indonesia',
 'Iran',
 'Iraq',
 'Ireland',
 'Israel',
 'Italy',
 'Japan',
 'Jordan',
 'Kazakhstan',
 'Kenya',
 'Kosovo',
 'Kuwait',
 'Kyrgyz Republic',
 'Latvia',
 'Lebanon',
 'Libya',
 'Liechtenstein',
 'Lithuania',
 'Luxembourg',
 'Macedonia',
 'Malaysia',
 'Malta',
 'Mauritius',
 'Mexico',
 'Moldova',
 'Mongolia',
 'Montenegro',
 'Morocco',
 'Myanmar',
 'Nepal',
 'Netherlands',
 'New Zealand',
 'Norway',
 'Oman',
 'Pakistan',
 'Palestine',
 'Panama',
 'Paraguay',
 'Peru',
 'Philippines',
 'Poland',
 'Portugal',
 'Qatar',
 'Romania',
 'Russia',
 'San Marino',
 'Saudi Arabia',
 'Serbia',
 'Singapore',
 'Slovakia',
 'Slovenia',
 'South Africa',
 'South Korea',
 'Spain',
 'Sri Lanka',
 'Sweden',
 'Switzerland',
 'Syria',
 'Taiwan',
 'Tajikistan',
 'Tanzania',
 'Thailand',
 'Tunisia',
 'Turkey',
 'UAE',
 'UK',
 'USA',
 'Ukraine',
 'Uruguay',
 'Uzbekistan',
 'Venezuela',
 'Vietnam',
 'Yugoslavia']
   
with st.container(border=True):
    country = st.selectbox("Country", Country)
# Function to get country_max_height  
df= pd.read_csv('Country_max_heigth_list.csv')
def get_highest_peak(country):
    country = country.lower()
    if country in df['Country'].str.lower().values:
        peak = df[df['Country'].str.lower() == country]['Highest_Peak_m']
    else:
        peak = df[df['Country'].str.lower() == 'other']['Highest_Peak_m']
    if not peak.empty:
        return peak.values[0]
country_max_height = get_highest_peak(country)
if st.button("🚀 Confirm and Continue"):
    # Only run this after the button is clicked
    st.success("Thanks! Processing your inputs...")

    st.markdown("<h3 style='color: white; font-family: Georgia;'>According to our model, you can tackle peaks of up to {country_max_height}.</h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: white; font-family: Georgia;'>Taking your difficulty preferences into account, we can suggest you take a look at the following peaks. We have modelled your personalised probability of success for each of them!🎉</h3>", unsafe_allow_html=True)
    # Definition of new data for model 1 
    
    new_data = pd.DataFrame({
        'mseason': [season],
        'sex': [sex],
        'country_max_height': [country_max_height],
        'mo2used': [o2used],
        'nb_members': [nb_members],
        'pct_hired': [pct_hired],
        'age': [age],
    })
    
    # Here we need to run model 1 to get max_height
    df=pd.read_csv('peak_coord_1_.csv')
    #df.columns
    df_map=df.tail(3)

    label_i = "Death rate"
    main_i = "Peak name"
    note_i = "Height"
    note_i_1 = "Success probability"
    
    label_1 = df_map.iloc[0][ 'death_rate']
    main_1 = df_map.iloc[0][ 'pkname']
    note_1 = "df_map.iloc[0][ 'success_prob']"
    note_1_1 = df_map.iloc[0][ 'heightm']
    
    label_2 = df_map.iloc[1][ 'death_rate']
    main_2 = df_map.iloc[1][ 'pkname']
    note_2 = "df_map.iloc[1][ 'success_prob']"
    note_2_1 =  df_map.iloc[1][ 'heightm']
    
    label_3 = df_map.iloc[2][ 'death_rate']
    main_3 = df_map.iloc[2][ 'pkname']
    note_3 = "df_map.iloc[2][ 'success_prob']"
    note_3_1 = df_map.iloc[2][ 'heightm']
    
    # Display in columns
    col1, col2, col3 , col4 = st.columns(4)

    #index
    col1.markdown(f"""
        <div style='text-align: center; line-height: 1.2;'>
            <div style='color: red;'>{label_i}</div>
            <div style='color: white; font-size: 28px; font-weight: bold;'>{main_i}</div>
            <div style='color: white;'>{note_i_1}meters</div>
            <div style='color: green; font-size: 22px;'>{note_i}</div>
        </div>
    """, unsafe_allow_html=True)
    
    
    # First column
    col2.markdown(f"""
        <div style='text-align: center; line-height: 1.2;'>
            <div style='color: red;'>{label_1}</div>
            <div style='color: white; font-size: 28px; font-weight: bold;'>{main_1}</div>
            <div style='color: white;'>{note_1_1}meters</div>
            <div style='color: green; font-size: 22px;'>{note_1}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Second column
    col3.markdown(f"""
        <div style='text-align: center; line-height: 1.2;'>
            <div style='color: red;'>{label_2}</div>
            <div style='color: white; font-size: 28px; font-weight: bold;'>{main_2}</div>
            <div style='color: white;'>{note_2_1}meters</div>
            <div style='color: green; font-size: 22px;'>{note_2}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Third column
    col4.markdown(f"""
        <div style='text-align: center; line-height: 1.2;'>
            <div style='color: red;'>{label_3}</div>
            <div style='color: white; font-size: 28px; font-weight: bold;'>{main_3}</div>
            <div style='color: white;'>{note_3_1}meters</div>
            <div style='color: green; font-size: 22px;'>{note_3}</div>
        </div>
    """, unsafe_allow_html=True)
    
    #  Definition of new data for model 2
    
    new_data2 = pd.DataFrame({
        'mseason': [season],
        'sex': [sex],
        'country_max_height': [country_max_height],
        'mo2used': [o2used],
        'nb_members': [nb_members],
        'pct_hired': [pct_hired],
        'age': [age],
        'peakid': ['EVER']
    })
    
    ### Add map
    df=pd.read_csv('peak_coord_1_.csv')
    #df.columns
    df_map=df.tail(3)
    mean_lat = df_map['latitude'].mean()
    mean_lon = df_map['longitude'].mean()
      
    import plotly.express as px
    fig=px.scatter_map(df_map,lat='latitude', lon= 'longitude',size='success_rate',color='success_rate',hover_data='pkname',color_continuous_scale='RdYlGn',)
    fig.update_layout(map_style="open-street-map", mapbox_center={"lat": mean_lat, "lon": mean_lon})
    fig.show()    
    st.plotly_chart(fig)

