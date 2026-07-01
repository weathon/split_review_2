## Summary

This paper proposes **ScaPre**, a framework for large-scale concept unlearning in text-to-image diffusion models. It introduces three components: (1) a spectral trace regularizer with S and R matrices that stabilizes the optimization under conflicting concept updates, (2) Bures-distance geometry alignment that preserves global covariance structure, and (3) a mutual-information-based Informax Decoupler that localizes updates to concept-relevant channels. The core optimization reduces to a Sylvester equation (efficiently solvable in closed form), with the non-quadratic geometry alignment handled via a separate proximal refinement. Experiments on Imagenette, ImageNet-Diversi50 (50 concepts), ImageNet-Confuse5, and artistic-style benchmarks show strong unlearning performance while maintaining generative quality, often surpassing existing methods by a wide margin.

---

## Strengths

- **Novel, well-motivated method architecture.** The three components (spectral trace regularizer, Bures-distance geometry alignment, Informax Decoupler) are each non-trivial and grounded in distinct principles (second-order statistics, covariance geometry, mutual information). The closed-form Sylvester-equation solution for the quadratic sub-objective is elegant and avoids iterative fine-tuning.
- **Consistently strong empirical results across diverse settings.** On Imagenette (Table 1): 0.8% Avg Acc vs. next-best closed-form methods (RECE 4.9%, UCE 8.5%). On ImageNet-Confuse5 (Table 4): 84.3% Overall Acc vs. next-best (SP at 50.3%, ESD at 50.2%). On Diversi50 (Table 3): ScaPre achieves 3.9% Avg Acc with CLIP 29.41, while UCE/RECE collapse to 0.0% / 22.23 and 21.78 respectively — demonstrating the method avoids the "destroy the model" failure mode.
- **Genuine efficiency advantage.** 120 seconds for 50 concepts at 5 GB peak memory on a single A6000 is a concrete, verifiable claim backed by GPU-hour and memory reports for all baselines (Figure 3).
- **Honest reporting of limitations.** The paper acknowledges that ScaPre does not reach 0% unlearning accuracy on Diversi50 (it gets 3.9%) and does not claim otherwise, lending credibility to the results.

---

## Weaknesses

### Fatal
None.

### Major
None that threaten the core claims. The following issues are substantive but addressable.

### Minor

- **Efficiency inconsistency between text and figure.** Section 5.5 states ScaPre "completes the unlearning of 50 concepts within only **120 seconds**" (2 minutes). However, Figure 3 reports ScaPre's execution time as **~1.5 hours** (90 minutes). The discrepancy spans two orders of magnitude. The text claims ScaPre is more efficient than UCE (which Figure 3 lists at ~0.5 hours), yet at 1.5 hours ScaPre would be *slower* than UCE. The figure's scope (total experiment time vs. per-benchmark time) is not stated, so the reader cannot resolve this inconsistency. This needs clarification.

- **No statistical uncertainty reported.** Every result in every table is a single point estimate. No standard deviations, confidence intervals, or multi-seed runs are provided. Given that unlearning accuracy can be sensitive to classifier choice, generation sampling noise, and the adaptive threshold in the Informax Decoupler, the reader cannot assess whether the large gaps (e.g., 0.8% vs. 4.9% on Imagenette) are robust. Standard practice for an empirical paper claiming state-of-the-art results.

- **The "closed-form" framing is overstated.** The abstract, introduction, and conclusion repeatedly describe ScaPre as a "closed-form solution." However, as the paper itself transparently explains in Sec. 4.3, the geometry alignment term $\mathcal{L}_g(W)$ involves matrix square roots and is "incompatible with direct closed-form optimization" — it requires a separate proximal refinement (Bures geodesic interpolation + Procrustes adjustment). The method is better described as a **hybrid**: a closed-form Sylvester solution for the quadratic sub-objective followed by a non-closed-form proximal step. The paper is transparent about the mechanics, but the headline framing leaves a misleading impression.

- **The "SP" baseline is never defined.** "SP" appears in every table (Tables 1–4, Figure 3) alongside FMN, SPM, ESD, MACE, UCE, and RECE. The Related Work section (Sec. 2) defines all other abbreviations but never introduces "SP." Based on context it likely refers to SPEED (Li et al., 2025b), a single-concept method cited in Sec. 2.1, but the paper never makes this connection explicit — nor explains how a single-concept method was applied to multi-concept benchmarks. Readers cannot tell what they are comparing against.

