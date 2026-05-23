# Agentic Data Pipeline Monitoring System
### Powered by LangGraph · Groq (LLaMA 3) · Multi-Agent Orchestration

A production-grade multi-agent system that autonomously monitors data pipelines, performs root cause analysis, determines corrective actions, and generates professional incident reports — without any human intervention.

---

## What It Does

- Monitors multiple data pipelines simultaneously
- Detects anomalies (record count, SLA breaches, data quality, schema mismatches)
- Performs AI-powered root cause analysis using LLaMA 3
- Suggests specific corrective actions automatically
- Generates professional incident reports
- Smart routing — healthy pipelines skip unnecessary steps

---

## Multi-Agent Architecture

```
                    ┌─────────────────┐
                    │  Monitor Agent  │
                    │  Detects anomalies│
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │ Anomalies?                  │
           YES│                          NO │
              ▼                             │
   ┌──────────────────┐                    │
   │  Diagnosis Agent │                    │
   │  Root cause LLM  │                    │
   └────────┬─────────┘                    │
            │                              │
            ▼                              │
   ┌──────────────────┐                    │
   │  Recovery Agent  │                    │
   │  Corrective LLM  │                    │
   └────────┬─────────┘                    │
            │                              │
            └──────────────┬───────────────┘
                           ▼
                ┌─────────────────────┐
                │   Reporting Agent   │
                │  Incident Report LLM│
                └─────────────────────┘
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Agent Orchestration | LangGraph |
| LLM | Groq API (LLaMA 3.3 70B) |
| Framework | LangChain |
| State Management | LangGraph StateGraph |
| Language | Python |

---

## Agents

### 1. Monitor Agent
- Checks pipeline metrics against thresholds
- Detects record count anomalies, SLA breaches, error spikes, data quality issues, schema mismatches
- Routes to diagnosis if anomalies found, else straight to report

### 2. Diagnosis Agent
- Uses LLaMA 3 to perform root cause analysis
- Identifies most likely cause, related anomalies, and severity level
- Context-aware — considers all pipeline metrics

### 3. Recovery Agent
- Uses LLaMA 3 to suggest corrective actions
- Provides immediate action, short-term fix, and long-term prevention
- Based on diagnosis output for accurate recommendations

### 4. Reporting Agent
- Generates professional incident reports
- Structured format: Summary, Findings, Actions, Recommendations
- Includes timestamp and severity level

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/agentic-pipeline-monitor.git
cd agentic-pipeline-monitor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create .env file
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at: https://console.groq.com

### 4. Run the application
```bash
python main.py
```

---

## Usage

```
Agentic Data Pipeline Monitoring System
Powered by LangGraph + Groq (LLaMA 3) + Multi-Agent

Available Pipelines:
  1. Customer_Orders_ETL
  2. Sales_Analytics_Pipeline
  3. User_Events_Streaming
  4. Inventory_Sync_Pipeline
  5. Monitor All Pipelines
  0. Exit

Select pipeline to monitor (0-5): 2

Monitoring: Sales_Analytics_Pipeline

🔍 Monitor Agent: Checking pipeline health...
  ⚠️  Found 5 anomalies!
     → Record count anomaly: processed 0 but expected 50000
     → SLA breach: took 45 mins vs expected 30 mins

🧠 Diagnosis Agent: Analyzing root cause...
🔧 Recovery Agent: Determining corrective actions...
📊 Reporting Agent: Generating incident report...

FINAL REPORT:
Pipeline Incident Report: Sales_Analytics_Pipeline
...
```

---

## Project Structure

```
agentic-pipeline-monitor/
├── main.py              # Main application with all agents
├── requirements.txt     # Dependencies
├── .env                 # API keys (not pushed to GitHub)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

---

## Key Features

- **Multi-Agent Orchestration** — 4 specialized agents with defined responsibilities
- **Conditional Routing** — LangGraph routes flow based on pipeline health
- **LLM-Powered Analysis** — Root cause and recovery use LLaMA 3.3 70B
- **Stateful Workflow** — Full pipeline state passed between agents
- **Zero Human Intervention** — Fully autonomous from detection to report
- **Batch Monitoring** — Monitor all pipelines in one command

---

## Anomaly Detection Thresholds

| Metric | Threshold |
|---|---|
| Record count | < 95% of expected |
| Processing time | > 120% of expected |
| Error count | > 50 errors |
| Null percentage | > 5% |
| Schema mismatch | Any mismatch |

---

## Future Improvements

- [ ] Connect to real pipeline sources (Airflow, Databricks)
- [ ] Add Slack/email alerting integration
- [ ] Build dashboard UI with Streamlit
- [ ] Add historical anomaly tracking with ChromaDB
- [ ] Dockerize for production deployment
- [ ] Add automated pipeline restart capability

---

## Author

**Venkataraman B**
AI Engineer | LLM Systems & Enterprise Automation

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/venkataraman-b-977831244)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/Sanathanvenkat)