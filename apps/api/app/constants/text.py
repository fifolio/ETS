import re

# Scripts written without spaces between words: Thai, Japanese kana, and Chinese ideographs.
UNSPACED_SCRIPTS = re.compile(r"[\u0e00-\u0e7f\u3040-\u30ff\u3400-\u9fff]")
