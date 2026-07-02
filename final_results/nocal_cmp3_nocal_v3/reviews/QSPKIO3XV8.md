Here is the final consolidated review:

---

## Summary

This paper proposes Dimension Domain Co-Decomposition (3D), a PINNs-based framework combining dimension decomposition (via a shared MLP with indexed inputs) with a Mixture-of-Experts (MoE) based domain decomposition. The paper also introduces Variable Interpretability (VI), a metric that quantifies alignment between learned per-dimension components and ground-truth factors. Experiments on Poisson, Wave, Burgers, and Transport equations demonstrate parameter efficiency, interpretability, and adaptive domain partitioning.

## Strengths

1. **Parameter-efficient shared-MLP architecture.** Encoding coordinate values together with a dimension index and feeding all dimensions through a single shared MLP decouples parameter count from input dimensionality. Table 1 verifies this: the shared MLP has 5,392 parameters regardless of whether the PDE is 5d or 10d, while independent MLPs grow from 26,640 to 53,280. This is a clean architectural improvement over per-axis network designs used in prior work.

2. **Principled VI metric for subspace alignment.** The VI metric (Section 3.2) uses QR decomposition and principal angles to quantify how well the subspace spanned by learned dimension components captures the subspace of ground-truth factors. It is scale-invariant, mathematically sound, and fills a real gap in the quantitative evaluation of interpretability for separable PDE solvers.

3. **Clean demonstration that learned MoE partitions align with physical features.** Figure 4 for Burgers shows that with K=2, the router assigns one expert primarily to each side of the shock at x≈0. For the Transport equation (Figure 5), the experts consistently learn diagonal stripe structures. Reproducibility across random seeds (Section 4.3) supports that the decomposition is driven by PDE structure, not initialization.

## Weaknesses

### Major

1. **No experimental comparison against SPINNs, the most directly relevant dimension-decomposition baseline.** The paper explicitly positions itself relative to SPINNs (Cho et al., 2023), stating that the proposed architecture "differs in several key aspects that bring advantages" (line 80) — yet SPINNs is never compared against in any experiment. The evaluation compares against "vanilla PINNs" (a generic 10-layer MLP) and "independent MLPs" (a per-axis baseline the paper constructs). While independent MLPs capture the per-axis network design, the paper claims specific advantages over SPINNs (e.g., memory efficiency for high-dimensional problems, natural MoE compatibility) that cannot be assessed without direct comparison. This gap weakens the central claim that the shared-MLP innovation improves upon the existing separable approach.

2. **The full "co-decomposition" (dimension + domain decomposition working together) is only demonstrated on 2D problems, undercutting the high-dimensional framing.** The title, abstract, and introduction repeatedly frame the contribution around solving "high-dimensional PDEs." The dimension decomposition component is tested on 5d and 10d Poisson — but without MoE. The MoE-driven domain decomposition is only tested on the viscous Burgers equation (1 spatial + 1 time) and linear transport equation (1 spatial + 1 time). The full 3D framework combining both decomposition strategies is therefore never demonstrated at high dimensionality. The high-dimensional claim rests on the dimension decomposition alone, while the "automatic domain decomposition" claim rests only on 2D problems. This creates a disconnect between the paper's framing and the experimental evidence.

### Minor

3. **The VI metric is only demonstrated on problems with exactly separable closed-form solutions.** The paper acknowledges this limitation in the conclusion and suggests a Fourier-series approximation for non-separable cases, but this workaround is neither implemented nor evaluated. All four benchmarks are tested only in settings where exact factorizations are known analytically. This substantially narrows the demonstrated scope of VI to separable PDEs, while its usefulness for the broader class of physically interesting non-separable PDEs is unvalidated.

4. **The related work characterization of APINNs may overstate the distinction.** The paper notes that APINNs uses "soft gating mechanisms" (line 46) yet simultaneously claims that "all existing approaches require predefined partitions." If APINNs' soft gating is functionally similar to the MoE router (adaptively assigning weights), then the novelty of the MoE component relative to this prior work is less clear than the paper suggests. A more careful differentiation is warranted.

5. **Figure 2's presentation is potentially misleading.** The text fairly reports each method's error at its own termination (shared MLP: 1.8×10⁻⁴ at 11,400 steps; PINNs: 7.5×10⁻³ at 23,400 steps). However, the figure truncates at 11,400 steps where PINNs has not converged, while the caption labels the PINNs error as "final." The advantage is real, but the presentation obscures the fact that the methods converge at different rates.

6. **No variance reported for key accuracy numbers.** The 5d Poisson error of 1.843×10⁻⁴ (shared MLP) is reported without variance, even though VI is averaged over 5 seeds. The 10d Poisson error of 1.25×10⁻³ similarly lacks variance.

7. **The claim that "dense MoE avoids expert collapse and provides more stable training" (line 104) is asserted without evidence or citation.** This is a consequential design choice that should be justified.

8. **No inference-time cost analysis.** The paper reports training parameter counts but does not discuss inference cost, relevant for practical surrogate modeling use.

### Trivial

- The dimension expansion claim (line 141) is mentioned in a single sentence and entirely deferred to the appendix, leaving the reader without supporting evidence in the main text.

## Nice-to-Haves

- Add SPINNs as a baseline for the dimension decomposition experiments (Poisson and Wave).
- Add at least one domain decomposition baseline (XPINNs or APINNs) for the Burgers/Transport experiments.
- Demonstrate the full 3D framework on at least one higher-dimensional problem with MoE (e.g., K=2 or K=3 on a 5d problem).
- Implement and validate the Fourier-series approximation for VI on one non-separable PDE.
- Provide a breakdown of router vs. expert vs. dimension-decomposition parameters within each MoE configuration.
- Compare dense vs. sparse MoE to justify the design choice.

## Removed Points

These points from the input review were removed with justifications:

- **"Unfair truncation inflates PINNs disadvantage":** Removed — the text actually compares each method at its own termination (converged) state, which is fair. The shared MLP terminates at 11,400 (error 1.8×10⁻⁴), PINNs at 23,400 (error 7.5×10⁻³). The advantage is real and holds at convergence. A weakened version about figure presentation clarity is kept as Minor #5.
- **"SPINNs forward-mode AD argument incomplete":** Removed — this is a parser artifact (sentence truncated by PDF extraction), not an author error.
- **"Why higher r is needed for higher-dimensional separable problems":** Removed — this is a curiosity, not a weakness; the paper correctly reports the empirical finding without claiming to explain it theoretically.
- **"Missing related works":** Removed per policy — cannot verify existence of missing citations without external sources.
- **"Missing appendix content / proofs":** Removed per policy — appendices are stripped by the parser.
- **"Generic weaknesses about evaluation lacking rigor":** Removed — lacked concrete anchors to specific claims in the paper.

## Novel Insights

None beyond the paper's own contributions. The review surfaces the expected gaps (missing baseline comparisons, limited scope of the full framework demonstration) but does not reveal unexpected findings beyond what the paper itself presents.

## Suggestions

1. Compare against SPINNs for the dimension decomposition benchmarks. This is the most critical missing experiment.
2. Demonstrate the full 3D framework (dimension decomposition + MoE) on at least one higher-dimensional PDE, even with modest K.
3. Implement the Fourier-series approximation for VI on one non-separable PDE to validate the proposed path to generalization.
4. Report accuracy numbers with variance over multiple random seeds, consistent with the reporting standard used for VI.
5. Clarify the distinction between the proposed MoE approach and APINNs' soft gating, either by adding a direct comparison or by more carefully qualifying the related work claims.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>