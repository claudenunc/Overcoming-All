# AI Platform: ARCHITECT

A meta-level intelligent system designed to create, manage, and coordinate specialized AI agents for any project or business need, built with FastAPI and Transformers.

## Features

- Create customized agent teams for specific tasks and projects
- Orchestrate workflows between multiple specialized agents
- Monitor performance and continuously improve agent capabilities
- Web interface for interacting with your AI agent ecosystem
- API endpoints for integration with other applications

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