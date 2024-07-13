import config
import tiktoken

def count_tokens(rows: list[dict[str]]) -> dict[str, int]:
    """Count the number of tokens in each row."""
    encoder = tiktoken.encoding_for_model(config.COMPLETIONS_MODEL)
    tokens_per_row = []
    for row in rows:
        # whole dict to string including keys and values
        tokens_per_row.append(len(encoder.encode(row)))    
    return {"tokens_per_row": tokens_per_row}

def get_token_length(context: str) -> int:
    """Get the token length of a context."""
    encoder = tiktoken.encoding_for_model(config.COMPLETIONS_MODEL)
    return len(encoder.encode(context))
