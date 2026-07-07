Now let me produce the final consolidated review.

## Summary

This paper introduces GMD-25, a benchmark for evaluating compositional generalization of Machine Learning Force Fields (MLFFs). It proposes four controlled tasks — Length Extrapolation, Functional Group Composition, Functional Group Duplication, and Functional Group Combination — each designed to isolate a specific generalization challenge. Five MLFFs (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2) are evaluated. The core empirical finding is that all models suffer OOD errors one to two orders of magnitude higher than ID errors across all tasks, demonstrating a fundamental failure of current MLFFs to generalize compositionally.

## Strengths

- **Well-motivated, controlled task design.** The four tasks are carefully constructed to probe distinct facets of compositional generalization. The paper builds *controlled* train/test splits that isolate specific challenges (e.g., length, functional-group composition, duplication, asymmetric combination), which is a genuine methodological improvement over prior benchmarks that simply expand dataset diversity. This design allows the paper to attribute failures to specific generalization deficits rather than to general OOD hardness.

- **Clear, convincing demonstration of the generalization gap.** The core finding — that all five models fail at compositional generalization, with OOD errors often one to two orders of magnitude above ID errors — is presented clearly and is likely reproducible. The logarithmic-scale plots (Figures 2–4) make the degradation unambiguous. Even where individual model rankings vary across metrics/tasks, the central takeaway (current MLFFs do not generalize compositionally) is strongly supported.

- **Practical motivation for each task.** Each task is connected to a concrete application domain (drug discovery for length extrapolation, polymer science for duplication, etc.) with cited justifications. These connections are not afterthoughts — they are argued in §3.1 — which strengthens the case that these generalization capabilities are practically relevant, not just academic curiosities.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Unexplained baseline labels in Figure 2 and Figure 3 captions.** The Figure 2 caption lists "PBE0" as a compared model and the Figure 3 caption lists "m4s" — neither appears in the model description (§4.1), which describes only SchNet, PAINN, DimeNet++, GemNet, and EquiFormerV2. Figure 2 appears to replace PAINN with "PBE0"; Figure 3 introduces an additional model "m4s" (bringing the count to six). These names may be parser artifacts from image alt-text extraction, but if they correspond to actual curves in the figures, the authors must clarify what they represent. The core trends remain visible from Figure 4 (which uses only the five described models), so this does not invalidate the main findings, but it creates confusion in two of the paper's primary result figures.

- **Mismatch between "physical principles" framing and the GFN2-xTB reference.** The paper motivates the benchmark by asking whether MLFFs "capture the underlying physical principles" (§1), but the reference labels come from GFN2-xTB, a semi-empirical tight-binding method with known systematic errors relative to higher-level DFT. This creates a framing mismatch: failure to generalize on GFN2-xTB labels could reflect difficulty learning the specific quirks of the semi-empirical model rather than failure to learn physics. The paper acknowledges GFN2-xTB's nature (semi-empirical, "balance between computational efficiency and accuracy" in §3), but the "physical principles" language in the intro and conclusion is overly strong given the reference. A small calibration experiment comparing GFN2-xTB to DFT on a subset of OOD configurations would substantially strengthen the paper.

- **No error bars or multi-seed results.** No confidence intervals or multi-seed variance estimates are reported. With training set sizes of ~10,000 frames from only 5 molecules (base length extrapolation), variance across training runs could be substantial. The paper's stated goal of identifying "architectural biases" through model rankings would be more credible with evidence that the rankings are robust.

### Trivial
None.

## Nice-to-Haves

- **Inclusion of MACE.** MACE (Batatia et al., 2022) — arguably the most prominent MLFF of recent years — is cited but not evaluated. Its higher-order equivariant message passing is specifically motivated by data efficiency and generalization, making it a natural inclusion that would strengthen the claim of evaluating "a diverse set of state-of-the-art MLFFs."

- **Physically motivated baselines.** Classical force fields (e.g., UFF, GAFF) or GFN2-xTB applied to OOD molecules without retraining would establish a performance floor, helping readers assess how far current MLFFs are from a useful baseline versus from an idealized target.

