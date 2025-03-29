from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="AI Platform")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Import and include routes
from app.api import routes as api_routes
app.include_router(api_routes.router, prefix="/api")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "AI Platform"})

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
