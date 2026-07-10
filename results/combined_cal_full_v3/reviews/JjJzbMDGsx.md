Now I have all the information needed. Let me produce the final consolidated review.

---

## Summary

This paper introduces the Language Confusion Gate (LCG), a lightweight plug-in MLP that dynamically filters inappropriate tokens during decoding to reduce language confusion in multilingual LLMs. LCG is trained via norm-adjusted self-distillation on the frozen model's own top-k/p predictions, leveraging mechanistic insights about token embedding norm bias. Evaluated across 7 models (both standard and reasoning-focused) on multiple benchmarks, LCG reduces confusion by an order of magnitude with only 0.4% computational overhead, while preserving legitimate code-switching ability.

## Strengths

- **Well-motivated, practically grounded problem.** The paper convincingly documents language confusion in state-of-the-art commercial models (Table 2: GPT-5-Chat shows 0.57% CJ and 0.67% Latin confusion; Qwen3-235B shows 2.27% CJ and 5.07% Latin confusion), establishing that this is a real, unsolved problem.

- **Clean, mechanistically motivated method design.** LCG is grounded in three concrete observations (Section 3.1–3.2): confusion is rare (~0.3% of tokens), correct-language tokens are almost always in the top-5 (99.29% within top-3), and token embedding norms systemically bias sampling toward high-resource languages. The norm-adjusted self-distillation directly operationalizes the latter two observations into a coherent training procedure — this chain from analysis to design is the paper's strongest intellectual contribution.

- **Genuinely lightweight and practical.** The measured 0.4% overhead (Section 6: 15.95ms → 15.99ms per step) and compatibility with speculative decoding (Appendix F) make this deployable in production settings where retraining-based methods are not.

- **Thorough evaluation coverage.** The paper evaluates 4 base models (Qwen3-30B, Qwen3-8B, Llama3.1-8B, Gemma3-12B) and 3 reasoning models, on FLORES+, INCLUDE, and Humaneval-XL, with separate code-switch preservation analysis, norm-adjustment ablation, comparisons against ICL/greedy/ORPO baselines, and ablation of intervention rules.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **No variance or statistical significance reported for any result.** Confusion rates in Tables 3–5 are point estimates with no confidence intervals, bootstrapped estimates, or repeated runs. At the low confusion rates measured, small differences (e.g., Latin% 0.6% vs 0.5% for Gemma3-12B; BLEU 13.2→13.4 for Qwen3-30B) could be within noise. This is most relevant for comparisons between LCG-adjusted and LCG-unadjusted, where gaps shrink. The main effect (No LCG vs LCG) is large enough to survive this concern, but the norm-adjustment ablation specifically would benefit from variance reporting.

- **The first code-switch preservation experiment (line 284) has a constrained scope.** It selects cases where the base model's English use was judged by human annotators as "natural, appropriate code-switch" and then checks whether LCG permits these tokens. This is a valid test of over-suppression but does not test whether LCG correctly handles cases where the original model was uncertain or where code-switching is intrinsically required by the prompt. The second experiment (Table 5) provides a complementary view but shows LCG can reduce code-switching below ground-truth rates for Qwen3-8B (25.90% vs 38.36%), suggesting possible over-suppression. The paper does acknowledge that the ground-truth rate is "not a ground truth optimal code-switch rate."

- **Training hyperparameters for the gate are not reported.** The 2-layer MLP is trained on ~78k samples via self-distillation, but the paper omits batch size, learning rate, optimizer (including any schedule), number of epochs, and regularization (dropout/weight decay). These details matter because the gate must generalize across 200+ languages from modest data.

- **The "No Rule" ablation (Figure 3) is presented only visually.** No numeric values for the "No Rule" condition appear in the text or in a table, making quantitative comparisons harder.

- **The ORPO baseline implementation lacks sufficient detail.** The paper states that preference pairs were synthesized "similar to Lee et al. (2025)" but does not report how many pairs were created, whether quality filtering was applied, or what the ORPO hyperparameters were. This makes it difficult to assess whether ORPO was given a fair configuration.

### Trivial

- **Table 4 caption error.** The caption reads "Effectiveness of LCG Intervention on 'No-Think' Models measured on Humaneval-XL," but the section text (line 269) and the table content describe thinking-model evaluation. This is a clear copy-paste error from Table 3's caption.

## Nice-to-Haves

