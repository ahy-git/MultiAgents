from crewai import Agent, Crew, Task
import os
import streamlit as st
from config.helper import get_openai_api_key, get_serper_api_key
from config.llm_models import llm_models
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

# Initialize the tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

llm1 = 'geminiflash'

# Define agents
search = Agent(
    role="Product Price Finder",
    backstory="This agent is responsible for searching product prices on various e-commerce platforms.",
    goal="Accurately find and list product prices from reputable e-commerce sites.",
    tools=[search_tool, scrape_tool],
    verbose=True,
    llm=llm_models.get_model(llm1)
)

data_cleaner = Agent(
    role="Data Cleaning & Normalization Specialist",
    backstory="This agent is responsible for cleaning and normalizing the price data.",
    goal="Ensure accurate price data by filtering out incorrect entries and converting currencies.",
    tools=[],
    verbose=True,
    llm=llm_models.get_model(llm1)

)

comparison = Agent(
    role="Price Comparison Specialist",
    backstory="This agent compares product prices to find the best deal across platforms.",
    goal="Compare product prices from different e-commerce platforms and return the best deal.",
    tools=[],
    verbose=True,
    allow_delegation=True,
    llm=llm_models.get_model(llm1)

)

reporting_agent = Agent(
    role="Final Report Generator",
    backstory="This agent generates the final report summarizing the best product deal.",
    goal="Summarize the best product deal and generate a structured comparison report.",
    tools=[],
    verbose=True,
    llm=llm_models.get_model(llm1)
)

# Define tasks
search_task = Task(
    description="Find all prices for the product from trusted e-commerce websites.",
    expected_output="A structured list of product prices with store links.",
    human_input=True,
    agent=search,
)

cleaning_task = Task(
    description="Filter out incorrect product prices, remove duplicates, and convert to the correct currency.",
    expected_output="A cleaned dataset with accurate prices.",
    human_input=False,
    agent=data_cleaner,
)

comparison_task = Task(
    description="Compare prices across different platforms and highlight the best deal.",
    expected_output="A ranked list of the best prices with recommendations.",
    human_input=False,
    agent=comparison,
)

reporting_task = Task(
    description="Generate a user-friendly price comparison report.",
    expected_output="A structured report with the best-reviewed option and store links.",
    human_input=False,
    agent=reporting_agent,
)

st.title("Price Comparison Tool")
st.write("Enter product details to compare prices across multiple platforms.")

product_name = st.text_input(
    "Product Name", "itel s25 with Bromo black color 6GB 128GB")
country = st.text_input("Country", "Pakistan")

if st.button("Compare Prices"):
    event_management_crew = Crew(
        agents=[search, data_cleaner, comparison, reporting_agent],
        tasks=[search_task, cleaning_task, comparison_task, reporting_task],
        verbose=True,
    )

    event_details = {'product': product_name, 'country': country}
    result = event_management_crew.kickoff(inputs=event_details)
    results = reporting_task.execute()

    st.subheader("Price Comparison Report")
    st.write(results)
