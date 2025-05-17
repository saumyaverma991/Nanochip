from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import re

# Initialize the FastAPI app
app = FastAPI()

origins = [
    "http://localhost:5173",  # Your React app's URL, usually localhost in development
]

# Add the CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows access from the React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the DHT sensor API"}
    
@app.get("/terminal")
async def terminal():
    # Path to your script
    script_path = r"/home/pi/Desktop/NanoChip/backend/sensor.py"
    
    # Run the script and capture the output
    process = subprocess.run(
        ["python", script_path], 
        capture_output=True, 
        text=True
    )

    # Extract values using regular expressions from the stdout
    stdout = process.stdout
    temp_celsius = re.search(r"Temp=(\d+\.\d+)ºC", stdout)
    temp_fahrenheit = re.search(r"Temp=(\d+\.\d+)ºF", stdout)
    humidity = re.search(r"Humidity=(\d+\.\d+)%", stdout)

    # Prepare the output dictionary with the desired format
    output_data = {}

    if temp_celsius:
        output_data["Temp_Celsius"] = f"{temp_celsius.group(1)}ºC"
    if temp_fahrenheit:
        output_data["Temp_Fahrenheit"] = f"{temp_fahrenheit.group(1)}ºF"
    if humidity:
        output_data["Humidity"] = f"{humidity.group(1)}%"

    # Return the formatted output
    return output_data



# uvicorn main:app --reload
