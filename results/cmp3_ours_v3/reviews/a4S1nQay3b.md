Now I'll compose the final review with all the filtering applied.

## Summary

This paper proposes CorreGen, a generative framework for multi-view clustering under noisy correspondence (NC). It identifies two types of NC — category-level mismatch (same-class pairs treated as negatives) and sample-level mismatch (misaligned or corrupted pairs) — and formulates correspondence learning as maximum likelihood estimation solved via EM. The E-step uses optimal transport with GMM-informed marginals and a virtual sample to infer soft correspondences; the M-step updates the encoder to maximize expected log-likelihood. Experiments on four datasets show consistent improvements over seven baselines.

## Strengths

1. **Clear problem decomposition (Section 3.1, Definitions 1 & 2).** Distinguishing category-level from sample-level mismatch gives the paper a crisp conceptual foundation. Prior MVC work on NC treats misalignment as a single phenomenon; this decomposition provides a vocabulary for discussing what different methods do and do not address, and it directly motivates the method design (GMM marginals for class-level structure, virtual sample for outliers).

2. **Novel EM formulation with OT-based E-step (Section 3.2).** Framing NC in MVC as maximum likelihood estimation over latent correspondences (rather than as robustified contrastive learning) is a genuinely different starting point. The E-step combination of GMM-guided marginals (cluster-adaptive alignment capacity) with optimal transport augmented by a virtual sample (to absorb unalignable outliers) is technically inventive and directly responsive to the two NC types identified.

3. **Consistent and often large empirical gains (Tables 1–2).** CorreGen outperforms all seven baselines across nearly every setting. The advantage is especially clear on UMPC-Food101 (the most realistic noisy dataset), where the gap over the next-best method reaches 10–15 percentage points and remains large even at 80% mismatch ratio. These results are not cherry-picked — the method wins on 3 of 4 datasets at every noise level.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

1. **Category-level mismatch, a claimed key differentiator, is not quantitatively evaluated.** The paper's contributions begin with identifying and formalizing category-level mismatch, and the method is repeatedly motivated by its ability to handle it. Yet the main experiments (Tables 1–2) only evaluate sample-level mismatch (controlled by MR and CR). The paper acknowledges this (lines 226–227): *"Since MVC is an unsupervised task, category-level correspondences depend on the underlying class sizes and distributions, making category-level mismatch an intrinsic challenge rather than one that can be explicitly specified."* The only evidence offered is a qualitative posterior visualization (Figure 3). The paper's headline results do not measure the phenomenon the method is designed to address, and the qualitative figure does not isolate whether the improvement comes from handling category-level mismatch, sample-level mismatch, or both. Constructing a controlled experiment (e.g., deliberately treating cross-view same-class pairs as negatives and measuring recovery) would directly test the claimed advantage.

2. **No standard deviations or variance estimates reported.** Table 1 states *"All the results are the mean of five individual runs with different random seeds,"* but no standard deviations, confidence intervals, or any measure of dispersion are provided anywhere. With 5 runs, several comparisons are close enough that variance could matter (e.g., Caltech101 at MR=0%: Ours ACC=68.52 vs CANDY=67.64, gap 0.88; Scene15 at MR=0%: Ours NMI=48.92 vs ROLL=48.71, gap 0.21). Without variance, the reader cannot assess whether the gaps are meaningful.

3. **Limited NC-specific baselines.** The paper compares against seven MVC methods; only ROLL (Sun et al., 2025) is explicitly an NC-handling method. The related work (lines 66–68) describes reweighting-based (Huang et al., 2021; Yang et al., 2024) and realignment-based (Lin et al., 2024) NC solutions, but none appear as baselines. While these methods originate from different domains (cross-modal retrieval, video reasoning) and may not be straightforwardly adaptable to MVC, their absence weakens the comparison against the NC-specific state of the art.

4. **The GMM marginal formula (Eq. 13–14) is heuristic.** The marginal probability 
   $p(\mathbf{x}_i^{(v)}; \theta^{(t)}) = \frac{m^{d_i} - 1}{m - 1} \cdot \frac{N_c}{N}$ depends on two free hyperparameters ($\epsilon$, $m$) and uses a curve-shaping function not derived from any statistical principle. The intuition (confident cluster members get higher mass) is sensible, but the paper provides no sensitivity analysis for $\epsilon$ or $m$ in the main text, nor does it justify this particular functional form over simpler alternatives (e.g., using GMM posterior responsibility directly). This weakens the claim that the E-step is "principled."

### Trivial

