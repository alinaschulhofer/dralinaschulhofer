import re, pathlib, sys, html, json
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent  # deploy files live at repo root; master source lives in src/
sys.path.insert(0, str(HERE))
from common import DOMAIN, FONTS, NAV, SCRIPT, CSS_LINK, GA_SCRIPT, VISITOR_LOGGER_SCRIPT, IMG_VERSION, FAVICON, NOSCRIPT_FALLBACK, FAB_BOOK, IAG_POPUP, CAL_SCRIPT, CAL_FREE_CONSULT_SLUG, CAL_INTAKE_SLUG, CAL_INTENSIVE_SLUG, CAL_ALL_URL, cal_book_attrs
from build_blog import load_posts, human_date
src=open(HERE/'therapy_template.html',encoding='utf-8').read()

# --- 1. extract <style> content, drop embedded base64 @font-face (we use Google Fonts) ---
style=re.search(r'<style>(.*?)</style>', src, re.S).group(1)
style_lines=[ln for ln in style.split('\n') if 'base64,__' not in ln]
css="\n".join(style_lines).strip()
open(ROOT/'styles.css','w',encoding='utf-8').write(css)

# --- 2. body content ---
body=re.search(r'<body>(.*?)</body>', src, re.S).group(1)
# swap embedded image data-uris for asset files (?v= busts Safari's aggressive image cache)
body=body.replace('data:image/jpeg;base64,__PABOUT__',f'assets/portrait-about.jpg?v={IMG_VERSION}')
body=body.replace('data:image/jpeg;base64,__PCIRCLE__',f'assets/portrait-circle.jpg?v={IMG_VERSION}')
body=body.replace('data:image/jpeg;base64,__FACE__',f'assets/face.jpg?v={IMG_VERSION}')
body=body.replace('data:image/jpeg;base64,__PPHIL__',f'assets/about-hero-photo.jpg?v={IMG_VERSION}')
body=body.replace('data:image/jpeg;base64,__THERAPYPHIL__',f'assets/therapy-philosophy-photo.jpg?v={IMG_VERSION}')
body=body.replace('data:image/jpeg;base64,__THERAPYHERO__',f'assets/therapy-hero-photo.jpg?v={IMG_VERSION}')
body=body.replace('data:image/jpeg;base64,__ABOUTHERO__',f'assets/philosophy-photo.jpg?v={IMG_VERSION}')

# extract each page's inner content
def page_inner(pid):
    m=re.search(r'<div class="page[^"]*" id="'+pid+r'">(.*?)</div>\s*(?=<!-- =+ |<footer>)', body, re.S)
    return m.group(1).strip()
pages={pid:page_inner(pid) for pid in ['home','about','services','faq']}

# homepage — inject the newest blog post into the featured-post teaser
posts=load_posts()
if posts:
    latest=posts[0]  # load_posts() sorts newest-first by date
    fp_html=f'''<p class="fp-kicker">From the Blog</p>
      <p class="fp-meta"><span class="fp-tag">{html.escape(latest['tag'])}</span>{human_date(latest['date'])}</p>
      <h2><a href="{latest['slug']}.html">{html.escape(latest['title'])}</a></h2>
      <p class="fp-excerpt">{html.escape(latest['excerpt'])}</p>
      <a href="{latest['slug']}.html" class="fp-link">Read the Full Post <span class="arrow">&rarr;</span></a>'''
    pages['home']=pages['home'].replace('<!-- __FEATURED_POST__ -->', fp_html)

# footer
footer='<footer>'+re.search(r'<footer>(.*?)</footer>', body, re.S).group(1)+'</footer>'

JSONLD='''<script type="application/ld+json">
{"@context":"https://schema.org","@type":["Psychologist","MedicalBusiness"],"name":"Dr. Alina Schulhofer — Concierge Psychological Services","description":"Depth-oriented virtual psychotherapy for high achievers — executives, entrepreneurs, creatives, founders, high-net-worth individuals, high-profile clients, and professional athletes. Licensed clinical psychologist in Florida and New York.","url":"https://www.dralinaschulhofer.com","telephone":"+1-786-671-4945","email":"alina@dralinaschulhofer.com","areaServed":[{"@type":"State","name":"Florida"},{"@type":"State","name":"New York"}],"availableService":[{"@type":"MedicalTherapy","name":"Individual Therapy"},{"@type":"MedicalTherapy","name":"Couples & Family Therapy"},{"@type":"MedicalTherapy","name":"Therapy Intensives"}],"founder":{"@type":"Person","name":"Dr. Alina Schulhofer","jobTitle":"Licensed Clinical Psychologist (PsyD)","alumniOf":"Nova Southeastern University"},"knowsAbout":["Psychotherapy","Trauma","Personality","Relationships","High Performance Psychology","Executive Wellbeing","High-Net-Worth Individuals"],"sameAs":["https://architectureofexcellence.com"]}
</script>'''

