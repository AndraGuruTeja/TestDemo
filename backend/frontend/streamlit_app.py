import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# FastAPI backend URL
BACKEND_URL = "http://localhost:8000"

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
    st.session_state['token'] = None
    st.session_state['page'] = 'login'
    st.session_state['city'] = None
    st.session_state['username'] = None
    st.success("Logged out successfully!")

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
        st.error("Failed to fetch weather data")
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
        st.error("Failed to fetch historical weather data")
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
        st.error("Failed to fetch weather trends")
        return None

# Login Page
def login_page():
    st.title("Login")
    username = st.text_input("Email or Username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        if not username or not password:
            st.error("Username and password are required")
        else:
            if login(username, password):
                st.rerun()

    if st.button("Don't have an account? Signup", key="signup_button"):
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
    st.title("Weather Information")

    # User icon and logout option in the top-right corner
    col1, col2 = st.columns([10, 2])
    with col2:
        if st.button("👤"):
            st.write(f"Logged in as: {st.session_state['username']}")
            if st.button("Logout"):
                logout()
                st.rerun()

    # Search bar and Enter button
    city = st.text_input("Enter city name", key="city_input", value=st.session_state.get('city', ''))
    if st.button("Enter", key="enter_button"):
        if city:
            st.session_state['city'] = city
        else:
            st.error("City name is required")

    # Automatically fetch and display weather data when city is entered
    if st.session_state['city']:
        with st.spinner("Fetching weather data..."):
            weather_data = get_weather(st.session_state['city'])
            if weather_data:
                with st.container():
                    st.markdown(
                        f"""
                        <div style="padding: 10px; border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
                            <h3>🌤️ Weather in {weather_data['city']}</h3>
                            <p><b>Temperature:</b> {weather_data['temperature']}°C</p>
                            <p><b>Humidity:</b> {weather_data['humidity']}%</p>
                            <p><b>Description:</b> {weather_data['description']}</p>
                            <p><b>Cached:</b> {weather_data['cached']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    # Dropdown for days selection
    days_history = st.selectbox("Select days for history", [7, 14, 30], key="days_history")
    days_trends = st.selectbox("Select days for trends", [7, 14, 30], key="days_trends")

    # Historical Data and Trends side by side
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state['city']:
            with st.expander("📅 Historical Weather Data"):
                history_data = get_history(st.session_state['city'], days_history)
                if history_data:
                    df_history = pd.DataFrame(history_data)
                    st.write(df_history)

    with col2:
        if st.session_state['city']:
            with st.expander("📈 Weather Trends"):
                trends_data = get_trends(st.session_state['city'], days_trends)
                if trends_data:
                    df_trends = pd.DataFrame(trends_data)
                    df_trends['date'] = pd.to_datetime(df_trends['date'])

                    # Plotly chart for trends
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df_trends['date'], y=df_trends['avg_temperature'],
                        mode='lines+markers', name='Avg Temperature',
                        hoverinfo='x+y', line=dict(color='blue')
                    ))
                    fig.add_trace(go.Scatter(
                        x=df_trends['date'], y=df_trends['max_temperature'],
                        mode='lines+markers', name='Max Temperature',
                        hoverinfo='x+y', line=dict(color='red')
                    ))
                    fig.add_trace(go.Scatter(
                        x=df_trends['date'], y=df_trends['min_temperature'],
                        mode='lines+markers', name='Min Temperature',
                        hoverinfo='x+y', line=dict(color='green')
                    ))
                    fig.update_layout(
                        title="Temperature Trends",
                        xaxis_title="Date",
                        yaxis_title="Temperature (°C)",
                        hovermode="x unified"
                    )
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