SAMPLES = [
    {
        "id": "sales-pitch",
        "title": "Enterprise Cloud Migration Pitch",
        "person_company": "Apex Logistics (CTO Sarah Jenkins & VP Ops Dave Miller)",
        "date_time": "Tomorrow, 10:30 AM EST",
        "purpose": "Pitch our automated cloud migration and compliance platform to replace their legacy on-prem warehouse management system.",
        "previous_notes": "Had a 15-minute discovery call last week. Dave was receptive to cutting infrastructure costs by 35%. Sarah was concerned about zero downtime requirements during peak season (November).",
        "additional_info": "Annual budget cycle ends next month. They are also reviewing AWS native solutions. Decision committee includes CFO who wants ROI within 9 months."
    },
    {
        "id": "one-on-one",
        "title": "Q3 Engineering Growth & Performance 1-on-1",
        "person_company": "Alex Rivera (Senior Frontend Engineer)",
        "date_time": "Thursday, 2:00 PM EST",
        "purpose": "Discuss Alex's transition into a Tech Lead role, review feedback on the design system rollout, and calibrate workload.",
        "previous_notes": "In our last 1-on-1, Alex mentioned feeling slightly overwhelmed by context-switching between junior mentorship and high-priority feature sprints.",
        "additional_info": "Alex exceeded expectations on the recent checkout redesign. Expressed strong interest in software architecture and leading team sprint planning."
    },
    {
        "id": "client-kickoff",
        "title": "Phase 2 AI Customer Support Implementation Kickoff",
        "person_company": "Vanguard Financial Services (Head of CX Marcus Vance)",
        "date_time": "Friday, 11:00 AM EST",
        "purpose": "Align on milestones, API security gateways, stakeholder sign-offs, and rollout schedule for the customer-facing AI agent.",
        "previous_notes": "Phase 1 proof of concept succeeded with 92% answer accuracy. Security team requested SOC2 Type II compliance certificate and on-prem PII redaction confirmation.",
        "additional_info": "Marcus is eager to announce the pilot internally at their upcoming executive town hall. Key milestone is sandbox launch in 4 weeks."
    },
    {
        "id": "investor-update",
        "title": "Series A Due Diligence & Metrics Review",
        "person_company": "Horizons Capital (Partner Elena Rostova)",
        "date_time": "Monday, 3:30 PM EST",
        "purpose": "Walk through Q2 cohort retention data, customer acquisition unit economics, and pipeline forecast for the Series A term sheet.",
        "previous_notes": "Partner liked our product demo and 140% Net Revenue Retention (NRR). Asked for deeper cohort breakdown on enterprise vs mid-market accounts.",
        "additional_info": "Elena has led 3 major B2B SaaS investments in our sector. Their fund standard check size is $4M-$6M. Expect rigorous questions on CAC payback."
    }
]

def get_sample_by_id(sample_id):
    for sample in SAMPLES:
        if sample["id"] == sample_id:
            return sample
    return None
