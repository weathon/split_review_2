## Summary

AdaBoN addresses the problem of making Best-of-N alignment more efficient by adaptively allocating the sampling budget across a batch of prompts. The paper proposes a two-stage method: (1) use a uniform exploration budget *d* per prompt to estimate reward distributions via KDE, (2) allocate the remaining budget via a greedy algorithm on estimated marginal gains. The method is evaluated across 12 LM-RM pairs, 3 datasets, and 50 random batches per setting, using two bespoke metrics (BWR and EST). Results show AdaBoN consistently outperforms uniform allocation with the same total budget and is competitive against uniform allocations with ~20% larger budgets.

## Strengths

1. **Well-motivated problem and clean formulation.** The paper correctly identifies that applying a fixed *N* uniformly across all prompts wastes computation on "easy" prompts. Framing this as a batch allocation problem (Section 2.3) is clean and natural. The motivating Bernoulli example (p. 3, lines 84-85) effectively illustrates why adaptivity can matter, and the two-stage design is a principled way to introduce adaptivity while respecting latency constraints.

2. **The EST metric captures something genuinely informative.** The Expected Survival Time (Equation 5) — how large a uniform budget AdaBoN matches or exceeds — provides a concrete, interpretable measure of computational savings. An EST of 150 against *B*=120 (Table 2a) translates to ~25% effective budget savings, and the observation that some batches achieve EST ≥ 160 (~33% savings) is the paper's most compelling quantitative result.

3. **Comprehensive evaluation scope.** The paper evaluates on 12 LM-RM pairs (4 LMs × 3 RMs), across 3 datasets, 50 random batches per setting, varying *K* and *B*. This is substantially broader than the closest related work (Damani et al., 2024), and the consistency of results across LM-RM pairs suggests the phenomenon is general rather than an artifact of a particular model combination.

4. **Clean theoretical anchor.** Proposition 3.1 (concavity and monotonicity of the expected-max function, line 108) is the right theoretical observation to justify the greedy allocation algorithm, and the paper honestly acknowledges that it applies to the *true* value vectors, not the estimated ones (line 121).

## Weaknesses

### Major

1. **The exploration budget *d*=0.75*B* consumes most of the budget and its effect is not isolated from the adaptive component.** With *d*=0.75*B*, AdaBoN spends 75% of the total budget in a *uniform* exploration phase; only the remaining 25% is allocated adaptively. The paper tunes *d* over the narrow range {0.60*B*, 0.70*B*, 0.75*B*, 0.80*B*} (line 242) — every option in this range has exploration as the dominant term. Without ablations that test substantially smaller *d* (e.g., *d* ∈ {0.1*B*, 0.25*B*, 0.5*B*}) or a "no-adaptivity" baseline that uses the same two-stage structure but allocates the remaining budget uniformly, it is impossible to tell whether the reported gains come primarily from the adaptive allocation mechanism or from the large uniform exploration phase. The abstract calls the exploration budget "small" (line 9), which is misleading for *d*=0.75*B*.

2. **No comparison against any alternative allocation strategy.** The paper compares only against the uniform baseline, which any adaptive method with strictly more information should be expected to beat. The closest related work (Damani et al., 2024) is discussed but not compared against (line 188), and no simple adaptive heuristic baseline is provided (e.g., "allocate all remaining budget to the prompt with the highest observed max after exploration," or a round-robin with early stopping). The paper's cost justification for not comparing against Damani et al. contains an arithmetic error: it claims "216,000 MLPs" (line 189), but the correct figure is 21,600 (600 values of *b* × 12 LM-RM pairs × 3 datasets) — a factor-of-10 error that, while the number is still large, undermines confidence in the diligence of this justification.

### Minor

3. **The "smooth and easy to learn" claim (Contribution 1, line 27) is supported only by visual inspection.** The paper asserts that reward distributions are "smooth and easy to learn," but the only support is a few histograms (Figure 1 and Appendix F). No quantitative measure of smoothness or estimation accuracy as a function of *d* is provided.

4. **Latency claim would benefit from more precision.** The paper states that AdaBoN "minimizes latency" (line 136) because it makes "only two calls to the base LM." However, the first call generates *d*=90 responses per prompt (with *K*=5, *B*=120), which can be parallelized but still dominates wall-clock time. The latency advantage is relative to *fully sequential* adaptive methods (bandit approaches), not to uniform allocation, which also batch-generates *B*=120 responses in one pass. The paper should state this more precisely.

5. **Computational overhead of the planning stage is not reported.** The Monte Carlo estimation uses *m*=1024 samples per *Vᵢ,ⱼ* estimate. For *K*=5, *B*=120, *d*=90, there are roughly 750 estimates, each requiring 1024 KDE draws — ~768,000 draws per batch (line 150). The paper does not report the wall-clock overhead of this planning phase relative to the LM generation time, making it hard to assess practical efficiency.

6. **EST truncation at 2*B* (line 215) is mentioned without justification.** Though the reported ESTs (148-156) are well below the cap, a brief sensitivity analysis confirming that a larger truncation bound does not change results would strengthen the metric's credibility.

### Trivial

None.

## Nice-to-Haves

