from pathlib import Path
from google.adk.agents.llm_agent import Agent
from google.genai import types

root_folder = Path(__file__).parent.resolve()

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
)
