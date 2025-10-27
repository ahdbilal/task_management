from pathlib import Path
import logging
import logging.handlers
import sys
import os
from datetime import datetime

# Determine logs directory based on environment
# In production: /home/ahmedbilal/workspace/logs
# In CI/test: ./logs relative to current directory
def get_logs_dir():
    """Get logs directory, handling different environments gracefully"""
    # Check if we're in CI environment
    if os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS'):
        logs_dir = Path('./logs')
    else:
        # Try production path
        prod_path = Path('/home/ahmedbilal/workspace/logs')
        if prod_path.parent.exists():
            logs_dir = prod_path
        else:
            # Fallback to relative path
            logs_dir = Path('./logs')

    # Create directory if it doesn't exist
    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
    except (PermissionError, OSError) as e:
        # Last resort: use temp directory
        logs_dir = Path('/tmp/logs')
        logs_dir.mkdir(parents=True, exist_ok=True)

    return logs_dir

LOGS_DIR = get_logs_dir()

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

