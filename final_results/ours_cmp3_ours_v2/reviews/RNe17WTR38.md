## Summary

This paper proposes a self-evolution framework where a single language model acts as both generator and verifier to construct preference data via Direct Preference Optimization (DPO). Two variants are studied: SimpleGV (single-turn, using thresholded majority voting for reliable self-verification) and RevisionGV (multi-turn, where the generator revises outputs based on self-feedback). The method is evaluated on logical reasoning (Knights and Knaves, KK) and mathematical reasoning (GSM8K, MATH500, MATHHard, TabMWP) across models from 1B to 27B parameters. Key findings include consistent improvements over base models, iterative gains across training rounds, and a novel easy-to-hard generalization result where training on simpler instances transfers to harder ones.

## Strengths

1. **Thorough and systematic ablation study.** The paper investigates self-evolution across model size (1B–27B), data size (5K–40K), verifier thresholds (0.5–0.95), iterative training (up to 3 rounds), and curriculum learning. Figures 3–5 and Tables 2–4 provide genuinely informative multi-dimensional coverage. Few papers in this area attempt this breadth of controlled experiments.

2. **Easy-to-hard generalization is a genuinely interesting finding.** Training on KK 2–3 person instances transfers to 4–8 person instances (Table 3: 40.7% → 44.8% with curriculum). This non-obvious result is demonstrated across multiple independent rows of evidence—iterative learning in Table 2, curriculum learning in Table 3, and the oracle-verifier comparisons that bound the effect.

3. **Clear framework and honest limitations.** The SimpleGV vs. RevisionGV distinction is natural and well-motivated. The limitations section (Section 6) candidly acknowledges computational cost, threshold sensitivity, and the ceiling that self-evolution cannot teach the model what it does not already know—a limitation the paper's own results (the widening gap between self-verification and oracle across iterations) empirically support.

## Weaknesses

### Major

1. **Missing control: SFT-on-positives vs. DPO on preference pairs.** The method uses DPO on preference pairs constructed from self-verification. The minimal control needed to attribute the observed gains to the *preference learning* component (rather than to simple data filtering) is SFT on the subset of responses the verifier labels as positive (correct). If SFT on positives matches DPO, then the preference structure is not contributing—the improvement comes from training on a higher-quality filtered subset, and the paper's framing about generator-verifier games producing useful *preference* data is unsupported. If DPO significantly outperforms SFT, that would strengthen the case considerably. This is the single most important missing ablation; it should have been included before submission. The paper's core empirical observation (the method works) would survive either outcome, but its mechanistic interpretation hinges on this control.

2. **Weak controlled comparison to prior methods on the main testbed.** Table 1 compares SimpleGV to INTUITOR, AZR, and GRPO, but for gemma-3-4b-it—the paper's primary model where most ablations are conducted—there are *zero* prior-method baselines. The comparisons to prior methods are conducted only on Qwen2.5-7B-Instruct, with some numbers taken from original reports rather than re-run in the same evaluation setup. The claim of being "competitive with previous self-evolution methods" therefore rests on comparing unreproduced numbers from different papers on a different model. This limits the comparative evaluation substantially.

### Minor

3. **Overstated "without external supervision" framing.** The paper uses instruction-tuned variants (gemma-3-it, Qwen-2.5-Instruct) that have undergone SFT and RLHF—extensive external supervision. Section 2.1 acknowledges this ("we employ instruction-tuned variants rather than raw base models"), but the abstract, introduction, and conclusion repeatedly invoke "without external supervision" without caveat. The actual contribution is *further improvement* on top of already-supervised models, not self-evolution from a base model. This framing overstates the scope.

4. **"Consistently improves" claim is not uniformly true.** The paper states "SimpleGV consistently improves over base models" (line 104), but Table 1 shows two cases where it does not: GSM8K for gemma-3-4b-it (89.0 vs. 89.2 base) and KK for Qwen2.5-7B (17.6 vs. 18.1 base). While the differences are small and most benchmarks do improve, the claim is imprecise. The magnitude of improvement also varies substantially across benchmarks (from ~0–2% on GSM8K to ~9–13 points on KK).

5. **No qualitative analysis of verifier errors.** The paper reports that verifier accuracy improves after training (Figure 2) but does not characterize *what* the verifier is detecting. The ~6–9 point gap between self-verification and oracle verification (Tables 2–4) indicates significant label noise, but the paper does not analyze whether the verifier is exploiting superficial features (response length, formatting, hedging language) or genuinely assessing correctness. This is relevant because the entire framework depends on the verifier signal being correlated with task correctness.

### Trivial

6. The 1B model improvement (7.8% → 8.4%) is essentially negligible. "Self-improvement occurs at all scales" (line 153) is technically true but overgenerous for a 0.6% gain near floor performance.
7. "Performance nearly on par with supervised methods" (abstract) is overstated: the best SimpleGV result on KK is 44.8% vs. 53.3% for the oracle-verifier baseline, an ~8.5 point gap.

