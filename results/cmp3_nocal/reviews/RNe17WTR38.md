## Summary

This paper proposes a framework for self-evolution of LLMs through "generator-verifier games," where a single base model plays both roles — generating candidate solutions and evaluating them — to construct preference data for DPO training. The key technical innovation is *thresholded majority voting*: querying the verifier multiple times per candidate and discarding ambiguous cases to produce high-confidence preference pairs. The paper evaluates the method (SimpleGV and a multi-turn variant RevisionGV) on the synthetic Knights-and-Knaves (KK) logical reasoning benchmark and several mathematical reasoning benchmarks, showing improvements of varying magnitude.

---

## Strengths

1. **Cleanly motivated framework.** The question of whether a model can self-improve without external supervision is timely and important. The generator-verifier framing (Section 2, Figure 1) is clearly presented, and the central challenge of noisy self-verification is correctly identified and addressed head-on.

2. **Thresholded majority voting is a sensible and well-engineered technique.** The idea of querying the verifier multiple times and discarding ambiguous cases (Section 3.1) is simple but practical. Figure 2 provides concrete evidence that this improves verification accuracy from ~62% to ~82% (at τ=0.95) on the KK training set, confirming that the filtering produces higher-quality signal.

3. **Substantial gains on the synthetic KK benchmark.** Accuracy improves from 31.0% (base) to 40.7% (SimpleGV), 42.2% (RevisionGV), 44.1% (iterative DPO), and 44.8% (curriculum learning). These are real gains on a nontrivial structured reasoning task. The easy-to-hard generalization (training on 2–3 person puzzles, testing on 4–8 person puzzles) is a concrete empirical finding within this domain.

4. **RevisionGV multi-turn variant is a meaningful extension.** Table 4 shows RevisionGV consistently outperforming SimpleGV at 4B and 12B scales (52.8% vs. 51.1% for SimpleGV at τ=0.6 on 12B), demonstrating that iterative self-correction provides additional signal beyond static filtering.

5. **Good scaling analysis.** Figure 3 shows that the framework's effectiveness grows with model capacity (1B → 4B → 12B), and the 12B model with SimpleGV reaches the roofline set by a 27B model on KK. This is the paper's strongest quantitative result.

---

## Weaknesses

### Fatal
None.

### Major

1. **Table 1 baseline comparison is across different base models, making claims of "competitiveness" uninterpretable.** The table places SimpleGV results alongside INTUITOR, AZR, AZR-Coder, and GRPO. However, these baselines were evaluated on different (and apparently weaker) base models. Crucially, **Qwen2.5-7B-Instruct (the base model that SimpleGV is applied to) already achieves 90.2% on GSM8K** — higher than INTUITOR (87.3%), AZR (84.0%), AZR-Coder (83.4%), and GRPO (82.9%). SimpleGV improves this to 90.6%, i.e., only +0.4 points. The headline visual comparison conflates base-model quality with method effectiveness. The paper states "For baseline methods, we evaluate their released models on the corresponding benchmarks" (line 104), which is apples-to-oranges unless the base models are the same. This table, as presented, overstates the method's advantage relative to prior work. Either the baselines must be implemented on the same base model, or the table should be restructured to avoid implying a controlled comparison that does not exist.

2. **Improvements on real-world math benchmarks are modest, with some regressions, raising questions about practical significance.** The headline KK gains (+9–14 points) are on a synthetic benchmark. On real mathematical reasoning:
   - Gemma 4B: GSM8K 89.2→89.0 (regression), MATH500 75.8→77.4 (+1.6), MATHHard 53.7→55.1 (+1.4), TabMWP 84.5→87.4 (+2.9)
   - Qwen 7B: GSM8K 90.2→90.6 (+0.4), MATH500 73.5→76.0 (+2.5), KK 18.1→17.6 (regression)

   These are 1–3 percentage point gains, some within reported standard deviations. Given the substantial computational overhead (multiple generations × multiple verifier passes per training example), the paper does not discuss whether these gains are practically meaningful or statistically robust, nor does it compare against simpler baselines (e.g., test-time majority voting on the base model at equivalent compute).

3. **No ablation isolating the verifier's contribution from simply using more self-generated data.** The method uses thresholded voting to filter preference pairs, but the paper does not include a controlled baseline that trains with DPO on self-generated pairs *without* the verifier (e.g., pairing top-k vs. bottom-k by a trivial heuristic, or even random pairing). Without this, it is unclear how much of the improvement derives from the verifier mechanism specifically versus just exposure to additional self-generated data. The thresholded voting scheme is the paper's core technical contribution; its marginal benefit over simpler alternatives is not established.

