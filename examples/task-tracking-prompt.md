# Task Tracking System Prompt

This prompt helps you build a task tracking system that makes agent work visible without digging through logs.

## Why Task Tracking?

OpenClaw can feel like a black box. You don't know what it's doing, what's stuck, or what needs your attention. A task tracking system solves this by making all agent work visible in a tool you already check (Todoist, GitHub Projects, Linear, etc.).

## About This Approach

This example uses Todoist, but the pattern works with any task manager that has an API. The key is creating visibility into agent state through a tool you can glance at anytime.

## Prerequisites

Before giving this prompt to your agent:

1. **Todoist account** - Free or paid (https://todoist.com)

2. **API token** - Get from Todoist:
   - Settings → Integrations → Developer → API Token
   - Copy the token

3. **Projects** - Either create manually or let the agent create:
   - Backlog/Queue project
   - Active project
   - Optional: Waiting/Blocked project (or use task assignment)

4. **Credentials directory** - Set up with proper permissions:
   ```bash
   mkdir -p ~/.openclaw/credentials
   echo "your-todoist-api-token-here" > ~/.openclaw/credentials/todoist
   chmod 700 ~/.openclaw/credentials
   chmod 600 ~/.openclaw/credentials/todoist
   ```

## Prompt Template

Copy and customize this prompt to give to your agent:

```
Build a Todoist-based task tracking system for OpenClaw:

GOAL: Make agent work visible without checking logs. Glance at Todoist and see exactly what's happening.

STATE MODEL:
- Queue/Backlog: Tasks waiting to start
- Active: Work currently in progress
- Waiting/Assigned to me: Blocked on human input
- Done: Completed

OPERATIONS NEEDED:
1. create_task(title, project) - Add task to queue/backlog
2. move_to_active(task_id) - Start work, move to Active project
3. assign_to_me(task_id, reason) - Mark blocked, assign with comment explaining why
4. complete_task(task_id) - Mark done and close
5. add_comment(task_id, status) - Add progress updates to task

RECONCILIATION (runs via heartbeat every 30 min):
- Find Active tasks with no updates >24 hours (stalled)
- List tasks assigned to me (need my attention)
- Report summary if issues found, otherwise HEARTBEAT_OK

TECHNICAL:
- Use Todoist REST API v1: https://api.todoist.com/api/v1/
- API Documentation: https://developer.todoist.com/api/v1/
- Python SDK: https://doist.github.io/todoist-api-python/
- TypeScript SDK: https://doist.github.io/todoist-api-typescript/
- Store API token in ~/.openclaw/credentials/todoist (raw token, no ENV format)
- Create separate projects for Queue, Active, etc. or use a single project with labels
- Handle API rate limits gracefully

VISIBILITY:
I should open Todoist and immediately understand:
- What the agent is working on right now
- What's waiting for me
- What's stuck
- What's been completed

Adapt this to my Todoist setup. Ask me for project IDs or let me create them first.
```

## Customization

**For different task managers:**
- GitHub Projects: Use GitHub Projects API
- Linear: Use Linear API
- Notion: Use Notion database API
- Asana: Use Asana API

**State model variations:**
- Simpler: Queue → Active → Done (no waiting state)
- More complex: Queue → Active → Review → Waiting → Done
- Kanban-style: To Do → In Progress → Blocked → Done

**Reconciliation frequency:**
- More aggressive: Every 15 minutes
- Less aggressive: Every hour
- Time-windowed: Only during work hours

## Expected Behavior

Once built, the system should:

1. **Auto-create tasks** when the agent starts work
2. **Update task status** as work progresses
3. **Assign to you** when blocked on input
4. **Add comments** with progress updates
5. **Complete tasks** when done
6. **Report stalled work** via reconciliation

You should be able to open Todoist and immediately see:
- Current work (Active project)
- Blocked work (Assigned to you)
- Queued work (Backlog project)
- Recent completions (Recently completed)

## Troubleshooting

**Agent not creating tasks:**
- Verify API token is correct
- Check credentials file has raw token (no ENV format)
- Ensure projects exist or agent has permission to create them

**Tasks stuck in Active:**
- Check reconciliation is running (heartbeat every 30 min)
- Look for stalled task reports
- Manually move tasks if needed

**Rate limit errors:**
- Todoist API has rate limits (consult docs)
- Add exponential backoff in error handling
- Reduce reconciliation frequency if needed

## Alternative Approaches

Instead of building from scratch, you can:

1. **Look for inspiration** - Browse https://clawhub.com for task management skills to use as reference, not drop-ins
2. **Have your agent build it** - Use the prompt above and let your agent create the system
3. **Integrate with existing tools** - GitHub Issues, Jira, etc.
4. **Build your own state tracking** - File-based, database, etc.

**Note on third-party skills:** Be cautious with installing skills directly from others. A poorly written or malicious skill can cause real problems. Treat community skills as inspiration rather than drop-ins. Your agent is capable of building this - use the prompt.

The key is making agent work visible, not the specific tool.
