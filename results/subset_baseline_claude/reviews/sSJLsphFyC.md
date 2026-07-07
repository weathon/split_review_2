## Summary

This paper proposes MVU-DM (Maximum Variance Unfolding on Disjoint Manifolds), an extension of Maximum Variance Unfolding (MVU) to datasets whose neighborhood graphs are disconnected. The method runs MVU separately on each connected component, selects a small set of "representative points" per component, applies a global MVU step on those representative points to determine inter-component placement, and uses affine transformations to translate all remaining points into the global embedding. The authors claim improvements in embedding quality, computational speed, and memory usage over vanilla MVU.

---

## Strengths

- **Addresses a genuine limitation of MVU.** Disconnected neighborhood graphs cause MVU to become unbounded; the proposed method handles this in a principled way without requiring additional hyperparameters, which is a concrete practical advantage over naive workarounds (e.g., forced graph connectivity).

- **Computational benefits are real and quantified.** The decomposition into independent per-component MVU problems enables parallelism and reduces problem size. Table 4 shows speedups of up to ~16× on several datasets, and the $O((kN)^3)$ complexity argument makes the benefit analytically transparent.

- **Empirical coverage is reasonable.** Experiments span four artificial and four natural datasets, using three complementary metrics (1-NN error, trustworthiness, continuity) and include eight competing methods. MVU-DM generally matches or exceeds vanilla MVU and is competitive with the broader field.

---

## Weaknesses

### Fatal
None.

### Major

1. **The affine transformation step lacks theoretical justification.** The core claim is that an affine transformation applied to each component's locally-computed embedding correctly places it in the global space. However, there is no analysis of when this is valid. MVU embeddings are rotation/reflection invariant but the affine map (step 6) may distort the local isometry that MVU is specifically designed to guarantee. The paper asserts that "it is guaranteed that…there is no loss of information" without proof, and this is the most critical step of the algorithm.

2. **Inconsistent and sometimes negative speedups.** Table 4 reports speedup < 1 for Olivetti at $k=5$ (0.55×), meaning MVU-DM is slower. No explanation is provided. Given that computational efficiency is a core selling point, the regime in which the method is actually faster needs to be characterized, not just reported selectively.

3. **The paper is visibly incomplete.** The text in Section 3 contains the string "We provide a notation (glossary? variable index?) table in **Appendix TODO**," indicating a draft artifact that should have been resolved before submission. More substantively, the paper states it "experiments with two methods for representative point selection" (Section 3.1) but only one method (extrema along principal directions) is described anywhere in the readable portion of the paper. The second method is never presented, making the claim incomparable.

4. **Performance regression on Four Moons (FM).** MVU-DM achieves 2.65% 1-NN error on FM while vanilla MVU achieves 0.00%, and trustworthiness/continuity are lower (97.62% vs 98.64% and 99.21% vs 99.45%). This is the most geometrically structured artificial dataset—nested C-shaped manifolds—and the method that claims to handle disjoint manifolds regresses precisely here. The paper does not analyze why.

### Minor

- The selection of $|\mathcal{Z}_p| = 2d_p$ representative points is presented as a design choice but never ablated. Whether 1×, 3×, or 5× $d_p$ would give meaningfully different results is unknown.

- The exclusion of t-SNE is reasonable, but UMAP—which has largely supplanted both t-SNE and older spectral methods in practice and handles disconnected graphs—is absent without comment.

### Trivial

- Minor: the speedup table (Table 4) would be more interpretable with absolute runtimes alongside ratios.

---

## Nice-to-Haves

- An ablation varying the number of representative points and comparing both selection strategies would support the design choices made.
- A theoretical result, even an informal bound, on how the affine translation step affects local isometry would substantially strengthen the paper's core claim.
- Analysis of the regime (dataset size, number of components, $k$) in which speedup is reliably obtained would make the computational claim more actionable.

---

## Novel Insights

The observation that MVU's local isometry guarantee, combined with variance-maximized "unfolding," makes each component's embedding a good approximation of its convex hull—and that this property enables a meaningful choice of representative points—is a genuinely useful insight. However, it is not fully exploited: the paper does not provide a rigorous treatment of how well a $2d_p$-point representative set captures the component geometry, nor does it derive conditions under which the affine stitching preserves MVU's isometry in the global embedding.

---

## Suggestions

- Provide at minimum a lemma or informal argument for why the affine transformation in step 6 does not violate local isometry guarantees, or explicitly acknowledge its approximate nature and quantify the distortion.
- Report absolute runtimes in Table 4 alongside ratios, and discuss the Olivetti $k=5$ case where MVU-DM is slower.
- Present and evaluate the second representative-point selection method that is mentioned but absent.
- Analyze the FM regression explicitly—it is the most informative failure mode in the experiments.

---

## Score and Decision

MVU-DM addresses a real limitation of a well-studied method and delivers measurable empirical benefits. However, the paper has a critical gap in theoretical justification for its central stitching step, presents an inconsistency in its efficiency claims, regresses on the most pertinent artificial dataset without explanation, and is visibly unfinished in key sections. These are not minor presentation issues; they concern the validity and completeness of the core contribution. The contribution is incremental by design and would need the theoretical gap resolved to be convincing at a top venue.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>