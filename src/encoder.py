import os
import uuid

import cv2
import numpy as np

PATCH_SIZE = 8
IMAGES_DIR = "/tmp/images"


def ensure_images_directory():
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR, mode=0o777)


def get_available_bytes(width, height):
    return (width // PATCH_SIZE) * (height // PATCH_SIZE) * 3 // 8


def encode_image(image_path, input_text):
    ensure_images_directory()
    # Convert input text to bytes
    input_bytes = input_text.encode("utf-8")
    len_input_bytes = len(input_bytes)
    len_bytes = len_input_bytes.to_bytes(4, "big")
    input_bytes = len_bytes + input_bytes

    input_bits = []
    for byte in input_bytes:
        for i in range(8):
            input_bits.append((byte >> (7 - i)) & 1)
    print(f"Input bits: {len(input_bits)}")

    # Read image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to read image from {image_path}")
    image = np.array(image, dtype=np.uint8)

    width = image.shape[1] // PATCH_SIZE
    height = image.shape[0] // PATCH_SIZE

    for i in range(len(input_bits)):
        y_index = i // (width * 3)
        x_index = (i % (width * 3)) // 3
        channel = i % 3
        if input_bits[i] == 1:
            image[
                y_index * PATCH_SIZE : (y_index + 1) * PATCH_SIZE,
                x_index * PATCH_SIZE : (x_index + 1) * PATCH_SIZE,
                channel,
            ] ^= 1

    new_image_path = str(uuid.uuid4()) + ".png"
    full_path = os.path.join(IMAGES_DIR, new_image_path)
    success = cv2.imwrite(full_path, image)
    if not success:
        raise ValueError(f"Failed to save image to {full_path}")
    return new_image_path


def decode_image(original_image_path, encoded_image_path):
    original_image = cv2.imread(original_image_path)
    encoded_image = cv2.imread(encoded_image_path)

    original_image = np.array(original_image, dtype=np.int16)
    encoded_image = np.array(encoded_image, dtype=np.int16)

    width = original_image.shape[1] // PATCH_SIZE
    height = original_image.shape[0] // PATCH_SIZE

    input_bits = []
    for i in range(width * height * 3):
        y_index = i // (width * 3)
        x_index = (i % (width * 3)) // 3
        channel = i % 3
        encoded_patch = encoded_image[
            y_index * PATCH_SIZE : (y_index + 1) * PATCH_SIZE,
            x_index * PATCH_SIZE : (x_index + 1) * PATCH_SIZE,
            channel,
        ]
        original_patch = original_image[
            y_index * PATCH_SIZE : (y_index + 1) * PATCH_SIZE,
            x_index * PATCH_SIZE : (x_index + 1) * PATCH_SIZE,
            channel,
        ]

        diff = np.sum(np.abs(encoded_patch - original_patch))

        if diff > PATCH_SIZE * PATCH_SIZE // 2:
            input_bits.append(1)
        else:
            input_bits.append(0)

    # Convert bits to bytes
    input_bytes = []
    for i in range(len(input_bits) // 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | input_bits[i * 8 + j]
        input_bytes.append(byte)

    # Get the length of the input bytes
    len_bytes = input_bytes[:4]
    len_input_bytes = int.from_bytes(len_bytes, "big")
    input_bytes = input_bytes[4 : len_input_bytes + 4]
    print(f"Length of input bytes: {len_input_bytes}")

    # Convert bytes to text
    input_text = bytes(input_bytes).decode("utf-8")
    return input_text