## Removed Points

These points from the input review were removed with justification:

1. **"PBE0/m4s makes figures uninterpretable (fatal)"** — Downgraded from fatal to minor. The core trend is visible from Figure 4 alone (which uses only the 5 described models). The inconsistency is confusing but does not invalidate the paper's main conclusion. Additionally, the names appear only in figure captions and could be parser artifacts.

2. **"Missing limitations section"** — Removed. This is a formatting preference; the reproducibility statement (§5) serves a related function. Most ICLR papers at this stage do not require a separate limitations section.

3. **"16 fs timestep is unusually large"** — Removed. The paper cites FlashMD (Bigi et al., 2025), a method designed for long-stride simulations, which adequately justifies the choice.

4. **"Augmented Length Extrapolation framing is imprecise"** — Removed. The paper explicitly notes this variant "might expect ... to be easier" (§3.1), and the task tests compositional generalization (functional-group transfer across lengths) rather than raw length extrapolation, which is a valid and clearly described goal.

5. **"Missing MACE as a critical omission"** — Downgraded from major weakness to nice-to-have. The five models evaluated represent a reasonable diversity of architectural families. MACE would strengthen the set but its absence does not undermine the findings.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the Figure 2/3 caption inconsistency.** Clarify whether PBE0 and m4s correspond to actual baselines or are PDF-extraction artifacts. If they are real baselines, describe them in §4.1; if they are artifacts, correct the captions.
2. **Add error bars or multi-seed results** for at least the main findings to establish robustness of model rankings.
3. **Calibrate the GFN2-xTB reference** against a higher-level DFT method (e.g., PBE0 or ωB97X-D3(BJ)) on a small subset of OOD configurations to quantify the approximation gap and better contextualize the "physical principles" framing.
4. **Soften the "physical principles" language** in the introduction and conclusion unless the calibration experiment is added.

## Score and Decision

**Scoring calibration.** I retrieved and item-weighted several anchors:

| Anchor | Avg Score | Comparison |
|--------|-----------|------------|
| `EGraFFBench` (NvJxTjTQtq) | 6.00 | Similar MLFF benchmark paper. Had much heavier negatives (-8.04, -8.38 about lack of novelty, -4.80 about wrong experimental results). Our paper has milder weaknesses. |
| `Understanding and Mitigating Distribution Shifts for MLFFs` (Xk9Q0CrJQc) | 6.25 | Similar topic (MLFF OOD generalization). Had heavy negatives about limited practical utility (-8.30) and modest gains (-7.06). Our paper has no such claim-reality gap. |
| `A new framework for OOD generalization in biochemical domain` (qFZnAC4GHR) | 6.67 | Similar topic (OOD generalization benchmark). Had very heavy negatives (-10.32, -9.31) about utility/novelty concerns. |
| `Pushing Limits of All-Atom Geom-GNNs` (4S2L519nIX) | 6.50 | Related but more about pre-training. Shared some positive weight profiles. |

**Weighted-item comparison.** Our paper's strongest negative weights (PBE0/m4s at -1.96, GFN2-xTB framing at -1.55) are substantially milder than the -5 to -10 negatives in all anchors above. Our positive weights (+4.75 for the generalization gap demonstration, +4.28 for practical motivation) are in the same range as the anchors' best positives. This places the paper comfortably above the 6.0 anchors and in line with the 6.5–6.67 range. I bracket to **6.0–7.0** after Round 1, then narrow to **6.5** after comparing item weights.

The paper makes a solid, well-motivated contribution: a controlled benchmark for compositional generalization in MLFFs, with carefully designed tasks and a clear demonstration that current models fail at this capability. The weaknesses are presentational (figure caption inconsistencies), framing-related (overstated "physical principles" language), and methodological (lack of error bars). None of these threaten the paper's core finding, and they are addressable in a rebuttal/revision.

**Score: 6.5 — Borderline Accept**

**Decision: Accept**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>