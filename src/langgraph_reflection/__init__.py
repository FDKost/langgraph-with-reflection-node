from typing import TypedDict, Dict, Any
import json
import argparse
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START

class ReflectState(TypedDict):
    question: str
    draft: str
    critique: str
    verdict: str
    round: int
    max_rounds: int

def draft_answer(state: ReflectState) -> Dict[str, Any]:
    llm = ChatOpenAI()
    prompt = f"Answer the following question in 5-10 sentences:\n\nQuestion: {state['question']}"
    answer = llm.invoke(prompt)
    return {"draft": answer}

def reflect(state: ReflectState) -> Dict[str, Any]:
    llm = ChatOpenAI()
    prompt = f"""Critique the following draft answer. Output a JSON object with keys:
- verdict: 'ok' or 'needs_revision'
- critique: a string with 2-3 critique points.

Draft: {state['draft']}"""
    response = llm.invoke(prompt)
    try:
        data = json.loads(response)
        verdict = data.get("verdict", "needs_revision")
        critique = data.get("critique", "")
    except json.JSONDecodeError:
        verdict = "needs_revision"
        critique = response
    return {"verdict": verdict, "critique": critique}

def rewrite(state: ReflectState) -> Dict[str, Any]:
    llm = ChatOpenAI()
    prompt = f"""Rewrite the draft answer incorporating the following critique. Ensure the answer is improved and still 5-10 sentences.

Draft: {state['draft']}

Critique: {state['critique']}"""
    new_answer = llm.invoke(prompt)
    return {"draft": new_answer, "round": state["round"] + 1}

def condition(state: ReflectState) -> str:
    if state["verdict"] == "ok":
        return "END"
    elif state["round"] < state["max_rounds"]:
        return "rewrite"
    else:
        return "END"

def build_graph() -> StateGraph:
    graph = StateGraph(ReflectState)
    graph.add_node("draft_answer", draft_answer)
    graph.add_node("reflect", reflect)
    graph.add_node("rewrite", rewrite)

    graph.add_edge(START, "draft_answer")
    graph.add_edge("draft_answer", "reflect")
    graph.add_conditional_edges("reflect", condition, {"rewrite": "rewrite", "END": END})
    graph.add_edge("rewrite", "reflect")

    return graph.compile()

def main() -> None:
    parser = argparse.ArgumentParser(description="LangGraph Reflection Demo")
    parser.add_argument("question", type=str, help="Question to answer")
    parser.add_argument("--max-rounds", type=int, default=2, help="Maximum number of reflection rounds")
    args = parser.parse_args()

    initial_state: ReflectState = {
        "question": args.question,
        "draft": "",
        "critique": "",
        "verdict": "",
        "round": 1,
        "max_rounds": args.max_rounds,
    }

    graph = build_graph()
    final_state = graph.invoke(initial_state)

    print("\nFinal Answer:\n", final_state["draft"])
    print("\nCritique:\n", final_state["critique"])
    print("\nVerdict:\n", final_state["verdict"])

if __name__ == "__main__":
    main()
