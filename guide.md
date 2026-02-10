# Running OpenClaw Without Burning Money, Quotas, or Your Sanity

## TL;DR

OpenClaw is useful, but most of the pain people run into comes from letting one model do everything, chasing hype, or running expensive models in places that don't need them.

What worked for me was treating OpenClaw like infrastructure instead of a chatbot. Keep a cheap model as the coordinator, use agents for real work, be explicit about routing, and make memory and task state visible. Cheap models handle background work fine. Strong models are powerful when you call them intentionally instead of leaving them as defaults.

You don't need expensive hardware, and you don't need to host giant local models to get value out of this. Start small, get things stable before letting it run all the time, and avoid the hype train. If something feels broken, check the official docs and issues first. OpenClaw changes fast, and sometimes it really is just a bug.

If you want flashy demos and YouTube thumbnails with shocked faces, this probably isn't it. The rest of this post covers what boring, day-to-day usage actually looks like.

---

I kept seeing the same questions come up around OpenClaw. People asking why it feels slow, why it keeps planning instead of doing, why it forgets things, or why free tiers disappear overnight. After answering the same threads over and over, it made more sense to write this once and link it.

This is not official guidance, and I am not affiliated with OpenClaw or any model provider. This is simply what I learned by running it, breaking it, and doing that loop more times than I'd like to admit.

One thing up front: OpenClaw changes fast. Sometimes daily, sometimes more. When something strange happens, it isn't always because you misconfigured something. Sometimes it's a regression, a bug, or a feature that just landed.

Before taking blind advice from anyone on the internet, including me, check the official OpenClaw resources first:

