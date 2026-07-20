import Image from "next/image";
import Link from "next/link";
import ContactForm from "./ContactForm";

const PORTFOLIO = [
  {
    name: "Dune Buggy",
    tag: "Food Truck · Grand Rapids, MI",
    img: "/portfolio/dunebuggy.jpg",
    href: "/dunebuggy/",
  },
  {
    name: "Orange Beach Fish Charter Services",
    tag: "Fishing Charter · Orange Beach, AL",
    img: "/portfolio/orangebeachfish.jpg",
    href: "/orangebeachfish/",
  },
];

const STEPS = [
  {
    n: "01",
    title: "We build your site first",
    body: "No deposit, no contract. We design and build your real website using your real business info before you pay a cent.",
  },
  {
    n: "02",
    title: "You review & tell us what to change",
    body: "Photos, colors, wording, prices — whatever you want different, we fix it. As many rounds as it takes.",
  },
  {
    n: "03",
    title: "Pay only if you love it",
    body: "$300 flat. No monthly fee, no lock-in. If you don't love it, you owe us nothing and walk away.",
  },
];

const FAQS = [
  {
    q: "Why is it only $300?",
    a: "We're a small, lean operation without agency overhead — and we'd rather earn your trust with a fair price than oversell you on your first site. Most of our clients come back for our growth services once the site's live.",
  },
  {
    q: "Is there a catch — hidden fees, contracts?",
    a: "No. $300 flat, once, when you're happy. No monthly hosting fee, no contract. If you ever want ongoing SEO, content, or lead-gen help after that, we'll talk about it separately — never bundled into the first sale.",
  },
  {
    q: "What if I want changes after it's live?",
    a: "Minor updates (a new phone number, a price change, a new photo) are free — just ask. Bigger redesigns are quoted separately.",
  },
  {
    q: "Do I own the site?",
    a: "Yes. Once you pay, the site and its domain setup are yours. We're not a subscription you can get locked into.",
  },
];

