class PlannerAgent:
    """
    PHASE 1 Planner: Deterministic Formatter (Clean Output)

    - No LLM
    - No hallucination
    - Groups sources cleanly
    """

    def decide(self, evidence, product, use_case):
        if "refusal" in evidence:
            return f"REFUSAL:\n{evidence['refusal']}"

        recommended = evidence.get("recommended", [])
        avoid = evidence.get("avoid", [])

        if not recommended:
            return "REFUSAL:\nNo compatible accessories found in official specifications."

        lines = []
        lines.append("Recommended:")

        # Collect unique sources
        all_sources = set()

        for item in recommended:
            lines.append(f"- {item['accessory']}")
            all_sources.update(item.get("sources", []))

        if avoid:
            lines.append("\nAvoid:")
            for item in avoid:
                lines.append(f"- {item['accessory']}")
                all_sources.update(item.get("sources", []))

        lines.append("\nSources:")
        for src in sorted(all_sources):
            lines.append(f"- {src}")

        confidence = min(0.9, 0.6 + 0.1 * len(recommended))
        lines.append(f"\nConfidence: {round(confidence, 2)}")

        return "\n".join(lines)
