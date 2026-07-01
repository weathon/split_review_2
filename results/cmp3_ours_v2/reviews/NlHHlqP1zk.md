Now let me finalize and write the complete review.

## Summary

This paper proposes the Fast and Slow Effect (FSE) framework to evaluate whether LLM/VLM-generated concept annotations are "sufficient" — i.e., whether the textual concepts alone, without the original image, enable accurate classification. The framework has the model first annotate concepts through a five-stage coarse-to-fine refinement process, then measures the Class Representation Index (CRI): the accuracy with which the *same model* classifies using only its textual concepts (slow mode) vs. using the full image (fast mode). Experiments across six models and five datasets find that slow mode underperforms fast mode by ~25% on fine-grained datasets, while the opposite holds on general datasets. A fusion experiment (image + concepts) shows high CRI (~90%) while concept-only CRI is low (~50%), demonstrating that downstream utility does not imply annotation sufficiency.

## Strengths

1. **The motivating example (Figure 1) is compelling and clearly exposes the problem.** The dialogue showing an LLM correctly classifying an image, generating plausible concepts, but then using those same concepts to pick the wrong class cleanly illustrates the gap between annotation plausibility and annotation sufficiency. This is a non-obvious problem that the paper convincingly establishes as worth studying.

2. **The empirical finding in Table 4 — the dissociation between fusion accuracy and concept-only accuracy — is the paper's strongest contribution.** Fusion mode achieves ~90% CRI while slow mode alone scores ~50%, providing direct evidence that the commonly used "utility-as-proxy" assumption is unreliable. This should give pause to practitioners using accuracy gain as a proxy for annotation quality.

3. **The pattern reversal between fine-grained and general datasets (Table 3) is genuinely interesting.** On CIFAR-100/Caltech-101, slow mode *outperforms* fast mode at t=5 (94% vs. 84-91%), while on fine-grained datasets the gap is -25% to -27%. This non-trivial result shows that the framework can distinguish annotation scenarios where LLMs succeed vs. fail.

## Weaknesses

### Fatal

None.

### Major

1. **CRI conflates concept quality with reasoning ability, but the paper's core interpretation assumes it measures only the former.** The CRI measures the accuracy with which the *same LLM that generated the concepts* can use those concepts (text-only) to predict a class. A low CRI can arise from either: (a) the concepts themselves lack sufficient discriminative information, or (b) the LLM is bad at reasoning from textual concepts — even though it "knows" the class when shown the image (fast mode is high). The paper consistently attributes low slow-mode CRI to interpretation (a) and frames this as a *finding* about annotation insufficiency (abstract: "current annotation methods fail to provide sufficient semantic coverage"; Section 6: "the models still struggle to externalize their implicit expertise"), but it does not adequately acknowledge this as a *confound in what CRI measures*. The paper's Definition 3.1 defines sufficiency as concepts being "expressive, clear, and precise enough to enable accurate inference," but the operationalization through self-evaluation means CRI measures the compound concept-quality × reasoning-ability. This ambiguity runs through every result and conclusion. A proper control would involve cross-model evaluation (concepts from GPT-4o evaluated by Llama as reasoner, and vice versa) or a human baseline to separate the two factors. **Without this, the paper's central claim — that "annotation methods fail to provide sufficient semantic coverage" — is underdetermined by the evidence.**

2. **The fusion experiment does not fully address the utility-as-proxy assumption in the form used by actual concept bottleneck models.** The fusion mode gives the LLM *both* the image and the concepts jointly, which is more akin to multimodal prompting than to a true CBM where concepts serve as an information bottleneck (class predicted *only from concepts*). The paper's conclusion that "high utility can be misleading" is still reasonable, but the evidence is weaker than claimed for the specific CBM setting, where the bottleneck structure is stricter.

### Minor

1. **No human baseline for interpreting absolute CRI values.** The paper proposes to evaluate "sufficiency" of automated annotations but never establishes what "good" means. If human-written concept descriptions also achieve only 50–60% CRI in slow mode on fine-grained datasets, then the finding would reflect the inherent difficulty of text-based fine-grained classification, not the insufficiency of LLM-generated annotations specifically. Without this anchor, the absolute CRI numbers are hard to interpret, and the paper's title question ("Are LLMs good XAI annotators?") cannot be fully answered.

2. **The sample sizes (l) for the main experiments are not stated in the main text.** The preliminary experiment uses 100 images per dataset (stated explicitly), but it is unclear whether the main CRI experiments (Tables 2-4) use the same sample size, full datasets, or something else. This is a reproducibility concern.

3. **The formula in Equation 2 has a typo in the summation bounds.** The equation reads `(1/t) Σ_{i=1}^t` when it should read `(1/l) Σ_{i=1}^l`, where l is the total number of test cases. This does not affect the actual computed results (the reported numbers are sensible), but it is confusing and should be corrected.

### Trivial

None.

## Nice-to-Haves

