from __future__ import annotations

import csv
import html
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"


@dataclass
class Finding:
    category: str
    title: str
    issue: str
    action: str
    estimated_savings: float
    confidence: str


@dataclass
class AgentStep:
    agent: str
    status: str
    response: str


@dataclass
class AgentCase:
    finding: Finding
    steps: list[AgentStep]
    approval_required: bool
    final_action: str
    audit_note: str
    root_cause: str
    fallback_note: str


def read_csv(file_path: Path) -> list[dict[str, str]]:
    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_csv_text(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(text.splitlines()))


def to_float(value: str) -> float:
    return float(value.strip().replace(",", ""))


def detect_duplicate_spend(rows: list[dict[str, str]]) -> list[Finding]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    findings: list[Finding] = []

    for row in rows:
        key = (
            row["vendor"].strip().lower(),
            row["invoice_amount"].strip(),
            row["invoice_month"].strip(),
        )
        grouped[key].append(row)

    for (vendor, amount, month), matches in grouped.items():
        if len(matches) > 1:
            duplicate_count = len(matches) - 1
            estimated_savings = duplicate_count * to_float(amount)
            findings.append(
                Finding(
                    category="Procurement",
                    title=f"Possible duplicate invoices from {vendor.title()}",
                    issue=f"{len(matches)} invoices with the same amount were found in {month}.",
                    action="Block payment for duplicate entries and send them to finance review.",
                    estimated_savings=estimated_savings,
                    confidence="High",
                )
            )

    return findings


def detect_rate_optimization(rows: list[dict[str, str]]) -> list[Finding]:
    findings: list[Finding] = []
    vendor_rows: dict[str, dict[str, str]] = {}

    for row in rows:
        vendor_rows[row["vendor"].strip().lower()] = row

    for row in vendor_rows.values():
        vendor_rate = to_float(row["current_rate"])
        market_rate = to_float(row["benchmark_rate"])
        monthly_units = to_float(row["monthly_units"])
        gap = vendor_rate - market_rate

        if gap > 0:
            findings.append(
                Finding(
                    category="Vendor Rate",
                    title=f"Vendor rate optimization opportunity for {row['vendor']}",
                    issue=f"Current unit rate is {vendor_rate:.2f}, benchmark is {market_rate:.2f}.",
                    action="Open renegotiation workflow or shift approved volume to a lower-cost vendor.",
                    estimated_savings=gap * monthly_units,
                    confidence="Medium",
                )
            )

    return findings


def detect_unused_licenses(rows: list[dict[str, str]]) -> list[Finding]:
    findings: list[Finding] = []

    for row in rows:
        purchased = int(row["licenses_purchased"])
        active = int(row["licenses_active"])
        monthly_cost = to_float(row["monthly_cost_per_license"])
        unused = max(purchased - active, 0)

        if unused > 0:
            findings.append(
                Finding(
                    category="Software Usage",
                    title=f"Unused licenses in {row['tool_name']}",
                    issue=f"{unused} licenses are inactive out of {purchased} purchased seats.",
                    action="Remove inactive licenses in the next billing cycle after manager approval.",
                    estimated_savings=unused * monthly_cost,
                    confidence="High",
                )
            )

    return findings


def detect_sla_risks(rows: list[dict[str, str]]) -> list[Finding]:
    findings: list[Finding] = []

    for row in rows:
        risk_score = int(row["risk_score"])
        penalty_amount = to_float(row["penalty_if_breached"])
        tickets_at_risk = int(row["tickets_at_risk"])

        if risk_score >= 75:
            preventable_value = penalty_amount * 0.8
            findings.append(
                Finding(
                    category="SLA Risk",
                    title=f"Approaching SLA breach in {row['process_name']}",
                    issue=f"{tickets_at_risk} tickets are at risk and risk score is {risk_score}/100.",
                    action="Auto-escalate to the operations lead and reassign work to the backup queue.",
                    estimated_savings=preventable_value,
                    confidence="Medium",
                )
            )

    return findings


def generate_summary(findings: list[Finding]) -> dict[str, float]:
    summary: dict[str, float] = defaultdict(float)
    for finding in findings:
        summary[finding.category] += finding.estimated_savings
    return dict(summary)


