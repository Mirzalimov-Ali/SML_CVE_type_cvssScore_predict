import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/predict"


def predict(cve_id, description, cwe, vendor, product, publish_date):
    payload = {
        "cve_id": cve_id,
        "description": description,
        "cwe": cwe,
        "vendor": vendor,
        "product": product,
        "publish_date": publish_date
    }

    response = requests.post(API_URL, json=payload, timeout=5)
    response.raise_for_status()
    result = response.json()

    return result["attack_type"], result["cvss_score"]


CUSTOM_CSS = """
body {
    background: radial-gradient(circle at top, #0f172a, #020617);
}

/* center everything */
.center {
    max-width: 720px;
    margin: auto;
    padding: 40px;
}

.gr-box {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.08);
}

h1 {
    text-align: center;
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 30px;
}

.gradient-text {
    background: linear-gradient(to right, #38bdf8, #22c55e);
    -webkit-background-clip: text;
    color: transparent;
}

button {
    width: 100%;
    background: linear-gradient(135deg, #22c55e, #38bdf8) !important;
    color: black !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    height: 58px !important;
}

.gr-textbox label {
    text-align: left !important;
}

"""


with gr.Blocks(css=CUSTOM_CSS, theme=gr.themes.Soft()) as demo:

    with gr.Column(elem_classes="center"):

        gr.Markdown("""
        <h1>
            🔐 <span class="gradient-text">CVE Attack Type & Cvss Score Predictor</span>
        </h1>
        """)

        Cve_Id = gr.Textbox(label="CVE ID", placeholder="CVE-2023-12345")
        Cwe = gr.Textbox(label="CWE", placeholder="CWE-79")
        publish_date = gr.Textbox(label="Publish Date", placeholder="YYYY-MM-DD")
        vendor = gr.Textbox(label="Vendor", placeholder="linagora")
        product = gr.Textbox(label="Affected Product")

        Description = gr.Textbox(
            label="Description",
            lines=5,
            placeholder="Detailed vulnerability description..."
        )

        predict_btn = gr.Button("🚀 Predict CVE")

        attack_type = gr.Textbox(
            label="Predicted Attack Type",
            interactive=False
        )

        cvss_score = gr.Textbox(
            label="Predicted CVSS Score",
            interactive=False
        )

        predict_btn.click(
            predict,
            inputs=[
                Cve_Id,
                Description,
                Cwe,
                vendor,
                product,
                publish_date
            ],
            outputs=[
                attack_type,
                cvss_score
            ]
        )


if __name__ == "__main__":
    demo.launch()
