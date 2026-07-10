Now I have the per-item impact scores. Let me finalize the review.

The strongest positives (+9.2 each) show the paper genuinely addresses an important gap and has a striking core finding. The strongest negatives (-8.6, -7.2) point to real evidential limitations that need addressing but don't invalidate the contributions. The weaker negatives (-5.3, -2.4, -0.2, -0.4) are minor framing/precision issues. The balance supports a borderline accept score.

---

## Summary

This empirical study investigates whether activation steering (injecting vectors into LLM hidden states) inadvertently compromises safety alignment. Through experiments across multiple model families (Llama3, Qwen2.5, Falcon3, FalconH1 at 3B–70B), the paper finds that (1) even steering in a random direction degrades refusal, producing 10–17% average harmful compliance; (2) steering with benign SAE features (e.g., "brand identity") shows comparable risk, with 668/1000 features jailbreaking at least 5 prompts; and (3) averaging 20 random jailbreaking vectors creates a transferable attack that increases compliance by up to 4× on several models, without requiring model weights, gradients, or harmful training data.

## Strengths

- **Addresses a genuine, overlooked gap.** Prior work on activation-steering safety has focused on adversarially *optimized* jailbreak vectors. The question of whether *benign, legitimate* steering vectors inadvertently compromise safety is a real and under-studied problem, and the paper articulates this gap clearly (Sec. 2, last paragraph). [impact: +9.2/10]
- **The universal attack finding is genuinely surprising and practically significant.** Averaging 20 random vectors that jailbreak a single prompt produces a transferable vector that increases compliance by up to 4× on several models (e.g., Falcon3-7B: 5.7% → 63.4%), without requiring model weights, gradients, or harmful training data (Sec. 4.4, Fig. 6). This is the paper's strongest contribution. [impact: +9.2/10]
- **Broad model coverage.** Random steering experiments span 8 models across 4 families at 3B–70B scales, supporting the claim that the vulnerability is not model-specific (Sec. 4.1, 4.4). [impact: +6.7/10]
- **The Goodfire API case study (Sec. 4.3)** grounds the findings in real-world risk, concretely showing that a "brand identity" feature — semantically benign and likely to pass any safety review — can elicit detailed harmful instructions from a production model. [impact: +6.3/10]
- **Finding that the most dangerous SAE features are semantically benign** (e.g., "brand identity," "physical positioning") is an important result with practical safety-monitoring implications (Sec. 4.2, Fig. 4a). [impact: +5.9/10]
- **Systematic sweep across dimensions** (model family, layer depth, steering coefficient, vector type) provides a solid methodological foundation for identifying the most vulnerable configurations (Sec. 4.1). [impact: +5.8/10]

## Weaknesses

### Fatal
None.

### Major

1. **The evidence for the core "benign steering" claim rests on a narrow empirical base.** The paper's headline claim — that benign, legitimate steering vectors compromise safety — is primarily supported by SAE experiments confined to a single model (Llama3.1-8B) and a single SAE (Goodfire's layer 19 SAE). The paper transparently states this limitation (Sec. 3.3), but it means the most central claim lacks breadth. The random-direction experiments, while extensive, speak to robustness failures from *noise*, not directly to whether *semantically meaningful* benign steering (as used in practice) is comparably dangerous. The 2–4% gap between SAE and random compliance (Fig. 2c) would also benefit from testing across more models to assess its generality. [impact: -8.6/10]

2. **No uncertainty or variance measures are reported.** Every result is a point estimate (average over 1,000 vectors) without confidence intervals, standard deviations, or any variance measure. With 1,000 random vectors per condition, computing basic descriptive statistics is straightforward and standard practice. Without them, the reader cannot assess whether differences (e.g., the SAE-vs-random gap in Fig. 2c, or model-to-model differences in Fig. 6) are reliable or within measurement noise. [impact: -7.2/10]