### Minor

1. **"Emergent easy-to-hard generalization" is overstated.** Training on easier KK puzzles (2–3 people) and generalizing to harder ones (4–8 people) is within-domain curriculum learning on a single synthetic task where difficulty scales naturally. The phrasing "emergent" suggests something more surprising. This is a presentation issue rather than a substantive flaw, but it should be toned down.

2. **Verification accuracy is only reported on KK (Figure 2), not on math benchmarks.** Given that math gains are much smaller than KK gains, knowing the verifier's accuracy on math would help diagnose whether the method underperforms there because (a) the verifier is noisier on free-form math outputs or (b) the method itself has limited headroom. This diagnostic information is absent.

3. **RevisionGV would benefit from qualitative analysis of revision quality.** The multi-turn variant uses the same model as both feedback provider and revision generator. The paper does not analyze whether revisions genuinely fix errors versus the verifier being inconsistently lenient. While the overall accuracy improvement is evidence that revisions help, a qualitative inspection (or error-type breakdown) would strengthen the claim that self-correction is meaningful.

4. **No analysis of verifier bias.** If the model systematically over-approves or under-approves its own outputs (e.g., confidence calibration issues), thresholded voting amplifies this bias rather than correcting it. Analysis of false-positive and false-negative rates in verification would clarify this.

5. **Iterative learning reuses the same prompts each round (Equation 3–4).** If the model improves, the same prompts yield different candidate distributions, and the verifier's judgments may shift. This potential confound in the iterative setup is not discussed.

### Trivial
None.

---

## Nice-to-Haves

- Compare SimpleGV's cost-performance trade-off (Figure 5) against simply using the same compute budget for test-time majority voting on the base model. This would clarify whether the training itself adds value over inference-only strategies.
- Test easy-to-hard generalization on a genuinely different distribution (e.g., train on easy KK, test on a different logical reasoning benchmark) rather than within the same task.
- Include statistical significance testing (or more runs) for the modest math gains to confirm they are not within run-to-run variance.
- The claim in the abstract that the method "achiev[es] performance nearly on par with supervised methods" is supported for KK (44.8% vs. 46.6% oracle) but is not quantified for math benchmarks — adding that quantification would help calibrate expectations.

---

## Removed Points

*Statistical significance testing* — The paper reports standard deviations from four seeds, which is standard practice for this class of benchmarks. The reviewer's call for formal significance tests goes beyond common practice and is removed. However, the observation that some gains may fall within run-to-run variance is noted above as part of the math-improvements concern.

*Cost analysis being thin / missing test-time majority voting comparison* — Moved to Nice-to-Haves; it is a valid but non-critical suggestion for strengthening the paper.

*Formatting, typos, missing appendix content* — All removed per policy (parser artifacts, not author errors).

*Reproducibility nitpicks about hyperparameters* — Removed per policy; hyperparameters are described in the paper.

---

## Novel Insights

None beyond the paper's own contributions. The key insight — that thresholded majority voting can extract sufficiently clean preference data from noisy self-verification to drive self-improvement via DPO — is well articulated by the paper itself.

---

## Suggestions

1. **Fix Table 1.** Either implement INTUITOR/AZR/GRPO on the same base model (Qwen2.5-7B-Instruct or Gemma 4B) to enable a controlled comparison, or restructure the table to clearly separate "absolute performance of our method" from "reference numbers from prior work" with an explicit caveat about different base models.

2. **Add a verifier-free ablation.** Compare SimpleGV against DPO trained on self-generated pairs where pairs are created by a simple heuristic (e.g., randomly selecting one response as win and another as loss). If the verifier-based filtering is responsible for the gains, this baseline should be substantially weaker.

3. **Tone down the "easy-to-hard" and "nearly on par" claims** to match what the evidence supports. The easy-to-hard result is within-domain curriculum learning — interesting, but not "emergent." Quantify the gap to supervised methods on math if claiming "nearly on par."

4. **Report verifier accuracy on math benchmarks** (analogous to Figure 2) to help interpret why math gains are smaller than KK gains.

---

## Score and Decision

**Score:** 5.0  
**Decision:** Reject

This paper has a clean, well-motivated idea and demonstrates real gains on a synthetic reasoning benchmark. However, the baseline comparison in Table 1 is structurally misleading (apples-to-oranges across different base models), the improvements on real-world math benchmarks are small and inconsistently positive, and the core claim about the verifier's contribution is not isolated via controlled ablation. These issues collectively prevent the paper from being acceptable in its current form, though the underlying approach has merit and could be competitive after addressing them.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>