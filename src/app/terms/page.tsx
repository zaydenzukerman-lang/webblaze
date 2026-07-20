import type { Metadata } from "next";
import { Nav, Footer } from "@/components/site";

export const metadata: Metadata = {
  title: "Terms & Conditions — WebBlaze",
  description: "The terms that govern WebBlaze's websites and services.",
};

export default function Terms() {
  return (
    <>
      <Nav onDark={false} />
      <main className="pt-24">
        <div className="mx-auto max-w-[760px] px-6 py-16">
          <p className="eyebrow text-[var(--flame)]">Legal</p>
          <h1 className="mt-3 text-[length:var(--fs-h2)] font-bold">Terms &amp; Conditions</h1>
          <p className="mt-3 text-sm text-[var(--ink-soft)]">Last updated: July 2026</p>
          <hr className="hair my-10" />

          <div className="legal-prose">
            <p>
              These Terms &amp; Conditions govern your use of <strong>webblaze.io</strong> and the
              services provided by <strong>WebBlaze</strong> (&ldquo;we,&rdquo; &ldquo;us&rdquo;).
              By working with us, you agree to these terms.
            </p>

            <h2>Our services</h2>
            <p>
              We design and build websites for small businesses for a <strong>$300 flat fee</strong>.
              We may also offer optional growth services (such as local SEO and lead generation) —
              these are always quoted and agreed separately, never bundled into the website fee.
            </p>

            <h2>Build-first model &amp; payment</h2>
            <ul>
              <li>We build your website <strong>first</strong>, with no deposit and no contract.</li>
              <li>You pay the <strong>$300 flat fee only if you approve</strong> the finished site.</li>
              <li>If you decide not to proceed, you owe us nothing and there is no obligation.</li>
              <li>Payment is made once, by invoice. There are no recurring or hidden fees for the website itself.</li>
            </ul>

            <h2>Revisions</h2>
            <p>
              We include reasonable revisions before payment so the site is genuinely yours. After
              launch, small updates (a phone number, a price, a photo) are free — just ask. Larger
              redesigns or new features are quoted separately.
            </p>

            <h2>Ownership &amp; intellectual property</h2>
            <ul>
              <li>Once the $300 fee is paid in full, the website and the assets we created for it are <strong>yours</strong>.</li>
              <li>You are responsible for ensuring you have the rights to any content you provide (logos, photos, text).</li>
              <li>We may feature the work in our portfolio unless you ask us not to.</li>
            </ul>

            <h2>Your responsibilities</h2>
            <ul>
              <li>Provide accurate business information and timely feedback.</li>
              <li>Ensure you own or have permission to use any materials you supply.</li>
              <li>For regulated industries, confirm any required legal or compliance text before your site goes live.</li>
            </ul>

            <h2>No guarantee of specific results</h2>
            <p>
              We build high-quality, professional websites — but we do not guarantee specific search
              rankings, traffic numbers, or sales. Results depend on many factors outside our control.
            </p>

            <h2>Third-party services</h2>
            <p>
              Your website may rely on third-party services (domain registration, hosting, email,
              analytics). Your use of those services is subject to their own terms.
            </p>

            <h2>Limitation of liability</h2>
            <p>
              Our services are provided &ldquo;as is.&rdquo; To the fullest extent permitted by law,
              WebBlaze is not liable for any indirect or consequential damages, and our total
              liability will not exceed the fees you have paid us.
            </p>

            <h2>Ending the engagement</h2>
            <p>
              Because we build first, either side can walk away before payment with no cost or
              obligation. After payment, the completed site is yours to keep.
            </p>

            <h2>Changes to these terms</h2>
            <p>
              We may update these terms from time to time. The &ldquo;last updated&rdquo; date above
              reflects the current version.
            </p>

            <h2>Contact us</h2>
            <p>
              Questions? Email <a href="mailto:zayden@webblaze.io">zayden@webblaze.io</a>.
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
