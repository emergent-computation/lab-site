# Fieldnotes — Emergent Computation Lab

[Open the bilingual student idea browser](https://emergent-computation.github.io/lab-site/).

- 200 undergraduate research ideas, organized into 12 topics.
- Chinese by default, with an English switch; search works in either language.
- One shared eight-component assessment rubric, total/component sorting, and score explanations.
- Browser-local shortlists and notes, comparison of up to three projects, and manual Markdown export.
- No accounts, analytics, submission backend, or connection to the private lab control panel.

## Edit translations

The current Chinese wording is an initial draft; the owner plans to refine it with a Chinese model.

| File | What to edit |
|---|---|
| `locales/ideas-zh-{a1,a2,f1,f2}.json` | Chinese project descriptions, entry plans, risks and paper descriptions |
| `locales/evidence-zh-{a,f}.json` | Chinese explanations for each score component |
| `locales/ui.json` | Interface text: each value is `[English, Chinese]` |
| `locales/shared-zh.json` | Topics, featured titles, related-project descriptions and common caveats |
| `rubric.json` | Chinese labels, descriptions and scoring anchors; keep its copy in `scores.json` in sync |
| `scores.json` | Chinese assessment summaries and next checks; preserve numeric assessments |

Keep proposal IDs, field names, quantities, paper identifiers and URLs intact. Preserve conditional claims and preparation requirements. Translation edits do not change scores.

## Build and preview

Python 3 and its standard library are sufficient; there are no browser runtime dependencies.

```sh
python3 scripts/build_page.py
python3 -m http.server 8765 --directory docs
```

Open `http://127.0.0.1:8765/`, or open `docs/index.html` directly offline.

The builder checks all 200 IDs, bilingual coverage, reference URLs, component rationale keys, score bounds, weights and totals. It creates a standalone HTML file with a script-hash content security policy. `provenance/build-manifest.json` records every build input and the output hash.

To run the inherited browser interaction suite, install Playwright for development, then run `node scripts/qa_v2.cjs`. `PLAYWRIGHT_MODULE` can name an existing module installation; `SITE_URL` optionally tests a hosted same-origin copy. Browser tooling is not deployed.

## Publish changes

1. Create a feature branch and edit the source files.
2. Run the builder and commit both sources and generated `docs/index.html`/manifest.
3. Open a pull request; obtain independent review and pass the site checks.
4. Merge the verified PR. GitHub Pages publishes `main:/docs` using its native build/deployment service.

The initial empty repository uses an empty bootstrap branch, a reviewed publication PR, and then a rename of the merged default branch to `main`; no site content is pushed directly to `main`.

`main` uses reviewed PRs. Agent-written commits include an `Assisted-by` trailer; PRs state the agent/model, human-review status, review evidence and verification. Human-reviewed means a person reviewed the actual diff.

The lab automation registry records the checks and native Pages deployment before activation. Stop publishing in Settings → Pages; recover with a reviewed revert/rebuild and the normal Pages deployment. GitHub hosts deployment logs and artifacts. No local daemon or cron is needed.

## Assessment limits and future work

- Scores are provisional model judgments about proposals, not students or publication probabilities. References and resource estimates remain preliminary.
- Historical Astra/Fable scores remain separately attributed. New scores share one rubric; selected calibration disagreements and factual corrections are retained.
- Scope, source text and language refinements can be revisited without changing stable proposal IDs.
- This first public release keeps the approved translations. Further language refinement, lab homepage pages and a connection to the ideation workflow are separate later tasks.
- A full scientific novelty audit, student pilot and comprehensive accessibility/browser certification have not been completed.
