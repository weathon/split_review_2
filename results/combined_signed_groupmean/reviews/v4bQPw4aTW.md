## Summary

AdaBoN proposes a two-stage adaptive allocation strategy for Best-of-N inference-time alignment: first, uniformly sample d samples per prompt to estimate reward distributions via Gaussian KDE; second, greedily allocate the remaining budget across prompts based on estimated marginal gains. The paper also introduces BWR and EST as evaluation metrics and presents experiments across 12 LM-RM pairs, 3 datasets, and 50 batches per setting.

## Strengths

- **Broad and systematic evaluation (Section 4).** The paper evaluates across 12 LM-RM pairs (4 LMs × 3 RMs), 3 datasets (AlpacaEval, HH-RLHF, PKU-SafeRLHF), 50 distinct batches per setting, multiple batch sizes, and multiple inference budgets. For a method paper on inference allocation, this breadth is a genuine strength — it gives confidence the results are not cherry-picked. The impact score from the trained model rates this as +9.92 (decisive).

- **Simple and deployable method.** AdaBoN requires no auxiliary training, works with any LM-RM combination out of the box, and uses Gaussian KDE with Scott's rule for automatic bandwidth selection (effectively one hyperparameter d). The two-stage design minimizes sequential LM calls (only two rounds), which is genuinely useful for latency-sensitive applications (+9.74 impact).

- **The problem is real and well-motivated (Section 1, 2.3).** Uniform Best-of-N allocation is wasteful when prompt difficulty varies. The Bernoulli example in Section 2.3 cleanly illustrates why adaptivity can help, and the paper correctly identifies the practical importance of this setting.

## Weaknesses

### Major

**1. Framing-evidence mismatch on the exploration budget (d=0.75B).** The abstract describes the exploration phase as using "a small exploration budget." However, with d=0.75B, **75% of the total inference budget is spent on uniform exploration**, leaving only the remaining **25% for adaptive allocation**. Concretely, for the main experiment (K=5, B=120): exploration uses 90 samples per prompt (450 total), and the adaptive component distributes the remaining 30 samples per prompt (150 total across all prompts). The headline results (BWRs of 0.54–0.62) reflect whether adaptively distributing the *last 25%* of the budget outperforms uniform allocation of the *full* budget — a much weaker statement than what "adaptive Best-of-N" suggests. The motivating example in Section 2.3 uses d=10/B=25 (40% exploration), not 75%, and this gap is never addressed. The paper would be substantially stronger if it demonstrated meaningful performance with smaller d (e.g., d=0.1B or d=0.2B). *(Impact: -10.00 — decisive)*

**2. No comparison against any adaptive baseline.** The paper compares AdaBoN only against uniform allocation. The closest prior work (Damani et al., 2024) addresses the same problem but the paper does not implement a comparison. The stated reasons (no public implementation, prohibitive training cost) are understandable, but the paper could have implemented simple adaptive baselines — e.g., an oracle with perfect knowledge of reward distributions, a greedy-first strategy, or a threshold-based reallocation heuristic. Without *any* adaptive baseline, the reader cannot assess whether AdaBoN is a genuinely effective adaptive strategy or merely a marginal improvement over uniform that any reasonable adaptive heuristic would also achieve. This is a structural gap in the evaluation design. *(Impact: -9.99 — decisive)*

### Minor

**3. Modest effect sizes.** The median BWRs across Tables 1 and 2 range from 0.54 to 0.62 — a 4–12 percentage point improvement over the 0.50 baseline. The paper describes this as "consistently and often significantly outperforming," but these are small effects. The EST values (148–153 for B=120) are more impressive (competitive with ~25% larger budget), but this metric has caveats (see Weakness 5). The paper's language highlighting best cases ("as high as 70%" on some batches) should be balanced against the fact that for most LM-RM pairs, the improvement over uniform is incremental.

**4. Disconnect between optimization objective and evaluation metric.** AdaBoN's greedy allocation (Algorithm 1) maximizes expected cumulative max reward (Equation 1), but the primary evaluation metric is BWR (batch win rate), which measures whether AdaBoN beats uniform in a pairwise comparison rather than by how much. The paper's justification (Section 4.2) — that reward values are "often only meaningful comparatively" — is reasonable but incomplete: a method could improve BWR by sacrificing large gains on easy prompts for small gains on many prompts, potentially reducing expected cumulative reward while improving BWR. Reporting both metrics would resolve this concern.

