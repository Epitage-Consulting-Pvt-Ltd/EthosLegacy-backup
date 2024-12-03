from time import sleep
import threading
from .fps_main import Fingerprint
# from env_config import EnvConfig

class FingerprintVerifier:
    def _init_(self):
        self.fps = Fingerprint('/dev/ttyUSB0', 115200)
        self.thread = None

    def verify_fingerprint(self):
        try:
            # with self.fingerprint as fp:
            if self.fps.init():
                result = self.fps.identify()
                if result is not None:
                    print("Verify Fingerprint: %s" % str(result))
                else:
                    print("Fingerprint identification failed.")
            sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}")
        # finally:
        #     self.fingerprint.close_serial()

    def start_fps_thread(self):
        self.thread = threading.Thread(target=self.verify_fingerprint)
        self.thread.start()

    def wait_for_fps_thread(self):
        if self.thread:
            self.thread.join()

    def cleanup(self):
        self.fps.close_serial()