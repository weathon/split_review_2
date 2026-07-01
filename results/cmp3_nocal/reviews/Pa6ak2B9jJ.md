## Summary

This paper proposes AUTO-RT, a reinforcement learning framework for automated jailbreak strategy exploration in LLMs. It decomposes the attack model into a strategy generator (AM^g) and a strategy rephraser (AM^r), and introduces Dynamic Strategy Pruning (DSP) to terminate redundant/inconsistent exploration branches, and Progressive Reward Tracking (PRT) with a First Inverse Rate (FIR) metric to select appropriately weakened downgrade models for reward shaping. The framework is evaluated on 16 white-box and 2 black-box LLMs.

## Strengths

- **Hierarchical decomposition of the attack model into strategy generation (AM^g) and strategy rephrasing (AM^r) is a sensible architectural choice** (Section 2.2). Separating high-level strategy search from instantiation onto specific toxic behaviors is a genuine structural improvement over direct query generation, and it cleanly motivates why strategy-level exploration is worth studying separately.

- **Dynamic Strategy Pruning (DSP) is straightforward and clearly motivated** (Section 2.3.2). Inserting intermediate checkpoints for diversity and consistency constraints, terminating redundant/inconsistent branches early, and propagating a penalty is clean. The ablation (Table 2) shows consistent improvements over the RL baseline across all tested models.

- **The FIR metric for downgrade model selection is the paper's most distinctive empirical finding** (Section 2.3.3, Figure 4). The insight that there is a "sweet spot" of weakening — before the model's safety boundaries become non-monotonic — is nontrivial, and Figure 4's demonstration that selecting the model before the FIR spike yields the best attack performance is compelling.

- **The evaluation covers 16 white-box models across 6 model families**, which is a broad scope for this literature, and the ablation study (Table 2) provides credible evidence that both DSP and PRT contribute positively relative to the basic RL baseline.

## Weaknesses

### Fatal
None.

### Major

- **The ASR\(_{\text{st}}\) metric selects the top 100 strategies based on their performance on the test set T\(_{\text{st}}\) — this is a form of test set leakage** (Section 3.1, Equation 6). The metric computes each strategy's ASR on T\(_{\text{st}}\), ranks by it, selects the top 100, and then averages their ASR on the *same* T\(_{\text{st}}\). This means the test set is used both to select which strategies count and to compute the reported number. This inflates absolute ASR numbers and can differentially benefit methods that produce more diverse strategies (since a larger pool increases the chance that some strategies will score well on the test distribution by chance). The correct protocol would select the top 100 based on a held-out validation split and evaluate only on T\(_{\text{st}}\), or additionally report the average over *all* generated strategies. This concern directly affects every effectiveness number in Tables 1 and 2. While the relative ordering between methods may be partially preserved, the absolute values and the magnitude of claimed gains cannot be taken at face value in the current form.

### Minor

- **The claim that AUTO-RT "consistently achieves the highest ASR\(_{\text{st}}\) across a wide range of models" is overstated.** Table 1 shows three cases that contradict this: Mistral 7B (IL = 54.88 vs AUTO-RT = 52.65 — AUTO-RT is worse), Gemma 2 9B (RL = 44.85 vs AUTO-RT = 44.80 — effectively a tie), and R2D2 (FS = 27.18 vs AUTO-RT = 12.45 — AUTO-RT is substantially worse). The Mistral and Gemma 9B results are not acknowledged in the text. While AUTO-RT wins on the majority of models, the claim should be qualified.

- **The comparison against human-based methods (Table 3) weakens the paper's effectiveness narrative.** AutoDAN achieves ASR\(_{\text{rst}}\) = 55.23 vs AUTO-RT = 38.38 — a gap of nearly 17 percentage points in first-round attack success. The abstract's claim of "significantly improves success rates (by up to 16.63%)" cannot be benchmarked against the strongest available method (AutoDAN) since AUTO-RT underperforms it by a larger margin. The paper's genuine strength here is in sustained attack capability (DeD: AUTO-RT = 38.19 vs AutoDAN = 17.88), and the framing should foreground this rather than suggesting uniform superiority.

