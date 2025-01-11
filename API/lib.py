from PIL import Image
import numpy as np
import io

WIDTH = 30
HEIGHT = 30
CHANNELS = 3

def process_image(content, model):
    image = Image.open(io.BytesIO(content))
    image = image.resize([WIDTH, HEIGHT])
    image = np.array(image) / 255
    
    pred = np.argmax(
        model.predict(image.reshape(1, WIDTH, HEIGHT, CHANNELS))
    )
    
    return str(pred)
