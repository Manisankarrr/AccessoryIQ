from app.agents.evidence_agent import EvidenceAgent
from app.agents.search_agent import SearchAgent
from app.agents.planner_agent import PlannerAgent
import logging


def run_pipeline(category, model, accessory, use_case):
    logging.info(f"[PIPELINE] {category=} {model=} {accessory=}")

    evidence_agent = EvidenceAgent()
    search_agent = SearchAgent()
    planner = PlannerAgent()

    evidence = evidence_agent.gather(
        category=category,
        brand=model.split()[0],
        model=model,
        accessory_type=accessory
    )

    # --- RAG FAILS → SEARCH ---
    if evidence.get("needs_search"):
        logging.info("[PIPELINE] RAG failed → invoking SearchAgent")
        return search_agent.search(model, accessory)

    # --- RAG SUCCESS ---
    logging.info("[PIPELINE] RAG successful → Planner formatting")
    return planner.decide(evidence, model, use_case)
