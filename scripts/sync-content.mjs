import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outDir = path.join(repoRoot, "src/content/runbook");
const assetDir = path.join(repoRoot, "public/assets/examples");
const basePath = "/openclaw-runbook";

const topics = [
  "openclaw",
  "ai-agents",
  "runbook",
  "tailscale",
  "self-hosting",
  "security-hardening",
];

const pages = [
  {
    sourcePath: "guide.md",
    outPath: "guide.md",
    route: "/guide/",
    section: "guide",
    order: 10,
    description:
      "The full field guide for private access, explicit model routing, memory, automation, local skills, and security guardrails.",
  },
  {
    sourcePath: "CONTRIBUTING.md",
    outPath: "contributing.md",
    route: "/contributing/",
    section: "project",
    order: 900,
    description:
      "Contribution standards for practical, operational OpenClaw guidance.",
  },
  {
    sourcePath: "LICENSE",
    outPath: "license.md",
    route: "/license/",
    section: "project",
    order: 910,
    title: "License",
    description: "MIT license for the OpenClaw Runbook.",
  },
  {
    sourcePath: "examples/agent-prompts.md",
    outPath: "examples/agent-prompts.md",
    route: "/examples/agent-prompts/",
    section: "examples",
    order: 110,
    description:
      "Specialized agent examples for model routing, shared instructions, and coordinator-worker patterns.",
  },
  {
    sourcePath: "examples/check-quotas-README.md",
    outPath: "examples/check-quotas.md",
    route: "/examples/check-quotas/",
    section: "examples",
    order: 120,
    description:
      "A quota check helper for making provider limits visible before automation gets expensive.",
  },
  {
    sourcePath: "examples/config-example-guide.md",
    outPath: "examples/config-example-guide.md",
    route: "/examples/config-example-guide/",
    section: "examples",
    order: 130,
    description:
      "Annotated config reference for gateway access, models, tools, channels, hooks, and memory search.",
  },
  {
    sourcePath: "examples/heartbeat-example.md",
    outPath: "examples/heartbeat-example.md",
    route: "/examples/heartbeat-example/",
    section: "examples",
    order: 140,
    description:
      "Heartbeat checklist and task-block pattern for lightweight awareness without pretending it is a scheduler.",
  },
  {
    sourcePath: "examples/model-delegation-troubleshooting.md",
    outPath: "examples/model-delegation-troubleshooting.md",
    route: "/examples/model-delegation-troubleshooting/",
    section: "examples",
    order: 150,
    description:
      "Notes for testing and debugging model delegation, aliases, and provider-prefix behavior.",
  },
  {
    sourcePath: "examples/security-hardening.md",
    outPath: "examples/security-hardening.md",
    route: "/examples/security-hardening/",
    section: "examples",
    order: 160,
    description:
      "Security baseline covering access boundaries, secrets, tool policy, channels, skills, and emergency commands.",
  },
  {
    sourcePath: "examples/security-patterns.md",
    outPath: "examples/security-patterns.md",
    route: "/examples/security-patterns/",
    section: "examples",
    order: 170,
    description:
      "Prompt injection rules and operating patterns for treating untrusted content as data.",
  },
  {
    sourcePath: "examples/security-quickstart.md",
    outPath: "examples/security-quickstart.md",
    route: "/examples/security-quickstart/",
    section: "examples",
    order: 180,
    description:
      "Copyable prompts for auditing and tightening a personal OpenClaw setup.",
  },
  {
    sourcePath: "examples/skill-builder-prompt.md",
    outPath: "examples/skill-builder-prompt.md",
    route: "/examples/skill-builder-prompt/",
    section: "examples",
    order: 190,
    description:
      "Prompt template for rebuilding local skills from inspected ideas instead of installing unknown packages blindly.",
  },
  {
    sourcePath: "examples/spawning-patterns.md",
    outPath: "examples/spawning-patterns.md",
    route: "/examples/spawning-patterns/",
    section: "examples",
    order: 200,
    description:
      "Current sessions_spawn and subagent coordination patterns, including what not to poll.",
  },
  {
    sourcePath: "examples/task-tracking-prompt.md",
    outPath: "examples/task-tracking-prompt.md",
    route: "/examples/task-tracking-prompt/",
    section: "examples",
    order: 210,
    description:
      "A task-ledger pattern for inspectable OpenClaw work without an external black box.",
  },
  {
    sourcePath: "examples/vps-setup.md",
    outPath: "examples/vps-setup.md",
    route: "/examples/vps-setup/",
    section: "examples",
    order: 220,
    description:
      "VPS setup checklist with Tailscale as the default remote access path.",
  },
  {
    sourcePath: "showcases/agent-orchestrator.md",
    outPath: "showcases/agent-orchestrator.md",
    route: "/showcases/agent-orchestrator/",
    section: "showcases",
    order: 310,
    description:
      "Route coding tasks to configured agents and tools without making one default agent do everything.",
  },
  {
    sourcePath: "showcases/autonomous-operation.md",
    outPath: "showcases/autonomous-operation.md",
    route: "/showcases/autonomous-operation/",
    section: "showcases",
    order: 320,
    description:
      "Community-contributed health-check pattern for autonomous operation with a thin main session.",
  },
  {
    sourcePath: "showcases/claworc.md",
    outPath: "showcases/claworc.md",
    route: "/showcases/claworc/",
    section: "showcases",
    order: 330,
    description:
      "Community-contributed review of an external OpenClaw orchestration control-plane project.",
  },
  {
    sourcePath: "showcases/coeus-knowledge-base.md",
    outPath: "showcases/coeus-knowledge-base.md",
    route: "/showcases/coeus-knowledge-base/",
    section: "showcases",
    order: 340,
    description:
      "Local semantic knowledge-base pattern with capture, search, brief, and storage notes.",
  },
  {
    sourcePath: "showcases/daily-brief.md",
    outPath: "showcases/daily-brief.md",
    route: "/showcases/daily-brief/",
    section: "showcases",
    order: 350,
    description:
      "Morning summary pattern for weather, calendar, and tasks using a balanced or cheap model.",
  },
  {
    sourcePath: "showcases/homelab-access.md",
    outPath: "showcases/homelab-access.md",
    route: "/showcases/homelab-access/",
    section: "showcases",
    order: 360,
    description:
      "Safer remote SSH through Telegram confirmations and Tailscale-first access.",
  },
  {
    sourcePath: "showcases/idea-pipeline.md",
    outPath: "showcases/idea-pipeline.md",
    route: "/showcases/idea-pipeline/",
    section: "showcases",
    order: 370,
    description:
      "Overnight research pattern for captured ideas with bounded scope and evidence capture.",
  },
  {
    sourcePath: "showcases/linkedin-drafter.md",
    outPath: "showcases/linkedin-drafter.md",
    route: "/showcases/linkedin-drafter/",
    section: "showcases",
    order: 380,
    description:
      "Weekly draft-generation pattern that keeps public writing behind human review.",
  },
  {
    sourcePath: "showcases/tech-discoveries.md",
    outPath: "showcases/tech-discoveries.md",
    route: "/showcases/tech-discoveries/",
    section: "showcases",
    order: 390,
    description:
      "Curated tech-discovery pattern for watching useful changes without a noisy feed.",
  },
  {
    sourcePath: "showcases/template.md",
    outPath: "showcases/template.md",
    route: "/showcases/template/",
    section: "showcases",
    order: 399,
    description:
      "Template for adding a new showcase while preserving prerequisites, tests, and security notes.",
  },
];

