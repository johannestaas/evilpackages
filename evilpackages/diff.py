import json
import logging
from collections import defaultdict

from Levenshtein import distance

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('evilpackages')


def compare_package_names(
    src_stats,
    recent='last_month',
    max_dist=2,
    min_downloads=10000,
):
    packages = [
        key for key in src_stats
        if src_stats[key] is not None
    ]
    stats = {
        pkg: src_stats[pkg][recent]
        for pkg in packages
    }
    possible_evil = defaultdict(list)
    for pkg in packages:
        if stats[pkg] < min_downloads:
            continue
        for evil in packages:
            if evil == pkg:
                continue
            if stats[evil] > stats[pkg]:
                # It won't have more downloads than a popular package...
                # hopefully.
                continue
            if distance(pkg, evil) > max_dist:
                # Assume that it will swap two chars or change one at most.
                continue
            possible_evil[pkg].append(evil)
    results = []
    for pkg, evils in possible_evil.items():
        results.append({
            'package': pkg,
            recent: stats[pkg],
            'suspicious': sorted(
                (
                    {'package': evil, recent: stats[evil]}
                    for evil in evils
                ),
                key=lambda x: x[recent],
                reverse=True,
            ),
        })
    return sorted(results, key=lambda x: x[recent], reverse=True)


def save_diff(
    stats_path='stats.json',
    output_path='diff.json',
    recent='last_month',
    max_dist=2,
    min_downloads=10000,
):
    with open(stats_path) as f:
        src_stats = json.load(f)
    results = compare_package_names(
        src_stats,
        recent=recent,
        max_dist=max_dist,
        min_downloads=min_downloads,
    )
    LOG.info('top 10:')
    for result in results[:10]:
        LOG.info(f'package {result["package"]}, {recent}: {result[recent]}')
        for evil in result['suspicious']:
            LOG.info(
                f'  (suspicious) {evil["package"]}, {recent}: {evil[recent]}'
            )
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)
    LOG.info(f'dumped to {output_path}')
