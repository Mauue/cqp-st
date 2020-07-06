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


def request_get(url):
    return requests.get(url, proxies=proxies)


def test():
    url = "https://danbooru.donmai.us/posts?page={page}&tags={tag}"
    resp = requests.get(url.format(page=1, tag=tag), proxies=proxies)
    it = re.finditer(r'<article.*?data-id="(\d+)".*?</article>', resp.text, re.S)
    for match in it:
        id = match.group(1)
        r = request_get(post_url.format(id=id))
        rating = re.search('<li id="post-info-rating">Rating: (.*?)</li>', r.text).group(1)
        url = re.search('<a download.*?href="(.*?)"', r.text).group(1)
        db.new_img(id=id, rating=rating, url=url)
        time.sleep(1)


if __name__ == "__main__":
    test()

