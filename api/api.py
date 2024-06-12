from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from api.routes import read, health
from api.config import Settings, get_settings

#Load setting values
settings: Settings = get_settings()

#Auth
api_key_env_name = "ASSISTANT_API_KEY"
api_key = APIKeyHeader(name="x-api-key", auto_error=False)

async def verify_api_key(api_key_header: str = Security(api_key)):
    if api_key_header != settings.assistant_api_key:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return api_key_header

#Run API
app = FastAPI(dependencies=[Depends(verify_api_key)])

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.assistant_api_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Get router actions
app.include_router(read.router)
app.include_router(health.router)