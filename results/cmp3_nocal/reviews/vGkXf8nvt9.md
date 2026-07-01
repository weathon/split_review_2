Here is the final consolidated review.

---

## Summary

This paper proposes Forget-to-Focus (F2F), a two-stage protocol that first performs targeted machine unlearning on a "forget set" of general-domain data (with an optional retain set for stability) and then fine-tunes on a domain-specific dataset. The core idea is to repurpose unlearning—normally a privacy mechanism—as a preparatory intervention to suppress irrelevant pretraining knowledge that may interfere with domain specialization. Experiments span 5 models (0.6B–72B), 3 domains (coding, medicine, math), multiple unlearning variants, and several forget-set construction strategies. The paper reports that F2F consistently outperforms standard fine-tuning, DAPT, and parameter-efficient baselines on most configurations.

## Strengths

1. **Novel and well-motivated research question.** Repurposing machine unlearning—conventionally a privacy safeguard—as a preparatory step for downstream specialization is a genuinely novel direction. The paper correctly identifies that fine-tuning inherits everything from pretraining, and asks whether actively removing interfering features before adaptation can help. This is a worthwhile question regardless of the specific results.

2. **Broad experimental scope.** The paper covers 5 models (Qwen-0.6B, Gemma-2B, LLaMA 8B/13B, Qwen-72B), 3 domains, 4 unlearning variants (GA+GD, GA-only, NPO, GA+KL), 3 forget-set construction strategies (BC-Select, BC-Mixed, BC-Cosine), and multiple fine-tuning baselines (SFT, DAPT, LoRA, CurlLoRA). Table 3 alone presents results across 6 benchmarks for 3 models with multiple forget-set and unlearning configurations. This scale of experimentation is rare and should be acknowledged.

3. **Some practically meaningful gains.** The best reported results show substantial improvements in several cases—e.g., Qwen-0.6B HumanEval pass@1 improves from 31.71 (SFT) to 42.07 (F2F+SFT), and Qwen-72B improves from 71.12 (SFT) to 78.50 (F2F+SFT). If robust, these gains are practically meaningful.

## Weaknesses

### Fatal
None.

### Major

1. **No control isolating the effect of the additional training phase from targeted forgetting.** The F2F protocol adds an unlearning phase *before* fine-tuning, so F2F models receive more total gradient steps than the SFT baseline. The paper's central causal claim is that *targeted forgetting* of irrelevant knowledge drives the improvements, but there is no control experiment that substitutes the forget set with (a) random non-domain data, (b) data from a different domain, or (c) gradient ascent with random labels. Without such a control, the reported improvements could be explained by simply having a longer training budget, the regularization effect of a two-phase procedure regardless of content, or a generic perturbation to initialization. The paper cannot attribute improvements to the *content* of the forget set rather than to the mere presence of an extra pre-fine-tuning optimization phase.

2. **Retain set contamination gives F2F an inherent advantage over baselines.** The paper states (Section 3.3, line 129): "The retain set is a small subset of the fine-tuning data, following prior work (Geng et al., 2025)." This means the unlearning phase trains on a subset of the same examples that will later be used for fine-tuning. The SFT baseline never sees these examples twice. This gives F2F a built-in advantage—effectively semi-supervised pretraining on the target distribution before fine-tuning—that is unrelated to the forgetting mechanism. A proper control would draw the retain set from a held-out portion of general data, not from the downstream task itself.

3. **Abstract, introduction, and conclusion claim calibration improvements as a verified finding without evidence in the main body.** The abstract states that F2F "helps improved calibration on medical QA tasks, reducing overconfidence and mitigating reliability issues." The contribution list (line 29) and conclusion (line 301) repeat this claim. **No calibration analysis—ECE, reliability diagrams, confidence-vs-accuracy comparisons, or any quantitative calibration metric—appears anywhere in the main body.** The main body presents CKA and SVCCA representational analyses but no calibration evaluation. If the calibration analysis exists only in the appendix (which was stripped from this review copy), the abstract still overstates what the main body demonstrates: a reader of the main paper cannot verify this claimed finding. The paper should either present key calibration results in the main body or remove these claims from the abstract, contributions, and conclusion.

### Minor

4. **Theoretical analysis is disconnected from the experiments.** The Proposition and Corollary (Section 2) analyze gradient-descent dynamics on a convex linear surrogate model with orthogonal feature decomposition. While the paper acknowledges this is a surrogate for the LLM setting, the theory never connects to the experiments: it does not predict which forget sets will work better, does not guide any hyperparameter choices, is not validated empirically (e.g., by checking whether the contraction bound approximately holds), and offers no insight into why observed gains vary across models and domains. The theory occupies roughly 25% of the method section but contributes nothing to the paper's experimental design or interpretation.

