- Test Commands

- **Setup:**  
  For Python: `pip install -r requirements.txt`

- **Linting:**  
  For Python: `flake8 .`  
  For JavaScript (if applicable): `npm run lint`

- **Testing:**  
  Run all tests: `pytest`  
  Run a single test: `pytest path/to/test_file.py::test_function`

## Code Style Guidelines
- **Python:** Use 4 spaces for indentation, PEP8 compliance.
- **JavaScript/TypeScript:** Use 2 spaces for indentation.

- **Dependencies:**
  - FastAPI
  - transformers
  - uvicorn
  - Jinja2

- **Scripts:**  
  - `run_server.sh`: A bash script to start the FastAPI server.
  - `setup_env.sh`: A script to set up environment variables.