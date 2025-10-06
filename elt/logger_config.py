"""
Logging configuration for ELT pipeline
Provides structured JSON logging with timestamps and context
"""

import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logger(name='elt_pipeline'):
    """
    Configure and return a structured JSON logger
    
    Args:
        name: Logger name (default: elt_pipeline)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    
    # JSON formatter with relevant fields
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        timestamp=True
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger