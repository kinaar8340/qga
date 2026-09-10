# Contributing

Read [START_HERE.md](START_HERE.md) first. Then [book/HOW_TO_USE.md](book/HOW_TO_USE.md) for claim labels.

- **Theorem / Model / Hypothesis / Software fact** is the contract. Do not promote a Model into a Theorem.
- `lib/` is pedagogical book code. Shared Hopf / quaternion / Hurwitz primitives belong in [`flux_hopf_lib`](https://github.com/kinaar8340/flux_hopf_lib).
- Do not add a path to `~/Projects/...`. Pin published tags.
- Run `python3 -m pytest -q` before a PR. PDF rebuild: `./scripts/build_latex.sh`.
- Open problems live in [notes/open_problems.md](notes/open_problems.md). OP5 status is a Partial result owned by [`op5`](https://github.com/kinaar8340/op5); do not mark it “all Open.”
