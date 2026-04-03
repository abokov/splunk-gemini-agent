import os
import splunklib.client as client
import splunklib.results as results
from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()

def run_splunk_search(spl_query: str) -> str:
    """
    Executes a Splunk Search Processing Language (SPL) query and returns the log results.
    Use this tool to investigate system errors, access logs, or check metrics.
    Ensure your query is valid SPL. The query MUST start with the word 'search'.
    """
    try:
        service = client.connect(
            host=os.getenv("SPLUNK_HOST"),
            port=os.getenv("SPLUNK_PORT"),
            username=os.getenv("SPLUNK_USER"),
            password=os.getenv("SPLUNK_PASSWORD"),
            autologin=True
        )

        if not spl_query.strip().startswith("search"):
            spl_query = f"search {spl_query}"

        kwargs_oneshot = {"earliest_time": "-24h", "latest_time": "now"}
        search_results = service.jobs.oneshot(spl_query, **kwargs_oneshot)
        
        reader = results.ResultsReader(search_results)
        events = [item.get("_raw", str(item)) for item in reader if isinstance(item, dict)]

        if not events:
            return "No results found for this query."
            
        combined_results = "\n".join(events)
        return combined_results[:8000] 

    except Exception as e:
        return f"Error executing Splunk search. Tell the user: {str(e)}"

splunk_agent = Agent(
    name="splunk_sre_agent",
    model="gemini-2.5-flash",
    description="An AI agent that troubleshoots systems using Splunk.",
    instruction="""You are an expert Site Reliability Engineer. 
    When the user asks about system health, anomalies, or errors, use the `run_splunk_search` tool to query the Splunk logs.
    Write efficient SPL. Analyze the returned logs and provide a concise, human-readable summary of the issue.
    If the search fails, explain why and ask the user for clarification.""",
    tools=[run_splunk_search]
)

