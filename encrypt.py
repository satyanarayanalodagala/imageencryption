import cv2
import numpy as np

def encrypt_image(input_image_path, output_image_path, key_path):
    image = cv2.imread(input_image_path)
    key = np.random.randint(0, 256, size=image.shape, dtype=np.uint8)
    encrypted_image = cv2.bitwise_xor(image, key)
    cv2.imwrite(output_image_path, encrypted_image)
    np.save(key_path, key)
