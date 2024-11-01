import os
import zipfile
import requests
from pydantic import BaseModel
from typing import Optional

# import modules.script_callbacks as script_callbacks
# from modules import shared, scripts


class Item(BaseModel):
    # image url.
    image_url: str
    # stringified pose JSON.
    pose: str


EXTENSION_DIR = os.path.dirname(os.path.realpath(__file__))
DIST_DIR = os.path.join(EXTENSION_DIR, "dist")


def get_latest_release(owner, repo) -> Optional[str]:
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data["tag_name"]
    else:
        return None


def get_current_release() -> Optional[str]:
    if not os.path.exists(DIST_DIR):
        return None

    with open(os.path.join(DIST_DIR, "version.txt"), "r") as f:
        return f.read()


def download_latest_release(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "assets" in data and len(data["assets"]) > 0:
        asset_url = data["assets"][0]["url"]  # Get the URL of the first asset
        headers = {"Accept": "application/octet-stream"}
        response = requests.get(asset_url, headers=headers, allow_redirects=True)

        if response.status_code == 200:
            filename = "dist.zip"
            with open(filename, "wb") as file:
                file.write(response.content)

            # Unzip the file
            with zipfile.ZipFile(filename, "r") as zip_ref:
                zip_ref.extractall(DIST_DIR)

            # Remove the zip file
            os.remove(filename)
        else:
            print(f"Failed to download the file {url}.")
    else:
        print(f"Could not get the latest release or there are no assets {url}.")


def need_update(current_version: Optional[str], package_version: str) -> bool:
    if current_version is None:
        print("Openpose-Editor distribution doesn't exist.")
        return True

    def parse_version(version: str):
        return tuple(int(num) for num in version[1:].split('.'))

    return parse_version(current_version) < parse_version(package_version)


def update_app():
    """Attempts to update the application to latest version"""
    owner = "huchenlei"
    repo = "sd-webui-openpose-editor"

    latest_version = get_latest_release(owner, repo)
    current_version = get_current_release()

    assert latest_version is not None
    if need_update(current_version, latest_version):
        print(f"Downloading latest version ({latest_version}) of Openpose-Editor.")
        download_latest_release(owner, repo)
