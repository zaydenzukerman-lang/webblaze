"use client";

import Image from "next/image";
import { motion, useReducedMotion } from "framer-motion";
import { Nav, Footer, Reveal, Stat, Marquee, Magnetic } from "@/components/site";
import ContactForm from "./ContactForm";

const WORK = [
  {
    name: "Sun Finance",
    tag: "Mortgage & Lending · Louisiana",
    desc: "A 65-year-old lender, brought into the modern era — trust-first, compliant, premium.",
    img: "/portfolio/sunfinance.jpg",
    href: "https://sunfinance.webblaze.io",
  },
  {
    name: "Orange Beach Fish Charter",
    tag: "Fishing Charter · Alabama",
    desc: "A dead website replaced with a coastal, booking-focused site that actually converts.",
    img: "/portfolio/orangebeachfish.jpg",
    href: "https://orangebeachfish.webblaze.io",
  },
  {
    name: "Dune Buggy",
    tag: "Food Truck · Grand Rapids, MI",
    desc: "Bold, appetite-first branding for a food truck that lived only on Facebook.",
    img: "/portfolio/dunebuggy.jpg",
    href: "https://dunebuggy.webblaze.io",
  },
];

const STEPS = [
  { n: "01", t: "We build it first", d: "No deposit, no contract. We design and build your real site using your real business info — before you pay a cent." },
  { n: "02", t: "You shape it", d: "Photos, copy, colors, prices — tell us what to change and we refine it. As many rounds as it takes to make it yours." },
  { n: "03", t: "Pay only if you love it", d: "$300 flat, once. No monthly fees, no lock-in. Don't love it? You owe nothing and walk away." },
];

const FAQS = [
  { q: "Why is it only $300?", a: "We're lean, with no agency overhead — and we'd rather earn your trust with a fair first project than oversell you. Most clients come back for growth services once the site's live." },
  { q: "Is there a catch — hidden fees or contracts?", a: "No. $300 flat, once, when you're happy. No monthly hosting fee, no contract. Any ongoing SEO or lead-gen help is discussed separately, never bundled into the first sale." },
  { q: "What if I want changes after it's live?", a: "Small updates — a new number, a price change, a fresh photo — are free. Just ask. Larger redesigns are quoted separately." },
  { q: "Do I own the site?", a: "Completely. Once you pay, the site and its domain setup are yours. We're not a subscription you can get locked into." },
];