def breadcrumb(name, canon):
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{DOMAIN}/"}},{{"@type":"ListItem","position":2,"name":"{name}","item":"{canon}"}}]}}
</script>'''

PERSON_LDJSON='''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Person","name":"Dr. Alina Schulhofer","jobTitle":"Licensed Clinical Psychologist (PsyD)","alumniOf":"Nova Southeastern University","url":"https://www.dralinaschulhofer.com/about.html","image":"https://www.dralinaschulhofer.com/assets/portrait-about.jpg","worksFor":[{"@type":"MedicalBusiness","name":"Dr. Alina Schulhofer — Concierge Psychological Services"},{"@type":"Organization","name":"Architecture of Excellence","url":"https://architectureofexcellence.com"}],"knowsAbout":["Psychotherapy","Trauma","Relationships","High Performance Psychology","Executive Coaching","High-Net-Worth Individuals"]}
</script>'''

SERVICE_LDJSON={
 'services':'''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"MedicalBusiness","name":"Therapy Services — Dr. Alina Schulhofer","description":"Individual therapy, couples & family therapy, and intensives for high achievers, high-net-worth individuals, and high-profile clients.","areaServed":[{"@type":"State","name":"Florida"},{"@type":"State","name":"New York"}],"provider":{"@type":"Person","name":"Dr. Alina Schulhofer"}}
