from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from schemas import InputData
from services.prediction import predict_package
from services.pricing import PACKAGE_PRICE_TABLE, SALES_MESSAGES
import traceback
from starlette.responses import FileResponse

app = FastAPI(
    title="Cogni Recommendation API",
    version="1.0.0",
    description="AI-powered mental health package recommender"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Serve static files (HTML/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def serve_chatbot():
    return FileResponse("static/index.html")

@app.post("/api/recommend")
async def get_recommendation(data: InputData):
    try:
        # Validate required fields
        if not all([data.org_type, data.team_size, data.client_volume]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Get prediction
        package, seats = predict_package(
            org_type=data.org_type,
            team_size=data.team_size,
            client_volume=data.client_volume,
            specialization=data.specialization,
            service_model=data.service_model
        )
        
        # Prepare response
        price = PACKAGE_PRICE_TABLE.get((package, seats), seats * 49)
        
        return {
            "package": package,
            "seats": seats,
            "price": price,
            "message": SALES_MESSAGES[package].format(
                seats=seats,
                price=price,
                features="See included features",
                next_steps=f"/details?package={package}"
            )
        }
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))