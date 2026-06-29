# LangGraph Reflection Agent

This project demonstrates a simple LangGraph agent that:
1. Drafts an answer to a user question.
2. Critiques the draft and decides if a revision is needed.
3. Rewrites the answer based on the critique.
4. Repeats the critique–rewrite loop up to a maximum number of rounds.

## Prerequisites

- Python 3.10 or newer
- An OpenAI API key (set the environment variable `OPENAI_API_KEY`)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/langgraph-reflection-agent.git
cd langgraph-reflection-agent

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\\Scripts\\activate`

# Install dependencies
pip install -e .
```

## Usage

```bash
# Run the CLI with a question
langgraph-reflection "Explain to a student the difference between tool and resource in MCP."

# Example output
Draft:
The difference between a tool and a resource in MCP is that a tool is a device or software that helps you perform a specific task, while a resource is a broader term that includes any material or information that can be used to support learning or development. Tools are often interactive and require active use, whereas resources can be passive references such as books, videos, or datasets. In MCP, tools might include calculators, code editors, or simulation software, while resources could be textbooks, research papers, or online tutorials. Tools are designed to facilitate the application of knowledge, whereas resources provide the knowledge itself. Understanding this distinction helps students choose the right support for their learning goals.

Critique:
{
  "verdict": "needs_revision",
  "feedback": [
    "The answer is too generic and does not mention MCP specifically.",
    "The explanation of 'tool' and 'resource' could be clearer.",
    "Add an example that illustrates the difference."
  ]
}

Rewritten Draft:
In the context of the MCP (Model-Driven Process), a *tool* is a specific instrument or software that assists in executing a particular task, such as a code editor or a simulation environment. A *resource*, on the other hand, is a broader category that includes any material—textbooks, research papers, or datasets—that provides knowledge or support for learning. While tools are interactive and require active use, resources can be passive references that students consult. For instance, a student might use a code editor (tool) to write and test code, while referring to a textbook (resource) to understand underlying concepts. Recognizing this distinction helps students select the appropriate support for their learning objectives.

Final Answer:
In the MCP (Model-Driven Process), a *tool* is a specific instrument or software that assists in executing a particular task, such as a code editor or a simulation environment. A *resource*, on the other hand, is a broader category that includes any material—textbooks, research papers, or datasets—that provides knowledge or support for learning. While tools are interactive and require active use, resources can be passive references that students consult. For instance, a student might use a code editor (tool) to write and test code, while referring to a textbook (resource) to understand underlying concepts. Recognizing this distinction helps students select the appropriate support for their learning objectives.
```

## How It Works

The agent follows this flow:

```
START
  └─> draft_answer
        └─> reflect
              ├─> if verdict == "ok" → END
              └─> if round < max_rounds → rewrite → reflect
```

The default maximum number of rounds is **2**.

## Customization

- Change the maximum rounds by passing `max_rounds` when initializing the graph.
- Swap the LLM provider by modifying the `get_llm()` function in `graph.py`.

## License

MIT License
