# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import os
from clinvar.items import ClinvarItem


class ClinvarCrawlerSpider(scrapy.Spider):
    name = 'clinvar_crawler'
    allowed_domains = ['www.ncbi.nlm.nih.gov']
    start_urls = []
    host_url = 'http://www.ncbi.nlm.nih.gov/clinvar/variation/'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self._idlist = kwargs['id'].split(',') if 'id' in kwargs else []
        self._file = kwargs['file'] if 'file' in kwargs else None

    def start_requests(self):
        if self._idlist:
            # from argument rs=
            yield from self.from_id_list()
        elif self._file:
            # from argument file=
            if os.path.exists(self._file):
                yield from self.from_id_file()
        return None

    def parse(self, response):
        vid = response.xpath('//div[@id="main_box"]//dl[@id="mainrevstatandid"]/dd/text()').extract()[0]
        sig = response.xpath('//div[@id="main_box"]//dl[@class="details clearfix clin_sig_dl"]/dd/a/text()').extract()[0]
        status = response.xpath('//div[@id="main_box"]//dl[@id="mainrevstatandid"]//span[@class="clinsig_confidence rating"]/span/span').extract()
        rsa = response.xpath('//div[@id="main_box"]//div[@class="dl_container_content"]//dd/a//text()').extract()
        rs = []
        for r in rsa:
            if r[0:2] == 'rs':
                rs.append(r)
        item = ClinvarItem()
        item['vid'] = vid
        item['significance'] = sig
        item['rs'] = rs
        yield item

    def from_id_list(self):
        """
        Load rs list from -a rs=rs1,rs2,...
        :return:
        """
        for i in self._idlist:
            yield Request(self.host_url + i, dont_filter=True)

    def from_id_file(self):
        """
        Load rs from file use -a file=rs_file_path
        Each rs per line or rs in the first column.
        :return:
        """
        with open(self._file) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                if line.find('\t') > 0:
                    cols = line.split('\t')
                    line = cols[0]
                elif line.find(',') > 0:
                    cols = line.split(',')
                    line = cols[0]
                yield Request(self.host_url + line, dont_filter=True)