5. **No statistical uncertainty reported.** All results are single-point estimates with no confidence intervals, error bars, or significance tests. Given the variability across models and forget-set types (where differences are sometimes only 1–2 points), it is impossible to assess which differences are reliable.

6. **Section 4.2 is confusingly structured.** Titled "F2F w/ Fine-Tuning Variants," but Table 2 only shows baseline methods (SFT, LoRA, CurlLoRA, DAPT) without any F2F results. The F2F results for the medical domain are deferred to Table 3 and Section 4.3. This makes the section difficult to follow.

7. **No dedicated analysis of math domain results.** Math is claimed as one of three domains, but unlike coding (Section 4.1) and medicine (Sections 4.2–4.3), there is no standalone section analyzing math performance. Math results only appear in Table 3 without dedicated discussion.

8. **Missing data point in Table 1.** The Qwen-72B row for `Unl_{GA+GD}` (unlearning-only checkpoint) shows 71.30 for MBPP but a blank entry for HumanEval. The reader cannot assess how much unlearning alone degrades the 72B model's coding performance on this metric.

9. **CKA analysis is over-interpreted.** The paper interprets F2F's greater representational dissimilarity from the starting point as evidence of "reshaping representational geometry toward domain-useful structure." However, CKA only measures *dissimilarity*, not direction or quality. F2F has undergone more total training (unlearning + fine-tuning > fine-tuning alone), so representations having drifted further is expected regardless of whether the drift is beneficial. The paper does not causally link the CKA measure to downstream performance.

### Trivial

- Section 4.1 lists "four principal insights" (labeled 1–4) but adds a fifth unlabeled observation, creating a mismatch.
- The Qwen-72B column in Table 1 has an extra trailing empty column, suggesting a possible formatting misalignment.

## Nice-to-Haves

- Adding a control experiment with random-data unlearning (or gradient ascent on random labels) before fine-tuning would substantially strengthen the paper's causal claims.
- Drawing the retain set from held-out general data rather than from the downstream fine-tuning set would eliminate the data-leakage confound.
- Including simpler regularization baselines (e.g., dropout, weight decay, early stopping) would help isolate whether the gains are specific to unlearning or result from any form of regularization applied before fine-tuning.
- Reporting DAPT training details (data volume, number of steps) would help the reader assess whether this baseline received comparable resources.

## Removed Points

- *Criticism about Fisher information and PCA-shift analyses not appearing in the main body.* These are listed in the contribution list alongside CKA/SVCCA as analyses performed. Per the paper's note ("Rest of paper (reference and Appendix) is removed"), these analyses likely exist in the appendix. Following the rule against penalizing missing appendix content, this criticism is removed.
- *Criticism that LLaMA 13B base HumanEval score of 0.60 "suggests instruction tuning format mismatch."* This is speculation not supported by the paper's content.
- *Criticism that GSM8K results for Qwen 0.6B are "uninformative."* The paper reports these numbers transparently; low scores on a hard benchmark for a small model are a finding, not a flaw.
- *Criticism that "DAPT appears undertrained."* The paper does not provide DAPT training step counts, but the specific claim that DAPT is undertrained is speculative.
- *Criticism about inconsistent reference points in abstract vs. contributions.* Both numbers are accurate for the comparisons they make; the minor phrasing inconsistency is not a substantive issue.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the core methodological gaps (no control for extra training phase, retain-set contamination) but do not add novel scientific insights beyond what the paper already states and fails to address.

## Suggestions

1. Add a control experiment where the unlearning phase performs gradient ascent on random non-domain data (or data from a different domain than the downstream task) before fine-tuning. This is the single most important experiment to validate the paper's central causal claim.
2. Either remove the calibration claims from the abstract, introduction, and conclusion, or present the calibration analysis (with key quantitative results) in the main body.
3. Re-run the experiments with a retain set drawn from held-out general data, not from the downstream fine-tuning set.
4. Add confidence intervals or error bars (e.g., over 3–5 seeds) to at least the key comparisons.
5. Restructure Section 4.2 to clearly separate the baseline analysis from the F2F comparison, and add a dedicated math results section.
6. Include a "same-optimization-different-data" control to isolate the effect of targeted forgetting from the effect of additional training steps.

## Score and Decision

The paper's core idea—using unlearning as a preparatory step for domain specialization—is novel and timely, and the experimental scope is commendably broad. However, the paper has two decisive methodological gaps. First, the F2F pipeline adds an extra training phase with a retain set drawn from the downstream task's training data, but provides no control to distinguish targeted forgetting from generic benefits of additional pre-fine-tuning optimization. Second, the abstract and conclusion claim calibration improvements without any supporting evidence in the main body. These issues prevent the paper from convincingly supporting its central causal claims. The paper would need substantial additional controls and restructuring before it could be accepted. Recommend rejection, with encouragement to resubmit after addressing the control experiments and removing unsupported claims.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>