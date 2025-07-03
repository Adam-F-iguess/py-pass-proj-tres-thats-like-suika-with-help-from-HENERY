from PIL import Image
import os

def create_icns_from_png(png_path, icns_path):
    """Convert PNG to ICNS format for macOS"""
    try:
        # Load the original image
        img = Image.open(png_path)
        
        # Create iconset directory
        iconset_dir = "watermelon.iconset"
        os.makedirs(iconset_dir, exist_ok=True)
        
        # Define the required sizes for macOS icons
        sizes = [
            (16, "icon_16x16.png"),
            (32, "icon_16x16@2x.png"),
            (32, "icon_32x32.png"),
            (64, "icon_32x32@2x.png"),
            (128, "icon_128x128.png"),
            (256, "icon_128x128@2x.png"),
            (256, "icon_256x256.png"),
            (512, "icon_256x256@2x.png"),
            (512, "icon_512x512.png"),
            (1024, "icon_512x512@2x.png"),
        ]
        
        # Generate all required sizes
        for size, filename in sizes:
            resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
            resized_img.save(os.path.join(iconset_dir, filename))
        
        # Convert iconset to icns using macOS command line tool
        os.system(f"iconutil -c icns {iconset_dir}")
        
        # Clean up iconset directory
        import shutil
        shutil.rmtree(iconset_dir)
        
        print(f"Successfully created {icns_path}")
        
    except Exception as e:
        print(f"Error creating ICNS file: {e}")
        print("Make sure you're running this on macOS with iconutil available")

if __name__ == "__main__":
    create_icns_from_png("sprites/watermelon.png", "watermelon.icns")