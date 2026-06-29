# LangGraph Reflection Agent

This project demonstrates a simple LangGraph workflow that generates an answer to a user question, critiques it, and rewrites it if necessary. The agent uses OpenAI’s GPT-4o-mini model to produce the answer, critique, and rewrite.

## Features

- **Draft Generation** – Produces an initial concise answer (5–10 sentences).
- **Reflection** – Critiques the draft and decides whether a rewrite is needed.
- **Rewrite** – Incorporates feedback to produce an improved draft.
- **Loop Control** – Repeats the critique–rewrite cycle up to a maximum number of rounds (default 2).
- **CLI** – Run the agent from the command line.

## Prerequisites

- Python 3.11 or newer
- An OpenAI API key

## Setup

```bash
# Clone the repository
git clone https://github.com/your-username/langgraph-reflection-agent.git
cd langgraph-reflection-agent

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Create a .env file with your OpenAI key
cp .env.example .env
# Edit .env and set your key
```

## Usage

```bash
# Run the agent with a question
python main.py "Explain to a student the difference between tool and resource in MCP."
```

Sample output:

```
=== Draft (Round 1) ===
A tool is a device or software that performs a specific function, while a resource is a broader term that includes any material, information, or asset that can be used to achieve a goal. In the context of MCP, a tool might be a calculator or a spreadsheet, whereas a resource could be a textbook, a dataset, or a team member’s expertise. Tools are often tangible or digital, whereas resources can be intangible. Both are essential for effective problem solving. The key difference lies in their purpose: tools execute tasks, resources provide the means to accomplish tasks.

=== Critique ===
{
  "verdict": "needs_revision",
  "feedback": [
    "The answer conflates 'resource' with 'asset' without clear distinction.",
    "The explanation of 'tool' is too generic; give a concrete example.",
    "The sentence structure is repetitive."
  ]
}

=== Final Answer ===
A tool is a device or software that performs a specific function, such as a calculator or a spreadsheet, while a resource is a broader term that includes any material, information, or asset that can be used to achieve a goal. In the context of MCP, a tool might be a calculator or a spreadsheet, whereas a resource could be a textbook, a dataset, or a team member’s expertise. Tools are often tangible or digital, whereas resources can be intangible. Both are essential for effective problem solving. The key difference lies in their purpose: tools execute tasks, resources provide the means to accomplish tasks. The main distinction is that tools are designed to perform tasks, whereas resources are the underlying assets that enable those tasks.
```

## Project Structure

```
├── main.py          # Entry point and LangGraph workflow
├── README.md        # Documentation
├── requirements.txt # Python dependencies
├── .env.example     # Example environment file
└── .gitignore
```

## Extending the Agent

- **Change the LLM** – Edit `llm = ChatOpenAI(...)` in `main.py`.
- **Adjust prompts** – Modify the `PromptTemplate` definitions.
- **Increase rounds** – Set `state["max_rounds"]` to a higher value.

## License

MIT License
