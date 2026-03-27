# CostPilot AI

AI for Enterprise Cost Intelligence and Autonomous Action

My solution for Problem Statement 3 of the ET AI Hackathon 2026:

`AI for Enterprise Cost Intelligence & Autonomous Action`

## Problem Statement
Build an AI system that goes beyond dashboards. It should continuously monitor enterprise operations data, identify cost leakage or inefficiency patterns, and initiate corrective actions with quantifiable financial impact.

## Solution Overview
CostPilot AI is a multi-agent prototype that detects enterprise cost leakage, estimates business impact, and shows how a case moves from detection to action inside an approval-based workflow.

The solution focuses on:
- duplicate invoice detection
- vendor rate optimization
- unused software license detection
- SLA breach and penalty prevention

## Prototype
This repository includes a working local browser prototype.

### Run The Prototype
```bash
cd "/Users/saurabhbarve/Documents/New project"
python3 app/web_app.py
```

Open in browser:
```text
http://127.0.0.1:8000
```

### Hosting Note
The current demo is designed for local prototype use.

### What The Prototype Includes
- upload-based CSV testing flow
- sample analysis mode
- case-by-case agent workflow
- case summary with issue, root cause, recommended action, and fallback path
- approval simulation
- downloadable report and dashboard

### Run The Analysis Script
```bash
cd "/Users/saurabhbarve/Documents/New project"
python3 app/main.py
```

## Multi-Agent Workflow
- Monitoring Agent
- Impact Agent
- Decision Agent
- Approval Agent
- Action Agent
- Audit Agent

## Setup Instructions
1. Install Python 3 if required
2. Open Terminal
3. Go to the project folder
4. Run `python3 app/web_app.py`
5. Open `http://127.0.0.1:8000`

## Folder Structure
```text
app/      -> application logic and browser prototype
data/     -> sample CSV datasets
docs/     -> pitch, architecture, and supporting material
output/   -> generated dashboard/report output
```

## Tech Stack
- Python 3
- CSV datasets
- HTML/CSS/JavaScript prototype UI
- Markdown report output

## Architecture Summary
The workflow is designed as a connected agent system:
- one agent identifies the issue
- one agent calculates the impact
- one agent recommends the next step
- one agent manages approval logic
- one agent prepares the action
- one agent logs the workflow

Each case is presented in a simple business flow so a non-technical people can follow how agents pass the case from detection to decision.

## Impact Model
The prototype estimates savings using simple business logic:
- duplicate invoice savings = blocked duplicate payment amount
- vendor savings = benchmark gap x usage
- license savings = inactive licenses x monthly license cost
- SLA savings = avoided penalty exposure

## Assumptions
- duplicate invoices can be prevented before payment is processed
- vendor rates can be improved through renegotiation or vendor shift
- inactive licenses can be removed in the next billing cycle
- high-risk SLA cases can be escalated early enough to reduce or avoid penalty impact

## Business Context
I approached this problem from a Business Analyst perspective with insurance-domain experience in workflow improvement, reporting, process control, and operational efficiency.

## Insurance Relevance
This design is also relevant to insurance operations:
- duplicate claim-related payments
- SLA risks in claims processing queues
- reconciliation mismatches
- partner and vendor inefficiencies

## Enterprise Extensions
In a production environment, the same model could connect to:
- SAP / Oracle / ERP systems
- ServiceNow / Jira / Zendesk
- Slack / Teams / Email approvals
- SaaS admin tools
- audit logs and dashboards

## Hackathon Repository Fit
This repository includes:
- source code
- setup instructions
- a working prototype
- supporting architecture and pitch material in `docs/`
- commit history showing the build process
