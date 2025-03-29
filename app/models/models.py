from pydantic import BaseModel, Field

class TextGenerationRequest(BaseModel):
    prompt: str = Field(..., description="The input prompt for text generation")
    max_length: int = Field(100, description="Maximum length of generated text")
    temperature: float = Field(0.7, description="Temperature for sampling")

class TextGenerationResponse(BaseModel):
    generated_text: str = Field(..., description="The generated text")
