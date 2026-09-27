#!/usr/bin/env python3
"""
Build the indexable city landing pages (/video-production-<city>/) from the
New Brunswick landing page template.

The template (video-production-new-brunswick/index.html) is the Google Ads LP
and stays noindex. Each city page is a general LIF Media brochure with its own
title, meta, headline, local section, FAQ answer and schema, and IS indexed.
City pages are intentionally not linked from the header or footer; the homepage
"Where We Work" map links to them.

Usage (from the repo root):
    python3 scripts/build-city-pages.py

Re-run after editing CITIES below or the template. Add new URLs to sitemap.xml.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / 'video-production-new-brunswick' / 'index.html'
SITE = 'https://www.lifmedia.ca'

FR_LINE = 'Nous réalisons vos vidéos en français, en anglais ou dans les deux langues.'

CITIES = [
    {
        'slug': 'moncton', 'name': 'Moncton',
        'description': 'Video production in Moncton, NB. LIF Media creates cinematic commercials, social media content, brand documentaries and event films for Greater Moncton.',
        'sub': 'Moncton is home. Commercials, social content, brand films &amp; event coverage for businesses across Greater Moncton.',
        'local_title': 'Moncton is <em>home base</em>',
        'p1': 'LIF Media is based at 21 Rue Foxtrot in Moncton. Being local means easy site visits before production day and a crew that already knows the city&rsquo;s venues, neighbourhoods and people.',
        'p2': 'Whether it&rsquo;s a downtown storefront, a production floor in the industrial park or a conference in the Hub City, we produce commercials, social content, brand documentaries and event films that help Moncton businesses grow.',
        'distance': 'Home base', 'languages': 'English, French &amp; Spanish', 'nearby': 'Dieppe, Riverview, Shediac, Salisbury',
        'faq_q': 'Do you work outside of Moncton?',
        'faq_a': 'Yes. We&rsquo;re based in Moncton and work across Greater Moncton &mdash; Dieppe, Riverview and Shediac &mdash; plus the rest of New Brunswick and Atlantic Canada.',
    },
    {
        'slug': 'dieppe', 'name': 'Dieppe',
        'description': 'Bilingual video production in Dieppe, NB. LIF Media films commercials, social media content, brand documentaries and event films in French and English.',
        'sub': 'Bilingual video production for Dieppe businesses &mdash; commercials, social content, brand films &amp; event coverage, minutes from our Moncton base.',
        'local_title': 'Dieppe, <em>en français</em> and in English',
        'p1': 'Dieppe sits right next door to our Moncton base, about ten minutes away. It&rsquo;s a growing, proudly francophone city, so we plan scripts, interviews and captions in the language your audience actually speaks.',
        'p2': 'From retail and restaurants to the businesses around the Greater Moncton Rom&eacute;o LeBlanc International Airport, we help Dieppe brands show up with video that feels local and looks cinematic.',
        'fr': True,
        'distance': 'About 10 minutes', 'languages': 'French &amp; English', 'nearby': 'Moncton, Memramcook, Shediac',
        'faq_q': 'Do you come to Dieppe?',
        'faq_a': 'Yes. Dieppe is about 10 minutes from our Moncton base, so on-site meetings and shoots are easy to schedule. We film in French, English or both.',
    },
    {
        'slug': 'riverview', 'name': 'Riverview',
        'description': 'Video production in Riverview, NB. LIF Media makes commercials, social media content and brand films for local businesses, just across the river from Moncton.',
        'sub': 'Video production for Riverview businesses &mdash; just across the Petitcodiac from our Moncton base.',
        'local_title': 'Riverview, <em>right across the river</em>',
        'p1': 'Riverview is just across the Petitcodiac River from our Moncton base, about ten minutes away. That makes it easy to scout locations, meet in person and plan shoots around your hours.',
        'p2': 'We help Riverview businesses, clinics, trades and community organizations tell their story with commercials, social content and brand documentaries made for the people who live and work here.',
        'distance': 'About 10 minutes', 'languages': 'English &amp; French', 'nearby': 'Moncton, Dieppe, Hillsborough',
        'faq_q': 'Do you come to Riverview?',
        'faq_a': 'Yes. Riverview is about 10 minutes from our Moncton base. We regularly meet clients on site and schedule shoots around your business hours.',
    },
    {
        'slug': 'fredericton', 'name': 'Fredericton',
        'description': 'Video production in Fredericton, NB. LIF Media produces commercials, social content, brand documentaries and event films for the capital region.',
        'sub': 'Video production for Fredericton businesses, institutions and organizations &mdash; commercials, social content, brand films &amp; event coverage.',
        'local_title': 'Fredericton, the <em>capital</em>',
        'p1': 'Fredericton is New Brunswick&rsquo;s capital, home to government, universities, research and a growing tech sector. It&rsquo;s about two hours from our Moncton base, so we plan Fredericton productions around focused, efficient shoot days.',
        'p2': 'Conferences, research stories, public-sector campaigns and brand films for local businesses: we bring a cinematic crew to the capital region and deliver content that&rsquo;s ready to publish.',
        'distance': 'About 2 hours', 'languages': 'English &amp; French', 'nearby': 'Oromocto, New Maryland, Hanwell',
        'faq_q': 'Do you travel to Fredericton?',
        'faq_a': 'Yes. Fredericton is about two hours from our Moncton base. We plan the shoot in advance so everything you need is captured in as few production days as possible.',
    },
    {
        'slug': 'saint-john', 'name': 'Saint John',
        'description': 'Video production in Saint John, NB. LIF Media creates commercials, social content, brand documentaries and event films for businesses in the port city.',
        'sub': 'Video production for Saint John businesses &mdash; cinematic commercials, social content, brand films &amp; event coverage for the port city.',
        'local_title': 'Saint John, the <em>port city</em>',
        'p1': 'Saint John is New Brunswick&rsquo;s port city on the Bay of Fundy, with a strong industrial and energy base and a busy Uptown. It&rsquo;s about an hour and a half from our Moncton base.',
        'p2': 'From industrial and construction sites to Uptown restaurants and events, we film efficiently on location and turn one production day into a library of content.',
        'distance': 'About 1.5 hours', 'languages': 'English &amp; French', 'nearby': 'Quispamsis, Rothesay, Grand Bay-Westfield',
        'faq_q': 'Do you travel to Saint John?',
        'faq_a': 'Yes. Saint John is about an hour and a half from our Moncton base, and we film there regularly for commercial, industrial and event clients.',
    },
    {
        'slug': 'miramichi', 'name': 'Miramichi',
        'description': 'Video production in Miramichi, NB. LIF Media produces commercials, social media content, brand documentaries and event films for Miramichi organizations.',
        'sub': 'Video production for Miramichi businesses and organizations &mdash; commercials, social content, brand films &amp; event coverage.',
        'local_title': 'Miramichi, <em>on the river</em>',
        'p1': 'Miramichi is built along one of the world&rsquo;s best-known Atlantic salmon rivers, with deep roots in forestry, fishing and tourism. It&rsquo;s about an hour and a half north of our Moncton base.',
        'p2': 'We help Miramichi businesses, outfitters, festivals and community organizations share their story with video that captures the place as much as the people.',
        'distance': 'About 1.5 hours', 'languages': 'English &amp; French', 'nearby': 'Neguac, Rogersville, Blackville',
        'faq_q': 'Do you travel to Miramichi?',
        'faq_a': 'Yes. Miramichi is about an hour and a half from our Moncton base. We plan the shoot ahead of time so your production day runs smoothly.',
    },
    {
        'slug': 'bathurst', 'name': 'Bathurst',
        'description': 'Bilingual video production in Bathurst, NB and the Chaleur region. LIF Media films commercials, social media content, brand documentaries and event films.',
        'sub': 'Bilingual video production for Bathurst and the Chaleur region &mdash; commercials, social content, brand films &amp; event coverage.',
        'local_title': 'Bathurst and the <em>Chaleur</em> region',
        'p1': 'Bathurst sits on the Baie des Chaleurs in northern New Brunswick, a bilingual region with roots in mining, forestry and tourism. It&rsquo;s about two and a half hours from our Moncton base.',
        'p2': 'We plan northern productions around focused shoot days, so your team gets commercials, social content and brand films without disrupting operations.',
        'fr': True,
        'distance': 'About 2.5 hours', 'languages': 'French &amp; English', 'nearby': 'Beresford, Petit-Rocher, Caraquet',
        'faq_q': 'Do you travel to Bathurst?',
        'faq_a': 'Yes. Bathurst is about two and a half hours from our Moncton base. We schedule northern shoots carefully and film in French, English or both.',
    },
    {
        'slug': 'edmundston', 'name': 'Edmundston',
        'description': 'Video production in Edmundston, NB, in French and English. LIF Media creates commercials, social content, brand documentaries and event films for Madawaska.',
        'sub': 'Video production in French and English for Edmundston businesses &mdash; commercials, social content, brand films &amp; event coverage.',
        'local_title': 'Edmundston, <em>en fran&ccedil;ais</em>',
        'p1': 'Edmundston is the heart of the Madawaska region, a francophone city on the borders of Quebec and Maine. It&rsquo;s our longest trip in the province, about four and a half hours from Moncton, so we plan every shoot carefully and make each production day count.',
        'p2': 'We produce French, English and bilingual video for Edmundston businesses, institutions and events, with scripts and captions written for your audience.',
        'fr': True,
        'distance': 'About 4.5 hours', 'languages': 'French &amp; English', 'nearby': 'Grand Falls, Saint-L&eacute;onard, Saint-Jacques',
        'faq_q': 'Do you travel to Edmundston?',
        'faq_a': 'Yes. Edmundston is about four and a half hours from our Moncton base, so we plan the full production in advance and capture everything in focused shoot days.',
    },
    {
        'slug': 'shediac', 'name': 'Shediac',
        'description': 'Video production in Shediac, NB. LIF Media creates social media content, commercials and event films for restaurants, tourism and local businesses by the shore.',
        'sub': 'Video production for Shediac businesses &mdash; hospitality, tourism and local brands, about 25 minutes from our Moncton base.',
        'local_title': 'Shediac, <em>by the shore</em>',
        'p1': 'Shediac calls itself the Lobster Capital of the World. It&rsquo;s home to Parlee Beach and one of the busiest summer seasons in the province, about 25 minutes from our Moncton base.',
        'p2': 'We help restaurants, resorts, tourism operators and local businesses capture the season with social content and commercials that bring people to the shore.',
        'fr': True,
        'distance': 'About 25 minutes', 'languages': 'French &amp; English', 'nearby': 'Cap-Pel&eacute;, Grande-Digue, Bouctouche',
        'faq_q': 'Do you come to Shediac?',
        'faq_a': 'Yes. Shediac is about 25 minutes from our Moncton base. For seasonal businesses, we recommend planning shoots before and during the summer rush.',
    },
    {
        'slug': 'sussex', 'name': 'Sussex',
        'description': 'Video production in Sussex, NB. LIF Media produces commercials, social media content, brand documentaries and event films for Sussex and Kings County businesses.',
        'sub': 'Video production for Sussex businesses &mdash; commercials, social content, brand films &amp; event coverage for Kings County.',
        'local_title': 'Sussex and <em>Kings County</em>',
        'p1': 'Sussex is known for its dairy farms, covered bridges and the Atlantic Balloon Fiesta. It sits about 50 minutes from our Moncton base, halfway to Saint John.',
        'p2': 'From farms and agri-food producers to local shops and summer events, we film Sussex stories with care and deliver content ready for every platform.',
        'distance': 'About 50 minutes', 'languages': 'English &amp; French', 'nearby': 'Petitcodiac, Norton, Hampton',
        'faq_q': 'Do you travel to Sussex?',
        'faq_a': 'Yes. Sussex is about 50 minutes from our Moncton base, an easy trip for site visits and shoot days anywhere in Kings County.',
    },
    {
        'slug': 'sackville', 'name': 'Sackville',
        'description': 'Video production in Sackville, NB. LIF Media creates event films, interviews, social media content and commercials for businesses and organizations in Tantramar.',
        'sub': 'Video production for Sackville businesses and the Tantramar region &mdash; commercials, social content, brand films &amp; event coverage.',
        'local_title': 'Sackville and the <em>Tantramar</em>',
        'p1': 'Sackville is a university town on the Tantramar Marshes, home to Mount Allison University and a lively arts scene. It&rsquo;s about 40 minutes from our Moncton base, close to the Nova Scotia border.',
        'p2': 'We help local businesses, cultural organizations and campus events produce event films, interviews and social content that reach audiences well beyond town.',
        'distance': 'About 40 minutes', 'languages': 'English &amp; French', 'nearby': 'Dorchester, Memramcook, Amherst (NS)',
        'faq_q': 'Do you travel to Sackville?',
        'faq_a': 'Yes. Sackville is about 40 minutes from our Moncton base, and we also cover nearby communities in the Tantramar region and across the Nova Scotia border.',
    },
]

LOCAL_CSS = '''
/* ── City page: local section ── */
.lp-local { background: var(--off-white); }
.lp-local__grid { display: grid; gap: 40px; }
.lp-local p { font-size: 1rem; line-height: 1.8; color: var(--lp-gray); margin-top: 16px; max-width: 600px; }
.lp-local .lp-local__fr { font-family: var(--font-accent); font-style: italic; color: var(--deep-olive); font-size: 1.1rem; }
.lp-local__facts { display: grid; gap: 0; align-self: start; border-top: 1px solid rgba(26,26,26,0.1); }
.lp-local__facts div { padding: 18px 0; border-bottom: 1px solid rgba(26,26,26,0.1); }
.lp-local__facts dt { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; color: var(--terracotta); margin-bottom: 6px; }
.lp-local__facts dd { font-family: var(--font-accent); font-size: 1.25rem; color: var(--obsidian); }
.lp-local__more { margin-top: 48px; display: flex; flex-wrap: wrap; align-items: center; gap: 8px 10px; font-size: 0.85rem; }
.lp-local__more span { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; color: var(--lp-gray); margin-right: 6px; }
.lp-local__more a { padding: 6px 14px; border: 1px solid rgba(66,104,46,0.25); border-radius: 9999px; color: var(--deep-olive); transition: background 0.3s, color 0.3s; }
.lp-local__more a:hover { background: var(--deep-olive); color: #fff; }
@media (min-width: 760px) { .lp-local__grid { grid-template-columns: 1.4fr 1fr; gap: 72px; } }
'''


def plain(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s))


def sub1(pattern, repl, text):
    new, n = re.subn(pattern, lambda m: repl, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('Template marker not found: ' + pattern)
    return new


def build(city, template):
    slug, name = city['slug'], city['name']
    url = f'{SITE}/video-production-{slug}/'
    title = f'Video Production {name} NB | LIF Media'
    desc = city['description']
    t = template

    t = sub1(r'<!-- Standalone Google Ads landing page.*?-->\n<meta name="robots" content="noindex, follow">',
             f'<!-- City landing page (indexed, in sitemap.xml). Generated by scripts/build-city-pages.py — edit there. -->\n<meta name="robots" content="index, follow">', t)
    t = sub1(r'<title>.*?</title>', f'<title>{title}</title>', t)
    t = sub1(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', t)
    t = sub1(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', t)
    t = sub1(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', t)
    t = sub1(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', t)
    t = sub1(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', t)
    t = sub1(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">', t)
    t = sub1(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{desc}">', t)

    t = sub1(r'<div class="lp-eyebrow">[^<]*</div>', f'<div class="lp-eyebrow">Video Production &middot; {name}, NB</div>', t)
    t = sub1(r'<h1 data-swap="headline">.*?</h1>', f'<h1 data-swap="headline">Video Production in <em>{name}</em>, New Brunswick</h1>', t)
    t = sub1(r'(<p class="lp-hero__sub" data-swap="subheadline">).*?(</p>)', f'<p class="lp-hero__sub" data-swap="subheadline">\n        {city["sub"]}\n      </p>', t)
    t = sub1(r'<summary>Do you work outside of Moncton\?</summary>', f'<summary>{city["faq_q"]}</summary>', t)
    t = sub1(r'(<div class="lp-faq__answer" data-swap="geo-faq">).*?(</div>)', f'<div class="lp-faq__answer" data-swap="geo-faq">{city["faq_a"]}</div>', t)
    location = 'Moncton, New Brunswick, Canada' if slug == 'moncton' else f'Serving {name}, New Brunswick &middot; Based in Moncton'
    t = sub1(r'<span data-swap="footer-location">[^<]*</span>', f'<span data-swap="footer-location">{location}</span>', t)
    t = sub1(r"LEAD_SOURCE: '[^']*'", f"LEAD_SOURCE: 'City page: video-production-{slug}'", t)

    # Local section, right after the value proposition
    others = ''.join(f'\n      <a href="../video-production-{c["slug"]}/">{c["name"]}</a>' for c in CITIES if c['slug'] != slug)
    fr = f'\n      <p class="lp-local__fr" lang="fr">{FR_LINE}</p>' if city.get('fr') else ''
    local = f'''<!-- ════════════ 3b. LOCAL — {name} ════════════ -->
<section class="lp-section lp-local">
  <div class="lp-section__inner lp-local__grid">
    <div>
      <div class="lp-section__label">Working in {name}</div>
      <h2 class="lp-section__title">{city["local_title"]}</h2>
      <p>{city["p1"]}</p>
      <p>{city["p2"]}</p>{fr}
    </div>
    <dl class="lp-local__facts">
      <div><dt>From our Moncton base</dt><dd>{city["distance"]}</dd></div>
      <div><dt>We film in</dt><dd>{city["languages"]}</dd></div>
      <div><dt>Also nearby</dt><dd>{city["nearby"]}</dd></div>
    </dl>
  </div>
  <div class="lp-section__inner lp-local__more">
    <span>Also serving</span>{others}
  </div>
</section>

<!-- ════════════ 4. RECENT WORK'''
    t = sub1(r'<!-- ════════════ 4\. RECENT WORK', local, t)

    # Schema: service in this city, breadcrumb, FAQ
    faqs = re.findall(r'<summary>(.*?)</summary>\s*<div class="lp-faq__answer"[^>]*>(.*?)</div>', t, re.S)
    schema = [
        {
            '@context': 'https://schema.org', '@type': 'Service',
            'name': f'Video Production in {name}, NB', 'serviceType': 'Video Production', 'url': url,
            'description': desc,
            'provider': {'@type': 'VideoProductionCompany', '@id': f'{SITE}/#business', 'name': 'LIF Media',
                         'url': SITE, 'telephone': '+1-506-688-7043'},
            'areaServed': {'@type': 'City', 'name': name,
                           'containedInPlace': {'@type': 'AdministrativeArea', 'name': 'New Brunswick'}},
        },
        {
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': f'{SITE}/'},
                {'@type': 'ListItem', 'position': 2, 'name': f'Video Production {name}', 'item': url},
            ],
        },
        {
            '@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': plain(q),
                            'acceptedAnswer': {'@type': 'Answer', 'text': plain(a)}} for q, a in faqs],
        },
    ]
    ld = ''.join(f'<script type="application/ld+json">\n{json.dumps(s, indent=2, ensure_ascii=False)}\n</script>\n' for s in schema)
    t = sub1(r'\n<style>', '\n' + ld + '\n<style>', t)
    t = sub1(r'\n</style>\n(?=(?:<link[^>]*>\n)*</head>)', LOCAL_CSS + '</style>\n', t)
    return t


def main():
    template = TEMPLATE.read_text()
    for city in CITIES:
        n = len(html.unescape(city['description']))
        if not 140 <= n <= 165:
            print(f'  ! {city["slug"]}: meta description is {n} chars')
        out = ROOT / f'video-production-{city["slug"]}' / 'index.html'
        out.parent.mkdir(exist_ok=True)
        out.write_text(build(city, template))
        print(f'✓ /video-production-{city["slug"]}/')


if __name__ == '__main__':
    main()
