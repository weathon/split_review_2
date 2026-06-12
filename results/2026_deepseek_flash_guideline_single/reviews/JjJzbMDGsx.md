## Summary

The paper introduces the Language Confusion Gate (LCG), a lightweight plug-in module trained via norm-adjusted self-distillation that filters tokens at decoding time to reduce language confusion in multilingual LLMs. A key mechanistic insight—that high-resource language tokens dominate the top-5% of embedding norms, biasing sampling toward them—grounds the method. Across four base models (Qwen3-8B/30B, Llama3.1-8B, Gemma3-12B) and two task types, LCG reduces CJ and Latin confusion by roughly an order of magnitude with ~0.4% per-step overhead and no degradation in task performance.

---

## Strengths

1. **Mechanistically grounded method (Section 3.2, Figure 2, Table 1).** The token embedding norm decomposition (logit = norm × cosine similarity) and the systematic demonstration that CJ/Latin tokens dominate the top-5% of embedding norms across all five examined models is a clean, falsifiable insight. Figure 2's concrete example—where norm-adjustment causes CJ tokens to vanish from the top-10 logits at a Hebrew confusion point—directly validates the mechanism and motivates the norm-adjusted self-distillation training. This gives LCG a principled foundation rather than being a heuristic.

2. **Large and consistent empirical reductions (Tables 3, 4).** LCG reduces confusion by roughly an order of magnitude across Qwen3-8B, Qwen3-30B, Llama3.1-8B, and Gemma3-12B on both translation (FLORES-NO-LATIN) and knowledge/reasoning (INCLUDE). Examples: Qwen3-8B Latin confusion 12.1% → 2.0%, Llama3.1-8B Latin 8.4% → 2.9%. BLEU and accuracy remain stable or improve marginally. Thinking-model results on Humaneval-XL show similar reductions with minimal Pass@1/Pass@10 impact. This consistency across architectures and task types is the paper's strongest empirical asset.

3. **Practical deployability.** The intervention rate of ~0.33–0.38% and per-step overhead of ~0.4% (15.95ms → 15.99ms) are convincingly low. The gate requires no base-model modification and is trained via self-distillation without external labels, making it immediately usable in multilingual deployments.

---

## Weaknesses

### Fatal
None.

### Major

1. **Code-switch preservation evaluation is incomplete for the paper's central claim (Section 5.3).** The paper states LCG "preserves the model's code-switch ability" (line 282), but the evidence has two gaps. First, the token-level experiment (86.7% preservation) checks whether the gate permits code-switching at points *from the model's own generations* that humans judged as appropriate—this tests whether the gate aligns with the model's preferred mixing patterns, not whether it preserves code-switching in genuinely diverse multilingual contexts (e.g., prompts that explicitly require mixing, such as explaining a foreign phrase in English, bilingual instruction following, or technical terms in non-English text). Second, on FLORES-WITH-LATIN, the code-switch rate drops from 46.34% → 25.90% for Qwen3-8B (~44% relative reduction). While the paper notes baselines are "just references," the magnitude of reduction could suppress legitimate bilingual behavior that the human reference happened not to include. The paper acknowledges it is tricky but does not provide per-output analysis showing the suppression targets genuinely incorrect mixing rather than appropriate code-switching.

2. **ORPO baseline comparison lacks sufficient implementation detail (Section 5.3, Figure 3).** The comparison against ORPO is reported with essentially no implementation details: dataset size, training compute, epochs, learning rate, hyperparameter tuning status, or whether the base model was frozen. The reported accuracy degradation (Qwen3-8B: 61.4 → 57.3; Llama3.1-8B: 46.1 → 43.2) is substantial enough to suggest suboptimal configuration rather than a fundamental limitation of the ORPO method. The paper's positioning depends partly on showing that training-based methods degrade performance (lines 15–16), but what is shown is that *this particular implementation* of ORPO underperforms—not that the method itself is inferior. Since the paper also notes ORPO achieves "performance comparable to LCG on Llama3.1-8B," the claim "LCG also outperforms training-based methods" (line 312) is overstated.

### Minor

3. **No statistical variance reporting.** All confusion rates and task scores are point estimates without confidence intervals, standard deviations, or run counts. This is particularly important for rare-event metrics (often <1% confusion) where a single confused generation can shift percentages meaningfully. Accuracy differences of 0.5–1.5 points (e.g., Qwen3-30B INCLUDE: 71.12 → 70.83) fall within typical LLM evaluation noise. Multiple seeds or bootstrapped confidence intervals would strengthen reliability.

4. **Reasoning-model evaluation does not match the motivating claim.** The introduction (line 15) asserts "Large Reasoning Models seem to reintroduce the problem," citing DeepSeek-R1 training issues, but the thinking-model evaluation is restricted to code generation (Humaneval-XL). No multilingual reasoning benchmark (e.g., MMLU in multiple languages, chain-of-thought translation, or translation-with-reasoning) is tested, so the paper's own experiments do not directly substantiate the reasoning-model framing.

