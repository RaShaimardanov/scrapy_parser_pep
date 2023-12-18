import csv
from datetime import datetime

from pep_parse.settings import DT_FORMAT, BASE_DIR, RESULTS


class PepParsePipeline:

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        status = item.get('status')
        spider.state[status] = spider.state.get(status, 0) + 1
        return item

    def close_spider(self, spider):
        now_time = datetime.now().strftime(DT_FORMAT)
        filename = f'status_summary_{now_time}.csv'
        with open(
            BASE_DIR / RESULTS / filename,
            mode="w", encoding='utf-8', newline=''
        ) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(
                (
                    ('Статус', 'Количество'),
                    *spider.state.items(),
                    ('Итого', sum(spider.state.values()))
                )
            )
