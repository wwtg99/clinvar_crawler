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
        status = response.xpath('//div[@id="main_box"]//dl[@id="mainrevstatandid"]//span[@class="rev_stat_text hide"]/text()').extract()
        if len(status) > 0:
            status = status[0]
        else:
            status = 0
        # alleles
        titles = response.xpath('//div[@id="main_box"]//h4')
        for title in titles:
            t = title.xpath('text()').extract()[0]
            item = ClinvarItem()
            item['vid'] = vid
            item['significance'] = sig
            item['status'] = status
            item['title'] = t
            dts = title.xpath('//div[@id="main_box"]//h4')[0].xpath('following-sibling::div/div[@class="dl_container_content"]/dl/dt')
            for d in dts:
                tt = d.xpath('text()').extract()[0]
                dd = d.xpath('following-sibling::dd[1]')
                if tt == 'Variant type:':
                    item['variant_type'] = dd.xpath('text()').extract()[0]
                elif tt == 'Genomic location:':
                    item['location'] = dd.xpath('./ul/li/span/text()').extract()
                elif tt == 'NCBI 1000 Genomes Browser:':
                    item['rs'] = dd.xpath('./a/text()').extract()[0]
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
