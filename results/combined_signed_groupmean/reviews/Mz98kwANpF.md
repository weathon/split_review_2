Here is my final consolidated review.

## Summary

This paper challenges the prevailing multi-component LoRA paradigm for multi-task learning. It first shows that simplifying a multi-head LoRA design (M-LoRA) by removing the dynamic router yields better performance despite higher inter-head similarity, contradicting the assumption that head diversity is essential. It then demonstrates that a single high-rank LoRA adapter can match multi-component architectures. Building on these observations, the paper proposes Align-LoRA, which adds a KL-divergence-based alignment loss on the down-projection matrix's output to encourage task-shared representations. The method adds zero inference overhead and is evaluated across LLaMA2/3 and Qwen2.5 models (3B–14B).

## Strengths

- **M-LoRA finding is a genuine empirical contribution.** The observation that removing the dynamic router from R-LoRA (producing M-LoRA) results in higher inter-head similarity yet *better* multi-task performance (Table 1, Figure 2) directly challenges the prevailing diversity-is-beneficial assumption in multi-head LoRA designs. This is the paper's most compelling result and stands as a meaningful finding regardless of Align-LoRA's merits.

- **High-rank LoRA experiment fills a gap.** Demonstrating that a single LoRA adapter with matching parameter count is broadly competitive with multi-component architectures (Tables 2 and 3) is a useful sanity check that prior multi-adapter papers largely omitted. This is a clean experimental contribution.

- **Align-LoRA is simple and practical.** The method adds a KL-based alignment loss on the down-projection A's output, introduces zero inference overhead, and can be merged into the backbone. This simplicity is a genuine virtue compared to routing-based multi-component alternatives that incur non-mergeable inference latency.

- **Evaluation across multiple model families and scales** (LLaMA2 7B/13B, LLaMA3 8B, Qwen2.5 3B/7B/14B) is more thorough than many LoRA papers.

## Weaknesses

### Fatal
None.

### Major

- **No error bars, repeated runs, or variance reported anywhere.** Table 1 reports performance differences of 0.78 points (M-LoRA vs R-LoRA) and 1.41 points (M-LoRA vs HydraLoRA). Tables 4 and 5 report improvements of 1–3 points. Without standard deviations, confidence intervals, or information about the number of random seeds, there is no way to know whether these differences are statistically meaningful or within the noise of a single run. Given that MTL benchmark scores are noisy, this omission fundamentally limits the reliability of the paper's empirical claims. This is the single most important weakness.

- **A factually inaccurate claim about experimental results.** The paper states (Section 5.2, near line 251) that "both the KL and MMD-based alignment strategies elevate performance above the standard LoRA baseline." However, in Table 4 on Qwen2.5-7B, A-LoRA-M (47.53) scores *below* standard LoRA (48.36). On Qwen2.5-14B (Table 4), A-LoRA-M (52.24) also scores below standard LoRA (52.93). This inaccurate claim undermines confidence in the robustness claims about the MMD variant and should be corrected. The MMD variant's inconsistency across settings is itself a finding that needs analysis, not glossing over.

- **The theoretical analysis (Section 5.3) does not constitute a genuine contribution.** The generalization bound R_MTL(f) ≤ (1/M) Σ R_train + (λ/M) Σ Δ(D_i, D_j) + O(√(log(1/δ)/n_total)) is a standard multi-task/domain adaptation bound (essentially Ben-David et al., 2006). It contains no LoRA-specific terms (no rank dependence, no low-rank structure, no reference to the A/B decomposition). The claim that "Align-LoRA minimizes Δ(D_i, D_j) during training" simply restates what the method does — the bound says "if you minimize Δ the bound improves," which is circular reasoning, not a derivation that Align-LoRA has a tighter bound than alternatives. Calling this a "novel generalization bound" (Section 6) overstates what is provided. This section should be either substantially reworked to incorporate LoRA-specific analysis or removed.

### Minor

- **The evaluation scope is limited to classification/reasoning benchmarks** (BBH, QNLI, PIQA, ARC, GSM8K). For a paper claiming a general principle about multi-task PEFT (that "learning task-shared representations" is a superior paradigm), the lack of generative task evaluation (summarization, instruction following, dialogue) limits the generality of what can be concluded. Tasks that naturally require divergent features may behave differently under representation alignment.

- **The rank confound in the Align-LoRA ablation is not fully resolved.** In Table 4, A-LoRA-K uses rank 8 while M-LoRA uses rank 4. Although A-LoRA-K (0.20% params) uses fewer total parameters than LoRA rank 10 (0.25%) and still outperforms it, the cleaner comparison of A-LoRA-K vs M-LoRA at the same rank (e.g., both rank 4) is not presented in the main text, making it difficult to attribute improvements entirely to alignment versus increased rank capacity.

- **No limitations or failure case analysis.** The paper presents Align-LoRA uniformly as superior, but representation alignment could plausibly hurt in settings where tasks require genuinely divergent features (e.g., tasks with opposing input-output mappings, very different domains). There is no discussion of when the approach might fail, no analysis of task interference under alignment, and no acknowledgment of this scope limitation.