- [https://docs.openclaw.ai/help/faq](https://docs.openclaw.ai/help/faq)
- [https://docs.openclaw.ai/](https://docs.openclaw.ai/)
- [https://github.com/openclaw/openclaw/issues](https://github.com/openclaw/openclaw/issues)
- [https://github.com/openclaw/openclaw/pulls](https://github.com/openclaw/openclaw/pulls)

Reading open issues and recent PRs has saved me hours. More than once I thought I broke something, only to realize it was already known and actively being worked on.

---

## The mistake most people make early on

The most common mistake is treating OpenClaw like a single super-intelligent chatbot that should handle everything at once. Conversation, planning, research, coding, memory, task tracking, monitoring. All through one model, all the time.

That setup ends in endless follow-up questions, permission loops, silent failures, and burned quotas. When it works, it's expensive. When it breaks, it's hard to tell why.

What clicked for me was that the main model should be a coordinator, not a worker. The default agent should be capable but not overkill. Expensive models stay out of the hot path.

My config looks roughly like this:

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "anthropic/claude-sonnet-4-5",
      "fallbacks": [
        "kimi-coding/k2p5",
        "synthetic/hf:zai-org/GLM-4.7",
        "openrouter/google/gemini-3-flash-preview",
        "openrouter/openai/gpt-5-mini",
        "openrouter/openai/gpt-5-nano",
        "openrouter/google/gemini-2.5-flash-lite"
      ]
    }
  }
}
```

The exact model list matters less than the intent. Expensive models aren't sitting in the default loop, and fallback behavior is explicit.

---

## Auto-mode and blind routing

I tried auto-mode and blind routing early on. Stopped using both.

The idea of letting the system decide which model to use sounds great. When I actually ran it, it led to indecision, unexpected cost spikes, and behavior I couldn't reason about when something went wrong.

Being explicit works better. Default routing stays cheap and predictable. Agents get pinned to specific models for specific jobs. When something expensive runs, it's because I asked for it.

Less magical. Far more debuggable.

---

## Why strong models shouldn't be defaults

High-quality models like Opus are useful. I use them. They're great at restructuring prompts, designing agents, reasoning through messy problems, and unfucking things that are already broken.

Where I got burned was leaving that level of model running all day.

It felt powerful until I hit rate limits and ended up locked out waiting for quotas to refresh. At that point you're not building anything. You're just waiting.

Strong models work best when they're scoped. Pin them to specific agents and call them when you actually need them. Don't leave them in the default coordinator loop burning through your quota on routine work.

---

## Don't buy hardware yet

There's been a lot of hype around buying Mac minis or Mac Studios just to run OpenClaw. I'd strongly recommend against doing this early.

Not everyone has $600 to drop on a tool, and even if you do, it's usually the wrong move to make first. The FOMO around OpenClaw is real. It's easy to feel like you need dedicated hardware immediately.

Learn your workflow first. Learn your costs. Figure out your failure modes. I would have saved money if I had done that before buying anything.

---

## The reality of local models

Local models get pitched as the solution to everything. The math rarely works out unless you already have serious hardware.

A Mac Studio with 512 GB of unified memory and 2 TB of storage runs over $9,000. To realistically host something like Kimi 2.5 with usable performance, you're looking at two of them. Roughly $18,000 in hardware.

Unless you're building a business that needs that hardware for more than just OpenClaw, skip it.

Local models are fine for experimentation and simple tasks. But I've found that bending over backwards to save a few cents usually costs more in lost time and degraded performance than just paying for API calls.

One related note: some free-tier hosted options aren't much better. NVIDIA NIM's free tier for Kimi K2.5, for example, regularly has 150+ requests in queue. That kind of latency makes it unusable for agent workflows where you need responses in seconds, not minutes. "Free" doesn't always mean "usable."

---

## The hype problem

This part is worth saying.

There is a lot of hype around OpenClaw right now. Flashy demos, YouTube videos promising it will replace everything you do, "this changes everything" energy on every social platform. I've watched people spend more time configuring OpenClaw than doing the work they wanted OpenClaw to help with.

I'd encourage people to resist the FOMO and ignore most of the YouTube content. A lot of it is optimized for clicks, not for the kind of boring Tuesday-afternoon usage that actually matters.

OpenClaw gets useful when you stop expecting magic and start expecting a tool that needs tuning.

---

## Cheap models are fine, actually

One of the bigger mental shifts for me was realizing how cheap some models are when used correctly.

Heartbeats run often but do simple checks. No reason to burn premium models on background plumbing. I've seen tens of thousands of heartbeat tokens cost fractions of a cent on cheap models.

For the specific model recommendations and cost math, see [`examples/config-example-guide.md`](examples/config-example-guide.md#heartbeat-model-heartbeatmodel).

Concurrency limits also matter for cost control:

```json
"maxConcurrent": 4,
"subagents": {
  "maxConcurrent": 8
}
```

Those limits prevent one bad task from cascading into retries and runaway cost.

---

## A Practical Rotating Heartbeat Pattern

Instead of running separate cron jobs for different periodic checks, I use a single heartbeat that rotates through checks based on how overdue each one is.

The idea is simple. Each check has a cadence (how often it should run), an optional time window (when it's allowed to run), and a record of the last time it ran. On each heartbeat tick, the system runs whichever check is most overdue.

This batches background work, keeps costs flat, and avoids the "everything fires at once" problem.

All heartbeat checks run on a very cheap model. If a check finds something that needs work, it spawns the appropriate agent instead of trying to do it inline.

For the full implementation pattern and prompt template, see [`examples/heartbeat-example.md`](examples/heartbeat-example.md).

---

## Making memory explicit

Most memory complaints I see come from assuming memory is automatic. It isn't, and the default behavior is confusing if you don't configure it.

I made memory explicit and cheap. I use cheap embeddings for search (`text-embedding-3-small`), prune context based on cache TTL (6 hours), and set up compaction to automatically flush sessions to daily memory files when they hit 40k tokens.

This one change eliminated most of the "why did it forget that" moments I was having. Before I set this up, I was losing context constantly and blaming the model when it was really a configuration problem.

For the specific config settings and explanations, see [`examples/config-example-guide.md`](examples/config-example-guide.md).

---

## A note on sharing my config

A few people asked to see a sanitized version of my OpenClaw config. I'm sharing it here as a reference, not something to copy verbatim.

It reflects my usage patterns, my constraints, and my tolerance for cost and latency. Yours will almost certainly be different.

The intent is to show how pieces fit together, not to suggest this is "the right" configuration.

Sanitized config (secrets removed): See [`examples/sanitized-config.json`](examples/sanitized-config.json) in this repository.

---

## Skills: build your own first

I'm cautious with third-party skills.

I've had better luck building my own and treating community skills as inspiration rather than drop-ins. A poorly written or malicious skill can cause real problems, and debugging someone else's abstractions when something breaks at 2am is miserable.

I also set basic rules in memory, like never exposing secrets or API keys. Not foolproof, but it helps as a guardrail.

### Asking the bot to build or optimize a skill

One thing that helped me was getting more disciplined about how I ask the bot to create or refactor skills. Vague instructions produce bloated, token-hungry skills every time.

The structure I use follows the AgentSkills specification from [https://agentskills.io](https://agentskills.io/). I'm not affiliated with it, but following that model made skills easier to maintain and cheaper to run.

For a detailed prompt template and examples, see [`examples/skill-builder-prompt.md`](examples/skill-builder-prompt.md).

The key is giving the bot hard constraints on line count and structure so it doesn't produce a 2,000-line skill file that eats half your context window.

---

## Using Todoist for task visibility

Early on, OpenClaw felt like a black box. I couldn't tell what it was doing, what it had finished, or what was stuck. The logs weren't enough.

I fixed that by wiring up Todoist as the source of truth for task state. Tasks get created when work starts, updated as state changes, assigned to me when human intervention is required, and closed when done. If something fails, it leaves a comment on the task instead of retrying forever.

A lightweight heartbeat reconciles what's open, what's in progress, and what looks stalled. It's not sophisticated, but I can glance at Todoist and know exactly where things stand without digging through logs.

For a prompt template to build your own task tracking system, see [`examples/task-tracking-prompt.md`](examples/task-tracking-prompt.md).

---

## Running on a VPS

If you want to run OpenClaw on a VPS, you don't need a large machine. A Hetzner CX23 is plenty.

I'd strongly recommend Tailscale on both your local machine and the VPS. Install it on the VPS with the `--ssh=true` flag and you can log in over Tailscale directly. Then block port 22 entirely in the Hetzner firewall.

I block all inbound traffic and access everything over Tailscale. Simple setup, and one less thing to worry about.

For the full VPS setup process, security hardening, and validation workflow, see [`examples/vps-setup.md`](examples/vps-setup.md).

---

## Prompt Injection Defense

If your OpenClaw setup can read untrusted content (web pages, GitHub issues, documents, email), assume someone will eventually try to steer it.

I make expectations explicit and load them every session. The exact rules I keep in my `AGENTS.md`, attack patterns to watch for, and security configuration are documented in [`examples/security-patterns.md`](examples/security-patterns.md).

Not foolproof, but it helps set clear boundaries.

---

## What this costs me per month

I don't pay for everything through APIs.

I use two coding subscriptions at about $20 each. On top of that, API usage runs about $5-$10 per month split between OpenRouter and OpenAI.

Most months I land around $45-$50 total.

---

## Your numbers will be different

If you let agents run nonstop, allow unlimited retries, or route everything through premium models, costs will climb. I've seen people hit $200+ in a weekend by leaving things uncapped.

If you scope models, cap concurrency, and keep background work on cheap models, costs flatten out fast.

---

## On Anthropic bans

From what I've seen, bans usually come down to how aggressively Claude is being hit through the API, not OpenClaw itself. I'm not saying bans never happen. The cases I've seen were tied to aggressive automated usage patterns, not simply running OpenClaw. If you're not hammering the API beyond normal usage, there's no obvious reason to worry about it.

---

## Get things stable before going 24/7

I don't start with always-on mode.

I get things stable first, usually in a local VM or container. I watch behavior and cost for a few days. Only after things are predictable do I let it run unattended for longer stretches.

Letting an agent run unsupervised before you understand its failure modes is how you wake up to a $300 API bill and a Todoist full of gibberish.

---

## Final thoughts

You don't need expensive hardware or expensive subscriptions to make OpenClaw useful. What you need is to be deliberate about configuration, keep visibility into what's happening, and resist the urge to over-engineer before you understand the basics.

If this saves you some time or frustration, it did its job.

---

## Links and referrals

A few people asked where I'm getting access to some of the models and services mentioned above.

For transparency: I'm not affiliated with OpenClaw, and nothing in this article depends on using these links.

Some providers I use offer referral programs. Included here for people who ask. Use them or don't.

### Z.ai (GLM models)

Z.ai provides access to GLM 4.6 and 4.7, which I use as capable, lower-cost options for agents that don't need premium models.

- Direct link: [https://z.ai/subscribe](https://z.ai/subscribe)
- Referral link (supports this guide): [https://z.ai/subscribe?ic=6PVT1IFEZT](https://z.ai/subscribe?ic=6PVT1IFEZT)

### Synthetic

Synthetic hosts several open-source and partner models under one subscription, including GLM 4.7 and Kimi 2.5, plus additional models via Fireworks and Together.

- Direct link: [https://synthetic.new](https://synthetic.new)
- Referral link (supports this guide): [https://synthetic.new/?referral=p7ZFKQRrWliKZGa](https://synthetic.new/?referral=p7ZFKQRrWliKZGa)

Use whichever links you prefer. Referrals help support this guide but aren't required.
