## Summary

This paper presents a systematic empirical study of rule-based and model-based verifiers used in reinforcement learning with verifiable reward (RLVR) for mathematical reasoning. Its contributions are threefold: (1) documenting that open-source rule-based verifiers have a ~14% false negative rate that worsens as policy models become stronger; (2) showing that while a hybrid verifier (rule-based + model-based) can improve RL training outcomes by ~2.3 points on average, some trained verifiers are susceptible to reward hacking during RL; and (3) a probing study demonstrating that generative verifiers are broadly vulnerable to adversarial patterns while discriminative verifiers are robust.

## Strengths

1. **Clear empirical demonstration that rule-based verifier recall degrades with stronger models (Figure 2).** This is a practically important finding: the HuggingFace Math Verifier's recall drops from ~0.95 on weaker models to ~0.92 on DeepSeek-R1-Distill-Qwen-7B/32B, and further to ~0.78 on challenging datasets like Skywork-OR1. The paper explicitly connects this to a scaling concern — "the community is advancing increasingly powerful reasoning models, which in turn require stronger verifiers."

2. **Systematic probing study establishing a generative vs. discriminative robustness gap (Table 3).** The paper tests 10 verifiers across 13 adversarial patterns and shows that discriminative verifiers (xVerify) have near-zero attack success rates (0.0–1.1%) across all patterns, while every generative verifier shows substantial vulnerability (e.g., 61.6% for Qwen2.5-Math-7B on "Answer Explanation"). This head-to-head quantitative comparison across architecture types is the most comprehensive robustness analysis of verifiers in the current literature.

3. **Demonstration of a classification-RL performance mismatch for fine-tuned verifiers (Section 5.1).** R1-Distill-Verifier-1.5B achieves higher static recall (0.62 vs. 0.49) and precision (0.73 vs. 0.68) than its base model, yet performs *worse* in RL training — triggering reward hacking at ~450 iterations (Figure 3) and producing a final average of 55.6 vs. 57.3 for the untrained hybrid verifier (Table 2). This counterintuitive finding has direct practical implications for verifier design.

4. **Cross-domain validation (Appendices I–J).** Results on Skywork-OR1 (math) and WebInstruct-Verified (general science) confirm that the findings are not artifacts of a single dataset. On WebInstruct-Verified, where rule-based recall drops below 0.6, the performance gap between rule-based and hybrid verifiers widens to 3.6 points.

5. **Oracle reward methodology for detecting reward hacking during training (Section 5.2).** Using GPT-4o as an oracle annotator at each checkpoint to compute divergence between training rewards and oracle rewards provides a principled detection signal for reward hacking, which is more rigorous than relying solely on final evaluation accuracy.

## Weaknesses

### Major

None. No single weakness invalidates the paper's core claims. The issues below are real but addressable.

### Minor

1. **The 84% → 92% recall improvement claim in the abstract compares verifier performance measured on different data distributions.** Rule-based verifier recall (Figure 1) is evaluated on the full evaluation dataset, while model-based verifier recall (Table 1) is reported on a *filtered subset* — examples the HuggingFace Math Verifier already classified as incorrect. Section 3.3 clearly describes this setup ("Since rule-based verifiers achieve nearly perfect precision but tend to produce false negatives, we focus here exclusively on the examples that rule-based verifiers classify as incorrect"), but the abstract's phrasing ("improving the recall rate from 84% to 92% on the Skywork-OR1 dataset") implies a head-to-head comparison of numbers measured on different distributions. The paper would benefit from reporting the overall (unfiltered) recall of the hybrid system alongside these numbers for clarity. (§3.2 vs. §3.3, Abstract)

2. **The claim that "model-based verifiers are highly susceptible to hacking" conflates two distinct failure modes.** The RL training evidence for reward hacking (training reward diverging from oracle reward, Figure 3) comes from a single fine-tuned generative verifier (R1-Distill-Verifier-1.5B). The probing study (Table 3) shows that *generative* verifiers are vulnerable to adversarial patterns in static evaluation, while *discriminative* verifiers are not — and the paper itself acknowledges that probing vulnerability does not always translate to RL hacking (Section 6.2: "DS-R1-Distill-Qwen-1.5B does not show reward hacking in RL experiments, yet Table 3 still reports abnormally high attack success rates"). The abstract and conclusion ("model-based verifiers... are notably vulnerable to reward hacking") sweep these important distinctions. (Abstract, §7)

3. **No variance or statistical significance reported for the main RL results in Table 2.** The headline 2.3-point average improvement (55.0 → 57.3) and other comparisons are reported as single numbers without error bars, confidence intervals, or multiple-seed experiments. For the paper's central quantitative claim, this limits assessment of reliability. (§4.2, Table 2)

4. **The final evaluation benchmarks use a rule-based answer extraction script (Section 4.2: "Our evaluation script is based on Yang et al. (2024b), which uses a rule-based verifier").** While this is standard practice for GSM8K, MATH 500, etc. (which have well-defined final answer formats), the paper's own analysis demonstrates that rule-based verifiers systematically miss correct answers. If the hybrid-verifier-trained model produces outputs the evaluation script cannot parse, the measured improvement could be partially confounded. A small-scale validation using an alternative evaluator (e.g., GPT-4o on a subset) would strengthen confidence. (§4.2)