def build_report(findings: list[Finding]) -> str:
    total = sum(item.estimated_savings for item in findings)
    summary = generate_summary(findings)

    lines = [
        "# Enterprise Cost Intelligence Report",
        "",
        "## Executive Summary",
        f"- Total identified monthly savings: INR {total:,.2f}",
        f"- Total findings: {len(findings)}",
        "",
        "## Savings by Category",
    ]

    for category, value in summary.items():
        lines.append(f"- {category}: INR {value:,.2f}")

    lines.extend(["", "## Findings"])

    for index, finding in enumerate(findings, start=1):
        lines.extend(
            [
                f"### {index}. {finding.title}",
                f"- Category: {finding.category}",
                f"- Issue: {finding.issue}",
                f"- Recommended action: {finding.action}",
                f"- Estimated monthly savings: INR {finding.estimated_savings:,.2f}",
                f"- Confidence: {finding.confidence}",
                "",
            ]
        )

    lines.extend(
        [
            "## Autonomous Action Logic",
            "- High confidence findings can create a finance or operations approval task automatically.",
            "- Medium confidence findings should be routed to a manager before any external system update.",
            "- All actions should be logged with timestamp, owner, and expected savings.",
            "",
            "## Demo Note",
            "This starter project uses sample data. In a real enterprise setup, the same logic would connect to ERP, procurement, ticketing, and SaaS admin systems.",
            "",
        ]
    )

    return "\n".join(lines)


