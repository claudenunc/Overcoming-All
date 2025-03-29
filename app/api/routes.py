from fastapi import APIRouter, HTTPException
from app.models.models import TextGenerationRequest, TextGenerationResponse
from app.utils.model_utils import generate_text

router = APIRouter()

@router.post("/generate", response_model=TextGenerationResponse)
async def generate_text_endpoint(request: TextGenerationRequest):
    """Generate text using the AI model"""
    try:
        # Use the model to generate text
        generated_text = generate_text(
            prompt=request.prompt,
            max_length=request.max_length,
            temperature=request.temperature
        )
        return TextGenerationResponse(generated_text=generated_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
