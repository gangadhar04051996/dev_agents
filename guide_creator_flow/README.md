# CodeWriter Assistant

A powerful AI-powered code generation and documentation tool built with crewAI. This project helps developers generate code implementations, documentation, and flow diagrams through an interactive UI interface.

## Features

- **Code Generation**: Generates code implementations in multiple programming languages
- **Flow Diagram Creation**: Automatically creates Mermaid flow diagrams for code visualization
- **Documentation**: Generates comprehensive documentation and reports
- **Multi-Agent System**: Leverages multiple AI agents for different aspects of code creation
  - Code Writer Agent: Generates the initial code implementation
  - Code Reviewer Agent: Reviews and suggests improvements
  - Flow Diagram Creator Agent: Creates visual representations of the code flow

## Project Structure

```
guide_creator_flow/
├── src/
│   └── guide_creator_flow/
│       ├── crews/
│       │   └── code_writer/
│       │       ├── config/
│       │       │   ├── agents.yaml
│       │       │   └── tasks.yaml
│       │       └── code_writer.py
│       └── main.py
├── output/
│   ├── code/
│   └── reports/
├── config/
├── pyproject.toml
└── README.md
```

## Prerequisites

- Python >=3.10, <3.13
- [UV](https://docs.astral.sh/uv/) package manager
- [Ollama](https://ollama.ai/) for local LLM support
- OpenAI API key (optional)

## Installation

1. Install UV if you haven't already:
```bash
pip install uv
```

2. Clone the repository:
```bash
git clone <repository-url>
cd guide_creator_flow
```

3. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. Install dependencies:
```bash
uv pip install -e .
```

## Running the Project

There are two ways to run the project:

### 1. Command Line Interface

Run the code generation flow from the command line:
```bash
crewai flow kickoff
```

This will:
- Prompt for the program you want to build
- Ask for the programming language
- Generate the implementation
- Create flow diagrams and documentation
- Save outputs to the `output/` directory

### 2. Streamlit UI Interface

WIP

## Output Structure

The project generates several files in the `output/` directory:

- `output/code/`: Contains generated code implementations
- `output/reports/`: Contains:
  - Implementation reports (markdown)
  - Flow diagrams (Mermaid format)
  - Documentation

## Local LLM Setup

1. Install Ollama from [ollama.ai](https://ollama.ai/)
2. Pull required models:
```bash
ollama pull gemma3
ollama pull granite3.3
```

## Troubleshooting

1. If you encounter LLM-related errors:
   - Ensure Ollama is running locally
   - Check if the required models are pulled
   - Verify your API keys in `.env`


## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
