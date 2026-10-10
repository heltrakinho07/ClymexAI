import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "CLYMEX AI — Predict Risk. Protect Tomorrow.",
  description:
    "Plataforma de Inteligência de Risco Climático orientada a Moçambique e África Austral. Monitoramento preditivo de cheias, secas e estresse hídrico integrando Sentinel-1 SAR, Sentinel-2, ERA5-Land, Google Open Buildings e telemetria IoT.",
  keywords: [
    "Climate Risk",
    "Moçambique",
    "Bacia do Incomati",
    "Flood Risk",
    "Drought",
    "Sentinel-1",
    "Google Open Buildings",
    "GeoAI",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-[#fafaf9] text-stone-900 min-h-screen`}
      >
        {children}
      </body>
    </html>
  );
}
