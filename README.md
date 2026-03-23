# CostPilot AI

AI for Enterprise Cost Intelligence and Autonomous Action

This project is a simple hackathon starter for Problem Statement 3 from the ET AI Hackathon 2026:

`AI for Enterprise Cost Intelligence & Autonomous Action`

It monitors sample enterprise data, identifies cost leakage, recommends actions, and calculates estimated monthly savings.

## What This Project Does
- Detects possible duplicate invoices
- Finds vendor rate optimization opportunities
- Finds unused software licenses
- Detects SLA breach risks before penalties happen
- Creates a business-style impact report

## Folder Structure
```text
app/      -> main Python logic
data/     -> sample CSV data
docs/     -> solution explanation
output/   -> generated report after running the code
```

## Tech Stack
- Python 3
- CSV files for sample input
- Markdown output report

## How To Run This Project

### Step 1: Install Python
Check if Python is already installed:

```bash
python3 --version
```

If you see a version number, you are ready.

### Step 2: Open this project folder
In terminal:

```bash
cd "/Users/saurabhbarve/Documents/New project"
```

### Step 3: Run the program
```bash
python3 app/main.py
```

### Step 4: See the report
The report will also be saved here:

`output/cost_intelligence_report.md`

## Sample Output
- Total identified monthly savings
- List of problems found
- Recommended action for each problem
- Estimated savings for each action

## Real-Life Implementation Plan

### Phase 1: Start Small
1. Pick one department first, like procurement or customer support.
2. Collect 3 data sources only:
   - invoice data
   - vendor contract rates
   - SLA or ticket data
3. Define 3 cost leakage problems to solve first.

### Phase 2: Build The Detection Layer
1. Connect data from ERP, ticketing, and SaaS tools.
2. Clean the data and standardize vendor names, dates, and cost fields.
3. Build rules and AI checks for:
   - duplicate invoices
   - high vendor rates
   - low software usage
   - upcoming SLA breaches

### Phase 3: Add Decision Intelligence
1. For each finding, define the next best action.
2. Add business rules:
   - low-risk actions can be auto-created as tasks
   - medium-risk actions go for manager approval
   - high-risk actions go to finance or operations head

### Phase 4: Add Action Layer
1. Create approval workflows in email, Slack, Teams, or ticketing systems.
2. Trigger actions automatically after approval.
3. Log every action for audit purposes.

### Phase 5: Measure Business Impact
1. Track money saved every month.
2. Track penalties avoided.
3. Track cycle time reduced.
4. Compare before vs after implementation.

## Practical Solution For Hackathon Presentation

### Problem
Enterprises lose money because waste is found too late.

### Solution
CostPilot AI monitors operations daily, detects leakage, and starts corrective action automatically.

### Value
- Lower operational cost
- Faster action
- Better control and auditability
- Clear ROI

## How To Upload This To GitHub

### Step 1: Create a GitHub account
Go to [GitHub](https://github.com/) and create an account if you do not have one.

### Step 2: Create a new repository
Repository name suggestion:

`costpilot-ai`

Keep it Public.

### Step 3: In terminal, run these commands
```bash
cd "/Users/saurabhbarve/Documents/New project"
git status
git add .
git commit -m "Add CostPilot AI hackathon starter project"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

Replace `YOUR_GITHUB_REPO_URL` with your GitHub repository URL.

Example:
```bash
git remote add origin https://github.com/yourname/costpilot-ai.git
```

## Suggested Demo Flow
1. Explain the business problem in simple terms
2. Show the sample data files
3. Run the Python program
4. Show the report generated
5. Explain how approvals and auto-actions would work in a real company
6. Show the savings math

## Important Note
This is a starter version for hackathon use. In a real company, you would connect this to:
- SAP / Oracle / ERP systems
- ServiceNow / Jira / Zendesk
- Slack / Teams / Email approvals
- SaaS admin tools
- Audit logs and dashboards
