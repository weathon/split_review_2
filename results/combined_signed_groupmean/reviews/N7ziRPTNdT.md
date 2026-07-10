Now I have a solid calibration basis. Let me finalize the review.

## Summary of Calibration

**Round 1 bracket:** 5.5–7.5, based on the closest related papers (compositional generalization, identifiability theory).

**Closest anchor:** `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7VPTUWkiDQ.md` (Brady et al. 2025, avg=7.33, Accept) — the paper this work builds on directly. 
- Shared high-magnitude items: theoretical guarantees for compositional generalization, identifiability framing. 
- Key difference: the current paper's novel theoretical result (encoder vs decoder asymmetry) and more realistic PUG experiments are genuine advances; however, the lack of error bars (impact=-9.86) is a significant empirical weakness that the anchor doesn't share. 
- The anchor's experiments used only simple synthetic data (-6.70); the current paper fixes that but introduces a different rigor gap.
- **Net effect:** the paper is slightly below the anchor (7.33) due to methodological gaps in experimental reporting, placing it at **7.0**.

**Other anchors in the band:**
- s1zO0YBEF8 (6.50, Accept): Has fundamental "not truly OOD" issues (impact=-10.00) — the current paper is much sounder.
- H98CVcX1eh (6.50, Accept): Poor clarity, no related work section — current paper is better.
- hKMPz3wkPV (6.75, Reject): Fundamental conceptual issues with the proposed definition — current paper doesn't suffer from this.
- QwrnH32tJV (5.67, Reject): Poor presentation, unclear problem — current paper is much clearer.

---

## Summary

This paper investigates whether generative (decoder-based) or non-generative (encoder-based) methods can achieve compositional generalization for visual perception. Theoretically, it shows that the constraints required to *guarantee* compositional generalization can be enforced on decoders (coordinate-aligned, data-independent) but not on encoders (manifold-dependent, requiring knowledge of unobserved OOD regions). Empirically, it evaluates both approaches on photorealistic PUG datasets, finding that non-generative methods often fail or require large-scale pretraining, while generative methods with search and replay significantly improve OOD performance. The paper is well-motivated, the theoretical contribution is genuine, and the experiments use an appropriate controlled setup.

## Strengths

- **Novel theoretical insight about encoder/decoder asymmetry (Theorem 3.2, Section 3).** The paper proves that when d_x ≥ d_z³, the derivatives of inverse generators in G_int can be arbitrary, so the constraint on encoders is manifold-dependent (Eq. 3.4) while the constraint on decoders is coordinate-aligned (Eq. 3.1). This is a non-trivial result that cleanly explains why explicit constraints are feasible for decoders but not encoders — a genuinely new theoretical contribution beyond Brady et al. (2025).

- **Clear formal framework (Section 2).** The paper formalizes perception as an inverse problem, defines generative vs. non-generative approaches through whether a decoder or encoder must identify the ground-truth generator/inverse (Eqs. 2.2–2.3), and connects this to OOD identifiability (Eqs. 2.5–2.6). The setup is principled and builds usefully on prior work.

- **Well-designed empirical evaluation (Section 5).** The use of PUG datasets with three controlled splits (Background, Texture, Object) that vary concept interaction degree is appropriate. The breadth of base encoders (DINOv1, DINOv2, CLIP, SigLIP2, I-JEPA, from-scratch ViT) provides useful comparison across pretraining scale. The results showing generative methods substantially improve OOD performance are consistent with the theory.

## Weaknesses

### Fatal
None.

### Major

- **No error bars, confidence intervals, or variance reporting (Fig 5, Fig 6).** All experimental results appear to be single-run with no measure of variability. Given the paper's strong comparative claims between generative and non-generative methods, the absence of statistical rigor makes it difficult to assess whether observed differences are meaningful or arise from noise. This is a significant methodological gap for an empirical paper making comparative claims, and it limits the strength of the evidence supporting the central narrative. The paper should report results across multiple seeds or at minimum provide error bars.

### Minor

- **Title overstates the findings.** "Generation is Required for Data-Efficient Perception" is more categorical than what the paper actually shows. The paper's own analysis notes that "whether compositional generalization occurs depends on whether the optimization process happens to avoid converging to such a solution" (line 143), and the experiments demonstrate that non-generative methods *can* succeed: all methods achieve near-perfect OOD accuracy on PUG-Object (n=0 case), and SigLIP2 reaches ~80% on PUG-Background. The paper honestly handles these nuances in the text, but the title implies a universality that doesn't match the evidence. A title like "Generation Enables Guaranteed Compositional Generalization" would better capture the actual contribution.

- **"Best-performing combination" selection could overstate results (line 213).** The paper reports OOD accuracy "obtained with the best-performing combination of slot encoder and fine-tuning choice" per base encoder. Since selection is over the very metric being reported, this introduces optimism bias. This actually works *against* the paper's main argument (non-generative methods are evaluated at their best and still underperform), so it doesn't weaken the paper's thesis, but it should be disclosed transparently.

- **The d_x ≥ d_z³ condition in Theorem 3.2 is presented without justification.** Readers are told this bound matters for the result but not whether it is tight or a technical artifact. The paper references Lemma A.4 (in the stripped appendix) suggesting the result generalizes, but the main text should at minimum discuss this condition.

