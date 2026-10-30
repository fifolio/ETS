import groq
from langchain_core.exceptions import OutputParserException

# Errors worth retrying on another model: API errors (rate limit, model not found,
# server error), connection problems, and output that doesn't match the schema.
FALLBACK_ERRORS = (groq.APIStatusError, groq.APIConnectionError, OutputParserException)
