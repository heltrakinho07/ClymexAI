import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#ffffff",
        foreground: "#1c1917",
        clymex: {
          forest: "#064e3b",
          emerald: "#059669",
          mint: "#10b981",
          sage: "#6b7280",
          sky: "#0284c7",
          ocean: "#0369a1",
          earth: "#b45309",
          amber: "#d97706",
          sand: "#fef3c7",
          cream: "#fafaf9",
        },
        risk: {
          low: "#059669",
          moderate: "#d97706",
          high: "#ea580c",
          very_high: "#dc2626",
          critical: "#991b1b",
        }
      },
    },
  },
  plugins: [],
};
export default config;
