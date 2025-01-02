import os
from PIL import Image
from nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

class ImageToIconNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_image": ("IMAGE",),  # Accepts an image input
                "output_directory": ("STRING", {
                    "default": "./outputs",
                    "placeholder": "Directory to save the ICO file"
                }),
                "icon_sizes": ("STRING", {
                    "default": "16,32,48,64,128,256",
                    "placeholder": "Comma-separated sizes (e.g., 16,32,48,256)"
                }),
                "file_name": ("STRING", {
                    "default": "output_icon",
                    "placeholder": "Output file name (no extension)"
                }),
            }
        }

    @classmethod
    def OUTPUT_TYPES(cls):
        return {
            "output_file_path": ("STRING",)  # Output path to the ICO file
        }

    @classmethod
    def CATEGORY(cls):
        return "Image Processing"  # Node category in the UI

    @classmethod
    def FUNCTION(cls):
        return "convert_to_ico"

    def convert_to_ico(self, input_image, output_directory, icon_sizes, file_name):
        # Ensure output directory exists
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Process icon sizes
        try:
            sizes = [(int(size), int(size)) for size in icon_sizes.split(",") if size.isdigit()]
        except ValueError:
            raise ValueError("Icon sizes must be a comma-separated list of integers.")

        if not sizes:
            raise ValueError("No valid icon sizes provided.")

        # Convert input image from tensor to PIL format
        image = Image.fromarray((input_image * 255).astype('uint8'))

        # Convert image to RGBA if required
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        # Prepare output file path
        output_file_path = os.path.join(output_directory, f"{file_name}.ico")

        # Save as ICO with specified sizes
        try:
            image.save(output_file_path, format="ICO", sizes=sizes)
        except Exception as e:
            raise ValueError(f"Failed to save ICO file: {str(e)}")

        return (output_file_path,)



