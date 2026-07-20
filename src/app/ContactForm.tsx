"use client";

import { useState, FormEvent } from "react";

// Web3Forms access key — set once Zayden verifies zayden@webblaze.io at
// web3forms.com and pastes the key in. Until then the form still renders
// and validates, it just can't deliver (submit will show the error state).
const WEB3FORMS_ACCESS_KEY = "REPLACE_WITH_WEB3FORMS_ACCESS_KEY";

type Status = "idle" | "sending" | "sent" | "error";

export default function ContactForm() {
  const [status, setStatus] = useState<Status>("idle");

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("sending");
    const form = e.currentTarget;
    const data = new FormData(form);
    data.append("access_key", WEB3FORMS_ACCESS_KEY);

    try {
      const res = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { Accept: "application/json" },
        body: data,
      });
      const json = await res.json();
      if (json.success) {
        setStatus("sent");
        form.reset();
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  }

  if (status === "sent") {
    return (
      <div className="rounded-2xl bg-white p-8 text-center shadow-lg">
        <p className="font-[family-name:var(--font-display)] text-xl font-bold text-[var(--burnt)]">
          Got it — thanks!
        </p>
        <p className="mt-2 text-sm text-[var(--ink-soft,#5A6470)]">
          We&apos;ll reach out shortly to start building your site.
        </p>
      </div>
    );
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-2xl bg-white p-6 text-left shadow-lg sm:p-8"
    >
      {/* Honeypot spam trap — hidden from real users */}
      <input type="checkbox" name="botcheck" className="hidden" style={{ display: "none" }} tabIndex={-1} autoComplete="off" />
      <input type="hidden" name="subject" value="New site request from webblaze.io" />

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label htmlFor="cf-name" className="mb-1 block text-sm font-semibold text-[var(--burnt)]">
            Name
          </label>
          <input
            id="cf-name"
            name="name"
            type="text"
            required
            autoComplete="name"
            placeholder="Your name"
            className="w-full rounded-lg border border-black/10 px-3.5 py-2.5 text-sm text-[#1C2126] outline-none focus:border-[var(--burnt)]"
          />
        </div>
        <div>
          <label htmlFor="cf-email" className="mb-1 block text-sm font-semibold text-[var(--burnt)]">
            Email
          </label>
          <input
            id="cf-email"
            name="email"
            type="email"
            required
            autoComplete="email"
            placeholder="you@business.com"
            className="w-full rounded-lg border border-black/10 px-3.5 py-2.5 text-sm text-[#1C2126] outline-none focus:border-[var(--burnt)]"
          />
        </div>
      </div>

      <div className="mt-4">
        <label htmlFor="cf-business" className="mb-1 block text-sm font-semibold text-[var(--burnt)]">
          Business name
        </label>
        <input
          id="cf-business"
          name="business"
          type="text"
          placeholder="e.g. Orange Beach Fish Charter"
          className="w-full rounded-lg border border-black/10 px-3.5 py-2.5 text-sm text-[#1C2126] outline-none focus:border-[var(--burnt)]"
        />
      </div>

      <div className="mt-4">
        <label htmlFor="cf-message" className="mb-1 block text-sm font-semibold text-[var(--burnt)]">
          What do you need?
        </label>
        <textarea
          id="cf-message"
          name="message"
          required
          rows={3}
          placeholder="Tell us a bit about your business and what you're looking for"
          className="w-full resize-y rounded-lg border border-black/10 px-3.5 py-2.5 text-sm text-[#1C2126] outline-none focus:border-[var(--burnt)]"
        />
      </div>

      {status === "error" && (
        <p className="mt-4 text-sm font-medium text-red-100">
          Something went wrong sending that — try again, or email us directly at{" "}
          <a href="mailto:zayden@webblaze.io" className="underline">
            zayden@webblaze.io
          </a>
          .
        </p>
      )}

      <button
        type="submit"
        disabled={status === "sending"}
        className="mt-6 w-full rounded-full bg-[var(--burnt)] px-8 py-3.5 text-sm font-semibold text-white shadow-lg transition-transform hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {status === "sending" ? "Sending…" : "Get your free build"}
      </button>
    </form>
  );
}
