import urllib.request
from invoke import task
import json
import os
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def download_releases(base_dir, repo, target_dir):
    if not base_dir:
        base_dir = f"../release"
    asset_dir = f"{base_dir}/{target_dir}"
    if not os.path.exists(asset_dir):
        os.makedirs(asset_dir)

    release_json_path = f'{asset_dir}/releases.json'
    urllib.request.urlretrieve(
        f"https://api.github.com/repos/{repo}/releases", filename=release_json_path)
    with open(release_json_path) as json_file:
        tags = json.load(json_file)

    logger.info(f"{release_json_path} downloaded")
    for tag in tags:
        if not tag['prerelease']:
            tag_dir = f"{asset_dir}/{tag['tag_name']}"
            if not os.path.exists(tag_dir):
                os.makedirs(tag_dir)
            for asset in tag['assets']:
                asset_path = f"{tag_dir}/{asset['name']}"
                if not os.path.exists(asset_path):
                    download_url = asset['browser_download_url']
                    logger.info(f"start to request {download_url}")
                    urllib.request.urlretrieve(
                        download_url, filename=asset_path)
                else:
                    logger.debug(f"skip to download {asset_path}")


@task
def sync_release(c, base_dir=None, repo=None, target=None):
    download_releases(base_dir, repo, target)
