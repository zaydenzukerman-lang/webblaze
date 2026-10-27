import type { Metadata } from "next";
import { Inter, Space_Grotesk } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

const spaceGrotesk = Space_Grotesk({
  variable: "--font-space-grotesk",
  subsets: ["latin"],
  weight: ["500", "600", "700"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://webblaze.io"),
  title: "WebBlaze | Websites & SEO for Local Businesses in Miami",
  description:
    "WebBlaze builds your website first — you only pay if you love it. Just $629 a year, hosting and updates included, with a 30-day money-back guarantee. Then SEO, blog posts and backlinks get you found on Google and Google Maps.",
  alternates: { canonical: "/" },
  openGraph: {
    title: "WebBlaze | Websites & SEO for Local Businesses in Miami",
    description: "We build your website first, you only pay if you love it. Then we get you found on Google with SEO, blog posts and backlinks.",
    url: "https://webblaze.io", siteName: "WebBlaze", locale: "en_US", type: "website",
    images: [{ url: "/logo-wordmark.png" }],
  },
  robots: { index: true, follow: true },
  icons: {
    icon: [
      { url: "/favicon-32.png", sizes: "32x32", type: "image/png" },
      { url: "/favicon-192.png", sizes: "192x192", type: "image/png" },
    ],
    shortcut: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${spaceGrotesk.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