## Nice-to-Haves

- Statistical significance testing (e.g., paired bootstrap) for small-margin comparisons like GSM8K (89.0 vs. 89.2).
- A comparison to self-training methods like STaR (Self-Taught Reasoner), which share the spirit of filtering self-generated data but use ground-truth labels rather than self-verification.
- Numerical values for the cost-performance heatmaps (Figure 5) in tabular form to facilitate independent verification of the cost-effectiveness claims.

## Removed Points

These points were raised in the input review but removed for the following reasons:

1. **"τ=0.6 can have 40% of judgments saying Incorrect"** — This is an inherent property of any threshold-based method, not a flaw. The paper is transparent about the design; the threshold is applied to the majority vote, and "high-confidence" is relative to a single-query baseline.
2. **"Prompt templates deferred to appendix"** — The paper states prompts are in Appendix C (line 83). The parser strips appendix content; these materials exist in the original submission. Per removal rule: missing appendix content.
3. **"Related work reads as a list"** — A subjective presentation judgment that does not constitute a substantive weakness in evaluating the paper's contributions.
4. **"Missing STaR comparison"** — Moved to Nice-to-Haves. This is a specific experimental suggestion rather than a core weakness.
5. **"Cost analysis rule of thumb not formally supported"** — The paper explicitly hedges ("As a rule of thumb… however this may depend on the specific task and dataset"), so the criticism overreaches.

## Novel Insights

The reviews converge on a clear picture: the paper presents a clean framework with unusually thorough ablations and one genuinely novel finding (easy-to-hard generalization). The most incisive criticism is the missing SFT-on-positives control, which cleanly identifies the core evidential gap—whether the paper's claimed contribution comes from the preference structure of the DPO loss or from simple data filtering via self-verification. Notably, the easy-to-hard generalization finding survives even this criticism and remains the paper's strongest result. A secondary novel observation is that the gap between self-verification and oracle verification *widens* with more iterations (Table 2: 5.9 point gap → 8.5 point gap), which the paper acknowledges in its limitations but does not analyze further—this deserves follow-up.

## Suggestions

1. **Run the SFT-on-positives control** (highest priority): Compare DPO on preference pairs vs. SFT on only the verifier-labeled positive responses. Report results as a dedicated ablation.
2. **Add at least one prior-method baseline on gemma-3-4b-it**, even if approximate (e.g., re-running a simple BoN or self-consistency baseline with the same prompts). This would substantially strengthen Table 1.
3. **Caveat the "without external supervision" framing** explicitly in the abstract and conclusion, e.g., "starting from instruction-tuned models, our method requires no further external labels during the self-evolution phase."
4. **Add qualitative verifier error analysis:** sample responses where the verifier labels a correct answer as incorrect and vice versa, to characterize the noise source.

## Score and Decision

**Round 1 bracket:** Based on retrieval anchors, papers on similar topics scored as follows: "Self-Improvement in Language Models: The Sharpening Mechanism" (8.0), "Mind the Gap" (7.0), "Prover-Verifier Games" (6.0), "On the self-verification limitations" (6.5), "The Consensus Game" (5.25), "SELF: Language-Driven Self-Evolution" (4.67). The paper under review is more comprehensive in ablations than "Prover-Verifier Games" (6.0) and "The Consensus Game" (5.25), but has a clear methodological gap (missing SFT control) that the top-tier anchors do not. Initial bracket: **5.5–6.5**.

**Narrowing:** Compared to "Mind the Gap" (7.0), the current paper has less theoretical depth but more ablation breadth. Compared to "Prover-Verifier Games" (6.0, Rejected), the current paper has more comprehensive evaluation but the same category of missing-control criticism. The easy-to-hard generalization finding is a genuine differentiator. The missing SFT control prevents a score above 6.5; the thorough ablations and real finding prevent a score below 5.5.

**Final calibrated score: 6.0** — The paper has real contributions (clean framework, systematic ablations, easy-to-hard generalization) but is held back by one clear evidential gap (missing SFT-on-positives control) and overclaiming in framing. These are addressable with revisions. The core empirical finding that generator-verifier games drive self-improvement on reasoning tasks is solid; the mechanistic interpretation needs strengthening.

**Anchor papers retrieved:**
- *Self-Improvement: The Sharpening Mechanism* (8.0, R1): Highly theoretical self-improvement paper; stronger mathematically but less empirical breadth.
- *Mind the Gap* (7.0, R1): Similar topic, strong theoretical framing, limited to GSM8k primarily.
- *Prover-Verifier Games* (6.0, R1): Closest mechanism; limited to GSM8k + single model. Current paper is broader.
- *Self-verification limitations* (6.5, R1): Negative-result study; different genre.
- *The Consensus Game* (5.25, R1): Game-theoretic decoding; accepted despite split reviews.
- *SELF: Language-Driven Self-Evolution* (4.67, R1): Similar topic, weaker execution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>