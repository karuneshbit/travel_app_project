import streamlit as st
from typing import List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langfuse.langchain import CallbackHandler

# --- 1. PYDANTIC OUTPUT DATA STRUCTURES ---
class ItineraryActivity(BaseModel):
    activity_name: str = Field(description="Name of the activity")
    description: str = Field(description="Summary of what to do")
    estimated_cost: str = Field(description="Cost tier (Free, $, $$, $$$)")

class DailyItinerary(BaseModel):
    day_number: int = Field(description="Sequential day number")
    theme: str = Field(description="Main theme for the day")
    activities: List[ItineraryActivity] = Field(description="List of activities")

class TravelPlan(BaseModel):
    destination: str = Field(description="Destination city and country")
    daily_schedule: List[DailyItinerary] = Field(description="Day-by-day plan")

# --- 2. STREAMLIT INTERFACE ---
st.set_page_config(page_title="AI Travel Concierge", page_icon="✈️")
st.title("🗺️ Production AI Travel Concierge")
st.write("Generate a type-safe structured travel itinerary instantly.")

with st.form("itinerary_form"):
    destination = st.text_input("Where are you going?", placeholder="e.g. Paris, France")
    days = st.slider("Number of Days", min_value=1, max_value=7, value=3)
    start_date = st.text_input("When does it start?", placeholder="e.g. October 15th")
    submit_button = st.form_submit_button("Generate Plan")

# --- 3. PRODUCTION EXECUTION ---
if submit_button:
    if not destination or not start_date:
        st.error("Please fill in all the text fields!")
    else:
        with st.spinner("Our AI Concierge is mapping your adventure..."):
            try:
                import os
                os.environ["LANGFUSE_PUBLIC_KEY"] = st.secrets["LANGFUSE_PUBLIC_KEY"]
                os.environ["LANGFUSE_SECRET_KEY"] = st.secrets["LANGFUSE_SECRET_KEY"]
                os.environ["LANGFUSE_HOST"] = st.secrets["LANGFUSE_HOST"]

                # 2. Initialize the handler with NO arguments
                langfuse_handler = CallbackHandler()

                model = ChatOpenAI(
                    model="meta-llama/llama-3.3-70b-instruct:free"
                    openai_api_key=st.secrets["OPENROUTER_API_KEY"],
                    openai_api_base="https://openrouter.ai/api/v1",
                    temperature=0.7
                )

                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are an expert local travel concierge. Plan a highly customized travel itinerary."),
                    ("user", "Create a {days}-day travel itinerary for {destination} starting on {start_date}.")
                ])

                travel_chain = prompt | model.with_structured_output(TravelPlan)

                result = travel_chain.invoke(
                    {"destination": destination, "days": days, "start_date": start_date},
                    config={"callbacks": [langfuse_handler]}
                )

                st.success(f"Trip to {result.destination} successfully built!")
                
                for day in result.daily_schedule:
                    with st.expander(f"📅 Day {day.day_number}: {day.theme}", expanded=True):
                        for act in day.activities:
                            st.markdown(f"**📍 {act.activity_name}** (`{act.estimated_cost}`)" )
                            st.caption(act.description)
                            
            except Exception as e:
                st.error(f"An infrastructure error occurred: {e}")
