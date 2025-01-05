import torch
import numpy as np
from PIL import Image, ImageDraw
import os


class ConvertToIconNode:
    """
    Custom ComfyUI Node to convert an input image tensor to an icon file (ICO) while preserving the alpha channel
    and applying rounded corners to the image. Also displays the saved icon image within the node.
    """

    # Node metadata
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),  # Accepts an image input tensor
                "filename": ("STRING", {"default": "output.ico"}),  # Output filename base
                "size": ("INT", {"default": 256, "min": 16, "max": 512}),  # Icon size
                "corner_radius": ("INT", {"default": 20, "min": 1, "max": 128}),  # Corner radius for rounding
            },
        }

    RETURN_TYPES = ("STRING", "IMAGE",)  # Return the file path and the image preview
    FUNCTION = "convert_to_icon"  # Main function name
    CATEGORY = "Image Processing"  # Category in ComfyUI
    OUTPUT_NODE = True

    def convert_to_icon(self, image, filename, size, corner_radius):
        """
        Converts the input tensor image to an ICO file, preserving alpha transparency,
        rounding the corners, with an incrementing filename and saving it to the 'icons' subfolder.
        """

        # Convert PyTorch tensor to PIL Image
        if isinstance(image, torch.Tensor):
            image = image.squeeze(0).cpu().numpy()  # Remove batch dimension
            image = (image * 255).astype("uint8")  # Scale to 0-255 and convert type

            # Ensure correct RGB or RGBA format
            if image.shape[-1] == 3:  # RGB
                image = Image.fromarray(image, mode="RGB")
            elif image.shape[-1] == 4:  # RGBA
                image = Image.fromarray(image, mode="RGBA")
            else:
                raise ValueError("Unsupported image format. Ensure 3 (RGB) or 4 (RGBA) channels.")

        # Resize image to specified size
        image = image.resize((size, size), Image.LANCZOS)

        # Apply rounded corners
        image = self.apply_rounded_corners(image, corner_radius)

        # Define the output folder and ensure it exists
        output_folder = os.path.join(os.getcwd(), "output", "icons")
        os.makedirs(output_folder, exist_ok=True)

        # Generate the incrementing filename
        base_filename = filename.split(".")[0]  # Remove the extension
        extension = ".ico"
        counter = 1
        output_path = os.path.join(output_folder, f"{base_filename}_{counter}{extension}")
        while os.path.exists(output_path):  # Check if the file exists and increment if necessary
            counter += 1
            output_path = os.path.join(output_folder, f"{base_filename}_{counter}{extension}")

        # Save as ICO file, preserving transparency
        image.save(output_path, format="ICO")

        # Convert the image to NumPy array for preview
        preview_image = np.array(image.convert("RGBA"))  # Fixed conversion

        # Return the output file path and the preview image as tensor
        return output_path, torch.from_numpy(preview_image).float().div(255.0).unsqueeze(0)

    def apply_rounded_corners(self, image, radius):
        """
        Apply rounded corners to the image.
        """
        # Create a mask for rounded corners
        width, height = image.size
        rounded_mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(rounded_mask)
        draw.rounded_rectangle(
            (0, 0, width, height), radius, fill=255
        )

        # Create a new image with rounded corners using the mask
        image.putalpha(rounded_mask)

        # Return the image with rounded corners
        return image