</script>''',
}

FAQ_ITEMS=[
 ("Do you accept insurance?","No. I am a private-pay provider and do not accept insurance, which means no mental health diagnosis has to be placed on your record. Your care is guided entirely by your needs and goals, rather than limited by the session frequency, length, or duration an insurance company might otherwise dictate."),
 ("Are sessions in-person or virtual?","All sessions are conducted virtually via Zoom."),
 ("Who do you typically work with?","I work with individuals, couples, and families across a wide range of life experiences, though I specialize in working with high achievers, high-net-worth individuals, and high-profile clients—including executives, entrepreneurs, creatives, founders, professional athletes, academics, and medical professionals."),
 ("What is your therapeutic approach?","My approach is relational psychoanalytic, which means I make use of what takes place between me and my clients to better understand how they relate to other people in their lives—what goes well, and where they may inadvertently create or replay painful dynamics. I take a holistic perspective that sees and treats the person as an interconnected being, including mind, body, spirit, and the broader systems in which we live and work."),
 ("How long are sessions, and how often do we meet?","Standard individual sessions are 50 minutes, typically held weekly, though frequency is determined collaboratively based on your needs. Extended sessions can be arranged on a case-by-case basis. Couples and families begin with a comprehensive initial evaluation—one 90-minute joint session followed by individual 60-minute sessions—then typically meet weekly for 50-minute sessions, with extended 90-minute sessions available."),
 ("What is a therapy intensive, and is it right for me?","Therapy intensives offer a more focused and transformative experience than standard weekly sessions, allowing us to work for extended periods in a contained way. They may be helpful if you're navigating a significant life transition, an interpersonal crisis, trauma that feels difficult to approach in shorter sessions, feeling stuck in ongoing patterns, a desire for accelerated growth, or a schedule that makes weekly therapy challenging. Intensives can take place as extended 90-minute or 2-hour sessions, or as full-day (4–5 hour) intensives with breaks."),
 ("What are concierge services, and how do they work?","For those who want a higher level of accessibility and support, I offer concierge-style care through a monthly subscription. This includes extended session options, priority scheduling, and the ability to reach me directly between sessions for guidance during moments that can't wait for your next appointment. Please inquire directly to discuss whether this level of care is the right fit for you."),
]
_faq_entities=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ_ITEMS]
FAQ_LDJSON='<script type="application/ld+json">\n'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":_faq_entities})+'\n</script>'

# NAV, FONTS, DOMAIN, SCRIPT now come from common.py (shared with build_blog.py).
# the home content still has id references (#about etc via data-go?) none now. It uses hero cta href="#contact" and about page as separate file.
META={
 'home':('index.html','Dr. Alina Schulhofer, PsyD | Therapy for High Achievers, FL & NY',
         'Depth-oriented virtual psychotherapy for executives, entrepreneurs, high-net-worth and high-profile individuals in Florida and New York. Private-pay, concierge care.'),
 'about':('about.html','About Dr. Alina Schulhofer, PsyD | Licensed Psychologist',
          'Meet Dr. Alina Schulhofer, PsyD, a licensed clinical psychologist providing depth-oriented virtual therapy for high performers, high-net-worth, and high-profile individuals in Florida and New York.'),
 'services':('services.html','Therapy Services & Investment | Dr. Alina Schulhofer, PsyD',
             'Individual and couples therapy plus intensives, private-pay virtual care for high-demand, high-net-worth, and high-profile lives in Florida and New York.'),
 'faq':('faq.html','Frequently Asked Questions | Dr. Alina Schulhofer, PsyD',
        'Answers to common questions about private-pay therapy, licensing, confidentiality, concierge services, and intensives with Dr. Alina Schulhofer.'),
}
PAGE_NAME={'about':'About','services':'Therapy Services','faq':'FAQ'}

for pid,content in pages.items():
    fn,title,desc=META[pid]
    canon=DOMAIN+'/'+('' if fn=='index.html' else fn)
    extra_ldjson=JSONLD if pid=='home' else ''
    if pid=='about':
        extra_ldjson=PERSON_LDJSON+'\n'+breadcrumb(PAGE_NAME[pid], canon)
    elif pid in SERVICE_LDJSON:
        extra_ldjson=SERVICE_LDJSON[pid]+'\n'+breadcrumb(PAGE_NAME[pid], canon)
    elif pid=='faq':
        extra_ldjson=FAQ_LDJSON+'\n'+breadcrumb(PAGE_NAME[pid], canon)
    head=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{canon}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{canon}" />
<meta property="og:image" content="{DOMAIN}/assets/portrait-about.jpg?v={IMG_VERSION}" />
<meta name="twitter:card" content="summary_large_image" />
{FAVICON}
{FONTS}
{CSS_LINK}
{NOSCRIPT_FALLBACK}
{extra_ldjson}
{GA_SCRIPT}
</head>
<body>
{NAV(pid)}
{content}
{footer}
{FAB_BOOK}
{IAG_POPUP}
{SCRIPT}
{CAL_SCRIPT}
{VISITOR_LOGGER_SCRIPT}
</body>
</html>'''
    open(ROOT/fn,'w',encoding='utf-8').write(head)
    print('wrote', fn, len(head), 'bytes')
print('css bytes', len(css))

# --- 3. custom 404 page (GitHub Pages serves 404.html automatically for any unmatched path) ---
not_found_body='''<section class="pg-head">
  <div class="container">
    <h1>Page Not Found</h1>
    <p class="sub">The page you're looking for doesn't exist or may have moved.</p>
    <a href="index.html" class="btn-solid" style="margin-top:26px;display:inline-block;">Return Home</a>
  </div>
</section>'''
not_found_head=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Page Not Found | Dr. Alina Schulhofer</title>
<meta name="robots" content="noindex" />
{FAVICON}
{FONTS}
{CSS_LINK}
{NOSCRIPT_FALLBACK}
{GA_SCRIPT}
</head>
<body>
{NAV('')}
{not_found_body}
{footer}
{FAB_BOOK}
{SCRIPT}
{CAL_SCRIPT}
{VISITOR_LOGGER_SCRIPT}
</body>
</html>'''
open(ROOT/'404.html','w',encoding='utf-8').write(not_found_head)
print('wrote 404.html')

# --- 3b. unlisted free-guide download page (not in NAV, not in sitemap — reached only after
# submitting an email in the IAG_POPUP lead-capture form) ---
iag_body=f'''<section class="pg-head">
  <div class="container narrow">
    <p class="eyebrow">Free Mini E-Book</p>
    <h1>The Inner Alignment Guide</h1>
    <p class="sub">Thank you &mdash; your copy is ready. Click below to download.</p>
  </div>
