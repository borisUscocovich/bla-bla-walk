# Bla Bla Walk team

Challenge: heat-aware walking in Basel · Repository: [bla-bla-walk](https://github.com/danielbarmaimon/bla-bla-walk)

## People and proposed work areas

Replace each `TBD` with the contributor's GitHub username after the team chooses the role. See [ROADMAP.md](ROADMAP.md) for task dependencies, file ownership, and effort estimates. [TASK_START.md](TASK_START.md) gives copyable prompts and model settings. The task acceptance checks remain in [docs/plan.md](docs/plan.md).

| Slot | GitHub username | Work area |
|---|---|---|
| A | TBD | T0, T4 · Source feasibility, temperature and fountains |
| B | TBD | T2, T5 · Domain rules and route evaluation |
| C | TBD | T3, T9 · Screen design and checked walking routes |
| D | TBD | T1, T6 screen · Map foundation and comparison screen |
| E | @danielbarmaimon | T8, T10 calculation · City geometry and shade calculation |
| F | TBD | T10 cache/API, T6 integration, T7 · Integration and demo |

Demo and end-to-end integration owner: TBD (slot F). Timekeeper: the team can assign one if useful.

## Working rules

- Keep one shared repository. Each contributor works in their own clone, on a branch named for the task, never directly on `main`.
- Follow the file ownership in the roadmap. Ask the owner before changing their files, and agree on a handoff when the work depends on their result.
- Open a pull request when a task is ready. At least one teammate reviews it; merge only after the contributor explicitly approves.
- Keep `main` runnable. Share progress and blockers with the team regularly; there are no fixed sync times.
- Run `bash scripts/hack-guard.sh` before commits and pushes. Never bypass the privacy check.
- Record team-wide choices in `docs/decisions.md`. Keep task status in the relevant `handoff/` file.