### Trivial
- The scalability/iteration cost of gradient-based search is not discussed, though it requires per-image optimization at test time.

## Nice-to-Haves
- **Directly measure the hypothesized mechanism.** The theory predicts that failed encoders violate the G_int manifold constraint (Eq. 3.4) on OOD data while successful ones (SigLIP2) implicitly satisfy it. Directly measuring this would strengthen the causal link between the theoretical impossibility result and empirical failures.
- **Control experiments for the n=0 case.** An ablation that makes concepts interact (e.g., occlusions) while keeping architecture fixed would more directly test whether G_int complexity is the causal factor.
- **Provide multiple runs / variance** as discussed above.

## Removed Points
These points from the input review were removed after cross-checking against the paper:

1. **"The theoretical result applies to the inverse of F_int, not to all possible encoders" / "impossibility of explicit constraints doesn't imply impossibility of learning."** The paper already explicitly addresses this at line 143: "whether compositional generalization occurs depends on whether the optimization process happens to avoid converging to such a solution." The paper does not claim that learning is impossible — it claims that *guaranteeing* through explicit constraints is infeasible, which is a different claim. This criticism is already addressed by the paper's own text.

2. **"Asymmetric comparison in experiments."** The critic noted that generative methods use a decoder designed for F_int while non-generative methods use standard encoders. This is the paper's central thesis — the whole point is that constraints are straightforward for decoders and infeasible for encoders. The critic acknowledges "this confound is partly inherent — the paper's argument is precisely that such constraints are straightforward for decoders and infeasible for encoders. So one cannot control for it." This is not a valid weakness against the paper's claims; it is the paper demonstrating its claimed result.

3. **"PUG-Object result cuts against the central narrative."** The paper explicitly discusses the n=0 case as a special case where G_int is more structured (lines 127, 215) and predicts that this structure makes compositional generalization easier. The experiments confirm this prediction. This is supporting evidence for the theory, not counter-evidence.

4. **Section notes about search/replay not being novel.** The paper does not claim novelty for these techniques; they are existing methods re-purposed within the framework. Not a weakness.

5. **Section note about abstract line 8 wording.** The paper describes practical impossibility (manifold-dependent constraints), which is accurate per its theoretical analysis.

6. **Section note about the F_int assumption being strong.** The paper explicitly acknowledges this limitation in Section 7 and Appendix D.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add error bars / confidence intervals from multiple seeds to all experimental figures.
2. Calibrate the title to better match the nuanced findings, e.g., "Generation Enables Guaranteed Compositional Generalization."
3. Report results across all slot encoder/fine-tuning configurations or clarify the selection procedure's impact.
4. Discuss whether the d_x ≥ d_z³ bound is tight or merely a technical artifact.
5. Include iteration counts or wall-clock time for the gradient-based search procedure.

---

## Score and Decision

**Calibration summary:**
All anchor papers retrieved across rounds:

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7VPTUWkiDQ.md | 7.33 | R1 | Yes | Direct predecessor (Brady et al. 2025). Current paper has novel encoder/decoder asymmetry result and more realistic experiments but lacks error bars. Slightly below this anchor. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/s1zO0YBEF8.md | 6.50 | R1 | Yes | Has fundamental "not truly OOD" flaw. Current paper is sounder. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/H98CVcX1eh.md | 6.50 | R1 | Yes | Poor clarity, missing related work. Current paper is clearer. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/hKMPz3wkPV.md | 6.75 | R1 | Yes | Conceptual issues with definition. Current paper is more rigorous. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/QwrnH32tJV.md | 5.67 | R2 | Yes | Poor presentation. Current paper is much clearer. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7QGyDi9VsO.md | 5.00 | R1 | No | Distributed vs slotted representations. Less relevant. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0BBzwpLVpm.md | 4.25 | R1 | No | Concept learning for generation. Less relevant. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7oT1X8xjIk.md | 5.80 | R1 | No | Identifiability with noise. Tangential. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/UVSKuh9eK5.md | 5.67 | R1 | No | CLIP compositional generalization. Tangential. |

**Round-1 bracket:** 5.5–7.5.  
**Narrowing:** The closest anchor (Brady et al., 7.33) shares the identifiability framing and theoretical approach but the current paper contributes a genuinely new result about encoder/decoder asymmetry and uses more realistic data. However, the absence of error bars (impact=-9.86) is a meaningful methodological gap that the anchor doesn't share. Comparing itemized scores: the current paper's strongest strengths (Theorem 3.2 at +9.99, experiments at +9.61) are competitive with the anchor's (+9.80 for theory, +6.84 for guarantees), but the anchor's strongest weakness (-6.70 for synthetic-only experiments) is less severe than the current paper's strongest weakness (-9.86 for no error bars). Placing this paper below the anchor (7.33) and above the other compositional generalization papers (6.50) yields 7.0.

**Final score: 7.0 — Accept.** The theoretical contribution is genuine and well-executed, the experimental design is appropriate (despite the error bars gap), and the paper is clearly written. The error bars issue is the most significant concern and should be addressed in revision, but it does not invalidate the paper's core claims.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>