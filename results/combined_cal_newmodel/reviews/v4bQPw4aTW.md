Now I have all the data needed. Let me compile the final review.

## Summary

This paper proposes AdaBoN, a two-stage adaptive Best-of-N alignment method that allocates inference-time compute across prompts based on estimated difficulty. In the first stage, a fixed per-prompt exploration budget is used to estimate each prompt's reward distribution via KDE. In the second stage, the remaining budget is allocated greedily using estimated marginal gains. The method is evaluated across 12 LM-RM pairs, 3 datasets, and 50 batches per configuration, consistently outperforming the uniform allocation baseline.

## Strengths

- **Well-motivated problem.** The paper correctly identifies that Best-of-N with a uniform N across all prompts is wasteful (Section 1, lines 19–23), and the two-stage design is grounded in a latency argument (Section 2.3, lines 93–96). **[favorability=13.74]**

- **Clean theoretical grounding.** Proposition 3.1 (line 108) shows the expected-max function is concave and monotonically increasing, justifying the greedy procedure in Algorithm 1 for optimal allocation on estimated quantities. **[favorability=10.66]**

- **The EST metric is a clever operationalization of computational savings.** Translating allocation gains into an equivalent uniform budget (Equation 5) makes practical savings tangible (e.g., EST of 151 with B=120 means AdaBoN matches a uniform allocation costing ~26% more compute). **[favorability=11.18]**

- **Broad empirical evaluation.** The paper covers 4 LMs × 3 RMs = 12 LM-RM pairs across 3 datasets, with 50 batches per configuration and 100 runs per batch. The consistent pattern of BWR > 0.50 across most configurations (Table 2b) indicates the result is reproducible across multiple settings. **[favorability=12.25]**

## Weaknesses

### Fatal

None.

### Major

- **The paper compares AdaBoN only against the uniform (non-adaptive) baseline.** While this demonstrates that adaptivity helps, it does not validate whether the specific KDE-based estimation + greedy allocation machinery yields meaningful gains over simpler adaptive heuristics (e.g., variance-based allocation allocating more budget to high-variance prompts, or gap-based allocation prioritizing prompts with lower current best reward). The paper's justification for not comparing against Damani et al. (2024) is reasonable (different regime, computational cost), but simple heuristic baselines would require negligible implementation effort and would isolate what drives the results. Without such comparisons, the marginal value of the paper's specific methodological choices over obvious alternatives is unclear. *Note: the closely related Damani et al. (2024) paper also received a "limited baselines" criticism from its reviewers (favorability -0.52) yet was accepted at 6.50 — however, AdaBoN's case is more acute because it has zero adaptive baselines while Damani et al. had at least random allocation.* **[favorability=-0.37]**

### Minor

- **The abstract and contribution list (lines 9, 28) describe the exploration budget as "small," but the main experiment uses d = 0.75B (line 215).** This means 75% of the total budget is spent uniformly, and the adaptive component controls only the remaining 25%. The framing overstates the degree of adaptivity. **[favorability=0.59]**