1. **"Generative" framing nuance.** The joint distribution $p(\mathbf{x}_i^{(v_1)}, \mathbf{x}_j^{(v_2)}; \theta)$ in Eq. (17) is parameterized as a normalized similarity score (softmax over pairwise similarities), not as an actual generative process. Calling it "generative" is defensible as maximum likelihood over latent correspondences, but readers should be aware this differs from classic generative models (VAEs, diffusion models).

2. **Minor overstatement in the abstract.** The abstract claims evaluation on "synthetic and real-world noisy datasets," but the experiments evaluate only real-world datasets with synthetic noise injection (controlled MR/CR). There is no evaluation on a purely synthetic dataset with known ground-truth correspondence structure.

## Nice-to-Haves

- **Sensitivity analysis for $\epsilon$ and $m$** (Eq. 13–14) in the main text would clarify how robust the method is to these hyperparameter choices. Appendix E is referenced but stripped by the parser.
- **Ablation isolating the virtual sample mechanism's contribution** (OT with vs. without virtual sample) would be informative.
- **Runtime/scaling discussion** would be helpful — the OT-based E-step involves Sinkhorn iterations on an $(N+1) \times (N+1)$ matrix each iteration.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **"Proposition 2 is trivial"** (from Harsh Critic). The proposition shows InfoNCE as a special case under stated assumptions (uniform marginals, degenerate posteriors). This is a clean theoretical connection and standard practice; the assumptions are clearly stated. Removing the CorreGen-specific machinery naturally recovers a simpler baseline — this is informative, not trivial.

2. **"Generative model is actually discriminative"** (overstated version). The formulation is framed as maximum likelihood over latent correspondences, and the softmax parameterization is standard in energy-based and self-supervised learning. The criticism is technically correct but applies to most modern "generative" formulations in representation learning and is not unique to this paper.

3. **"Improvement over DIVIDE is ablation-by-addition"**. The paper transparently states it builds on DIVIDE (lines 222). The improvement over DIVIDE is the cleanest measure of CorreGen's added value. This is standard practice, not a weakness.

4. **"Missing appendix content, abalation, proofs"**. The parser strips appendix content. These exist in the original submission.

5. **Demands for the paper to address problems outside its stated scope** (larger datasets, more views, different modalities). The paper evaluates on four standard benchmarks with a reasonable set of baselines and noise levels.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Report standard deviations** for all metrics in Tables 1–2. This is the single highest-leverage improvement for credibility.
2. **Add a controlled category-level mismatch experiment.** For example: take a clean dataset, deliberately mark some cross-view same-class pairs as negatives in the contrastive objective for baselines, and measure whether CorreGen recovers them (high posterior probability) and whether clustering accuracy is more robust. This would directly test the claimed advantage.
3. **Include at least one NC-specific MVC baseline** beyond ROLL (e.g., adapt a reweighting method like Huang et al. (2021) to MVC, or explain why adaptation is infeasible).
4. **Add a sensitivity analysis** for $\epsilon$ and $m$ (or include the appendix results in the main text).
5. **Tone down the "generative" framing** or clarify that the joint distribution in Eq. 17 is a normalized similarity score, to avoid potential confusion.

## Score and Decision

**Round 1 bracket:** After retrieval, the most similar accepted papers in the calibration corpus ranged from ~6.2 (MVP: incomplete MVC with VAEs, avg 6.25) to ~7.25 (COPER: permutation-based MVC, avg 7.25) to ~8.0 (Norton: OT for noisy correspondence in video-language). The CorreGen paper sits below Norton (which has more polished evaluation) and comparably to COPER and MVP.

**Narrowing:** Compared to MVP (6.25), CorreGen has a more novel formulation (EM vs. cyclic permutations on VAEs) but weaker variance reporting. Compared to COPER (7.25), CorreGen has stronger novelty but a larger evaluation gap (category-level mismatch not isolated). Compared to Norton (8.0), CorreGen has a more significant unaddressed weakness (the missing evaluation of its central claim).

**Anchors used:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/s4MwstmB8o.md` — MVP, avg 6.25 (Round 2). Incomplete MVC with VAE permutations. Similar-tier paper with comparable novelty and experimental depth, but CorreGen has a larger evaluation gap.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5ZEbpBYGwH.md` — COPER, avg 7.25 (Rounds 1&2). MVC with permutation-based CCA. Stronger on dataset coverage, but CorreGen has more novel problem formulation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9Cu8MRmhq2.md` — Norton, avg 8.0 (Round 1). OT for noisy correspondence in video-language. More polished evaluation, fewer evidential gaps.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/SNNdmfqWFu.md` — SpecRaGE, avg 3.4 (Rounds 1&2). Rejected MVC paper. CorreGen has substantially stronger novelty and results.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/AXC9KydyZq.md` — M3C, avg 7.0 (Round 2). Graph matching and clustering. Similar score tier but different subfield.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>