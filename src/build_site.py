import re, pathlib
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent  # deploy files live at repo root; master source lives in src/
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
pages={pid:page_inner(pid) for pid in ['home','about','services','faq']}

# footer
footer='<footer>'+re.search(r'<footer>(.*?)</footer>', body, re.S).group(1)+'</footer>'

DOMAIN='https://www.dralinaschulhofer.com'
FONTS='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@300;500&display=swap" rel="stylesheet">'

JSONLD='''<script type="application/ld+json">
{"@context":"https://schema.org","@type":["Psychologist","MedicalBusiness"],"name":"Dr. Alina Schulhofer — Concierge Psychological Services","description":"Depth-oriented virtual psychotherapy for high achievers — executives, entrepreneurs, creatives, founders, and professional athletes. Licensed clinical psychologist in Florida and New York.","url":"https://www.dralinaschulhofer.com","telephone":"+1-786-671-4945","email":"alina@dralinaschulhofer.com","areaServed":[{"@type":"State","name":"Florida"},{"@type":"State","name":"New York"}],"availableService":[{"@type":"MedicalTherapy","name":"Individual Therapy"},{"@type":"MedicalTherapy","name":"Couples & Family Therapy"},{"@type":"MedicalTherapy","name":"Concierge Therapy"},{"@type":"MedicalTherapy","name":"Therapy Intensives"}],"founder":{"@type":"Person","name":"Dr. Alina Schulhofer","jobTitle":"Licensed Clinical Psychologist (PsyD)","alumniOf":"Nova Southeastern University"},"knowsAbout":["Psychotherapy","Trauma","Personality","Relationships","High Performance Psychology","Executive Wellbeing"]}
</script>'''

NAV=lambda active:f'''<header class="top">
  <div class="container">
    <a href="index.html" class="wordmark">Dr. Alina Schulhofer</a>
    <nav class="nav" id="nav">
      <a href="index.html"{' class="active"' if active=="home" else ''}>Home</a>
      <a href="about.html"{' class="active"' if active=="about" else ''}>About</a>
      <a href="services.html"{' class="active"' if active=="services" else ''}>Clinical Services</a>
      <a href="faq.html"{' class="active"' if active=="faq" else ''}>FAQ</a>
      <a href="index.html#contact" class="btn">Contact</a>
    </nav>
    <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>'''

SCRIPT='''<script>
  var nav=document.getElementById('nav'), navToggle=document.getElementById('navToggle');
  var topBar=document.querySelector('.top');
  if(topBar){ var onTopScroll=function(){ topBar.classList.toggle('scrolled', window.scrollY>40); }; window.addEventListener('scroll', onTopScroll, {passive:true}); onTopScroll(); }
  if(navToggle){ navToggle.addEventListener('click',function(){
    var open=nav.classList.toggle('open'); navToggle.classList.toggle('open',open);
    navToggle.setAttribute('aria-expanded',open?'true':'false');
  }); }
  var cf=document.getElementById('contactForm');
  if(cf){ cf.addEventListener('submit',function(e){
    e.preventDefault();
    var name=(document.getElementById('cf-name').value||'').trim();
    var email=(document.getElementById('cf-email').value||'').trim();
    var phone=(document.getElementById('cf-phone').value||'').trim();
    var msg=(document.getElementById('cf-msg').value||'').trim();
    var btn=cf.querySelector('button'); btn.disabled=true; btn.textContent='Sending\\u2026';
    fetch('https://formspree.io/f/xzdwqnvk',{method:'POST',headers:{'Accept':'application/json','Content-Type':'application/json'},body:JSON.stringify({name:name,email:email,phone:phone,message:msg,_subject:'Free Consultation Request \\u2014 '+name})})
    .then(function(r){ if(!r.ok){throw new Error('x');} cf.style.display='none'; var s=document.getElementById('cf-success'); if(s){s.style.display='block';} })
    .catch(function(){ var body='Name: '+name+'%0D%0AEmail: '+email+'%0D%0APhone: '+phone+'%0D%0A%0D%0A'+encodeURIComponent(msg); window.location.href='mailto:alina@dralinaschulhofer.com?subject='+encodeURIComponent('Free Consultation Request \\u2014 '+name)+'&body='+body; btn.disabled=false; btn.textContent='Request My Free Consultation'; });
  }); }
  document.body.classList.add('anim');
  var revealSel=['.trust-prose','.helpwith .container','.philosophy-band .prose','.founder .container','.contact-band .container','.about-head-row','#about .prose','.pg-head','.container.narrow'];
  revealSel.forEach(function(sel){ document.querySelectorAll(sel).forEach(function(el){ el.classList.add('reveal'); }); });
  document.querySelectorAll('.about-face').forEach(function(el){ el.classList.add('reveal-img'); });
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(en){ en.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('is-visible'); io.unobserve(e.target);} }); },{threshold:0.12,rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.reveal,.reveal-img').forEach(function(el){ io.observe(el); });
  } else { document.querySelectorAll('.reveal,.reveal-img').forEach(function(el){ el.classList.add('is-visible'); }); }
</script>'''

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
<link rel="stylesheet" href="styles.css" />
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
