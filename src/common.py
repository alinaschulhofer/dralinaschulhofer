"""Shared constants for build_site.py and build_blog.py — keep nav/fonts/domain in one place
so every generated page (marketing pages + blog) stays in sync."""
import re, pathlib

DOMAIN = 'https://www.dralinaschulhofer.com'

def get_footer():
    """Footer markup lives once in therapy_template.html — extract it so build_blog.py
    never drifts from what build_site.py puts on the marketing pages."""
    here = pathlib.Path(__file__).resolve().parent
    src = open(here / 'therapy_template.html', encoding='utf-8').read()
    return '<footer>' + re.search(r'<footer>(.*?)</footer>', src, re.S).group(1) + '</footer>'

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@300;500&display=swap" rel="stylesheet">'

NAV = lambda active: f'''<header class="top">
  <div class="container">
    <a href="index.html" class="wordmark">Dr. Alina Schulhofer</a>
    <nav class="nav" id="nav">
      <a href="index.html"{' class="active"' if active=="home" else ''}>Home</a>
      <a href="about.html"{' class="active"' if active=="about" else ''}>About</a>
      <a href="services.html"{' class="active"' if active=="services" else ''}>Clinical Services</a>
      <a href="coaching.html"{' class="active"' if active=="coaching" else ''}>Consulting</a>
      <a href="faq.html"{' class="active"' if active=="faq" else ''}>FAQ</a>
      <a href="blog.html"{' class="active"' if active=="blog" else ''}>Blog</a>
      <a href="index.html#contact" class="btn">Contact</a>
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
  var revealSel=['.trust3','.helpwith .container','.philosophy-band .prose','.founder .container','.contact-band .container','.about-head-row','#about .prose','.pg-head','.container.narrow'];
  revealSel.forEach(function(sel){ document.querySelectorAll(sel).forEach(function(el){ el.classList.add('reveal'); }); });
  document.querySelectorAll('.tphoto img, .about-face').forEach(function(el){ el.classList.add('reveal-img'); });
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(en){ en.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('is-visible'); io.unobserve(e.target);} }); },{threshold:0.12,rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.reveal,.reveal-img').forEach(function(el){ io.observe(el); });
  } else { document.querySelectorAll('.reveal,.reveal-img').forEach(function(el){ el.classList.add('is-visible'); }); }
</script>'''
