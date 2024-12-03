import logging
from logging.handlers import RotatingFileHandler
import sys
import traceback
from datetime import datetime, timedelta

class LogManager:
    def __init__(self, log_file_path, max_file_size_bytes=1024*1024, backup_count=5):
        self.log_file_path = log_file_path
        self.max_file_size_bytes = max_file_size_bytes
        self.backup_count = backup_count
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger("MyLogger")
        logger.setLevel(logging.DEBUG)

        # Rotate logs based on size, keep backup_count old log files
        handler = RotatingFileHandler(self.log_file_path, maxBytes=self.max_file_size_bytes,
                                      backupCount=self.backup_count)
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger

    def log_message(self, level, message):
        if level == 'debug':
            self.logger.debug(message)
        elif level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'critical':
            self.logger.critical(message)

    def purge_old_logs(self, days_to_keep=7):
        # Purge logs older than the specified number of days
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        with open(self.log_file_path, 'r') as file:
            lines = file.readlines()
        with open(self.log_file_path, 'w') as file:
            for line in lines:
                log_date_str = line.split(' - ')[0]
                log_date = datetime.strptime(log_date_str, '%Y-%m-%d %H:%M:%S,%f')
                if log_date >= cutoff_date:
                    file.write(line)

def global_exception_handler(exc_type, exc_value, exc_traceback):
    # Log the exception globally
    exception_message = f"Exception Type: {exc_type}\nException Value: {exc_value}"
    exception_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    log_file_path = "error.log"
    with open(log_file_path, 'a') as file:
        file.write(f"\n\n{datetime.now()} - Global Exception Handler:\n{exception_message}\n{exception_traceback}")

if __name__ == "__main__":
    # Set up global exception handler
    sys.excepthook = global_exception_handler

    # Initialize LogManager
    log_file_path = "example.log"
    log_manager = LogManager(log_file_path)

    # Example usage
    log_manager.log_message('info', 'This is an informational message.')

    # Simulate an unhandled exception for testing the global exception handler
    raise ValueError("This is a test error.")
