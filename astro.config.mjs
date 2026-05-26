import sitemap from "@astrojs/sitemap";
import { defineConfig, passthroughImageService } from "astro/config";

export default defineConfig({
  site: "https://digitalknk.github.io",
  base: "/openclaw-runbook",
  trailingSlash: "always",
  image: {
    service: passthroughImageService(),
  },
  integrations: [sitemap()],
  markdown: {
    shikiConfig: {
      theme: "github-light",
      wrap: true,
    },
  },
});
