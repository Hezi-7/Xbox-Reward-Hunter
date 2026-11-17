"""Public promotion discovery. Results are leads, NOT verified redeemable codes."""
import json, re, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

QUERIES = [
    'Xbox gift card giveaway official',
    'Microsoft Rewards Xbox gift card promotion',
    'site:news.xbox.com Xbox rewards promotion',
    'site:microsoft.com Microsoft Rewards Xbox gift card',
]
OFFICIAL = ('microsoft.com', 'xbox.com', 'news.xbox.com', 'rewards.bing.com')
OUT = Path(__file__).parent / 'docs' / 'offers.json'

def discover(query):
    url = 'https://news.google.com/rss/search?' + urllib.parse.urlencode({'q': query, 'hl': 'en-US', 'gl': 'US', 'ceid': 'US:en'})
    req = urllib.request.Request(url, headers={'User-Agent': 'XboxRewardHunter/2.0 (public RSS discovery)'})
    with urllib.request.urlopen(req, timeout=20) as res:
        root = ET.fromstring(res.read(2_000_000))
    for item in root.findall('./channel/item'):
        title = item.findtext('title', '').strip()
        link = item.findtext('link', '').strip()
        source = item.findtext('source', '').strip()
        date = item.findtext('pubDate', '').strip()
        if not title or not link or not link.startswith('https://'):
            continue
        if not any(term in title.lower() for term in ('xbox', 'microsoft rewards', 'gift card')):
            continue
        try:
            dt = parsedate_to_datetime(date).astimezone(timezone.utc).isoformat()
        except (TypeError, ValueError):
            dt = None
        domain = urllib.parse.urlparse(item.findtext('source', '') or '').hostname or ''
        # The RSS source label is informative only; not proof of authenticity.
        official_source = any(source.lower() == d or source.lower().endswith('.' + d) for d in OFFICIAL)
        yield {'title': title[:250], 'url': link, 'source': source[:100], 'published': dt,
               'category': 'Official-source lead' if official_source else 'Unverified lead',
               'note': 'Check original publisher, eligibility, expiration, and redemption terms.'}

def main():
    items, errors = {}, []
    for query in QUERIES:
        try:
            for item in discover(query):
                items.setdefault(item['url'], item)
        except Exception as exc:
            errors.append(f'{query}: {type(exc).__name__}: {exc}')
    if not items:
        raise RuntimeError('No feeds returned qualifying items; preserving previous results. ' + '; '.join(errors))
    previous = []
    if OUT.exists():
        try:
            previous = json.loads(OUT.read_text(encoding='utf-8')).get('offers', [])
        except (ValueError, OSError, AttributeError):
            pass
    for item in previous:
        if isinstance(item, dict) and item.get('url'):
            items.setdefault(item['url'], item)
    offers = sorted(items.values(), key=lambda x: x.get('published') or '', reverse=True)[:150]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({'last_scan_utc': datetime.now(timezone.utc).isoformat(),
                               'offers': offers, 'scan_warnings': errors}, indent=2), encoding='utf-8')
    print(f'Saved {len(offers)} candidate articles; warnings: {len(errors)}')

if __name__ == '__main__':
    main()
