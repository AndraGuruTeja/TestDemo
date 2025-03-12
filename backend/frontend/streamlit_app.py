import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# FastAPI backend URL
# BACKEND_URL = "http://backend:8000"  # Use the 'backend' service name from docker-compose.yml

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
# Session state to manage user authentication
if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'
if 'city' not in st.session_state:
    st.session_state['city'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Function to login
def login(username, password):
    response = requests.post(
        f"{BACKEND_URL}/token",

        data={"username": username, "password": password}
    )
                    
    if response.status_code == 200:
        st.session_state['token'] = response.json()['access_token']
        st.session_state['page'] = 'weather'
        st.session_state['username'] = username
        st.success("Logged in successfully!")
        return True
    else:
        st.error("Invalid credentials")
        return False

# Function to signup
def signup(username, password):
    response = requests.post(
        f"{BACKEND_URL}/register",
        json={"email": username, "password": password}
    )
    if response.status_code == 201:
        st.success("User created successfully! Please login.")
        st.session_state['page'] = 'login'
        return True
    elif response.status_code == 400:
        st.error("Email or Username already exists")
        return False
    else:
        st.error("Error creating user")
        return False

# Function to logout
def logout():
    st.session_state.update({
        'token': None,
        'page': 'login',
        'city': None,
        'username': None
    })
    st.experimental_rerun()

# Function to get weather data
def get_weather(city):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(
        f"{BACKEND_URL}/weather/{city}",
        headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Too Many Requests! Please try again after 1 minute.")
        return None

# Function to get historical weather data
def get_history(city, days=7):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(
        f"{BACKEND_URL}/weather/history/{city}",
        params={"days": days},
        headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Too Many Requests! Please try again after 1 minute")
        return None

# Function to get weather trends
def get_trends(city, days=7):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(
        f"{BACKEND_URL}/weather/trends/{city}",
        params={"days": days},
        headers=headers
    )
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Too Many Requests! Please try again after 1 minute")
        return None

# Login Page with Attractive Cards
def login_page():
    st.title("Welcome to Weather Dashboard 🌦️")
    st.markdown("""
        <div style="
            padding: 2rem;
            margin: 1rem 0;
            border-radius: 15px;
            background: linear-gradient(135deg, #6B8DD6 0%, #8E37D7 100%);
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <h2 style="margin: 0; font-size: 2rem;">Login to Access Weather Data</h2>
        </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Email or Username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        if not username or not password:
            st.error("Username and password are required")
        else:
            if login(username, password):
                st.rerun()

    st.markdown("""
        <div style="
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 15px;
            background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <h2 style="margin: 0; font-size: 1.5rem;">Don't have an account? Signup now!</h2>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Signup", key="signup_button"):
        st.session_state['page'] = 'signup'
        st.rerun()

# Signup Page
def signup_page():
    st.title("Signup")
    username = st.text_input("Email or Username")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Signup", key="signup_button"):
        if not username or not password:
            st.error("Username and password are required")
        else:
            if signup(username, password):
                st.rerun()

    if st.button("Already have an account? Login", key="login_button"):
        st.session_state['page'] = 'login'
        st.rerun()

# Weather Page
def weather_page():
    st.title("🌦️ Weather Dashboard")

    # User info and logout in top-right
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("Logout", key="logout_button"):
            logout()

    # Search bar with auto-focus
    city = st.text_input("Search City", 
                         key="city_input", 
                         value=st.session_state.get('city', ''),
                         help="Enter a city name to get weather information")
    
    # Update city on Enter button click
    if st.button("Enter", key="enter_button"):
        if city:
            st.session_state['city'] = city
        else:
            st.error("City name is required")

    # Weather Card Design
    if st.session_state['city']:
        with st.spinner("Fetching latest weather data..."):
            weather_data = get_weather(st.session_state['city'])
            if weather_data:
                # Determine weather icon based on description
                weather_icons = {
                    "clear sky": "☀️",
                    "few clouds": "⛅",
                    "scattered clouds": "☁️",
                    "broken clouds": "☁️☁️",
                    "overcast clouds": "☁️☁️☁️",
                    "rain": "🌧️",
                    "smoke": "🌫️"
                }
                icon = weather_icons.get(weather_data['description'].lower(), "🌍")
                
                st.markdown(f"""
                    <div style="
                        padding: 2rem;
                        margin: 1rem 0;
                        border-radius: 15px;
                        background: linear-gradient(135deg, #6B8DD6 0%, #8E37D7 100%);
                        color: white;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h2 style="margin: 0; font-size: 2.5rem;">{weather_data['city']}</h2>
                                <p style="margin: 0; font-size: 1.2rem;">{weather_data['description'].title()}</p>
                            </div>
                            <div style="font-size: 4rem;">{icon}</div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 2rem;">
                            <div style="text-align: center;">
                                <div style="font-size: 2.5rem; font-weight: bold;">{weather_data['temperature']}°C</div>
                                <div style="opacity: 0.8;">Temperature</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 2.5rem; font-weight: bold;">{weather_data['humidity']}%</div>
                                <div style="opacity: 0.8;">Humidity</div>
                            </div>
                        </div>
                        <div style="margin-top: 1rem; text-align: right; font-size: 0.9rem; opacity: 0.8;">
                            {'Cached data' if weather_data['cached'] else 'Live data'} • Updated {datetime.now().strftime('%H:%M')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # Historical and Trends Section
    if st.session_state['city']:
        days_filter = st.selectbox("Select Date Range", [7, 14, 30], 
                                  key="days_filter", 
                                  help="Select number of days to view historical data")

        # Historical Data Card
        with st.spinner("Fetching historical data..."):
            history_data = get_history(st.session_state['city'], days_filter)
            if history_data:
                st.markdown(f"""
                    <div style="
                        padding: 1rem;
                        margin: 1rem 0;
                        border-radius: 15px;
                        background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
                        color: white;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    ">
                        <h2 style="margin: 0; font-size: 1.5rem;">📅 Historical Data</h2>
                    </div>
                """, unsafe_allow_html=True)
                df_history = pd.DataFrame(history_data)
                df_history['timestamp'] = pd.to_datetime(df_history['timestamp']).dt.date
                st.dataframe(df_history.style.format({
                    'temperature': '{:.1f}°C',
                    'humidity': '{:.0f}%'
                }), use_container_width=True)

        # Trends Data Card
        with st.spinner("Fetching trends data..."):
            trends_data = get_trends(st.session_state['city'], days_filter)
            if trends_data:
                st.markdown(f"""
                    <div style="
                        padding: 1rem;
                        margin: 1rem 0;
                        border-radius: 15px;
                        background: linear-gradient(135deg, #FF9800 0%, #FFB74D 100%);
                        color: white;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    ">
                        <h2 style="margin: 0; font-size: 1.5rem;">📈 Temperature Trends</h2>
                    </div>
                """, unsafe_allow_html=True)
                df_trends = pd.DataFrame(trends_data)
                df_trends['date'] = pd.to_datetime(df_trends['date']).dt.date

                fig = px.line(df_trends, x='date', y=['avg_temperature', 'max_temperature', 'min_temperature'],
                             title="Temperature Trends Over Time",
                             labels={'value': 'Temperature (°C)', 'variable': 'Metric'},
                             color_discrete_sequence=['#4CAF50', '#FF9800', '#2196F3'])
                fig.update_layout(hovermode="x unified", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

# Main App Logic
def main():
    if st.session_state['token'] is None:
        if st.session_state['page'] == 'login':
            login_page()
        elif st.session_state['page'] == 'signup':
            signup_page()
    else:
        weather_page()

if __name__ == "__main__":
    main()