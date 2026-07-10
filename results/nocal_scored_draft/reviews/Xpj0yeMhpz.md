## Summary

This paper decouples class labels from target concepts in machine unlearning, identifying that prior work assumes these coincide. It formalizes three novel mismatch scenarios (target, model, data mismatch) via label domains (ℒ_D, ℒ_M, ℒ_T), analyzes forgetting dynamics at the representation level, and proposes TARF (TARget-aware Forgetting), a framework combining annealed gradient ascent with target-aware gradient descent. Empirically, TARF dramatically outperforms baselines on target and data mismatch settings, often by orders of magnitude (Gap 0.21 vs. 8.86 on CIFAR-100 target mismatch), and scales to ImageNet-1k and real-world applications.

## Strengths

- **Problem framing — decoupling class labels from target concepts (Section 1, Figure 1).** The paper identifies a genuine blind spot in unlearning research by formalizing three mismatch scenarios (target, model, data mismatch) using label domains and the ≺ relation. This taxonomy is conceptually well-structured and likely to influence how future unlearning work defines its settings.

- **Impressive quantitative results on target mismatch and data mismatch (Table 3).** On CIFAR-100 target mismatch, TARF achieves Gap=0.21 vs. the next best method (GA at 8.86); on data mismatch, TARF Gap=1.17 vs. GA's 2.43. TARF nearly matches the Retrained reference while baselines leave large accuracy on the target concept (UA of 20–60% for baselines vs. 0–0.31% for TARF). These are qualitatively different outcomes that strongly validate the paper's core thesis.

- **Representation gravity analysis (Theorem 3.2, Definition 3.3, Figures 3 and 5).** The paper provides a formal link between representation similarity and forgetting dynamics, then operationalizes this into I_con for target identification. Figure 5(a) empirically demonstrates clean separation: target-concept classes show sharp accuracy drops after Phase I gradient ascent while other classes do not.

- **Evaluation breadth.** Tests on CIFAR-10/100, Tiny-ImageNet, ImageNet-1k (Table 4), plus case studies on stable diffusion concept removal and LLM unlearning (TOFU). Scaling to ImageNet-1k is non-trivial and results are consistent with smaller-scale findings.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Gap metric arithmetic discrepancy for SCRUB in model mismatch (Table 3).** For SCRUB on CIFAR-10 model mismatch, the reported Gap is 2.60, but recomputing from the row values (UA=95.14, RA=99.81, TA=94.22, MIA=15.38 vs. Retrained: UA=87.76, RA=99.58, TA=95.91, MIA=20.57) gives (7.38+0.23+1.69+5.19)/4 = **3.62**. For CIFAR-100, reported Gap=2.45 vs. computed ≈1.70. These discrepancies affect the one setting where TARF is not dramatically better than baselines, so precision matters. (Note: the corrected Gap values would strengthen TARF's relative position — 2.90 vs. 3.62 on CIFAR-10 — but the reported numbers need verification regardless.)

- **Underspecification of target identification procedure (Section 3.3, Eq. 5, line 61).** The paper states it "assume[s] that the number of classes in D_un belonging to the target concept is known" for target mismatch. Separately, β is described as set by a quantile heuristic (top-10%). These are different mechanisms (exact count vs. heuristic threshold), and it is unclear which is used in the main results. An ablation without the count prior would clarify whether the method generalizes to settings where target concept size is unknown.

- **The theoretical contribution (Theorem 3.2) is motivational rather than predictive.** The bound contains terms (λ_max(J_θ), C_ℓ, O(η²)) that are never measured, controlled, or tracked empirically. No quantitative prediction follows from it. The paper's main contribution is empirical/algorithmic, and the framing should acknowledge this more directly.

- **The Gap metric equally weights four heterogeneous quantities (UA, RA, TA, MIA) with different scales across scenarios.** In model mismatch, the Retrained reference has UA=87.76 and MIA=20.57 (unlike the zero/near-100 profiles in other settings), so a single aggregate number conflates different failure modes. Reporting per-metric absolute differences alongside the aggregate Gap would substantially improve interpretability.

- **The TOFU application table (Table 5) shows suspiciously identical values across TARF(GA) and TARF(NPO) in every cell, and some sections show identical values between GA and TARF.** This needs clarification — either a formatting error or an explanation of why two TARF variants produce identical outputs across all settings.

- **Stable diffusion concept removal (Figure 6) is presented with only qualitative comparisons and no quantitative metric.** A CLIP-score change or other measure would strengthen this real-world application claim.

### Trivial
None.

## Nice-to-Haves
- Replace or supplement the aggregate Gap with per-metric distance plots or a radar chart.
- Derive a testable prediction from Theorem 3.2 (e.g., correlation between d_h and ΔL) to sharpen the analysis.
- Include an ablation where TARF must identify the target concept without knowing the class count (using only a quantile threshold).
- Add a brief discussion of Phase I's computational overhead for practitioners.

## Removed Points
These points are flagged to be removed, treat them with caution:
- "Table 2 shows TARF appearing twice" — Likely a PDF parser alignment artifact in the extracted text; the original formatting may differ.
- "The claim about real-world requests lacking concrete examples" — Minor motivational concern; the taxonomy itself is the contribution.
- "Phase II description confusion about τ=0" — The paper's description is coherent; data with τ=0 are excluded from gradient descent, a standard design choice.
- "Model structure ablation limited analysis" — The paper notes the capacity effect observation; deeper analysis is a nice-to-have.
- "Runtime comparison missing Phase I overhead" — Partially addressed by the ablation appendix reference.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Verify and correct the SCRUB Gap values for model mismatch in Table 3.
2. Clarify whether TARF's main results use the known count of target-concept classes or a quantile heuristic for β, and include an ablation without the count prior.
3. Add per-metric absolute difference components (|ΔUA|, |ΔRA|, |ΔTA|, |ΔMIA|) alongside the aggregate Gap to improve interpretability.
4. Add quantitative metrics (e.g., CLIP-score change) for the stable diffusion case study and clarify the duplicated values in the TOFU table.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>