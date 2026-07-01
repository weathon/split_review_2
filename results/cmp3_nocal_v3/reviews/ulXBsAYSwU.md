## Summary

MolMiner is a fragment-based autoregressive transformer for molecular design that unifies several capabilities in a single model: dynamic 3D geometry (forcefield relaxation at each generation step), symmetry-aware fragment attachment (cyclic permutation identification via Morgan fingerprints), order-agnostic rollout (randomized construction order as regularization), and multi-property conditional generation (12 physicochemical properties simultaneously). The GMM-based mechanism for completing partial conditioning vectors makes the system usable when users specify only a subset of targets.

---

## Strengths

- **Scale of multi-property conditioning.** Conditioning on 12 molecular properties simultaneously is substantially larger than prior work (typically 1–3 properties). The GMM completion mechanism for partial conditioning vectors is a practical design choice for real usage scenarios. This is the paper's headline contribution.

- **Principled symmetry handling for cyclic fragments.** The symmetry-aware attachment protocol (Section 3.2) addresses a genuine problem: when a fragment like benzene has indistinguishable attachment sites, canonical SMILES alone cannot resolve which atom is which. Using cyclic permutation identification via Morgan fingerprint similarity is a computationally lightweight and principled solution.

- **Dynamic geometry during autoregressive generation.** Using forcefield relaxation at each generative step (rather than freezing geometry early, as in G-SchNet) is a genuine improvement. The two-stage approach — precomputing rollouts with geometry for training, then dynamic relaxation at inference — is a sensible engineering compromise.

---

## Weaknesses

### Major

1. **No conditional baseline in the central conditional evaluation.**  
   The paper's conditional evaluation (Section 4.3) consists entirely of calibration plots for MolMiner alone. There is no comparison to any conditional generative model: no conditional VAE, no property-conditioned diffusion model, no guided sampling approach, not even an ablation of MolMiner with fewer conditioning dimensions. Calibration plots show that *within the model's own framework* prompted and predicted values correlate, but without a baseline, a reader cannot assess whether this correlation is strong, weak, or trivial. The paper claims "accurate and calibrated conditional generation" — but a reader has no comparator to judge what "accurate" means. The criticism is not that the paper must beat every existing method, but that the primary claimed capability (multi-property conditional control) is demonstrated via a self-consistency check with no external anchor.

2. **Ablation findings asserted without any quantitative support.**  
   Section 4.1 states three ablation findings: (i) more properties improve conditioning, (ii) geometry-aware attention helps with positive bias, (iii) rollout resampling reduces overfitting. **No numbers, tables, or figures support any of these claims.** For a paper that makes multiple architectural claims (dynamic geometry, symmetry handling, order-agnostic rollout, GMM conditioning), quantitative ablation results are essential to evaluate whether each component pulls its weight. Without them, the reader cannot assess whether geometry-aware attention improves Wasserstein distance by 5% or 0.5%, or whether order-agnostic regularization is a first-order effect or marginal.

3. **Unconditional performance gap undermines confidence in conditional results.**  
   Table 1 shows HierVAE beating MolMiner on 11 of 12 Wasserstein distance metrics in the unconditional setting — often by large margins (molWt: 15 vs. 65 for MolMinerS; TPSA: 2.3 vs. 10.9; MR: 3.8 vs. 16.3). The paper's explanation (early termination bias from imbalanced termination actions in training rollouts) is plausible but untested. The model's known failure modes (molWt, TPSA, MR) in the unconditional setting also appear as "systematic deviations" in the conditional calibration plots (the paper notes this itself). This pattern suggests the conditional control may be mediated by the same distributional biases rather than reflecting genuine structure-property understanding. At minimum, the paper should investigate the early-termination hypothesis quantitatively (e.g., by reporting the distribution of fragment counts in generated vs. training molecules, or by attempting to balance termination actions).

### Minor

1. **The MolLeR comparison is framed uninformatively.**  
   The paper reports that MolLeR was run for 7 days but completed only ~10,000 training steps, after which samples were poor, and the model is excluded from the main comparison. The paper also notes these failures are consistent with known MolLeR issues. The handling is not unfair, but the framing in the main text could mislead a casual reader into thinking a proper comparison was attempted and failed. Either the model should be trained to a more established convergence point (even if expensive), or the discussion should be more clearly caveated about the insufficient training duration.

