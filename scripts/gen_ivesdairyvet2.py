#!/usr/bin/env python3
"""Generator for the Animal Clinic of Ives Dairy Road rebuild — /ivesdairyvet2/.
All content verified from ivesdairyanimalclinic.com (screenshots + HTML, 2026-11-12).
No AI-generated images anywhere (her StockCake/ai-generated files excluded by law)."""
import os, re

ROOT = os.path.expanduser("~/webblaze/public/ivesdairyvet2")
BASE = "/ivesdairyvet2"
PHONE = "(305) 653-3939"
TEL = "tel:+13056533939"
EMAIL = "info@ivesdairyanimalclinic.com"
ADDR1 = "1562 NE 205th St"
ADDR2 = "Miami, FL 33179"
MAPQ = "https://maps.google.com/?q=1562+NE+205th+St,+Miami,+FL+33179"
MAPEMBED = "https://www.google.com/maps?q=Animal+Clinic+of+Ives+Dairy+Road,+1562+NE+205th+St,+Miami,+FL+33179&output=embed"

HOURS = [("Monday","8AM–5PM"),("Tuesday","8AM–5PM"),("Wednesday","Closed"),
         ("Thursday","8AM–5PM"),("Friday","8AM–5PM"),("Saturday","8AM–12PM"),("Sunday","Closed")]

