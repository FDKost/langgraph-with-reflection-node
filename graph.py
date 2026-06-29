from typing import TypedDict, List, Dict, Any
import json
import os

from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

# ---------- State Definition ----------
class ReflectState(TypedDict):
    question: str
    draft: str
    critique: str  # JSON string with verdict and feedback
    verdict: str   # "ok" or "needs_revision"
    round: int
    max_rounds: int

# ---------- LLM Setup ----------
def get_llm():
    return ChatOpenAI(
        temperature=0.7,
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

# ---------- Draft Node ----------
draft_prompt = PromptTemplate(
    input_variables=["question"],
    template=(
        "You are an expert tutor. Answer the following question in 5-10 sentences:\n"
        "Question: {question}\n"
        "Answer:"
    ),
)

def draft_answer(state: ReflectState) -> Dict[str, Any]:
    llm = get_llm()
    chain = draft_prompt | llm | StrOutputParser()
    draft = chain.invoke({"question": state["question"]}).strip()
    return {"draft": draft, "round": 0, "verdict": ""}

# ---------- Reflection Node ----------
reflect_prompt = PromptTemplate(
    input_variables=["draft"],
    template=(
        "You are a critical reviewer. Critique the following draft answer.\n"
        "Draft:\n{draft}\n\n"
        "Provide a JSON object with the following keys:\n"
        "  - verdict: \"ok\" if the answer is satisfactory, otherwise \"needs_revision\"\n"
        "  - feedback: a list of 2-3 concise points for improvement\n"
        "Example output:\n"
        "{{\"verdict\": \"needs_revision\", \"feedback\": [\"Point 1\", \"Point 2\"]}}\n"
        "Your output:"
    ),
)

def reflect(state: ReflectState) -> Dict[str, Any]:
    llm = get_llm()
    chain = reflect_prompt | llm | StrOutputParser()
    critique = chain.invoke({"draft": state["draft"]}).strip()
    # Ensure valid JSON
    try:
        critique_json = json.loads(critique)
    except json.JSONDecodeError:
        # Fallback: treat entire output as feedback
        critique_json = {"verdict": "needs_revision", "feedback": [critique]}
    verdict = critique_json.get("verdict", "needs_revision")
    return {"critique": json.dumps(critique_json), "verdict": verdict}

# ---------- Rewrite Node ----------
rewrite_prompt = PromptTemplate(
    input_variables=["draft", "feedback"],
    template=(
        "You are rewriting the following draft answer based on the provided feedback.\n"
        "Draft:\n{draft}\n\n"
        "Feedback:\n{feedback}\n\n"
        "Rewrite the answer to address the feedback. Keep the answer concise and clear.\n"
        "Rewritten Answer:"
    ),
)

def rewrite(state: ReflectState) -> Dict[str, Any]:
    llm = get_llm()
    feedback = json.loads(state["critique"]).get("feedback", [])
    feedback_text = "\n".join(f"- {item}" for item in feedback)
    chain = rewrite_prompt | llm | StrOutputParser()
    new_draft = chain.invoke({"draft": state["draft"], "feedback": feedback_text}).strip()
    new_round = state["round"] + 1
    return {"draft": new_draft, "round": new_round}

# ---------- Graph Definition ----------
def create_graph(max_rounds: int = 2) -> StateGraph[ReflectState]:
    graph = StateGraph(ReflectState)

    # Set the maximum rounds in the state
    def set_max_rounds(state: ReflectState) -> Dict[str, Any]:
        return {"max_rounds": max_rounds}

    graph.add_node("set_max_rounds", set_max_rounds)
    graph.add_node("draft_answer", draft_answer)
    graph.add_node("reflect", reflect)
    graph.add_node("rewrite", rewrite)

    # Flow
    graph.set_entry_point("set_max_rounds")
    graph.add_edge("set_max_rounds", "draft_answer")
    graph.add_edge("draft_answer", "reflect")

    def should_continue(state: ReflectState) -> str:
        if state["verdict"] == "ok":
            return "END"
        if state["round"] < state["max_rounds"]:
            return "rewrite"
        return "END"

    graph.add_conditional_edges("reflect", should_continue, {"rewrite": "rewrite", "END": "END"})
    graph.add_edge("rewrite", "reflect")

    return graph.compile()

# ---------- Helper to Run ----------
def run_agent(question: str, max_rounds: int = 2) -> Dict[str, Any]:
    graph = create_graph(max_rounds)
    initial_state: ReflectState = {
        "question": question,
        "draft": "",
        "critique": "",
        "verdict": "",
        "round": 0,
        "max_rounds": max_rounds,
    }
    final_state = graph.invoke(initial_state)
    return final_state
