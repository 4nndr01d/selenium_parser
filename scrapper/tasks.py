from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .scrapper import HhParser



@shared_task(name='scrapping_hh')
def scrapping_hh(language=None):
    hh_parser = HhParser()
    hh_parser.scrap(language)
