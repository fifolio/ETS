import re

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
INLINE_HEADING = re.compile(r"^\s*(?P<keyword>[^:：]{1,40}?)\s*[:：]")
MAX_HEADING_WORDS = 4
MAX_UNSPACED_LINE_CHARS = 30  # Chinese, Japanese, Thai have no spaces, so limit by length
UNSPACED_HEADING_WINDOW = 12  # for those scripts, the keyword must start near the line start
