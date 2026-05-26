import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const runbook = defineCollection({
  loader: glob({ base: "./src/content/runbook", pattern: "**/*.md" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    section: z.enum(["guide", "examples", "showcases", "project"]),
    order: z.number(),
    sourcePath: z.string(),
    route: z.string(),
    topics: z.array(z.string()).default([]),
  }),
});

export const collections = { runbook };
