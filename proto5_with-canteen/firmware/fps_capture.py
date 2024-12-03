# fps_capture_fingerprint.py
from time import sleep
from fps_main import Fingerprint
from env_config import EnvConfig

def capture_fingerprint():
    config = EnvConfig()
    f = Fingerprint(config.PORT, config.BAUD_RATE)
    if f.init():
        print("Capture Fingerprint: %s" % str(f.capture_finger()))
        f.close_serial()

# if __name__ == '__main__':
#     capture_fingerprint()
