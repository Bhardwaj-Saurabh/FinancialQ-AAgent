# 🚀 Installation and Usage Guide

Guide to set up and run

# 📑 Table of Contents

- [📋 Prerequisites](#-prerequisites)
- [🎯 Getting Started](#-getting-started)
- [📁 Project Structure](#-project-structure)
- [🏗️ Set Up Your Local Infrastructure](#-set-up-your-local-infrastructure)
- [⚡️ Running the Code for Each Module](#️-running-the-code-for-each-module)

# 📋 Prerequisites

## Local Tools

For all the modules, you'll need the following tools installed locally:

| Tool | Version | Purpose | Installation Link |
|------|---------|---------|------------------|
| Python | 3.11 | Programming language runtime | [Download](https://www.python.org/downloads/) |
| uv | ≥ 0.4.30 | Python package installer and virtual environment manager | [Download](https://github.com/astral-sh/uv) |
| Git | ≥2.44.0 | Version control | [Download](https://git-scm.com/downloads) |
| Docker | ≥27.4.0 | Containerization platform | [Download](https://www.docker.com/get-started/) |

<details>
<summary><b>📌 Windows users also need to install WSL

</details>

## Cloud Services

Also, the course requires access to these cloud services. The authentication to these services is done by adding the corresponding environment variables to the `.env` file:

| Service | Purpose | Cost | Environment Variable | Setup Guide | Starting with Module |
|---------|---------|------|---------------------|-------------| ---------------------|
| [Opik](https://rebrand.ly/philoagents-opik) | LLMOps | Free tier (Hosted on Comet - same API Key) | `COMET_API_KEY` | [Quick Start Guide](https://rebrand.ly/philoagents-opik-quickstart) | Module 5 |
| [OpenAI API](https://openai.com/index/openai-api/) | LLM API used for evaluation | Pay-per-use | `OPENAI_API_KEY` | [Quick Start Guide](https://platform.openai.com/docs/quickstart) | Module 5 |

When working locally, the infrastructure is set up using Docker.

To deploy the code, setup the following services with their corresponding environment variables:

| Service | Purpose | Cost | Required Credentials | Setup Guide |
|---------|---------|------|---------------------|-------------| 
| [MongoDB](https://rebrand.ly/philoagents-mongodb) | Document database | Free tier | `MONGODB_URI` | 1. [Create a free MongoDB Atlas account] <br> 2. [Create a Cluster] </br> 3. [Add a Database User] </br> 4. [Configure a Network Connection] |

# 🎯 Getting Started

## 1. Clone the Repository

Start by cloning the repository and navigating to the `philoagents-api` project directory:
```
git clone https://github.com/neural-maze/philoagents-course.git
cd financeragagent/
```

Next, we have to prepare your Python environment and its dependencies.

## 2. Installation

Inside the `ragagent` directory, to install the dependencies and activate the virtual environment, run the following commands:

```bash
uv venv .venv
. ./.venv/bin/activate # or source ./.venv/bin/activate
uv sync
```

Test that you have Python 3.11.9 installed in your new `uv` environment:
```bash
uv run python --version
# Output: Python 3.11.9
```

This command will:
- Create a virtual environment with the Python version specified in `.python-version` using `uv`
- Activate the virtual environment
- Install all dependencies from `pyproject.toml`

## 3. Environment Configuration

Before running any command, inside the `ragagent` directory, you have to set up your environment:
1. Create your environment file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and configure the required credentials following the inline comments and the recommendations from the [Cloud Services](#-prerequisites) section.

# 📁 Project Structure

The project follows a clean architecture structure commonly used in production Python projects:

```bash
financeragagent/
    ├── dataset/                  # Data files
    ├── notebooks/             # Notebooks
    ├── src/ragagent/          # Main package directory
    │   ├── application/       # Application layer
    │   ├── domain/            # Domain layer
    │   ├── infrastructure/    # Infrastructure layer
    │   └── config.py          # Configuration settings
    ├── run/                   # Entrypoint scripts that use the Python package
    ├── .env.example           # Environment variables template
    ├── .python-version        # Python version specification
    ├── Dockerfile             # API Docker image definition
    ├── docker-compose.yml     # to run the api application
    └── pyproject.toml         # Project dependencies
```

# 🏗️ Set Up Your Local Infrastructure

Use Docker to set up the local infrastructure (Agent API, MongoDB).

# ⚡️ Running the Code for Each Module

> [!WARNING]
> Before running the command below, ensure you do not have any processes running on ports `27017` (MongoDB), and `8000` (Agent API).

From the root directory, to start the api application, run:
```bash
docker compose up

```
To run agent on command line:
```pwsh
$env:PYTHONPATH="src"
```

To run agent on command line:
```bash
python run\main.py
```

To evaluate agent:
```bash
python run\evaluate_agent.py
```

To start data ingestion:
```bash
python run\ingest_data.py
```
