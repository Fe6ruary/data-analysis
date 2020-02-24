# -*- coding: utf-8 -*-


import json
import codecs



class Huxiuv1Pipeline(object):

    def __init__(self):
        self.file = codecs.open('items.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        print(item)
        line = json.dumps(dict(item), indent=4, ensure_ascii=False) + "\n"  # python3解决scrapy中文编码存储问题

        self.file.write(line)
        return item
    

