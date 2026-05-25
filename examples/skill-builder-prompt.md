# Skill Builder Prompt

Use this prompt when you want your agent to create a local OpenClaw skill or rebuild one from an idea you found elsewhere.

The preferred pattern in this runbook is not to install third-party skills blindly. Use ClawHub or a GitHub repo as source material, inspect it, then rebuild the behavior locally with only the tools and instructions you need.

## Prompt Template

Copy and customize this prompt:

```text
I need help creating or rebuilding an OpenClaw skill.

Skill name:
[your-skill-name]

Purpose:
[what the skill does and when it should activate]

Source or inspiration:
[ClawHub page, GitHub repo, docs, or notes to inspect]

Keep from the source:
[specific behavior worth preserving]

Do not keep:
[unwanted commands, broad permissions, dependencies, network calls, tone, or scope]

Triggers:
[tasks or questions that should activate this skill]

Tools needed:
[tools, commands, APIs, or files it can use]

Security boundaries:
[secrets policy, confirmation requirements, allowed paths, network limits]

Reference docs:
[docs/specs that should live in references/ for on-demand loading]

Existing local skill, if any:
[path to SKILL.md]

Please:
- Build a local skill rather than installing third-party code.
- Keep SKILL.md focused on activation rules and core workflow.
- Move long examples, API docs, and error tables into references/.
- Keep SKILL.md under about 500 lines unless there is a clear reason.
- Include any helper scripts separately under scripts/.
- Show the final file tree and the contents of new or changed files.
- Call out the exact tools the skill expects to use.
- Call out anything from the source you intentionally did not copy.
```

## Why Rebuild Instead of Install

Third-party skills can be useful to read. They can also carry:

- broader tool access than you need;
- assumptions about another person's workspace;
- hidden network or shell behavior;
- stale commands;
- prompt bloat;
- dependencies you do not want to maintain.

Rebuilding locally gives you a smaller skill that matches your setup and is easier to debug.

## Example: Build From an Idea

```text
I found a weather skill on ClawHub. Do not install it.

Inspect the public source, then build my own local skill named weather-checker.

Keep:
- current weather lookup
- 3-day forecast
- no API key requirement

Do not keep:
- any location tracking
- any background scheduling
- any write access

Tools:
- OpenClaw web fetch or curl against wttr.in only

Security:
- never store location history
- ask before using a non-user-provided location

Please create the local skill with a short SKILL.md, references/wttr.md, and no extra dependencies.
```

## Example: Refactor a Bloated Skill

```text
I need help shrinking an OpenClaw skill.

Existing skill:
~/.openclaw/workspace/skills/my-bloated-skill/SKILL.md

Problem:
SKILL.md is 1,800 lines and burns too much context.

Please:
- preserve behavior;
- keep activation rules and core workflow in SKILL.md;
- move details into references/;
- move reusable commands into scripts/ if helpful;
- remove generic advice and duplicated examples;
- show what changed.
```

## Recommended Structure

```text
skills/
└── your-skill-name/
    ├── SKILL.md
    ├── references/
    │   ├── api.md
    │   └── examples.md
    └── scripts/
        └── helper.sh
```

## Local Review Checklist

- Does the skill name match its real purpose?
- Are triggers narrow enough?
- Are secrets excluded?
- Are destructive actions gated by confirmation?
- Are references loaded only when needed?
- Are command paths and external URLs explicit?
- Does the skill need every tool it asks for?
- Can you test it without giving it broad access?

## Related

- [Config guide](config-example-guide.md)
- [Security hardening](security-hardening.md)
- [Spawning patterns](spawning-patterns.md)
