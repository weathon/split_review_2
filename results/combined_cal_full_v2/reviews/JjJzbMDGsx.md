## Summary

This paper introduces the Language Confusion Gate (LCG), a lightweight plug-in MLP that filters tokens by language family during LLM decoding to reduce cross-script language confusion. The method is grounded in three empirical observations: language confusion is rare, correct-language tokens are usually within the top-3 predictions (99.29% of the time), and output token embedding norms systematically favor high-resource languages. LCG is trained via a clever norm-adjusted self-distillation procedure — debiasing logits by dividing by token embedding norms before constructing pseudo-targets — and intervenes sparsely (0.33–0.38% of tokens) with only 0.4% per-step latency overhead. Evaluations across Qwen3, Llama3.1, Gemma3, and GPT-OSS show confusion reductions by roughly an order of magnitude on the FLORES-NO-LATIN benchmark and the INCLUDE reasoning dataset, without measurable degradation on task metrics.

## Strengths

- **Clear mechanistic analysis grounding the method (Sections 3.1–3.2).** The norm decomposition (Equation 1), the observation that correct-language tokens appear within top-3 99.29% of the time at confusion points, and the norm imbalance analysis (Table 1 showing high-resource language tokens dominate the top 5% of embedding norms) concretely motivate the design. The demonstration in Figure 2 — where norm-adjusted logits surface correct-language tokens that were previously buried — is instructive and analysis-driven.

- **Norm-adjusted self-distillation (Section 4.2).** Instead of using raw model logits as pseudo-targets (which would bake in the norm bias), the training procedure debiases by dividing logits by token embedding norms before constructing targets. The ablation in Table 3 confirms this matters: LCG-adjusted consistently outperforms LCG-unadjusted across all models for both CJ% and Latin%.

- **Genuinely practical overhead.** A 0.4% increase in per-step latency (Section 6) and intervention rates of 0.33–0.38% (Section 5.3) mean the method could realistically be deployed in production. The paper reports actual production-system benchmarks, not just toy estimates.

- **Honest treatment of the code-switching tension.** Rather than ignoring the obvious objection that masking tokens by language family would break legitimate code-switching, the paper directly addresses it — with the FLORES-WITH-LATIN subset, the human-evaluated token-level preservation experiment, and the comparison against ground-truth and Claude baselines in Table 5. The result that code-switching is reduced but not eliminated is presented honestly rather than spun as an unqualified success.

## Weaknesses

### Fatal
None.

### Major

- **No statistical significance or variance reporting for any result.** All results in Tables 3, 4, and 5 are reported as point estimates with no confidence intervals, standard deviations, or error bars. This is problematic because (a) many comparisons involve very small percentages (e.g., CJ% going from 0.12% to 0.00% in Table 4, or from 0.07% to 0.00% for Gemma3 in Table 3) where differences could be within sampling noise; (b) INCLUDE accuracy differences are tiny (e.g., 71.12 vs. 70.83 for Qwen3-30B; 46.12 vs. 46.34 for Llama3.1-8B) yet used to claim "no degradation"; and (c) FLORES BLEU scores show very small variations (e.g., 13.2 → 13.4 → 13.3 for Qwen3-30B) that are within typical BLEU variance. This is a significant omission for a paper making quantitative claims about improvements and non-degradation.

- **The human evaluation supporting the 86.7% token-level code-switch preservation claim is critically underspecified.** The methodology is described in a single sentence (line 284): *"we select cases where the model's use of English was judged by human annotators to be natural, appropriate code-switch."* Missing details include: number of annotators, inter-annotator agreement, annotation guidelines, number of examples annotated, and whether annotations were conducted blindly. Human judgments of "natural code-switching" are notoriously subjective, and without these details the central claim that LCG preserves 86.7% of legitimate code-switching is not verifiable from the paper as presented.

### Minor

- **LCG operates at script-level granularity, not language-level granularity.** The gate classifies tokens into 4 script-based categories (CJ, Latin, Symbols, Low-Res), so it cannot distinguish between confusion involving same-script languages (e.g., Spanish vs. English, Hindi vs. Marathi). The paper acknowledges this in the conclusion (lines 320–321), but the abstract and introduction frame the method as addressing "language confusion" broadly without adequate caveating. Latin confusion is the most common form in the paper's own data (Table 3: Qwen3-8B shows 12.1% Latin vs. 4.5% CJ), yet LCG's response to a Latin-script error is to suppress all Latin tokens — a blunt intervention that cannot differentiate between English technical terms and actual confusion.

- **The Latin confusion evaluation is on a narrow, curated subset.** FLORES-NO-LATIN is limited to 5 target languages (Arabic, Hebrew, Korean, Thai, Chinese) and sentences whose references contain no Latin characters at all. This measures a best-case scenario where any Latin token is unambiguously an error. In real-world usage, distinguishing legitimate Latin code-switching from confusion remains unaddressed. The paper's own code-switch data (Table 5) shows LCG reduces the code-switch rate from 46.34% to 25.90% vs. a ground-truth answer rate of 38.36% — though the Claude Sonnet 4 baseline (23.29%) is slightly below LCG's rate, suggesting some over-suppression may be occurring relative to ground truth.

- **Intervention rule hyperparameters are not justified.** The thresholds for Rule (2) — (top-k=5/p=0.999) or (top-k=20/p=0.95) — determine the precision/recall trade-off for intervention timing but are stated without motivation or sensitivity analysis.

- **The key confusion point analysis (correct-language tokens within top-3 99.29% of the time) is reported only for Qwen3-8B on FLORES-NO-LATIN** (Section 3.1), without evidence that this finding generalizes across models.

