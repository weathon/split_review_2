## Summary

SPOT proposes using attention weights from a Preference Transformer to identify subgoals in preferred trajectories, training a CVAE to generate context-appropriate subgoals, and using cosine similarity between predicted subgoals and next states as a reward-shaping signal to mitigate extrapolation error in offline preference-based RL. The dual-criteria filtering (attention weight percentile + above-average predicted reward) is a sensible mechanism for selecting meaningful subgoals.

## Strengths

- **Method motivation and design.** The core idea — using the Preference Transformer's learned attention weights to identify critical decision points as subgoals, then generating them via CVAE for reward shaping — is well-motivated. The dual-criteria filtering (Eq. 5–6) addresses the genuine failure mode where high-attention states from marginally-preferred trajectories could be misleading.

- **Diagnostic evidence for the core claim.** Figure 2b directly tests the paper's thesis by showing that SPOT's shaped-reward policy leads to states where the shared reward model makes smaller extrapolation errors compared to PT's unshaped policy, at comparable similarity-to-subgoal levels. This is the right kind of analysis for a paper claiming subgoal guidance mitigates extrapolation error.

- **Broad evaluation scope.** The paper evaluates across 10 tasks from three benchmark families (D4RL, Robosuite, Meta-World) with 6 baselines plus Oracle, and includes a query-efficiency experiment (Table 4) showing SPOT maintains competitive performance with fewer preference queries.

## Weaknesses

### Major

- **Oracle baseline inconsistency undermines experimental confidence.** The Oracle is described as "ground-truth reward from the dataset" using IQL (p.5, line 210), which should be an upper bound. Yet in Table 1, preference-based methods routinely outperform it: hop-m-e Oracle=62.10 vs DTR=102.12 and SPOT=98.73; lift-mh Oracle=81.62 vs MR=95.62; can-mh Oracle=34.30 vs DTR=60.28 and SPOT=60.55. If the true reward function (Oracle+IQL) scores 81.62 on lift-mh while a learned preference model (MR) scores 95.62, this suggests either different hyperparameters/evaluation protocols between Oracle and other methods, or that the evaluation metric does not align with what the true reward optimizes. The paper provides no explanation. This casts doubt on whether the entire comparison table reflects fair, controlled conditions.

- **Empirical results are overstated relative to per-task evidence, including a factual error.** SPOT is outright best on only 2 of 10 tasks (walk-m-r, plate-slide) and tied on a 3rd (can-mh). On several tasks it is substantially behind: lift-mh (65.17 vs MR's 95.62), can-ph (63.82 vs Oracle's 73.25), drawer-open (66.80 vs IPL's 87.64). The average improvement (78.82 vs PT's 74.76) is modest. More critically, the paper makes a **factually incorrect claim** (line 216): "In the hopper environment, SPOT achieves state-of-the-art performance on both medium-replay and medium-expert datasets" — but DTR outperforms SPOT on hop-m-r (94.18 vs 85.08) and hop-m-e (102.12 vs 98.73). The abstract and introduction claim "state-of-the-art performance" and "superior performance compared to existing methods," which is broader than what the data supports.

### Minor

- **High variance and selective support in the reward-shaping ablation.** Table 3 shows striking variance: on hopper-m, cosine similarity at λ=0.1 gives 55.85 ± 42.94 (std=77% of the mean). The claim "cosine similarity achieves superior performance on both environments" (line 245) is only clearly supported at λ=1.0 on hopper-m (97.36) and across most λ on walker2d-m; at other λ values it is often worse or highly unstable. The "superior" claim is overstated.

- **Missing experimental details for reproducibility.** The Setup section (line 212) specifies only Top-K%=10, β=1, λ=1. Missing: number of preference pairs used for training, trajectory length, transformer architecture (layers/heads/embedding), CVAE architecture (latent dimension, layers), learning rates, batch sizes, training steps for both the reward model and CVAE, and IQL hyperparameters (expectile, temperature). These are needed for fair comparison and reproduction.

- **Circular dependency in dual-criteria filtering not discussed.** The reward constraint (r̂_t ≥ r̄) uses predicted reward from the same PT model whose noise the method aims to mitigate. If PT's reward estimates are unreliable for certain states, the filter could discard genuinely good subgoals while retaining spuriously high-reward ones. This is not discussed.

