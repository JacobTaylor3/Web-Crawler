import logging
FILETYPES = [
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".mp3",
    ".mp4",
    ".zip",
    ".rar",
    ".exe",
]

def enableLogging():
    logging.basicConfig(
    filename="logs/app.log",  # File where logs are saved
    level=logging.INFO,  # Minimum log level to capture
    format="%(asctime)s - %(levelname)s - %(funcName)s() - %(message)s",
    datefmt="%b %d %Y %I:%M:%S %p",  # Custom date format: "Jan 09 2025 06:24:00 PM"# Log format
    filemode="w",  # Overwrite the file each time the program runs (use 'a' to append)
)


