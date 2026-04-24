import logging
import os
from datetime import datetime

class Logger:
    """Custom logger for the application"""
    
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.setup_logger()
    
    def setup_logger(self):
        """Setup logger configuration"""
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        handler = logging.FileHandler(f'logs/{datetime.now().strftime("%Y-%m-%d")}.log')
        handler.setFormatter(logging.Formatter(log_format))
        
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def debug(self, message):
        self.logger.debug(message)
