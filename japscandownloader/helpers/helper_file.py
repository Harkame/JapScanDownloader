import os

def delete_images(path):
    for file in os.listdir(path):
        if file.endswith('.jpg') or file.endswith('.png'):
            os.remove(os.path.join(path, file))
