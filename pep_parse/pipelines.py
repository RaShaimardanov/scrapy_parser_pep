import csv
from datetime import datetime
from collections import defaultdict

from pep_parse.settings import DT_FORMAT, BASE_DIR, RESULTS, ENCODING


class PepParsePipeline:

    def __init__(self):
        self.results_dir = BASE_DIR / RESULTS
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.status_counts = defaultdict(int)

    def process_item(self, item, spider):
        self.status_counts[item.get('status')] += 1
        return item

    def close_spider(self, spider):
        now_time = datetime.now().strftime(DT_FORMAT)
        filename = f'status_summary_{now_time}.csv'
        with open(
            self.results_dir / filename,
            mode='w', encoding=ENCODING
        ) as csvfile:
            csv.writer(
                csvfile, dialect=csv.unix_dialect, quoting=csv.QUOTE_NONE,
            ).writerows(
                (
                    ('Статус', 'Количество'),
                    *self.status_counts.items(),
                    ('Итого', sum(self.status_counts.values()))
                )
            )
