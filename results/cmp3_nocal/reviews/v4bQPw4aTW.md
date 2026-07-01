## Summary

This paper proposes AdaBoN, a two-stage adaptive Best-of-N alignment method. Given a batch of prompts and a fixed inference budget, AdaBoN first spends a uniform exploration phase to estimate per-prompt reward distributions (via KDE), then uses a greedy allocation procedure on the remaining budget based on each prompt's estimated marginal gain. The method is model-agnostic, requires no auxiliary training, and makes only two serial calls to the base LM. Experiments across 12 LM-RM pairs, 3 datasets, and 50 batches show consistent improvements over uniform allocation (BWRs ~0.54–0.62) and competitiveness against uniform allocations with ~23–27% larger budgets.

## Strengths

- **Clean formalization of the adaptive allocation problem (Section 2.3).** The paper precisely defines the objective (Equation 1), establishes uniform allocation as minimax-optimal in the non-adaptive setting, and uses a concrete Bernoulli example to motivate the need for adaptivity. This provides a clear framework that the method directly addresses.

- **Proposition 3.1 (Section 3).** The proof that the expected-max-of-samples function is concave and monotonically increasing for any distribution cleanly justifies the greedy allocation procedure. Though modest (it follows from known properties of order statistics), it directly supports Algorithm 1 and is used correctly.

- **Thorough empirical scope.** The evaluation covers 12 LM-RM pairs (4 LMs × 3 RMs), 3 datasets, 50 batches each, and multiple values of K and B — substantially broader than the most closely related work (Damani et al., 2024), which evaluates on a single LM, RM, and prompt batch for the real-valued reward setting.

- **Latency-aware design (Algorithm 2).** The two-stage structure ensures only two serial calls to the base LM (one parallelized exploration pass, one parallelized allocation pass). This is a genuine practical advantage over fully sequential bandit-style approaches.

## Weaknesses

### Fatal
None.

### Major

- **Exploration budget of d=0.75B is called "small" but constitutes 75% of the total budget.** The abstract and contributions (lines 9, 28) describe the exploration phase as using "a small exploration budget." In all main experiments, d = 0.75B, meaning the adaptive component controls only the remaining 25% of samples. The ablation for d is limited to the narrow range {0.60B, 0.70B, 0.75B, 0.80B} (line 242) and does not include genuinely small budgets (e.g., 0.1B, 0.25B). Without evidence that AdaBoN works with small exploration budgets, the "adaptive" framing is inflated relative to the empirical setup.

- **No empirical comparison with Damani et al. (2024), the most directly related prior work on the same allocation problem.** The paper provides justifications (different regime focus, unavailable implementation, computational cost of re-implementation — lines 50–56, 188), but these are stated rather than demonstrated. The claimed advantage of model-agnosticity and training-free operation over Damani et al. is asserted without supporting evidence. Given that this is the paper's central differentiator from prior work, the absence of any comparative evaluation is a significant gap.

### Minor

- **Only one baseline (uniform allocation).** No heuristic alternatives are compared — not even simple strategies such as allocating more budget to prompts with higher reward variance during exploration. While uniform is a natural minimax-optimal non-adaptive baseline, adding even a single simple heuristic would substantially strengthen the evidence that the full KDE+greedy machinery is worthwhile.

