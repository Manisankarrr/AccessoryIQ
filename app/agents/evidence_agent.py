from app.rag.vector_store import VectorStore


class EvidenceAgent:
    """
    RAG-FIRST Evidence Agent
    - Uses RAG if possible
    - Signals when search fallback is needed
    """

    def __init__(self):
        self.vs = VectorStore()
        self.vs.load()

    def gather(self, category, brand, model, accessory_type):
        rag_chunks = self.vs.search(
            query=f"{brand} {accessory_type} compatible accessories",
            category=category,
            brand=brand
        )

        supported_models = self._extract_supported_models(rag_chunks)

        # 🚨 MODEL NOT FOUND → TRIGGER SEARCH
        if not self._model_supported(model, supported_models):
            return {
                "needs_search": True,
                "reason": f"Model '{model}' not found in official documentation"
            }

        # Extract accessories from RAG
        result = self._extract_accessories(rag_chunks, model, accessory_type)

        if not result["recommended"]:
            return {
                "needs_search": True,
                "reason": "No accessories found in official documentation"
            }

        return result

    # ----------------------------
    # MODEL EXTRACTION
    # ----------------------------
    def _extract_supported_models(self, chunks):
        models = set()

        for chunk in chunks:
            lines = [l.strip() for l in chunk["text"].splitlines()]
            in_section = False

            for line in lines:
                if "supported models" in line.lower():
                    in_section = True
                    continue

                if in_section:
                    if not line.startswith(("•", "-")):
                        break
                    models.add(line.lstrip("•- ").strip().lower())

        return models

    def _model_supported(self, model, supported_models):
        model = model.lower()
        return any(model in m or m in model for m in supported_models)

    # ----------------------------
    # ACCESSORY EXTRACTION
    # ----------------------------
    def _extract_accessories(self, chunks, model, accessory_type):
        SECTION_MAP = {
            "charging": ["charging", "power"],
            "audio": ["audio"],
            "cooling": ["cooling"],
            "display": ["display"],
            "connectivity": ["connectivity"],
            "storage": ["storage"],
            "controller": ["controller"]
        }

        valid_sections = SECTION_MAP.get(accessory_type.lower(), [])

        recommended = []

        for chunk in chunks:
            source = chunk["source_pdf"]
            lines = [l.strip() for l in chunk["text"].splitlines() if l.strip()]

            current_section = None

            for line in lines:
                lower = line.lower()

                for sec in valid_sections:
                    if sec in lower:
                        current_section = sec
                        break

                if not current_section:
                    continue

                if "compatible" in lower:
                    continue

                if line.startswith(("•", "-", "o")):
                    recommended.append({
                        "accessory": line.lstrip("•-o ").strip(),
                        "reason": "Listed as a compatible accessory in official specifications",
                        "sources": [source]
                    })

        return {
            "recommended": self._dedupe(recommended),
            "avoid": []
        }

    def _dedupe(self, items):
        seen = set()
        out = []
        for item in items:
            if item["accessory"] not in seen:
                seen.add(item["accessory"])
                out.append(item)
        return out
