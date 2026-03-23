from __future__ import annotations

import csv
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


def read_csv(file_path: Path) -> list[dict[str, str]]:
    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


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


def main() -> None:
    procurement_rows = read_csv(DATA_DIR / "procurement_spend.csv")
    license_rows = read_csv(DATA_DIR / "resource_utilization.csv")
    sla_rows = read_csv(DATA_DIR / "sla_operations.csv")

    findings = []
    findings.extend(detect_duplicate_spend(procurement_rows))
    findings.extend(detect_rate_optimization(procurement_rows))
    findings.extend(detect_unused_licenses(license_rows))
    findings.extend(detect_sla_risks(sla_rows))

    findings.sort(key=lambda item: item.estimated_savings, reverse=True)

    report = build_report(findings)
    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = OUTPUT_DIR / "cost_intelligence_report.md"
    report_path.write_text(report, encoding="utf-8")

    print(report)
    print(f"Report also saved to: {report_path}")


if __name__ == "__main__":
    main()
