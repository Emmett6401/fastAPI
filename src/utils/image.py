def load_image(image_path):
    from PIL import Image
    import numpy as np

    image = Image.open(image_path)
    return np.array(image)

def preprocess_image(image_array, target_size=(640, 640)):
    from cv2 import resize

    return resize(image_array, target_size)