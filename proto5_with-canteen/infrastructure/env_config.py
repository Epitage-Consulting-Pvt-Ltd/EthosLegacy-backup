# import os
# from dotenv import load_dotenv


# class EnvConfig:
#     def __init__(self, dotenv_path="../.env"):
#         self.dotenv_path = dotenv_path
#         self.load_env_variables()

#     def load_env_variables(self):
#         if os.path.exists(self.dotenv_path):
#             load_dotenv(self.dotenv_path)
#             print(f"Environment variables loaded from {self.dotenv_path}")
#         else:
#             print(
#                 f"{self.dotenv_path} not found. Make sure to create the file with your configuration.")

#     def set_env_variable(self, name, value):
#         os.environp[name] = value

#     @property
#     def DB_PATH(self):
#         return os.getenv("DB_PATH")

#     @property
#     def PORT_NAME(self):
#         return os.getenv("PORT")

#     @property
#     def BAUD_RATE_NAME(self):
#         return os.getenv("BAUD_RATE")

#     @property
#     def INTERVAL_NAME(self):
#         return os.getenv("INTERVAL")

#     @property
#     def IMAGE_BASE_PATH(self):
#         return os.getenv("IMAGE_BASE_PATH")
import os


class EnvConfig:
    def __init__(self):
        # Hardcoded default values
        self.default_config = {
            "DB_PATH": "infrastructure/database/ethos_firmware.db",
            "PORT": "/dev/ttyUSB0",  # Replace with your actual port name
            "BAUD_RATE": "115200",
            "INTERVAL": "500",
            "IMAGE_BASE_PATH": "assets/"  # Default folder for images
        }

    def set_env_variable(self, name, value):
        os.environ[name] = value

    @property
    def DB_PATH(self):
        return self.default_config.get("DB_PATH")

    @property
    def PORT_NAME(self):
        return self.default_config.get("PORT")

    @property
    def BAUD_RATE_NAME(self):
        return self.default_config.get("BAUD_RATE")

    @property
    def INTERVAL_NAME(self):
        return self.default_config.get("INTERVAL")

    @property
    def IMAGE_BASE_PATH(self):
        return self.default_config.get("IMAGE_BASE_PATH")
