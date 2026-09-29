import json
import re
import requests
from typing import Dict, Any, Optional

def detect_meeting_type(title: str, purpose: str, person_company: str) -> str:
    text = f"{title} {purpose} {person_company}".lower()
    if any(k in text for k in ['1:1', '1-on-1', 'one on one', 'review', 'performance', 'feedback', 'appraisal']):
        return '1on1'
    if any(k in text for k in ['pitch', 'demo', 'sales', 'prospect', 'pricing', 'close', 'deal', 'proposal', 'vendor']):
        return 'sales'
    if any(k in text for k in ['investor', 'fundraise', 'venture', 'vc', 'angel', 'seed', 'series a', 'due diligence']):
        return 'investor'
    if any(k in text for k in ['client', 'customer', 'account', 'kickoff', 'onboarding', 'quarterly', 'qbr', 'renewal']):
        return 'client'
    if any(k in text for k in ['interview', 'candidate', 'hiring', 'talent', 'recruitment']):
        return 'interview'
    if any(k in text for k in ['tech', 'architecture', 'engineering', 'sprint', 'code', 'api', 'system', 'infra']):
        return 'technical'
    if any(k in text for k in ['partner', 'alliance', 'integration', 'collaboration', 'synergy']):
        return 'partnership'
    return 'general'

