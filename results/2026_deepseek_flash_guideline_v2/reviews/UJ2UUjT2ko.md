## Summary

This paper investigates how language models retrieve bound entities in-context (e.g., answering "Who loves pie?" after seeing "Ann loves pie"). It challenges the prevailing view that LMs rely solely on a positional mechanism, finding instead that they mix three mechanisms — positional (using group index), lexical (using the query entity to look up its bound counterpart), and reflexive (a direct pointer to the answer). The positional mechanism degrades in a U-shaped pattern (strong at edges, diffuse in middle), and the lexical and reflexive mechanisms compensate. A causal model combining all three achieves 95% JSS. Results are validated across 9 models (2B–72B parameters) and 10 tasks.

## Strengths

1. **Counterfactual design that surgically separates three mechanisms (§3.2).** The binding matrix design (Eq. 1) ensures that positional, lexical, and reflexive mechanisms each predict a *different* entity under interchange intervention. This goes substantially beyond prior work (Prakash et al., 2025; Dai et al., 2024), which only tested a single mechanism and could not causally distinguish between alternatives.

2. **Rigorous validation of the reflexive mechanism (§3.4).** A well-designed counterfactual where the answer entity is absent from the original input, combined with a control at layer ℓ+1 ruling out a suppression confound, cleanly distinguishes the reflexive pointer from the answer entity itself. This two-layer diagnostic goes beyond what prior work on binding mechanisms has demonstrated.

3. **Broad evaluation across 9 models and 10 tasks.** The paper tests Llama, Gemma, and Qwen families from 2B to 72B parameters, and for two models tests all 10 binding tasks. This breadth directly supports the claim that the three-mechanism mixture is a general phenomenon rather than an artifact of a single model or task.

4. **Causal model achieving 95% JSS, far above the positional-only baseline.** The combined model (Eq. 2) achieves JSS 0.95 while the positional-only baseline ("prevailing view") scores only 0.44, below even a uniform baseline of 0.50. Ablation patterns are internally consistent with the theory: ablating the lexical mechanism hurts most when t_entity=3, and ablating the reflexive hurts most when t_entity=1.

## Weaknesses

### Fatal
None.

### Major

- **The causal model (§4) is evaluated only in-distribution, limiting what it tells us about mechanism identity.** The model is trained on 70% of (i_P, i_L, i_R) combinations for n=20 entity groups and evaluated on held-out combinations from the *same* n=20 distribution. While the high JSS (0.95) shows that the Gaussian + two one-hot parameterization is a good descriptive summary, it does not test whether the three mechanisms are genuinely distinct causal circuits. A stronger test would train on n=20 and evaluate on n=10 or n=40, or on a different model family, to see if the parameterization generalizes in predictable ways. Without OOD evaluation, the causal model is more a compact *description* of LM behavior than a *test* of the three-mechanism hypothesis. The additional tasks in Appendix E still use the same model and same n=20 setup.

### Minor