- **The UQ metric is relative, limiting cross-table comparability.** UQ is defined as $UQ = 100 \cdot \frac{2\tilde{A}\tilde{C}}{\tilde{A}+\tilde{C}}$ where $\tilde{A} = \sigma((\mu_A - A)/\sigma_A)$ and $\tilde{C} = \sigma((C - \mu_C)/\sigma_C)$ — the sigmoid of a z-score computed *across the methods within each table*. Consequently, a UQ of 64.09 in Table 1 is not directly comparable to a UQ of 65.30 in Table 3, because the reference distribution differs. The raw scores (Avg Acc, CLIP) tell a cleaner story, but the paper uses UQ as a headline metric without acknowledging this relativity.

- **The adaptive threshold $\tau_i$ in the Informax Decoupler is unspecified.** The paper states that $\tau_i$ is "an adaptive threshold" (Sec. 4.2) but never explains how it is computed. This makes the mutual information estimation (Eq. 6) irreproducible. The nature of the "neutral inputs" (label $y=0$) is also not stated explicitly, though they are likely empty/generic prompts.

### Trivial
- The inconsistency between the "no additional data" claim and the need for "neutral inputs" for the Informax Decoupler should be clarified (e.g., "empty prompts").

---

## Nice-to-Haves

- **Per-component ablation.** The paper references ablation studies in Appendix C.5–C.7 (stripped by the parser). An ablation that isolates the contribution of each of the three components (spectral trace regularizer, geometry alignment, Informax Decoupler) — particularly on the Confuse5 benchmark to validate the Decoupler's role in precision — would strengthen the paper.
- **Failure case / concept interaction analysis.** The paper's narrative centers on resolving conflicting updates, but no concrete example of which concepts cause conflicts under prior methods or how ScaPre resolves them is provided. A case study of 2–3 interfering concepts (e.g., "golden retriever" vs. "labrador retriever") with and without the R-matrix regularization would be informative.
- **Per-layer computational breakdown.** Reporting wall-clock time for the SVD (in R), the Sylvester solve, and the Bures/Procrustes refinement separately would help practitioners identify bottlenecks.

---

## Removed Points

These points were raised in the input review but are removed here with justification:

1. **"No ablation isolating the three main components"** — The paper explicitly states "ablation studies in Appendix C.5–C.7." The appendix is stripped by the parser; penalizing its absence would be unfair.
2. **"Missing derivation of proximal refinement in Appendix B.2"** — Same reason: the appendix is stripped by the parser.
3. **"The vectorized form in Eq. 10 should carry an explicit caveat that it is not the recommended computational path"** — This is a presentation suggestion, not a weakness. Standard Sylvester solvers avoid the Kronecker product, and the paper already notes this.
4. **"No analysis of failure cases or concept interactions"** — Moved to Nice-to-Haves. This is a suggestion for strengthening, not a flaw.
5. **"Computational cost of Bures distance (O(d³) eigendecomposition per layer)"** — The paper reports total time (120 seconds for 50 concepts), which implicitly accounts for this. Breaking it out per-layer would be nice but is not required.

---

## Novel Insights

None beyond the paper's own contributions. The insights from the reviews are largely confirmatory: the method is novel and empirically strong, but the closed-form framing needs adjustment, the efficiency numbers have an inconsistency, and the evaluation would benefit from variance reporting.

---

## Suggestions

1. **Resolve the efficiency inconsistency.** Clarify whether Figure 3 reports total GPU-hours across all experiments (with per-benchmark breakdown in the appendix) or per-run time. If the latter, correct the discrepancy with the 120-second claim.
2. **Add variance estimates.** Report standard deviations or confidence intervals (at least 3 seeds) for the main tables.
3. **Define "SP" explicitly** and specify how it was applied to multi-concept settings.
4. **Specify how $\tau_i$ is computed** and what constitutes a "neutral input."
5. **Qualify the "closed-form" framing** in the abstract and conclusion to acknowledge the proximal refinement step, or describe ScaPre as a "hybrid closed-form + proximal refinement" method.

---

## Score and Decision

This is a strong paper with a genuinely novel method architecture, compelling empirical results, and a concrete efficiency advantage. The weaknesses are real but bounded — none invalidate the core contributions. The efficiency inconsistency and missing variance reporting are the most substantive concerns and should be addressed in a revision.

**Score: 8** (Accept)

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>