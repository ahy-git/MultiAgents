import glob
import os

def get_pending_posts(post_type):
    """
    Checks for pending Instagram content of a specific type.

    :param post_type: Type of content ('posts', 'stories', 'carousels', 'reels').
    :return: List of pending post folders.
    """
    valid_types = {"posts": "post", "stories": "stories", "carousels": "carousel", "reels": "reels"}
    
    if post_type not in valid_types:
        print(f"❌ Invalid post type: {post_type}. Choose from {list(valid_types.keys())}.")
        return []

    # Look for folders matching the post type pattern
    post_folders = sorted(glob.glob(f"./assets/*_{valid_types[post_type]}_*"))

    if not post_folders:
        print(f"✅ No pending {post_type.capitalize()} found.")
        return []

    return post_folders
