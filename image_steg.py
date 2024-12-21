import argparse
from PIL import Image

def encode_message_in_image(image_path, message, output_image_path):
    image = Image.open(image_path)
    
    # Convert the message to bytes and append the delimiter
    message_bytes = message.encode('utf-8') + b"<END>"
    binary_message = ''.join(format(byte, '08b') for byte in message_bytes)
    
    binary_index = 0
    pixels = list(image.getdata())
    encoded_pixels = []

    for pixel in pixels:
        r, g, b = pixel[:3]  # Get RGB values
        if binary_index < len(binary_message):
            r = (r & ~1) | int(binary_message[binary_index])  # Modify LSB of red
            binary_index += 1
        if binary_index < len(binary_message):
            g = (g & ~1) | int(binary_message[binary_index])  # Modify LSB of green
            binary_index += 1
        if binary_index < len(binary_message):
            b = (b & ~1) | int(binary_message[binary_index])  # Modify LSB of blue
            binary_index += 1

        encoded_pixels.append((r, g, b) + pixel[3:] if len(pixel) == 4 else (r, g, b))  # Preserve alpha if present

    image.putdata(encoded_pixels)
    image.save(output_image_path)

def decode_message_from_image(image_path):
    image = Image.open(image_path)
    binary_message = ''
    pixels = list(image.getdata())

    for pixel in pixels:
        r, g, b = pixel[:3]  # Get RGB values
        binary_message += str(r & 1)  # Extract LSB of red
        binary_message += str(g & 1)  # Extract LSB of green
        binary_message += str(b & 1)  # Extract LSB of blue

    # Split binary string into bytes
    message_bytes = bytearray()
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            message_bytes.append(int(byte, 2))
            if message_bytes[-5:] == b"<END>":  # Check for the end delimiter
                message_bytes = message_bytes[:-5]  # Remove the delimiter
                break

    # Convert bytes to string
    return message_bytes.decode('utf-8')

def main():
    parser = argparse.ArgumentParser(description="Hide and Retrieve Messages in an Image using Steganography")
    parser.add_argument('action', choices=['encode', 'decode'], help="Action to perform: encode or decode")
    parser.add_argument('image', help="Path to the image file")
    parser.add_argument('output', help="Path to the output image (for encoding) or file to save decoded message")
    parser.add_argument('--message', help="Message to hide (for encoding only)", default=None)

    args = parser.parse_args()

    if args.action == 'encode':
        if not args.message:
            print("Please provide a message to encode using --message")
            return
        encode_message_in_image(args.image, args.message, args.output)  # Encode the message in the image
        print(f"Message encoded and saved in {args.output}")

    elif args.action == 'decode':
        decoded_message = decode_message_from_image(args.image)  # Decode the message from the image
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(decoded_message)
        print(f"Decoded message saved to {args.output}")

if __name__ == "__main__":
    main()