- **The thinking model evaluation (Table 4) uses only coding tasks (Humaneval-XL),** where Latin character usage is expected and baseline confusion rates are already very low (CJ% of 0.12–1.50%). The marginal improvements (0.12% → 0.00%, 0.38% → 0.06%) are unlikely to be practically meaningful, especially without confidence intervals.

### Trivial
None.

## Nice-to-Haves

- A sensitivity analysis of the intervention rule hyperparameters (Rule 2 thresholds) to show the precision/recall trade-off between confusion reduction and code-switch preservation.
- An error analysis of gate failures — characterizing the cases where LCG fails to suppress confusion or incorrectly blocks legitimate tokens.
- Reporting results on the LCB benchmark (with appropriate caveats about its limitations) would help situate results in the existing literature.

## Removed Points

These points from the input review are excluded:
- Claim that the Introduction's citation of FLORES-200 and XL-Sum constitutes a "minor framing issue" about "multilingual understanding" — this is a nitpick about citation scope with no bearing on the paper's contribution.
- Characterization of the thinking model section as "filling space" — subjective editorializing, not a substantive weakness.
- Suggestion to add training-data/norm correlation from Appendix G to the main text — the appendix exists in the original submission (parser-stripped).
- Various section-by-section editorial notes (e.g., about the "No Rule" ablation, etc.) that are either acknowledged by the paper or are minor presentation points.

## Novel Insights

None beyond the paper's own contributions. The reviews confirm the paper's claimed contributions (mechanistic analysis, norm-adjusted self-distillation, practical efficiency) without adding new critical perspectives the paper itself does not already address.

## Suggestions

1. Add confidence intervals, error bars, or statistical significance tests to all main results (Tables 3, 4, 5) to make the small-percentage comparisons interpretable.
2. Provide full documentation of the human evaluation methodology: annotator count, inter-annotator agreement, annotation guidelines, number of examples, and whether annotations were conducted blindly.
3. Add a sensitivity analysis of the intervention rule hyperparameters (Rule 2 thresholds) to show how the precision/recall trade-off varies.
4. Caveat the script-level limitation more prominently in the abstract and introduction — the method's actual capability is cross-script confusion, not all language confusion.

---

### Calibration Summary

**Retrieved anchors across all rounds:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| gwZ90hFSL2.md | 1.00 | R1 | No | Unrelated paper (humanoid robots, rejected) |
| 8QTpYC4smR.md | 1.00 | R1 | No | Literature review, rejected — much weaker |
| 5kMwiMnUip.md | 1.40 | R1 | No | Jailbreaking paper, rejected — unrelated |
| fSbPwHjdDG.md | 3.00 | R1 | Yes | Causal intervention on latent language — weaker: single model, single task, poor presentation |
| UHg1xTRzZK.md | 5.00 | R1 | Yes | Rationale distillation for translation — weaker: limited novelty, missing baselines |
| r3GxWNGpSj.md | 4.75 | R1 | No | Multilingual transplantation — weaker methodology |
| T2h2V7Rx7q.md | 5.25 | R1 | No | Scaling laws for multilingual LMs — different contribution type |
| 5bUy4F59mk.md | 6.00 | R1 | Yes | Tool Decoding (plug-and-play decoding intervention) — **most structurally similar:** comparable strength, our paper has stronger analysis but similar methodological gaps |
| xOtOfdbBqK.md | 5.75 | R1 | No | Speculative decoding adaptation — different problem |
| 0JjsZC0w8x.md | 5.75 | R1 | No | Order-agnostic language modeling — different topic |
| tyEyYT267x.md | 8.00 | R1 | No | Diffusion language models — unrelated (state-of-the-art) |
| 1oijHJBRsT.md | 8.00 | R1 | No | Instruction backtranslation — different problem |
| f4gF6AIHRy.md | 8.00 | R1 | No | Submodular data selection — different problem |
| HMa8mIiBT8.md | 6.00 | R2 | Yes | Cross-lingual knowledge consistency — similar score but different contribution type |
| BCyAlMoyx5.md | 5.67 | R2 | Yes | Crosslingual knowledge barriers — weaker: lack of originality as core weakness (-3.25, -5.69) |
| i7oU4nfKEA.md | 6.25 | R2 | No | Multilingual language modeling scaling study — different methodology |
| CP6CAqxAGJ.md | 5.67 | R2 | No | Vocabulary unification — different problem |
| QiyQJqpcYe.md | 4.75 | R2 | No | Linguistic reasoning benchmark — different problem |
| ck4SG9lnrQ.md | 6.33 | R2 | No | Chinese benchmark CMMLU — different contribution |

**Round 1 bracket:** 5.5–6.5. The paper is clearly stronger than the 3.00 and 5.00 anchors (which had fundamental issues like lack of originality, single-model experiments, and severe presentation problems). It is structurally most similar to Tool Decoding (6.00, accept), a plug-and-play decoding intervention paper.

**Round 2 narrowing:** Compared against Tool Decoding (6.00) and Crosslingual Capabilities (5.67), the paper's weighted items show stronger positive contributions (strength weights 7.50–10.65 vs. similar-range strengths in the anchors) and milder negative weights (only -1.51 and -1.23 vs. -2.99 to -7.28 in the lower anchors). The core methodological novelty (norm-adjusted self-distillation, analysis-driven design) is clearer than in the anchors. The main gaps — no variance reporting and underspecified human evaluation — are fixable but non-trivial.

**Final placement: 6.0.** This paper makes a genuine contribution with a well-motivated, practical method. Its two major weaknesses (no variance reporting, underspecified human evaluation) are real methodological gaps, but they are addressable and do not invalidate the core contribution. The paper sits at the borderline-accept threshold: the community would benefit from the work, but these evidential gaps should be resolved before publication.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>