import requests
import os
from urllib.parse import urlparse
import hashlib 


def fetch_image(url):
    try:
        # Create directory if not exists
        os.makedirs("Fetched_Images", exist_ok=True)

        # Fetch the image with timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check for HTTP errors

        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # Generate fallback filename if empty
        if not filename:
            filename = "downloaded_image.jpg"

        # Avoid duplicates: use hash of content
        file_hash = hashlib.md5(response.content).hexdigest()
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{file_hash[:8]}{ext}" if ext else f"{name}_{file_hash[:8]}.jpg"

        # Save the image in binary mode
        filepath = os.path.join("Fetched_Images", filename)
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        print("\nConnection strengthened. Community enriched.\n")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")


def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Ask for multiple URLs (comma-separated)
    urls = input("Please enter one or more image URLs (comma separated): ").split(",")

    for url in urls:
        url = url.strip()
        if url:
            fetch_image(url)



def group_similar_images(folder="Fetched_Images", hash_size=8, threshold=5):
    """
    Groups similar images in the specified folder using perceptual hashing.
    Each group is placed in a subfolder named 'group_X'.
    """
    import imagehash
    from PIL import Image
    from collections import defaultdict

    # Collect image files
    image_files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif"))]
    hashes = []
    groups = defaultdict(list)
    group_id = 1

    for img_file in image_files:
        img_path = os.path.join(folder, img_file)
        try:
            with Image.open(img_path) as img:
                img_hash = imagehash.average_hash(img, hash_size=hash_size)
        except Exception as e:
            print(f"Could not process {img_file}: {e}")
            continue

        # Try to find a similar hash in existing groups
        found_group = False
        for h, gid in hashes:
            if img_hash - h <= threshold:
                groups[gid].append(img_file)
                found_group = True
                break
        if not found_group:
            hashes.append((img_hash, group_id))
            groups[group_id].append(img_file)
            group_id += 1

    # Move files into group folders
    for gid, files in groups.items():
        group_folder = os.path.join(folder, f"group_{gid}")
        os.makedirs(group_folder, exist_ok=True)
        for f in files:
            src = os.path.join(folder, f)
            dst = os.path.join(group_folder, f)
            if not os.path.exists(dst):
                os.rename(src, dst)
    print(f"\nGrouped {len(image_files)} images into {len(groups)} groups.")


if __name__ == "__main__":
    main()
    # After fetching, group similar images
    group_similar_images()
