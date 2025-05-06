from app.signature import get_signature
import requests

# Global context that helps "train" the AI for every prompt
AI_CONTEXT = """
You're writing on behalf of Paul Schneider at Higher Logic. Our platform powers customer communities for major B2B brands. Use the voice of a sharp, confident, friendly BDR — short and helpful.

Here are key facts and benefits you can use:

- Higher Logic powers over 3,000 customer communities.
- King Games saw a 145% increase in posts after switching to us.
- Quicken increased NPS by 10%.
- Reckon saw a 7% boost in SEO traffic from community.
- F-Secure saved 20% in call deflection.
- Anaplan found 95% of customers with a community account increased spending.
- Higher Logic provides expert-led onboarding and migration support.
- We integrate with platforms like SlapFive, Salesforce, Zendesk, and more.
- Customers like Oracle, IBM, TeamViewer, Udemy, Skillsoft, Pokémon, and Smartsheet trust us.
- The platform includes gamification, AI moderation, advocacy tools, and advanced reporting.
- Our CSMs are also community strategists and help guide long-term ROI.
- Mention ROI: reduce churn, drive referrals, improve onboarding, boost self-service.
- CTA: Ask if they have 30 mins to connect and see if we’re a fit.
- Use company names or metrics if similar to the prospect’s industry or role.
- Avoid any mention of 'Vanilla.' Say only 'Higher Logic.'
- Be impactful, interesting and fun in your tone, yet professional
- Keep it under 100 words. Sound helpful, not salesy or AI-written."""

def has_community(website):
    try:
        r = requests.get(website, timeout=5)
        content = r.text.lower()
        keywords = ["community", "/community", "/forums", "join the discussion", "customer portal"]
        return any(kw in content for kw in keywords)
    except Exception:
        return False

def get_prompt(contact, attempt):
    first_name = contact.name.split(' ')[0] if contact.name else "there"
    community_status = "already has a community" if has_community(contact.website) else "might be exploring new ways to build customer connection"
    signature = get_signature()

    prompt = (
        f"{AI_CONTEXT}\n\n"
    	f"You're a BDR writing an email to {first_name}, who is a {contact.title} at {contact.company}, "
    	f"a company that {community_status}. Their company website is {contact.website}. "
    	f"Their focus area is {contact.persona}.\n\n"
    	"Generate a cold outbound email as HTML.\n\n"
    	"Your email should:\n"
   	 "- Begin with the subject line in this exact format: <b>Subject:</b> Boost Engagement at [Company Name]	<br><br>\n"
    	"- Then start the email body with: Hi [First Name],<br><br>\n"
    	"- Use <br> tags for all new lines and paragraph breaks\n"
    	"- Include a value prop and one stat from a similar company\n"
   	"- End with a CTA and Paul’s full HTML signature\n"
    	"- Do NOT merge the subject with the body\n"
    	"- Keep the email professional and under 150 words\n\n"
    	f"Use this signature exactly as-is:\n{signature}"
    )

    return prompt
