Here is my final consolidated review.

## Summary

This paper introduces LoLoRA, a method that replaces gradient-based training of the LoRA adapter matrix A with local unsupervised updates (HPCA or autoencoder) during the forward pass, thereby avoiding activation storage for A's backward pass. The paper also provides a theoretical characterization (Theorem 4.4) proving that under a random-regression assumption, optimal A matrices for frozen-A LoRA are nonsingular linear transformations of the top-r eigenvectors of the input covariance matrix — connecting to and theoretically grounding the empirical EVA initialization.

## Strengths

- **Clean theoretical characterization of optimal A initialization (Theorem 4.4, Section 4).** Under the random-regression assumption (ΔW₀ with i.i.d. Gaussian entries), Theorem 4.4 proves that optimal A matrices for frozen-A LoRA are exactly the nonsingular linear transformations of the top-r eigenvectors of the input covariance matrix. This provides a theoretical explanation for why the empirical EVA initialization (Paischer et al., 2024) works — directly addressing a gap that prior work on EVA was criticized for lacking. Theorem 4.5's finding that no analogous optimal initialization exists for B also formalizes the asymmetry observed empirically in prior work. [scorer impact: +10.00]

- **Thorough ablation study (Tables 5, 6, Section 5.4).** The paper systematically compares four initialization methods for LoRA-FA (uniform, orthogonal, PiSSA, EVA) and five local update rules for LoLoRA (HPCA variants, AE, SoftHebb) across three ranks. The finding that EVA initialization dominates all other initializations for frozen-A settings, and that HPCA, AE, and HPCA (svd first) perform similarly, provides useful empirical grounding for practitioners. [scorer impact: +7.64]

## Weaknesses

### Fatal

None.

### Major

- **The central empirical claim is not supported by the data.** The Conclusion (line 332) states "HPCA consistently outperforms standard LoRA-FA in two out of three experimental setups." This is misleading:
  - **GLUE (Tables 1-2):** LoLoRA HPCA is worse than or tied with LoRA-FA (uniform) on 7 of 8 tasks (e.g., CoLA: 66.3 vs 67.9, RTE: 84.6 vs 86.4, MNLI: 90.3 vs 90.6).
  - **Math reasoning (Table 3):** LoLoRA (0.829±0.004) and LoRA-FA (EVA) (0.829±0.005) are statistically indistinguishable; the edge over LoRA-FA (uniform) (0.826±0.005) is within error bars.
  - **Multimodal (Table 4):** LoLoRA (2.93) is better than LoRA-FA (uniform) (2.97) but *worse* than both LoRA-FA (EVA) (2.92) and standard LoRA (EVA) (2.89).
  The honest reading is that **LoLoRA roughly matches LoRA-FA (EVA) across all settings** — a finding worth reporting, but the current claim overstates it significantly. This overclaiming undermines trust in the rest of the paper. [scorer impact: -10.00]

- **The method's motivation is unclear relative to the LoRA-FA baseline.** LoRA-FA already achieves the same core memory savings (no activation storage for A's backward pass). LoLoRA additionally requires an optimizer state for local updates, making it slightly *more* memory-intensive (Table 4: LoRA-FA 23.9 GB vs LoLoRA 24.1 GB). The abstract's framing — "further reducing the memory required for fine-tuning" — is accurate vs standard LoRA but not vs LoRA-FA, which is the more relevant baseline. The paper adds complexity (HPCA hyperparameters, optimizer state, per-step local updates) without articulating a clear problem that LoLoRA solves that the simpler LoRA-FA does not. [scorer impact: -10.00]

- **The most directly informative comparison — LoLoRA HPCA (EVA init) vs LoRA-FA (EVA) in Table 4 — shows local updates making things slightly worse** (2.93 vs 2.92 perplexity, 24.1 GB vs 23.9 GB). The paper acknowledges this ("HPCA updates do not improve EVA-initialized adapters") but under-emphasizes its significance: if you already have a good initialization, online HPCA updates do not help and cost extra memory. [scorer impact: -5.48]

