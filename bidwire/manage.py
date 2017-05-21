from manager import Manager

import scraper
import notifier
import logging

from bid import Bid
from bidwire_settings import SITE_CONFIG
from db import Session
from document import Document


manager = Manager()


@manager.command
def scrape(site=''):
    """runs scraper for given <site>"""
    scraper.scrape(get_site_config(site))


@manager.command
def notify(site='', recipients=''):
    """runs notifier for given <site>, sending email to <recipient>"""
    site_config = get_site_config(
        site, [r.strip() for r in recipients.split(',')])
    notifier.send_new_notifications(site_config)


@manager.command
def dryrun(site='', recipients=''):
    """scrape/notify for given <site>, sending email to <recipient>"""
    scrape(site)
    notify(site, recipients)


def get_site_config(site_str, recipients=None):
    """Returns the default config dictionary for the given site string."""
    site_enum = to_site_enum(site_str)
    site_dict = SITE_CONFIG[site_enum]
    if recipients:
        site_dict['recipients'] = recipients
    return {site_enum: site_dict}


def to_site_enum(site_str):
    """Turns a string into a site Enum, or raises exception."""
    site = Bid.Site[site_str]
    if site:
        return site
    site = Document.Site[site_str]
    if site:
        return site
    raise ValueError("Couldn't find Site enum for {}".format(site_str))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    manager.main()
