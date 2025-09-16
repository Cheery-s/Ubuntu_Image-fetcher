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


if __name__ == "__main__":
    main()
    
    


