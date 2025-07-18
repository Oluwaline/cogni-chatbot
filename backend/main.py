from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from urllib.parse import quote
from typing import List, Optional
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

class RecommendationRequest(BaseModel):
    org_type: str
    team_size: str
    team_roles: List[str] = []
    client_volume: str
    services: List[str] = []
    specializations: List[str] = []

@app.post("/getRecommendation")
async def get_recommendation(data: RecommendationRequest):
    try:
        # Validate input
        if not data.org_type or not data.team_size or not data.client_volume:
            raise HTTPException(status_code=422, detail="Missing required fields")
        
        # Determine package and seats (your business logic)
        package, seats = determine_recommendation(
            data.org_type,
            data.team_size,
            data.client_volume,
            data.specializations,
            data.services
        )
        
        # Calculate pricing
        price = calculate_price(package, seats)
        
        # Generate secure Streamlit URL
        streamlit_url = generate_streamlit_url(package, seats)
        
        return {
            "recommended_package": package,
            "recommended_seats": seats,
            "estimated_pricing": f"${price}",
            "key_features": get_features(package),
            "next_steps": streamlit_url,
            "sales_message": generate_sales_message(package, seats, price, data)
        }
        
    except Exception as e:
        logging.error(f"Recommendation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def determine_recommendation(org_type, team_size, client_volume, specializations, services) -> tuple:
    """Your business logic for determining the package"""
    # Base recommendation based on organization type
    if org_type == "Insurance Provider / EAS":
        return "Enterprise Access (Insurance & EAS)", 20
    elif org_type == "Mental Health Practitioner – Private Practice":
        if team_size in ["1 (Solo practice)", "2–5 providers"]:
            return "Fresh Start", 4
        elif team_size == "6–15 providers":
            return "Practice Plus", 8
        else:
            return "Community Access", 16
    elif org_type == "Mental Health or Healthcare Provider – Public System":
        if team_size in ["16–50 providers", "51+ providers"]:
            return "Enterprise Care (Public Health)", 20
        else:
            return "Practice Plus", 6
    elif org_type == "Home Care or Specialized Residential Services":
        return "Community Access", 20
    
    # Adjust based on specializations
    if "Trauma-informed care" in specializations:
        return "Practice Plus", 8
    
    # Adjust based on services
    if "Group therapy or workshops" in services and team_size in ["16–50 providers", "51+ providers"]:
        return "Community Access", 20
    
    # Fallback
    return "Community Access", 10

def calculate_price(package, seats):
    """Pricing model"""
    pricing = {
        "Fresh Start": 49,
        "Practice Plus": 89,
        "Community Access": 49,
        "Enterprise Care (Public Health)": 199,
        "Enterprise Access (Insurance & EAS)": 199
    }
    return seats * pricing.get(package, 49)

def generate_streamlit_url(package, seats):
    """Generate properly encoded Streamlit URL"""
    base_url = "https://cogni-recommendation-chuiv5x8slzxktq3mzbb5p.streamlit.app"
    params = {
        "tier": package,
        "seats": seats,
        "utm_source": "chatbot"
    }
    query = "&".join(f"{k}={quote(str(v))}" for k,v in params.items())
    return f"{base_url}/?{query}"

def get_features(package):
    """Package features"""
    features = {
        "Fresh Start": [
            "Basic self-guided tools",
            "AI self-assessment",
            "1 group session/month",
            "1 report template"
        ],
        "Practice Plus": [
            "Full AI suite",
            "Group modules",
            "2 sessions/month",
            "Custom reports",
            "Provider dashboard"
        ],
        "Community Access": [
            "Multilingual AI tools",
            "Scalable group support",
            "Onboarding support",
            "Usage dashboard",
            "Volume discounts for 500+ users"
        ],
        "Enterprise Care (Public Health)": [
            "Full AI triage",
            "Post-session care",
            "Real-time analytics",
            "API access",
            "Client monitoring & support",
            "Unlimited video, audio, and text-based monitoring tools"
        ],
        "Enterprise Access (Insurance & EAS)": [
            "API integration",
            "Branded self-assessments",
            "Usage analytics",
            "Employer group modules",
            "Outcome dashboards",
            "Unlimited monitoring tools"
        ]
    }
    return features.get(package, [])

def generate_sales_message(package, seats, price, data):
    """Generate the complete sales message"""
    features = "\n".join(f"- {f}" for f in get_features(package))
    
    return f"""
    **Recommended Package:** {package}

    Thank you for your details! Based on your {data.org_type} organization with {data.team_size} team and {data.client_volume} client volume, we recommend:

    **Package:** {package}  
    **Seats:** {seats}  
    **Price:** ${price}  

    **Key Features:**  
    {features}

    [📊 Click here for your detailed report]({generate_streamlit_url(package, seats)})
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=800)