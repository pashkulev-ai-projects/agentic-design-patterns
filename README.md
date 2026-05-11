# Agentic Design Patterns using OpenAI Agents SDK

A hands-on exploration of the **OpenAI Agents SDK** that goes beyond documenting individual
features. Each demo is built around a real-world scenario, and together they cover every major
**agentic workflow design pattern** in use today — making the concepts applicable to any
agentic framework, not just OpenAI.

---

## Overview

This project implements all major agentic workflow design patterns using the OpenAI Agents SDK.
Rather than isolated feature demos, each example is a complete pipeline built around a realistic
scenario — code review, customer support routing, research automation, and iterative unit test
generation. The patterns covered here are framework-agnostic.

- **10 progressive demos** — from a single agent to a multi-agent parallel pipeline
- **Every core SDK concept** covered: agents, tools, streaming, tracing, structured outputs, guardrails, handoffs, parallelization, and persistent memory
- **Every major agentic workflow pattern** implemented: prompt chaining, orchestrator-worker, routing, parallelization, and evaluator-optimizer
- **Multi-model architecture** — OpenAI models (gpt-4o, gpt-4o-mini), a local model via Ollama (Deepseek R1:8b), and a cloud model via Mistral API (mistral-large-latest) working together in a single pipeline
- **Real scenarios** — code review, customer support routing, research assistant, automated unit test generation, and persistent AI memory

---

## Table of Contents

