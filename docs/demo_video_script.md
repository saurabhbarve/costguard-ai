# 3-Minute Demo Walkthrough Script

## Title
CostPilot AI Demo Walkthrough

## Script

Hello everyone.

This is a demo of **CostPilot AI**, our solution for **AI for Enterprise Cost Intelligence and Autonomous Action**.

The idea behind CostPilot AI is simple:
enterprises lose money through small leakages that are usually detected too late.
Examples include duplicate invoices, high vendor rates, unused software licenses, and SLA penalties.

Our system continuously monitors enterprise data, identifies these leakages, estimates financial impact, and initiates the next best action through an approval workflow.

Let me quickly show how the demo works.

First, here are the sample data files.
We are using three business datasets:
- procurement spend data
- resource utilization data
- SLA operations data

These represent the kind of data that would normally come from ERP systems, SaaS admin tools, and ticketing platforms.

Now I will run the solution.

We execute the Python script, which reads the data, detects cost leakage patterns, and generates a business-friendly report.

The system checks for four key scenarios:
- duplicate invoices
- vendor rate optimization opportunities
- unused software licenses
- SLA breach risks

Now we can see the output report.

The report gives us an executive summary first.
In this sample run, CostPilot AI identified total monthly savings of **INR 205,900**.

Below that, it breaks savings down by category.
For example:
- procurement savings from duplicate invoice detection
- operational savings from SLA risk prevention
- software savings from removing unused licenses
- vendor savings from rate optimization

Now let us look at one example.

Here, the system found a possible duplicate invoice from the same vendor with the same amount in the same month.
Instead of only flagging the issue, it recommends the next action:
block payment and send the case to finance review.

Here is another example.
The system identified a support queue that is close to an SLA breach.
It recommends escalating and rerouting work before the financial penalty happens.

This is important because the value of the system is not only detection.
It is also action.

And in a real enterprise environment, these actions would connect to finance approval, operations workflows, email alerts, or collaboration tools like Slack or Teams.

The system also supports governance.
High-confidence cases can trigger automated tasks.
Medium-risk cases can go to managers for approval.
Every action is logged for auditability.

So to summarize:
CostPilot AI helps enterprises detect hidden waste, take action faster, and clearly measure savings.

Instead of waiting for monthly reports, organizations can move to continuous cost intelligence with autonomous action.

Thank you.

## Suggested Recording Flow
1. Show project folder
2. Open data files briefly
3. Run `python3 app/main.py`
4. Show the report output
5. Explain 2 example findings
6. Close with total savings and business value
