import os


def get_absolute_path(image_path):
    current_directory = os.getcwd()
    return os.path.join(current_directory, image_path)
