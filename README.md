# Adaptive Learning Platform

An adaptive learning platform designed to build a learner profile, assess
knowledge, create a personalized study plan, and provide tutoring that can
adjust to the learner's progress.

## Project structure

```text
frontend/
  streamlit_app.py
backend/
  agents/
    profile_agent.py
    assessment_agent.py
    planner_agent.py
    tutor_agent.py
    adaptive_agent.py
  services/
    openai_service.py
    cosmos_service.py
    search_service.py
  models/
    learner_profile.py
  orchestrator/
    workflow.py
config/
  settings.py
requirements.txt
.env
```

The agents are intended to handle learner profiling, assessment, planning,
tutoring, and adaptation. Backend services provide integrations for language
model access, learner data persistence, and search. The Streamlit frontend is
the planned learner-facing application.

## Status

The five agent modules are initial implementations that accept a text-generation
callable, keeping them independent of a particular model provider. The service
modules provide OpenAI text generation and Azure Cosmos DB and Azure AI Search
adapters. `LearnerProfile` stores learner profile data, `LearningWorkflow`
coordinates the agents, and `Settings` loads and validates environment-based
configuration. The frontend entry point and dependency manifest have not yet
been created, so the application cannot be installed or run yet.

## Configuration and secrets

Keep credentials and other sensitive values out of version control. The
services read configuration from the process environment; a `.env` file is not
loaded automatically. Set the variables for the integrations you use:

| Variable | Used by | Required |
| --- | --- | --- |
| `OPENAI_API_KEY` | `OpenAIService` | Yes |
| `OPENAI_MODEL` | `OpenAIService` | No; defaults to `gpt-4o-mini` |
| `OPENAI_TIMEOUT` | `Settings`, `OpenAIService` | No; defaults to 30 seconds |
| `COSMOS_ENDPOINT` | `CosmosService` | Yes |
| `COSMOS_KEY` | `CosmosService` | Yes |
| `COSMOS_DATABASE` | `CosmosService` | Yes |
| `COSMOS_CONTAINER` | `CosmosService` | Yes |
| `AZURE_SEARCH_ENDPOINT` | `SearchService` | Yes |
| `AZURE_SEARCH_KEY` | `SearchService` | Yes |
| `AZURE_SEARCH_INDEX` | `SearchService` | Yes |

OpenAI access uses Python's standard library. Install the optional Azure SDK
packages when using the corresponding services: `pip install azure-cosmos
azure-search-documents`.

## Development setup

After `requirements.txt` and `frontend/streamlit_app.py` are available, a
typical local setup will be:

1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Set the required environment variables in the process environment; a `.env`
   file by itself is not loaded automatically.
4. Start the frontend with `streamlit run frontend/streamlit_app.py`.
