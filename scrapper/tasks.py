from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .scrapper import HhParser, AreaScrapper



@shared_task(name='scrapping_hh')
def scrapping_hh(language=None):
    print('hi')
    hh_parser = HhParser()
    hh_parser.scrap(language)

@shared_task(name='area_scrapping')
def area_scrapping():
    area_scrapper = AreaScrapper()
    area_scrapper.scrap_areas()