- **EST truncation analysis:** Verify that capping the sum at a value larger than 2*B* does not meaningfully change the reported EST values.
- **Quantify distribution smoothness:** Provide a simple measure of KDE estimation error (e.g., log-likelihood on held-out samples) as a function of *d* across prompts.

## Removed Points

*These points are flagged to be removed. Treat them with caution.*

- **BWR metric validity (Critic's Issue 3).** Removed. The paper's justification for BWR (line 172) is internally consistent: RM scores from a single RM are on a common scale, and comparing sums of max rewards across prompts via a win rate is a form of pairwise comparison at the batch level, which does not require cardinal interpretability of individual scores. The criticism misunderstands the metric.
- **Bernoulli example uses binary vs. continuous rewards.** Removed. The Bernoulli example (lines 84-85) is a pedagogical illustration of why adaptivity matters *in principle*, not a claim about empirical reward distributions. Papers commonly use simplified examples for intuition.
- **KDE bandwidth details (Scott's rule).** Removed. This is an implementation detail. The method works empirically across all 12 LM-RM pairs, which is sufficient validation.
- **Figure caption parser artifacts.** Removed. The "Medical, Math, ArXiv" text in Figure 3's embedded alt-text (lines 232-234) is a PDF-parser artifact; the actual paper caption (line 236) correctly states the AlpacaEval dataset.

## Novel Insights

The review surfaces an important structural concern that the paper itself does not adequately address: AdaBoN's two-stage design places 75% of its budget into the non-adaptive exploration phase, and the experimental design does not distinguish between gains from the adaptive allocation of the remaining 25% versus gains from having a large uniform sample. Additionally, the absence of comparison with any alternative allocation strategy — even simple heuristic ones — means the evaluation establishes only that AdaBoN beats the uniform baseline, which is the weakest possible positive result for an adaptive method. These issues are fixable and the core idea is promising, but the evidence in its current form is suggestive rather than conclusive.

## Suggestions

1. Ablate *d* over a much wider range (e.g., *d* ∈ {0.1*B*, 0.25*B*, 0.5*B*, 0.75*B*}) and include a "no-adaptivity" baseline that uses the same two-stage structure but allocates the remaining budget uniformly. This would directly isolate the contribution of the adaptive component.
2. Add at least one simple adaptive baseline (e.g., "greedy-allocate-to-best" after exploration: allocate all remaining budget to the prompt(s) with the highest observed max reward so far).
3. Correct the arithmetic error in the MLP count (line 189) or clarify what is being counted.
4. Report wall-clock time of the planning stage (KDE fitting + Monte Carlo sampling) relative to LM generation latency.
5. Quantify the "smooth and easy to learn" claim with a measure of estimation error (e.g., held-out log-likelihood) as a function of exploration budget *d*.

## Score and Decision

**Calibration anchors used:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6qUUgw9bAZ.md` (Damani et al., avg 6.50, Round 1, itemized) — same inference allocation problem; AdaBoN is training-free with broader evaluation but has the *d*=0.75*B* confound that Damani does not. AdaBoN is slightly weaker overall.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/77gQUdQhE7.md` (Inference-Aware BoN, avg 5.67, Round 1, itemized) — BoN-related method; AdaBoN's evaluation is much broader but both have similar types of experimental confounds. Comparable quality.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8HQS1X2AK4.md` (HyRe test-time alignment, avg 5.33, Round 1, itemized) — test-time alignment; AdaBoN has cleaner assumptions but also lacks baselines. Slightly stronger than HyRe.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Yz7ts36V7A.md` (Backoff Decoding, avg 3.67, Round 1, itemized) — AdaBoN is clearly stronger than this paper.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/JLDAWbzTUg.md` (C2MAB-V bandit selection, avg 5.50, Round 2, itemized) — bandit-based budget allocation; AdaBoN is more directly applicable to BoN and has cleaner evaluation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/VNckp7JEHn.md` (Inference Scaling Laws, avg 5.75, Round 2, itemized) — empirical study with limited scope; AdaBoN has a clearer method contribution.

**Round 1 bracket:** 4.0–6.0 (based on overlap with Damani et al. 6.50, Inference-Aware BoN 5.67, HyRe 5.33, and Backoff Decoding 3.67).

**Round 2 narrowing:** Comparing itemized weights, AdaBoN shares the "limited baselines" weakness with Damani et al. (weight -2 to -3) and HyRe (weight -4), and has a confound analogous to Inference-Aware BoN's "improvement may stem from increased sample selection" (weight -4). AdaBoN's key advantages — broad evaluation (12 LM-RM pairs) and training-free method — are missing from those weaker anchors, pulling it upward. The narrow *d* ablation range and lack of adaptive baselines are the primary factors distinguishing it from the 6.0+ level of Damani et al. Final score placed at 5.5.

**Final score:** 5.5

**Final decision:** Reject

The core idea is sound, the method is clean, and the evaluation scope is admirable. However, the experimental design does not adequately separate the effect of the large (75%) uniform exploration phase from the effect of the adaptive allocation mechanism, and the absence of comparison against any adaptive baseline limits the strength of the empirical claims. With improved ablations and baselines, this paper could be competitive for acceptance.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>