import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from tools import analyze_corridor_risk

load_dotenv()

# Setup
HAZARD_ZONES = [{"name": "I-85 Highway", "coords": (33.825, -84.343), "radius_km": 0.5, "severity": "CRITICAL"}]

# Initialize Agent
agent = LlmAgent(name="waypoint_ecological_agent", model="gemini-2.5-flash", instruction="You are WayPointAI.")

# AUTO-DIAGNOSTIC
print(f"DEBUG: Available methods: {[m for m in dir(agent) if not m.startswith('_')]}")

def process_telemetry_stream(message):
    try:
        lat, lon = message.split(",")
        current_loc = (float(lat.strip()), float(lon.strip()))
        active_risks = analyze_corridor_risk(current_loc, HAZARD_ZONES)
        prompt = f"Telemetry: {current_loc}. Risks: {active_risks}. Provide summary."
        
        # We will use the list you see on startup to pick the right method
        # If you see 'generate_content', use it. If not, paste the list here.
        return agent.generate_content(prompt)
            
    except Exception as e:
        return f"Processing Error: {e}"

if __name__ == "__main__":
    print("Agent Online. Enter 'lat, lon' or 'exit'.")
    while True:
        user_input = input("\nAgent Task/Input > ").strip()
        if user_input.lower() == 'exit': break
        if ',' in user_input:
            print(process_telemetry_stream(user_input))