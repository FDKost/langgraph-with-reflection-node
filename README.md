# LangGraph with Reflection Node

This project demonstrates how to build a simple LangGraph workflow that uses a reflection loop to improve the quality of generated answers.  
The workflow consists of three main nodes:

1. **draft_answer** – Generates an initial answer to a user‑supplied question.  
2. **reflect** – Critiques the draft and decides whether it is good enough.  
3. **rewrite** – If the draft is not satisfactory, rewrites it using the critique.

The graph runs until the answer is deemed satisfactory or a maximum number of rounds is reached.

## Features

- Uses LangChain 1.x `ChatOpenAI` for LLM calls.  
- Implements a simple JSON‑based critique protocol.  
- CLI entry point for quick experimentation.  
- Configurable maximum number of reflection rounds.

## Installation

```bash
# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # On Windows use `.venv\\Scripts\\activate`

# Install dependencies
pip install .
```

> **Note**:  
> The project uses the OpenAI API.  
> Set your API key in the environment:

```bash
export OPENAI_API_KEY="sk-..."
```

## Usage

```bash
python -m langgraph_reflection "Explain the theory of relativity in simple terms."
```

Optional arguments:

- `--max-rounds N` – Maximum number of reflection rounds (default: 2).

Example output:

```
Final Answer:
 The theory of relativity, developed by Albert Einstein, is a fundamental theory of physics that describes the relationship between space, time, and gravity. It is divided into two parts: special relativity and general relativity. Special relativity deals with objects moving at constant speeds, especially close to the speed of light, and introduces the famous equation E=mc², which shows that energy and mass are interchangeable. General relativity extends this idea to include gravity, describing it as the curvature of spacetime caused by mass and energy. This theory has been confirmed by numerous experiments and is essential for understanding phenomena such as black holes, gravitational waves, and the expansion of the universe.

Critique:
 All good

Verdict:
 ok
```

## Project Structure

```
langgraph-reflection/
├── pyproject.toml
├── src/
│   └── langgraph_reflection/
│       └── __init__.py
├── README.md
└── tests/
    └── test_graph.py
```

## Testing

Run the unit tests with:

```bash
pytest
```

The tests mock the LLM calls to verify that the graph correctly iterates and terminates.

## License

MIT License
