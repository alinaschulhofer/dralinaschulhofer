import re, pathlib, sys, html
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent  # deploy files live at repo root; master source lives in src/
sys.path.insert(0, str(HERE))
from common import DOMAIN, FONTS, NAV, SCRIPT, CSS_LINK
from build_blog import load_posts, human_date
src=open(HERE/'therapy_template.html',encoding='utf-8').read()

# --- 1. extract <style> content, drop embedded base64 @font-face (we use Google Fonts) ---
style=re.search(r'<style>(.*?)</style>', src, re.S).group(1)
style_lines=[ln for ln in style.split('\n') if 'base64,__' not in ln]
css="\n".join(style_lines).strip()
open(ROOT/'styles.css','w',encoding='utf-8').write(css)

# --- 2. body content ---
body=re.search(r'<body>(.*?)</body>', src, re.S).group(1)
# swap embedded image data-uris for asset files
body=body.replace('data:image/jpeg;base64,__PABOUT__','assets/portrait-about.jpg')
body=body.replace('data:image/jpeg;base64,__PCIRCLE__','assets/portrait-circle.jpg')
body=body.replace('data:image/jpeg;base64,__FACE__','assets/face.jpg')

# extract each page's inner content
def page_inner(pid):
    m=re.search(r'<div class="page[^"]*" id="'+pid+r'">(.*?)</div>\s*(?=<!-- =+ |<footer>)', body, re.S)
    return m.group(1).strip()
pages={pid:page_inner(pid) for pid in ['home','about','services','faq','coaching']}

# homepage — inject the newest blog post into the featured-post teaser
posts=load_posts()
if posts:
    latest=posts[0]  # load_posts() sorts newest-first by date
    fp_html=f'''<p class="fp-kicker">From the Blog</p>
      <p class="fp-meta"><span class="fp-tag">{html.escape(latest['tag'])}</span>{human_date(latest['date'])}</p>
      <h2><a href="{latest['slug']}.html">{html.escape(latest['title'])}</a></h2>
      <p class="fp-excerpt">{html.escape(latest['excerpt'])}</p>
      <a href="{latest['slug']}.html" class="fp-link">Read the Full Post →</a>'''
    pages['home']=pages['home'].replace('<!-- __FEATURED_POST__ -->', fp_html)

# footer
footer='<footer>'+re.search(r'<footer>(.*?)</footer>', body, re.S).group(1)+'</footer>'

JSONLD='''<script type="application/ld+json">
{"@context":"https://schema.org","@type":["Psychologist","MedicalBusiness"],"name":"Dr. Alina Schulhofer — Concierge Psychological Services","description":"Depth-oriented virtual psychotherapy for high achievers — executives, entrepreneurs, creatives, founders, and professional athletes. Licensed clinical psychologist in Florida and New York.","url":"https://www.dralinaschulhofer.com","telephone":"+1-786-671-4945","email":"alina@dralinaschulhofer.com","areaServed":[{"@type":"State","name":"Florida"},{"@type":"State","name":"New York"}],"availableService":[{"@type":"MedicalTherapy","name":"Individual Therapy"},{"@type":"MedicalTherapy","name":"Couples & Family Therapy"},{"@type":"MedicalTherapy","name":"Concierge Therapy"},{"@type":"MedicalTherapy","name":"Therapy Intensives"}],"founder":{"@type":"Person","name":"Dr. Alina Schulhofer","jobTitle":"Licensed Clinical Psychologist (PsyD)","alumniOf":"Nova Southeastern University"},"knowsAbout":["Psychotherapy","Trauma","Personality","Relationships","High Performance Psychology","Executive Wellbeing"]}
</script>'''

# NAV, FONTS, DOMAIN, SCRIPT now come from common.py (shared with build_blog.py).
# the home content still has id references (#about etc via data-go?) none now. It uses hero cta href="#contact" and about page as separate file.
META={
 'home':('index.html','Dr. Alina Schulhofer — Concierge Psychological Services | Virtual Therapy, Florida & New York',
         'Depth-oriented virtual psychotherapy for high achievers — executives, entrepreneurs, creatives, and professional athletes. Licensed clinical psychologist in Florida & New York.'),
 'about':('about.html','About Dr. Alina Schulhofer — Licensed Clinical Psychologist | Florida & New York',
          'Meet Dr. Alina Schulhofer, PsyD — a licensed clinical psychologist offering depth-oriented virtual therapy for high performers in Florida and New York.'),
 'services':('services.html','Services & Investment — Concierge Therapy | Dr. Alina Schulhofer',
             'Individual, couples & family therapy, concierge care, and intensives — virtual, private, and tailored to high-demand lives. Florida & New York.'),
 'faq':('faq.html','FAQ — Therapy with Dr. Alina Schulhofer',
        'Common questions about virtual concierge psychotherapy with Dr. Alina Schulhofer — insurance, fees, scheduling, and how to begin.'),
 'coaching':('coaching.html','Consulting — Dr. Alina Schulhofer',
             'Organizational consulting, education, and executive coaching through Architecture of Excellence™, founded by Dr. Alina Schulhofer — separate from her clinical practice.'),
}

for pid,content in pages.items():
    fn,title,desc=META[pid]
    canon=DOMAIN+'/'+('' if fn=='index.html' else fn)
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
<meta property="og:image" content="{DOMAIN}/assets/portrait-about.jpg" />
<meta name="twitter:card" content="summary_large_image" />
{FONTS}
{CSS_LINK}
{JSONLD if pid=='home' else ''}
</head>
<body>
{NAV(pid)}
{content}
{footer}
{SCRIPT}
</body>
</html>'''
    open(ROOT/fn,'w',encoding='utf-8').write(head)
    print('wrote', fn, len(head), 'bytes')
print('css bytes', len(css))