- **The novelty claim is somewhat overstated.** The paper states it is "the first work to systematically apply statistical distance metrics for this purpose within the multi-task LoRA framework" (Section 5.1). The qualifier "within the multi-task LoRA framework" narrows the scope, but applying KL divergence or MK-MMD to align representation distributions is well-established in domain adaptation (the paper itself cites Pan et al., 2010 and Gretton et al., 2012). The incremental contribution — applying this idea to LoRA's low-dimensional space — should be more carefully delineated.

### Trivial
None.

## Nice-to-Haves

- A sensitivity analysis on the Gaussian diagonal-covariance assumption for the batch-wise distributions and its robustness to small batch sizes per task.
- Quantified training-time overhead of computing pairwise KL divergences across M tasks per batch.

## Removed Points

These points from the harsh review input are removed with justification:

1. **"The M-LoRA attribution explanation (heads forming a collaborative ensemble) is one explanation among several"** — The paper provides dropout-ablation evidence (HydraLoRA w/o Router) supporting its hypothesis. Scientific explanations can have alternatives; this is not a weakness.
2. **"Section 4 claim of 'competitive/superior' is only partially true"** — The paper says "competitive with, and at times superior to" (line 144), which is accurate given Table 3 results. This criticism is not factually grounded.
3. **"Gaussian assumption not justified / small batch covariance concerns"** — Overly speculative; the paper is an empirical NLP systems paper, not a statistical methodology paper. The appendix (stripped by parser) may address this.
4. **"Missing generative task evaluation"** — Retained as "evaluation scope" minor weakness above, but demoted from the more severe framing the reviewer gave it.
5. **Missing related works speculations** — Removed per policy.
6. **Formatting/style nitpicks and appendix-stripped content concerns** — Removed per policy.

## Novel Insights

The reviews surface a structural tension in the paper: its strongest contribution (the M-LoRA finding empirically challenging the diversity assumption) is largely independent from its proposed method (Align-LoRA adding an alignment loss). The paper's narrative connects them through the "task-shared knowledge" hypothesis, but the M-LoRA finding is an observational challenge to the existing paradigm, while Align-LoRA is a prescriptive intervention. These could be treated as two distinct contributions — the empirical challenge stands on its own, while the alignment method needs tighter experimental controls (same-rank comparison, error bars) to confirm that alignment per se is the driver rather than increased capacity. The factual error about A-LoRA-M's performance relative to standard LoRA is particularly concerning because it suggests the paper's broad claims about the MMD variant's effectiveness do not hold across all settings tested, and this is not acknowledged.

## Suggestions

1. **Add error bars** — Report results from at least 3 random seeds with standard deviations for all main tables. This is essential given the modest margins.
2. **Correct the inaccurate claim** — Acknowledge that A-LoRA-M underperforms standard LoRA on 2 of 3 models in Table 4, and discuss why the MMD variant is inconsistent.
3. **Either rework or remove the theoretical analysis** — If kept, the bound must incorporate LoRA-specific properties (rank, low-dimensional structure) and produce a comparison that explains why Align-LoRA specifically achieves a tighter bound. If this cannot be done, remove the section — it adds no value as currently written.
4. **Add the rank-controlled ablation** — Compare A-LoRA-K (rank 4) against M-LoRA (rank 4) and standard LoRA (rank 4) to cleanly isolate the effect of alignment from capacity.
5. **Include a limitations section** — Discuss when alignment might hurt, computational overhead during training, and the scope of evaluation.

## Score and Decision

**Calibration round 1 bracket:** I bracketed by retrieving papers on multi-task LoRA across score bands. Strong-reject band (avg ≤1.5) returned papers on unrelated topics. Bands 1.5–3.5 returned **UnoLoRA (3.0)**, **DLP-LoRA (3.0)**, **ATM (3.0)**. Band 3.5–5.5 returned **MORE (4.0)**, **I-LoRA (4.0)**, **Seeded LoRA (5.0)**, **LoraHub (5.33)**, **PaLoRA (5.50)**. Band 5.5–7.5 returned **C-Poly (6.0)**, **Parameter-Efficient Multi-Task Model Fusion (7.0)**, **VeRA (7.25)**. Band 7.5–8.5 returned **HiRA (8.0)**. No papers above 8.5.

**Calibration round 2 narrowing:** I itemized the closest topical anchors: **UnoLoRA (3.0)** — method unclear, only T5 experiments, no error bars; **MORE (4.0)** — limited novelty over MoE-LoRA, only GLUE; **Seeded LoRA (5.0)** — limited novelty (model soup to LoRA), only LLaMA2; **LoraHub (5.33)** — novel framework but underperformed ICL; **PaLoRA (5.50)** — accepted, good presentation and efficient Pareto front method.

**Final score placement:** The paper under review is clearly stronger than UnoLoRA (3.0) and MORE (4.0) — broader evaluation, more interesting empirical findings. It is comparable to Seeded LoRA (5.0) and LoraHub (5.33), both of which were rejected. Like those papers, this paper has real contributions undermined by significant methodological weaknesses. The decisive weaknesses — no error bars (-10.00), factual inaccuracy about A-LoRA-M (-10.00), and non-contributory theory (-10.00) — collectively pull the score below the acceptance threshold despite very strong strengths (the M-LoRA finding, high-rank experiment, and clean method each scoring +9.5+). The paper shares with Seeded LoRA the pattern of an interesting core idea with insufficient empirical rigor. I therefore place it at **5.0**, in the borderline-reject zone where the contributions are recognized but the weaknesses are too significant for acceptance in the current form.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>