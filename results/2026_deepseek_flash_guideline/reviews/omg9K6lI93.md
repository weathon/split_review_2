Now I have sufficient calibration data. Let me finalize the review.

My bracket analysis: The paper is most comparable to "Evading Data Contamination Detection" (avg 4.25, rejected) and "Rethinking Memorization" (avg 3.50, rejected). Our paper has empirical substance and a novel probing method, but suffers from a fundamental experimental design flaw (English test items in p=0) and an internal contradiction, making it weaker than the Evading paper. I place it at **3.0 (Reject)** — a clear reject due to the design issue undermining the core claim, but not a strong reject since the research question and some methodological components have value.

---

## Summary

This paper investigates whether translating evaluation benchmarks (MMLU, XQuAD, MLQA) into Arabic masks data contamination signals. The authors fine-tune four open-weight LLMs on English test data plus varying proportions (0%, 10%, 50%, 100%) of Arabic-translated test data, then evaluate on the original English benchmarks. They extend TS-Guessing with a choice-reordering strategy (Index-Recall Rate, IDR) to probe memorization, and propose a Translation-Aware Contamination Detection (TACD) framework as a forward-looking blueprint.

## Strengths

1. **Choice-reordering IDR metric is a principled behavioral probe.** The Index-Recall Rate (Section 3.4) targets the specific way MCQ contamination manifests — memorized index-letter patterns — and captures signals that ROUGE-L F1 misses (Table 3a: LLaMA IDR of 0.643 at 50% contamination vs. ROUGE-L of 0.006). This is a genuinely useful diagnostic extension of Deng et al. (2024).

2. **Multi-architecture evidence across four model families.** Results span Llama-3.2-1B, Mistral-7B, Gemma-3-1B, and Qwen3-1.7B (Section 3.1), and the general pattern of MMLU gains with Arabic contamination proportion appears across all of them. This rules out model-specific tokenizer or architecture artifacts.

3. **Embedding analysis provides a mechanistic explanation.** Section 4.3 reports that Arabic→English translations have high cosine similarity to their English originals in representation space, explaining why semantic content (and thus memorized knowledge) survives translation even when surface forms differ. This moves beyond observation to explanation.

4. **Dose-response experimental structure.** Using four contamination levels (0%, 10%, 50%, 100%) allows the paper to study the gradient of the effect rather than just a binary comparison, which is a sound design choice in principle.

## Weaknesses

### Fatal

1. **The experimental design studies deliberate test-set leakage, not real-world contamination, and the p=0 baseline is already maximally contaminated.** Section 3.1 defines the training set as D_EN^d ∪ D_AR^d(p), where D_EN^d is explicitly *"English test items formatted as MCQ"* (for MMLU) or *"English QA"* (for XQuAD/MLQA). This means every model under study, including the p=0 "clean" condition, has been fine-tuned on the exact English test data. The central finding — "translation masks contamination" — is therefore a second-order effect on top of blatant English test-set leakage. To isolate whether translation alone confers an evaluation advantage, a genuinely clean baseline (no English or Arabic test data in training) is required. As designed, the experiment conflates the effect of translation with the overwhelming signal of English test-set exposure, undermining the paper's core claim.

### Major

2. **The evidence does not distinguish contamination-driven memorization from cross-lingual transfer.** The paper attributes MMLU gains to "contamination-driven memorization," but the observed behavior is equally consistent with genuine cross-lingual transfer: fine-tuning a multilingual model on Arabic math/science questions can improve English performance because the concepts transfer. The TS-Guessing probe (Table 3) was supposed to resolve this ambiguity, but the results are too weak and inconsistent to do so. Mistral's IDR is essentially 0.000–0.001 at all contamination levels (i.e., the probe detects nothing). Gemma's IDR *decreases* with more contamination (0.350 → 0.029 → 0.005), which is the opposite of what the contamination hypothesis would predict. XQuAD Exact Match rates are 0.000–0.103 across all conditions. These numbers are noise, not signal. The paper lacks control conditions — e.g., fine-tuning on Arabic non-benchmark content of similar domain — that could separate cross-lingual transfer from memorization.

3. **Internal contradiction: Section 4.2 claims "approximately equal performance" and "near-flat trend" across contamination levels, but Table 2 shows clear, substantial increases.** Section 4.2 states *"Across contamination levels p ∈ {10, 50, 100}%, the models exhibit approximately equal performance on all evaluated benchmarks."* Yet Table 2 shows, for example: Mistral MMLU goes 0.580 → 0.690 → 0.690 (a 19% relative jump from 10% to 50%); LLaMA goes 0.381 → 0.389 → 0.431; Gemma goes 0.244 → 0.261 → 0.284. XQuAD also shifts substantially (Mistral: 0.455 → 0.272 → 0.114; Gemma: 0.481 → 0.577 → 0.606). These are not "approximately equal" or "near-flat." The paper cannot simultaneously claim that contamination causes performance gains (Section 4.1) and that performance is flat across contamination levels (Section 4.2). This contradiction requires resolution.

### Minor

