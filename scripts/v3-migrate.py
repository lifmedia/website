#!/usr/bin/env python3
"""
Move an existing page onto the v3 design without touching its content or SEO.

What it changes:
  • adds css/v3.css + css/v3-skin.css at the end of <head> (nothing else in <head>)
  • <body> gets class="v3 v3-skin"
  • swaps the old #lif-hdr header and <footer class="lif-footer"> for the v3 ones
What it never changes: URL, <title>, meta, canonical, JSON-LD, body copy, forms.

Usage (repo root):  python3 scripts/v3-migrate.py cinematic-commercials events ...
       python3 scripts/v3-migrate.py --landing video-production-new-brunswick
--landing keeps the page's own minimal footer and turns the header action into
a tap-to-call (landing pages convert; they should not send people elsewhere).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HEADER = '''<div id="lif-hdr">
  <a href="{r}" class="hdr-logo" aria-label="LIF Media Home">
    <img class="logo-w" src="https://res.cloudinary.com/dsqbqhqvf/image/upload/f_auto,q_auto/v1775331352/Brand_lifmedia_white_logo_1_vdztdx.png" alt="LIF Media" width="200" height="80">
    <img class="logo-d" src="https://res.cloudinary.com/dsqbqhqvf/image/upload/f_auto,q_auto/v1775331346/Brand_lifmedia_logo_light_no_background_fb0qu9.png" alt="LIF Media" width="200" height="80">
  </a>
  <div class="hdr-right">
    <ul class="v3-nav">
      <li><a href="{r}portfolio/">Work</a></li>
      <li><a href="{r}about-us/">Studio</a></li>
      <li><a href="{r}blog/">Journal</a></li>
      <li><a href="{r}contact/" class="v3-nav__cta">Start a project</a></li>
    </ul>
    <button class="hdr-menu-btn" id="lifMenuBtn" aria-label="Open menu">
      <span>Menu</span>
      <span class="menu-lines"><span></span><span></span></span>
    </button>
  </div>
</div>

'''

FOOTER = '''<footer class="v3-footer">
  <div class="v3-wrap">
    <div class="v3-footer__top">
      <div class="v3-footer__brand">
        <a href="{r}" aria-label="LIF Media Home"><img src="https://res.cloudinary.com/dsqbqhqvf/image/upload/f_auto,q_auto/v1775331352/Brand_lifmedia_white_logo_1_vdztdx.png" alt="LIF Media" width="200" height="80" loading="lazy"></a>
        <p>Video studio in Moncton, New Brunswick.<br>Working across Atlantic Canada.</p>
      </div>
      <div class="v3-footer__reach">
        <span class="v3-footer__label">Start a project</span>
        <a class="v3-footer__mail" href="mailto:contact@lifmedia.ca">contact@lifmedia.ca</a>
        <a class="v3-footer__tel" href="tel:+15066887043" onclick="return gtag_report_conversion(\'tel:+15066887043\');">+1 (506) 688-7043</a>
        <span class="v3-footer__addr">21 Rue Foxtrot, Moncton, NB</span>
      </div>
    </div>
    <nav class="v3-footer__nav" aria-label="Footer">
      <div>
        <h5>Studio</h5>
        <ul>
          <li><a href="{r}portfolio/">Work</a></li>
          <li><a href="{r}about-us/">About</a></li>
          <li><a href="{r}blog/">Journal</a></li>
          <li><a href="{r}reviews/">Reviews</a></li>
          <li><a href="{r}contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <h5>Services</h5>
        <ul>
          <li><a href="{r}video-marketing/">Video Marketing</a></li>
          <li><a href="{r}cinematic-commercials/">Commercials</a></li>
          <li><a href="{r}documentaries-interviews/">Documentaries</a></li>
          <li><a href="{r}social-media/">Social Content</a></li>
          <li><a href="{r}events/">Event Films</a></li>
        </ul>
      </div>
      <div>
        <h5>Industries</h5>
        <ul>
          <li><a href="{r}industries/construction/">Construction</a></li>
          <li><a href="{r}industries/restaurants-hospitality/">Hospitality</a></li>
          <li><a href="{r}industries/government-political/">Government</a></li>
          <li><a href="{r}industries/real-estate/">Real Estate</a></li>
          <li><a href="{r}industries/">All industries</a></li>
        </ul>
      </div>
      <div>
        <h5>Follow</h5>
        <ul>
          <li><a href="https://www.instagram.com/lifmedia/" target="_blank" rel="noopener">Instagram</a></li>
          <li><a href="https://www.linkedin.com/company/lif-media/" target="_blank" rel="noopener">LinkedIn</a></li>
          <li><a href="https://www.tiktok.com/@lifmedia" target="_blank" rel="noopener">TikTok</a></li>
          <li><a href="https://www.facebook.com/lifmediaca/" target="_blank" rel="noopener">Facebook</a></li>
        </ul>
      </div>
    </nav>
    <div class="v3-footer__base">
      <p class="v3-footer__note">LIF Media operates a social media management platform that helps businesses schedule, manage, and publish content across their social media channels — including Facebook, Instagram, LinkedIn, and YouTube — on their behalf and with their authorization. Authorized users connect their accounts to plan and publish posts and videos from a single dashboard. <a href="{r}platform/">About the platform</a></p>
      <div class="v3-footer__legal"><span>&copy; 2026 LIF Media Inc.</span><span><a href="{r}privacy/">Privacy</a><a href="{r}terms/">Terms</a></span></div>
    </div>
  </div>
  <div class="v3-footer__mark" aria-hidden="true"><img src="https://res.cloudinary.com/dsqbqhqvf/image/upload/f_auto,q_auto/v1775331352/Brand_lifmedia_white_logo_1_vdztdx.png" alt="" width="200" height="80" loading="lazy"></div>
</footer>'''


LANDING_CTA = '<li><a href="tel:+15066887043" onclick="return gtag_report_conversion(\'tel:+15066887043\');" class="v3-nav__cta">Call (506) 688-7043</a></li>'


def migrate(page, landing=False):
    if page.endswith('.html'):
        # Root-level files like 404.html are served at any depth: use absolute links
        path, r = ROOT / page, '/'
    else:
        path = ROOT / page / 'index.html'
        r = '../' * len(Path(page).parts)
    s = path.read_text()
    if 'css/v3-skin.css' in s:
        return 'already migrated'

    head_before = s[:s.index('</head>')]
    s = s.replace('</head>', f'<link rel="stylesheet" href="{r}css/v3.css">\n<link rel="stylesheet" href="{r}css/v3-skin.css">\n</head>', 1)
    body_cls = 'v3 v3-skin v3-lp' if landing else 'v3 v3-skin'
    s, n = re.subn(r'<body[^>]*>', f'<body class="{body_cls}">', s, count=1)
    assert n == 1, 'no <body>'
    header = HEADER.format(r=r)
    if landing:
        header = re.sub(r'<li><a href="[^"]*contact/" class="v3-nav__cta">Start a project</a></li>', LANDING_CTA, header)
    s, n = re.subn(r'<div id="lif-hdr">.*?(?=(?:<!--[^>]*-->\s*)?<div id="lif-mob">)', header, s, count=1, flags=re.S)
    assert n == 1, 'header not found'
    if not landing:
        s, n = re.subn(r'<footer class="lif-footer">.*?</footer>', FOOTER.format(r=r), s, count=1, flags=re.S)
        assert n == 1, 'footer not found'
    # Guard: everything in <head> before our new links must be untouched
    assert s.startswith(head_before), 'head changed'
    path.write_text(s)
    return 'ok'


if __name__ == '__main__':
    args = sys.argv[1:]
    landing = '--landing' in args
    for p in (a for a in args if a != '--landing'):
        print(p.ljust(32), migrate(p.strip('/'), landing))
