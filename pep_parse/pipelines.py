import csv

from collections import Counter
from datetime import datetime

from pep_parse.settings import BASE_DIR


class PepParsePipeline:
    def __init__(self):
        self.status_counts = Counter()
        self.results_dir = f'{BASE_DIR}/results'

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        status = item.get('status')
        self.status_counts[status] += 1
        return item

    def close_spider(self, spider):
        template_csv = f'{self.results_dir}/status_summary_%Y-%m-%d-%H-%M.csv'
        filename = datetime.now().strftime(template_csv)
        with open(filename, mode='w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['Статус', 'Количество']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            writer.writerows(self.status_counts.items())
            writer.writerow(['Total', self.status_counts.total()])
            csvfile.close()
