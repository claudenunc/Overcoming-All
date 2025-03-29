from transformers import pipeline

# Global variable to hold the model
text_generator = None

def get_text_generator():
    """Get or initialize the text generation model"""
    global text_generator
    
    if text_generator is None:
        # Load a small model for demonstration
        # In production, you would use a more powerful model
        text_generator = pipeline("text-generation", model="distilgpt2")
    
    return text_generator

def generate_text(prompt, max_length=100, temperature=0.7):
    """Generate text using the loaded model"""
    generator = get_text_generator()
    
    # Generate text
    result = generator(
        prompt, 
        max_length=max_length, 
        temperature=temperature,
        num_return_sequences=1
    )
    
    # Extract the generated text
    generated_text = result[0]["generated_text"]
    
    return generated_text