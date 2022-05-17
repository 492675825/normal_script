from goldapp.gold.script import gold_spider, data_transform, log_function
import pandas as pd

class run:
    def app_run(self):
        spider = gold_spider.gold_data()
        spider.get_data_by_page_number(page_number=1)  # 只抓取最新一页的数据
        transform = data_transform.data_transform()
        transform.main()
