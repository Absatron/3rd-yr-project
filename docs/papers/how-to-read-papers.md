# How to read research papers (project reference)

Based on established practice: Keshav (2012) [*How to Read a Paper*](https://cseweb.ucsd.edu/~dstefan/cse227-spring22/papers/keshav:how.pdf); Carey et al. (2020) [*Ten simple rules for reading a scientific paper*](https://doi.org/10.1371/journal.pcbi.1008032), *PLOS Computational Biology*.

**Core rule:** Read for a **question**, not for completion. Do not read front-to-back on first contact.

---

## Before you open the PDF

Write 1–3 questions you want this paper to answer. Examples for this project:

- How is the perception → imagery split defined?
- Which decoders generalise and which fail?
- What metrics separate decoding from generative prior effects?

---

## Pass 1 — Screen (~15–20 min)

**Read:** title, abstract, figure/table captions, conclusions.

**Skip:** related work, methods detail, proofs.

**Decide:** Keep reading (Pass 2) or drop from active list?

**Answer (Keshav’s five Cs):** Category, context, correctness, contributions, clarity.

---

## Pass 2 — Understand (~45–60 min)

**Order (not necessarily sequential):**

1. Introduction (motivation + contributions)
2. Methods / experimental setup
3. Results + figures
4. Discussion (limitations, interpretation)

**Skip on Pass 2:** long related work (mine citations later), appendix unless you need a metric definition.

**While reading:** fill [`notes/TEMPLATE.md`](notes/TEMPLATE.md).

**Carey et al. — six questions to answer:**

1. What did the authors want to know?
2. What did they do?
3. Why that approach?
4. What do the results show?
5. How do the authors interpret them?
6. What should be done next?

---

## Pass 3 — Implement / cite deeply (as needed)

Only for **core papers** you will reproduce or ablate (e.g. NSD-Imagery, MIRAGE).

- Methods subsections in full
- Equations (what each term does, not full re-derivation)
- Appendix (hyperparameters, ablation variants)
- Related work → snowball citations

---

## Reading order for this project

| Paper | Pass 1 | Pass 2 | Pass 3 |
|-------|--------|--------|--------|
| NSD-Imagery | ✓ | ✓ | Before experimental design |
| MIRAGE | ✓ | ✓ | Before MIRAGE reproduction |
| MindEye2, Brain Diffuser | ✓ | ✓ | Only if comparing architectures |
| Supporting neuroscience / CLIP–brain | ✓ | Optional | Rarely |

---

## Notes vs literature review

| Artifact | Purpose |
|----------|---------|
| `docs/papers/notes/*.md` | Your per-paper quarry — what you extracted |
| `hypothesis_formulation/` | Agent + you — synthesis, H₀, gaps across papers |
| Final report Related Work | Narrative argument — cites subset of what you read |

Not every paper in your notes file appears in the final report. Not every read paper needs full notes — only papers that inform design, methods, or argument.

---

## References

- Keshav, S. (2012). How to read a paper. *ACM SIGCOMM Computer Communication Review*. https://cseweb.ucsd.edu/~dstefan/cse227-spring22/papers/keshav:how.pdf
- Carey, M. A., Steiner, K. L., & Petri, W. A. (2020). Ten simple rules for reading a scientific paper. *PLOS Computational Biology*, 16(7), e1008032. https://doi.org/10.1371/journal.pcbi.1008032
- Raff, J. How to read and understand a scientific paper. Duke ARC. https://arc.duke.edu/how-to-read-and-understand-a-scientific-paper-a-guide-for-non-scientists/
