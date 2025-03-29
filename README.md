# AI Platform

A web-based platform for interacting with AI models, built with FastAPI and Transformers.

## Features

- Web interface for text generation
- API endpoints for integration with other applications
- Extensible architecture for adding new AI models

## Setup

1. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the server:
   ```
   ./run_server.sh
   # OR
   python -m app.main
   ```

4. Access the web interface at http://localhost:8000

## API Usage

### Text Generation

```python
import requests

response = requests.post(
    "http://localhost:8000/api/generate", 
    json={
        "prompt": "Hello, world!",
        "max_length": 100,
        "temperature": 0.7
    }
)
print(response.json())
```

## Development

- Run tests: `pytest`
- Run linting: `flake8 .`

## License

MIT