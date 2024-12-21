from PIL import Image

def encode_message(image_path, message, output_path):
    """Encodes a secret message into an image."""
    image = Image.open(image_path)
    encoded_image = image.copy()
    width, height = image.size
    message += "<END>"  # Delimiter

    binary_message = ''.join([format(ord(char), '08b') for char in message])  # Convert message to binary
    binary_message_length = len(binary_message)
    pixel_data = list(encoded_image.getdata())

    if binary_message_length > len(pixel_data) * 3:
        raise ValueError("Message is too large to encode in the given image.")

    encoded_pixels = []
    binary_index = 0

    for pixel in pixel_data:
        r, g, b = pixel[:3]  # Get RGB values
        if binary_index < binary_message_length:
            r = (r & ~1) | int(binary_message[binary_index])  # Modify LSB of red
            binary_index += 1
        if binary_index < binary_message_length:
            g = (g & ~1) | int(binary_message[binary_index])  # Modify LSB of green
            binary_index += 1
        if binary_index < binary_message_length:
            b = (b & ~1) | int(binary_message[binary_index])  # Modify LSB of blue
            binary_index += 1

        encoded_pixels.append((r, g, b) + pixel[3:] if len(pixel) == 4 else (r, g, b))  # Preserve alpha if present

    encoded_image.putdata(encoded_pixels)
    encoded_image.save(output_path)
    print(f"Message successfully encoded into {output_path}")

def decode_message(image_path):
    """Decodes a secret message from an image."""
    image = Image.open(image_path)
    pixel_data = list(image.getdata())

    binary_message = ""
    for pixel in pixel_data:
        r, g, b = pixel[:3]
        binary_message += str(r & 1)  # Extract LSB from red
        binary_message += str(g & 1)  # Extract LSB from green
        binary_message += str(b & 1)  # Extract LSB from blue

    decoded_message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        decoded_message += chr(int(byte, 2))
        if "<END>" in decoded_message:  
            break

    return decoded_message.replace("<END>", "")

if __name__ == "__main__":
    
    encode_message("input_image.png", "This is a secret message", "encoded_image.png")

    secret_message = decode_message("encoded_image.png")
    print(f"Decoded Message: {secret_message}")
