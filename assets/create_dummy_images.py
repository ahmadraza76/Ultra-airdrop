#!/usr/bin/env python3
"""
Script to create dummy image files for the bot assets
Run this script to create placeholder images if you don't have actual images
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_dummy_image(filename, text, size=(400, 300), bg_color=(100, 150, 200), text_color=(255, 255, 255)):
    """Create a dummy image with text"""
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position to center it
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    draw.text((x, y), text, fill=text_color, font=font)
    img.save(filename)
    print(f"Created: {filename}")

def main():
    # Create assets directory if it doesn't exist
    os.makedirs("assets", exist_ok=True)
    os.makedirs("assets/captcha_images", exist_ok=True)
    
    # Create dummy images
    create_dummy_image("assets/banner.jpg", "JHOOM AIRDROP\nWelcome!", (600, 400), (50, 100, 200))
    create_dummy_image("assets/success_icon.png", "SUCCESS", (200, 200), (50, 200, 50))
    create_dummy_image("assets/error_icon.png", "ERROR", (200, 200), (200, 50, 50))
    create_dummy_image("assets/withdrawal_banner.jpg", "WITHDRAWAL\nREQUEST", (500, 300), (150, 100, 200))
    create_dummy_image("assets/tasks_banner.jpg", "COMPLETE\nTASKS", (500, 300), (100, 150, 100))
    
    # Create dummy captcha images
    for i in range(5):
        create_dummy_image(f"assets/captcha_images/captcha_{i+1}.png", f"CAPTCHA\n{i+1}", (300, 200), (80, 80, 80))
    
    print("\nAll dummy images created successfully!")
    print("Replace these with your actual images when ready.")

if __name__ == "__main__":
    main()