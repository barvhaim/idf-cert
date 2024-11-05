import os
import json
from PIL import Image, ImageDraw, ImageFont

# Load your certificate template in JPEG format
template_path = "certificate_template.jpeg"  # Path to the certificate template image (JPEG)
output_dir = "output/"  # Directory where certificates will be saved
font_path = "hebrew_font.ttf"  # Path to a .ttf font file (adjust path as needed)
font_size = 36  # Adjust font size as needed


def load_names():
    with open('names.json') as f:
        names = json.load(f)
    return names


def run():
    names = load_names()
    os.makedirs(output_dir, exist_ok=True)

    # Load the certificate template
    template = Image.open(template_path)
    draw = ImageDraw.Draw(template)

    font = ImageFont.truetype(font_path, font_size)
    text_x, text_y = 512, 512  # Position of the text on the certificate

    for name in names:
        # Make a copy of the template for each certificate
        certificate = template.copy()
        draw = ImageDraw.Draw(certificate)

        # Adjust text for right-to-left display using python-bidi
        name_display = name

        # Calculate text width and height using textbbox
        text_bbox = draw.textbbox((0, 0), name_display, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Position the text centered around (text_x, text_y)
        position = (text_x - text_width // 2, text_y - text_height // 2)

        # Draw the name on the certificate in white color
        draw.text(position, name_display, fill="white", font=font)  # Set text color to white

        # Save the certificate as a JPEG with the soldier's name in the filename
        output_path = f"{output_dir}{name.replace(' ', '_')}_certificate.jpeg"
        certificate.save(output_path, format="JPEG")
        print(f"Saved certificate for {name} at {output_path}")


if __name__ == '__main__':
    run()