- A finer-grained analysis of which language families benefit most and least from norm-adjustment — Table 1 shows Gemma3-12B has only 0.94% CJ tokens in the top 5% of norms (vs 10.74% for Qwen3-8B), which may explain differential impacts of norm-adjustment across models.
- A brief discussion acknowledging that the gate is model-specific (must be retrained for each LLM using that model's hidden states), though the lightweight training makes this feasible.

## Removed Points

These points were raised in the original review but are removed with justification:

- *"Rule (2) in Section 4.3 is circular"* — Removed. The rule checks the *model's own* high-confidence candidate sets (using non-adjusted logits with stricter thresholds), which are different from the gate's training signal (norm-adjusted logits). This is a legitimate safeguard, not a circular check.

- *"Section 4.2 edge case: all-four-active or all-zero targets"* — Removed. All-positive targets still provide a learning signal through BCE loss with sigmoid. And Symbols are always present in the candidate set (since symbols are never masked), so all-zero targets cannot occur.

- *"Section 3.2 Gemma3 norm statistics look concerning"* — Removed. This is speculation about what the numbers "should" mean for the method, not a concrete weakness.

- *"Section 1 Large Reasoning Models claim needs more evidence"* — Removed. A single reference (Guo et al. 2025) is appropriate for contextual motivation in the introduction.

- *"Section 3.3 should be more explicit about how gate handles code-switch"* — Removed. The mechanism (Symbol tokens never masked, Low-Res never masked) is clearly described in Section 4.3, which is the appropriate place.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add bootstrapped confidence intervals for confusion rates (resample over evaluation instances) for the main results, especially for LCG-adjusted vs LCG-unadjusted comparisons where gaps are small.
- Include a numeric table for the "No Rule" ablation alongside the visual presentation in Figure 3.
- Report gate training hyperparameters (optimizer, LR, batch size, epochs, regularization) in the experimental setup section.
- Correct the Table 4 caption.
- Provide more detail on the ORPO baseline: number of preference pairs, quality filtering procedures, and key hyperparameters.

---

### Calibration Report

**Round 1 anchors (bracketing):**

| Anchor | Path | Avg | Round | Itemized? | Comparison to Paper |
|--------|------|-----|-------|-----------|---------------------|
| Crosslingual Capabilities | BCyAlMoyx5 | 5.67 | R1 | Yes | Weaker: has fundamental concerns (limited language selection, novelty questioned with favorability as low as -5.69) |
| The Same but Different | NCrFA7dq8T | 6.60 | R1 | Yes | Comparable: solid methodology but narrower scope; paper under review has stronger practical contribution |
| Speculative Decoding | xOtOfdbBqK | 5.75 | R1 | Yes | Weaker: marginal improvements, missing baselines |
| MLLM Hallucination | 4z3IguA4Zg | 6.00 | R1 | Yes | Comparable: similar spirit (decoding-time mitigation) but paper under review has more thorough evaluation across more models |
| Interpolating AR+DD | tyEyYT267x | 8.00 | R1 | No | Different topic (diffusion LMs); included as extreme anchor |
| Self-Alignment | 1oijHJBRsT | 8.00 | R1 | No | Different topic (instruction following); too dissimilar for close comparison |

**Round 2 (narrowing 6.0–8.0):**

| Anchor | Path | Avg | Round | Itemized? | Comparison to Paper |
|--------|------|-----|-------|-----------|---------------------|
| Sparse MoE Language-Guided | ySS7hH1smL | 7.50 | R2 | Yes | Stronger evaluation scale but had baseline reproducibility concerns (favorability 2.11–3.76); paper under review has cleaner execution |
| LM Cascades | KgaBScZ4VI | 7.00 | R2 | Yes | Strong presentation but only tested on one base model; paper under review evaluates 7 models |
| Unified Rep Space | FrFQpAgnGE | 7.00 | R2 | Yes | Novelty questioned relative to prior work (favorability 0.97); paper under review's contribution is more distinct |

**Final score placement:**

The round-1 bracket was [5.5, 7.5]. After itemized comparison, the paper sits above the 5.67/5.75 anchors (which have clear flaws like novelty concerns and baseline issues) and is comparable to the 6.60–7.00 anchors. The paper's strengths have very high favorability (8.69–10.78 from the trained model), and all weaknesses are minor with moderate favorability (3.27–6.32). No weakness is fatal or even major. The paper lacks the kinds of severe low-favorability items seen in the 5.67 anchor (e.g., -5.69 for "contribution lacks originality"). It shares with the 7.00 anchors the profile of clear contributions with only minor gaps in presentation detail. The final score of **7.0** reflects a well-executed paper with a practical contribution and thorough evaluation, held back from higher scores by the lack of variance reporting and a few missing reproducibility details — all addressable issues.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>