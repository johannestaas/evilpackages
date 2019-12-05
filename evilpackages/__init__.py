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
        '--out', '-o', dest='output', default='stats.json',
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
        '--in', '-i', dest='input', default='stats.json',
        help='input path, default: %(default)s',
    )
    subparser.add_argument(
        '--out', '-o', dest='output', default='diff.json',
        help='output path, default: %(default)s',
    )
    subparser.add_argument(
        '--recent', '-r', choices=('month', 'week', 'day'), default='month',
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
    args = parser.parse_args()

    if args.cmd == 'stats':
        save_download_stats(path=args.output, batch_size=args.batch_size)
    elif args.cmd == 'diff':
        save_diff(
            stats_path=args.input,
            output_path=args.output,
            recent=f'last_{args.recent}',
            max_dist=args.max_dist,
            min_downloads=args.min_downloads,
        )
    else:
        parser.print_usage()
