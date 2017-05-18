"""
This file contains running and processing of Heart Diseases Data set from UCI repository
"""
from constants import HDD_HEADERS
from processors.model_processor import Processor


class HddProcessor(Processor):
    def __init__(self, url=None, size=0):
        super(HddProcessor, self).__init__(url, size=size, cols=HDD_HEADERS)
        if not url:
            urls = self.dp.process_hdd()
            self.url = self.dp.join_hdd(urls)
            self.data = self.get_data(self.url).fillna(0)
#