const routeBySource = new Map([
  ["README.md", "/"],
  ["./README.md", "/"],
  ["showcases/README.md", "/showcases/"],
  ...pages.map((page) => [page.sourcePath, page.route]),
]);

const assetTargets = [
  "examples/check-quotas.sh",
  "examples/coeus.py",
  "examples/sanitized-config.json",
];

function asFrontmatterValue(value) {
  if (Array.isArray(value)) {
    return `[${value.map((item) => JSON.stringify(item)).join(", ")}]`;
  }
  if (typeof value === "number") {
    return String(value);
  }
  return JSON.stringify(value);
}

function getTitle(markdown, fallback) {
  const match = markdown.match(/^#\s+(.+)$/m);
  return fallback ?? match?.[1]?.trim() ?? "Untitled";
}

function normalizePath(fromSource, target) {
  if (/^(https?:|mailto:|tel:|#)/.test(target)) {
    return target;
  }

  const [targetPath, suffix = ""] = target.split(/(?=[#?])/);
  if (!targetPath) {
    return target;
  }

  const baseDir = path.posix.dirname(fromSource);
  const normalized = path.posix
    .normalize(path.posix.join(baseDir === "." ? "" : baseDir, targetPath))
    .replace(/^\.\//, "");

  if (routeBySource.has(normalized)) {
    return `${basePath}${routeBySource.get(normalized)}${suffix}`;
  }

  if (assetTargets.includes(normalized)) {
    return `${basePath}/assets/${normalized}${suffix}`;
  }

  return target;
}

function rewriteLinks(markdown, sourcePath) {
  return markdown.replace(
    /(\[[^\]]*\]\()([^)\s]+)(\))/g,
    (_match, open, target, close) => `${open}${normalizePath(sourcePath, target)}${close}`,
  );
}

function stripReadmeIntro(markdown, page) {
  if (page.sourcePath === "LICENSE") {
    return `# License\n\n\`\`\`text\n${markdown.trim()}\n\`\`\`\n`;
  }

  return markdown;
}

function normalizeFenceLanguages(markdown) {
  return markdown.replace(/^```(?:gitignore|sshconfig)$/gm, "```text");
}

async function sync() {
  await rm(outDir, { recursive: true, force: true });
  await rm(assetDir, { recursive: true, force: true });
  await mkdir(outDir, { recursive: true });
  await mkdir(assetDir, { recursive: true });

  for (const asset of assetTargets) {
    await mkdir(path.dirname(path.join(repoRoot, "public/assets", asset)), {
      recursive: true,
    });
    await cp(path.join(repoRoot, asset), path.join(repoRoot, "public/assets", asset));
  }

  for (const page of pages) {
    const sourceFile = path.join(repoRoot, page.sourcePath);
    const source = await readFile(sourceFile, "utf8");
    const body = rewriteLinks(
      normalizeFenceLanguages(stripReadmeIntro(source, page)),
      page.sourcePath,
    );
    const title = page.title ?? getTitle(body);
    const frontmatter = {
      title,
      description: page.description,
      section: page.section,
      order: page.order,
      sourcePath: page.sourcePath,
      route: page.route,
      topics,
    };

    const frontmatterText = Object.entries(frontmatter)
      .map(([key, value]) => `${key}: ${asFrontmatterValue(value)}`)
      .join("\n");
    const output = `---\n${frontmatterText}\n---\n\n${body}`;
    const outputFile = path.join(outDir, page.outPath);
    await mkdir(path.dirname(outputFile), { recursive: true });
    await writeFile(outputFile, output);
  }
}

await sync();
