# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import xlwt


class ToutiaoPipeline(object):
    def __init__(self):
        self.book = xlwt.Workbook()
        self.sheet = self.book.add_sheet('sheet', cell_overwrite_ok=True)
        head = [u'名字', u'点赞', u'回复', u'评论']
        i = 0
        for h in head:
            self.sheet.write(0, i, h)
            i += 1

    def process_item(self, item, spider):
        self.sheet.write(item['Num'], 0, item['name'])
        self.sheet.write(item['Num'], 1, item['like'])
        self.sheet.write(item['Num'], 2, item['reply'])
        self.sheet.write(item['Num'], 3, item['text'])
        self.book.save('TouTiao.xls')

    # def __init__(self):
    #     # pymongo.MongoClient连接到数据库
    #     connection = pymongo.MongoClient(settings['MONGODB_HOST'], settings['MONGODB_PORT'])
    #     # 创建数据库'db1'
    #     db = connection[settings['MONGODB_NAME']]
    #     # 连接到数据集'toutiao'，类型为dict
    #     self.post = db[settings['MONGODB_DOCNAME']]
    #
    # def process_item(self, item, spider):
    #     # 插入数据到数据库
    #     self.post.update({'text': item['text']}, {'$set': dict(item)}, upsert=True)
    #     print
    #     u'插入成功!'
    #     return item