- **The paper does not specify which decoding parameters (temperature, top_p, top_k, do_sample) are used**, stating only "the default decoding strategy from HuggingFace" (line 215). Since Best-of-N relies on sufficient stochasticity in the base policy, and different models have different defaults, this omission affects both reproducibility and interpretation (some models' defaults may be near-deterministic). **[favorability=1.74]**

- **The exploration budget d is tuned over a narrow grid {0.60B, 0.70B, 0.75B, 0.80B} (line 242).** Testing smaller values (e.g., d = 0.1B, 0.25B, 0.5B) would help characterize when the adaptive component begins to contribute meaningfully, which is especially relevant given that 75% of the budget is currently reserved for exploration. **[favorability=2.45]**

- **The KDE bandwidth is selected using Scott's rule without ablation (line 150).** With only d ≈ 90 samples per prompt, the bandwidth can substantially affect the estimated Vᵢ,ⱼ values and thus the allocation. An ablation varying the bandwidth would strengthen confidence in robustness. **[favorability=2.38]**

### Trivial

None.

## Nice-to-Haves

- Adding two simple heuristic baselines (e.g., variance-based allocation after initial d samples, gap-based allocation prioritizing prompts with lower current best) would substantially strengthen the paper's ability to attribute gains to the specific KDE + greedy allocation machinery — and would be the single most impactful improvement.
- Reporting the actual variance in per-prompt final allocations (how much budget is actually redistributed away from uniform) would clarify whether the greedy procedure makes meaningful allocation decisions.

## Removed Points

These points from the harsh review are removed with justification:

- **"Gains are modest (BWR 0.54–0.62)":** The paper is transparent about these numbers; the EST metric shows meaningful savings (~26% larger budget equivalence). Whether gains are "modest" is a subjective interpretation, not a verifiable weakness.
- **"The paper cannot actually demonstrate that its specific method is valuable":** Overstated — the paper shows the specific method beats the non-adaptive baseline, which is a valid (if limited) demonstration. The core issue (lack of adaptive baselines) is already captured in the Major weakness.
- **Bernoulli example uses different exploration ratio:** This is an illustrative example and does not need to match experimental settings exactly.
- **"Personalized on-device inference" claim mismatch:** Minor scope creep that does not affect the core technical contribution.
- **KDE estimation from only d=90 samples is noisy:** The paper shows empirical success across 12 LM-RM pairs, demonstrating the approach works despite this potential concern.
- **Section-by-section notes that are opinion-based or non-substantive** (e.g., the gap between example exploration ratio and actual, the "at most 6% above chance" framing of BWR).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The single most impactful improvement would be to add two simple adaptive baselines requiring no training: (1) variance-based allocation — after the initial d samples, allocate more budget to prompts with higher observed reward variance; (2) gap-based allocation — allocate more budget to prompts whose current best observed reward is lowest. If AdaBoN outperforms these, the paper would have strong evidence that its specific machinery is genuinely better. If not, the framing should be adjusted accordingly.

## Score and Decision

### Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized? | Comparison to Reviewed Paper |
|---|---|---|---|---|---|
| Damani et al. (2024) | 6qUUgw9bAZ.md | 6.50 | Bracketing | Yes | Most closely related work; had similar "weak baselines" criticism but scored higher due to more diverse task domains (code, math, chat) and use of both best-of-k and routing. AdaBoN has broader LM-RM evaluation but more modest gains and the d=0.75B framing issue. |
| Inference-Aware Fine-Tuning for BoN | 77gQUdQhE7.md | 5.67 | Bracketing | Yes | Accepted with weakness about limited evaluation (single model, single task). AdaBoN has broader evaluation, making it at least comparable. |
| Large Language Monkeys | 0xUEBQV54B.md | 5.00 | Bracketing | Yes | Rejected due to "trivial findings" criticism. AdaBoN has a more novel methodological contribution. |
| Online Learning for Prompt Selection | k73R7xdWtl.md | 5.33 | Narrowing | Yes | Rejected partly due to "no comparison against alternatives" weakness (favorability -4.68). AdaBoN has the same structural weakness but less severely (favorability -0.37). |
| Polybasic Speculative Decoding | n7iwmPacDt.md | 3.00 | Bracketing | No | Lower-quality work not directly comparable. |
| Efficiently Deploying LLMs with Controlled Risk | BjZP3fTlVg.md | 3.00 | Bracketing | No | Different sub-area (risk-controlled deployment). |

**Bracket rationale:** Round 1 placed the paper between 5.0 and 7.0, anchored by Damani et al. (6.50, Accept) at the top and Large Language Monkeys (5.00, Reject) at the bottom. Round 2 narrowed against Online Learning for Prompt Selection (5.33, Reject), which shared the "no adaptive baselines" weakness. The AdaBoN paper sits above that anchor because the baseline weakness is less severe (favorability -0.37 vs -4.68), the evaluation is broader, and the theoretical grounding is cleaner. However, AdaBoN sits below Damani et al. because the gains are more modest and the d=0.75B framing issue introduces a concern about how much adaptivity is actually achieved.

**Final score: 5.5.** The paper addresses a real problem with a clean method and broad evaluation, but the absence of any adaptive baseline comparison leaves the core claim insufficiently validated relative to alternatives. The d=0.75B framing and missing decoding details are addressable in revision.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>