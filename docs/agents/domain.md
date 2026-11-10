# Domain Docs

This repository uses a single context: root `GLOSSARY.md` and `docs/adr/`.

## Before exploring the codebase

Read the root glossary and the ADRs relevant to the area you are about to work in. If these documents are absent, proceed without creating placeholders; create them lazily when terms or decisions are resolved through domain modeling.

## Vocabulary

Use the glossary's canonical terms in issues, specifications, code discussions, and refactor proposals. If a needed concept is missing, decide whether it is a real domain gap before adding it. Keep implementation details out of the glossary.

## Decisions

Surface conflicts with existing ADRs explicitly before proposing a contradictory change. Record a new ADR only for a consequential, hard-to-reverse decision with genuine alternatives and context a future reader would need.
