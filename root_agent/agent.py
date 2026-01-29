from pathlib import Path

from google.adk.agents.llm_agent import Agent
from google.genai import types
from google.cloud import bigquery

root_folder = Path(__file__).parent.resolve()

def record_analysis_results_in_bigquery(
    entity_name: str, signed_date: str, filed_date: str
) -> str:
    """Records the analysis results of a business filing into a BigQuery table.

    After successfully analyzing a business filing, and AFTER receiving positive
    confirmation from the user, this tool should be called to persist the extracted
    information.

    Args:
        entity_name: The name of the business entity from the filing.
        signed_date: The date the filing was signed, in 'YYYY-MM-DD' format.
        filed_date: The date the filing was approved/filed, in 'YYYY-MM-DD' format.

    Returns:
        "SUCCESS" if the data was saved, otherwise "FAILURE".
    """
    try:
        client = bigquery.Client()
        table_id = "document_analysis.results"
        rows_to_insert = [
            {"entity_name": entity_name, "signed_date": signed_date, "filed_date": filed_date}
        ]
        errors = client.insert_rows_json(table_id, rows_to_insert)
        return "SUCCESS" if not errors else "FAILURE"
    except Exception:
        return "FAILURE"

static_instruction = types.Content(
    role='user',
    parts=[
        types.Part.from_text(
            text=Path(f"{root_folder}/instructions.txt").read_text()
        ),
        types.Part.from_text(
            text="Now, here are the current forms you'll be comparing against. Please carefully read these:"
        ),
        types.Part.from_bytes(
            data=Path(f"{root_folder}/forms/532a_web.pdf").read_bytes(),
            mime_type='application/pdf',
        ),
        types.Part.from_bytes(
            data=Path(f"{root_folder}/forms/532b_web.pdf").read_bytes(),
            mime_type='application/pdf',
        ),
        types.Part.from_bytes(
            data=Path(f"{root_folder}/forms/617.pdf").read_bytes(),
            mime_type='application/pdf',
        ),
        types.Part.from_text(
            text="And that's all for your instructions. The next thing you see will be from the end user..."
        ),
    ]
)

root_agent = Agent(
    model='gemini-2.5-pro',
    name='root_agent',
    description='A super-agent (written in Python) that analyses and reports on old business filings.',
    static_instruction=static_instruction,
    tools=[record_analysis_results_in_bigquery],
)
