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
post_search_url = "https://danbooru.donmai.us/posts?page={page}&tags={tag}"


def request_get(url):
    return requests.get(url, proxies=proxies)


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
                        r = request_get(post_url.format(id=post_id))
                        rating = re.search('<li id="post-info-rating">Rating: (.*?)</li>', r.text).group(1)
                        url = re.search('<a download.*?href="(.*?)"', r.text).group(1)
                        db.new_img(id=post_id, rating=rating, url=url)
                        time.sleep(0.2)
                message = "获取结果共{}页".format(page_max)
        except Exception as e:
            message = "发生错误:{}".format(e)
        finally:
            self._searching = False
        return message


if __name__ == "__main__":
    s = SearchMachine()
    print(s.search(tag))