def build_heuristic_brief(title: str, person_company: str, date_time: str, purpose: str, previous_notes: str, additional_info: str) -> Dict[str, Any]:
    """Generates an intelligent, highly tailored meeting preparation brief without external API dependencies."""
    meeting_type = detect_meeting_type(title, purpose, person_company)
    target_name = person_company.strip() or "the stakeholder"
    meeting_title = title.strip() or "Upcoming Discussion"
    core_purpose = purpose.strip() or f"Align on strategic priorities with {target_name}"

    # Extract highlights from previous notes if present
    prev_notes_list = [p.strip() for p in re.split(r'[\n\.\;]', previous_notes) if len(p.strip()) > 4]
    add_info_list = [a.strip() for a in re.split(r'[\n\.\;]', additional_info) if len(a.strip()) > 4]

    # 1. Meeting Objective
    if meeting_type == 'sales':
        primary_obj = f"Validate {target_name}'s core challenges, present tailored value propositions, and secure consensus on a clear evaluation timeline or pilot."
        success_criteria = [
            f"Mutual understanding of {target_name}'s budget, decision authority, and timeframe (BANT/MEDDIC).",
            "Clear agreement on next milestone (e.g. proof of concept or contract review).",
            "Identified the single biggest blocker to moving forward."
        ]
    elif meeting_type == '1on1':
        primary_obj = f"Conduct an open, constructive conversation with {target_name} regarding progress, roadblocks, professional growth, and actionable support."
        success_criteria = [
            "Honest alignment on workload, wellbeing, and priorities.",
            "Reviewed progress on past action items and resolved bottlenecks.",
            "Documented 2-3 concrete development commitments for the coming weeks."
        ]
    elif meeting_type == 'client':
        primary_obj = f"Strengthen the partnership with {target_name}, review recent milestones, address any operational friction, and align on upcoming goals."
        success_criteria = [
            f"{target_name} feels heard and confident in project momentum.",
            "Open issues or pending deliverables have clear owners and deadlines.",
            "Identified growth or expansion opportunities for the engagement."
        ]
    elif meeting_type == 'investor':
        primary_obj = f"Demonstrate clear market traction, unit economics, and strategic vision to generate conviction and advance to formal due diligence with {target_name}."
        success_criteria = [
            "Conveyed key defensible metrics, team unfair advantage, and market size.",
            "Answered critical unit economics and go-to-market queries confidently.",
            "Established explicit timeline for data room access and follow-up partner meeting."
        ]
    elif meeting_type == 'technical':
        primary_obj = f"Reach technical consensus on architecture, feasibility, trade-offs, and implementation plan with {target_name}."
        success_criteria = [
            "Resolved outstanding technical blockers and agreed on architecture pattern.",
            "Explicit timeline and sprint allocation defined.",
            "Risk mitigations established for performance, security, and edge cases."
        ]
    elif meeting_type == 'partnership':
        primary_obj = f"Explore synergistic opportunities with {target_name}, establish mutual value drivers, and outline a joint integration roadmap."
        success_criteria = [
            "Validated mutual strategic interest and business alignment.",
            "Identified joint pilot or co-marketing opportunity.",
            "Agreed on technical and commercial diligence prerequisites."
        ]
    else:
        primary_obj = f"Achieve clear alignment with {target_name} on '{meeting_title}' and establish concrete next steps."
        success_criteria = [
            f"Addressed core objectives outlined in: '{core_purpose}'.",
            "All participants share a consistent definition of success.",
            "Explicit action items assigned with deadlines and responsible owners."
        ]

    # 2. Person/Company Summary
    company_context = f"{target_name} is a key stakeholder for this interaction. "
    if previous_notes:
        company_context += f"Based on prior discussions: {prev_notes_list[0] if prev_notes_list else previous_notes[:140]}... "
    else:
        company_context += f"This interaction focuses on advancing discussions regarding {meeting_title.lower()}. "

    if additional_info:
        company_context += f"Context highlights: {add_info_list[0] if add_info_list else additional_info[:140]}."
    else:
        company_context += f"Establishing a collaborative, consultative dynamic will yield the highest quality outcome."

    # 3. Key Discussion Points (Prioritized agenda)
    discussion_points = []
    discussion_points.append({
        "topic": "Welcome & Agenda Alignment (5 mins)",
        "details": f"Set positive tone, confirm {target_name}'s target wrap-up time, and validate the agenda priorities."
    })
    
    if prev_notes_list:
        discussion_points.append({
            "topic": "Review Past Action Items & Updates (10 mins)",
            "details": f"Directly address items from previous notes: '{prev_notes_list[0][:80]}'. Clarify what has progressed and what remains open."
        })

    discussion_points.append({
        "topic": f"Core Topic: {core_purpose} (20 mins)",
        "details": f"Deep dive into the primary focus: {core_purpose}. Focus on outcomes, mutual incentives, and practical requirements."
    })

    if add_info_list:
        discussion_points.append({
            "topic": "Strategic Context & Specific Constraints (10 mins)",
            "details": f"Discuss relevant details noted: '{add_info_list[0][:90]}'."
        })
    else:
        discussion_points.append({
            "topic": "Operational Feasibility & Resource Alignment (10 mins)",
            "details": f"Examine bandwidth, budget constraints, technical prerequisites, and key team dependencies."
        })

    discussion_points.append({
        "topic": "Wrap-Up & Immediate Next Steps (5 mins)",
        "details": f"Summarize key takeaways, verify consensus, and lock in specific dates for follow-up deliverables."
    })

    # 4. Important Questions to Ask
    questions = []
    if meeting_type == 'sales':
        questions = [
            f"What does a successful partnership look like for {target_name} over the next 6 to 12 months?",
            "What are the primary metrics or KPIs your leadership team will evaluate this decision on?",
            "Who else on your team needs to participate before we can formalize a decision?",
            "What potential hurdles or security/compliance requirements should we plan for early?"
        ]
    elif meeting_type == '1on1':
        questions = [
            "What project or task has been most energizing for you lately, and what has felt draining?",
            "Are there any blockers, cross-team dependencies, or resource gaps where I can step in to clear the path?",
            "Looking ahead over the next quarter, which skills or leadership areas do you want to intentionally develop?",
            "What can I do differently as a manager to better support your day-to-day productivity?"
        ]
    elif meeting_type == 'client':
        questions = [
            f"How is the current progress meeting your expectations compared to initial goals?",
            "Are there upcoming shifts in your business priorities that we should adapt our roadmap towards?",
            "Where do you see the biggest opportunity for us to deliver higher impact over the coming weeks?",
            "Is there any friction or communication lag that we can optimize immediately?"
        ]
    elif meeting_type == 'investor':
        questions = [
            "How does our model compare to your existing portfolio thesis in this sector?",
            "What are the 2-3 specific metrics you'd need to validate before moving to an investment committee review?",
            "What is your typical due diligence cadence and timeline from here?",
            "Which areas of our go-to-market strategy would you like us to drill deeper into?"
        ]
    else:
        questions = [
            f"From your perspective at {target_name}, what is the critical milestone that must be achieved first?",
            "What constraints or non-negotiables should we keep top-of-mind during execution?",
            "How can we ensure clear accountability and smooth communication across both sides?",
            "What would cause this initiative to be delayed, and how can we mitigate it today?"
        ]

    # Add question derived from previous notes if provided
    if prev_notes_list:
        questions.insert(1, f"Following up on our last note ('{prev_notes_list[0][:60]}...'), what has been the recent evolution on that front?")

    # 5. Suggested Talking Points
    talking_points = []
    talking_points.append(f"State the shared objective early: 'Our goal today is to ensure {target_name} has complete clarity on {meeting_title.lower()} and an actionable path forward.'")
    
    if meeting_type == 'sales':
        talking_points.append(f"Emphasize ROI and time-to-value: Highlight how solving '{core_purpose}' eliminates operational overhead and saves budget.")
        talking_points.append("De-risk the transition: Emphasize dedicated onboarding support, step-by-step rollout, and responsive assistance.")
    elif meeting_type == '1on1':
        talking_points.append("Acknowledge contributions: Begin by recognizing recent milestones and resilience in tackling complex tasks.")
        talking_points.append("Focus on coaching rather than policing: Frame challenges as shared problem-solving opportunities.")
    elif meeting_type == 'client':
        talking_points.append(f"Reaffirm commitment: 'We view {target_name} as a long-term partner and want to ensure every deliverable directly supports your business goals.'")
        talking_points.append("Proactively share roadmap insights: Demonstrate forward-looking vision and proactive improvements.")
    else:
        talking_points.append(f"Focus on practical outcomes: Connect the purpose '{core_purpose}' to tangible, measurable results.")
        talking_points.append("Keep communication open: Encourage direct feedback and validate assumptions before finalizing decisions.")

    if additional_info:
        talking_points.append(f"Reference strategic details: Respectfully weave in: '{additional_info[:120]}'.")

    # 6. Possible Concerns or Objections & Strategic Mitigations
    concerns_objections = []
    if meeting_type == 'sales':
        concerns_objections.append({
            "concern": "Budget constraints or competing Q4/Q1 priorities",
            "mitigation": "Highlight flexible phased rollout or pilot phase; quantify cost of inaction and immediate payback period."
        })
        concerns_objections.append({
            "concern": "Implementation bandwidth and team learning curve",
            "mitigation": "Demonstrate turnkey onboarding, template libraries, and low friction integration requiring minimal IT overhead."
        })
        concerns_objections.append({
            "concern": "Security, privacy, or compliance validation delays",
            "mitigation": "Offer pre-packaged compliance documentation, SOC2/GDPR sheets, and direct architecture walkthrough."
        })
    elif meeting_type == '1on1':
        concerns_objections.append({
            "concern": "Reluctance to share burnout, overload, or team friction",
            "mitigation": "Create a high-trust, non-judgmental space. Ask neutral open-ended questions like 'On a scale of 1-10, where is your mental energy right now?'"
        })
        concerns_objections.append({
            "concern": "Unclear career progression or feeling stagnant",
            "mitigation": "Anchor discussion around tangible development goals, mentorship opportunities, and leadership visibility."
        })
    elif meeting_type == 'client':
        concerns_objections.append({
            "concern": "Delays or misunderstandings on previous deliverables",
            "mitigation": "Own the friction transparently, provide an immediate remediation timeline, and install updated check-in gates."
        })
        concerns_objections.append({
            "concern": "Scope creep or pricing adjustment resistance",
            "mitigation": "Show clear trade-offs between speed, scope, and quality. Provide modular options so the client stays in control."
        })
    else:
        concerns_objections.append({
            "concern": "Lack of clarity on decision-making authority or ownership",
            "mitigation": "Explicitly identify a Single Point of Contact (SPOC) for each workstream and establish weekly asynchronous status reports."
        })
        concerns_objections.append({
            "concern": "Unforeseen technical dependencies or deadline slippage",
            "mitigation": "Build in a 15-20% buffer on milestones and identify alternative contingency pathways."
        })

    # 7. Recommended Next Steps (Action Plan)
    next_steps = [
        {
            "action": f"Send comprehensive follow-up summary email to {target_name}",
            "timing": "Within 2-4 hours post-meeting",
            "owner": "You"
        },
        {
            "action": "Document all agreed decisions and update project tracker / CRM",
            "timing": "Same day",
            "owner": "You"
        },
        {
            "action": "Deliver requested collateral, proposals, or technical documentation",
            "timing": "Within 48 hours",
            "owner": "Team / You"
        },
        {
            "action": f"Calendar next checkpoint / review meeting with {target_name}",
            "timing": "Before meeting concludes",
            "owner": "Both"
        }
    ]

    # Pre-meeting quick prep checklist (value add!)
    checklist = [
        f"Review {target_name}'s recent updates or LinkedIn/website announcements (2 mins)",
        "Have presentation deck or supporting documentation open in clean browser tabs (1 min)",
        "Test microphone, video, and screen sharing setup (1 min)",
        "Keep notepad open to capture exact customer phrasing and commitments (ongoing)"
    ]

    # Suggested Follow-Up Email Draft
    email_draft = f"""Subject: Notes & Next Steps: {meeting_title} - {target_name}

Hi {target_name},

Thank you for your time today discussing {meeting_title.lower()}. It was great connecting with you.

Key Highlights & Decisions:
• {core_purpose}
• [Summarize agreed point 1]
• [Summarize agreed point 2]

Agreed Next Steps:
1. [Action item 1] - Owner: You (Target Date: [Date])
2. [Action item 2] - Owner: {target_name} (Target Date: [Date])

Looking forward to our continued collaboration. Please let me know if I missed anything!

Best regards,
[Your Name]"""

    return {
        "metadata": {
            "title": meeting_title,
            "person_company": target_name,
            "date_time": date_time or "Scheduled time",
            "purpose": core_purpose,
            "meeting_type": meeting_type.title(),
            "generated_by": "Meeting Prep Agent Engine"
        },
        "meeting_objective": {
            "primary": primary_obj,
            "success_criteria": success_criteria
        },
        "person_company_summary": company_context,
        "key_discussion_points": discussion_points,
        "important_questions": questions,
        "suggested_talking_points": talking_points,
        "possible_concerns_objections": concerns_objections,
        "recommended_next_steps": next_steps,
        "pre_meeting_checklist": checklist,
        "follow_up_email_template": email_draft
    }

