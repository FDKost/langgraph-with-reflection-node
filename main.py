import os
import json
import argparse
from typing import TypedDict, Dict, Any
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Define the state structure
class ReflectState(TypedDict):
    question: str
    draft: str
    critique: str
    verdict: str
    round: int
    max_rounds: int
    # Optional keys for debugging / demonstration
    draft_before_rewrite: str

# Initialize the LLM
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# Prompt templates
draft_prompt = PromptTemplate(
    input_variables=["question"],
    template=(
        "Write a concise answer (5-10 sentences) to the following question:\n\n{question}"
    ),
)

reflect_prompt = PromptTemplate(
    input_variables=["draft"],
    template=(
        "You are a reviewer. Critique the following answer:\n\n{draft}\n\n"
        "Provide a verdict: 'ok' if the answer is satisfactory, otherwise 'needs_revision'.\n"
        "Also provide 2-3 points of feedback. Output in JSON format with keys 'verdict' and 'feedback'."
    ),
)

rewrite_prompt = PromptTemplate(
    input_variables=["draft", "feedback"],
    template=(
        "Rewrite the answer incorporating the following feedback:\n\n{feedback}\n\n"
        "Original answer:\n\n{draft}\n\n"
        "Provide a revised answer that is concise and correct."
    ),
)

# Node functions
def draft_answer(state: ReflectState) -> ReflectState:
    question = state["question"]
    prompt = draft_prompt.format(question=question)
    response = llm.invoke(prompt)
    state["draft"] = response.strip()
    state["draft_before_rewrite"] = state["draft"]
    return state

def reflect(state: ReflectState) -> ReflectState:
    draft = state["draft"]
    prompt = reflect_prompt.format(draft=draft)
    response = llm.invoke(prompt)
    try:
        data = json.loads(response.strip())
        state["verdict"] = data.get("verdict", "needs_revision").lower()
        state["critique"] = data.get("feedback", "")
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        state["verdict"] = "needs_revision"
        state["critique"] = response.strip()
    return state

def rewrite(state: ReflectState) -> ReflectState:
    draft = state["draft"]
    feedback = state["critique"]
    prompt = rewrite_prompt.format(draft=draft, feedback=feedback)
    response = llm.invoke(prompt)
    state["draft"] = response.strip()
    state["round"] += 1
    return state

def condition(state: ReflectState) -> str:
    if state["verdict"] == "ok" or state["round"] >= state["max_rounds"]:
        return "end"
    return "rewrite"

# Main entry point
def main():
    parser = argparse.ArgumentParser(description="LangGraph Reflection Agent")
    parser.add_argument("question", type=str, help="The question to answer")
    args = parser.parse_args()

    # Initial state
    state: ReflectState = {
        "question": args.question,
        "draft": "",
        "critique": "",
        "verdict": "",
        "round": 1,
        "max_rounds": 2,
        "draft_before_rewrite": "",
    }

    # Build the graph
    graph = StateGraph(ReflectState)
    graph.add_node("draft_answer", draft_answer)
    graph.add_node("reflect", reflect)
    graph.add_node("rewrite", rewrite)
    graph.add_conditional_edges("reflect", condition, {"rewrite": "rewrite", "end": END})
    graph.set_entry_point("draft_answer")
    graph.add_edge("rewrite", "reflect")

    # Run the graph
    final_state = graph.invoke(state)

    # Display results
    print("\n=== Draft (Round 1) ===")
    print(state["draft_before_rewrite"])
    print("\n=== Critique ===")
    print(state["critique"])
    print("\n=== Final Answer ===")
    print(final_state["draft"])

if __name__ == "__main__":
    main()
