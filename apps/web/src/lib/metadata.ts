
import type { Metadata } from "next";

const siteName = "ETS";
const siteTitle = "ETS: Employment Targeting System";

const siteDescription =
  "ETS (Employment Targeting System) is an open-source, AI-powered tool that compares a job post with your CV and tells you in seconds whether to smash or pass. It also flags unrealistic or copy-pasted requirements.";

const siteUrl = "https://github.com/fifolio/ETS"; // later add canonical URL
const authorName = "Firas Dabbabi";
const authorUrl = "https://github.com/fifolio";

export const siteMetadata: Metadata = {
  metadataBase: new URL(siteUrl),

  title: {
    default: siteTitle,
    template: `%s | ${siteName}`,
  },

  description: siteDescription,

  applicationName: siteName,
  authors: [{ name: authorName, url: authorUrl }],
  creator: authorName,
  category: "career",

  keywords: [
    "anti-ATS",
    "job search",
    "CV matching",
    "resume matching",
    "applicant tracking system",
    "AI-powered job search",
    "large language models",
    "open-source software",
    "browser extension",
  ],

  openGraph: {
    title: siteTitle,
    description: siteDescription,
    siteName,
    type: "website",
  },
};
