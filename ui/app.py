import gradio as gr
from app.pipeline.main_pipeline import run_pipeline

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# --------------------------------------------------
# Accessory options derived from PDF scope
# --------------------------------------------------
ACCESSORY_MAP = {
    "Mobile": ["Charging", "Audio", "Protection", "Connectivity"],
    "Laptop": ["Charging", "Connectivity", "Docking", "Display", "Cooling", "Audio"],
    "TV": ["Display", "Audio", "Mounting", "Power", "Connectivity"],
    "Gaming": ["Controller", "Storage", "Audio", "Display", "Power"]
}


# --------------------------------------------------
# Correct dropdown update (FORCED)
# --------------------------------------------------
def update_accessories(category):
    if not category:
        return gr.update(choices=[], value=None)

    return gr.update(
        choices=ACCESSORY_MAP[category],
        value=ACCESSORY_MAP[category][0],  # force selection
        interactive=True
    )


# --------------------------------------------------
# Run pipeline (safe)
# --------------------------------------------------
def run(category, model, accessory, use_case):
    if not category or not model or not accessory:
        return "REFUSAL:\nPlease select Category, Model, and Accessory Type."

    return run_pipeline(
        category=category.lower(),
        model=model.strip(),
        accessory=accessory.lower(),
        use_case=use_case.strip() if use_case else ""
    )


# --------------------------------------------------
# UI Layout
# --------------------------------------------------
with gr.Blocks(title="AccessoryIQ") as demo:
    gr.Markdown("## 🔌 AccessoryIQ – Evidence-Based Accessory Intelligence")

    category = gr.Dropdown(
        choices=["Mobile", "Laptop", "TV", "Gaming"],
        label="Product Category",
        interactive=True
    )

    accessory = gr.Dropdown(
        choices=["Select category first"],  # IMPORTANT
        label="Accessory Type",
        interactive=True,
        allow_custom_value=False
    )

    model = gr.Textbox(
        label="Product Model",
        placeholder="e.g., iPhone 15, Dell XPS 13, Samsung QN90C"
    )

    use_case = gr.Textbox(
        label="Use Case (optional)",
        placeholder="e.g., gaming, office work, travel"
    )

    category.change(
        fn=update_accessories,
        inputs=category,
        outputs=accessory
    )

    output = gr.Textbox(
        label="Accessory Recommendation",
        lines=22,
        interactive=False
    )

    submit = gr.Button("Get Recommendation")

    submit.click(
        fn=run,
        inputs=[category, model, accessory, use_case],
        outputs=output
    )

demo.launch()
