AI Travel Itinerary Generator

An AI-powered travel planning application built with Python and Streamlit that generates personalized travel itineraries using the Groq LLM API. The application also provides destination images, live weather information, optimized tourist routes, hotel suggestions, packing recommendations, interactive maps, and downloadable PDF itineraries.

Overview

Planning a trip often requires searching through multiple websites for destinations, accommodations, weather conditions, and travel routes. This project simplifies the entire planning process by integrating Artificial Intelligence with mapping and travel-related services into a single web application.

Users simply enter their destination, travel duration, budget, and interests. The application automatically generates a customized itinerary and displays useful travel information.


Features
AI-generated travel itinerary
Personalized trip planning
Budget-based recommendations
Destination images
Live weather information
Interactive destination map
Tourist landmark visualization
Route optimization
Hotel recommendations
Smart packing checklist
PDF itinerary download
Simple and responsive Streamlit interface

| Technology              | Purpose                         |
| ----------------------- | ------------------------------- |
| Python                  | Backend Programming             |
| Streamlit               | Web Application Framework       |
| Groq API                | AI Itinerary Generation         |
| Llama 3.3 70B Versatile | Large Language Model            |
| Folium                  | Interactive Maps                |
| Streamlit-Folium        | Display Maps in Streamlit       |
| Geopy (Nominatim)       | Geocoding Locations             |
| OpenWeather API         | Live Weather Information        |
| Pexels API              | Destination Images              |
| FPDF                    | PDF Generation                  |
| Requests                | API Communication               |
| Dotenv                  | Environment Variable Management |


AI-Travel-Itinerary-Generator/
│
├── app.py
├── .env
├── requirements.txt
├── README.md
├── itinerary.pdf
└── assets/


Working Process
 User enters
 Destination
 Number of days
 Budget
 Interests
 The application sends the prompt to the Groq LLM.
 AI generates a personalized itinerary.
 Landmarks are extracted automatically.
 Destination coordinates are obtained using Geopy.
 Folium displays an interactive map.
 Route optimization calculates the travel path.
 Weather information is fetched from OpenWeather.
 Destination images are retrieved using Pexels.
 Hotel recommendations are generated based on budget.
 AI creates a customized packing checklist.
 Users can download the itinerary as a PDF.

APIs Used
  Groq API Used for:
   AI itinerary generation
   Packing list generation
  OpenWeather API Provides:
    Current temperature
    Humidity
    Weather conditions
    Feels-like temperature
  Pexels API Used for:
    Destination images

Installation
Clone Repository
   git clone https://github.com/yourusername/AI-Travel-Itinerary-Generator.git
Move into Project
    cd AI-Travel-Itinerary-Generator
Install Dependencies
    pip install -r requirements.txt
Create Environment File
    
Create a .env file.
    GROQ_API_KEY=your_groq_api_key
    OPENWEATHER_API_KEY=your_openweather_api_key
    PEXELS_API_KEY=your_pexels_api_key
Run Application
      streamlit run app.py

Project Workflow
  User Input
     │
     ▼
Groq AI
     │
     ▼
Travel Itinerary
     │
     ├────────► Landmarks
     │              │
     │              ▼
     │        Route Optimization
     │              │
     ▼              ▼
Weather       Interactive Map
     │
     ▼
Packing List
     │
     ▼
Hotel Suggestions
     │
     ▼
PDF Download


Application Screens

The application contains the following sections:

 Trip Planner
 AI Itinerary
 Destination Image
 Interactive Map
 Weather Information
 Hotel Recommendations
 Packing Suggestions
 PDF Download

Advantages
 Personalized travel planning
 Time-saving itinerary generation
 Interactive visualization
 Live weather updates
 Budget-friendly recommendations
 Easy-to-use interface
 Downloadable travel plans
 AI-powered recommendations

Author
Tejaswini Allavarapu
MCA Final Year Project
Project Title: AI Travel Itinerary Generator

