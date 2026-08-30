"""Shared constants for build_site.py and build_blog.py — keep nav/fonts/domain in one place
so every generated page (marketing pages + blog) stays in sync."""
import re, pathlib

DOMAIN = 'https://www.dralinaschulhofer.com'

# Bump this on every deploy that changes styles.css — the link tag below embeds it as
# ?v=N so browsers/CDNs treat it as a new URL instead of serving a stale cached copy.
CSS_VERSION = 4
CSS_LINK = f'<link rel="stylesheet" href="styles.css?v={CSS_VERSION}" />'

def get_footer():
    """Footer markup lives once in therapy_template.html — extract it so build_blog.py
    never drifts from what build_site.py puts on the marketing pages."""
    here = pathlib.Path(__file__).resolve().parent
    src = open(here / 'therapy_template.html', encoding='utf-8').read()
    return '<footer>' + re.search(r'<footer>(.*?)</footer>', src, re.S).group(1) + '</footer>'

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@300;500&display=swap" rel="stylesheet">'

# Blog nav link is held back until there's at least one real post — flip this to True
# (and re-run build_site.py + build_blog.py) to relaunch it site-wide.
SHOW_BLOG_NAV = False

def NAV(active):
    blog_link = ''
    if SHOW_BLOG_NAV:
        blog_cls = ' class="active"' if active == 'blog' else ''
        blog_link = f'<a href="blog.html"{blog_cls}>Blog</a>\n      '
    return f'''<header class="top">
  <div class="container">
    <a href="index.html" class="wordmark">Dr. Alina Schulhofer</a>
    <nav class="nav" id="nav">
      <a href="index.html"{' class="active"' if active=="home" else ''}>Home</a>
      <a href="about.html"{' class="active"' if active=="about" else ''}>About</a>
      <a href="services.html"{' class="active"' if active=="services" else ''}>Clinical Services</a>
      <a href="coaching.html"{' class="active"' if active=="coaching" else ''}>Consulting</a>
      <a href="faq.html"{' class="active"' if active=="faq" else ''}>FAQ</a>
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
    .catch(function(){ var body='Name: '+name+'%0D%0AEmail: '+email+'%0D%0APhone: '+phone+'%0D%0A%0D%0A'+encodeURIComponent(msg); window.location.href='mailto:alina@dralinaschulhofer.com?subject='+encodeURIComponent('Free Consultation Request \\u2014 '+name)+'&body='+body; btn.disabled=false; btn.textContent='Request My Free Consultation'; });
  }); }
  document.body.classList.add('anim');
  var revealSel=['.trust3','.svc-teaser .container','.helpwith .container','.philosophy-band .prose','.founder .container','.contact-band .container','.about-head-row','#about .prose','.pg-head','.container.narrow'];
  revealSel.forEach(function(sel){ document.querySelectorAll(sel).forEach(function(el){ el.classList.add('reveal'); }); });
  document.querySelectorAll('.tphoto img, .about-face').forEach(function(el){ el.classList.add('reveal-img'); });
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(en){ en.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('is-visible'); io.unobserve(e.target);} }); },{threshold:0.12,rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.reveal,.reveal-img').forEach(function(el){ io.observe(el); });
  } else { document.querySelectorAll('.reveal,.reveal-img').forEach(function(el){ el.classList.add('is-visible'); }); }
</script>'''