### Trivial

None.

## Nice-to-Haves

- A direct distributional analysis (e.g., MMD or density estimation) showing that SPOT's policy visits states with higher density overlap with the training data would strengthen the causal link between subgoal guidance and extrapolation error reduction.
- Clarifying that Figure 2b compares the induced state distributions of the two policies (not the error on identical state-action pairs) would improve exposition. The current analysis is valid but the caption is ambiguous.
- Reporting reward prediction accuracy on held-out preference data would help assess whether the reward model is better calibrated under SPOT.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Overstated gap in research positioning:** The claim that existing methods "overlook the rich information contained in preference datasets, dismissing valuable signals" (line 17-22) is a reasonable framing of the paper's contribution gap, not a weakness.
- **Figure 2 being "confounded":** The reviewer argued this is a "methodological gap," but the figure compares the policies' induced state distributions, which is the intended comparison. The complaint is primarily about exposition clarity (addressed under Nice-to-Haves).
- **Speculation about image-based observations:** The reviewer questions cosine similarity on "raw pixels" for Robosuite/Meta-World, but these benchmarks commonly use low-dimensional state vectors. Not supported by evidence in the paper.
- **Missing statistical comparison / reward model quality analysis / computational cost discussion:** These are nice-to-haves or community-standard-optional analyses, not core weaknesses.
- **CVAE temporal relationship underspecified:** The paper does explain the temporal relationship (line 136), and Figure 3 provides qualitative validation. Adequately addressed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Resolve the Oracle inconsistency** — either clarify that the Oracle uses a different hyperparameter/evaluation protocol, or explain why the ground-truth reward does not align with the normalized evaluation metric.
2. **Correct the factual error** about hopper performance (line 216): DTR outperforms SPOT on both hop-m-r and hop-m-e.
3. **Calibrate the paper's claims** to match the per-task evidence. Replace "state-of-the-art" with precise language such as "competitive performance with the highest average score across tasks."
4. **Provide complete experimental details** (architectures, hyperparameters, training setup) for reproducibility.
5. **Discuss the circular dependency** in the dual-criteria filtering where the PT reward model's own predictions are used to filter subgoals.

## Score and Decision

**Calibration anchors** (all retrieved across rounds):

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| Hindsight Preference Learning (4HNfKrGlSJ) | 5.20 | R1, R2 | Yes | Similar offline PbRL with VAE. Mixed reviews (3-8), rejected. SPOT has stronger method motivation but weaker empirical reliability (Oracle issue). |
| OPRIDE (MFwYXa796v) | 5.00 | R1, R2 | No | Offline PbRL query efficiency. Rejected. Similar weakness severity. |
| LEASE (38kLrJNwaM) | 6.00 | R2 | Yes | Offline PbRL with theoretical analysis. Rejected despite one 8. SPOT lacks theoretical grounding that LEASE attempted. |
| Outward Odyssey/PPE (gXV84CnMUm) | 5.50 | R2 | Yes | PbRL with policy exploration. Rejected. SPOT has a cleaner method but similar empirical overclaim issues. |
| Sim-OPRL (2pJpFtdVNe) | 6.80 | R1 | Yes | Theoretical + empirical offline PbRL. Accepted. Above SPOT's level. |
| UA-PbRL (RKOAU5ti1y) | 7.00 | R1 | Yes | Distributional PbRL. Accepted. Above SPOT's level. |

**Round-1 bracket:** 3.5–5.5 (reject range for offline PbRL papers)
**Round-2 narrowing:** The closest topical anchors (HPL at 5.20, OPRIDE at 5.00, LEASE at 6.00) all received Reject decisions. SPOT shares the HPL weakness profile (method is motivated but empirical evidence is weaker than claimed) and adds the Oracle inconsistency that HPL did not face. The two decisive weaknesses — Oracle inconsistency (−9.99 impact) and factually incorrect/overclaimed results (−10.00 impact) — each individually carry enough severity to pull a strong score below acceptance. The factual error about hopper performance (line 216 directly contradicts Table 1) is particularly concerning as it is verifiable from the paper's own data.
**Final score:** 4.5

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>