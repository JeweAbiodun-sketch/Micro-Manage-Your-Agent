# Micromanage Your Agents

> A custom LangSmith evaluation lab for **AI-assisted blog writing** — building a dataset, tracing model calls, scoring outputs with LLM-as-judge evaluators, and comparing models side-by-side.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Quick Start](#quick-start)
- [Notebook Walkthrough](#notebook-walkthrough)
- [Evaluation Results](#evaluation-results)
- [Key Findings](#key-findings)
- [Author](#author)

---

## Project Overview

This project implements a full LangSmith evaluation pipeline for a blog content generation system. Given a topic and a writing brief, the system generates a 600–800 word blog post and scores it across three quality dimensions using LLM-as-judge evaluators.

**Goals:**

- Build a reproducible custom evaluation dataset with 10 domain-specific examples
- Trace all model calls through LangSmith for full observability
- Evaluate `gpt-4o-mini` and `gpt-4o` side-by-side on the same dataset
- Identify failure patterns and make data-driven model recommendations

This was first executed using 10 examples and subsequently run using 20 examples to compare results.

---

## Repository Structure

```text
Micromanage_your_agents/
│
├── blog_eval_lab
├── blog_eval_langsmith.ipynb   # Main lab notebook
├── .env                        # Local credentials (not committed)
│
├── Screenshots/
│   ├── Screenshot 2026-05-30 074207.png   # LangSmith A/B comparison dashboard
│   ├── Screenshot 2026-05-30 074526.png   # Per-example score table
│   └── Screenshot 2026-05-30 074823.png   # gpt-4o experiment detail + latency
│
├── evaluation_summary.md     # Methodology, results, and key findings
├── evaluation_report.md      # Full analysis — error patterns, per-example scores, recommendations
├── optimization_summary.md   # Cost-performance analysis and model selection guide
└── README.md                 # This file
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A [LangSmith API key](https://smith.langchain.com)

### 1. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create `blog_eval_lab/.env` with the following:

```env
OPENAI_API_KEY=sk-...
LANGSMITH_API_KEY=ls__...
LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com
LANGSMITH_PROJECT=blog_eval_langsmith
```

### 4. Select the Jupyter kernel

In VS Code or Jupyter, open the notebook and select **"Python (Micro-Manage-Your-Agent)"** from the kernel picker.

This kernel is registered from the project `.venv`, so notebook cells will run in the same environment as the dependency install above.

### 5. Run the notebook

Open `blog_eval_lab/blog_eval_langsmith.ipynb` and run all cells **top to bottom**.

---

## Notebook Walkthrough

| Section | Description |
| --- | --- |
| **1. Tracing** | `@traceable` smoke-test — one live blog post logged to LangSmith |
| **2. Dataset** | 10 blog-writing examples pushed to `blog-writing-eval` in LangSmith |
| **3. Experiment** | `gpt-4o-mini` target + 3 LLM-as-judge evaluators via `client.evaluate()` |
| **4. A/B Comparison** | Same dataset evaluated with `gpt-4o` for side-by-side model comparison |
| **5. Results** | Mean scores per dimension and per model in a pandas DataFrame |
| **6. Reproducibility** | Same input run twice to demonstrate output variance at `temperature=0.7` |

---

## Evaluation Results

Three LLM-as-judge evaluators score each blog post on a **0–100 scale**:

| Dimension | What it measures |
| --- | --- |
| `coverage` | Does the post address all outline points and key requirements from the brief? |
| `structure_clarity` | Clear intro, descriptive H2 sections, short paragraphs, concise conclusion? |
| `tone_match` | Does the tone and language match the specified audience and brief? |

### Model Comparison — 10-Example Run

| Model | Coverage | Structure Clarity | Tone Match | Overall | Avg Latency | Relative Cost |
| --- | --- | --- | --- | --- | --- | --- |
| `gpt-4o-mini` | 80.5 | 82.0 | 81.0 | **81.2** | ~5.5 s | 1× |
| `gpt-4o` | 78.5 | 83.0 | 82.0 | **81.2** | ~9.4 s | ~3–4× |

### Model Comparison — 20-Example Run

| Model | Coverage | Structure Clarity | Tone Match | Overall | Relative Cost |
| --- | --- | --- | --- | --- | --- |
| `gpt-4o-mini` | 80.05 | 81.75 | 84.25 | **82.0** | 1× |
| `gpt-4o` | 77.40 | 80.40 | 86.25 | **81.4** | ~3–4× |

---

## Key Findings

- **gpt-4o-mini leads at 20 examples (82.0 vs 81.4)** — models tied at 10 examples; doubling the dataset breaks the tie
- **Coverage is the weakest dimension** — posts satisfy 2 of 3 key requirements across both runs; the most consistent failure
- **Tone match improved significantly at scale** (+3.25 for mini, +4.25 for gpt-4o) — diverse topic briefs play to tone strengths
- **gpt-4o structure degrades at scale (−2.60)** — over-elaborates on open-ended topics; gpt-4o-mini holds steady (−0.25)
- **Model gap is negligible (≤3 pts per dimension)** — prompt quality drives results more than model choice
- **Recommendation: use `gpt-4o-mini`** for human-reviewed workflows — better average at 20 examples, 3–4× lower cost

> For full analysis, error breakdowns, and recommendations see [`evaluation_report.md`](evaluation_report.md)

---

## Author

**Abiodun Olawuyi**
Prepared as part of the IronHack *Micromanage Your Agents* Lab — LangSmith Evaluation Module.