4. **Unsupported claim about Arabic proficiency in the abstract.** The abstract states that models with *"stronger Arabic capabilities"* benefit more from Arabic-translated contamination, yet the paper contains no measurement of Arabic capability, no comparison of models' relative Arabic proficiency, and no experiment testing this claim. It appears in only the abstract and introduction, with zero supporting evidence.

5. **TS-Guessing operationalization has limited sensitivity and the paper does not discuss this.** For MMLU, the probe masks the text of an *incorrect* answer (not the correct answer), so correct recall signals contamination only if the model memorized the distractor's text — a weak and indirect signal. For XQuAD/MLQA, masking a single "critical token" in the question (Section 3.3) is fragile: the token could be predictable from context alone (e.g., "capital" in "What is the [MASK] of France?" when context mentions Paris), producing false positives from non-contaminated reasoning.

6. **No confidence intervals or repeated-run statistics.** All results in Tables 2 and 3 are point estimates. Given the non-monotonic patterns and small model sizes, variance estimates are essential to distinguish meaningful trends from noise. The post-hoc explanations for non-monotonic MLQA patterns ("overfitting to distributional quirks," Section 4.1) are unsupported speculation without such statistics.

### Trivial

7. The TACD framework (Section 5) is presented as a "forward-looking blueprint rather than a complete implementation" (Section 5.3). This is transparent but means it cannot be evaluated as a contribution. The embedding analysis in Section 4.3 is referenced but only a single cosine similarity equation is given.

## Nice-to-Haves

- Adding a control condition: fine-tuning on Arabic *non-benchmark* content of similar domain, to distinguish cross-lingual transfer from memorization.
- Adding a control condition: fine-tuning on English-paraphrased test data, to test whether any surface-form perturbation masks contamination or whether translation is special.
- Directly testing whether existing detection methods (Min-K% Prob, guided prompting, n-gram overlap) actually fail on Arabic-translated data, rather than asserting they do.
- Correlating measured Arabic task performance with contamination benefit to support the claim about "stronger Arabic capabilities."

## Removed Points

- **"The paper lacks novelty/technical depth"** — too generic; the paper does have specific empirical results and a novel probing extension.
- **"Model size range is narrow (1B–7B)"** — a common constraint in open-weight research; not a genuine weakness.
- **"Missing related works"** — cannot verify without external sources.
- **"Reproducibility nitpicks about hyperparameters"** — standard practice; appendix covers these.
- **"Typos/formatting complaints"** — parser artifacts.
- **"Missing appendix content"** — parser strips appendix; content exists in original submission.
- **"The paper would be strengthened by..."** generic suggestions — moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The most interesting observation is the gap between IDR and ROUGE-L in Table 3a, which suggests that MCQ contamination can persist through surface-form changes while evading n-gram overlap metrics. However, the weakness of the TS-Guessing results overall prevents this from being a well-supported insight.

## Suggestions

1. **Restructure the experiment so that the p=0 condition does NOT include English test items in the training set.** The core research question is whether translated benchmarks alone (without English leakage) confer an evaluation advantage. The current design cannot answer this question.

2. **Reconcile the contradiction between Sections 4.1 (clear gains) and 4.2 ("flat" trends).** These cannot both be true as stated — either the MMLU gains are real (contradicting the "flatness" claim) or they aren't.

3. **Add control conditions** that separate cross-lingual transfer from memorization: (a) fine-tuning on non-benchmark Arabic content, (b) fine-tuning on English-paraphrased test data to benchmark the "translation" effect against generic surface-form perturbation.

4. **Either remove the unsupported claim about Arabic capabilities from the abstract, or add experiments that test it.** The current paper contains no evidence for this claim.

5. **Add confidence intervals or repeated-run standard deviations** to all reported metrics in Tables 2 and 3.

## Score and Decision

**Anchor comparisons for calibration:**

| Path | Avg Human Score | Round | Comparison |
|------|:-:|:-:|-----------|
| /home/.../Nk1MegaPuG.md (Evading Data Contamination Detection) | 4.25 | R1 | Similar theme (evading contamination detection via surface-form perturbation). That paper had a cleaner experimental design but was rejected for lack of depth. Our paper has more empirical substance but a more fundamental design flaw (p=0 includes English test items). |
| /home/.../rAylWUIKtu.md (Benchmark Inflation) | 4.25 | R1 | Contamination detection via retro-holdouts. Better methodology but narrower scope. Our paper has a more interesting research question but weaker execution. |
| /home/.../Nsms7NeU2x.md (How much can we Forget) | 6.75 | R1 | Rigorous contamination study with theory. Our paper is substantially weaker in experimental design and theoretical grounding. |
| /home/.../hFQZmKFtlT.md (Rethinking Memorization) | 3.50 | R2 | Similar quality level — interesting question, flawed execution, rejected. Our paper has comparable methodological issues. |

**Bracket:** Round 1 bracketing placed the paper between scores 3–5. Round 2 (narrowing within 1.5–4.5) retrieved anchors at 3.50 and 4.25. Our paper's fatal design flaw (p=0 includes English test items) makes it weaker than the 4.25 "Evading Contamination" anchor, placing it near the 3.50 "Rethinking Memorization" anchor. The research question is worthwhile and the IDR metric is a genuine contribution, but the experimental design undermines the core claim.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>