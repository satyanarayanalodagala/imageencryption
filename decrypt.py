import numpy as np
from PIL import Image

def decrypt_image(input_image_path, key_path, output_image_path):
    # Load the key
    key = np.load(key_path, allow_pickle=True)

    # Open the encrypted image
    encrypted_image = Image.open(input_image_path)
    encrypted_image_array = np.array(encrypted_image)

    # Decrypt the image
    decrypted_image_array = encrypted_image_array ^ key

    # Convert the decrypted array back to an image
    decrypted_image = Image.fromarray(decrypted_image_array)

    # Save the decrypted image
    decrypted_image.save(output_image_path)
