MIN_TEXT_LENGTH = 100  # below this, the PDF is probably empty or a scanned image
MAX_PAGES = 10  # a CV longer than this is almost certainly the wrong file
MAX_CV_BYTES = 5 * 1024 * 1024  # matches the Appwrite bucket limit
