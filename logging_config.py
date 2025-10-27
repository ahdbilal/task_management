from pathlib import Path
import logging
import logging.handlers
import sys
from datetime import datetime

# Configure logging directory (use workspace logs)
LOGS_DIR = Path("/home/ahmedbilal/workspace/logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)


# Rest of logging config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.handlers.RotatingFileHandler(
            LOGS_DIR / 'app.log',
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
    ]
)

def setup_logging():
    pass

def get_logger(name):
    return logging.getLogger(name)