**5. EST metric sensitivity to capping.** The EST (Equation 5) involves an infinite sum capped at 2B (Section 4.3, line 215: "We estimate the EST by capping the sum in Equation 5 to 2B."). The paper does not discuss sensitivity to this cap: if BWTR decays slowly, the cap could meaningfully underestimate EST.

**6. "Smooth and easy to learn" claim not quantified.** Section 3.1 claims reward distributions are "mostly smooth, have a few modes, and can be skewed" based on visual inspection of histograms (Figure 1). This claim could be quantified — e.g., by reporting convergence rates of KDE estimates, or by comparing estimated vs. held-out reward distributions via KL divergence. Without quantification, it remains a subjective observation.

### Trivial

None.

## Nice-to-Haves

- Ablating d more aggressively (d=0.1B, 0.2B, 0.3B) would demonstrate the adaptive component's standalone value.
- Reporting expected cumulative max reward alongside BWR would resolve the optimization-evaluation disconnect.
- Including an oracle adaptive baseline (perfect knowledge of reward distributions) would establish an upper bound on achievable gains.
- Adding statistical significance tests (e.g., confidence intervals for individual batch BWRs against 0.50) would quantify confidence in improvements.

## Removed Points

*(These points are flagged to be removed; treat them with caution.)*

- **"Proposition 3.1 not novel"**: The paper presents concavity of max-of-i.i.d. as a known property used to justify greedy optimality, not as a claimed novel contribution. The criticism mischaracterizes what the paper asserts.
- **"Motivating example uses 40% not 75%"**: The example was illustrative for a deliberately extreme case. The actual parameter choice is a separate design decision, noted in Weakness 1.
- **Section-by-section presentation nits**: Formatting observations, parser artifacts, and minor phrasing suggestions that do not affect technical merit.
- **"Damani et al. comparison not done"**: The paper already discloses the practical infeasibility (lines 188). The criticism about missing *any* adaptive baseline (Weakness 2) stands, but the specific complaint about not implementing Damani is softened by the paper's own disclosure.
- **Generic "lack of statistical significance"**: While true, this is standard for large-benchmark evaluations and does not threaten core claims.

## Novel Insights

None beyond the paper's own contributions. The primary insight from the review is that the paper's framing ("adaptive Best-of-N") implies a more aggressive adaptive strategy than what is implemented (75% uniform exploration, 25% adaptive tail allocation). This tension between framing and execution is the most significant issue.

## Suggestions

1. **Rebalance the framing.** Replace "small exploration budget" with an honest description: "we allocate a majority of the budget to uniform exploration (d=0.75B as default) and redistribute the remaining fraction adaptively." Report results with smaller d values to establish the method's standalone adaptive value.
2. **Add at least one adaptive baseline.** A simple threshold-based heuristic (e.g., allocate extra budget to prompts whose current max reward falls below a percentile) or an oracle baseline would allow the reader to calibrate AdaBoN's performance.
3. **Report the expected cumulative max reward** alongside BWR across batches, to verify that BWR gains are not masking overall reward degradation.

## Score and Decision

### Calibration Summary

Round 1 bracket (3.5–6.5) was established by comparison to the most closely related anchors:
- **Damani et al. (6qUUgw9bAZ.md, avg 6.50)** — Same problem. Had one decisive weakness (baselines -9.99) but stronger results (50% compute reduction). Our paper has an additional decisive weakness (framing mismatch) and weaker effect sizes.
- **Inference-Aware Fine-Tuning (77gQUdQhE7.md, avg 5.67)** — BoN-related. Weaknesses about limited eval scope (-8.62). Our paper has better breadth but more weaknesses.
- **Inference Scaling Laws (VNckp7JEHn.md, avg 5.75)** — BoN-related. Had limited task scope (-9.08) but strong theoretical contributions (+9.98).

Round 2 narrowing (4.0–6.5) confirmed placement below Damani (6.50) but above papers scoring <4.0 with unrelated topics. The deciding factor: our paper shares with Damani the decisive baseline weakness (-9.99) but adds a framing-evidence mismatch (-10.00) unique to this paper, while the EST results and evaluation breadth provide partial counterweights.

**Final placement: 5.0** — The paper addresses a real problem with a clean method and admirably broad evaluation, but the central claim is over-sold (75% exploration is not "small"), no adaptive baseline exists for comparison, and the effect sizes are modest. These gaps are fixable but limit the paper's current contribution.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>