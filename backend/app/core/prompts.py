def build_investment_prompt(company: dict, news_headlines: list[str]) -> str:
    headlines_text = "\n".join(f" - {h}" for h in news_headlines[:8])

    return f"""
You are a financial research assisstant. Analyze the following company and recent news,
then give an investment perspective for a retail investor.help

COMPANY PROFILE:
- Name : {company.get('name')}
- Sector: {company.get('sector')}
- Industry: {company.get('industry')}
- Market Cap: ${company.get('market_cap',0)}
- P/E Ratio: {company.get('pe_ratio')}
- Dividend Yield: {company.get('dividend_yield')}
- 52-Week High: {company.get('fifty_two_week_high')}
- 52-Week-Low: {company.get('fifty_two_week_low')}
- Description: {company.get('description',"")[:500]}

RECENT NEWS HEADLINES
{headlines_text}

Based on the above, provide:
1. SUMMARY: A 3-4 sentence investment summary in plain English.
2. PROS: 3 bullet points of investment strengths.
3. CONS: 3 bullet points of investment risks.
4. VERDICT: One of - BUY / HOLD / AVOID / RESEARCH MORE\
5. CONFIDENCE: A number from 0.0 to 1.0 showing how confident you are.

Format your response EXACLTY like this:
SUMMARY: <text>
PROS: <bullet1> | <bullet2> | <bullet3>
CONS: <bullet1> | <bullet2> | <bullet3>
VERDICT: <verdict>
CONFIDENCE: <number>
"""