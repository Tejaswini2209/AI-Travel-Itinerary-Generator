import streamlit as st
from groq import Groq
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from fpdf import FPDF
from dotenv import load_dotenv
import os
import re
import requests
import random

# Load environment variables
load_dotenv()

# --- CONFIG ---
st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")

# --- API ---
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY or API_KEY.strip() == "":
    st.error("❌ GROQ API key not found. Add it to .env file.")
    st.stop()

client = Groq(api_key=API_KEY)

# --- SESSION STATE ---
if "itinerary" not in st.session_state:
    st.session_state.itinerary = ""

if "landmarks" not in st.session_state:
    st.session_state.landmarks = []

if "destination" not in st.session_state:
    st.session_state.destination=""

if "image_url" not in st.session_state:
    st.session_state.image_url=""

if "weather" not in st.session_state:
    st.session_state.weather = None

if "hotels" not in st.session_state:
    st.session_state.hotels = []

if "packing_list" not in st.session_state:
    st.session_state.packing_list = ""
# --- SIDEBAR ---


# --- FUNCTIONS ---

@st.cache_data(show_spinner=False)
def get_coordinates(place):
    try:
        geo = Nominatim(user_agent="travel_app")
        location = geo.geocode(place, timeout=10)
        if location:
            return (location.latitude, location.longitude)
    except Exception as e:
        print(f"Geocoding error:  {e}")
        return None
    return None





def generate_itinerary(destination,days,budget,interests):
    max_days_per_call=10
    full_plan=""
    for start in range(1,days +1,max_days_per_call):
        end=min(start + max_days_per_call -1, days)
        prompt = f"""
        Create a concise {days}-day travel itinerary for {destination}.
        keep each day brief (4-5 points only)
        Budget:  ₹{budget}
        Interests: {', '.join(interests)}

        Requirements:
        -Break down each day
        -Include places to visit
        -Suggest food and activities
        -Mention estimated cost for each activity( in  ₹)
        -suggest budget-friendly, mid-range, or luxury options based on total budget

        Also include:
        -Approx hotel cost per night
        -Food cost per day
        -Transport cost per day
        
        Format:
        Title:
        Day 1:
        - Place:...
        - Activity:...
        - Cost:...

        End with:
        LANDMARKS: place1, place2, place3
        """

        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            
            if res.choices:
                full_plan += res.choices[0].message.content + "\n\n"

            #after loop ends
            return full_plan if full_plan else None
        except Exception as e:
            st.error(f"API Error: {e}")
            return None
    full_plan += "\nLANDMARKS: tourist spots in "+ destination

    return full_plan

def extract_landmarks(text):
    if not text:
        return[]
    
    match = re.search(r"LANDMARKS:\s*(.*)", text,re.IGNORECASE)

    if match:
        return [x.strip() for x in match.group(1).split(",") if x.strip()]
    return []