5. **Scope limitation to script-level granularity is acknowledged but not tested.** The four-category (CJ/Latin/Symbols/Low-Res) scheme cannot distinguish confusion between same-script languages (Spanish vs. English, Hindi vs. Marathi). The paper acknowledges this (line 320) but does not test whether LCG *worsens* such errors by masking broad families—a targeted experiment on a same-script confusion pair would clarify the method's actual failure modes.

### Trivial
None.

---

## Nice-to-Haves
- A dedicated evaluation set of genuinely required code-switching contexts (e.g., bilingual prompts, English technical terms in non-English text) to directly test the central claim about preserving legitimate mixing.
- Reporting the fraction of confusion events attributable to norm bias vs. direction (cosine similarity) to clarify the method's boundaries.
- Reporting results on the LCB benchmark alongside custom FLORES filtering for comparability with prior work.

---

## Removed Points
- **"Code-switch evaluation is circular (test set from same model as training data)."** Removed because the gate is trained via self-distillation on the model's *hidden states and norm-adjusted language family predictions*, not on its output generations. The test set uses human annotators judging the model's outputs; there is no direct data leakage. The retained weakness (#1) reframes this as an issue of *distributional diversity*, not circularity.
- **Strengths about "addressing an important problem" or "targeting an interesting question."** Removed as generic/superficial; the retained strengths are specific and evidence-grounded.
- **"Missing appendix, missing related works, formatting issues."** Removed per instruction — these are parser artifacts or not substantive.
- **"Not using LCB creates a methodological gap."** The paper provides a reasoned explanation (lines 233) for why LCB is unsuitable; this is reasonable, not a weakness.
- **Harsh critic's "Strengthening the Paper on Its Own Terms" and "Missing Parts" sections.** These are suggestions, not critiques of existing flaws. The actionable ones are absorbed into Nice-to-Haves and Suggestions.

---

## Novel Insights
**The reviewer's observation that the code-switch evaluation conflates "preserving the model's behavior" with "preserving genuine code-switching" is a genuinely useful framing.** The paper's 86.7% and Table 5 results are real data, but they answer a narrower question than the paper claims. This insight—that self-distillation from a model's own outputs can entrench the model's preferred mixing patterns rather than general-purpose code-switch competence—is a nuance worth articulating when the authors strengthen this analysis. Beyond this, the reviews surface no novel insight beyond the paper's own contributions.

---

## Suggestions
- Provide full ORPO training details (dataset composition, hyperparameters, compute budget, learning curves). Consider using the original authors' published checkpoints if available, or run a controlled comparison with documented tuning.
- Construct a dedicated code-switch evaluation set from genuinely bilingual contexts (prompts requiring English technical terms in non-English text, bilingual explanations, language-study scenarios) and measure the gate's suppression rate on these.
- Report bootstrapped confidence intervals for confusion rates, or repeat main experiments across multiple seeds and report variance.
- Include a targeted experiment on same-script confusion pairs (e.g., English→Spanish, Hindi→Marathi) to demonstrate the method's known limitation does not actively worsen such errors.
- Replace or supplement the introduction's reasoning-model claim with an experiment on a multilingual reasoning benchmark, or temper the claim to match the code-generation evaluation actually performed.

---

## Score and Decision

**Round 1 bracket (wide):** The paper was compared against the full topical search across all score bands. Irrelevant or trivial papers (<1.5) and very strong papers (>7.5) were clearly not a match. The most comparable papers cluster in the 3.5–7.5 range. Specific anchors:
- **XTransplant** (avg 4.75, reject): cross-lingual inference intervention with data leakage issues — weaker than LCG which has fairer evaluation and cleaner methodology. 
- **Babel Tower** (avg 5.25, accept): multilingual code LLM evolution analysis with practical pretraining optimization — similar contribution depth but narrower scope (code only). LCG has broader model coverage.
- **Crosslingual Knowledge Barriers** (avg 5.67, reject): evaluation study with simple mitigation — LCG has a stronger novel method. 
- **TransLLM** (avg 6.25, reject): engineering-focused LLM adaptation — LCG has more novelty (norm analysis) and better writing.
- **The Same but Different** (avg 6.60, accept): high-quality multilingual mechanistic interpretability case study — LCG has broader empirical validation but less methodological depth in analysis.

**Narrowing:** The paper's core contribution (norm analysis + LCG method) is substantiated and practically useful. The evaluation has two meaningful but non-fatal gaps (code-switch evaluation incompleteness, under-documented ORPO baseline). These are addressable without changing the method. The paper is clearly above the 4–5 reject range but below the 7.5+ accept range reserved for papers with no significant evaluation gaps.

**Final score: 6.5** — borderline accept. The contribution is real (mechanistic insight + practical method + strong results) but the evaluation has gaps that should be resolved.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>