def head(title, desc, active=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{BASE}/img/logo-mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{BASE}/site.css">
</head>
<body>
<div class="topbar"><div class="wrap topbar-in"><span>Same-day appointments whenever possible, especially for sick patients</span><a href="{TEL}">{PHONE}</a></div></div>
<header class="nav">
  <div class="wrap nav-in">
    <a class="brand" href="{BASE}/"><img src="{BASE}/img/logo-mark.png" alt="Animal Clinic of Ives Dairy Road logo" width="46" height="46"><span class="brand-nm">Animal Clinic<em>of Ives Dairy Road</em></span></a>
    <input type="checkbox" id="nt" class="nav-toggle" aria-label="Open menu">
    <label for="nt" class="nav-burger"><span></span><span></span><span></span></label>
    <nav class="nav-links">
      <a href="{BASE}/services/"{' class="active"' if active=='services' else ''}>Services</a>
      <a href="{BASE}/about/"{' class="active"' if active=='about' else ''}>About</a>
      <a href="{BASE}/payment-options/"{' class="active"' if active=='payment' else ''}>Payment Options</a>
      <a href="{BASE}/contact/"{' class="active"' if active=='contact' else ''}>Contact</a>
      <a class="btn btn-dark btn-nav" href="{BASE}/appointments/">Book Now</a>
    </nav>
  </div>
</header>
<main>
"""

def bookband(h="Ready to book a visit?", p="Call us or request an appointment online — we offer same-day appointments whenever possible, especially for our sick patients."):
    return f"""
<section class="bookband">
  <div class="wrap bookband-in">
    <div><h2>{h}</h2><p>{p}</p></div>
    <div class="bookband-cta"><a class="btn btn-cream" href="{BASE}/appointments/">Request Appointment</a><a class="btn btn-ghost-w" href="{TEL}">Call {PHONE}</a></div>
  </div>
</section>"""

def footer():
    hours_rows = "".join(f'<tr><td>{d}</td><td class="{ "closed" if h=="Closed" else "" }">{h}</td></tr>' for d,h in HOURS)
    return f"""</main>
<footer class="foot">
  <div class="wrap foot-in">
    <div class="foot-brand">
      <img src="{BASE}/img/logo.png" alt="Animal Clinic of Ives Dairy Road" width="190" height="190">
    </div>
    <div class="foot-col">
      <h4>Location</h4>
      <p><a href="{MAPQ}" target="_blank" rel="noopener">{ADDR1},<br>{ADDR2}</a></p>
      <h4 class="mt">Contact</h4>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{TEL}">Phone: {PHONE}</a><br>Fax: (786) 471-4053</p>
    </div>
    <div class="foot-col">
      <h4>Hours</h4>
      <table class="hours">{hours_rows}</table>
    </div>
    <div class="foot-col">
      <h4>Explore</h4>
      <p class="foot-links">
        <a href="{BASE}/services/wellness/">Wellness Visits</a>
        <a href="{BASE}/services/urgent-care/">Urgent Care &amp; Sick Visits</a>
        <a href="{BASE}/services/surgery-dentistry/">Surgery &amp; Dentistry</a>
        <a href="{BASE}/services/health-certificates/">Health Certificates</a>
        <a href="{BASE}/appointments/">Appointments</a>
        <a href="{BASE}/payment-options/">Payment Options</a>
      </p>
    </div>
  </div>
  <div class="wrap foot-base">
    <span>© 2026 Animal Clinic of Ives Dairy Road · {ADDR1}, {ADDR2}</span>
    <span class="foot-award">2026 Neighborhood Fave · Voted by neighbors on Nextdoor</span>
  </div>
</footer>
</body>
</html>"""

def page(path, html):
    d = os.path.join(ROOT, path)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w") as f:
        f.write(html)
    print("wrote", os.path.join(path, "index.html") or "index.html")

# ---------------------------------------------------------------- HOME
wellness_bullets = ["New Puppy and Kitten exams","Adult and Senior Wellness","Immunizations / Vaccines","Microchipping","Parasite control","Preventative Medicine","Weight and Nutrition Management","Behavioral Management"]
urgent_bullets = ["Allergy and Itchy Skin","Gastrointestinal Distress","Coughing","Ear Infections","Limping","Eye Issues","Lethargy","Arthritis"]
surgery_bullets = ["Spays and Neuters","Mass Removals","Full Mouth Dental X-Rays","Dental Cleaning and Polishing","Tooth Extractions","Bladder Stone Removal"]

def card_list(items, n=5):
    lis = "".join(f"<li>{i}</li>" for i in items[:n])
    more = f'<li class="more">+ {len(items)-n} more</li>' if len(items) > n else ""
    return f"<ul class='svc-ul'>{lis}{more}</ul>"

home = head("Animal Clinic of Ives Dairy Road | Veterinarian in Miami, FL",
            "Your pet's second home in North Miami Beach. Wellness visits, urgent care, surgery and dentistry, and USDA health certificates. Call (305) 653-3939.") + f"""
<section class="hero">
  <img class="hero-img" src="{BASE}/img/hero-main.jpg" alt="A veterinarian gently embracing a happy dog during a checkup" fetchpriority="high">
  <div class="hero-scrim"></div>
  <div class="wrap hero-in">
    <p class="hero-kicker">Animal Clinic of Ives Dairy Road · Miami, FL</p>
    <h1>Welcome to Your Pet&rsquo;s Second&nbsp;Home</h1>
    <p class="hero-sub">A neighborhood veterinary clinic in North Miami Beach, led by Cornell-trained Dr.&nbsp;Aditi&nbsp;Ahuja, DVM — where every visit feels like coming home.</p>
    <div class="hero-cta"><a class="btn btn-cream" href="{BASE}/appointments/">Book an Appointment</a><a class="btn btn-ghost-w" href="{BASE}/services/">Explore Our Services</a></div>
  </div>
</section>

<section class="trust">
  <div class="wrap trust-in">
    <div class="trust-it"><strong>4.6&#9733;</strong><span>Google rating, 230+ reviews</span></div>
    <div class="trust-it"><strong>2026 Fave</strong><span>Voted by neighbors on Nextdoor</span></div>
    <div class="trust-it"><strong>Fear Free</strong><span>Certified veterinarian</span></div>
    <div class="trust-it"><strong>Cornell DVM</strong><span>Phi Zeta Honor Society</span></div>
    <div class="trust-it"><strong>Same-day</strong><span>Appointments for sick patients</span></div>
  </div>
</section>

<section class="sec sec-cream">
  <div class="wrap split">
    <div class="split-txt">
      <p class="eyebrow">A second home for your pet</p>
      <h2>Care that feels personal, because it is</h2>
      <p>We&rsquo;re a small clinic on Ives Dairy Road that treats your pets the way we treat our own. From a puppy&rsquo;s first exam to a senior dog&rsquo;s golden years, Dr.&nbsp;Ahuja and our team take the time to know your pet &mdash; their history, their quirks, and what makes them feel safe.</p>
      <p>Our veterinarian is Fear Free Certified, which means every visit is designed to lower stress for your pet, not just treat the problem. That&rsquo;s what a second home should feel like.</p>
      <a class="arrow-link" href="{BASE}/about/">Meet your veterinary team</a>
    </div>
    <figure class="split-img"><img src="{BASE}/img/hero.jpg" alt="A happy golden retriever relaxing at home" loading="lazy"></figure>
  </div>
</section>

<section class="awardband"><img src="{BASE}/img/herovet.jpg" alt="2026 Fave Winner — voted by neighbors on Nextdoor" loading="lazy"></section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Our services</p>
      <h2>Explore what we offer</h2>
      <p class="lede">At our veterinary clinic, we&rsquo;re passionate about providing personalized, top-notch care for your furry friends. Our dedicated team is here to ensure your pets are happy and healthy every step of the way.</p>
    </div>
    <div class="svc-grid">
      <a class="svc-card" href="{BASE}/services/wellness/">
        <figure><img src="{BASE}/img/card-wellness.jpg" alt="A kitten receiving a gentle wellness exam on the table" loading="lazy"></figure>
        <h3>Wellness Visits</h3>
        {card_list(wellness_bullets)}
        <span class="svc-go">Learn more</span>
      </a>
      <a class="svc-card" href="{BASE}/services/urgent-care/">
        <figure><img src="{BASE}/img/card-urgent.jpg" alt="A veterinarian examining a dog during a sick visit" loading="lazy"></figure>
        <h3>Urgent Care and Sick Visits</h3>
        {card_list(urgent_bullets)}
        <span class="svc-go">Learn more</span>
      </a>
      <a class="svc-card" href="{BASE}/services/surgery-dentistry/">
        <figure><img src="{BASE}/img/det-surgery.jpg" alt="A veterinary professional demonstrating dental care" loading="lazy"></figure>
        <h3>Surgery and Dentistry</h3>
        {card_list(surgery_bullets)}
        <span class="svc-go">Learn more</span>
      </a>
    </div>
  </div>
</section>

<section class="sec sec-cream">
  <div class="wrap travel">
    <div class="travel-imgs">
      <figure class="tv1"><img src="{BASE}/img/svc-list-certs.jpg" alt="A woman and her dog looking out of a car window on a trip"></figure>
      <figure class="tv2"><img src="{BASE}/img/airport.jpg" alt="An airport terminal at sunrise"></figure>
    </div>
    <div class="travel-txt">
      <p class="eyebrow">Traveling with your pet?</p>
      <h2>Health Certificates and Pet Travel</h2>
      <p>Planning to travel with your pet? Our USDA-certified veterinarian will work with you to provide vaccines, testing, and health certificates for both domestic and international travel.</p>
      <p>Please consult the USDA&rsquo;s pet travel guidelines as early as possible to avoid any travel delays. Our team is here to make the process smooth, safe, and stress-free for you and your pet.</p>
      <a class="btn btn-teal" href="{BASE}/services/health-certificates/">Health Certificate Details</a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap doc">
    <div class="doc-txt">
      <p class="eyebrow">Your veterinarian</p>
      <h2>Dr. Aditi Ahuja, <span class="dvm">DVM</span></h2>
      <p>Dr. Ahuja earned her Doctorate of Veterinary Medicine from Cornell University, where she was inducted into the Phi Zeta Veterinary Honor Society. She completed a rotating internship in Small Animal Medicine and Surgery at Friendship Hospital for Animals in Washington, D.C., and has a passion for diagnosing and managing chronic diseases.</p>
      <p>She is Fear Free Certified and an active member of the AVMA and the Veterinary Business Management Association &mdash; and she finds deep fulfillment in helping families understand their pets&rsquo; health at every step.</p>
      <a class="arrow-link" href="{BASE}/about/">Read her full story and meet the team</a>
    </div>
    <div class="doc-quote">
      <blockquote>&ldquo;Her true passion lies in guiding pet owners through the journey of early diagnosis, intervention, and lifelong care.&rdquo;</blockquote>
      <div class="doc-creds"><span>Cornell University DVM</span><span>Phi Zeta Honor Society</span><span>Fear Free Certified</span><span>AVMA &amp; VBMA Member</span></div>
    </div>
  </div>
</section>

<section class="sec sec-cream">
  <div class="wrap pay-tease">
    <div>
      <p class="eyebrow">Payment options</p>
      <h2>Treat now, pay later</h2>
      <p>Care shouldn&rsquo;t have to wait. We partner with Cherry so you can split your bill into easy payments &mdash; no hard credit checks, true 0% APR options, and approvals up to $50,000. We also accept CareCredit, Trupanion, and all types of insurances.</p>
      <a class="btn btn-dark" href="{BASE}/payment-options/">See Payment Options</a>
    </div>
    <div class="pay-points">
      <div class="pp"><strong>60 sec</strong><span>to apply with Cherry</span></div>
      <div class="pp"><strong>0% APR</strong><span>options available</span></div>
      <div class="pp"><strong>No hard</strong><span>credit checks, ever</span></div>
    </div>
  </div>
</section>
""" + bookband() + footer()
page("", home)

# ---------------------------------------------------------------- SERVICES OVERVIEW
services = head("Services | Animal Clinic of Ives Dairy Road",
                "Wellness visits, urgent care and sick visits, surgery and dentistry, and USDA health certificates at Animal Clinic of Ives Dairy Road in Miami, FL.", "services") + f"""
<section class="pagehead">
  <div class="wrap">
    <p class="eyebrow">Our services</p>
    <h1>Explore what we offer</h1>
    <p class="lede">At our veterinary clinic, we&rsquo;re passionate about providing personalized, top-notch care for your furry friends. Our dedicated team is here to ensure your pets are happy and healthy every step of the way.</p>
  </div>
</section>
<section class="sec sec-tight">
  <div class="wrap list-grid">
    <a class="list-card" href="{BASE}/services/wellness/">
      <figure><img src="{BASE}/img/det-wellness.jpg" alt="Two veterinary professionals examining a dog on the table" loading="lazy"></figure>
      <div class="list-body">
        <h2>Wellness Visits</h2>
        <p>From a puppy or kitten&rsquo;s very first exam to senior wellness, vaccines, microchipping, parasite control, and nutrition — preventative care that keeps small problems small.</p>
        <span class="svc-go">View wellness care</span>
      </div>
    </a>
    <a class="list-card" href="{BASE}/services/urgent-care/">
      <figure><img src="{BASE}/img/det-urgent.jpg" alt="A beagle resting its head, feeling under the weather" loading="lazy"></figure>
      <div class="list-body">
        <h2>Urgent Care and Sick Visits</h2>
        <p>Itchy skin, tummy trouble, coughing, limping, ear and eye issues, lethargy, arthritis — when something&rsquo;s off, we offer same-day appointments whenever possible.</p>
        <span class="svc-go">View urgent care</span>
      </div>
    </a>
    <a class="list-card" href="{BASE}/services/surgery-dentistry/">
      <figure><img src="{BASE}/img/card-surgery2.jpg" alt="A focused surgical team at work in the operating room" loading="lazy"></figure>
      <div class="list-body">
        <h2>Surgery and Dentistry</h2>
        <p>Spays and neuters, mass removals, full mouth dental X-rays, cleaning and polishing, extractions, and bladder stone removal — performed with care and clear communication.</p>
        <span class="svc-go">View surgery &amp; dentistry</span>
      </div>
    </a>
    <a class="list-card" href="{BASE}/services/health-certificates/">
      <figure><img src="{BASE}/img/det-health-certs.jpg" alt="A dog riding in a bicycle basket on a city trip" loading="lazy"></figure>
      <div class="list-body">
        <h2>Health Certificates</h2>
        <p>USDA-certified health certificates, vaccines, and testing for domestic and international pet travel — start early and we&rsquo;ll make it smooth and stress-free.</p>
        <span class="svc-go">View health certificates</span>
      </div>
    </a>
  </div>
</section>
""" + bookband("Not sure which visit your pet needs?", f"Call us at {PHONE} and we&rsquo;ll point you in the right direction — same-day appointments whenever possible.") + footer()
page("services", services)

# ---------------------------------------------------------------- SERVICE DETAILS
def detail(slug, title, img, alt, intro, list_title, bullets, expect, extra=""):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    steps = "".join(f'<div class="step"><span class="step-n">0{i+1}</span><h3>{t}</h3><p>{p}</p></div>' for i,(t,p) in enumerate(expect))
    return head(f"{title} | Animal Clinic of Ives Dairy Road",
                f"{title} at Animal Clinic of Ives Dairy Road in Miami, FL. Call {PHONE} to book.", "services") + f"""
<section class="dethero">
  <figure class="dethero-img"><img src="{BASE}/img/{img}" alt="{alt}" fetchpriority="high"></figure>
  <div class="dethero-txt">
    <p class="eyebrow"><a href="{BASE}/services/">Services</a> / {title}</p>
    <h1>{title}</h1>
    <p>{intro}</p>
    <div class="hero-cta"><a class="btn btn-dark" href="{BASE}/appointments/">Book This Visit</a><a class="btn btn-ghost" href="{TEL}">Call {PHONE}</a></div>
  </div>
</section>
<section class="sec sec-cream">
  <div class="wrap two-col">
    <div>
      <h2>{list_title}</h2>
      <ul class="check-ul">{lis}</ul>
    </div>
    <div>
      <h2>What to expect</h2>
      <div class="steps">{steps}</div>
    </div>
  </div>
</section>
{extra}
""" + bookband(f"Book a {title.lower()} visit", f"Request an appointment online or call {PHONE} — same-day appointments whenever possible.") + footer()

page("services/wellness", detail("wellness","Wellness Visits","home-wellness.jpg",
    "A veterinarian giving a small dog a careful wellness exam",
    "Preventative care is the heart of a long, healthy life. Whether it&rsquo;s a brand-new puppy or kitten, an adult in their prime, or a senior who needs a closer eye, our wellness visits are built around your pet&rsquo;s age and lifestyle.",
    "Wellness care includes", wellness_bullets,
    [("A thorough exam","Dr. Ahuja examines your pet nose to tail and takes the time to hear what you&rsquo;ve noticed at home."),
     ("A plan for their stage of life","Vaccines, parasite prevention, weight and nutrition, and behavior — tailored to your pet, not a template."),
     ("Clear next steps","You leave knowing exactly what your pet needs now and what to watch for before the next visit.")]))

page("services/urgent-care", detail("urgent-care","Urgent Care and Sick Visits","home-urgent.jpg",
    "A pet owner comforting a dog that isn't feeling well at home",
    "When something&rsquo;s off — itching, vomiting, limping, coughing, low energy — don&rsquo;t wait and worry. We offer same-day appointments whenever possible, especially for our sick patients.",
    "Common problems we see", urgent_bullets,
    [("Call us first","Describe what&rsquo;s going on and we&rsquo;ll get you in as soon as possible — same-day whenever we can."),
     ("Diagnosis, explained","Dr. Ahuja has a passion for diagnosing and managing disease — and for making sure you understand what&rsquo;s happening and why."),
     ("Treatment and follow-up","We treat your pet, then stay with you: clear instructions, medications, and a plan to recheck if needed.")]))

page("services/surgery-dentistry", detail("surgery-dentistry","Surgery and Dentistry","home-surgery.jpg",
    "A veterinarian carefully examining a dog before a procedure",
    "From routine spays and neuters to dental cleanings and extractions, we handle surgical and dental care with careful monitoring, pain management, and honest communication at every step.",
    "Surgical and dental services", surgery_bullets,
    [("Pre-surgical assessment","Every procedure starts with an exam and the right pre-anesthetic testing so we know your pet is a safe candidate."),
     ("The procedure","Your pet is monitored closely throughout, with pain management planned before we ever begin."),
     ("Recovery at home","You get clear discharge instructions and a direct line to us for anything that doesn&rsquo;t look right.")]))

page("services/health-certificates", detail("health-certificates","Health Certificates","home-care.jpg",
    "A woman hugging her dog outdoors, ready for new adventures",
    "Planning to travel with your pet? Our USDA-certified veterinarian will work with you to provide vaccines, testing, and health certificates for both domestic and international travel.",
    "Travel paperwork we handle",
    ["Domestic health certificates","International health certificates","Travel vaccine requirements","Pre-travel testing","Microchip verification","USDA requirement guidance"],
    [("Start early","Please consult the USDA&rsquo;s pet travel guidelines as early as possible to avoid any travel delays — some destinations need months of lead time."),
     ("Exam and paperwork","We examine your pet, bring vaccines and testing up to the destination&rsquo;s requirements, and complete the certificate."),
     ("Travel with confidence","Our team is here to make the process smooth, safe, and stress-free for you and your pet.")],
    extra=f"""
<section class="sec">
  <div class="wrap note-band">
    <h2>One tip from our team</h2>
    <p class="lede">Every country — and every airline — has its own rules, and they change. The single best thing you can do is call us the moment you know your travel dates. We&rsquo;ll map the timeline backwards from your departure so nothing is left to the last minute.</p>
    <a class="btn btn-teal" href="{BASE}/appointments/">Start Your Travel Visit</a>
  </div>
</section>"""))

# ---------------------------------------------------------------- ABOUT
about = head("About | Your Veterinary Team | Animal Clinic of Ives Dairy Road",
             "Meet Dr. Aditi Ahuja, DVM and the veterinary team at Animal Clinic of Ives Dairy Road in Miami, FL.", "about") + f"""
<section class="pagehead">
  <div class="wrap">
    <p class="eyebrow">About us</p>
    <h1>Your Veterinary Team</h1>
    <p class="lede">A small team that knows your pet by name — voted a 2026 Neighborhood Fave by our neighbors on Nextdoor.</p>
  </div>
</section>

<section class="sec sec-tight">
  <div class="wrap vet-feature">
    <figure class="vet-photo"><img src="{BASE}/img/team/ahuja.jpg" alt="Dr. Aditi Ahuja, DVM, holding a small white dog at the clinic"></figure>
    <div class="vet-bio">
      <h2>Aditi Ahuja, <span class="dvm">DVM</span></h2>
      <p>Dr. Aditi Ahuja earned her Doctorate of Veterinary Medicine from Cornell University College of Veterinary Medicine, where she focused on Small Animal Medicine and was inducted into the Phi Zeta Veterinary Honor Society. She is also Fear Free Certified and an active member of the AVMA and Veterinary Business Management Association (VBMA).</p>
      <p>Dr. Ahuja has a passion for diagnosing and managing chronic diseases. She completed a rotating internship in Small Animal Medicine and Surgery at Friendship Hospital for Animals in Washington, D.C., gaining hands-on experience in emergency care and multiple specialties. While she once considered pursuing a residency in internal medicine, her true passion lay in guiding pet owners through the journey of early diagnosis, intervention, and lifelong care. She finds deep fulfillment in helping families understand their pets&rsquo; health and supporting them every step of the way.</p>
      <p>Outside of work, she enjoys spending time with her dogs, baking, and hosting board game nights.</p>
      <div class="doc-creds"><span>Cornell University DVM</span><span>Phi Zeta Honor Society</span><span>Fear Free Certified</span><span>AVMA &amp; VBMA Member</span></div>
    </div>
  </div>
</section>

<section class="groupband">
  <figure><img src="{BASE}/img/group.jpg" alt="The Animal Clinic of Ives Dairy Road team together at the front desk" loading="lazy"></figure>
  <p class="groupband-cap">The team at 1562 NE 205th Street — your pet&rsquo;s second home.</p>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">The people your pet will love</p>
      <h2>Your Veterinary Support Team</h2>
    </div>
    <div class="team-grid">
      <div class="tm"><figure><img src="{BASE}/img/team/karina.jpg" alt="Karina, receptionist" loading="lazy"></figure><h3>Karina</h3><p>Receptionist</p></div>
      <div class="tm"><figure><img src="{BASE}/img/team/lailah.jpg" alt="Lailah, veterinary technician" loading="lazy"></figure><h3>Lailah</h3><p>Veterinary Technician</p></div>
      <div class="tm"><figure><img src="{BASE}/img/team/frenchie.jpg" alt="Frenchie, veterinary technician" loading="lazy"></figure><h3>Frenchie</h3><p>Veterinary Technician</p></div>
      <div class="tm"><figure><img src="{BASE}/img/team/eveliz.jpg" alt="Eveliz, veterinary assistant" loading="lazy"></figure><h3>Eveliz</h3><p>Veterinary Assistant</p></div>
    </div>
  </div>
</section>

<section class="sec sec-cream">
  <div class="wrap split">
    <figure class="split-img"><img src="{BASE}/img/about-story.jpg" alt="A friendly front-desk team welcoming patients" loading="lazy"></figure>
    <div class="split-txt">
      <p class="eyebrow">How we work</p>
      <h2>Fear Free, and proud of it</h2>
      <p>A vet visit shouldn&rsquo;t be the scariest day of your pet&rsquo;s month. As a Fear Free Certified practice, we work to lower stress at every step — how we handle, how we schedule, even how the room feels — so pets come back happy to see us.</p>
      <p>We serve pets in North Miami Beach, Aventura, Sunny Isles, Hallandale Beach, and anyone willing to make the drive.</p>
      <a class="arrow-link" href="{BASE}/contact/">Visit us on Ives Dairy Road</a>
    </div>
  </div>
</section>
""" + bookband("Come meet us in person", "Book your pet&rsquo;s first visit — we&rsquo;ll take the time to get to know both of you.") + footer()
page("about", about)

# ---------------------------------------------------------------- APPOINTMENTS
appointments = head("Appointments | Animal Clinic of Ives Dairy Road",
                    "Schedule a time with us. Request an appointment by phone or manage visits in the free PetCare by DaySmart Vet app.", "") + f"""
<section class="dethero">
  <figure class="dethero-img"><img src="{BASE}/img/appointments-cat.jpg" alt="A gray tabby cat being held gently in a lap at the clinic" fetchpriority="high"></figure>
  <div class="dethero-txt">
    <p class="eyebrow">Appointments</p>
    <h1>Schedule a time with us</h1>
    <p>Looking to schedule a visit for your furry friend? Our caring veterinarians are here to ensure they get the best care possible. Book your appointment today and let us help keep your pet happy and healthy!</p>
    <div class="hero-cta"><a class="btn btn-teal" href="{TEL}">Request Appointment — {PHONE}</a></div>
    <p class="award-chip">2026 Fave Winner &mdash; voted by neighbors on Nextdoor</p>
  </div>
</section>

<section class="sec sec-cream">
  <div class="wrap split">
    <div class="split-txt">
      <p class="eyebrow">Pet portal</p>
      <h2>Download Our Free Pet Portal Mobile App!</h2>
      <p>We&rsquo;re excited to announce that we now have a pet portal mobile app! With the PetCare by DaySmart Vet mobile app, you can easily:</p>
      <ul class="check-ul">
        <li>Book, confirm, or cancel appointments</li>
        <li>Pay for appointment deposits and invoices</li>
        <li>Quickly access pet vitals and medical records</li>
      </ul>
      <p>To get started, simply download the PetCare app for iPhone or Android, create an account, and select <strong>&ldquo;Animal Clinic of Ives Dairy Road&rdquo;</strong> as your veterinarian within the app. It&rsquo;s that simple!</p>
      <div class="hero-cta"><a class="btn btn-dark" href="https://apps.apple.com/us/app/petcare-by-daysmart-vet/id1641860089" target="_blank" rel="noopener">Download for iOS</a><a class="btn btn-ghost" href="https://play.google.com/store/apps/details?id=com.daysmart.vet" target="_blank" rel="noopener">Download for Android</a></div>
    </div>
    <figure class="split-img"><img src="{BASE}/img/appointments.jpg" alt="A warm welcome at the clinic front desk" loading="lazy"></figure>
  </div>
</section>

<section class="sec">
  <div class="wrap two-col">
    <div>
      <h2>Good to know before you book</h2>
      <div class="steps">
        <div class="step"><span class="step-n">01</span><h3>Same-day when it matters</h3><p>We offer same-day appointments whenever possible, especially for our sick patients. Call us as early in the day as you can.</p></div>
        <div class="step"><span class="step-n">02</span><h3>Our hours</h3><p>Monday, Tuesday, Thursday and Friday 8AM&ndash;5PM &middot; Saturday 8AM&ndash;12PM &middot; closed Wednesday and Sunday.</p></div>
        <div class="step"><span class="step-n">03</span><h3>Where to find us</h3><p>{ADDR1}, {ADDR2} — serving North Miami Beach, Aventura, Sunny Isles, and Hallandale Beach.</p></div>
      </div>
    </div>
    <div class="contact-card">
      <h2>Request by phone or email</h2>
      <p class="big-tel"><a href="{TEL}">{PHONE}</a></p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p class="muted">Prefer to come by? Find directions and our full hours on the contact page.</p>
      <a class="btn btn-teal" href="{BASE}/contact/">Contact &amp; Directions</a>
    </div>
  </div>
</section>
""" + footer()
page("appointments", appointments)

# ---------------------------------------------------------------- PAYMENT OPTIONS
payment = head("Payment Options | Animal Clinic of Ives Dairy Road",
               "Treat now, pay later with Cherry — 0% APR options, no hard credit checks. We also accept CareCredit, Trupanion, and all types of insurances.", "payment") + f"""
<section class="pagehead">
  <div class="wrap">
    <p class="eyebrow">Payment options</p>
    <h1>Treat now, pay later</h1>
    <p class="lede">Your pet&rsquo;s care shouldn&rsquo;t have to wait for payday. We partner with <strong>Cherry</strong> to let you split your bill into easy monthly payments.</p>
  </div>
</section>

<section class="sec sec-tight">
  <div class="wrap cherry">
    <div class="cherry-main">
      <ul class="check-ul big">
        <li><strong>No hard credit checks</strong>, ever</li>
        <li><strong>True 0% APR</strong> options available</li>
        <li>Interest-bearing plans with APRs <strong>as low as 5.99%</strong></li>
        <li>Up to <strong>$50,000</strong> approvals</li>
        <li><strong>No hidden fees</strong></li>
      </ul>
      <div class="hero-cta"><a class="btn btn-teal" href="https://pay.withcherry.com" target="_blank" rel="noopener">See If You Qualify</a><a class="btn btn-ghost" href="https://pay.withcherry.com" target="_blank" rel="noopener">Manage Your Account</a></div>
      <div class="cherry-example">
        <h3>See an example of what you could pay</h3>
        <p>Curious what a <strong>$750</strong> treatment could look like per month? Applying takes 60 seconds, doesn&rsquo;t affect your credit, and shows your exact personalized options.</p>
        <a class="arrow-link" href="https://pay.withcherry.com" target="_blank" rel="noopener">Get personalized options</a>
        <p class="pay-mini"><span>&#10003; No hard credit checks, ever</span><span>&#10003; 60 seconds to apply</span></p>
        <p class="fineprint">0% APR and other promotional rates subject to eligibility. See footer for details.</p>
      </div>
    </div>
    <figure class="cherry-img"><img src="{BASE}/img/payment.jpg" alt="Two cats cuddled up together, perfectly content" loading="lazy"></figure>
  </div>
</section>

<section class="sec sec-cream">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Three simple steps</p><h2>How Cherry works</h2></div>
    <div class="steps steps-row">
      <div class="step"><span class="step-n">01</span><h3>See if you qualify</h3><p>It only takes 60 seconds to complete the application.</p></div>
      <div class="step"><span class="step-n">02</span><h3>Get care</h3><p>Use your approval to pay for your treatment.</p></div>
      <div class="step"><span class="step-n">03</span><h3>Pay over time</h3><p>Choose a plan length that fits your needs with 0% APR options.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap two-col">
    <div>
      <h2>What is Cherry?</h2>
      <p>Cherry is a buy now, pay later company making it fast and easy to pay for health and wellness purchases over time.</p>
      <div class="hero-cta"><a class="btn btn-ghost" href="https://withcherry.com/" target="_blank" rel="noopener">View All FAQs</a><a class="btn btn-ghost" href="https://withcherry.com/" target="_blank" rel="noopener">Visit Help Center</a></div>
    </div>
    <div>
      <h2>More ways to pay</h2>
      <p class="lede">We also accept <strong>CareCredit</strong>, <strong>Trupanion</strong>, and all types of insurances.</p>
      <p class="muted">Not sure if your plan is covered? Call us at <a href="{TEL}">{PHONE}</a> and we&rsquo;ll check together.</p>
    </div>
  </div>
</section>

<section class="sec sec-tight">
  <div class="wrap">
    <p class="fineprint block">These are examples only. 0% APR and other promotional rates subject to eligibility. Exact terms and APR depend on credit score and other factors. For example, a $400 payment plan with Cherry may cost $100/month over 3 months at 0% APR with down payment in the amount of monthly payment due at the time of purchase. Not every provider that uses Cherry will offer the payment plan terms listed above. Payment options through Cherry Technologies, Inc. are issued by the following lending partners: <a href="https://withcherry.com/lending-partners" target="_blank" rel="noopener">withcherry.com/lending-partners</a>. See <a href="https://withcherry.com/terms" target="_blank" rel="noopener">withcherry.com/terms</a> for details. Iowa only: borrowers are subject to Iowa state specific underwriting criteria. APR for all Iowa borrowers is capped at 20.99%. Cherry is committed to making its product accessible. For their accessibility statement and feedback form, see <a href="https://withcherry.com/accessibility" target="_blank" rel="noopener">withcherry.com/accessibility</a>.</p>
  </div>
</section>
""" + bookband("Questions about cost?", f"Call {PHONE} — we&rsquo;ll walk you through an estimate and your payment options before any treatment.") + footer()
page("payment-options", payment)

# ---------------------------------------------------------------- CONTACT
contact = head("Contact | Animal Clinic of Ives Dairy Road",
               "Contact Animal Clinic of Ives Dairy Road: 1562 NE 205th St, Miami, FL 33179. Call (305) 653-3939.", "contact") + f"""
<section class="pagehead">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Contact Us</h1>
    <p class="lede">We&rsquo;d love to hear from you! Whether you have questions about your pet&rsquo;s health, need to schedule an appointment, or just want to learn more about our services, our team is here to help.</p>
  </div>
</section>

<section class="sec sec-tight">
  <div class="wrap contact-grid">
    <div class="contact-card">
      <h2>Reach us</h2>
      <p class="big-tel"><a href="{TEL}">{PHONE}</a></p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a><br>Fax: (786) 471-4053</p>
      <p><a href="{MAPQ}" target="_blank" rel="noopener">{ADDR1}, {ADDR2}</a></p>
      <table class="hours dark">{"".join(f'<tr><td>{d}</td><td class="{ "closed" if h=="Closed" else "" }">{h}</td></tr>' for d,h in HOURS)}</table>
      <a class="btn btn-teal" href="{BASE}/appointments/">Request Appointment</a>
    </div>
    <div class="contact-side">
      <div class="mapframe"><iframe src="{MAPEMBED}" title="Map to Animal Clinic of Ives Dairy Road" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
      <figure class="contact-photo"><img src="{BASE}/img/contact.jpg" alt="A woman hugging her poodle on a park bench" loading="lazy"></figure>
    </div>
  </div>
</section>

<section class="sec sec-cream">
  <div class="wrap note-band">
    <h2>Who we serve</h2>
    <p class="lede">We service pets in North Miami Beach, Aventura, Sunny Isles, Hallandale Beach, and anyone willing to make the drive. We offer same-day appointments whenever possible, especially for our sick patients. Reach out by phone or email and we will get back to you as soon as possible — your pet&rsquo;s well-being is our top priority.</p>
  </div>
</section>
""" + footer()
page("contact", contact)

print("ALL PAGES GENERATED")
