import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.firecrawl import FirecrawlTools
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Keys
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Agent
agent = Agent(
    name="shopping partner",
    model=Gemini(id="gemini-2.0-flash-exp", api_key=GOOGLE_API_KEY),
    instructions=[
        "You are a product recommender agent specializing in finding products that match user preferences.",
        "Prioritize finding products that satisfy as many user requirements as possible, but ensure a minimum match of 50%.",
        "Search for products only from authentic and trusted e-commerce websites such as Google Shopping, Amazon, Flipkart, Myntra, Meesho, Nike, and other reputable platforms.",
        "Verify that each product recommendation is in stock and available for purchase.",
        "Avoid suggesting counterfeit or unverified products.",
        "Clearly mention the key attributes of each product (e.g., price, brand, features) in the response.",
        "Format the recommendations neatly and ensure clarity for ease of user understanding.",
        "Also provide the exact link of shoes in the response.",
    ],
    tools=[FirecrawlTools(api_key=FIRECRAWL_API_KEY)],
)

# Streamlit App
st.title("Shopping Partner - Running Shoe Recommendations")

# Input Section
st.subheader("Enter Your Preferences")
color = st.text_input("Preferred Colors (e.g., Blue, Green):")
purpose = st.text_input("Purpose (e.g., Long-distance running):")
budget = st.number_input("Budget (Rs.):", min_value=5000)
brand = st.text_input("Preferred Brand (e.g., New Balance):")
count = st.slider("Number of Recommendations:", min_value=1, max_value=10, value=5)

# Generate Recommendations
if st.button("Find Shoes"):
    # Create Query
    query = (
        f"I am looking for running shoes with the following preferences: "
        f"Color: {color} Purpose: {purpose} Budget: Below {budget} Rs "
        f"Brand: {brand} and must show me {count} shoes of my interest mentioned."
    )

    # Get Response
    with st.spinner("Finding the best options for you..."):
        try:
            response = agent.run(query)
            st.write(response.content)
        #     if response:
        #         st.success("Here are your recommendations:")
        #         st.write(response)
        #     else:
        #         st.warning("No specific results found. Here are some general recommendations:")
        #         st.write(
        #             "1. Visit official websites like New Balance, Amazon, or Flipkart.\n"
        #             "2. Use filters for 'Running Shoes' and your preferred colors.\n"
        #             "3. Check stock availability before purchase."
        #         )
        except Exception as e:
            st.error(f"An error occurred: {e}")
