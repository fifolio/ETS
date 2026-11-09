from app.constants.metrics import READING_WORDS_PER_MINUTE, STORED_DECIMALS


def words_to_minutes(words: int) -> float:
    return round(words / READING_WORDS_PER_MINUTE, STORED_DECIMALS)
