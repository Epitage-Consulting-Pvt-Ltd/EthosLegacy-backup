# fps_enroll.py
from time import sleep
from fps_main import Fingerprint
import threading
from infrastructure.env_config import EnvConfig


class FingerprintEnrollmentThread(threading.Thread):
    def __init__(self, event):
        super().__init__()
        self.config = EnvConfig()
        self.event = event

    def run(self):
        FingerprintEnrollmentThread  # Signal that the thread has finished


def start_enrollment_thread():
    stop_event = threading.Event()
    enrollment_thread = FingerprintEnrollmentThread(stop_event)
    enrollment_thread.start()
    return enrollment_thread, stop_event


def close_enrollment_thread(thread, event):
    event.wait()  # Wait for the thread to finish (optional)
    thread.join()

# Example usage:
# enrollment_thread, stop_event = start_enrollment_thread()
# Close the thread
# close_enrollment_thread(enrollment_thread, stop_event)
