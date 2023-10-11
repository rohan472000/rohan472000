import requests
import base64
import re
from PIL import Image
from io import BytesIO

readme_content_url = (
    "https://api.github.com/repos/rohan472000/rohan472000/contents/README.md"
)

try:
    response = requests.get(readme_content_url)
    response.raise_for_status()

    content_info = response.json()
    content = content_info["content"]
    encoding = content_info["encoding"]

    if encoding == "base64":
        decoded_content = base64.b64decode(content).decode("utf-8")

        image_url_pattern = r"!\[Funny Meme\]\((.*?)\)"
        match = re.search(image_url_pattern, decoded_content)

        if match:
            image_url = match.group(1)

            print("Image URL:")
            print(image_url)

            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img.show()
        else:
            print("Image URL not found in README content.")
    else:
        print("Unsupported encoding:", encoding)

except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching the README: {e}")
