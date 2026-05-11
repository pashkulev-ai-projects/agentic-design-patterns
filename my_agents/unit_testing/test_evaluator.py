import os
from openai import AsyncOpenAI
from agents import Agent, ModelSettings, OpenAIChatCompletionsModel
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv(override=True)


mistral_model = OpenAIChatCompletionsModel(
    model="mistral-large-latest",
    openai_client= AsyncOpenAI(
        base_url="https://api.mistral.ai/v1",
        api_key=os.environ["MISTRAL_API_KEY"],
    )
)


class TestEvaluation(BaseModel):
    score: int  # 1-10
    feedback: str
    missing_cases: list[str]
    approved: bool  # True when score >= 8


test_evaluator_agent = Agent(
    name="Test_Evaluator",
    instructions=(
        "You are a senior Java engineer and testing expert. "
        "You receive a Java class and a set of JUnit 5 unit tests written for it. "
        "Evaluate the tests on: "
        "1. Method coverage — are all public methods tested? "
        "2. Edge cases — null/blank inputs, zero, negative, boundary values, insufficient funds. "
        "3. Exception paths — are all thrown exceptions asserted with assertThrows? "
        "4. Assertion quality — are results verified with specific assertEquals/assertTrue calls? "
        "5. Test independence — each test sets up its own state, no shared mutable state. "
        "Score from 1 (very poor) to 10 (exemplary). "
        "Set approved=true only when score >= 8. "
        "List every specific missing test case in missing_cases."
    ),
    output_type=TestEvaluation,
    model_settings=ModelSettings(temperature=0),
    model=mistral_model,
)