</section>
<section class="section" style="padding:40px 0 110px;">
  <div class="container narrow" style="max-width:420px;text-align:center;">
    <img src="assets/inner-alignment-guide-cover.jpg?v={IMG_VERSION}" alt="Lead From Within: The Inner Alignment Guide for High Performers" style="width:100%;max-width:280px;margin:0 auto 36px;display:block;border-radius:4px;box-shadow:0 20px 50px rgba(21,21,26,.18);" />
    <a href="assets/inner-alignment-guide.pdf?v={IMG_VERSION}" download class="btn-solid">Download the Guide</a>
  </div>
</section>'''
iag_head=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>The Inner Alignment Guide | Dr. Alina Schulhofer</title>
<meta name="robots" content="noindex" />
{FAVICON}
{FONTS}
{CSS_LINK}
{NOSCRIPT_FALLBACK}
{GA_SCRIPT}
</head>
<body>
{NAV('')}
{iag_body}
{footer}
{FAB_BOOK}
{SCRIPT}
{CAL_SCRIPT}
{VISITOR_LOGGER_SCRIPT}
</body>
</html>'''
open(ROOT/'inner-alignment-guide.html','w',encoding='utf-8').write(iag_head)
print('wrote inner-alignment-guide.html')

# --- 3c. unlisted all-options booking page (not in NAV, not in sitemap — linked from the
# footer's "See all booking options" link). Embeds the full Cal.com booking page inline so
# visitors can see every event type without leaving the site. ---
book_body='''<section class="pg-head">
  <div class="container narrow">
    <p class="eyebrow">Schedule Online</p>
    <h1>Book a Session</h1>
    <p class="sub">Choose the option that fits where you are right now.</p>
    <p class="svc-booking-area">Available to clients located in Florida and New York.</p>
  </div>
</section>
<section class="section" style="padding:24px 0 110px;">
  <div class="container narrow">
    <div id="calBookingInline" style="width:100%;min-height:700px;overflow:auto;"></div>
    <p style="text-align:center;font-size:13px;color:var(--ink3);margin-top:18px;">If the calendar doesn&rsquo;t load, <a href="https://cal.com/dralinaschulhofer" target="_blank" rel="noopener" style="color:var(--accent);text-decoration:underline;text-underline-offset:.15em;">view booking options directly on Cal.com &rarr;</a></p>
  </div>
</section>'''
# Runs after CAL_SCRIPT (which defines window.Cal as a queuing stub synchronously, even before
# the actual embed.js has finished loading) so the inline-embed call is always safe to make here.
book_inline_script='''<script>
  if (window.Cal) {
    Cal("inline", { elementOrSelector: "#calBookingInline", calLink: "dralinaschulhofer", layout: "month_view" });
  }
</script>'''
book_head=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Book a Session | Dr. Alina Schulhofer</title>
<meta name="robots" content="noindex" />
{FAVICON}
{FONTS}
{CSS_LINK}
{NOSCRIPT_FALLBACK}
{GA_SCRIPT}
</head>
<body>
{NAV('')}
{book_body}
{footer}
{FAB_BOOK}
{SCRIPT}
{CAL_SCRIPT}
{book_inline_script}
{VISITOR_LOGGER_SCRIPT}
</body>
</html>'''
open(ROOT/'book.html','w',encoding='utf-8').write(book_head)
print('wrote book.html')

# --- 4. robots.txt + sitemap.xml (regenerated every build so new blog posts are always included) ---
open(ROOT/'robots.txt','w',encoding='utf-8').write(
    f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n'
)
import datetime
today=datetime.date.today().isoformat()
sitemap_urls=[(DOMAIN+'/', today, 'weekly', '1.0')]
for pid,(fn,_,_) in META.items():
    if fn=='index.html':
        continue
    sitemap_urls.append((f'{DOMAIN}/{fn}', today, 'monthly', '0.8'))
sitemap_urls.append((f'{DOMAIN}/blog.html', today, 'weekly', '0.7'))
for post in posts:
    sitemap_urls.append((f'{DOMAIN}/{post["slug"]}.html', post['date'], 'monthly', '0.6'))
sitemap_xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for loc,lastmod,changefreq,priority in sitemap_urls:
    sitemap_xml+=f'  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>\n'
sitemap_xml+='</urlset>\n'
open(ROOT/'sitemap.xml','w',encoding='utf-8').write(sitemap_xml)
print('wrote robots.txt and sitemap.xml —', len(sitemap_urls), 'urls')
