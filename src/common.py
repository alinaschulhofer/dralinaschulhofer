"""Shared constants for build_site.py and build_blog.py — keep nav/fonts/domain in one place
so every generated page (marketing pages + blog) stays in sync."""
import re, pathlib

DOMAIN = 'https://www.dralinaschulhofer.com'

# Bump this on every deploy that changes styles.css — the link tag below embeds it as
# ?v=N so browsers/CDNs treat it as a new URL instead of serving a stale cached copy.
CSS_VERSION = 140
CSS_LINK = f'<link rel="stylesheet" href="styles.css?v={CSS_VERSION}" />'

# Bump this whenever a file in assets/ changes (photos, etc.) — same cache-busting trick as
# CSS_VERSION. Browsers (especially Safari) cache images very aggressively with no other signal
# that the file changed, since the filename itself stays the same.
IMG_VERSION = 20

def get_footer():
    """Footer markup lives once in therapy_template.html — extract it so build_blog.py
    never drifts from what build_site.py puts on the marketing pages."""
    here = pathlib.Path(__file__).resolve().parent
    src = open(here / 'therapy_template.html', encoding='utf-8').read()
    return '<footer>' + re.search(r'<footer>(.*?)</footer>', src, re.S).group(1) + '</footer>'

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Alex+Brush&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@300;500&display=swap" rel="stylesheet">'

FAVICON = '<link rel="icon" href="favicon.ico" sizes="any" /><link rel="icon" href="favicon.png" type="image/png" /><link rel="apple-touch-icon" href="apple-touch-icon.png" />'

# Fallback for the body-fade-in polish (body starts at opacity:0, JS adds .anim to fade it in) —
# without this, a page would stay invisible forever if JavaScript is blocked or fails to run.
NOSCRIPT_FALLBACK = '<noscript><style>body{opacity:1 !important;}</style></noscript>'

# Floating "Book a Consultation" button — present on every page, links out to Calendly.
CALENDLY_URL = 'https://calendly.com/dralinaschulhofer/consultation-15min'
FAB_BOOK = f'''<a href="{CALENDLY_URL}" target="_blank" rel="noopener" class="fab-book" aria-label="Book a consultation on Calendly">
  <svg viewBox="0 0 40 40"><rect x="7" y="9" width="26" height="24" rx="4"/><path d="M7 17h26"/><path d="M14 5v6M26 5v6" stroke-linecap="round"/><path d="M15 24l3.2 3.2L26 19" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <span>Book Consultation</span>
</a>'''

# Free-ebook lead-capture popup — appears site-wide (via SCRIPT below) 5s after page load,
# skipped on the gated download page itself and suppressed after a visitor has already opted in.
# Submits to the same Formspree endpoint as the contact form (tagged with a distinct _subject
# so Alina can tell lead-magnet signups apart from consultation requests), then redirects to
# the unlisted inner-alignment-guide.html page where the PDF can be downloaded.
IAG_POPUP = '''<div class="iag-overlay" id="iagOverlay">
  <div class="iag-modal">
    <button type="button" class="iag-close" id="iagClose" aria-label="Close">&times;</button>
    <p class="eyebrow">Free Mini E-Book</p>
    <h3 class="iag-title">The Inner Alignment Guide</h3>
    <p class="iag-sub">A free guide from Architecture of Excellence&trade; on leading and living from greater alignment within.</p>
    <form id="iagForm" class="iag-form">
      <input type="email" id="iagEmail" placeholder="Your email address" required />
      <button type="submit">Send Me the Guide</button>
    </form>
  </div>
</div>'''

# Traffic tracking — mirrors the setup on architectureofexcellence.com (see visitor-logger/SETUP.md).
GA_MEASUREMENT_ID = 'G-VXF1MBZZHC'
GA_SCRIPT = f'''<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_MEASUREMENT_ID}');
</script>'''

VISITOR_LOGGER_WORKER_URL = 'https://dralinaschulhofer-visitor-logger.alina-cae.workers.dev/log'
VISITOR_LOGGER_SCRIPT = f'''<script>
  (function(){{
    var w = "{VISITOR_LOGGER_WORKER_URL}";
    var p = encodeURIComponent(location.pathname);
    var r = encodeURIComponent(document.referrer);
    fetch(w + "?page=" + p + "&ref=" + r).catch(function(){{}});
  }})();
</script>'''

# Blog nav link is held back until there's at least one real post — flip this to True
# (and re-run build_site.py + build_blog.py) to relaunch it site-wide.
SHOW_BLOG_NAV = True

def NAV(active):
    blog_link = ''
    if SHOW_BLOG_NAV:
        blog_cls = ' class="active"' if active == 'blog' else ''
        blog_link = f'<a href="blog.html"{blog_cls}>Insights</a>\n      '
    faq_cls = ' class="active"' if active == 'faq' else ''
    return f'''<header class="top">
  <div class="container">
    <a href="index.html" class="wordmark">Dr. Alina Schulhofer</a>
    <nav class="nav" id="nav">
      <a href="about.html"{' class="active"' if active=="about" else ''}>About</a>
      <a href="services.html"{' class="active"' if active=="services" else ''}>Therapy</a>
      <a href="https://architectureofexcellence.com" target="_blank" rel="noopener">Performance &amp; Consulting</a>
      <a href="faq.html"{faq_cls}>FAQ</a>
      {blog_link}<a href="index.html#contact" class="btn">Contact</a>
    </nav>
    <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>'''

