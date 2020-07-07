import os
import random
import time

import requests
import re
import db

tag = "princess_connect!"
proxies = {
    'http': '127.0.0.1:1080',
    'https': '127.0.0.1:1080'
}
post_url = "https://danbooru.donmai.us/posts/{id}"
post_search_url = "https://danbooru.donmai.us/posts?page={page}&tags=order%3Ascore+rating%3Asafe+{tag}"

# image_path = "C:/Users/Administrator/Desktop/酷Q Pro/data/image/temp/"
image_path = "D:/Workspace/Python/setu"


def request_get(url):
    times = 0
    err = None
    while times < 5:
        try:
            resp = requests.get(url, proxies=proxies)
            return resp
        except Exception as e:
            times += 1
            err = e
            print("发送错误 尝试重试：", e)
            time.sleep(0.5)
    raise e


def get_random_img_in_file():
    image_list = os.listdir(image_path)
    filename = random.choice(image_list)
    return filename


def get_file_count():
    files = os.listdir(image_path)
    return len(files)


def download_image(url, filename):
    r = request_get(url)
    with open(os.path.join(image_path, filename), 'wb') as f:
        f.write(r.content)


def random_download(num=10):
    images = db.get_img_url(mark=False, num=num)
    for image in images:
        download_image(image["url"], image["filename"])
        db.download_image(image["id"])
    return len(images)


def delete_image(filename):
    os.remove(os.path.join(image_path, filename))


def clean_image_mark():
    mark_list = db.get_mark_img()
    files = os.listdir(image_path)
    for file in files:
        if file in mark_list:
            delete_image(file)


def check_image_download():
    db.clean_download_record()
    files = os.listdir(image_path)
    for file in files:
        id = file.split('.')[0]
        db.download_image(id)


class SearchMachine:
    def __init__(self):
        self._searching = False

    def search(self, _tag):
        if self._searching:
            return "搜索任务尚未完成"
        self._searching = True
        message = ""
        try:
            resp = request_get(post_search_url.format(page=1, tag=_tag))
            r = re.findall(r"<li class='numbered-page'>.*?>(\d+)<.*?</li>", resp.text)
            if not r:
                message = "搜索结果不存在"
            else:
                page_max = int(r[-1])
                for i in range(1, page_max + 1):
                    resp = request_get(post_search_url.format(page=i, tag=_tag))
                    it = re.finditer(r'<article.*?data-id="(\d+)".*?</article>', resp.text, re.S)
                    for match in it:
                        post_id = match.group(1)
                        if db.has_img(post_id):
                            continue
                        r = request_get(post_url.format(id=post_id))
                        rating = re.search('<li id="post-info-rating">Rating: (.*?)</li>',
                                           r.text).group(1)
                        url = re.search('<a download.*?href="(.*?)"', r.text).group(1)
                        filename = post_id + '.' + re.search(r'\.(.*?)\?',
                                                             url.split('/')[-1]).group(1)
                        # print(url)
                        db.new_img(id=post_id, rating=rating, url=url, filename=filename)
                        time.sleep(0.1)
                message = "获取结果共{}页".format(page_max)
        except Exception as e:
            message = "发生错误:{}".format(e)
        finally:
            self._searching = False
        return message


if __name__ == "__main__":
    s = SearchMachine()
    print(s.search(tag))
    # print(clean_image_mark())
    # check_image_download()
