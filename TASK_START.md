# Pick a task and start

This is the team's task launcher. Read [HACKAMRHEIN.md](HACKAMRHEIN.md) for first-time setup. [ROADMAP.md](ROADMAP.md) shows order and dependencies. [docs/plan.md](docs/plan.md) defines each task's acceptance check. [TEAM.md](TEAM.md) maps slots to GitHub usernames.

Open this repository in Codex. Start one fresh chat per task. Choose the listed model and effort under the message box. Use **Advanced** when needed. Keep **Fast mode off**. Copy one prompt below into that chat. Codex handles branching, checks, handoff and the pull request.

The settings follow the local [HackAmRhein model guide](.agents/skills/hack-models/SKILL.md) and [official OpenAI model guidance](https://developers.openai.com/api/docs/guides/model-selection). Luna handles scoped work. Sol handles complex decisions and integrations. These are starting settings; the model picker controls availability.

## Shared metaprompt

Each launch prompt invokes these instructions:

> Read AGENTS.md and HACKAMRHEIN.md. Read TEAM.md, ROADMAP.md and docs/plan.md. Apply my local profile. Use the named task skill. Check the task's Needs against merged main. Check handoff/ for active ownership. If blocked, name the exact dependency. Start my selected task when ready. Work in my own clone. Create a task branch from current main. Respect listed file ownership. Follow the task's Done when. Work one checkable step first. Save handoff before changing chats. Run relevant checks and the privacy guard. Commit and push completed checkpoints. Open a pull request after completion. Ask before merging that pull request. Keep replies brief.

For a long task, complete one checkpoint. Save its state in handoff/. Continue in a fresh chat. For shared T10 and T6, complete only your assigned portion. Open a PR for that portion. Merge it before the next portion. Mark the parent task done after its full acceptance check passes.

## Who takes which slot

Assign slots by remaining Codex usage and interest. Give **E** the largest available allowance. Give **D** and **F** strong allowances. A and B need room for careful source and rule work. C has the lightest estimated workload. Actual allowances remain private to each person.

| Slot | Work queue | Estimated effort | Start now? |
|---|---|---:|---|
| A | T0 → T4 | 9–15 h | T0 |
| B | T2 → T5 | 8–13 h | T2 |
| C | T3 → T9 | 5–9 h | T3 |
| D | T1 → T6 screen | 7–11 h | T1 |
| E | T8 → T10 calculation | 12–22 h | Wait for T0/T1 |
| F | T10 cache/API → T6 integration → T7 | 7–13 h | Wait for T10/T6 |

Four tasks can start independently. Start T0, T1, T2 and T3 together. E and F can review early pull requests while waiting. Review work leaves task files with their owners.

## Copy one launch prompt

### A · T0 · Source and geometry feasibility

**Start:** now. **Model:** GPT-6.1 Sol. **Effort:** Medium.

```text
Start T0 for Slot A. Use $hack-build. Follow TASK_START.md's shared metaprompt. Read T0 in docs/plan.md. Begin the first verifiable source check.
```

### D · T1 · Small map foundation

**Start:** now. **Model:** GPT-6.1 Sol. **Effort:** Medium.

```text
Start T1 for Slot D. Use $hack-build. Follow TASK_START.md's shared metaprompt. Read T1 in docs/plan.md. Build the smallest runnable foundation first.
```

### B · T2 · Demo walk and rules

**Start:** now. **Model:** GPT-6.1 Sol. **Effort:** Light.

```text
Start T2 for Slot B. Use $hack-build. Follow TASK_START.md's shared metaprompt. Read T2 in docs/plan.md. Begin with one real walk example.
```

### C · T3 · Map screen design

**Start:** now. **Model:** GPT-6.1 Sol. **Effort:** Light.

```text
Start T3 for Slot C. Use $hack-design and $hack-build. Follow TASK_START.md's shared metaprompt. Read T3 in docs/plan.md. Produce the reviewable screen guide.
```

### A · T4 · Observations and fountains

**Start:** after T1 merges. T0's relevant source admission must also merge. **Model:** GPT-6 Luna. **Effort:** High.

```text
Start T4 for Slot A. Use $hack-build. Follow TASK_START.md's shared metaprompt. Read T4 in docs/plan.md. Check T1 and source admission first.
```

### E · T8 · City geometry

**Start:** after T1 merges. T0's boundary and inventory must also merge. **Model:** GPT-6.1 Sol. **Effort:** Medium.

Read [the compact preparation handoff](handoff/data-compact-offline.md) first: ingestion and offline resources already exist. Continue the remaining T8 spatial/scene/bridge checks using the configured encoding; do not repeat source downloads when matching prepared files can be verified and reused.

```text
Start T8 for Slot E. Use $hack-build. Follow TASK_START.md's shared metaprompt. Read T8 in docs/plan.md. Check T1 and T0 inventory first.
```

### C · T9 · Walking alternatives

**Start:** after T1 and T2 merge. **Model:** GPT-6 Luna. **Effort:** High.

```text
Start T9 for Slot C. Use $hack-build. Follow TASK_START.md's shared metaprompt. Read T9 in docs/plan.md. Check T1 and T2 first.
```

T4, T8 and T9 use separate files. Run them in parallel once ready.

### E · T10 · Shade calculation

**Start:** after T8 merges. **Model:** GPT-6.1 Sol. **Effort:** Medium.

```text
Start T10 calculation for Slot E. Use $hack-build. Follow TASK_START.md's shared metaprompt. Read T10 in docs/plan.md. Implement and validate the shade calculation. Hand off cache/API work to Slot F.
```

### F · T10 · Cache, API, performance

**Start:** after E's calculation merges. **Model:** GPT-6.1 Sol. **Effort:** Medium.

```text
Continue T10 cache/API for Slot F. Use $hack-build. Follow TASK_START.md's shared metaprompt. Read T10 and E's handoff. Finish caching, API and performance checks.
```

### B · T5 · Route comparison

**Start:** after T10, T9 and T2 merge. **Model:** GPT-6.1 Sol. **Effort:** Medium.

```text
Start T5 for Slot B. Use $hack-build. Follow TASK_START.md's shared metaprompt. Read T5 in docs/plan.md. Check T10, T9 and T2 first.
```

### D · T6 · Comparison screen

**Start:** after T4, T5 and T3 merge. **Model:** GPT-6 Luna. **Effort:** High.

```text
Start T6 screen work for Slot D. Use $hack-build. Follow TASK_START.md's shared metaprompt. Read T6 in docs/plan.md. Build the screen portion. Hand off integration to Slot F.
```

### F · T6 · Journey integration

**Start:** after D's screen portion merges. **Model:** GPT-6.1 Sol. **Effort:** Medium.

```text
Continue T6 integration for Slot F. Use $hack-build. Follow TASK_START.md's shared metaprompt. Read T6 and D's handoff. Connect and verify the full journey.
```

### F · T7 · Demo and fallback

**Start:** after T6 fully merges. **Model:** GPT-6.1 Sol. **Effort:** Light.

```text
Start T7 for Slot F. Use $hack-demo and $hack-build. Follow TASK_START.md's shared metaprompt. Read T7 in docs/plan.md. Prepare the demo and offline fallback.
```

## When a task is blocked

Wait for its named prerequisites. Review an active pull request. Keep file ownership with its owner. Recheck main after that PR merges. Start the next free task then.

The collaborative-report extension starts after its plan reaches main. The current launcher covers T0–T10.