SCRIPT = '''<script>
  var nav=document.getElementById('nav'), navToggle=document.getElementById('navToggle');
  var topBar=document.querySelector('.top');
  if(topBar){ var onTopScroll=function(){ topBar.classList.toggle('scrolled', window.scrollY>40); }; window.addEventListener('scroll', onTopScroll, {passive:true}); onTopScroll(); }
  if(navToggle){ navToggle.addEventListener('click',function(){
    if(topBar){ document.documentElement.style.setProperty('--nav-h', topBar.getBoundingClientRect().height+'px'); }
    var open=nav.classList.toggle('open'); navToggle.classList.toggle('open',open);
    navToggle.setAttribute('aria-expanded',open?'true':'false');
  }); }
  document.querySelectorAll('.svc-menu-item').forEach(function(a){
    a.addEventListener('click',function(){
      var hash=a.getAttribute('href').split('#')[1];
      var target=hash && document.getElementById(hash);
      if(target && target.tagName==='DETAILS'){ target.open=true; }
    });
  });
  if(location.hash){
    var hashTarget=document.getElementById(location.hash.slice(1));
    if(hashTarget && hashTarget.tagName==='DETAILS'){ hashTarget.open=true; }
  }
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
    .catch(function(){ var body='Name: '+name+'%0D%0AEmail: '+email+'%0D%0APhone: '+phone+'%0D%0A%0D%0A'+encodeURIComponent(msg); window.location.href='mailto:alina@dralinaschulhofer.com?subject='+encodeURIComponent('Free Consultation Request \\u2014 '+name)+'&body='+body; btn.disabled=false; btn.textContent='Request Consultation'; });
  }); }
  document.body.classList.add('anim');
  var revealSel=['.trust3','.svc-teaser .container','.helpwith .container','.cf-text','.rhp-row','.featured-post .container','.founder .container','.contact-band .container','.about-head-row','#about .prose','.pg-head','.container.narrow'];
  revealSel.forEach(function(sel){ document.querySelectorAll(sel).forEach(function(el){ el.classList.add('reveal'); }); });
  // groups whose direct children (heading, paragraphs, button) fade up one after another
  // instead of all at once — see .reveal-stagger in the CSS.
  var staggerSel=['.split-text','.home-trust-intro'];
  staggerSel.forEach(function(sel){ document.querySelectorAll(sel).forEach(function(el){ el.classList.add('reveal-stagger'); }); });
  document.querySelectorAll('.tphoto img, .about-face, .split-photo img, .eh-photo img, .xb-photo img').forEach(function(el){ el.classList.add('reveal-img'); });
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(en){ en.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('is-visible'); io.unobserve(e.target);} }); },{threshold:0,rootMargin:'0px 0px 800px 0px'});
    document.querySelectorAll('.reveal,.reveal-img,.reveal-stagger,.split-divider').forEach(function(el){ io.observe(el); });
  } else { document.querySelectorAll('.reveal,.reveal-img,.reveal-stagger,.split-divider').forEach(function(el){ el.classList.add('is-visible'); }); }
  (function(){
    var overlay=document.getElementById('iagOverlay');
    if(!overlay || location.pathname.indexOf('inner-alignment-guide')>-1) return;
    try{
      if(localStorage.getItem('iagSubscribed') || sessionStorage.getItem('iagPopupShown')) return;
    }catch(e){}
    setTimeout(function(){
      overlay.classList.add('open');
      try{ sessionStorage.setItem('iagPopupShown','1'); }catch(e){}
    }, 5000);
    var closeBtn=document.getElementById('iagClose');
    if(closeBtn){ closeBtn.addEventListener('click', function(){ overlay.classList.remove('open'); }); }
    overlay.addEventListener('click', function(e){ if(e.target===overlay){ overlay.classList.remove('open'); } });
    var form=document.getElementById('iagForm');
    if(form){ form.addEventListener('submit', function(e){
      e.preventDefault();
      var email=(document.getElementById('iagEmail').value||'').trim();
      var btn=form.querySelector('button'); btn.disabled=true; btn.textContent='Sending\\u2026';
      var go=function(){ try{ localStorage.setItem('iagSubscribed','1'); }catch(e){} window.location.href='inner-alignment-guide.html'; };
      fetch('https://formspree.io/f/xzdwqnvk',{method:'POST',headers:{'Accept':'application/json','Content-Type':'application/json'},body:JSON.stringify({email:email,_subject:'Free Guide Signup \\u2014 '+email,message:'New opt-in for The Inner Alignment Guide: '+email})})
      .then(go).catch(go);
    }); }
  })();
</script>'''
