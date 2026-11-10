# Issue tracker: GitHub

Issues and specs for this repo live in GitHub Issues for `szarkab/audio-book`. Use the `gh` CLI for issue operations from this repository.

## Conventions

- Create an issue: `gh issue create --title "..." --body-file <file>`. Use an actual UTF-8 file for multiline bodies.
- Read an issue: `gh issue view <number> --comments`; fetch labels with `gh issue view <number> --json number,title,body,labels,comments` when relevant.
- List issues: `gh issue list --state open --json number,title,body,labels`, adding label and state filters as needed.
- Comment: `gh issue comment <number> --body-file <file>`.
- Apply or remove labels: `gh issue edit <number> --add-label "..."` or `--remove-label "..."`. Use the mapping in `triage-labels.md`.
- Close: `gh issue close <number> --comment "..."`.

Resolve the repository from the Git remote; this project is `szarkab/audio-book`. If `gh` is unavailable or unauthenticated, report that prerequisite rather than silently switching to another tracker.

## Pull requests as a triage surface

**PRs as a request surface: no.**

## Skill routing

When a skill says “publish to the issue tracker”, create a GitHub issue. When it says “fetch the relevant ticket”, read the issue and its comments.

## Wayfinding operations

For wayfinder workflows, use one map issue labelled `wayfinder:map` and child issues labelled `wayfinder:<type>` (`research`, `prototype`, `grilling`, or `task`). Link children with GitHub sub-issues where available; otherwise use a task list in the map and a `Part of #<map>` reference in each child.

Use native GitHub issue dependencies when available. Otherwise record `Blocked by: #<number>` references and check whether those issues remain open. An unassigned open child with no open blocker is eligible to claim, in map order. Claim with `gh issue edit <number> --add-assignee @me`. After resolving a child, close it and record its answer and link in the map.
