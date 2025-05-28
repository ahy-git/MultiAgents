import os

class RenameFailedImage:
    """
    Renames an image by appending a fail suffix if it does not pass the verification step.
    """

    @staticmethod
    def rename_image(image_path):
        """
        Renames the image by adding 'fail001' to its filename.

        :param image_path: Path to the image file that failed verification.
        :return: New image path after renaming.
        """
        directory, filename = os.path.split(image_path)
        name, ext = os.path.splitext(filename)

        # Generate the new filename
        new_filename = f"{name}_fail001{ext}"
        new_image_path = os.path.join(directory, new_filename)

        # Rename the file
        os.rename(image_path, new_image_path)
        print(f"❌ Image verification failed. Renamed to: {new_image_path}")

        return new_image_path
