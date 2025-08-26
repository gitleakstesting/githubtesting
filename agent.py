import os
import json
import logging
import vertexai
from google.adk.agents import LlmAgent

# ---------- LOGGING ----------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MODEL = "gemini-2.0-flash"

# ---------- VERTEX INIT ----------
vertexai.init(
    project="gke-elastic-394012",   # <-- replace with your project
    location="us-central1",
    staging_bucket="gs://daphne_adk"  # <-- replace with your bucket
)

# ---------- TOOL ----------
def get_capital_city(country: str) -> str:
    """Retrieves the capital city for a given country."""
    capitals = {
        "france": "Paris",
        "japan": "Tokyo",
        "canada": "Ottawa"
    }
    return capitals.get(country.lower(), f"Sorry, I don't know the capital of {country}.")

# ---------- ROOT AGENT ----------
root_agent = LlmAgent(
    name="capitalagent",
    model=MODEL,
    description="Answers user questions about the capital city of a given country.",
    instruction=(
        "You are an agent that provides the capital city of a country.\n\n"
        "When a user asks for the capital of a country:\n"
        "1. Identify the country name from the user's query.\n"
        "2. Use the 'get_capital_city' tool to find the capital.\n"
        "3. Respond clearly to the user, stating the capital city.\n\n"
        "Example Query: What's the capital of France?\n"
        "Example Response: The capital of France is Paris.\n"
    ),
    tools=[get_capital_city]
)
