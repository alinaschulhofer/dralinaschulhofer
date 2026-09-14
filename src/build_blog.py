"""Builds the Blog section (blog.html index + one page per post) from JSON files in src/posts/.

Usage: python3 src/build_blog.py   (run from the repo root)

To add a post: drop a new src/posts/<slug>.json (see src/posts/README.md for the schema),
then re-run this script. It regenerates blog.html and every post page from scratch, so it's
safe to re-run any time — nothing here is hand-edited at the repo root.
"""
import json, pathlib, sys, datetime, html

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from common import DOMAIN, FONTS, NAV, SCRIPT, get_footer, CSS_LINK, GA_SCRIPT, VISITOR_LOGGER_SCRIPT, IMG_VERSION

POSTS_DIR = HERE / 'posts'
FOOTER = get_footer()


def load_posts():
    posts = []
    for fp in sorted(POSTS_DIR.glob('*.json')):
        data = json.loads(fp.read_text(encoding='utf-8'))
        required = ['slug', 'title', 'date', 'tag', 'excerpt', 'body']
        missing = [k for k in required if not data.get(k)]
        if missing:
            raise SystemExit(f'{fp.name}: missing required field(s): {", ".join(missing)}')
        posts.append(data)
    # newest first, by ISO date
    posts.sort(key=lambda p: p['date'], reverse=True)
    return posts


def human_date(iso):
    return datetime.date.fromisoformat(iso).strftime('%B %-d, %Y')


def page_shell(active, title, desc, canonical, body_html, extra_head=''):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{canonical}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{DOMAIN}/assets/portrait-about.jpg?v={IMG_VERSION}" />
<meta name="twitter:card" content="summary_large_image" />
{FONTS}
{CSS_LINK}
{extra_head}
{GA_SCRIPT}
</head>
<body>
{NAV(active)}
{body_html}
{FOOTER}
{SCRIPT}
{VISITOR_LOGGER_SCRIPT}
</body>
</html>'''


def render_card(post):
    return f'''      <a href="{post['slug']}.html" class="blog-card">
        <div class="blog-meta">
          <span class="blog-tag">{html.escape(post['tag'])}</span>
          <span class="blog-date">{human_date(post['date'])}</span>
        </div>
        <h2 class="blog-title">{html.escape(post['title'])}</h2>
        <p class="blog-excerpt">{html.escape(post['excerpt'])}</p>
        <span class="blog-read">Read →</span>
      </a>'''


def render_index(posts):
    if posts:
        grid = '\n'.join(render_card(p) for p in posts)
        grid_html = f'    <div class="blog-grid">\n{grid}\n    </div>'
    else:
        grid_html = '    <p class="blog-empty">New reflections are on their way — check back soon.</p>'

    body = f'''<section class="pg-hero">
  <img class="th-hero-img" src="assets/portrait-about.jpg?v={IMG_VERSION}" alt="" />
  <div class="container">
    <h1>Where Excellence Meets Wellbeing</h1>
    <p class="sub">Insights at the Intersection of Psychology, Relationships, Leadership, and Organizational Behavior</p>
  </div>
</section>
<section class="section" style="padding-top:14px;">
  <div class="container">
{grid_html}
  </div>
</section>
<section class="excellence-band">
  <div class="xb-photo"><img src="assets/portrait-about.jpg?v={IMG_VERSION}" alt="Dr. Alina Schulhofer, founder of Architecture of Excellence" /></div>
  <div class="xb-text">
    <h2>For Those Who Demand Excellence.</h2>
    <a href="index.html#contact" class="eh-btn">Begin the Conversation</a>
  </div>
</section>'''
    title = 'Psychology, Leadership & Performance Insights | Dr. Schulhofer'
    desc = 'Insights at the intersection of psychology, relationships, leadership, and organizational behavior, from Dr. Alina Schulhofer.'
    canon = DOMAIN + '/blog.html'
    breadcrumb = f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{DOMAIN}/"}},{{"@type":"ListItem","position":2,"name":"Insights","item":"{canon}"}}]}}
</script>'''
    return page_shell('blog', title, desc, canon, body, extra_head=breadcrumb)


def render_post(post):
    paragraphs = '\n      '.join(post['body'])
    body = f'''<section class="pg-head">
  <div class="container narrow">
    <a href="blog.html" class="article-back">← All Posts</a>
    <div class="blog-meta">
      <span class="blog-tag">{html.escape(post['tag'])}</span>
      <span class="blog-date">{human_date(post['date'])}</span>
    </div>
    <h1>{html.escape(post['title'])}</h1>
    {f'<p class="sub">{html.escape(post["subtitle"])}</p>' if post.get('subtitle') else ''}
    <p class="blog-author">By Dr. Alina Schulhofer</p>
  </div>
</section>
<section class="section" style="padding:14px 0 0;">
  <div class="container narrow prose">
    <hr class="divider-full" style="margin-top:10px;margin-bottom:44px;" />
      {paragraphs}
    <hr class="divider-full" style="margin-top:40px;margin-bottom:0;" />
  </div>
</section>
<section class="contact-band">
  <div class="container">
    <h2>Ready to Begin?</h2>
    <p>Book a free 15-minute consultation to see if working together is the right fit.</p>
    <a href="index.html#contact">Book a Free Consultation</a>
  </div>
</section>'''
    title = f'{html.escape(post["title"])} — Dr. Alina Schulhofer'
    desc = html.escape(post['excerpt'])
    canon = f'{DOMAIN}/{post["slug"]}.html'
    ldjson = f'''<meta name="author" content="Dr. Alina Schulhofer" />
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BlogPosting","headline":{json.dumps(post['title'])},"description":{json.dumps(post['excerpt'])},"datePublished":"{post['date']}","url":"{canon}","image":"{DOMAIN}/assets/portrait-about.jpg","author":{{"@type":"Person","name":"Dr. Alina Schulhofer"}},"publisher":{{"@type":"Person","name":"Dr. Alina Schulhofer"}}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{DOMAIN}/"}},{{"@type":"ListItem","position":2,"name":"Insights","item":"{DOMAIN}/blog.html"}},{{"@type":"ListItem","position":3,"name":{json.dumps(post['title'])},"item":"{canon}"}}]}}
</script>'''
    return page_shell('blog', title, desc, canon, body, extra_head=ldjson)


def main():
    posts = load_posts()
    (ROOT / 'blog.html').write_text(render_index(posts), encoding='utf-8')
    print('wrote blog.html')
    for post in posts:
        fn = f'{post["slug"]}.html'
        (ROOT / fn).write_text(render_post(post), encoding='utf-8')
        print('wrote', fn)
    print(f'{len(posts)} post(s)')


if __name__ == '__main__':
    main()