- **The black-box evaluation is too thin to support generality claims** (Section 3.3.4). Only 2 models are tested, absolute ASR values are low (~14–15%), and the comparison set excludes human-crafted baselines. The theoretical containment assumption of PRT (Figure 2) — that the downgrade model's unsafe region contains the target model's unsafe region — has no empirical verification when the downgrade model is constructed via ICL on a *different* model.

- **The SeD value for AUTO-RT is left blank in Table 3 with no explanation.** This omission needs justification, especially since the paper emphasizes diversity as a key evaluation dimension.

### Trivial

- **Notation inconsistency in Equation 3.** The symbols \(\text{AM}_g^d\) and \(\text{AM}^\tau\) are used without explicit definition in the main text, while the paper otherwise uses \(\text{AM}^g\) and \(\text{AM}^r\). This makes the equation harder to parse.

## Nice-to-Haves

- Provide confidence intervals or variance estimates for the ASR numbers, especially for cases where AUTO-RT only slightly edges the baseline (e.g., Llama 3 8B: 15.00 vs RL 14.55).
- Include a table of example generated strategies (with their ASR) to give intuition about what the strategy space looks like and whether the method discovers genuinely novel attack templates.
- The paper could discuss whether optimizing the shaped reward \(R_s\) (Equation 4) could theoretically lead to suboptimal policies, given that it departs from potential-based reward shaping; the paper acknowledges this but does not analyze it formally.

## Removed Points

These points were raised in the input review but are removed for the following reasons:

- *PRT reward shaping may not preserve optimal policy* — the paper explicitly acknowledges this (line 109) and explains how FIR-based downgrade model selection addresses it; the criticism does not add new information.
- *Downgrade model construction underspecified* — the paper states that details are in the appendices (B, D), which are standard practice to defer; per policy, missing appendix details are not treated as weaknesses.
- *Dataset overlap between HarmBench and AdvBench* — the paper uses HarmBench for evaluation and AdvBench for downgrade model construction; these are explicitly stated as different benchmarks, so the concern is unfounded.
- *DeD metric / defense construction underspecified* — deferred to appendix; standard practice.
- *"16.63%" claim not traceable* — the number appears with a footnote marker in the abstract (<sup>1</sup>); footnote content is stripped by the parser and may contain the derivation.
- *IL baseline conflation with hierarchical decomposition* — implementation details are deferred to Appendix B.
- *Violin plots only show AUTO-RT vs RL* — the paper's text (line 189) explicitly states it is comparing AUTO-RT and RL; the scope is clear.
- *Reproducibility nitpicks about hyperparameters, training logs, etc.* — standard practice to defer to appendix.
- *Statistical significance / variance missing* — demoted to Nice-to-Have since single-run evaluation is common in this literature and the criticism is generic.

## Novel Insights

None beyond the paper's own contributions. The input review's most useful analytical contribution is the identification of test-set leakage in the ASR\(_{\text{st}}\) metric — a genuine methodological issue that the paper does not address. The observation that the FIR-based downgrade model selection (Figure 4) is the paper's most distinctive empirical finding also sharpens where the paper's core novelty lies.

## Suggestions

1. **Fix the ASR\(_{\text{st}}\) metric.** Partition T\(_{\text{st}}\) into a validation split (for top-100 selection) and a true held-out test split (for reporting). Alternatively, report the average ASR over *all* generated strategies as a supplementary metric. This one change would resolve the most serious credibility concern.
2. **Recalibrate the claims.** Qualify the "consistently achieves the highest ASR" statement to acknowledge Mistral 7B, Gemma 2 9B, and R2D2. In Table 3, frame the contribution as being about *sustained* attack capability (DeD) where AUTO-RT leads, and explicitly state that AutoDAN outperforms on first-round ASR.
3. **Fill in the blank.** Provide the missing SeD value for AUTO-RT in Table 3, or explain why it is omitted.
4. **Expand black-box evaluation** with more models and human-crafted baselines, or explicitly scope the generality claims to settings where the downgrade model can be meaningfully constructed.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>