
from ultralytics.utils.downloads import download
from pathlib import Path

yaml = {'path': 'datasets'}
# Download labels
dir = Path(yaml['path'])  # dataset root dir
url = 'https://github.com/ultralytics/assets/releases/download/v0.0.0/'
urls = [url + 'coco2017labels-pose.zip']  # labels
download(urls, dir=dir.parent)
# Download data
urls = ['http://images.cocodataset.org/zips/train2017.zip',  # 19G, 118k images
        'http://images.cocodataset.org/zips/val2017.zip',  # 1G, 5k images
        'http://images.cocodataset.org/zips/test2017.zip',  # 7G, 41k images (optional)
        'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'] # 241MB
download(urls, dir=dir / 'images', threads=4)