# COMP30030 Project Plan: Perception-to-Imagery Latent-Target Ablation

**Student:** Abdullah James  
**Supervisor:** Dr Jingyuan [Surname]  
**Start:** Week 0, 21 September 2026  
**Target:** Full dissertation **draft** by start of Semester 2 (~2 February 2027); implementation freeze and code submission per handbook; final report and screencast by official deadline.

**Methodology:** Milestone-driven delivery with quality gates (incremental: design → infrastructure → reproducible baseline → ablations → statistics → write-up). Aligns with supervisor guidance to verify pipeline and baseline before scaling experiments.

**Living technical plan:** `docs/workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-plan.md` (includes **CSF3 operational workflow**)  
**Progress log:** `docs/workflow_stages/execution_plans/2026-09-10-perception-imagery-latent-ablation-execution-log.md`, `runs/registry.yaml`  
**Gantt (CSV for Excel/Calc):** `docs/project-plan-gantt.csv`  
**CSF reference:** `docs/CSF/` (10-minute tutorial, onboarding response, hardware overview)

> **Handbook note:** Semester 2 key dates in the handbook are labelled as last year’s guide. For a September 2026 project start, **implementation stop** and **final report** are assumed to fall in **March–April 2027** (same week numbers, +1 year). Confirm exact dates with the COMP30030 team when published.

---

## Goals and deliverables

| #   | Deliverable                                                                               | Assessment / use          |
| --- | ----------------------------------------------------------------------------------------- | ------------------------- |
| D1  | Reproducible codebase (Option 3 dual-track: MIRAGE gate + ablation engine)                | Implementation submission |
| D2  | Reproduction gate pass (Track A vs MIRAGE Table 1)                                        | Methods / trust           |
| D3  | Ablation results (image / text / combined): decoder + reconstruction metrics + statistics | Results                   |
| D4  | Dissertation report (full draft by S2 start; final by deadline)                           | Main assessment           |
| D5  | Screencast                                                                                | Assessment                |
| D6  | Project plan + management section in report                                               | This document → report    |

**Out of scope for MVP (time buffer):** Setting B as secondary only if Setting A complete; Phase 5 extensions (ROI, MLP, VDVAE on/off).

---

## Hard and self-imposed milestones

| Date (target)                    | Milestone                                                                 | Type                      |
| -------------------------------- | ------------------------------------------------------------------------- | ------------------------- |
| **5 Oct 2026** (S1 W2)           | Project plan reviewed with supervisor                                     | Handbook                  |
| **Oct 2026**                     | CSF3 account active; Slurm tutorial + scratch layout                      | Self — **login verified** |
| **Nov 2026**                     | M0 manifest freeze (HG-0); M1 data on cluster                             | Self                      |
| **Dec 2026**                     | M2 Track A reproduction gate pass (HG-2)                                  | Self                      |
| **Jan 2027**                     | M5–M8 primary results (Setting A statistics)                              | Self                      |
| **~2 Feb 2027** (S2 W1)          | **Full dissertation draft** (all sections; results may need minor polish) | **Self (early finish)**   |
| **~27 Mar 2027** (S2 W8, 14:00)  | **Implementation / code submission stops**                                | Handbook (est.)           |
| **~27 Apr 2027** (S2 W10, 14:00) | **Final report + screencast**                                             | Handbook (est.)           |
| **28 Apr 2027+**                 | Q&A period                                                                | Handbook (est.)           |

---

## Gantt overview (Semester 1 → early Semester 2)

Columns: **S1 weeks** from 21 Sep 2026. `████` = primary focus that week. `▓` = secondary / writing alongside.