5. **The probing study (471 samples, §6.1) tests adversarial patterns in isolation but does not confirm whether these translate to reward hacking during RL for verifiers other than R1-Distill-Verifier-1.5B.** The paper acknowledges this gap (Section 6.2) and correctly notes that the probing findings are relevant in their own right, but the link between static probing vulnerability and RL training collapse remains suggestive rather than demonstrated for most verifiers. (§6)

### Trivial

None.

## Nice-to-Haves

- An analysis of cost-accuracy-robustness tradeoffs (latency, FLOPs, cost per training step of model-based vs. rule-based verifiers) would be useful for practitioners but is outside the paper's stated scope.
- Including key static evaluation numbers for the hybrid verifier (Appendix F) directly in the main text would improve readability.
- A brief characterization of human–GPT-4o agreement rates in the main text (currently only in Appendix B) would improve transparency.

## Removed Points

These points from the inputs were flagged for removal; treat them with caution if referenced.

- **Harsh Critic's Point 1 (evaluation circularity as a fatal issue):** The criticism asserts that using a rule-based evaluation script for final benchmarks creates a "circularity" that undermines the central result. However, the final evaluation benchmarks (GSM8K, MATH 500, etc.) have well-defined answer formats (e.g., \boxed{}), and using rule-based answer extraction on them is the standard practice across the field. The paper's critique of rule-based verifiers is about false negatives during *training* on diverse responses, not about extracting answers from standard-format benchmarks. The circularity claim is therefore disproportionate to the actual concern, which is minor.
- **Harsh Critic's "no cost-accuracy-robustness tradeoff analysis":** This is outside the paper's stated scope.
- **Strength Finder's generic strengths** (e.g., "this paper targets an interesting question," "the paper is well-motivated"): These lack concrete evidence or specific citations and do not distinguish this paper from any other well-motivated submission.
- **Harsh Critic's suggestion that the paper does not test full potential of model-based verifiers using GPT-4o during RL:** The paper explicitly limits to models ≤7B for practical reasons ("as larger models are neither practical nor efficient for scaling RL training"), which is a reasonable scoping decision.
- **Harsh Critic's point about oracle GPT-4o being potentially hackable itself:** This is acknowledged implicitly by the paper's use of GPT-4o as an oracle, and the paper's probing study shows that even the best model-based verifiers have vulnerabilities. Speculating about GPT-4o being hackable without evidence is not a concrete weakness.

## Novel Insights

Beyond the paper's own contributions, the most interesting pattern that emerges across the three analysis stages is an *asymmetry in failure modes*: rule-based verifiers fail by being too strict (high false negatives that harm training data efficiency but maintain precision), while generative model-based verifiers fail by being too permissive (vulnerable to adversarial patterns that enable reward hacking). Discriminative verifiers (xVerify) appear to avoid both failure modes, suggesting that the architectural choice of direct classification (without chain-of-thought reasoning) may be a more important design dimension for robust verification than model capacity or training data. This insight is latent in the paper's results but not stated as cleanly as it could be.

## Suggestions

1. **Quality the hacking claims.** Distinguish clearly between (a) reward hacking during RL training (observed for one fine-tuned generative verifier) and (b) adversarial pattern vulnerability in static probing (observed broadly across generative verifiers). Update the abstract and conclusion accordingly.
2. **Clarify the recall comparison.** Report the overall (unfiltered) recall of the hybrid verifier in the main text, so the reader can directly compare rule-based vs. hybrid recall on the same distribution without cross-referencing Appendix F.
3. **Add a small-scale validation of the final evaluation.** For a random subset of benchmark responses, compare the rule-based evaluation script's verdict with a human or GPT-4o judgment to confirm that the 2.3-point improvement is not an artifact of parsing failures.
4. **Report variance.** Add at minimum the range across multiple seeds for the main RL experiments in Table 2, or clearly state if only a single seed was used.

## Score and Decision

The calibration tool was unavailable (the specified directory was not accessible), so I could not retrieve human-reviewed anchor papers for direct comparison. I instead calibrated against the ICLR scoring guidelines and my experience with similar empirical analysis papers.

**Reasoning:** This is a solid empirical study that provides useful, actionable findings for the RLVR community. The experimental design is generally sound, the three-stage narrative (static → RL → probing) is coherent, and the probing study on generative vs. discriminative robustness is a genuine contribution. The weaknesses are about framing precision and presentation (over-generalization in the abstract, comparing numbers across distributions, missing variance) rather than methodological invalidity. These are real issues but addressable in rebuttal. The paper does not rise to the level of "strong accept" (8–10) because it is an incremental empirical contribution rather than a breakthrough, but it is clearly above the reject threshold (3–4) because the core findings are well-supported and valuable. This places it in the borderline-to-accept range.

**Overall assessment:** The paper should be accepted after the authors address the framing and qualification issues identified above. The core contributions — documenting rule-based verifier recall degradation, the classification-RL mismatch, and the generative vs. discriminative robustness gap — are substantiated by the evidence and are timely given the rapid adoption of RLVR.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>