### Minor

- **The theoretical analysis (Assumption 4.1) models ΔW₀ as i.i.d. Gaussian — i.e., an unstructured full-rank matrix.** This is at odds with LoRA's premise that ΔW has exploitable low-rank structure. While this assumption serves as an uninformative prior about unknown targets, it means the theory characterizes optimal A for a setting where low-rank adaptation is fundamentally limited (Theorem 4.4(i) shows the expected loss floor depends on tail eigenvalues). The paper acknowledges the limitation of isolated submodules with stationary targets but does not discuss this tension. [scorer impact: -9.53]

- **The claimed advantage of online methods over EVA's one-time pre-pass is unsubstantiated.** The paper states that "online methods have the advantage of not requiring a separate incremental PCA pass before training" (line 328), but provides no analysis of how many forward steps HPCA needs to converge, nor a comparison of the accumulated computational cost of online HPCA updates throughout training vs a one-time EVA pre-pass. [scorer impact: -4.69]

### Trivial

None.

## Nice-to-Haves

- A synthetic experiment where the input distribution shifts mid-training, testing whether LoLoRA's online updates adapt faster than frozen baselines — this would directly test the claimed advantage over one-time EVA initialization.
- A breakdown of LoLoRA's wall-clock time overhead per step compared to standard LoRA-FA.
- Sensitivity analysis of the HPCA smoothing factor (mentioned as 0.98 with no ablation).

## Removed Points

These points were flagged for removal; treat with caution:
1. "Related work does not engage with Lagani et al.'s finding that mixing Hebbian and SGD degrades performance" — REMOVED because the paper explicitly discusses this finding (Section 2, lines 60-67).
2. "EVA-init not used as LoLoRA-updated variant" — REMOVED because Table 4 already shows "LoLoRA HPCA (EVA)" at 2.93 perplexity.
3. "Standard LoRA outperforms LoLoRA in ablations (Table 6) implying near-lossless compression claim is misleading" — REMOVED because the paper's stated goal is memory savings, not quality improvement, and the 0.01-0.02 perplexity gap is consistent with a memory-quality trade-off.
4. Various format/style nitpicks and speculative criticisms lacking paper-verifiable grounding.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the central claim honestly.** The data show LoLoRA *matches* LoRA-FA (EVA), not that it outperforms standard LoRA-FA. This is still a real finding: local online updates can converge to the same subspace as a one-time data-driven initialization. Present the paper as a theoretical+empirical study of optimal A initialization, where the theory is the primary contribution.

2. **Articulate the specific advantage over LoRA-FA clearly.** If the advantage is adaptability to non-stationary distributions, test this explicitly. If the advantage is avoiding a separate EVA pre-pass, quantify the trade-off. As written, the paper does not establish a clear use case for LoLoRA over the simpler LoRA-FA baseline.

3. **Remove the overstated conclusion** that LoLoRA "consistently outperforms standard LoRA-FA" — it is contradicted by the paper's own tables and damages the credibility of the theoretical contribution.

## Score and Decision

**Calibration anchor comparison:** The closest anchors are the EVA paper (avg 4.75, Reject — lacks theory that LoLoRA provides), LoRA-FA paper (avg 5.33, Reject — simpler contribution, cleaner presentation), and EigenLoRA (avg 5.00, Reject — eigenvalue-based LoRA variant with mixed reviews). LoLoRA's theory (+10.00 scorer impact) is its strongest asset, but the two decisive weaknesses (both -10.00: overclaiming, unclear motivation vs LoRA-FA) pull the score down significantly. The paper sits between EVA (4.75) and LoRA-FA (5.33), slightly above EVA due to the theory and slightly below LoRA-FA due to the more severe overclaiming.

**Final score: 5.0** — a paper with a genuine theoretical contribution held back by empirical claims that are contradicted by its own data and an unclear value proposition relative to a simpler baseline.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>