| Task / work package                                              | W0–1 | W2–3 | W4–5 | W6–7 | W8–9 | W10–11 | W12–13 | W14–15 | S2 W1–2   |
| ---------------------------------------------------------------- | ---- | ---- | ---- | ---- | ---- | ------ | ------ | ------ | --------- |
| **A. Planning & admin** (plan, CSF, NSD access)                  | ████ | ██   | ▓    |      |      |        |        |        |           |
| **B. Design & protocol** (already largely complete)              | ██   |      |      |      |      |        |        |        |           |
| **C. Code scaffold** (`mirage_ablation`, Track A notebooks)      |      | ████ | ████ | ▓    |      |        |        |        |           |
| **D. M0–M1** manifests, ingest, splits (Tier 1→3 on CSF)         |      | ▓    | ████ | ████ | ▓    |        |        |        |           |
| **E. M2 Track A gate** (reproduce MIRAGE combined)               |      |      |      | ▓    | ████ | ████   | ▓      |        |           |
| **F. M3–M4** ridge, λ, latent cache (Track B)                    |      |      |      |      | ▓    | ████   | ████   | ▓      |           |
| **G. M5–M6** decoder metrics + diffusion recon                   |      |      |      |      |      | ▓      | ████   | ████   | ▓         |
| **H. M7–M8** parity + statistics (Setting A)                     |      |      |      |      |      |        | ▓      | ████   | ██        |
| **I. Dissertation writing** (Intro outline, Methods, background) |      | ▓    | ▓    | ▓    | ██   | ██     | ██     | ████   | ████      |
| **J. Full draft assembly**                                       |      |      |      |      |      |        | ▓      | ██     | ████      |
| **K. Setting B / appendix** (if slack)                           |      |      |      |      |      |        |        | ▓      | ▓         |
| **L. Final polish, screencast, code freeze prep**                |      |      |      |      |      |        |        |        | → Mar–Apr |

**Dependencies (critical path):** A → C → D → E → F → G → H → J. Writing (I) runs in parallel from W2 onward so the draft is not left until February.

---

## Week-by-week sketch (realistic, generous buffers)

| Week          | Dates (approx.)  | Focus                                                                  | Exit criterion                   |
| ------------- | ---------------- | ---------------------------------------------------------------------- | -------------------------------- |
| S1 W0–1       | 21 Sep – 4 Oct   | Finalise this plan; email Year 3 lead / CSF; NSD form; supervisor sync | Plan shown to supervisor         |
| S1 W2–3       | 5 – 18 Oct       | Implement minimal pipeline scaffold; Tier 1 AWS sync; local dev        | Repo runs preflight; HG-0 prep   |
| S1 W4–5       | 19 Oct – 1 Nov   | CSF data sync; M0 freeze; start M1 ingest                              | Manifests committed              |
| S1 W6–7       | 2 – 15 Nov       | Complete M1; leakage checklist HG-1                                    | Splits + processed betas on CSF  |
| S1 W8–9       | 16 – 29 Nov      | Track A env + ridge + inference (M2)                                   | Gate metrics computed            |
| S1 W10–11     | 30 Nov – 13 Dec  | Finish M2; HG-2; begin Track B S5–S6                                   | Gate pass or documented blockers |
| S1 W12–13     | 14 – 27 Dec      | S7–S8 (latents + decoder metrics); **holiday buffer**                  | $D_{s,i,c}$ tables               |
| S1 W14–15     | 28 Dec – 10 Jan  | S9–S10 reconstructions (GPU queue)                                     | $R_{s,i,c}$ tables               |
| S1 W16+ / Jan | Jan 2027         | M7 parity; M8 S11; draft Results                                       | Primary inference complete       |
| **S2 W1**     | **~2 Feb 2027**  | **Full draft due**; supervisor read-through                            | Complete draft PDF               |
| S2 W2–7       | Feb – mid Mar    | Revisions, Setting B if planned, screencast script                     | Near-final report                |
| S2 W8         | **~27 Mar 2027** | Code submission                                                        | Repo frozen                      |
| S2 W10        | **~27 Apr 2027** | Final report + screencast                                              | Submission                       |

---

## Data and compute management

