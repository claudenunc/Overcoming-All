from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="ARCHITECT AI Platform",
    description="A meta-level intelligent system designed to create, manage, and coordinate specialized AI agents",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Import and include routes
from app.api import routes as api_routes
from app.api import architect_routes
app.include_router(api_routes.router, prefix="/api")
app.include_router(architect_routes.router, prefix="/api")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "ARCHITECT AI Platform"})

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
