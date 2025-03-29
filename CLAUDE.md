# CLAUDE.md - AI Assistant Guidelines

## Build & Test Commands
- Setup: `npm install` or `pip install -r requirements.txt` (add based on project)
- Lint: `npm run lint` or `flake8 .` (add based on project)
- Test all: `npm test` or `pytest` (add based on project)
- Test single: `npm test -- -t "test name"` or `pytest path/to/test.py::test_name`

## Code Style Guidelines
- Formatting: Use consistent indentation (2 spaces JS/TS, 4 spaces Python)
- Imports: Group imports (standard library, third-party, local)
- Types: Use strong typing where available (TypeScript, Python type hints)
- Naming: camelCase for JS/TS, snake_case for Python, PascalCase for classes
- Error handling: Use try/catch or try/except with specific error types
- Documentation: Document functions with parameters, return values, examples
- Comments: Explain "why" not "what" in comments
- Async: Use async/await pattern for asynchronous code
- Testing: Write unit tests for new functionality

Update this file as project conventions evolve.