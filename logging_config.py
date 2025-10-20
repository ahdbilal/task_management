"""
Structured logging configuration for Task Management API
Logs to both file and stdout with JSON formatting for easy parsing
"""
import logging
import json
import sys
from datetime import datetime
from pathlib import Path

# Create logs directory
LOGS_DIR = Path("/home/azureuser/staging/logs") if Path("/home/azureuser/staging").exists() else Path("./logs")
LOGS_DIR.mkdir(exist_ok=True)

class JSONFormatter(logging.Formatter):
    """Format logs as JSON for easy parsing by log analytics tools"""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "task_id"):
            log_data["task_id"] = record.task_id
        if hasattr(record, "endpoint"):
            log_data["endpoint"] = record.endpoint
        if hasattr(record, "method"):
            log_data["method"] = record.method
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        
        return json.dumps(log_data)

def setup_logging():
    """Configure logging with JSON formatting"""
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remove default handlers
    root_logger.handlers = []
    
    # File handler (JSON format)
    file_handler = logging.FileHandler(LOGS_DIR / "app.log")
    file_handler.setFormatter(JSONFormatter())
    file_handler.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    
    # Error log file (only errors and critical)
    error_handler = logging.FileHandler(LOGS_DIR / "errors.log")
    error_handler.setFormatter(JSONFormatter())
    error_handler.setLevel(logging.ERROR)
    root_logger.addHandler(error_handler)
    
    # Console handler (human-readable for development)
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    
    return root_logger

def get_logger(name):
    """Get a logger instance"""
    return logging.getLogger(name)

