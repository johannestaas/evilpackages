import re
import json
import logging

import grequests
import requests
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO, filename='evilpackages.log')
LOG = logging.getLogger('evilpackages')

RE_PACKAGE_NAME = re.compile(r'/simple/([^/]+)')


def get_package_list():
    LOG.info('getting package list...')
    packages = []
    soup = BeautifulSoup(requests.get('https://pypi.org/simple/').text)
    for link in soup.find_all('a'):
        href = link.attrs['href']
        packages.append(RE_PACKAGE_NAME.match(href).group(1))
    return packages


def get_recent_downloads(package):
    """
    Returns dict like::

        {'last_day': 36702, 'last_month': 751456, 'last_week': 177635}

    """
    LOG.info(f'getting download stats for {package}')
    data = requests.get(
        f'https://pypistats.org/api/packages/{package}/recent'
    ).json()
    if data == 404:
        return None
    return data['data']


def get_recent_downloads_for_batch(packages):
    urls = [
        f'https://pypistats.org/api/packages/{package}/recent'
        for package in packages
    ]
    responses = grequests.map(grequests.get(url) for url in urls)
    data = {}
    for i, response in enumerate(responses):
        pkg = packages[i]
        response_data = response.json()
        if response_data == 404:
            data[pkg] = None
        else:
            data[pkg] = response_data['data']
    return data


def batch_list(lst, size=100):
    batch = []
    for item in lst:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def get_all_download_stats():
    packages = get_package_list()
    stats = {}
    total = len(packages)
    handled = 0
    try:
        for batch in batch_list(packages):
            LOG.info(f'{handled}/{total} ({handled / total:.2%})')
            download_stats = get_recent_downloads_for_batch(batch)
            stats.update(download_stats)
            handled += len(batch)
    except KeyboardInterrupt:
        LOG.debug(f'stats: {stats!r}')
    return stats


def save_download_stats():
    stats = get_all_download_stats()
    with open('stats.json', 'w') as f:
        json.dump(stats, f, indent=4)
    LOG.info('dumped to stats.json')
