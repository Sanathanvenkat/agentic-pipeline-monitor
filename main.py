import os
import random 
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph,END
from typing import TypedDict,List

load_dotenv()

# Initialize the Groq chat model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

# State Definition
class PipelineState(TypedDict):
    pipeline_name: str
    pipeline_data: dict
    anomalies: List[str]
    root_cause: str
    action_taken: str
    status: str
    report: str

# Simulated pipeline data
def generate_pipeline_data(pipeline_name: str) -> dict:
    """Simulate real pipeline metrics"""
    scenarios = [
        {
            "pipeline": pipeline_name,
            "records_processed": 0,
            "records_expected": 50000,
            "processing_time_mins": 45,
            "expected_time_mins": 30,
            "error_count": 152,
            "null_percentage": 35.5,
            "schema_mismatch": True,
            "last_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "FAILED"
        },
        {
            "pipeline": pipeline_name,
            "records_processed": 48500,
            "records_expected": 50000,
            "processing_time_mins": 32,
            "expected_time_mins": 30,
            "error_count": 12,
            "null_percentage": 2.1,
            "schema_mismatch": False,
            "last_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "WARNING"
        },
        {
            "pipeline": pipeline_name,
            "records_processed": 50000,
            "records_expected": 50000,
            "processing_time_mins": 28,
            "expected_time_mins": 30,
            "error_count": 0,
            "null_percentage": 0.1,
            "schema_mismatch": False,
            "last_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "SUCCESS"
        }
    ]
    return random.choice(scenarios)

# Agent 1 : Monitor Agent
def monitor_agent(state: PipelineState) -> PipelineState:
    """Monitors pipeline metrics and detects anomalies"""
    print("\n Monitor Agent: Checking pipeline health...")
    
    data = state["pipeline_data"]
    anomalies = []
 
    # Check record count
    if data["records_processed"] < data["records_expected"] * 0.95:
        anomalies.append(
            f"Record count anomaly: processed {data['records_processed']} "
            f"but expected {data['records_expected']}"
        )
 
    # Check processing time
    if data["processing_time_mins"] > data["expected_time_mins"] * 1.2:
        anomalies.append(
            f"SLA breach: took {data['processing_time_mins']} mins "
            f"vs expected {data['expected_time_mins']} mins"
        )
 
    # Check error count
    if data["error_count"] > 50:
        anomalies.append(f"High error count: {data['error_count']} errors detected")
 
    # Check data quality
    if data["null_percentage"] > 5:
        anomalies.append(f"Data quality issue: {data['null_percentage']}% null values")
 
    # Check schema
    if data["schema_mismatch"]:
        anomalies.append("Schema mismatch detected between source and target")
 
    if anomalies:
        print(f"Found {len(anomalies)} anomalies!")
        for a in anomalies:
            print(f"     → {a}")
    else:
        print("Pipeline looks healthy!")
 
    return {**state, "anomalies": anomalies, "status": data["status"]}

# Agent 2 : Diagnosis Agent
def diagnosis_agent(state: PipelineState) -> PipelineState:
    """Uses LLM to perform root cause analysis"""
    print("\nDiagnosis Agent: Analyzing root cause...")
 
    if not state["anomalies"]:
        return {**state, "root_cause": "No anomalies detected. Pipeline is healthy."}
 
    prompt = ChatPromptTemplate.from_template("""
You are a senior data engineering expert performing root cause analysis.
 
Pipeline: {pipeline_name}
Status: {status}
Detected Anomalies:
{anomalies}
 
Pipeline Metrics:
{metrics}
 
Perform a concise root cause analysis. Identify:
1. Most likely root cause
2. Which anomalies are related
3. Severity level (Critical/High/Medium/Low)
 
Keep response under 150 words.
""")
 
    chain = prompt | llm | StrOutputParser()
 
    root_cause = chain.invoke({
        "pipeline_name": state["pipeline_name"],
        "status": state["status"],
        "anomalies": "\n".join(f"- {a}" for a in state["anomalies"]),
        "metrics": str(state["pipeline_data"])
    })
 
    print(f"Root Cause: {root_cause[:100]}...")
    return {**state, "root_cause": root_cause}

# Agent 3 : Recovery Agent
def recovery_agent(state: PipelineState) -> PipelineState:
    """Uses LLM to determine and execute recovery actions"""
    print("\nRecovery Agent: Determining corrective actions...")
 
    if not state["anomalies"]:
        return {**state, "action_taken": "No action needed. Pipeline healthy."}
 
    prompt = ChatPromptTemplate.from_template("""
You are a data pipeline reliability engineer.
 
Pipeline: {pipeline_name}
Root Cause Analysis: {root_cause}
Current Status: {status}
 
Based on the root cause, provide specific recovery actions:
1. Immediate action to take right now
2. Short-term fix (within 1 hour)
3. Long-term prevention measure
 
Be specific and actionable. Keep response under 150 words.
""")
 
    chain = prompt | llm | StrOutputParser()
 
    action = chain.invoke({
        "pipeline_name": state["pipeline_name"],
        "root_cause": state["root_cause"],
        "status": state["status"]
    })
 
    print(f"Action: {action[:100]}...")
    return {**state, "action_taken": action}

