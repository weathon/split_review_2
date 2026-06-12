## Summary
HighClass is a metagenomic classification framework that replaces alignment with hash-based token mapping, using variable-length tokens from the existing QA-Token vocabulary and gradient-based sparsification. The paper claims state-of-the-art efficiency (4.2× speedup, 68% memory reduction) on CAMI II with 85.1% F1, and provides theoretical guarantees including generalization bounds, concentration under α-mixing, and classification consistency.

## Strengths
- **Solid empirical results**: HighClass achieves near-parity F1 (85.1%) with MetaTrinity (86.6%) while delivering substantial speedup and memory reduction. The ablation study convincingly decomposes contributions from variable-length tokens, quality weighting, and sparsification.
- **Principled architectural choice**: Replacing online alignment with pre-computed token-to-taxon hash lookups is a clean design that avoids position-dependent operations, and the theoretical complexity reduction from O(m log n + k log k) to O(|T|) is clearly motivated.
- **Comprehensive experimental setup**: Ten independent runs, bootstrap confidence intervals, Wilcoxon tests with Holm–Bonferroni correction, and Cohen’s d effect sizes are used, demonstrating rigor beyond typical ML benchmarks.

## Weaknesses
### Major
- **Limited algorithmic novelty**: The core innovations—variable-length tokenization, quality-aware scoring, and gradient-based sparsification—are taken **as is** from existing prior works (QA-Token, MetaTrinity, and Alser et al. 2024). HighClass’s design is an integration of these components rather than a new learning method. The paper does not introduce a new training procedure, representation, or optimization beyond the combination. For ICLR, a top ML venue, the incremental integration without a novel algorithmic contribution weakens the case for acceptance.
- **Theoretical claims are loosely coupled to the actual method**: The generalization bound (Theorem 6) and mixing analysis (Lemma 7) are presented at a high level, but their connection to the specific classifier (quality-weighted log-likelihood over token indicators) is not made explicit in the main text. The mixing analysis treats token dependencies within a read, yet the classifier averages over tokens; standard concentration arguments (e.g., via bounded differences or simple blocking) would suffice, and the reported variance inflation factor of 31.7 risks undermining rather than supporting the claim of tight concentration. The absence of concrete numerical values or simulated validation for the theoretical constants (e.g., C=2.3, γ=0.15) weakens confidence.
- **Unclear handling of pre-trained components**: The paper relies on pre-trained QA-Token vocabularies and gradient-based sparsification masks. It does not specify whether these were trained on the same benchmark data or separate data, nor does it discuss potential data leakage. Without clarity on how these components relate to the evaluation, the reported results may conflate generalization of the trained tokenizer with the efficacy of the HighClass indexing framework.
- **Inconsistent presentation of baselines**: Table 4 introduces “Metalign” without definition or citation, making the scalability comparison uninterpretable. This error suggests lack of careful copyediting and undermines trust in the comparison’s validity.

### Minor
- The paper claims “first rigorous theoretical framework for token-based genomic classification” but does not cite or refute existing theoretical analyses of k-mer classification (e.g., statistical properties of LSH for k-mers, concentration bounds for k-mer profiles). Overclaiming without positioning against prior theory is a weakness.
- The quality sensitivity η=1.8 is stated as “learned,” but the learning procedure (was it from the QA-Token PPO training? Or a separate calibration?) is not described, leaving the reproducibility of this hyperparameter unclear.

## Nice-to-Haves
- Show analytically or via simulation that the mixing rate γ ≈ 0.15 actually holds for the token dependency graph under typical read lengths, rather than simply citing an empirical value.
- Add a baseline that uses the same token vocabulary but with a simple unweighted majority vote to isolate the effect of quality-aware scoring more cleanly.

## Novel Insights
None beyond the paper’s own contributions. The integration of QA-Token, MetaTrinity-style indexing, and sparsification is the main idea; no unexpected principle emerges.

## Suggestions
- Clearly delineate which components are new contributions versus adopted from prior work, and justify why the integration itself constitutes a publishable advance for a machine learning audience.
- Provide explicit, self-contained statements of the theoretical results (even in the main text) that connect the constants to the method’s hyperparameters, and if possible, validate the mixing model on genomic data.
- Remove or properly introduce “Metalign” in Table 4, or replace with a known baseline.
- Include a discussion of the statistical significance of the 1.5% F1 gap relative to MetaTrinity—the overlap in confidence intervals and the reported p=0.032 suggest the gap is real but small; clarify whether near-parity is empirically claimed.

## Score and Decision
**Score**: 4  
**Decision**: Reject

MY FINAL SCORE: <score>4</score>  
MY FINAL DECISION: <decision>Reject</decision>