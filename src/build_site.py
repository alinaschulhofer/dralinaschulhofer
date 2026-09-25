import re, pathlib, sys, html
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent  # deploy files live at repo root; master source lives in src/
sys.path.insert(0, str(HERE))
from common import DOMAIN, FONTS, NAV, SCRIPT, CSS_LINK, GA_SCRIPT, VISITOR_LOGGER_SCRIPT, IMG_VERSION, FAVICON, NOSCRIPT_FALLBACK, FAB_BOOK
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
body=body.replace('data:image/jpeg;base64,__CONSULTHERO__',f'assets/consulting-hero.jpg?v={IMG_VERSION}')
body=body.replace('data:image/jpeg;base64,__PPHIL__',f'assets/about-hero-photo.jpg?v={IMG_VERSION}')
body=body.replace('data:image/jpeg;base64,__THERAPYPHIL__',f'assets/therapy-philosophy-photo.jpg?v={IMG_VERSION}')
body=body.replace('data:image/jpeg;base64,__THERAPYHERO__',f'assets/therapy-hero-photo.jpg?v={IMG_VERSION}')
body=body.replace('data:image/jpeg;base64,__CONSULTSPLIT__',f'assets/consulting-split-photo.jpg?v={IMG_VERSION}')
body=body.replace('data:image/jpeg;base64,__ABOUTHERO__',f'assets/philosophy-photo.jpg?v={IMG_VERSION}')

# extract each page's inner content
def page_inner(pid):
    m=re.search(r'<div class="page[^"]*" id="'+pid+r'">(.*?)</div>\s*(?=<!-- =+ |<footer>)', body, re.S)
    return m.group(1).strip()
pages={pid:page_inner(pid) for pid in ['home','about','services','coaching','execcoaching']}

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
{"@context":"https://schema.org","@type":["Psychologist","MedicalBusiness"],"name":"Dr. Alina Schulhofer — Concierge Psychological Services","description":"Depth-oriented virtual psychotherapy for high achievers — executives, entrepreneurs, creatives, founders, and professional athletes. Licensed clinical psychologist in Florida and New York.","url":"https://www.dralinaschulhofer.com","telephone":"+1-786-671-4945","email":"alina@dralinaschulhofer.com","areaServed":[{"@type":"State","name":"Florida"},{"@type":"State","name":"New York"}],"availableService":[{"@type":"MedicalTherapy","name":"Individual Therapy"},{"@type":"MedicalTherapy","name":"Couples & Family Therapy"},{"@type":"MedicalTherapy","name":"Concierge Therapy"},{"@type":"MedicalTherapy","name":"Therapy Intensives"}],"founder":{"@type":"Person","name":"Dr. Alina Schulhofer","jobTitle":"Licensed Clinical Psychologist (PsyD)","alumniOf":"Nova Southeastern University"},"knowsAbout":["Psychotherapy","Trauma","Personality","Relationships","High Performance Psychology","Executive Wellbeing"],"sameAs":["https://architectureofexcellence.com"]}
</script>'''

def breadcrumb(name, canon):
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{DOMAIN}/"}},{{"@type":"ListItem","position":2,"name":"{name}","item":"{canon}"}}]}}
</script>'''

PERSON_LDJSON='''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Person","name":"Dr. Alina Schulhofer","jobTitle":"Licensed Clinical Psychologist (PsyD)","alumniOf":"Nova Southeastern University","url":"https://www.dralinaschulhofer.com/about.html","image":"https://www.dralinaschulhofer.com/assets/portrait-about.jpg","worksFor":[{"@type":"MedicalBusiness","name":"Dr. Alina Schulhofer — Concierge Psychological Services"},{"@type":"Organization","name":"Architecture of Excellence","url":"https://architectureofexcellence.com"}],"knowsAbout":["Psychotherapy","Trauma","Relationships","High Performance Psychology","Executive Coaching"]}
</script>'''

SERVICE_LDJSON={
 'services':'''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"MedicalBusiness","name":"Therapy Services — Dr. Alina Schulhofer","description":"Individual, couples & family therapy, concierge care, and intensives.","areaServed":[{"@type":"State","name":"Florida"},{"@type":"State","name":"New York"}],"provider":{"@type":"Person","name":"Dr. Alina Schulhofer"}}
</script>''',
 'coaching':'''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","serviceType":"Organizational Consulting","name":"Organizational Consulting — Architecture of Excellence","provider":{"@type":"Organization","name":"Architecture of Excellence","url":"https://architectureofexcellence.com"},"areaServed":"Worldwide"}
</script>''',
 'execcoaching':'''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","serviceType":"Executive Coaching","name":"Executive Coaching — Dr. Alina Schulhofer","provider":{"@type":"Person","name":"Dr. Alina Schulhofer"},"audience":{"@type":"Audience","audienceType":"Executives, founders, leaders, and professional athletes"},"areaServed":"Worldwide"}
</script>''',
}

# NAV, FONTS, DOMAIN, SCRIPT now come from common.py (shared with build_blog.py).
# the home content still has id references (#about etc via data-go?) none now. It uses hero cta href="#contact" and about page as separate file.
META={
 'home':('index.html','Dr. Alina Schulhofer, PsyD | Therapy for High Achievers, FL & NY',
         'Depth-oriented virtual psychotherapy for executives, entrepreneurs, and high performers in Florida and New York. Private-pay, concierge care.'),
 'about':('about.html','About Dr. Alina Schulhofer, PsyD | Licensed Psychologist',
          'Meet Dr. Alina Schulhofer, PsyD, a licensed clinical psychologist providing depth-oriented virtual therapy for high performers in Florida and New York.'),
 'services':('services.html','Therapy Services & Investment | Dr. Alina Schulhofer, PsyD',
             'Individual, couples, and concierge therapy plus intensives, private-pay virtual care for high-demand lives in Florida and New York.'),
 'coaching':('coaching.html','Organizational Consulting & Leadership Advisory | AOE',
             'Organizational consulting, education, and executive coaching for teams, through Architecture of Excellence, founded by Dr. Alina Schulhofer.'),
 'execcoaching':('executive-coaching.html','Executive Coaching for Leaders & Founders | Dr. Schulhofer',
             'Private, 1:1 executive coaching for executives, founders, leaders, and professional athletes committed to sustainable high performance.'),
}
PAGE_NAME={'about':'About','services':'Therapy Services','coaching':'Organizational Consulting','execcoaching':'Executive Coaching'}

for pid,content in pages.items():
    fn,title,desc=META[pid]
    canon=DOMAIN+'/'+('' if fn=='index.html' else fn)
    extra_ldjson=JSONLD if pid=='home' else ''
    if pid=='about':
        extra_ldjson=PERSON_LDJSON+'\n'+breadcrumb(PAGE_NAME[pid], canon)
    elif pid in SERVICE_LDJSON:
        extra_ldjson=SERVICE_LDJSON[pid]+'\n'+breadcrumb(PAGE_NAME[pid], canon)
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
{SCRIPT}
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
{VISITOR_LOGGER_SCRIPT}
</body>
</html>'''
open(ROOT/'404.html','w',encoding='utf-8').write(not_found_head)
print('wrote 404.html')

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
