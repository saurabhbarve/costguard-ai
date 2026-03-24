from __future__ import annotations

import cgi
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from main import AgentCase, DATA_DIR, Finding, analyze_datasets, build_agent_cases, build_report, read_csv, read_csv_text


HOST = "127.0.0.1"
PORT = 8000
LAST_RESULT: dict[str, str] = {}


def load_default_rows() -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    return (
        read_csv(DATA_DIR / "procurement_spend.csv"),
        read_csv(DATA_DIR / "resource_utilization.csv"),
        read_csv(DATA_DIR / "sla_operations.csv"),
    )


def landing_page() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CostPilot AI Prototype</title>
  <style>
    :root {
      --bg-1: #edf4f7;
      --bg-2: #dce9ee;
      --panel: rgba(255,255,255,0.92);
      --ink: #16313b;
      --muted: #58707a;
      --primary: #0d6e8a;
      --secondary: #1b8f6e;
      --accent: #d97706;
      --line: #c8d9df;
    }
    body {
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      background: linear-gradient(135deg, var(--bg-1) 0%, var(--bg-2) 100%);
      color: var(--ink);
    }
    .wrap {
      max-width: 1100px;
      margin: 0 auto;
      padding: 36px 20px 48px;
    }
    .hero, .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 24px;
      padding: 28px;
      box-shadow: 0 18px 34px rgba(12, 39, 49, 0.08);
      margin-bottom: 22px;
    }
    h1 {
      margin: 0 0 10px;
      font-size: 2.5rem;
    }
    p {
      line-height: 1.6;
    }
    .eyebrow {
      display: inline-block;
      margin-bottom: 12px;
      padding: 8px 12px;
      border-radius: 999px;
      background: #e5f2f6;
      color: var(--primary);
      font-weight: bold;
      font-size: 0.9rem;
      letter-spacing: 0.02em;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 18px;
    }
    label {
      display: block;
      font-weight: bold;
      margin-bottom: 8px;
    }
    input[type="file"] {
      width: 100%;
      padding: 12px;
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 12px;
    }
    .actions {
      margin-top: 22px;
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }
    button, .link-button {
      background: var(--primary);
      color: white;
      border: none;
      border-radius: 999px;
      padding: 12px 20px;
      font-size: 1rem;
      cursor: pointer;
      text-decoration: none;
      display: inline-block;
    }
    .secondary {
      background: var(--secondary);
    }
    ul {
      margin: 10px 0 0 18px;
    }
    .mini-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 14px;
      margin-top: 18px;
    }
    .mini-card {
      background: #f7fbfc;
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 16px;
    }
    .mini-card strong {
      display: block;
      margin-bottom: 8px;
      color: var(--primary);
    }
    .hero-layout {
      display: grid;
      grid-template-columns: 1.3fr 0.9fr;
      gap: 20px;
      align-items: start;
    }
    .hero-side {
      background: linear-gradient(180deg, #0d6e8a, #154b67);
      color: white;
      border-radius: 22px;
      padding: 22px;
    }
    .hero-side h3 {
      margin-top: 0;
      font-size: 1.2rem;
    }
    .hero-side ul {
      margin-left: 18px;
    }
    @media (max-width: 800px) {
      .hero-layout {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <div class="hero-layout">
        <div>
          <div class="eyebrow">Insurance Operations Demo</div>
          <h1>CostPilot AI Prototype</h1>
          <p>Cost intelligence and action dashboard for enterprise and insurance-style operations.</p>
          <div class="actions">
            <a class="link-button secondary" href="/analyze-default">Run Sample Analysis</a>
          </div>
          <div class="mini-grid">
            <div class="mini-card">
              <strong>Claims Operations Lens</strong>
              Use SLA risk tracking and workflow escalation patterns similar to claims queues.
            </div>
            <div class="mini-card">
              <strong>Finance Control Lens</strong>
              Detect duplicate payment and rate mismatch risks before money leaks.
            </div>
            <div class="mini-card">
              <strong>BA Lens</strong>
              Show business rules, approvals, audit trail, and measurable impact.
            </div>
          </div>
        </div>
        <div class="hero-side">
          <h3>What This Demo Shows</h3>
          <ul>
            <li>Upload CSV files and run analysis</li>
            <li>View savings summary and priority findings</li>
            <li>See simple charts and action recommendations</li>
            <li>Present a realistic insurance-operations use case</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="panel">
      <div class="eyebrow">Step 1</div>
      <h2>Upload Your Own CSV Files</h2>
      <p>Use your own sample datasets or keep using the built-in demo data. This flow is designed to feel like a simple business application rather than a developer tool.</p>
      <form action="/analyze-upload" method="post" enctype="multipart/form-data">
        <div class="grid">
          <div>
            <label for="procurement">Procurement Spend CSV</label>
            <input type="file" id="procurement" name="procurement">
          </div>
          <div>
            <label for="licenses">Resource Utilization CSV</label>
            <input type="file" id="licenses" name="licenses">
          </div>
          <div>
            <label for="sla">SLA Operations CSV</label>
            <input type="file" id="sla" name="sla">
          </div>
        </div>
        <div class="actions">
          <button type="submit">Run Analysis</button>
        </div>
      </form>
    </div>

    <div class="panel">
      <div class="eyebrow">Step 2</div>
      <h2>Expected CSV Structure</h2>
      <ul>
        <li>Procurement: vendor, invoice_id, invoice_amount, invoice_month, current_rate, benchmark_rate, monthly_units</li>
        <li>Licenses: tool_name, licenses_purchased, licenses_active, monthly_cost_per_license</li>
        <li>SLA: process_name, tickets_at_risk, risk_score, penalty_if_breached</li>
      </ul>
    </div>
  </div>
</body>
</html>"""


def ai_explanation(case: AgentCase) -> str:
    finding = case.finding
    business_context = {
        "Procurement": "It points to avoidable spend risk in a finance-controlled process.",
        "Vendor Rate": "It suggests a recurring pricing issue that can continue to affect monthly cost.",
        "Software Usage": "It shows that business value is lower than the cost currently being paid.",
        "SLA Risk": "It indicates a likely service and penalty event if operations do not intervene in time.",
    }.get(finding.category, "It indicates a meaningful cost and control issue.")

    approval_note = (
        "Because this case is not fully low-risk, the workflow should pause for approval before execution."
        if case.approval_required
        else "Because this case is high-confidence, it can move directly into an approval-ready action queue."
    )

    return (
        f"The business risk in this case is clear. "
        f"The issue identified is: {finding.issue} "
        f"{business_context} "
        f"The estimated monthly impact is INR {finding.estimated_savings:,.0f}. "
        f"My recommended next step is: {finding.action} "
        f"{approval_note}"
    )


def ai_prestart_message(case: AgentCase) -> str:
    return (
        f"This case is ready for review."
    )


def ai_in_progress_message(case: AgentCase) -> str:
    return (
        f"The agents are reviewing this case now and passing information from detection to decision."
    )


def ai_approved_message(case: AgentCase) -> str:
    return (
        "The recommendation has been approved. The case can now move into execution, and the business can act on the identified savings opportunity."
    )


def ai_rejected_message(case: AgentCase) -> str:
    return (
        "The recommendation has been rejected, so no automatic action will be taken. This case should now move to manual business review for further investigation or a revised decision."
    )


def ai_waiting_approval_message(case: AgentCase) -> str:
    return (
        "The agents have completed their review. This case is now waiting for manager approval before the action can move forward."
    )


def render_results_page(findings: list[Finding], source_label: str) -> str:
    total = sum(item.estimated_savings for item in findings)
    agent_cases = build_agent_cases(findings)
    savings: dict[str, float] = {}
    for finding in findings:
        savings[finding.category] = savings.get(finding.category, 0.0) + finding.estimated_savings

    max_value = max(savings.values()) if savings else 1.0
    chart_rows = "".join(
        f"""
        <div class="bar-row">
          <div class="bar-label">{category}</div>
          <div class="bar-track"><div class="bar-fill" style="width:{(value / max_value) * 100:.1f}%"></div></div>
          <div class="bar-value">INR {value:,.0f}</div>
        </div>
        """
        for category, value in savings.items()
    )

    agent_cards_html = """
        <div class="agent-card"><strong>Monitoring Agent</strong><span>Finds a new issue</span></div>
        <div class="agent-card"><strong>Impact Agent</strong><span>Calculates business impact</span></div>
        <div class="agent-card"><strong>Decision Agent</strong><span>Chooses the next step</span></div>
        <div class="agent-card"><strong>Approval Agent</strong><span>Checks if approval is needed</span></div>
        <div class="agent-card"><strong>Action Agent</strong><span>Prepares execution</span></div>
        <div class="agent-card"><strong>Audit Agent</strong><span>Logs the full flow</span></div>
    """

    case_selector_html = "".join(
        f"""
        <button class="case-tab {'active' if index == 1 else ''}" id="tab-{index}" onclick="showCase({index})">
          <span class="tab-number">Case {index}</span>
          <span class="tab-title">{case.finding.title}</span>
          <span class="tab-save">INR {case.finding.estimated_savings:,.0f}</span>
        </button>
        """
        for index, case in enumerate(agent_cases, start=1)
    )

    case_panels_html = "".join(render_case_panel(index, case) for index, case in enumerate(agent_cases, start=1))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CostPilot AI Results</title>
  <style>
    :root {{
      --bg: #eef5f7;
      --panel: rgba(255,255,255,0.94);
      --ink: #17323b;
      --muted: #5c7279;
      --primary: #0d6e8a;
      --secondary: #1b8f6e;
      --accent: #d97706;
      --line: #cadee4;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      background: linear-gradient(135deg, #eef5f7 0%, #d8e8ee 100%);
      color: var(--ink);
    }}
    .wrap {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 28px 20px 56px;
    }}
    .hero, .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 20px;
      padding: 24px;
      box-shadow: 0 14px 28px rgba(18, 43, 53, 0.07);
      margin-bottom: 20px;
      backdrop-filter: blur(10px);
    }}
    .eyebrow {{
      display: inline-block;
      margin-bottom: 10px;
      padding: 7px 12px;
      border-radius: 999px;
      background: #e5f2f6;
      color: var(--primary);
      font-weight: bold;
      font-size: 0.88rem;
    }}
    h1 {{
      margin: 0 0 10px;
      font-size: 2.4rem;
    }}
    .sub {{
      color: var(--muted);
      line-height: 1.6;
      margin-bottom: 16px;
    }}
    .agent-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 12px;
    }}
    .agent-card {{
      background: #f8fcfd;
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 14px;
      box-shadow: 0 6px 16px rgba(18, 43, 53, 0.04);
      text-align: center;
    }}
    .agent-card strong {{
      display: block;
      margin-bottom: 6px;
      color: var(--primary);
      font-size: 0.95rem;
    }}
    .agent-card span {{
      color: var(--muted);
      line-height: 1.4;
      font-size: 0.88rem;
    }}
    .top-grid {{
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 18px;
      align-items: start;
    }}
    .impact-card {{
      background: linear-gradient(180deg, #0d6e8a, #17485d);
      color: white;
      border-radius: 18px;
      padding: 22px;
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.15);
    }}
    .impact-card .big {{
      font-size: 2.2rem;
      font-weight: bold;
      margin-top: 10px;
    }}
    .summary-card {{
      background: #f7fbfc;
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 18px;
      box-shadow: 0 6px 16px rgba(18, 43, 53, 0.04);
      margin-bottom: 12px;
    }}
    .summary-label {{
      color: var(--muted);
      margin-bottom: 8px;
    }}
    .summary-value {{
      font-size: 1.5rem;
      font-weight: bold;
      color: var(--secondary);
    }}
    .simple-grid {{
      display: grid;
      grid-template-columns: 0.8fr 1.2fr;
      gap: 20px;
    }}
    .case-tabs {{
      display: grid;
      gap: 10px;
    }}
    .case-tab {{
      border: 1px solid var(--line);
      background: #f8fcfd;
      border-radius: 14px;
      padding: 14px;
      text-align: left;
      cursor: pointer;
      display: block;
    }}
    .case-tab.active {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(13, 110, 138, 0.08);
      background: #ffffff;
    }}
    .tab-number {{
      display: block;
      font-size: 0.8rem;
      color: var(--muted);
      margin-bottom: 4px;
    }}
    .tab-title {{
      display: block;
      font-weight: bold;
      color: var(--ink);
      line-height: 1.4;
    }}
    .tab-save {{
      display: block;
      margin-top: 6px;
      color: var(--secondary);
      font-weight: bold;
    }}
    .bar-row {{
      display: grid;
      grid-template-columns: 140px 1fr 120px;
      align-items: center;
      gap: 12px;
      margin: 12px 0;
    }}
    .bar-label {{
      font-weight: bold;
    }}
    .bar-track {{
      height: 14px;
      background: #e5eef1;
      border-radius: 999px;
      overflow: hidden;
    }}
    .bar-fill {{
      height: 100%;
      background: linear-gradient(90deg, var(--primary), var(--secondary));
      border-radius: 999px;
    }}
    .bar-value {{
      text-align: right;
      color: var(--muted);
      font-weight: bold;
    }}
    .case-panel {{
      display: none;
      background: #fcfefe;
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 18px;
      box-shadow: 0 8px 18px rgba(18, 43, 53, 0.05);
    }}
    .case-panel.active {{
      display: block;
    }}
    .case-panel h3 {{
      margin: 0 0 10px;
    }}
    .case-meta {{
      color: var(--muted);
      margin-bottom: 14px;
      line-height: 1.5;
    }}
    .plain-box {{
      background: #f8fcfd;
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 14px;
      line-height: 1.6;
      margin-bottom: 14px;
    }}
    .step {{
      display: grid;
      grid-template-columns: 160px 110px 1fr;
      gap: 12px;
      align-items: start;
      padding: 12px 0;
      border-top: 1px solid #e8f0f3;
      opacity: 0.35;
      transition: opacity 0.35s ease, transform 0.35s ease;
      transform: translateY(4px);
    }}
    .step:first-of-type {{
      border-top: none;
    }}
    .step.active {{
      opacity: 1;
      transform: translateY(0);
    }}
    .step-agent {{
      font-weight: bold;
      color: var(--primary);
    }}
    .step-status {{
      display: inline-block;
      padding: 5px 9px;
      border-radius: 999px;
      background: #eaf5e8;
      color: #2d6f3d;
      font-size: 0.85rem;
      font-weight: bold;
      text-align: center;
    }}
    .step-status.waiting {{
      background: #fff2df;
      color: #9a5c00;
    }}
    .step-status.prepared {{
      background: #e5f2f6;
      color: #0d6e8a;
    }}
    .step-status.logged {{
      background: #efe9ff;
      color: #6846b7;
    }}
    .case-controls {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin: 10px 0 14px;
    }}
    button.workflow-btn {{
      border: none;
      border-radius: 999px;
      padding: 10px 14px;
      font-size: 0.95rem;
      cursor: pointer;
      color: white;
      background: var(--primary);
    }}
    button.workflow-btn.secondary {{
      background: var(--secondary);
    }}
    button.workflow-btn.warn {{
      background: var(--accent);
    }}
    .approval-box {{
      margin-top: 10px;
      padding: 12px;
      border-radius: 14px;
      background: #fff7eb;
      border: 1px solid #f2d4a7;
      color: #8a5a00;
    }}
    .summary-box {{
      margin-top: 12px;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: #f8fcfd;
      overflow: hidden;
      box-shadow: 0 6px 16px rgba(18, 43, 53, 0.04);
    }}
    .summary-head {{
      background: #eef6f8;
      color: var(--primary);
      font-weight: bold;
      padding: 10px 14px;
      border-bottom: 1px solid var(--line);
    }}
    .summary-body {{
      padding: 12px 14px;
      line-height: 1.6;
      opacity: 1;
      transition: opacity 0.35s ease;
      font-size: 0.98rem;
    }}
    .summary-body.fade {{
      opacity: 0.35;
    }}
    .thinking {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: var(--primary);
      font-weight: bold;
    }}
    .thinking-dots {{
      display: inline-flex;
      gap: 4px;
    }}
    .thinking-dots span {{
      width: 6px;
      height: 6px;
      border-radius: 999px;
      background: var(--primary);
      animation: blink 1.2s infinite ease-in-out;
    }}
    .thinking-dots span:nth-child(2) {{
      animation-delay: 0.15s;
    }}
    .thinking-dots span:nth-child(3) {{
      animation-delay: 0.3s;
    }}
    @keyframes blink {{
      0%, 80%, 100% {{ opacity: 0.25; transform: scale(0.9); }}
      40% {{ opacity: 1; transform: scale(1); }}
    }}
    .approval-actions.hidden,
    .summary-box.hidden,
    .approval-box.hidden {{
      display: none;
    }}
    .hidden {{
      display: none;
    }}
    .pill {{
      display: inline-block;
      padding: 6px 10px;
      border-radius: 999px;
      background: #fff2df;
      color: #9a5c00;
      font-size: 0.85rem;
      font-weight: bold;
    }}
    .actions {{
      display: flex;
      gap: 12px;
      margin-top: 18px;
      flex-wrap: wrap;
    }}
    a.button {{
      display: inline-block;
      text-decoration: none;
      background: var(--primary);
      color: white;
      padding: 11px 18px;
      border-radius: 999px;
    }}
    a.secondary {{
      background: var(--secondary);
    }}
    a.ghost {{
      background: #eef7f9;
      color: var(--primary);
      border: 1px solid var(--line);
    }}
    .footer-note {{
      margin-top: 16px;
      color: var(--muted);
      line-height: 1.5;
    }}
    @media (max-width: 900px) {{
      .top-grid, .simple-grid {{
        grid-template-columns: 1fr;
      }}
      .bar-row {{
        grid-template-columns: 1fr;
      }}
      .step {{
        grid-template-columns: 1fr;
      }}
      .bar-value {{
        text-align: left;
      }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <div class="eyebrow">Results</div>
      <h1>Simple Multi-Agent Cost Control Demo</h1>
      <div class="sub">A simple view of how agents move a case from detection to action.</div>
      <div class="top-grid">
        <div class="impact-card">
          <div>Estimated Monthly Savings</div>
          <div class="big">INR {total:,.0f}</div>
          <div style="margin-top:8px;">Data source: {source_label}</div>
        </div>
        <div>
          <div class="summary-card">
            <div class="summary-label">Total Cases</div>
            <div class="summary-value">{len(findings)}</div>
          </div>
          <div class="summary-card">
            <div class="summary-label">Agent Flow</div>
            <div class="summary-value">Connected</div>
          </div>
          <div class="summary-card">
            <div class="summary-label">Approval Model</div>
            <div class="summary-value">Controlled</div>
          </div>
        </div>
      </div>
      <div class="actions">
        <a class="button" href="/">Back to Upload Form</a>
        <a class="button secondary" href="/analyze-default">Run Sample Again</a>
        <a class="button ghost" href="/download/report.md">Download Report</a>
        <a class="button ghost" href="/download/dashboard.html">Download Dashboard</a>
      </div>
    </div>

    <div class="panel">
      <div class="eyebrow">Agents</div>
      <h2>Agent Roles</h2>
      <div class="agent-grid">
        {agent_cards_html}
      </div>
    </div>

    <div class="panel">
      <div class="eyebrow">Impact</div>
      <h2>Savings by Category</h2>
      {chart_rows}
    </div>

    <div class="panel">
      <div class="eyebrow">Cases</div>
      <h2>Select a Case</h2>
      <div class="simple-grid">
        <div>
          <div class="case-tabs">
            {case_selector_html}
          </div>
        </div>
        <div>
          {case_panels_html}
        </div>
      </div>
    </div>
  </div>
  <script>
    function setSummaryState(caseId, message) {{
      const summaryBox = document.getElementById(`summary-box-${{caseId}}`);
      const summaryBody = document.getElementById(`summary-body-${{caseId}}`);
      if (!summaryBox || !summaryBody) return;

      summaryBox.classList.remove('hidden');
      summaryBody.classList.add('fade');

      setTimeout(() => {{
        summaryBody.innerHTML = message;
        summaryBody.classList.remove('fade');
      }}, 100);
    }}

    function showCase(caseId) {{
      document.querySelectorAll('.case-tab').forEach(tab => tab.classList.remove('active'));
      document.querySelectorAll('.case-panel').forEach(panel => panel.classList.remove('active'));
      document.getElementById(`tab-${{caseId}}`).classList.add('active');
      document.getElementById(`case-panel-${{caseId}}`).classList.add('active');
    }}

    function startWorkflow(caseId, needsApproval) {{
      const steps = document.querySelectorAll(`#case-${{caseId}} .step`);
      const approvalActions = document.getElementById(`approval-actions-${{caseId}}`);
      const approvalBox = document.getElementById(`approval-box-${{caseId}}`);
      const summaryBox = document.getElementById(`summary-box-${{caseId}}`);
      const summaryBody = document.getElementById(`summary-body-${{caseId}}`);
      steps.forEach(step => step.classList.remove('active'));
      if (approvalActions) approvalActions.classList.add('hidden');
      if (approvalBox) approvalBox.classList.add('hidden');
      if (summaryBox) summaryBox.classList.add('hidden');
      steps.forEach((step, index) => {{
        setTimeout(() => {{
          step.classList.add('active');
          if (needsApproval && index === 3 && approvalActions) {{
            approvalActions.classList.remove('hidden');
            if (summaryBody) {{
              const waitingMessage = summaryBody.getAttribute('data-waiting');
              if (waitingMessage) setSummaryState(caseId, waitingMessage);
            }}
          }}
          if (!needsApproval && index === steps.length - 1 && summaryBox) {{
            setTimeout(() => {{
              if (summaryBody) {{
                const finalMessage = summaryBody.getAttribute('data-default');
                if (finalMessage) setSummaryState(caseId, finalMessage);
              }}
            }}, 100);
          }}
        }}, index * 150);
      }});
    }}

    function setApproval(caseId, outcome) {{
      const approvalBox = document.getElementById(`approval-box-${{caseId}}`);
      const approvalStatus = document.getElementById(`approval-agent-status-${{caseId}}`);
      const approvalResponse = document.getElementById(`approval-agent-response-${{caseId}}`);
      const actionStatus = document.getElementById(`action-agent-status-${{caseId}}`);
      const actionResponse = document.getElementById(`action-agent-response-${{caseId}}`);
      const summaryBody = document.getElementById(`summary-body-${{caseId}}`);
      if (!approvalBox || !approvalStatus || !approvalResponse || !actionStatus || !actionResponse) return;
      approvalBox.classList.remove('hidden');

      if (outcome === 'approved') {{
        approvalBox.innerHTML = '<strong>Manager Approval Simulation:</strong> Approved. Workflow proceeds to the Action Agent for execution.';
        approvalStatus.textContent = 'Approved';
        approvalStatus.className = 'step-status prepared';
        approvalResponse.textContent = 'Manager approval received. The case can now move forward.';
        actionStatus.textContent = 'Ready';
        actionStatus.className = 'step-status prepared';
        actionResponse.textContent = 'Action Agent prepared the approved execution step.';
        if (summaryBody) {{
          const approvedMessage = summaryBody.getAttribute('data-approved');
          if (approvedMessage) setSummaryState(caseId, approvedMessage);
        }}
      }} else {{
        approvalBox.innerHTML = '<strong>Manager Approval Simulation:</strong> Rejected. Workflow is returned for manual business review.';
        approvalStatus.textContent = 'Rejected';
        approvalStatus.className = 'step-status waiting';
        approvalResponse.textContent = 'Manager rejected the recommendation. The case returns for manual review.';
        actionStatus.textContent = 'Paused';
        actionStatus.className = 'step-status waiting';
        actionResponse.textContent = 'Execution paused because approval was not granted.';
        if (summaryBody) {{
          const rejectedMessage = summaryBody.getAttribute('data-rejected');
          if (rejectedMessage) setSummaryState(caseId, rejectedMessage);
        }}
      }}
    }}
  </script>
</body>
</html>"""


def render_case_panel(index: int, case: AgentCase) -> str:
    step_blocks = []
    for step in case.steps:
        step_slug = step.agent.lower().replace(" ", "-")
        step_blocks.append(
            f"""
            <div class="step">
              <div class="step-agent">{step.agent}</div>
              <div class="step-status {status_class(step.status)}" id="{step_slug}-status-{index}">{step.status}</div>
              <div id="{step_slug}-response-{index}">{step.response}</div>
            </div>
            """
        )
    steps_html = "".join(step_blocks)

    approval_controls = ""
    approval_box = ""
    if case.approval_required:
        approval_controls = f"""
        <div class="approval-actions hidden" id="approval-actions-{index}">
          <button class="workflow-btn secondary" onclick="setApproval({index}, 'approved')">Approve Action</button>
          <button class="workflow-btn warn" onclick="setApproval({index}, 'rejected')">Reject Action</button>
        </div>
        """
        approval_box = f"""
        <div class="approval-box hidden" id="approval-box-{index}">
          <strong>Manager Approval Simulation:</strong> Not yet selected.
        </div>
        """

    return f"""
    <div class="case-panel {'active' if index == 1 else ''}" id="case-panel-{index}">
      <div class="timeline-case" id="case-{index}">
      <h3>Case {index}: {case.finding.title}</h3>
      <div class="case-meta">
        Category: {case.finding.category} | Estimated Monthly Savings: INR {case.finding.estimated_savings:,.0f} | Approval Required: {"Yes" if case.approval_required else "No"}
      </div>
      <div class="case-controls">
        <button class="workflow-btn" onclick="startWorkflow({index}, {'true' if case.approval_required else 'false'})">Run Case</button>
        {approval_controls}
      </div>
      {steps_html}
      {approval_box}
      <div class="summary-box hidden" id="summary-box-{index}">
        <div class="summary-head">Case Summary</div>
        <div
          class="summary-body"
          id="summary-body-{index}"
          data-default="{ai_explanation(case)}"
          data-in-progress="{ai_in_progress_message(case)}"
          data-waiting="{ai_waiting_approval_message(case)}"
          data-approved="{ai_approved_message(case)}"
          data-rejected="{ai_rejected_message(case)}"
        >{ai_prestart_message(case)}</div>
      </div>
      </div>
    </div>
    """


def status_class(status: str) -> str:
    lowered = status.lower()
    if "waiting" in lowered:
        return "waiting"
    if "prepared" in lowered or "auto-qualified" in lowered:
        return "prepared"
    if "logged" in lowered:
        return "logged"
    return ""


class CostPilotHandler(BaseHTTPRequestHandler):
    def _send_html(self, content: str, status: int = 200) -> None:
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_html(landing_page())
            return

        if parsed.path == "/analyze-default":
            procurement_rows, license_rows, sla_rows = load_default_rows()
            findings = analyze_datasets(procurement_rows, license_rows, sla_rows)
            html_page = render_results_page(findings, "Built-in sample data")
            LAST_RESULT["html"] = html_page
            LAST_RESULT["report"] = build_report(findings)
            self._send_html(html_page)
            return

        if parsed.path == "/download/report.md":
            content = LAST_RESULT.get("report", "Run an analysis first to generate the report.")
            self._send_bytes(content.encode("utf-8"), "text/markdown; charset=utf-8", "costpilot_report.md")
            return

        if parsed.path == "/download/dashboard.html":
            content = LAST_RESULT.get("html", "<html><body><p>Run an analysis first to generate the dashboard.</p></body></html>")
            self._send_bytes(content.encode("utf-8"), "text/html; charset=utf-8", "costpilot_dashboard.html")
            return

        self._send_html("<h1>Page not found</h1>", status=404)

    def do_POST(self) -> None:
        if self.path != "/analyze-upload":
            self._send_html("<h1>Page not found</h1>", status=404)
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers.get("Content-Type", ""),
            },
        )

        try:
            procurement_text = form["procurement"].file.read().decode("utf-8-sig")
            licenses_text = form["licenses"].file.read().decode("utf-8-sig")
            sla_text = form["sla"].file.read().decode("utf-8-sig")

            findings = analyze_datasets(
                read_csv_text(procurement_text),
                read_csv_text(licenses_text),
                read_csv_text(sla_text),
            )
            html_page = render_results_page(findings, "Uploaded CSV files")
            LAST_RESULT["html"] = html_page
            LAST_RESULT["report"] = build_report(findings)
            self._send_html(html_page)
        except Exception as error:
            self._send_html(
                f"<h1>Upload Error</h1><p>Please upload all 3 CSV files in the expected format.</p><p>{error}</p>",
                status=400,
            )

    def _send_bytes(self, body: bytes, content_type: str, filename: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    server = HTTPServer((HOST, PORT), CostPilotHandler)
    print(f"CostPilot AI web app running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
