"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import {
  motion,
  useInView,
  useMotionValue,
  useSpring,
  useReducedMotion,
} from "framer-motion";

/* ---------------- Reveal ---------------- */
export function Reveal({
  children,
  delay = 0,
  y = 26,
  className = "",
  as = "div",
}: {
  children: React.ReactNode;
  delay?: number;
  y?: number;
  className?: string;
  as?: "div" | "span" | "li" | "h2" | "p";
}) {
  const reduce = useReducedMotion();
  const MotionTag = motion[as] as typeof motion.div;
  return (
    <MotionTag
      className={className}
      initial={reduce ? false : { opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{ duration: 0.75, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </MotionTag>
  );
}

/* ---------------- Stat counter ---------------- */
export function Stat({
  value,
  suffix = "",
  prefix = "",
  label,
}: {
  value: number;
  suffix?: string;
  prefix?: string;
  label: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-60px" });
  const [n, setN] = useState(0);
  const reduce = useReducedMotion();
  useEffect(() => {
    if (!inView) return;
    if (reduce) {
      setN(value);
      return;
    }
    let raf = 0;
    const dur = 1400;
    let start = 0;
    const step = (t: number) => {
      if (!start) start = t;
      const p = Math.min((t - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      setN(Math.round(eased * value));
      if (p < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [inView, value, reduce]);
  return (
    <div ref={ref}>
      <div className="font-[family-name:var(--font-space-grotesk)] font-bold leading-none tracking-tight text-[clamp(2.4rem,1.6rem+3vw,4rem)]">
        {prefix}
        {n}
        {suffix}
      </div>
      <div className="mt-2 text-sm text-[var(--on-noir-soft)]">{label}</div>
    </div>
  );
}

/* ---------------- Marquee ---------------- */
export function Marquee({ items }: { items: string[] }) {
  const row = [...items, ...items];
  return (
    <div className="relative overflow-hidden border-y border-[var(--noir-line)] py-5">
      <div className="flex w-max animate-[marquee_28s_linear_infinite] gap-10 whitespace-nowrap">
        {row.map((t, i) => (
          <span
            key={i}
            className="flex items-center gap-10 font-[family-name:var(--font-space-grotesk)] text-lg font-medium text-[var(--on-noir-soft)]"
          >
            {t}
            <span className="text-[var(--flame-2)]">✳</span>
          </span>
        ))}
      </div>
      <style>{`@keyframes marquee{to{transform:translateX(-50%)}}`}</style>
    </div>
  );
}

/* ---------------- Magnetic wrapper ---------------- */
export function Magnetic({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const sx = useSpring(x, { stiffness: 250, damping: 18 });
  const sy = useSpring(y, { stiffness: 250, damping: 18 });
  return (
    <motion.div
      ref={ref}
      style={{ x: sx, y: sy, display: "inline-flex" }}
      onMouseMove={(e) => {
        if (reduce || !ref.current) return;
        const r = ref.current.getBoundingClientRect();
        x.set((e.clientX - (r.left + r.width / 2)) * 0.25);
        y.set((e.clientY - (r.top + r.height / 2)) * 0.35);
      }}
      onMouseLeave={() => {
        x.set(0);
        y.set(0);
      }}
    >
      {children}
    </motion.div>
  );
}

/* ---------------- Nav ---------------- */
export function Nav({ onDark = true }: { onDark?: boolean }) {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const on = () => setScrolled(window.scrollY > 24);
    on();
    addEventListener("scroll", on, { passive: true });
    return () => removeEventListener("scroll", on);
  }, []);

  // In-page anchor scrolling. Native hash nav lands wrong here (overflow-x +
  // reveal transforms), so intercept same-page "#id" / "/#id" links and
  // scroll manually — reliable everywhere.
  useEffect(() => {
    const onClick = (e: MouseEvent) => {
      const a = (e.target as HTMLElement).closest?.("a[href*='#']") as HTMLAnchorElement | null;
      if (!a) return;
      const href = a.getAttribute("href") || "";
      const hashOnly = href.startsWith("#");
      const rootHash = href.startsWith("/#") && location.pathname === "/";
      if (!hashOnly && !rootHash) return;
      const id = href.slice(href.indexOf("#") + 1);
      const el = id && document.getElementById(id);
      if (!el) return;
      e.preventDefault();
      const y = el.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({
        top: y,
        behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth",
      });
      history.replaceState(null, "", href);
    };
    document.addEventListener("click", onClick);
    return () => document.removeEventListener("click", onClick);
  }, []);
  const light = scrolled || !onDark;
  return (
    <header
      className="fixed inset-x-0 top-0 z-50 transition-[background,box-shadow,border-color] duration-300"
      style={{
        background: light ? "rgba(251,250,248,0.82)" : "transparent",
        backdropFilter: light ? "blur(14px)" : "none",
        borderBottom: light ? "1px solid var(--line)" : "1px solid transparent",
      }}
    >
      <div className="mx-auto flex max-w-[1180px] items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-2.5">
          <Image src="/logo-mark.png" alt="" width={536} height={384} className="h-8 w-auto" priority />
          <span
            className="font-[family-name:var(--font-space-grotesk)] text-lg font-bold tracking-tight transition-colors"
            style={{ color: light ? "var(--ink)" : "var(--on-noir)" }}
          >
            WebBlaze
          </span>
        </Link>
        <nav
          className="hidden items-center gap-9 text-[0.92rem] font-medium md:flex transition-colors"
          style={{ color: light ? "var(--ink-soft)" : "var(--on-noir-soft)" }}
        >
          {[
            ["Work", "/#work"],
            ["Process", "/#process"],
            ["Pricing", "/#pricing"],
            ["FAQ", "/#faq"],
          ].map(([t, h]) => (
            <a key={t} href={h} className="transition-colors hover:text-[var(--flame)]">
              {t}
            </a>
          ))}
        </nav>
        <Magnetic>
          <a href="/#contact" className="btn btn-flame !px-6 !py-3 !text-sm">
            Start a project
          </a>
        </Magnetic>
      </div>
    </header>
  );
}

/* ---------------- Footer ---------------- */
export function Footer() {
  return (
    <footer className="relative isolate overflow-hidden bg-[var(--noir)] text-[var(--on-noir)] grain">
      <div className="relative z-10 mx-auto max-w-[1180px] px-6 py-16">
        <div className="grid gap-12 md:grid-cols-[1.5fr_1fr_1fr]">
          <div>
            <div className="flex items-center gap-2.5">
              <Image src="/logo-mark.png" alt="" width={536} height={384} className="h-7 w-auto" />
              <span className="font-[family-name:var(--font-space-grotesk)] text-lg font-bold">WebBlaze</span>
            </div>
            <p className="mt-4 max-w-xs text-sm leading-relaxed text-[var(--on-noir-soft)]">
              Websites and growth for small businesses. Built first — you only pay when you love it.
            </p>
            <a
              href="mailto:zayden@webblaze.io"
              className="mt-5 inline-block font-[family-name:var(--font-space-grotesk)] text-sm text-[var(--ember)] hover:text-[var(--flame-2)]"
            >
              zayden@webblaze.io
            </a>
          </div>
          <div>
            <h4 className="eyebrow text-[var(--on-noir-soft)]">Explore</h4>
            <ul className="mt-4 space-y-2.5 text-sm text-[var(--on-noir-soft)]">
              <li><a href="/#work" className="hover:text-white">Our Work</a></li>
              <li><a href="/#process" className="hover:text-white">Process</a></li>
              <li><a href="/#pricing" className="hover:text-white">Pricing</a></li>
              <li><a href="/#faq" className="hover:text-white">FAQ</a></li>
            </ul>
          </div>
          <div>
            <h4 className="eyebrow text-[var(--on-noir-soft)]">Legal</h4>
            <ul className="mt-4 space-y-2.5 text-sm text-[var(--on-noir-soft)]">
              <li><Link href="/privacy" className="hover:text-white">Privacy Policy</Link></li>
              <li><Link href="/terms" className="hover:text-white">Terms &amp; Conditions</Link></li>
              <li><a href="/#contact" className="hover:text-white">Start a project</a></li>
            </ul>
          </div>
        </div>
        <div className="mt-14 flex flex-col gap-3 border-t border-[var(--noir-line)] pt-6 text-xs text-[var(--on-noir-soft)] sm:flex-row sm:items-center sm:justify-between">
          <span>© 2026 WebBlaze. All rights reserved.</span>
          <span>Designed &amp; built in-house.</span>
        </div>
      </div>
    </footer>
  );
}