export default function Home() {
  const reduce = useReducedMotion();
  return (
    <>
      <Nav onDark />

      {/* ============ HERO ============ */}
      <header className="relative isolate overflow-hidden bg-[var(--noir)] text-[var(--on-noir)] grain">
        {/* animated flame glow */}
        <motion.div
          aria-hidden
          className="pointer-events-none absolute -top-40 right-[-12%] -z-0 h-[640px] w-[640px] rounded-full blur-[110px]"
          style={{ background: "radial-gradient(circle,rgba(234,88,12,.55),rgba(212,44,31,.25) 45%,transparent 70%)" }}
          animate={reduce ? {} : { scale: [1, 1.12, 1], opacity: [0.7, 0.95, 0.7] }}
          transition={{ duration: 9, repeat: Infinity, ease: "easeInOut" }}
        />
        <div className="relative z-10 mx-auto max-w-[1180px] px-6 pb-24 pt-40 md:pt-48">
          <motion.p
            className="eyebrow text-[var(--ember)]"
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            Websites & growth · built before you pay
          </motion.p>
          <h1 className="mt-6 max-w-[16ch] text-[length:var(--fs-display)] font-bold leading-[0.98]">
            {["Your business", "deserves a site", "that "].map((line, i) => (
              <motion.span
                key={i}
                className="block"
                initial={reduce ? false : { opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.15 + i * 0.12, ease: [0.22, 1, 0.36, 1] }}
              >
                {line}
                {i === 2 && <span className="flame-text">earns its keep.</span>}
              </motion.span>
            ))}
          </h1>
          <motion.p
            className="mt-8 max-w-[48ch] text-[length:var(--fs-lead)] text-[var(--on-noir-soft)]"
            initial={reduce ? false : { opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.6 }}
          >
            We design and build your website first — you only pay the $300 flat fee once you love it.
            No monthly fees. No contracts. Then, when you're ready, we help you get found and get booked.
          </motion.p>
          <motion.div
            className="mt-10 flex flex-wrap items-center gap-4"
            initial={reduce ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.75 }}
          >
            <Magnetic>
              <a href="#contact" className="btn btn-flame">Get your free build →</a>
            </Magnetic>
            <a href="#work" className="btn btn-ghost-noir">See our work</a>
          </motion.div>
        </div>
        <Marquee items={["$300 flat", "No monthly fees", "Built before you pay", "You own it", "No contracts", "Local SEO", "Lead generation"]} />
      </header>

      {/* ============ STATS ============ */}
      <section className="relative isolate bg-[var(--noir-2)] text-[var(--on-noir)] grain">
        <div className="relative z-10 mx-auto grid max-w-[1180px] grid-cols-2 gap-x-6 gap-y-12 px-6 py-20 md:grid-cols-4">
          {[
            { v: 300, prefix: "$", label: "Flat price. Nothing hidden." },
            { v: 0, label: "Upfront. Pay only if you love it." },
            { v: 3, suffix: "-day", label: "First draft in your inbox." },
            { v: 100, suffix: "%", label: "Yours. No lock-in, ever." },
          ].map((s, i) => (
            <Reveal key={i} delay={i * 0.08}>
              <Stat value={s.v} prefix={s.prefix} suffix={s.suffix} label={s.label} />
            </Reveal>
          ))}
        </div>
      </section>

      {/* ============ WORK ============ */}
      <section id="work" className="mx-auto max-w-[1180px] px-6 py-28">
        <Reveal><p className="eyebrow text-[var(--flame)]">Selected Work</p></Reveal>
        <Reveal delay={0.05}>
          <h2 className="mt-3 max-w-[18ch] text-[length:var(--fs-h2)] font-bold">
            Real sites, built for real businesses.
          </h2>
        </Reveal>
        <Reveal delay={0.1}>
          <p className="mt-5 max-w-[54ch] text-[var(--ink-soft)] text-[length:var(--fs-body)]">
            Every site is designed from scratch around the business it&apos;s for — never a template
            with a new logo dropped on top. Hover to explore.
          </p>
        </Reveal>

        <div className="mt-14 space-y-6">
          {WORK.map((w, i) => (
            <Reveal key={w.name} delay={i * 0.06}>
              <a
                href={w.href}
                target="_blank"
                rel="noopener noreferrer"
                className="group grid overflow-hidden rounded-[var(--radius)] border border-[var(--line)] bg-white md:grid-cols-[1.05fr_1fr]"
              >
                <div className="relative aspect-[16/11] overflow-hidden bg-[var(--paper-2)]">
                  <Image
                    src={w.img}
                    alt={`${w.name} website`}
                    fill
                    className="object-cover object-top transition-transform duration-[900ms] ease-[cubic-bezier(0.22,1,0.36,1)] group-hover:scale-[1.06]"
                    sizes="(min-width:768px) 55vw, 100vw"
                  />
                </div>
                <div className="flex flex-col justify-center gap-3 p-8 md:p-12">
                  <span className="eyebrow text-[var(--flame)]">{w.tag}</span>
                  <h3 className="text-[length:var(--fs-h3)] font-bold">{w.name}</h3>
                  <p className="max-w-[40ch] text-[var(--ink-soft)]">{w.desc}</p>
                  <span className="mt-2 inline-flex items-center gap-2 font-[family-name:var(--font-space-grotesk)] text-sm font-semibold text-[var(--burnt)]">
                    View live site
                    <span className="transition-transform duration-300 group-hover:translate-x-1.5">→</span>
                  </span>
                </div>
              </a>
            </Reveal>
          ))}
        </div>
      </section>

      {/* ============ PROCESS ============ */}
      <section id="process" className="relative isolate overflow-hidden bg-[var(--noir)] text-[var(--on-noir)] grain">
        <div className="relative z-10 mx-auto max-w-[1180px] px-6 py-28">
          <Reveal><p className="eyebrow text-[var(--ember)]">How it works</p></Reveal>
          <Reveal delay={0.05}>
            <h2 className="mt-3 max-w-[20ch] text-[length:var(--fs-h2)] font-bold">
              Zero risk. You see it before you pay for it.
            </h2>
          </Reveal>
          <div className="mt-16 grid gap-px overflow-hidden rounded-[var(--radius)] border border-[var(--noir-line)] bg-[var(--noir-line)] md:grid-cols-3">
            {STEPS.map((s, i) => (
              <Reveal key={s.n} delay={i * 0.1} className="bg-[var(--noir)]">
                <div className="h-full p-9">
                  <div className="flame-text font-[family-name:var(--font-space-grotesk)] text-5xl font-bold">{s.n}</div>
                  <h3 className="mt-5 text-[length:var(--fs-h3)] font-bold">{s.t}</h3>
                  <p className="mt-3 text-[var(--on-noir-soft)]">{s.d}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* ============ PRICING ============ */}
      <section id="pricing" className="mx-auto max-w-[1180px] px-6 py-28">
        <div className="grid items-center gap-14 md:grid-cols-2">
          <div>
            <Reveal><p className="eyebrow text-[var(--flame)]">Pricing</p></Reveal>
            <Reveal delay={0.05}>
              <h2 className="mt-3 text-[length:var(--fs-h2)] font-bold">One price. Nothing hidden.</h2>
            </Reveal>
            <Reveal delay={0.1}>
              <p className="mt-5 max-w-[42ch] text-[var(--ink-soft)] text-[length:var(--fs-body)]">
                Want ongoing help getting found on Google and booked more often? We offer growth &amp;
                lead-gen services too — but only after your site is live and you&apos;re happy. Never
                bundled, never pushy.
              </p>
            </Reveal>
          </div>
          <Reveal delay={0.1}>
            <div className="relative isolate overflow-hidden rounded-[24px] border border-[var(--line)] bg-white p-9 shadow-[0_30px_70px_-40px_rgba(0,0,0,.4)]">
              <div aria-hidden className="pointer-events-none absolute -right-16 -top-16 h-52 w-52 rounded-full blur-3xl" style={{ background: "radial-gradient(circle,rgba(234,88,12,.28),transparent 70%)" }} />
              <div className="relative z-10">
                <div className="flex items-end gap-2">
                  <span className="font-[family-name:var(--font-space-grotesk)] text-6xl font-bold tracking-tight">$300</span>
                  <span className="mb-2 text-sm text-[var(--ink-soft)]">flat · one time</span>
                </div>
                <ul className="mt-8 space-y-3.5 text-[0.97rem] text-[var(--ink-soft)]">
                  {["Custom-designed site, built for your business","Fast, mobile-first, easy to update","Built first — pay only once you're happy","Unlimited revisions before you pay","You own it — no contract, no lock-in"].map((f) => (
                    <li key={f} className="flex items-start gap-3">
                      <span className="mt-0.5 grid h-5 w-5 flex-none place-items-center rounded-full flame-bg text-[11px] text-white">✓</span>
                      {f}
                    </li>
                  ))}
                </ul>
                <Magnetic>
                  <a href="#contact" className="btn btn-flame mt-9 w-full">Get your free build</a>
                </Magnetic>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* ============ FAQ ============ */}
      <section id="faq" className="mx-auto max-w-[860px] px-6 pb-28">
        <Reveal><p className="eyebrow text-[var(--flame)]">FAQ</p></Reveal>
        <Reveal delay={0.05}>
          <h2 className="mt-3 text-[length:var(--fs-h2)] font-bold">Questions people actually ask.</h2>
        </Reveal>
        <div className="mt-12 divide-y divide-[var(--line)] border-y border-[var(--line)]">
          {FAQS.map((f, i) => (
            <Reveal key={f.q} delay={i * 0.05}>
              <details className="group py-6">
                <summary className="flex cursor-pointer list-none items-center justify-between gap-6 font-[family-name:var(--font-space-grotesk)] text-[1.08rem] font-semibold">
                  {f.q}
                  <span className="grid h-8 w-8 flex-none place-items-center rounded-full border border-[var(--line)] text-[var(--flame)] transition-transform duration-300 group-open:rotate-45">+</span>
                </summary>
                <p className="mt-4 max-w-[62ch] text-[var(--ink-soft)] leading-relaxed">{f.a}</p>
              </details>
            </Reveal>
          ))}
        </div>
      </section>

      {/* ============ CONTACT ============ */}
      <section id="contact" className="relative isolate overflow-hidden bg-[var(--noir)] text-[var(--on-noir)] grain">
        <div aria-hidden className="pointer-events-none absolute -bottom-40 left-[-10%] h-[560px] w-[560px] rounded-full blur-[120px]" style={{ background: "radial-gradient(circle,rgba(234,88,12,.4),transparent 70%)" }} />
        <div className="relative z-10 mx-auto grid max-w-[1180px] gap-14 px-6 py-28 md:grid-cols-[1fr_1fr] md:items-center">
          <div>
            <Reveal><p className="eyebrow text-[var(--ember)]">Start a project</p></Reveal>
            <Reveal delay={0.05}>
              <h2 className="mt-3 text-[length:var(--fs-h2)] font-bold">Let&apos;s build your site.</h2>
            </Reveal>
            <Reveal delay={0.1}>
              <p className="mt-5 max-w-[42ch] text-[var(--on-noir-soft)] text-[length:var(--fs-body)]">
                Tell us about your business and we&apos;ll start building — free, no obligation.
                You only pay if you love it.
              </p>
            </Reveal>
            <Reveal delay={0.15}>
              <a href="mailto:zayden@webblaze.io" className="mt-6 inline-block font-[family-name:var(--font-space-grotesk)] text-lg text-[var(--ember)] hover:text-[var(--flame-2)]">
                zayden@webblaze.io
              </a>
            </Reveal>
          </div>
          <Reveal delay={0.1}>
            <ContactForm />
          </Reveal>
        </div>
      </section>

      <Footer />
    </>
  );
}
