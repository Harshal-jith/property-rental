import os
from PIL import Image, ImageDraw, ImageFont

def generate_gradient_image(path, width, height, text, color1, color2):
    # Create gradient background
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_draw = ImageDraw.Draw(mask)
    for y in range(height):
        # Linear gradient calculation
        level = int(255 * (y / height))
        mask_draw.line([(0, y), (width, y)], fill=level)
    
    gradient_img = Image.composite(top, base, mask)
    draw = ImageDraw.Draw(gradient_img)
    
    # Try to load default font
    try:
        # standard fallback
        font = ImageFont.load_default()
    except IOError:
        font = None
        
    # Draw label text
    draw.text((30, height - 50), text, fill=(255, 255, 255), font=font)
    
    # Draw simple architectural overlays (boxes/lines representing windows/roofs) to look like real estate
    draw.rectangle([width - 150, height - 150, width - 50, height - 50], outline=(255, 255, 255, 128), width=3)
    draw.line([width - 170, height - 150, width - 100, height - 200, width - 30, height - 150], fill=(255, 255, 255), width=4)
    draw.rectangle([width - 130, height - 100, width - 100, height - 50], fill=(255, 255, 255, 80)) # Door
    draw.rectangle([width - 85, height - 120, width - 65, height - 100], fill=(255, 255, 255, 80)) # Window
    
    # Save file
    os.makedirs(os.path.dirname(path), exist_ok=True)
    gradient_img.save(path, 'JPEG', quality=90)
    print(f"Generated placeholder image at: {path}")

def main():
    # Make directories
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('media/properties/main', exist_ok=True)
    os.makedirs('media/properties/gallery', exist_ok=True)
    
    # Generate static assets placeholders
    generate_gradient_image(
        'static/images/hero-bg.jpg', 
        1200, 800, 
        "Modern Real Estate Portal - Find Your Home", 
        (15, 23, 42), (79, 70, 229)
    )
    
    generate_gradient_image(
        'static/images/why-choose-us.jpg', 
        800, 600, 
        "Premium Living Rooms & Transparent Deals", 
        (30, 41, 59), (99, 102, 241)
    )
    
    generate_gradient_image(
        'static/images/placeholder.jpg', 
        600, 400, 
        "Image Coming Soon", 
        (100, 116, 139), (148, 163, 184)
    )
    
    # Generate media property images
    properties_data = [
        ("villa", (124, 58, 237), (139, 92, 246)),
        ("apartment", (13, 148, 136), (20, 184, 166)),
        ("penthouse", (219, 39, 119), (236, 72, 153)),
        ("studio", (217, 70, 239), (240, 171, 252)),
        ("cottage", (220, 38, 38), (239, 68, 68)),
        ("townhouse", (202, 138, 4), (234, 179, 8))
    ]
    
    for prefix, color1, color2 in properties_data:
        # Main property photo
        generate_gradient_image(
            f'media/properties/main/{prefix}_main.jpg', 
            800, 533, 
            f"Luxury {prefix.capitalize()} - Main Exterior Showcase", 
            color1, color2
        )
        
        # Gallery secondary photo
        generate_gradient_image(
            f'media/properties/gallery/{prefix}_gallery1.jpg', 
            800, 533, 
            f"Interior view of {prefix.capitalize()}", 
            color2, color1
        )
        generate_gradient_image(
            f'media/properties/gallery/{prefix}_gallery2.jpg', 
            800, 533, 
            f"Kitchen / Living room of {prefix.capitalize()}", 
            (71, 85, 105), color1
        )

if __name__ == '__main__':
    main()
