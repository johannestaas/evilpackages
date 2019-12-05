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

from .diff import save_diff
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
        '--out', '-o', dest='path', default='stats.json',
        help='output path, default: %(default)s',
    )
    subparser.add_argument(
        '--batch-size', '-b', type=int, default=100,
        help='number of concurrent requests, default: %(default)s',
    )
    subparser = subs.add_parser(
        'diff',
        help='diff the downloaded stats',
    )
    subparser.add_argument(
        '--in', '-i', dest='stats_path', default='stats.json',
        help='input path, default: %(default)s',
    )
    subparser.add_argument(
        '--out', '-o', dest='output_path', default='diff.json',
        help='output path, default: %(default)s',
    )
    subparser.add_argument(
        '--recent', '-r',
        choices=('last_month', 'last_week', 'last_day'), default='last_month',
        help='download stats by month/week/day, default: %(default)s',
    )
    subparser.add_argument(
        '--dist', '-d', dest='max_dist', type=int, default=2,
        help='maximum levenshtein distance, default: %(default)s',
    )
    subparser.add_argument(
        '--min-downloads', '-m', type=int, default=10000,
        help='minimum downloads of source package, default: %(default)s',
    )
    subparser.add_argument(
        '--min-name-len', '-n', type=int, default=5,
        help='minimum source package name length, default: %(default)s',
    )
    args = parser.parse_args()

    kwargs = vars(args)
    if args.cmd == 'stats':
        save_download_stats(**kwargs)
    elif args.cmd == 'diff':
        save_diff(**kwargs)
    else:
        parser.print_usage()