2. **Inconsistent epoch count.** Section 4.1 states the final model was "trained with resampling for 50 epochs." Section 7 says "Training these models took approximately 7 days, or 30 epochs." This inconsistency should be resolved.

3. **Validity is hand-waved rather than quantified.** The paper omits validity metrics, stating that "our model enforces valence constraints during generation and consistently produces valid molecules." However, other sources of invalidity exist (e.g., steric clashes after geometry relaxation, unrealistic bond angles). Reporting a concrete validity percentage (>99% would be a strength) would strengthen the paper.

### Trivial

- Novelty and Uniqueness metrics in Table 1 are nearly saturated for all models (98–100%), making them uninformative as discriminators.
- The claim of "improved benchmarking methods" (Wasserstein distance, calibration plots) is overstated for what are standard tools.

---

## Nice-to-Haves

- The paper could include a simple conditional baseline, such as a CVAE using the same fragment vocabulary and conditioning vector, or property-conditioned HierVAE. This single addition would transform the conditional evaluation from a self-consistency check into a genuine scientific comparison.
- An analysis of how many unique rollout orders exist per molecule and how many the model sees over 50 epochs would help evaluate whether the Monte Carlo approximation of the expectation (Eq. 1/3) is adequate.
- Clarifying how the learnable scalar θ in the attention bias (Eq. 2) is initialized and how its learned value compares to the scale of g(h_i, h_j) would aid reproducibility.
- Reporting the distribution of molecular weights/fragment counts in generated vs. training molecules would help test the early-termination hypothesis.

---

## Removed Points

- **Criticism about missing appendix details (focalized readout description, etc.):** The appendix was stripped by the parser. These details exist in the original submission. REMOVED.
- **Criticism about the expectation approximation being insufficient (one rollout per epoch):** This is a reasonable technical question but not a demonstrated weakness, and the paper frames it as data augmentation over 50 epochs. Demoted to Nice-to-Have.
- **Criticism about the log-space vs. linear-space mixing in the attention bias:** A design choice explained in the paper. Demoted to Nice-to-Have.
- **Criticism that the dataset is "small and homogeneous":** The ~200K ZINC subset is a standard benchmark in this field. This is a generic criticism that could apply to most molecular generation papers. REMOVED.
- **Strength about "addressing an important problem":** Generic and not specific to this paper. REMOVED.

---

## Novel Insights

The harsh review's core insight — that the paper's central claim (multi-property conditional generation) is evaluated without any baseline comparison, and that the unconditional performance gap shares failure modes with the conditional calibration deviations — is a genuine observation about the paper's evidence structure that goes beyond simply listing missing baselines. It identifies a coherence problem: the model's systematic errors in unconditional generation reappear as systematic deviations in the conditional calibration plots, suggesting that the "conditional control" may be partially reflecting distributional biases rather than learned structure-property mappings. This is a substantive critique that the authors should address directly.

---

## Suggestions

1. Add at least one conditional baseline to the conditional evaluation — even a simple CVAE with the same fragment vocabulary, or a property-conditioned variant of HierVAE.
2. Provide quantitative ablation results (a table with Wasserstein distances) for the three claimed findings in Section 4.1.
3. Investigate the early-termination hypothesis: report fragment-count distributions, and either balance termination actions or attempt an RL fine-tuning to calibrate the termination policy.
4. Resolve the 30-epoch vs. 50-epoch inconsistency.
5. Add a concrete validity percentage to the metrics table.

---

## Score and Decision

The paper addresses a real need and makes several well-motivated methodological contributions (multi-property conditioning at this scale, symmetry-aware fragment handling, dynamic geometry integration). However, the evaluation has significant gaps: the central claim of conditional generation is evaluated without any baseline comparison, ablation claims are purely qualitative, and the unconditional performance gap is not adequately resolved. These issues are structural but not fatal — the method itself is sound and the contributions are genuine. The paper would be acceptable after addressing the conditional baseline requirement and providing quantitative ablations.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>