- **The "three mechanisms" framing is cleaner than the evidence warrants.** A non-trivial fraction of model behavior falls into "mixed" (none of the three mechanisms' predictions match), especially for middle entity groups where "mixed" can be comparable in magnitude to lexical and reflexive effects. The paper acknowledges this (mixed predictions cluster near the positional index) and handles it via the Gaussian positional term. However, this creates a tension: if the Gaussian is absorbing residuals from an incomplete decomposition, the claim of exactly *three* mechanisms is less precise than the framing suggests. The "mixed" cases may reflect a single noisy positional mechanism rather than three cleanly separable ones.

- **The generalization experiment (§5) uses entity-less filler sentences.** The paper introduces 1,000 filler sentences that explicitly avoid containing entities. While this is a step toward more realistic inputs, real text is dense with entities that create many additional binding opportunities. The claim that findings "generalize to substantially longer inputs of open-ended text interleaved with entity groups" somewhat overstates what entity-less padding demonstrates — it shows robustness to *padding*, not to *naturalistic entity distributions*.

- **The "lost-in-the-middle" claim is speculative.** The paper suggests that a weakening lexical mechanism relative to an increasingly noisy positional mechanism "might be a mechanistic explanation" of the lost-in-the-middle effect. However, the padding experiment shows *stable accuracy* (not degradation) as padding increases, so this connection is not directly tested by the data presented.

- **Error bars are missing for mechanism classification proportions (Figure 2).** Confidence intervals are reported for JSS scores but not for the proportions of behavior classified as positional, lexical, reflexive, or mixed. Since the classification depends on which mechanism's prediction matches model output, variability across runs or samples would help assess reliability.

- **The paper does not report exact-match accuracy on the original (unpatched) binding task.** We see mechanism proportions, confusion matrices, and JSS, but not how often the model actually answers correctly on unperturbed inputs. This would help contextualize the intervention results.

- **All nine tested models are instruction-tuned variants.** The mechanistic story may differ for base (non-instruction-tuned) models. The paper does not discuss this scope limitation.

### Trivial

- The "95% agreement" phrasing in the abstract is slightly misleading: JSS (1 − JSD) is not "agreement" in the standard exact-match sense, and the 0.95 figure applies to the specific test setting with one model and task.

## Nice-to-Haves

- Test the causal model on OOD settings (different n, different model families) to determine whether the three-mechanism parameterization captures genuinely stable causal structure or is merely a flexible family that fits any position-dependent distribution.
- Deeply analyze the "mixed" cases: are they truly intermediate (model uncertain between nearby positions) or qualitatively different (model predicting entities from unrelated groups)? Characterizing residuals would strengthen or refine the three-mechanism story.
- Include a learned positional-only baseline (e.g., a learned Gaussian without lexical/reflexive terms) to better isolate the marginal contribution of the lexical and reflexive mechanisms beyond what the one-hot positional baseline shows.
- Report exact-match accuracy on the original binding task to contextualize results.

## Removed Points

- **"Prevailing view baseline is configured to be weak"** — The paper itself acknowledges prior work found "low faithfulness"; the one-hot baseline represents a literal interpretation of the positional mechanism for comparison purposes. This is not misleading, and the paper provides ablation variants (e.g., P_oracle at 0.96 JSS) as upper bounds. Demoted from consideration as a weakness.
- **Generic formatting nitpicks** from reviewers — removed as parser artifacts.
- **Missing related works concerns** — cannot be verified without external sources.
- **Missing appendix/proofs concerns** — the parser strips these sections from all papers.
- **"JSS is not agreement in standard sense"** — While technically correct, this is a trivial terminology issue, moved to trivial.
- **"What about models without instruction tuning?"** — Kept as minor scope limitation.

## Novel Insights

None beyond the paper's own contributions. The reviews largely surface the same strengths and limitations that the paper itself acknowledges, without adding a new analytical perspective not already present in the submission.

## Suggestions

1. Add OOD evaluation of the causal model (different n values, different model families) to test whether the three-mechanism parameterization captures genuinely stable causal structure.
2. Report error bars for the mechanism classification proportions in Figure 2.
3. Include exact-match accuracy on the original binding task.
4. Add a brief discussion of the instruction-tuned scope limitation and how it might affect generality.
5. Either strengthen the "lost-in-the-middle" claim with appropriate experiments or soften the language.

## Score and Decision

Given that the calibration corpus is unavailable for retrieval due to a path error, I calibrate manually against ICLR standards. The paper makes a genuine empirical contribution: the central finding is novel, well-supported by clever counterfactual methodology, rigorously validated for the reflexive mechanism, and demonstrated across substantial breadth (9 models, 10 tasks). The limitations are real but bounded — the causal model is more descriptive than predictive, the filler experiment is artificial, and the three-mechanism framing is slightly cleaner than the messy evidence. The paper is solidly above the accept threshold; it presents clear new knowledge about LM internals with sound methodology. The score reflects a strong paper whose weaknesses are addressable extensions rather than fundamental flaws.

**MY FINAL SCORE: <score>7</score>**
**MY FINAL DECISION: <decision>Accept</decision>**