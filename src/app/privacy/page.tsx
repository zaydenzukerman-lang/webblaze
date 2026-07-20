import type { Metadata } from "next";
import { Nav, Footer } from "@/components/site";

export const metadata: Metadata = {
  title: "Privacy Policy — WebBlaze",
  description: "How WebBlaze collects, uses, and protects your information.",
};

export default function Privacy() {
  return (
    <>
      <Nav onDark={false} />
      <main className="pt-24">
        <div className="mx-auto max-w-[760px] px-6 py-16">
          <p className="eyebrow text-[var(--flame)]">Legal</p>
          <h1 className="mt-3 text-[length:var(--fs-h2)] font-bold">Privacy Policy</h1>
          <p className="mt-3 text-sm text-[var(--ink-soft)]">Last updated: July 2026</p>
          <hr className="hair my-10" />

          <div className="legal-prose">
            <p>
              This Privacy Policy explains how <strong>WebBlaze</strong> (&ldquo;we,&rdquo;
              &ldquo;us,&rdquo; or &ldquo;our&rdquo;) collects, uses, and protects information when
              you visit <strong>webblaze.io</strong> or contact us about our services. We keep this
              simple: we collect only what we need to build your website and reply to you, and we
              never sell your information.
            </p>

            <h2>Information we collect</h2>
            <ul>
              <li><strong>Information you give us.</strong> When you submit our contact form or email us, we collect your name, email address, business name, and whatever you tell us about your project.</li>
              <li><strong>Information collected automatically.</strong> Like most websites, our host records basic technical data (IP address, browser type, pages visited) to keep the site running and secure.</li>
            </ul>

            <h2>How we use your information</h2>
            <ul>
              <li>To respond to your inquiry and discuss your project.</li>
              <li>To design, build, and deliver your website.</li>
              <li>To send you communication directly related to your project.</li>
              <li>To improve our website and services.</li>
            </ul>
            <p>We do <strong>not</strong> sell, rent, or trade your personal information to anyone.</p>

            <h2>Cookies &amp; analytics</h2>
            <p>
              We use minimal cookies and basic, privacy-respecting analytics to understand how the
              site is used. You can block or delete cookies in your browser settings at any time
              without affecting your ability to contact us.
            </p>

            <h2>Service providers</h2>
            <p>
              We rely on a small number of trusted providers to operate — such as our website host
              and email provider. They only receive the information needed to perform their function
              and are bound to protect it.
            </p>

            <h2>Data retention</h2>
            <p>
              We keep your information only as long as needed to respond to your inquiry and complete
              any project, plus a reasonable period afterward for our records. You can ask us to
              delete it at any time.
            </p>

            <h2>Your rights</h2>
            <p>
              You can ask us to access, correct, or delete the personal information we hold about
              you. Just email <a href="mailto:zayden@webblaze.io">zayden@webblaze.io</a> and
              we&apos;ll take care of it.
            </p>

            <h2>Children</h2>
            <p>
              Our website and services are intended for business owners and are not directed at
              children under 13. We do not knowingly collect information from children.
            </p>

            <h2>Changes to this policy</h2>
            <p>
              We may update this policy from time to time. When we do, we&apos;ll revise the
              &ldquo;last updated&rdquo; date above.
            </p>

            <h2>Contact us</h2>
            <p>
              Questions about this policy? Email{" "}
              <a href="mailto:zayden@webblaze.io">zayden@webblaze.io</a>.
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