- [Demo Overview](#demo-overview)
- [SDK Concepts Covered](#sdk-concepts-covered)
- [Agentic Workflow Patterns](#agentic-workflow-patterns)
- [Prerequisites](#prerequisites)
- [OpenAI Account Setup](#openai-account-setup)
- [Project Setup](#project-setup)
- [Running the Demos](#running-the-demos)
- [Dependencies](#dependencies)

---

## Demo Overview

### 01 — Agents
**Concept:** The simplest possible agent run.

A Devil's Advocate agent receives a statement and constructs the strongest possible counter-argument.
Demonstrates `Agent`, `Runner.run()`, and the core request-response loop.

---

### 02 — Streamed Response
**Concept:** Real-time token streaming.

The same Devil's Advocate agent, now with `Runner.run_streamed()` and `stream_events()`.
Shows how to consume `ResponseTextDeltaEvent` tokens as they arrive — essential for any
production UI that needs to feel responsive.

---

### 03 — Tools
**Concept:** Agents that act on the world.

A Research Assistant agent equipped with a web search tool and an email tool. Given a natural
language prompt, it searches the web, synthesises the results, and delivers a summary by email —
all autonomously. Introduces `@function_tool`, tracing with `trace()`, and `gen_trace_id()`.

---

### 04 — Agents as Tools
**Concept:** Orchestrator-Worker pattern.

An orchestrator agent decomposes a research task and delegates to specialist sub-agents exposed
as tools via `.as_tool()`. Unlike handoffs, control returns to the orchestrator after each
sub-agent completes. Demonstrates hierarchical multi-agent coordination.

---

### 05 — Handoffs
**Concept:** Routing workflow pattern.

A Router agent handles incoming customer support messages. Based on intent, it permanently
transfers control — via `handoffs=[]` — to either a Billing Agent or a Tech Support Agent.
Each specialist has domain-specific instructions and responds accordingly.

---

### 06 — Structured Outputs & Prompt Chaining
**Concept:** Type-safe outputs flowing through a multi-agent pipeline.

A three-stage prompt chaining pipeline built around a code review scenario:

```
Code Reviewer  →  Frontend Developer  →  Email Sender
 (CodeReview)      (HTML email body)      (Resend API)
```

The Code Reviewer produces a typed `CodeReview` Pydantic model. The Frontend Developer
transforms it into a branded HTML email. The Email Sender delivers it via the Resend API —
complete with Strypes brand assets injected post-generation to avoid token overhead.

---

### 07 — Guardrails
**Concept:** Input and output protection in a pipeline.

The same prompt chaining pipeline from demo 06, hardened with two guardrails running
concurrently with the main agent:

- **Input guardrail** — detects prompt injection attacks embedded in submitted code and
  blocks the pipeline before any LLM call is made
- **Output guardrail** — inspects the code review output for hardcoded credentials and
  secrets, preventing sensitive data from being forwarded downstream

Three scenarios are run: injection attempt (blocked), buggy code with hardcoded secrets
(blocked), and clean code (pipeline completes and email is sent).

---

### 08 — Parallelization
**Concept:** Parallel specialist agents with sequential aggregation.

A four-stage pipeline that parallelises the expensive work:

```
                ┌─ Security Reviewer   ─┐
Code Input  ──► ├─ Performance Reviewer ─┤──► Aggregator ──► Frontend Dev ──► Email
                └─ Readability Reviewer ─┘
                   (asyncio.gather)
```

Three specialist agents run simultaneously via `asyncio.gather()`. Each has strict domain
boundaries enforced by system prompt. A fourth agent aggregates the results using a
deterministic `calculate_overall_score` tool to avoid LLM arithmetic errors. The full report
is then styled and delivered by email.

---

### 09 — Evaluator-Optimizer
**Concept:** Iterative quality improvement with a multi-model feedback loop.

A two-agent loop that generates and refines JUnit 5 unit tests for a Java class:

```
Generator (Deepseek R1:8b / Ollama) ──► Evaluator (mistral-large-latest / Mistral)
        ▲                                          │
        └──────────── feedback + score ────────────┘
```

The Generator starts with only happy-path tests. The Evaluator scores them (1–10) and
identifies missing cases. The loop continues until the score threshold is met or max
iterations are reached. Demonstrates cross-provider multi-model pipelines using
`OpenAIChatCompletionsModel` with a local Ollama instance and the Mistral cloud API.

---

### 10 — State & Memory
**Concept:** Ephemeral vs durable agent memory.

Two approaches compared side by side:

- **In-Thread (ephemeral):** conversation history passed explicitly via `to_input_list()`.
  With the thread: agent remembers. Without: blank slate. Dies when the session ends.
- **Persistent (durable):** facts stored in SQLite via `remember()` / `recall_all()` async
  function tools. Survives across separate `Runner.run()` calls and process restarts.
  Session 1 introduces the user; Session 2 — a completely fresh run — greets them by name.

---

## SDK Concepts Covered

| Concept | Demo |
|---|---|
| `Agent` + `Runner.run()` | 01 |
| `Runner.run_streamed()` + `stream_events()` | 02 |
| `@function_tool` | 03, 06, 08, 10 |
| `trace()` + `gen_trace_id()` | 03, 04, 05, 06, 07, 08, 09 |
| `output_type` (Pydantic structured outputs) | 06, 07, 08, 09 |
| `input_guardrail` + `output_guardrail` | 07 |
| `handoffs=[]` | 05 |
| `.as_tool()` (agent as tool) | 04 |
| `asyncio.gather()` parallelization | 08 |
| `OpenAIChatCompletionsModel` (non-OpenAI providers) | 09 |
| `to_input_list()` (in-thread memory) | 10 |
| `ModelSettings` | 08 |

---

## Agentic Workflow Patterns

| Pattern | Demo | Description |
|---|---|---|
| Single Agent | 01, 02 | One agent, one task |
| Prompt Chaining | 06, 07 | Sequential agents, typed outputs passed forward |
| Routing | 05 | Router classifies intent, hands off to specialist |
| Orchestrator-Worker | 04 | Orchestrator delegates to sub-agents as tools |
| Parallelization | 08 | Multiple agents run concurrently, results aggregated |
| Evaluator-Optimizer | 09 | Generator-evaluator feedback loop with iterative refinement |

---

## Prerequisites

| Requirement | Used in | Notes |
|---|---|---|
| Python 3.12+ | All | |
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | All | Package manager |
| OpenAI API key | All | See setup below |
| Serper API key | 03, 04 | Web search tool |
| Resend account + verified domain | 03, 04, 06, 07, 08 | Email delivery — see setup below |
| Mistral API key | 09 | Evaluator model |
| Ollama + deepseek-r1:8b | 09 | Generator model |

---

## Account Setup

### OpenAI
1. Go to [platform.openai.com](https://platform.openai.com) and create an account
2. Navigate to **Settings → Billing** and add a payment method
3. Top up a minimum of **$10** — this covers all demos comfortably
4. Go to **Dashboard → API Keys** and click **Create new secret key**
5. Copy the key immediately — you will not be able to see it again

### Serper (web search)
1. Create a free account at [serper.dev](https://serper.dev)
2. Copy your API key from the dashboard — the free tier includes 2,500 queries

### Resend (email)
Resend requires a verified domain to send emails from your own address. This involves adding DNS records to your domain provider (TXT and MX records). The process takes 5–10 minutes but requires domain access.

1. Create a free account at [resend.com](https://resend.com)
2. Go to **Domains** → add your domain → follow the DNS verification steps
3. Once verified, go to **API Keys** and create a new key
4. Set `EMAIL_FROM` to an address on your verified domain (e.g. `you@yourdomain.com`)

> **Don't want to set up Resend?** You can skip the email step by commenting out the email agent call at the end of each affected demo. The rest of the pipeline (review, aggregation, formatting) will still run and print results to the console.

### Mistral
1. Create an account at [console.mistral.ai](https://console.mistral.ai)
2. Go to **API Keys** and generate a new key
3. Add billing — the `mistral-large-latest` model is pay-per-use

> **Don't want to use Mistral?** In `demo/my_agents/unit_testing/test_evaluator.py`, replace `OpenAIChatCompletionsModel` with `model="gpt-4o-mini"` and remove the Mistral client. The evaluator-optimizer loop will work identically.

### Ollama (local model)
1. Install Ollama from [ollama.com](https://ollama.com)
2. Pull the model:

```bash
ollama pull deepseek-r1:8b
```

3. Make sure Ollama is running before executing demo 09

> **Don't want to use Ollama?** In `demo/my_agents/unit_testing/test_generator.py`, replace `OpenAIChatCompletionsModel` with `model="gpt-4o-mini"` and remove the Ollama client. No other changes needed.

---

## Project Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd <repo-folder>
```

### 2. Create your `.env` file

```bash
cp .env.example .env
```

Open `.env` and fill in your keys. `OPENAI_API_KEY` is required for all demos.
See `.env.example` for which keys are needed per demo.

### 3. Install dependencies

```bash
uv sync
```

This creates a `.venv` and installs all dependencies from `pyproject.toml`.

---

## Running the Demos

```bash
uv run python -m 01_agents
uv run python -m 02_agents_streamed_response
uv run python -m 03_tools
uv run python -m 04_agents_as_tools
uv run python -m 05_handoffs
uv run python -m 06_structured_outputs
uv run python -m 07_guardrails
uv run python -m 08_parallelization
uv run python -m 09_evaluator_optimizer
uv run python -m 10_state_and_memory
```

All runs are traced. Open the [OpenAI Traces dashboard](https://platform.openai.com/traces)
to inspect every LLM call, tool invocation, token count, and timing.

---

## Dependencies

| Package | Purpose |
|---|---|
| `openai-agents` | OpenAI Agents SDK |
| `openai` | OpenAI Python client |
| `pydantic` | Structured outputs and data validation |
| `python-dotenv` | `.env` file loading |
| `resend` | Email delivery (demos 03, 04, 06, 07, 08) |
| `httpx` | Async HTTP client (web search tool) |