| Item                      | Plan                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Compute**               | **CSF3 (Slurm)** — all training and diffusion via `sbatch`; max **4 GPUs** concurrent; submit steadily |
| **Login nodes**           | SSH, edit jobscripts, **AWS s3 sync only** — no ridge/diffusion on login                               |
| **Code**                  | Git repo on laptop + clone on CSF **home** (`~/comp30030-mirage-ablation/`)                            |
| **Jobscripts**            | `scripts/csf/*.sbatch` in repo; copy to scratch before submit                                          |
| **Raw NSD data**          | **CSF scratch** (`~/scratch/comp30030-mirage-ablation/data/`); sync from S3 on login node              |
| **Home (CSF)**            | Backed-up: jobscripts, manifests, env locks, small logs (quota-limited)                                |
| **Scratch (CSF)**         | Fast temporary: betas, artifacts, reconstructions — **3-month cleanup**; refresh from S3 if needed     |
| **RDS**                   | Long-term: final metrics, repro bundle (M10) per IT guidance                                           |
| **Laptop**                | Writing, Git push/pull, SSH to CSF; Tier 1 metadata optional locally                                   |
| **External 500 GB drive** | Optional personal backup; not primary execution store                                                  |
| **Re-runs**               | S7 latent cache on scratch so S8 can iterate without repeating all S9                                  |

### CSF workflow (summary)

1. Develop on laptop → push Git → pull on CSF home.
2. `cd ~/scratch/comp30030-mirage-ablation` → run data sync / `sbatch`.
3. Monitor `squeue`; read `slurm-*.out` on failure.
4. Copy small results to home or RDS; log job IDs in `runs/registry.yaml`.

See `docs/CSF/10-min_tutorial.md` and execution plan § CSF3 operational workflow.

---

## Risks and remedial action

| Risk                   | Likelihood | Impact | Mitigation                                                                        |
| ---------------------- | ---------- | ------ | --------------------------------------------------------------------------------- |
| CSF access delayed     | Medium     | High   | Tier 1 + code on laptop; escalate via supervisor; narrow smoke test on subset     |
| Track A gate fails     | Medium     | High   | Reproducibility log; fix env before ablations; do not report Track B until parity |
| GPU queue backlog      | High       | Medium | Submit jobs early Dec/Jan; reduce parallel conditions only after combined gate    |
| Underestimated S9 time | Medium     | High   | Track A gate first (smaller run count); schedule GPU weeks in Jan                 |
| Draft slip past Feb    | Medium     | Medium | Write Methods from execution plan now; Results templated before numbers arrive    |
| Handbook date shift    | Low        | Medium | Watch COMP30030 announcements; keep 2-week buffer before Mar/Apr                  |

---

## Progress to date (as of 2026-10-02)

| Area                                                                    | Status                                                        |
| ----------------------------------------------------------------------- | ------------------------------------------------------------- |
| Hypothesis, experimental design, pipeline, model design, execution plan | **Complete / approved**                                       |
| Execute-experiment kickoff (prerequisites, registry, logs)              | **Complete**                                                  |
| CSF3 account and login                                                  | **Complete** (`login3[csf3]`)                                 |
| Slurm first job + scratch layout                                        | **In progress** (10-min tutorial)                             |
| NSD access, data sync to scratch                                        | **Pending**                                                   |
| M0–M10                                                                  | **Not started** (awaiting NSD + scaffold + Slurm smoke tests) |

---

## Report section: Project management (boilerplate you can adapt)

I used a **milestone-driven** approach with **quality gates**, combining fixed upfront experimental design (to prevent data leakage and protocol drift) with **incremental execution**: manifests and ingest first, MIRAGE reproduction gate second, then ablation experiments and statistical inference. Progress is tracked in a run registry (`runs/registry.yaml`), an execution log, and milestone IDs M0–M10 defined in the approved execution plan. I planned tasks in **one- to two-week** chunks with explicit dependencies; a Gantt chart (above) maps work to Semester 1 weeks with a self-imposed milestone of a **full draft by Semester 2 Week 1**. Compute and large datasets are confined to **CSF cluster storage**; the personal machine is used for development and writing. Risks (access delays, reproduction failure, GPU scheduling) have documented mitigations. The plan is revised when blockers or supervisor feedback require cascade updates to downstream stages.

---

## Next actions

1. Show supervisor **`docs/project-plan-gantt.csv`** (open in Excel) + this document.
2. Finish CSF 10-minute tutorial; create `~/scratch/comp30030-mirage-ablation/`.
3. Clone repo on CSF home; add first `scripts/csf/` jobscript template.
4. NSD DUA → Tier 1–2 sync on login node → M0 on scratch.
5. Start **Methods** draft from `experimental_strategies/` (laptop, parallel).
