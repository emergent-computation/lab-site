# Publish the student browser on GitHub Pages

- Date: 2026-09-20; status: accepted under the owner's explicit publication request.
- Context: the bilingual local preview is ready; Chinese prose refinement is deferred by the owner.
- Decision: use the empty `emergent-computation/lab-site` repository and publish `main:/docs`.
- GitHub Free requires a public repository for Pages; this exposes only reviewed site sources and generated public files.
- Preserve separate editable locales, the common rubric, source attribution, and browser-local selections.
- Build with Python standard library; deploy only the static `docs/` output through native Pages.
- Register GitHub-hosted checks and deployment in lab-tools before activation; no local scheduled process.
- Initialize an empty bootstrap branch, merge a reviewed site PR into it, then rename that branch to `main`.
- Validation: deterministic build/data checks, inherited browser suite, release-content scan and hosted smoke check.
- Independent cross-family review covers the concrete release; full native receipts remain in the private coordination workspace.
- Limits: no full scientific novelty review or complete accessibility certification; no workflow/backend integration.
- Recovery: disable Pages or merge a reviewed revert, then rebuild the known-good revision.
- Human action: none required; the owner has authorized public publication.