- **BWR reports win frequency, not win magnitude.** The BWR metric measures how often AdaBoN beats uniform, but not by how much. Reported BWRs of 0.54–0.62 (Table 1) with lower quartiles as low as 0.51 leave the practical significance of the gains unclear. Reporting the magnitude of cumulative reward differences alongside BWR would help assess this. (The paper's justification that RM scores are only meaningful comparatively — line 172 — is noted, but within a fixed LM-RM pair the raw reward deltas are still informative.)

- **No analysis of what drives allocation decisions.** The paper does not examine whether AdaBoN allocates more budget to prompts with higher-variance distributions, lower means, or other properties. An analysis of the correlation between estimated distribution characteristics and final allocations would improve interpretability.

- **Contribution (1) is overstated as a research contribution.** The claim that "per-prompt reward distributions are smooth and easy to learn" (line 27) is an empirical observation, supported by histograms, but is not itself a method or a theoretical finding. It should be presented as motivating evidence for the design choice rather than as a contribution.

- **Scott's rule formula (line 150) may contain an error.** The paper writes `h = σ̂ d^{1/5}` with a positive exponent, whereas standard Scott's rule uses `d^{-1/5}` (bandwidth decreasing with sample size). This may be a LaTeX formatting artifact (missing minus sign), but as written the formula would produce bandwidth that grows with the number of samples, which is incorrect. The authors should verify and correct.

- **EST truncation at 2B is mentioned in passing** (line 215) but its effect is not analyzed. Though EST values (~148–153 with B=120) are far from the cap of 240, making truncation unlikely, the paper should explicitly confirm that the cap does not distort results.

### Trivial
None.

## Nice-to-Haves

- Ablation with genuinely small exploration budgets (e.g., d ∈ {0.1B, 0.25B}) to demonstrate when the method does and does not help.
- Comparison against simple heuristic baselines (e.g., variance-based reallocation).
- Reporting of raw cumulative reward differences alongside BWR.
- Analysis of the correlation between estimated distribution properties and final allocation.
- Per LM-RM pair statistical significance tests for BWR > 0.50.

## Removed Points

- *Dataset inconsistency in figure captions (OCR-extracted text mentions "Medical, Math, ArXiv" while paper uses AlpacaEval, HH-RLHF, PKU-SafeRLHF).* — Parser artifact from embedded figure images; the actual text captions correctly state the datasets. Removed per rule on formatting artifacts.
- *Bernoulli example uses d/B = 0.4 while experiments use 0.75.* — Not a weakness; toy examples naturally use different parameters than realistic settings.
- *Paper does not discuss batch-availability limitation.* — Factually incorrect; lines 246–247 explicitly discuss this. Removed.
- *EST claims are overstated (20% vs actual 23–27%).* — The paper rounds down, i.e., understates the gains if anything. Not a valid criticism.
- *Missing related works.* — Cannot be verified externally. Removed per instructions.
- *Formatting/style nitpicks and reproducibility concerns about undisclosed hyperparameters.* — Removed per hard rules.
- *"Reward distributions are smooth" conflicts with known prior work.* — The reviewer's assertion is itself unverifiable; the observation is presented as empirical evidence rather than claimed novelty.

## Novel Insights

The harsh reviewer's most valuable observation is the mismatch between the paper's "small exploration budget" framing and the empirical choice of d=0.75B. This is not just a rhetorical issue — it changes the interpretation of the results: if 75% of the budget is spent uniformly, the gains are being driven by at most 25% of the samples, and the method's practical value depends on whether similar gains are achievable with much smaller exploration budgets. This insight is not present in the paper itself, which treats d as a fixed hyperparameter without interrogating the exploration/exploitation tradeoff. The reviewer's suggestion to report win magnitude alongside win rate is also well-taken, though the paper's justification for focusing on BWR is reasonable.

Beyond this, the reviews do not surface genuinely novel technical insights beyond the paper's own contributions.

## Suggestions

1. **Revise the framing** of the exploration budget: do not describe d=0.75B as "small." Add ablations with d ∈ {0.1B, 0.25B, 0.5B} to establish the method's behavior across the full range.
2. **Add at least one heuristic baseline** — e.g., allocate remaining budget to prompts with the highest variance or lowest observed maximum during exploration. This would demonstrate the value of full distribution estimation (KDE + greedy) over simpler statistics.
3. **Verify and correct the Scott's rule formula.** If the exponent is indeed positive, this is an error; if it is a LaTeX artifact, ensure the correct formula `h = σ̂ d^{-1/5}` appears.
4. **Report the magnitude** of cumulative reward differences (e.g., median reward ratio or difference) alongside BWR for at least a representative subset of LM-RM pairs.
5. **Add a brief analysis** correlating distribution properties (variance, skew, mean) with allocation outcomes to improve interpretability.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>