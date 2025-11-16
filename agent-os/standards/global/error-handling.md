# Error Handling

- Clear, actionable messages (no technical details exposed)
- Fail fast with explicit errors
- Use specific exception types
- Centralize at boundaries (controllers, API layers)
- Graceful degradation for non-critical failures
- Exponential backoff for retries
- Clean up resources in finally blocks