export default function Home() {
  return (
    <>
      {/* ---------- Nav ---------- */}
      <header className="sticky top-0 z-50 border-b border-[var(--border)] bg-[var(--background)]/90 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link href="#top" className="flex items-center gap-2.5">
            <Image
              src="/logo-mark.png"
              alt=""
              width={536}
              height={384}
              className="h-8 w-auto md:h-9"
              priority
            />
            <span className="font-[family-name:var(--font-display)] text-lg font-bold tracking-tight">
              WebBlaze
            </span>
          </Link>
          <nav className="hidden items-center gap-8 text-sm font-medium text-[var(--foreground-soft)] md:flex">
            <a href="#work" className="hover:text-[var(--foreground)] transition-colors">
              Our Work
            </a>
            <a href="#how" className="hover:text-[var(--foreground)] transition-colors">
              How It Works
            </a>
            <a href="#pricing" className="hover:text-[var(--foreground)] transition-colors">
              Pricing
            </a>
            <a href="#faq" className="hover:text-[var(--foreground)] transition-colors">
              FAQ
            </a>
          </nav>
          <a
            href="#contact"
            className="rounded-full px-5 py-2.5 text-sm font-semibold text-white shadow-md shadow-red-900/10 transition-transform hover:-translate-y-0.5 flame-gradient"
          >
            Get your free build
          </a>
        </div>
      </header>

      <main id="top" className="flex-1">
        {/* ---------- Hero ---------- */}
        <section className="relative overflow-hidden">
          <div
            className="pointer-events-none absolute -top-32 right-[-10%] h-[520px] w-[520px] rounded-full opacity-25 blur-3xl flame-gradient"
            aria-hidden
          />
          <div className="mx-auto max-w-6xl px-6 pb-24 pt-20 md:pt-28">
            <span className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--surface-muted)] px-4 py-1.5 text-xs font-semibold uppercase tracking-wide text-[var(--slate)]">
              We build it before you pay
            </span>
            <h1 className="mt-6 max-w-3xl font-[family-name:var(--font-display)] text-4xl font-bold leading-[1.05] tracking-tight md:text-6xl">
              A real website for your business,{" "}
              <span className="flame-text-gradient">for $300 flat.</span>
            </h1>
            <p className="mt-6 max-w-xl text-lg text-[var(--foreground-soft)]">
              No monthly fees. No contracts. We design and build your site first —
              you only pay once you love it. Then, if you want, we help you get
              found and get booked.
            </p>
            <div className="mt-8 flex flex-wrap items-center gap-4">
              <a
                href="#contact"
                className="rounded-full px-7 py-3.5 text-sm font-semibold text-white shadow-lg shadow-red-900/20 transition-transform hover:-translate-y-0.5 flame-gradient"
              >
                Get your free build
              </a>
              <a
                href="#work"
                className="rounded-full border border-[var(--border)] px-7 py-3.5 text-sm font-semibold text-[var(--foreground)] transition-colors hover:bg-[var(--surface-muted)]"
              >
                See our work
              </a>
            </div>
            <div className="mt-10 flex flex-wrap gap-x-8 gap-y-2 text-sm font-medium text-[var(--foreground-soft)]">
              <span>$300 flat — no hidden fees</span>
              <span>Built before you pay</span>
              <span>No contracts, ever</span>
            </div>
          </div>
        </section>

        {/* ---------- Portfolio ---------- */}
        <section id="work" className="border-t border-[var(--border)] bg-[var(--surface-muted)] py-24">
          <div className="mx-auto max-w-6xl px-6">
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--burnt)]">
              Our Work
            </p>
            <h2 className="mt-2 font-[family-name:var(--font-display)] text-3xl font-bold tracking-tight md:text-4xl">
              Real sites, built for real businesses.
            </h2>
            <p className="mt-4 max-w-xl text-[var(--foreground-soft)]">
              Every site is designed from scratch around the business it&apos;s
              for — never a generic template with a new logo dropped in.
            </p>
            <div className="mt-12 grid gap-6 md:grid-cols-2">
              {PORTFOLIO.map((p) => (
                <a
                  key={p.name}
                  href={p.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group overflow-hidden rounded-2xl border border-[var(--border)] bg-[var(--surface)] shadow-sm transition-shadow hover:shadow-xl"
                >
                  <div className="relative aspect-[16/10] w-full overflow-hidden bg-[var(--surface-muted)]">
                    <Image
                      src={p.img}
                      alt={`${p.name} website preview`}
                      fill
                      className="object-cover object-top transition-transform duration-500 group-hover:scale-105"
                      sizes="(min-width: 768px) 50vw, 100vw"
                    />
                  </div>
                  <div className="flex items-center justify-between p-5">
                    <div>
                      <h3 className="font-[family-name:var(--font-display)] font-semibold">
                        {p.name}
                      </h3>
                      <p className="text-sm text-[var(--foreground-soft)]">{p.tag}</p>
                    </div>
                    <span className="text-sm font-semibold text-[var(--burnt)]">
                      View site →
                    </span>
                  </div>
                </a>
              ))}
            </div>
          </div>
        </section>

        {/* ---------- How it works ---------- */}
        <section id="how" className="py-24">
          <div className="mx-auto max-w-6xl px-6">
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--burnt)]">
              How It Works
            </p>
            <h2 className="mt-2 font-[family-name:var(--font-display)] text-3xl font-bold tracking-tight md:text-4xl">
              Zero risk. You see it before you pay for it.
            </h2>
            <div className="mt-12 grid gap-8 md:grid-cols-3">
              {STEPS.map((s) => (
                <div key={s.n} className="rounded-2xl border border-[var(--border)] bg-[var(--surface)] p-7">
                  <span className="font-[family-name:var(--font-display)] text-3xl font-bold flame-text-gradient">
                    {s.n}
                  </span>
                  <h3 className="mt-4 font-[family-name:var(--font-display)] text-lg font-semibold">
                    {s.title}
                  </h3>
                  <p className="mt-2 text-sm text-[var(--foreground-soft)]">{s.body}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ---------- Pricing ---------- */}
        <section id="pricing" className="border-t border-[var(--border)] bg-[var(--surface-muted)] py-24">
          <div className="mx-auto max-w-4xl px-6 text-center">
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--burnt)]">
              Pricing
            </p>
            <h2 className="mt-2 font-[family-name:var(--font-display)] text-3xl font-bold tracking-tight md:text-4xl">
              One price. Nothing hidden.
            </h2>
            <div className="mx-auto mt-12 max-w-md rounded-2xl border border-[var(--border)] bg-[var(--surface)] p-10 shadow-xl shadow-red-900/5">
              <p className="font-[family-name:var(--font-display)] text-5xl font-bold">
                $300
              </p>
              <p className="mt-1 text-sm font-medium text-[var(--foreground-soft)]">
                flat, one time — no monthly fee
              </p>
              <ul className="mt-8 space-y-3 text-left text-sm text-[var(--foreground-soft)]">
                {[
                  "Custom-designed site built for your business",
                  "Mobile-friendly, fast, and easy to update",
                  "Built first — pay only once you're happy",
                  "Unlimited rounds of changes before you pay",
                  "You own it — no contract, no lock-in",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-2">
                    <span className="mt-0.5 text-[var(--ember)]">✓</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
              <a
                href="#contact"
                className="mt-8 block rounded-full px-7 py-3.5 text-center text-sm font-semibold text-white shadow-md shadow-red-900/20 transition-transform hover:-translate-y-0.5 flame-gradient"
              >
                Get your free build
              </a>
            </div>
            <p className="mx-auto mt-8 max-w-md text-sm text-[var(--foreground-soft)]">
              Want ongoing help getting found on Google and booked more? We offer
              growth &amp; lead-gen services too — we&apos;ll talk about that
              separately, after your site is live and you&apos;re happy with it.
            </p>
          </div>
        </section>

        {/* ---------- FAQ ---------- */}
        <section id="faq" className="py-24">
          <div className="mx-auto max-w-3xl px-6">
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--burnt)]">
              FAQ
            </p>
            <h2 className="mt-2 font-[family-name:var(--font-display)] text-3xl font-bold tracking-tight md:text-4xl">
              Questions people actually ask.
            </h2>
            <div className="mt-10 divide-y divide-[var(--border)] rounded-2xl border border-[var(--border)] bg-[var(--surface)]">
              {FAQS.map((f) => (
                <details key={f.q} className="group p-6">
                  <summary className="flex cursor-pointer list-none items-center justify-between font-[family-name:var(--font-display)] font-semibold">
                    {f.q}
                    <span className="ml-4 text-[var(--foreground-soft)] transition-transform group-open:rotate-45">
                      +
                    </span>
                  </summary>
                  <p className="mt-3 text-sm text-[var(--foreground-soft)]">{f.a}</p>
                </details>
              ))}
            </div>
          </div>
        </section>

        {/* ---------- Final CTA ---------- */}
        <section
          id="contact"
          className="relative overflow-hidden py-24 text-white flame-gradient"
        >
          <div className="mx-auto max-w-3xl px-6 text-center">
            <h2 className="font-[family-name:var(--font-display)] text-3xl font-bold tracking-tight md:text-4xl">
              Let&apos;s build your site.
            </h2>
            <p className="mx-auto mt-4 max-w-xl text-white/90">
              Tell us a bit about your business and we&apos;ll start building —
              free, no obligation. You only pay if you love it.
            </p>
            <div className="mx-auto mt-8 max-w-lg">
              <ContactForm />
            </div>
          </div>
        </section>
      </main>

      {/* ---------- Footer ---------- */}
      <footer className="border-t border-[var(--border)] py-10">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-6 text-sm text-[var(--foreground-soft)] md:flex-row">
          <div className="flex items-center gap-2">
            <Image src="/logo-mark.png" alt="" width={536} height={384} className="h-5 w-auto" />
            <span>© {new Date().getFullYear()} WebBlaze</span>
          </div>
          <a href="mailto:zayden@webblaze.io" className="hover:text-[var(--foreground)] transition-colors">
            zayden@webblaze.io
          </a>
        </div>
      </footer>
    </>
  );
}
