import type { CollectionEntry } from "astro:content";

export const site = {
  name: "OpenClaw Runbook",
  title: "OpenClaw Runbook",
  description:
    "Unofficial OpenClaw runbook for running agents day to day without burning money, exposing your gateway, or trusting random automation.",
  checkedAgainst: "OpenClaw commit 5dccba7405",
  checkedDate: "2026-05-25",
  repoUrl: "https://github.com/digitalknk/openclaw-runbook",
  topics: [
    "openclaw",
    "ai-agents",
    "runbook",
    "tailscale",
    "self-hosting",
    "security-hardening",
  ],
};

export function withBase(pathname: string) {
  const base = import.meta.env.BASE_URL;
  const cleanPath = pathname.startsWith("/") ? pathname.slice(1) : pathname;
  return `${base}${cleanPath}`;
}

export function canonicalUrl(pathname: string) {
  const cleanPath = pathname.startsWith("/") ? pathname : `/${pathname}`;
  return new URL(`/openclaw-runbook${cleanPath}`, "https://digitalknk.github.io")
    .toString()
    .replace(/([^:]\/)\/+/g, "$1");
}

export function sortEntries(entries: CollectionEntry<"runbook">[]) {
  return [...entries].sort((a, b) => a.data.order - b.data.order);
}

export function routeFor(entry: CollectionEntry<"runbook">) {
  return withBase(entry.data.route);
}

export function sourceUrl(sourcePath: string) {
  return `${site.repoUrl}/blob/main/${sourcePath}`;
}
