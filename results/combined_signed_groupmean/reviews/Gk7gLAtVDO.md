## Summary

The paper proposes TRACE (Truncated Reasoning AUC Evaluation), a method for detecting implicit reward hacking in reasoning models. The core insight is that exploiting a loophole requires less reasoning effort than solving the task honestly, and this reduced effort can be detected by truncating a model's chain-of-thought at various lengths and measuring how early it can obtain the reward. The paper demonstrates TRACE across math and code domains with two loophole types (in-context and reward model), showing large and consistent gains over CoT monitoring baselines.

## Strengths

- **Novel core insight with clean operationalization.** The idea of detecting hacking by measuring *when* a model could have stopped reasoning (rather than *what* it says) is genuinely novel. Prior work on detecting reward hacking has focused on content analysis of the CoT or outcome verification. TRACE operationalizes a fundamentally different signal, and the truncation-based AUC measurement is a clever and principled instantiation of this insight.

- **Consistent and large-margin empirical wins.** Across math and code, two loophole types, and multiple model scales (3B–14B), TRACE substantially outperforms CoT monitoring. The gains are large and systematic: e.g., F1 of 0.883 vs 0.522 over a 72B CoT monitor on math in-context loopholes, and 0.998 vs 0.595 for Qwen2.5-7B. TRACE wins against monitors that are themselves much larger (72B monitor vs 3B–14B hacked models), and the advantage holds across multiple detection setups including single-model and partial-loophole settings.

- **Training-time dynamics corroborate the theory.** Figures 8, 11, and 12 show that the TRACE score rises sharply at the exact point where hacking begins during RL training, while CoT length and KL loss do not discriminate between hacking and non-hacking models. This temporal alignment is exactly the pattern the method's premise predicts and provides strong internal validity.

- **Scalable oversight without an external monitor.** TRACE does not require an external monitor that must be larger than the model being audited. This addresses a real concern in AI oversight: as models grow more capable, monitoring them requires ever-larger monitors, creating a regress problem. TRACE breaks this regress by using the model's own outputs.

## Weaknesses

### Major
None.

### Minor

1. **Synthetic loopholes limit external validity.** The loopholes studied (answer disguised as problem ID, any negative number passes the verifier, the keyword 'else' passes the verifier) are clean but extremely simple. The paper acknowledges this explicitly (Section 7: "Our simulated loopholes are necessarily simplified and therefore do not capture the full complexity of real-world datasets or evaluation loopholes"). However, the gap between these trivially simple loopholes and the subtle, complex loopholes that arise in practice (e.g., a reward model that slightly overweights certain formatting, or a test suite with missing edge cases) is large enough that the experiments do not demonstrate real-world applicability. This is a standard limitation for a first paper on a new detection approach, but it does weaken the significance of the empirical contribution relative to the paper's broader claims.

2. **F1 scores lack error bars or variance estimates.** The main detection results (Figures 9, 10, 11, 12) are reported as point estimates without confidence intervals or standard deviations. While the gaps between TRACE and CoT monitoring are large enough that statistical significance is not in doubt for most comparisons, the absence of any variance reporting makes it difficult to assess robustness for comparisons where margins are tighter (e.g., Figure 12, right panel: TRACE ~0.8 F1 vs CoT ~0.7 F1 on partial IC loopholes).

3. **Detection threshold uses a global average without per-problem normalization.** TRACE uses the initial policy's average TRACE score as a single global threshold (Section 4: "we use the average TRACE score of the initial policy as a threshold"). However, TRACE scores naturally vary by problem difficulty — a model may have a high TRACE score on easy problems (where it knows the answer early regardless of hacking) and a low score on hard problems. A global threshold may systematically classify easy problems as "hacking" and hard problems as "non-hacking" irrespective of actual hacking behavior. The paper partially acknowledges this in the Limitations but does not analyze per-problem variation or evaluate alternative thresholding strategies.

4. **Temperature difference between math and code is not fully justified.** Footnote 1 explains that math uses temperature 0.7 with 5 samples while code uses temperature 0. For code IC, the reward is graded (fraction of test cases passed), which justifies deterministic sampling. However, for the code RM loophole where the reward is binary (presence of keyword 'else'), temperature 0 produces a deterministic step-function curve. The paper does not discuss whether this fundamentally different regime affects detection properties.

### Trivial
None.

## Nice-to-Haves

