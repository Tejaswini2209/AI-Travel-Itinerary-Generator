# AI-Travel-Itinerary-Generator

AI Travel Itinerary Generator
Overview
The AI Travel Itinerary Generator is an intelligent web application that helps users create personalized travel itineraries based on their destination, budget, trip duration, and travel preferences. The application uses Artificial Intelligence to generate day-wise travel plans and integrates real-time travel information, including weather updates, destination images, interactive maps, hotel recommendations, packing suggestions, and downloadable PDF itineraries.
Developed using Python and Streamlit, the application provides an intuitive and user-friendly interface that enables users to plan their trips quickly and efficiently.
Features
• AI-powered travel itinerary generation
• Personalized day-wise travel planning
• Real-time weather information
• Destination image display
• Hotel recommendations
• Interactive destination maps
• Packing list suggestions
• PDF itinerary generation and download
• User-friendly Streamlit interface
Technologies Used
• Python 3.x
• Streamlit
• Groq API
• OpenWeather API
• Pexels API
• Folium
• Geopy
• Requests
• python-dotenv
• FPDF
Project Structure
AI-Travel-Itinerary-Generator/ 
│── app.py 
│── requirements.txt 
│── .env.example 
│── assets/ │── images/ │── README.md
Installation
1. Clone the repository:
git clone https://github.com/yourusername/AI-Travel-Itinerary-Generator.git
2. Navigate to the project directory:
cd AI-Travel-Itinerary-Generator
3. Install the required dependencies:
pip install -r requirements.txt
4. Create a .env file and add your API keys:
GROQ_API_KEY=your_groq_api_key OPENWEATHER_API_KEY=your_openweather_api_key PEXELS_API_KEY=your_pexels_api_key
5. Run the application:
streamlit run app.py
How It Works
1. Enter the travel destination.
2. Specify the number of travel days.
3. Enter your travel budget.
4. Select your travel preferences.
5. Click Generate Trip.
6. The AI generates a personalized day-wise itinerary.
7. View weather information, hotel recommendations, destination maps, and packing suggestions.
8. Download the itinerary as a PDF for future reference.
Future Enhancements
• Flight, train, and bus booking integration
• Online hotel reservation system
• User authentication and profile management
• Multi-language support
• Android and iOS mobile application
• Route optimization using AI
• Offline itinerary access
• AI-based budget optimization and personalized recommendations
Author
Tejaswini Allavarapu
Master of Computer Applications (MCA)