def distance(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5

def optimize_route(start,locations):
    route = []
    current = start
    remaining = locations.copy()

    while remaining:
        next_loc = min(remaining, key=lambda x: distance(current ,x[1]))
        route.append(next_loc)
        current = next_loc[1]
        remaining.remove(next_loc)
    return route

def get_destination_image(destination):
    API_KEY=os.getenv("PEXELS_API_KEY")
    if not API_KEY:
        return None
    
    url="https://api.pexels.com/v1/search"
    headers={"Authorization": API_KEY}
    params = {
        "query": f"{destination} travel",
        "per_page": 5
    }
    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        photos = data.get("photos",[])
        if photos:
            return random.choice(photos)["src"]["large"]
        
    except Exception as e:
        print("Image error:", e)

    

    return None


def get_weather(destination):
    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    if not API_KEY:
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": destination,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        res = requests.get(url, params=params)
        data = res.json()

        if res.status_code != 200:
            return None

        weather = {
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data.get("weather",[{}])[0].get("description","Unknown").title(),
            "city": data["name"]
        }

        return weather

    except Exception as e:
        print("Weather error:", e)
        return None

def suggest_hotels(destination, budget):
    destination = destination.title()

    if budget < 5000:
        return [
            f"🏨 Budget Lodge in {destination}",
            f"🛏️ Backpacker Hostel ({destination})",
            f"🏠 Affordable Guest House in {destination}"
        ]
    elif budget < 20000:
        return [
            f"🏨 3-Star Comfort Hotel in {destination}",
            f"🌆 City View Residency ({destination})",
            f"🛎️ Business Class Hotel in {destination}"
        ]
    else:
        return [
            f"🏨 Luxury 5-Star Hotel in {destination}",
            f"🏝️ Premium Resort & Spa ({destination})",
            f"👑 Palace Heritage Hotel in {destination}"
        ]    

def generate_packing_list(destination, weather, interests):
    prompt = f"""
    Create a smart travel packing checklist for visiting {destination}.

    Weather: {weather}
    Interests: {', '.join(interests)}

    Include:
    - Clothes
    - Travel essentials
    - Electronics
    - Medicines
    - Activity-specific items

    Keep it short and practical.
    Use bullet points.
    """

    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return res.choices[0].message.content

    except Exception as e:
        print("Packing list error:", e)
        return "Packing suggestions unavailable."

# --- PDF ---
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Travel Itinerary", 0, 1, "C")


def create_pdf(itinerary_text):
    pdf = FPDF()
    pdf.add_page()

    try:
        
        pdf.add_font("DejaVu", "","DejaVuSans.ttf",uni=True)
        pdf.set_font("DejaVu","",size=12)
    except:
        pdf.set_font("Arial", size=12)

    
    for line in itinerary_text.split("\n"):
        safe_line=line.encode('latin-1','ignore').decode('latin-1')
        pdf.set_x(10)
        pdf.multi_cell(0,10,txt=safe_line)

    pdf_bytes = pdf.output(dest='S')

    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode('latin-1')

    return bytes(pdf_bytes)


# --- MAIN UI ---
st.title("✈️ AI Travel Itinerary Generator")
st.caption("Plan smarter. Travel better.")
st.divider()
#-----HORIZONTAL INPUT BAR-----
with st.container():
    st.subheader("🧭 Plan Your Trip")

    destination = st.text_input("📍 Destination")

    days = st.number_input("🗓️ Number of Days",min_value= 1,max_value=10, value=3)

    budget = st.number_input(
        "💰 Budget (₹)",
        min_value=1000,
        max_value=500000,
        step=1000,
        value=10000
    )

    interests = st.multiselect(
        "🎯 Interests",
        ["Food", "Nature", "History", "Adventure", "Shopping"],
        default=["Food"]
    )

    generate = st.button("🚀 Generate Trip", use_container_width=True)


# --- GENERATE ---
if generate:
    if not destination:
        st.warning("Enter a destination")
    else:
        with st.spinner("Generating your travel plan..."):
            result = generate_itinerary(destination,days,budget,interests)

            if result:
                st.session_state.itinerary = result
                st.session_state.landmarks = extract_landmarks(result)
                st.session_state.destination= destination

                st.session_state.image_url=get_destination_image(destination)

                st.session_state.weather = get_weather(destination)
                
                st.session_state.hotels = suggest_hotels(destination, budget)
                weather_text = ""

                if st.session_state.weather:
                    weather_text = st.session_state.weather["description"]

                st.session_state.packing_list = generate_packing_list(
                    destination,
                    weather_text,
                    interests
                )

# --- DISPLAY ---
if st.session_state.itinerary:
    #---new (hero image banner)-----
    if st.session_state.image_url:
        st.image(st.session_state.image_url, width=400)
    else:
        st.warning("No image found")
    

    st.markdown("---")

    col_left, col_right = st.columns([2,1])
    # --------ITINERARY SECTION--------

    with col_left:
        st.subheader("📄 Itinerary")
        st.write(st.session_state.itinerary)

        pdf_data = create_pdf(st.session_state.itinerary)
        st.download_button(
            label=" Download PDF",
            data=pdf_data,
            file_name="itinerary.pdf",
            mime="application/pdf"
        )
    
    #--------Map Section------------

    with col_right:
        st.subheader("🗺️ Map View")

        coords = get_coordinates(st.session_state.destination)

        if coords:
            m = folium.Map(location=coords, zoom_start=12)

            # Start point
            folium.Marker(coords, tooltip=st.session_state.destination, icon=folium.Icon(color="red")).add_to(m)

            # Get coordinates of landmarks
            landmark_coords = []
            for place in st.session_state.landmarks:
                loc = get_coordinates(f"{place},{st.session_state.destination}")
                if loc:
                    landmark_coords.append((place, loc))

            # Optimize route
            optimized = optimize_route(coords, landmark_coords)

            # Draw markers + route
            route_points = [coords]

            for place, loc in optimized:
                folium.Marker(loc, tooltip=place).add_to(m)
                route_points.append(loc)

            # Draw line
            folium.PolyLine(route_points, color="blue", weight=3).add_to(m)

            st_folium(m, height=400)
        else:
            st.info("Map location not found")


if st.session_state.weather:
    w = st.session_state.weather

    st.subheader("🌦️ Current Weather")

    col1, col2, col3 = st.columns(3)

    col1.metric("🌡 Temperature", f"{w['temp']}°C")
    col2.metric("🤔 Feels Like", f"{w['feels_like']}°C")
    col3.metric("💧 Humidity", f"{w['humidity']}%")

    st.info(f"Condition: {w['description']}")
else:
    st.info("Weather data not available")

# --- HOTELS ---
if st.session_state.hotels:
    st.subheader("🏨 Recommended Stays")

    for hotel in st.session_state.hotels:
        st.markdown(f"- {hotel}")

# --- PACKING LIST ---
if st.session_state.packing_list:
    st.subheader("🎒 Packing Suggestions")

    st.markdown(st.session_state.packing_list)