3. **The "universal attack" label overclaims relative to the evidence.** The attack is called "universal" throughout (abstract, Sec. 4.4 header, conclusion), but it fails entirely on Qwen2.5-32B (9%→9% compliance) and barely improves Falcon-H1-34b (11%→18%). The paper acknowledges model-dependence ("highly model-dependent," Sec. 4.4), yet the "universal" framing implies coverage across all cases. A more precise term like "aggregated steering attack" or "transferable steering attack" would better communicate the model-dependent nature of the effect. [impact: -5.3/10]

### Minor

4. **Framing disconnect between motivating example and experiments.** The paper opens with a vivid example (Fig. 1) of steering for a "France concept" causing compliance with a harmful request. The SAE experiments test abstract meta-features (e.g., "brand identity," "physical positioning"), not topical-concept vectors like "France" or "Python." While both are "benign" vectors, the specific scenario that motivates the paper is never directly tested. Either adding experiments bridging this gap or explicitly noting this as an open question would improve alignment between motivation and evidence. [impact: -2.4/10]

5. **The SAE feature interpretation process is opaque.** The paper relies on "predetermined feature interpretations from Goodfire API" (Sec. 4.2) to label features as benign. The derivation and validation of these interpretations are not described, yet the claim that "benign features are dangerous" depends on features being correctly interpreted as benign. Some discussion of how these interpretations are validated would strengthen the paper. [impact: -0.2/10]

### Trivial

6. **The abstract reports an extreme range (2–27%) rather than typical values.** The 27% comes from the most vulnerable category on Llama3-8B (Malware/Hacking), while the overall average compliance rates are 10–17% (Fig. 3). The range is technically correct but frames the result at its most dramatic endpoints. The finding is still concerning at 10–17%, so this is more about responsible framing. [impact: -0.4/10]

## Nice-to-Haves

- Evaluate the universal attack's effect on benign (non-harmful) prompts to assess whether it degrades general performance.
- Summarize the human-validation results of the LLM judge (currently in Appx. B) in the main text.
- Conduct a finer-grained layer sweep around middle layers where vulnerability peaks.
- Expand investigation of the mechanism behind steering-induced safety failure.

## Removed Points

- *"No human validation of the LLM judge is visible in the main text"* — The paper explicitly references this in Appx. B, which is stripped by the parser. Removed per rules about parser-induced artifacts.
- *"The section on mechanism (App. E) is deferred to appendix"* — Removed per same rule.
- *"No test of whether the universal attack works on unseen safe prompts"* — Moved to Nice-to-Haves.
- Pure formatting nitpicks and speculative criticisms about appendix content were removed.

## Novel Insights

Beyond the paper's own contributions, the review process reveals a notable misalignment between the paper's strongest evidence and its most memorable motivating example. The paper opens with steering for a topical concept ("France") but the SAE experiments test abstract response-style features (brand identity, positioning). This gap poses an interesting follow-up question: are topical-concept vectors comparably dangerous, or is the risk specific to certain feature types? The paper would benefit from either testing this or explicitly marking the distinction as future work.

## Suggestions

1. **Add confidence intervals or standard deviations to all compliance rate figures.** With N=1,000 per condition, this is trivial and would significantly strengthen the evidence.
2. **Rename the "universal attack"** to something more precise (e.g., "aggregated steering attack" or "transferable steering attack").
3. **Either expand the SAE experiments to at least one additional model family, or reframe the paper's central claim** to match the scope of the evidence more precisely.
4. **Add an experiment testing topical-concept steering vectors** (analogous to the "France concept") to directly validate the motivating example, or explicitly note this as an open question.

## Score and Decision

The paper tackles a genuine and important problem, and the universal attack finding (Sec. 4.4) is a clear, publishable contribution. The SAE analysis showing that benign features can jailbreak is also valuable. However, the evidence for the core "benign steering" claim is narrower than the paper's framing suggests (one model for SAE experiments), the complete absence of uncertainty quantification weakens the evidential strength of all comparisons, and the "universal" label overstates the attack's generality. These are real but addressable weaknesses; they do not invalidate the paper's contributions but require the authors to better align their claims with their evidence.

**Score: 6** — The findings are worth publishing with revisions that calibrate the framing, add basic uncertainty measures, and either expand or more carefully scope the SAE evidence.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>