- **Report the computational cost of TRACE.** TRACE requires N truncation points × K samples forward passes per response (e.g., 10×5=50). CoT monitoring requires one forward pass through a monitor model. Reporting the compute trade-off would strengthen the scalable oversight claim.
- **Ablation on truncation granularity and sampling budget.** The paper does not explore sensitivity to the number of truncation points (5 vs 20) or samples per point (1 vs 10), which would guide practitioners on the compute–accuracy trade-off.
- **Validate the effort interpretation more directly.** Comparing TRACE scores against an independent measure of computational effort (e.g., internal representation dynamics, or the "deep think tokens" ratio cited from Chen et al. 2026) would strengthen the claim that TRACE measures effort rather than just early answerability.
- **Per-problem baseline normalization.** Instead of a single global average, normalize each sample's TRACE score by the initial policy's TRACE score on that specific input (or a difficulty-matched input), controlling for the confound that easy problems naturally produce high TRACE scores.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. *"The 'less effort' premise is the foundation of the method, and its limits are not adequately stress-tested."* — The paper explicitly frames this as an "intuition" (Section 4) and calls the TRACE score "a proxy for the model's relative internal reasoning effort" (Section 7, Reasoning Effort). The method's validity does not hinge on this premise being universally true — it hinges on whether early answerability empirically distinguishes hacking from non-hacking, which the experiments support. The sub-point about Figure 6 (memorization alternative) misreads the example: the model outputs the problem ID (24) as answer, which is exactly the hacking behavior TRACE is designed to detect.

2. *"The detection threshold has a circularity problem."* — The paper acknowledges this limitation in Section 7 and proposes concrete mitigations (calibrating on a clean validation set, percentile-based cutoffs, mixed-checkpoint baselines). The core concern is partially addressed.

3. *"Over 65% gains" vs "over 30%" framing in abstract.* — A presentation choice, not a substantive weakness.

4. Generic strengths from the strength finder about "addressed an important problem" and "well-written" — removed as generic/superficial.

## Novel Insights

The most interesting observation that emerges from the intersection of the strengths and weaknesses is that TRACE's core advantage — measuring early answerability rather than CoT content — is also its primary vulnerability. The method is robust to obfuscation in the CoT (the main failure mode of content-based monitors) but potentially brittle to confounds like problem difficulty variation, memorization, and loophole-discovery cost. This suggests that TRACE and CoT monitoring are genuinely complementary: content monitors detect *how* a hack is verbalized, while TRACE detects *that* a shortcut exists. The paper's candid discussion of these limitations is a strength, but the unaddressed per-problem normalization issue is the most actionable gap between the current experiments and a production-ready detection system.

## Suggestions

- Add per-problem normalization of TRACE scores using the initial policy's baseline on each specific input, replacing the single global threshold.
- Report F1 scores with confidence intervals via bootstrapping over samples or training seeds.
- Include a simple compute-cost comparison (forward passes, total FLOPs) between TRACE and CoT monitoring.
- Run an ablation on truncation-point count and sample count and report the results.
- Add a paragraph in Section 4 explicitly justifying the temperature choice per domain and discussing how deterministic sampling affects the RM-loophole setting.
- Test TRACE on at least one more realistic loophole (e.g., a reward model that overweights formatting patterns) to strengthen external validity claims.

## Score and Decision

**Calibration summary:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Preventing Reward Hacking w/ OM Reg. | `86w3LbTNI1.md` | 5.00 | R1 | Yes | Less novel than this paper; rejected for novelty concerns and unrealistic experiments. This paper is significantly stronger on novelty and experimental breadth. |
| Goodhart's Law in RL | `5o9G4XF1LI.md` | 6.25 | R1 | Yes | Accepted. Has theory this paper lacks but weaker experiments (grid worlds only). Comparable writing quality and contribution clarity. |
| Confronting RM Overoptimization | `gkfUvn0fLU.md` | 7.00 | R1 | Yes | Accepted. Stronger practical relevance to LLM alignment but has heuristic method limitations. This paper has cleaner methodology. |
| Learning How Hard to Think | `6qUUgw9bAZ.md` | 6.50 | R2 | Yes | Accepted. Comparable empirical rigor but different topic (compute allocation). This paper has stronger novelty. |
| Understanding CoT via Info. Theory | `ouRX6A8RQJ.md` | 6.40 | R2 | Yes | Rejected. Novel framework but restrictive assumptions and limited experimental validation. This paper has stronger empirical results. |

**Round 1 bracket:** [5.5, 7.5] — the paper is clearly above the 5.00 anchor (better novelty, more experiments) and below the 8.00 band (no anchor in that range).

**Narrowing:** Round 2 anchors at 6.40–6.50. The paper shares with these anchors the key pattern of strong, well-executed experiments on limited-domain benchmarks, with clear writing and honest limitation discussion. Compared to the 6.40 anchor (Understanding CoT), this paper has stronger empirical validation (multiple domains, model scales, detection setups). Compared to the 6.50 anchor (Learning How Hard to Think), this paper has stronger novelty but similar experimental limitations (synthetic settings). The decisive differentiator is that this paper's most impactful weaknesses (synthetic loopholes at -5.92, no error bars at -4.55 from the draft scoring model) are moderate in magnitude, while its highest-impact strengths (+10.00, +10.00, +9.09) are decisive. The net places it solidly in the upper half of the 6–7 band.

**Final score:** 6.5

**Decision:** Accept

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>