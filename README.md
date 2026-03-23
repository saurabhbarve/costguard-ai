# CostPilot AI

AI for Enterprise Cost Intelligence and Autonomous Action

This project was created as my solution for Problem Statement 3 of the ET AI Hackathon 2026:

`AI for Enterprise Cost Intelligence & Autonomous Action`

I come from a Business Analyst background with experience in the insurance domain, so I approached this problem from a business-value, workflow-control, and process-improvement angle rather than only from a coding angle.

My core idea was simple:
many enterprises do not lose money because of one large failure. They lose money through repeated leakages like duplicate invoices, poor vendor pricing, unused licenses, and avoidable SLA penalties.

CostPilot AI is a starter solution that shows how an AI-driven system can detect those issues early, recommend the next action, and estimate the financial impact in a practical way.

My work experience in claims-related process automation, requirement gathering, workflow design, SQL-based analysis, reporting, and UAT strongly influenced how I thought about this solution. I wanted to build something that looks realistic from an enterprise operations point of view.

## What This Project Does
- Detects possible duplicate invoices
- Finds vendor rate optimization opportunities
- Finds unused software licenses
- Detects SLA breach risks before penalties happen
- Creates a business-style impact report

## Why I Chose This Problem
I chose this problem because it sits at the intersection of business operations, cost control, and decision-making.

As a Business Analyst, this is the kind of challenge where I can add the most value:
- identify process inefficiencies
- define business rules
- map approval workflows
- connect actions to measurable business outcomes

For me, this problem is not just about AI.
It is about using AI in a way that is useful, measurable, and realistic for enterprise teams.

## Why I Am A Good Fit For This Problem
My background is in insurance operations and business analysis, where process delays, workflow gaps, and manual checks directly affect both cost and customer experience.

In my professional work, I have been involved in:
- claims workflow improvement
- process automation
- requirement gathering and documentation
- stakeholder coordination
- data analysis through SQL and Power BI
- UAT and production readiness

Because of that, I relate strongly to this problem statement.
I understand that enterprise AI is only useful when it fits into real workflows, approval structures, and measurable business KPIs.

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

## My Business Assumptions
This project uses sample data, so the savings numbers are directional and meant for demonstration.

The assumptions behind the model are:
- duplicate invoices can be prevented before payment is processed
- high vendor rates can be reduced through renegotiation or vendor shift
- inactive licenses can be removed in the next billing cycle
- high-risk SLA cases can be escalated in time to avoid part or all of the penalty

In a real enterprise implementation, these assumptions would be validated with finance, procurement, and operations teams.

## Insurance-Domain Relevance
Although this solution is designed as a general enterprise cost intelligence system, it is highly relevant to insurance operations as well.

Examples in insurance environments could include:
- identifying duplicate claim-related payments
- tracking SLA risks in claims processing queues
- finding reconciliation mismatches across insurer systems
- highlighting vendor or partner process inefficiencies
- reducing manual review effort through workflow-based actioning

This is one reason I found the problem especially meaningful from my own professional background.

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
This is a starter version built for hackathon demonstration. In a real company, the same design could be connected to:
- SAP / Oracle / ERP systems
- ServiceNow / Jira / Zendesk
- Slack / Teams / Email approvals
- SaaS admin tools
- Audit logs and dashboards

## Final Thought
The main purpose of this project is to show that enterprise AI should not stop at insights and dashboards.

If the system can detect leakage, estimate impact, and trigger the next best action within a controlled workflow, then it can create real business value.
