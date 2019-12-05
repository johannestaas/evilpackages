'''
evilpackages

Detect possible malicious pypi packages
'''

__title__ = 'evilpackages'
__version__ = '0.0.1'
__all__ = ()
__author__ = 'Johan Nestaas <johannestaas@gmail.com'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2019 Johan Nestaas'

from .pypi_stats import save_download_stats


def main():
    import argparse
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='cmd')
    subparser = subs.add_parser(
        'stats',
        help='download stats for all packages',
    )
    subparser.add_argument(
        '--out', '-o', default='stats.json',
        help='output path, default: %(default)s',
    )
    subparser.add_argument(
        '--batch-size', '-b', type=int, default=100,
        help='number of concurrent requests, default: %(default)s',
    )
    args = parser.parse_args()

    if args.cmd == 'stats':
        save_download_stats(path=args.out, batch_size=args.batch_size)
    elif args.cmd == 'diff':
        raise NotImplementedError('todo')
    else:
        parser.print_usage()
