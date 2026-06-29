import argparse
import json
import os

from graph import run_agent

def main():
    parser = argparse.ArgumentParser(description="LangGraph Reflection Agent CLI")
    parser.add_argument("question", type=str, help="The question to answer")
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=2,
        help="Maximum number of critique–rewrite rounds (default: 2)",
    )
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY environment variable not set")

    final_state = run_agent(args.question, args.max_rounds)

    print("\n=== Draft ===")
    print(final_state["draft"])
    print("\n=== Critique ===")
    print(json.dumps(json.loads(final_state["critique"]), indent=2))
    print("\n=== Final Answer ===")
    print(final_state["draft"])

if __name__ == "__main__":
    main()
