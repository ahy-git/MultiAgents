import os

def finalize_post(post_folder, post_id, imgur_client, imgur_data):
    """
    Marks a post as completed by creating a `.posted` file and deletes the image from Imgur.

    :param post_folder: Path to the post directory.
    :param post_id: ID of the post published on Instagram.
    :param imgur_client: Instance of `ImageUploader` to delete images.
    :param imgur_data: Dictionary containing Imgur image data (including `deletehash`).
    """
    posted_flag = os.path.join(post_folder, ".posted")

    # ✅ Save post ID to `.posted`
    with open(posted_flag, "w", encoding="utf-8") as f:
        f.write(f"Postado em: {post_id}\n")
    print(f"✅ Marked as posted: {posted_flag}")

    # ✅ Attempt to delete the image from Imgur
    deletehash = imgur_data.get("deletehash")
    if deletehash:
        print(f"🗑️ Deleting Imgur image: {deletehash}")
        if imgur_client.delete_image(deletehash, post_folder):
            print(f"✅ Successfully deleted image: {deletehash}")
        else:
            print(f"❌ Error deleting image: {deletehash}")
    else:
        print("⚠️ No deletehash found, skipping image deletion.")