def generate_ai_brief(title: str, person_company: str, date_time: str, purpose: str, previous_notes: str, additional_info: str, api_key: str) -> Optional[Dict[str, Any]]:
    """Optionally calls Google Gemini API if an API key is provided."""
    if not api_key or not api_key.strip():
        return None

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key.strip()}"
        
        system_instructions = """You are an elite executive meeting preparation strategist.
You produce comprehensive, high-stakes meeting preparation briefs.
You MUST output your response in strict JSON format matching the schema below without any markdown code fences.

JSON Schema:
{
  "metadata": {
    "title": "string",
    "person_company": "string",
    "date_time": "string",
    "purpose": "string",
    "meeting_type": "string",
    "generated_by": "Gemini 1.5 Flash AI"
  },
  "meeting_objective": {
    "primary": "string",
    "success_criteria": ["string", "string", "string"]
  },
  "person_company_summary": "string",
  "key_discussion_points": [
    {"topic": "string", "details": "string"}
  ],
  "important_questions": ["string", "string", "string", "string"],
  "suggested_talking_points": ["string", "string", "string"],
  "possible_concerns_objections": [
    {"concern": "string", "mitigation": "string"}
  ],
  "recommended_next_steps": [
    {"action": "string", "timing": "string", "owner": "string"}
  ],
  "pre_meeting_checklist": ["string", "string"],
  "follow_up_email_template": "string"
}"""

        prompt = f"""Generate a high-impact Meeting Preparation Brief for:
Meeting Title: {title}
Person/Company Name: {person_company}
Meeting Date & Time: {date_time}
Meeting Purpose: {purpose}
Previous Meeting Notes: {previous_notes}
Additional Information: {additional_info}

Ensure every section is insightful, strategic, and directly actionable."""

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": system_instructions + "\n\n" + prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "responseMimeType": "application/json"
            }
        }

        resp = requests.post(url, json=payload, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            raw_text = data['candidates'][0]['content']['parts'][0]['text']
            # Clean possible markdown wrap
            clean_text = re.sub(r'^```json\s*', '', raw_text.strip(), flags=re.MULTILINE)
            clean_text = re.sub(r'```$', '', clean_text.strip())
            parsed = json.loads(clean_text)
            return parsed
    except Exception as e:
        print(f"External API generation error (falling back to heuristic): {e}")
        return None

    return None

def generate_meeting_brief(title: str, person_company: str, date_time: str, purpose: str, previous_notes: str, additional_info: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Generates brief via AI if key provided, otherwise uses intelligent context engine."""
    if api_key and api_key.strip():
        ai_result = generate_ai_brief(title, person_company, date_time, purpose, previous_notes, additional_info, api_key)
        if ai_result:
            return ai_result

    return build_heuristic_brief(title, person_company, date_time, purpose, previous_notes, additional_info)
