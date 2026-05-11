from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv

load_dotenv(override=True)

_ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

test_generator_agent = Agent(
    name="Test_Generator",
    instructions=(
        "You are an expert Java developer specialising in unit testing. "
        "When given a Java class, generate comprehensive JUnit 5 unit tests covering: "
        "all public methods, valid inputs, boundary values, and all exception-throwing paths. "
        "When given previous tests along with evaluator feedback and missing cases, "
        "improve the existing tests to address every point raised. "
        "Return only the Java test class code — no explanation, no markdown fences."
    ),
    model=OpenAIChatCompletionsModel(
        model="deepseek-r1:8b",
        openai_client=_ollama_client,
    ),
)