def build_html_dashboard(findings: list[Finding]) -> str:
    total = sum(item.estimated_savings for item in findings)
    summary = generate_summary(findings)

    summary_cards = "\n".join(
        f"""
        <div class="card">
          <div class="label">{html.escape(category)}</div>
          <div class="value">INR {value:,.0f}</div>
        </div>
        """
        for category, value in summary.items()
    )

    finding_cards = "\n".join(
        f"""
        <div class="finding">
          <h3>{index}. {html.escape(finding.title)}</h3>
          <p><strong>Category:</strong> {html.escape(finding.category)}</p>
          <p><strong>Issue:</strong> {html.escape(finding.issue)}</p>
          <p><strong>Action:</strong> {html.escape(finding.action)}</p>
          <p><strong>Estimated monthly savings:</strong> INR {finding.estimated_savings:,.0f}</p>
          <p><strong>Confidence:</strong> {html.escape(finding.confidence)}</p>
        </div>
        """
        for index, finding in enumerate(findings, start=1)
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CostPilot AI Dashboard</title>
  <style>
    :root {{
      --bg: #f5f1e8;
      --panel: #fffdf8;
      --ink: #1e1d1a;
      --muted: #5d5a52;
      --accent: #b5542f;
      --accent-2: #1f6f78;
      --line: #e5dac7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      background: linear-gradient(135deg, #f5f1e8 0%, #efe5d2 100%);
      color: var(--ink);
    }}
    .wrap {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }}
    .hero {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 20px;
      padding: 28px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 2.2rem;
    }}
    .sub {{
      color: var(--muted);
      font-size: 1.05rem;
      line-height: 1.5;
      margin-bottom: 18px;
    }}
    .headline {{
      display: inline-block;
      background: #fff0e8;
      color: var(--accent);
      border: 1px solid #f1c7b7;
      padding: 10px 14px;
      border-radius: 999px;
      font-weight: bold;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin: 24px 0 8px;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 18px;
    }}
    .label {{
      color: var(--muted);
      font-size: 0.95rem;
      margin-bottom: 10px;
    }}
    .value {{
      font-size: 1.6rem;
      font-weight: bold;
      color: var(--accent-2);
    }}
    .section-title {{
      margin: 34px 0 14px;
      font-size: 1.4rem;
    }}
    .finding-list {{
      display: grid;
      gap: 16px;
    }}
    .finding {{
      background: rgba(255,255,255,0.8);
      border: 1px solid var(--line);
      border-left: 6px solid var(--accent);
      border-radius: 16px;
      padding: 18px;
    }}
    .finding h3 {{
      margin: 0 0 10px;
      font-size: 1.1rem;
    }}
    .finding p {{
      margin: 7px 0;
      line-height: 1.5;
    }}
    .footer-note {{
      margin-top: 28px;
      color: var(--muted);
      font-size: 0.95rem;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <h1>CostPilot AI</h1>
      <div class="sub">Enterprise Cost Intelligence and Autonomous Action Dashboard</div>
      <div class="headline">Total Monthly Identified Impact: INR {total:,.0f}</div>
      <div class="grid">
        <div class="card">
          <div class="label">Total Findings</div>
          <div class="value">{len(findings)}</div>
        </div>
        {summary_cards}
      </div>
    </div>

    <h2 class="section-title">Priority Findings</h2>
    <div class="finding-list">
      {finding_cards}
    </div>

    <div class="footer-note">
      This prototype uses sample enterprise data. In a production setup, these inputs would come from ERP, procurement, SaaS administration, and operations systems.
    </div>
  </div>
</body>
</html>
"""


def analyze_datasets(
    procurement_rows: list[dict[str, str]],
    license_rows: list[dict[str, str]],
    sla_rows: list[dict[str, str]],
) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(detect_duplicate_spend(procurement_rows))
    findings.extend(detect_rate_optimization(procurement_rows))
    findings.extend(detect_unused_licenses(license_rows))
    findings.extend(detect_sla_risks(sla_rows))
    findings.sort(key=lambda item: item.estimated_savings, reverse=True)
    return findings


def build_agent_case(finding: Finding) -> AgentCase:
    approval_required = finding.confidence != "High"

    monitoring_response = {
        "Procurement": "Detected a procurement pattern that may indicate duplicate or avoidable spend.",
        "Vendor Rate": "Detected a pricing variance between current vendor rate and benchmark rate.",
        "Software Usage": "Detected inactive or underutilized software licenses in current usage data.",
        "SLA Risk": "Detected an operational signal indicating a likely SLA breach and potential penalty exposure.",
    }.get(finding.category, "Detected a cost-related anomaly in enterprise operations data.")

    impact_response = (
        f"Estimated monthly financial impact is INR {finding.estimated_savings:,.0f} based on current data and business rules."
    )

    decision_response = {
        "Procurement": "Recommended next step is to place the payment into review and notify finance for validation.",
        "Vendor Rate": "Recommended next step is to open a vendor renegotiation or controlled vendor-shift workflow.",
        "Software Usage": "Recommended next step is to route inactive licenses for manager approval before removal.",
        "SLA Risk": "Recommended next step is to escalate, reassign workload, and prevent the expected penalty event.",
    }.get(finding.category, finding.action)

    if approval_required:
        approval_response = "This case requires manager or finance approval before the action agent can execute the next step."
        approval_status = "Waiting / Simulated Approval"
        final_action = f"Approved simulation: {finding.action}"
    else:
        approval_response = "This case is classified as high-confidence and can move directly into an approval-ready action queue."
        approval_status = "Auto-Qualified"
        final_action = f"Auto-ready action: {finding.action}"

    action_response = {
        "Procurement": "Created a simulated finance exception case and prepared a payment-hold action.",
        "Vendor Rate": "Created a simulated sourcing task for renegotiation and rate review.",
        "Software Usage": "Created a simulated license cleanup task for the next billing cycle.",
        "SLA Risk": "Created a simulated operations escalation and backup-queue reassignment task.",
    }.get(finding.category, final_action)

    root_cause = {
        "Procurement": "Likely duplicate invoice entry or repeated payment request for the same service period.",
        "Vendor Rate": "Current vendor pricing is above benchmark, suggesting contract drift or missing rate review.",
        "Software Usage": "Licenses were provisioned but a portion of them are inactive, creating avoidable monthly spend.",
        "SLA Risk": "Operational backlog and queue pressure are increasing the chance of missing the SLA window.",
    }.get(finding.category, "Operational data indicates a cost leakage pattern with a likely process-control issue.")

    fallback_note = {
        "Procurement": "If payment hold cannot be applied automatically, escalate to finance operations for manual exception review.",
        "Vendor Rate": "If renegotiation cannot proceed, escalate to sourcing or procurement leadership for contract review.",
        "Software Usage": "If automatic cleanup is blocked, route the case to the application owner for seat validation.",
        "SLA Risk": "If reassignment does not recover the timeline, escalate to the service manager with a recovery plan.",
    }.get(finding.category, "If the action cannot proceed automatically, escalate for manual business review.")

    audit_note = (
        f"Audit trail captured: category={finding.category}, confidence={finding.confidence}, "
        f"estimated_savings=INR {finding.estimated_savings:,.0f}, action='{finding.action}'."
    )

    return AgentCase(
        finding=finding,
        steps=[
            AgentStep(
                agent="Monitoring Agent",
                status="Completed",
                response=monitoring_response,
            ),
            AgentStep(
                agent="Impact Agent",
                status="Completed",
                response=impact_response,
            ),
            AgentStep(
                agent="Decision Agent",
                status="Completed",
                response=decision_response,
            ),
            AgentStep(
                agent="Approval Agent",
                status=approval_status,
                response=approval_response,
            ),
            AgentStep(
                agent="Action Agent",
                status="Prepared",
                response=action_response,
            ),
            AgentStep(
                agent="Audit Agent",
                status="Logged",
                response=audit_note,
            ),
        ],
        approval_required=approval_required,
        final_action=final_action,
        audit_note=audit_note,
        root_cause=root_cause,
        fallback_note=fallback_note,
    )


def build_agent_cases(findings: list[Finding]) -> list[AgentCase]:
    return [build_agent_case(finding) for finding in findings]


def main() -> None:
    procurement_rows = read_csv(DATA_DIR / "procurement_spend.csv")
    license_rows = read_csv(DATA_DIR / "resource_utilization.csv")
    sla_rows = read_csv(DATA_DIR / "sla_operations.csv")

    findings = analyze_datasets(procurement_rows, license_rows, sla_rows)

    report = build_report(findings)
    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = OUTPUT_DIR / "cost_intelligence_report.md"
    dashboard_path = OUTPUT_DIR / "dashboard.html"
    report_path.write_text(report, encoding="utf-8")
    dashboard_path.write_text(build_html_dashboard(findings), encoding="utf-8")

    print(report)
    print(f"Report also saved to: {report_path}")
    print(f"Dashboard also saved to: {dashboard_path}")


if __name__ == "__main__":
    main()