- **Cross-model evaluation:** Evaluating CRI where the reasoner is a *different* LLM than the annotator (e.g., GPT-4o concepts evaluated by Llama) would directly address the confound between concept quality and reasoning ability. If cross-model CRI is also low, that strengthens the case for annotation insufficiency; if it is higher than self-CRI, that indicates the original LLM's reasoning, not its concepts, was the bottleneck.
- **Discussion of exceptions:** Table 2 shows that Llama-3.2-vision-11b on Flower (+3.24%) and QwenVL2-7b on CUB-Bird (+7.50%) achieve *positive* CRI-Gaps. These exceptions could be informative about what enables slow-mode success.
- **Explicit discussion of the t=1 collapse:** Table 3 shows CRI collapsing to ~29-34% at t=1 (Background concepts only) on general datasets, then recovering to ~94% by t=5. This dramatic early-stage failure and late-stage recovery pattern deserves more analysis.

## Removed Points

These points from the harsh critic input were removed for the following reasons:

- **"Fast vs. slow mode comparison is not apples-to-apples"** — This concern is subsumed by Weakness #1 (the confound between concept quality and reasoning ability). The paper explicitly defines the two modes as operating on different inputs (image vs. text), so this is not a flaw in the design but a restatement of the interpretational ambiguity already captured.
- **DeepSeek-R1 result relegated to Appendix D** — Normal practice for supplementary findings; not a weakness.
- **Five-stage refinement not validated for consistent prompt behavior** — Appendix B (prompt formulations) was stripped by the parser; the paper cannot be faulted for content that exists in the original submission.
- **"FineGrained-Avg at t=0 is higher than CIFAR-100 fast mode"** — This is an observation about the data, not a weakness of the paper.
- **"The paper's title question cannot be answered without knowing what 'good' means"** — The paper operationalizes "good" through the CRI metric and comparison to fast mode. The lack of a human baseline (Minor Weakness #1) partially addresses this, but the strong framing is removed as overstated.
- **Code/data link is a placeholder** — The link says "here" with no URL, but this is a minor presentation issue in the review format.
- **Statistical detail thin** — The paper reports three runs with standard deviations shown in Figure 3 as error bars.
- **"CRI collapse at t=1 not adequately discussed"** — The paper presents the full trajectories in Table 3 and discusses the recovery. The pattern is clear from the data.

## Novel Insights

The most insightful finding that emerges from the reviews — and that goes beyond what the paper itself emphasizes — is the **reversal pattern**: LLMs' concept annotations are relatively sufficient for general-domain classification (slow mode beats fast mode on CIFAR-100/Caltech-101) but systematically insufficient for fine-grained classification. This suggests the insufficiency is not a general property of LLM-generated concepts but is specifically tied to the discriminative demands of fine-grained recognition, where the concepts needed to separate similar classes require a level of precision that current annotation methods do not reliably produce. The fusion vs. slow-mode dissociation further sharpens this: the concepts are *present* in the model's knowledge (the model can use them when also shown the image) but are not *accessible* through the concept-generation pipeline alone — a failure at the level of annotation *externalization* rather than knowledge. Whether this externalization failure is due to the concepts being genuinely insufficient or due to the LLM's own inability to reason from its textual concepts (the core confound) remains unresolved.

## Suggestions

1. **Add a cross-model control experiment.** Take concepts generated by GPT-4o and evaluate CRI using Llama-3.2 as the reasoner, and vice versa. This directly addresses the central confound and would substantially sharpen the paper's claims regardless of outcome. If cross-model CRI confirms the same pattern, the case for annotation insufficiency is strong; if not, the paper's conclusions need reframing.
2. **Add a small-scale human baseline** (e.g., 50 examples per dataset with concepts written by a knowledgeable annotator) to anchor the absolute CRI values.
3. **Report the test set sizes used in the main experiments** and state whether the results are from the full dataset or a sampled subset.
4. **Correct the summation bounds in Equation 2** from `(1/t) Σ_{i=1}^t` to `(1/l) Σ_{i=1}^l`.
5. **Reframe the paper's conclusions** to more precisely reflect what CRI measures — the compound of concept quality and the generating model's reasoning ability — and clearly state this as a limitation from the abstract onward.

## Score and Decision

Based on calibration against 18 anchor papers across all score bands:

**Round 1 bracket:** 3.5 – 5.5

**Anchors consulted:**
- Strong reject (avg 1.0–1.4): Systematic lit reviews, jailbreaking papers — far weaker than our paper.
- Reject (avg 3.0): "Evaluating the Unseen" (3.0) — similar evaluation framework for CBMs with a conceptual confound; our paper is stronger in experimental breadth.
- Reject (avg 3.67): "Are Large Language Models Post Hoc Explainers?" (3.67) — similar evaluation framing; our paper has better structure and more substantive findings.
- Reject (avg 4.67): "ConLUX" (4.67) — interesting concept-based explanation framework with good experiments but significant limitations; comparable in quality to our paper.
- Accept (avg 5.75): "Concept Bottleneck Large Language Models" (5.75) — stronger methodological contribution; our paper does not reach this level.
- Strong accept (avg 8.0): VLM analysis papers — clearly higher quality and impact.

**Narrowed to:** 4.0

The paper addresses a timely problem with a well-structured framework, interesting empirical patterns, and one genuinely valuable finding (the fusion/slow-mode dissociation). However, the central interpretive claim — that the CRI reveals annotation insufficiency — is undermined by the confound between concept quality and reasoning ability, which the paper does not adequately control for or acknowledge as a limitation of the metric itself. The paper's conclusions are overclaimed relative to what the evidence uniquely supports. These are real contributions that warrant revision and resubmission but do not yet meet the bar for acceptance.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>