# Agent 4 : Reporting Agent
def reporting_agent(state: PipelineState) -> PipelineState:
    """Generates final incident report"""
    print("\nReporting Agent: Generating incident report...")
 
    prompt = ChatPromptTemplate.from_template("""
Generate a concise pipeline incident report:
 
Pipeline: {pipeline_name}
Status: {status}
Anomalies Found: {anomaly_count}
Root Cause: {root_cause}
Actions Taken: {action_taken}
Timestamp: {timestamp}
 
Format as a professional incident report with sections:
SUMMARY | FINDINGS | ACTIONS | RECOMMENDATION
 
Keep it under 200 words.
""")
 
    chain = prompt | llm | StrOutputParser()
 
    report = chain.invoke({
        "pipeline_name": state["pipeline_name"],
        "status": state["status"],
        "anomaly_count": len(state["anomalies"]),
        "root_cause": state["root_cause"],
        "action_taken": state["action_taken"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
 
    return {**state, "report": report}

# Conditional Router
def should_diagnose(state: PipelineState) -> str:
    """Route to diagnosis if anomalies found, else go straight to report"""
    if state["anomalies"]:
        return "diagnose"
    return "report"

# Build Langgraph
def build_pipeline_monitor():
    workflow = StateGraph(PipelineState)
 
    # Add agents as nodes
    workflow.add_node("monitor", monitor_agent)
    workflow.add_node("diagnose", diagnosis_agent)
    workflow.add_node("recover", recovery_agent)
    workflow.add_node("report", reporting_agent)
 
    # Entry point
    workflow.set_entry_point("monitor")
 
    # Conditional routing after monitor
    workflow.add_conditional_edges(
        "monitor",
        should_diagnose,
        {
            "diagnose": "diagnose",
            "report": "report"
        }
    )
 
    # Linear flow after diagnosis
    workflow.add_edge("diagnose", "recover")
    workflow.add_edge("recover", "report")
    workflow.add_edge("report", END)
 
    return workflow.compile()

# Main
def main():
    print("  Agentic Data Pipeline Monitoring System")
    print("  Powered by LangGraph + Groq (LLaMA 3) + Multi-Agent")
 
    app = build_pipeline_monitor()
 
    pipelines = [
        "Customer_Orders_ETL",
        "Sales_Analytics_Pipeline",
        "User_Events_Streaming",
        "Inventory_Sync_Pipeline"
    ]
 
    while True:
        print("\nAvailable Pipelines:")
        for i, p in enumerate(pipelines, 1):
            print(f"  {i}. {p}")
        print("  5. Monitor All Pipelines")
        print("  0. Exit")
 
        choice = input("\nSelect pipeline to monitor (0-5): ").strip()
 
        if choice == "0":
            print("\nShutting down monitoring system. Goodbye!")
            break
 
        elif choice == "5":
            # Monitor all pipelines
            for pipeline in pipelines:
                print(f"Monitoring: {pipeline}")
                data = generate_pipeline_data(pipeline)
                initial_state = PipelineState(
                    pipeline_name=pipeline,
                    pipeline_data=data,
                    anomalies=[],
                    root_cause="",
                    action_taken="",
                    status="",
                    report=""
                )
                result = app.invoke(initial_state)
                print("FINAL REPORT:")
                print(result["report"])
 
        elif choice in ["1", "2", "3", "4"]:
            pipeline = pipelines[int(choice) - 1]
            print(f"Monitoring: {pipeline}")
 
            data = generate_pipeline_data(pipeline)
            print(f"\nPipeline Metrics:")
            for k, v in data.items():
                print(f"  {k}: {v}")
 
            initial_state = PipelineState(
                pipeline_name=pipeline,
                pipeline_data=data,
                anomalies=[],
                root_cause="",
                action_taken="",
                status="",
                report=""
            )
 
            result = app.invoke(initial_state)
 
            print("FINAL INCIDENT REPORT:")
            print(result["report"])
 
            if result["anomalies"]:
                print(f"\nAgents Triggered: Monitor → Diagnose → Recover → Report")
            else:
                print(f"\nAgents Triggered: Monitor → Report (No issues found)")
        else:
            print("Invalid choice. Please try again.")
 
if __name__ == "__main__":
    main()