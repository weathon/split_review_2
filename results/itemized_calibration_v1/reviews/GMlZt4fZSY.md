## Summary

This paper presents a data-centric framework for training sub-billion-parameter reasoning language models. The approach combines a leave-one-out (LOO) analysis to identify beneficial pre-training datasets, an influence-based data mixing method (Datamix) that weights datasets by cross-capability contributions, and a data-model co-evolution strategy for mid-training that iteratively filters training samples until convergence. Trained on 4.2T tokens drawn from ~2T curated unique tokens, MobileLLM-R1 models (140M-950M parameters) achieve competitive or superior reasoning performance compared to prior fully open-source models (OLMo-2, SmolLM2) and match Qwen3-0.6B on several benchmarks despite using only 11.7% of its training budget.

## Strengths

1. **The leave-one-out (LOO) analysis (Section 2.1, Figure 3) is genuinely informative.** Systematically removing individual datasets and measuring NLL changes on capability-probing datasets provides a principled way to disentangle data-source contributions. The finding that FineWeb-Edu acts as a cross-domain "glue" while domain-specific datasets primarily benefit their own domains is a nontrivial insight. The unexpected result that StarCoder helps math more than OpenWebMath helps code is also a genuinely interesting finding.

2. **The controlled SFT comparison (Table 2) is well-designed and provides the cleanest evidence for the pipeline's value.** By fine-tuning all baseline models on the same reasoning SFT corpus, the authors isolate the contribution of pre-training/mid-training from post-training. MobileLLM-R1* consistently outperforms OLMo-2 and SmolLM2 under identical SFT, demonstrating that the data curation pipeline produces genuinely better base models. This is precisely the kind of control that many data-curation papers omit.

3. **The post-training ablations (Table 1) are thorough and practically useful.** The staged comparison (Tulu first, reasoning second) vs. joint training, and the detailed exploration of math/science/code SFT data combinations, provides clear guidance for practitioners. The finding that scientific reasoning data transfers to math and code is nontrivial.

4. **The data-model co-evolution for mid-training (Section 3) is a novel contribution.** Iteratively using the model to filter its own training data based on influence scores, with convergence when scores approach zero, is a clean formulation with a natural stopping criterion. Figure 6's comparison showing subsampled data outperforming the original under both cross-entropy and knowledge distillation is compelling.

5. **Full openness.** The commitment to release all models, data, and training recipes is valuable and raises the bar for reproducibility in this space.

## Weaknesses

### Fatal
None.

### Major

1. **The influence-based data mixing method (Datamix, Section 2.2) lacks end-to-end validation on final benchmark accuracy.** The paper presents Datamix as a core contribution, but its only direct validation is Figure 4, which compares Datamix vs. uniform sampling using perplexity on benchmark datasets (MATH-500, GSM8K, HumanEval). While perplexity is a reasonable proxy for pre-training quality, the paper never demonstrates that using Datamix in the full pipeline (pre-training + mid-training + post-training) produces better final benchmark *accuracy* than simpler alternatives (e.g., uniform sampling or heuristic upweighting based on LOO results). Without this ablation, it is impossible to quantify how much of the overall pipeline's success comes from the influence-based mixing specifically vs. the combination of dataset selection, training budget, and well-tuned post-training. This does not invalidate the pipeline's value, but it limits what the paper can legitimately claim about this particular methodological component.

### Minor

1. **No variance or statistical significance reported for any result.** All results in Tables 1, 2, and the figures are point estimates with no confidence intervals, standard deviations, or multi-seed experiments. Given known stochasticity in LLM training and evaluation (especially at 140M and 360M scales), this makes it difficult to assess whether the reported performance gaps are significant. While single-run evaluation is common practice at this scale, the paper's core comparisons (e.g., "57.8 MATH vs. 53.0 for OLMo-2") would benefit from some indication of variance.

2. **The "benchmark-free" framing requires qualification.** The method does not directly optimize on benchmarks, but the capability-probing datasets used for influence computation are derived from training corpora that overlap substantially with benchmark domains (math, code, general knowledge). Additionally, the validation of Datamix (Figure 4) measures perplexity on actual benchmarks. The paper should acknowledge this alignment more explicitly.

### Trivial

1. **The "closed-form solution" claim (Section 2.2, line 187) is overstated.** What is presented in Eqs. 2-5 is a weighted averaging scheme for combining influence scores across checkpoints and capabilities, normalized into sampling weights. This is not a "closed-form solution" to an optimization problem in the standard mathematical sense. The method itself is reasonable, but the terminology inflates its perceived rigor.

## Nice-to-Haves

- An end-to-end ablation comparing Datamix vs. uniform sampling (and vs. a simple heuristic baseline like upweighting math/code based on LOO results) on final benchmark accuracy after the full pipeline would directly validate the marginal contribution of the influence-based mixing.
- A discussion of data repetition effects: the model trains on 4.2T tokens from ~2T unique tokens. Commentary on whether this repetition helps, hurts, or is neutral would strengthen the paper's rigor.
- The computational cost of the influence framework (training domain-specialized models to convergence at 10 checkpoints each) is not discussed. A cost-benefit analysis relative to the token savings would help practitioners assess the method's practicality.

## Removed Points

These points were flagged in the input review but are removed; treat them with caution:

- **"2T tokens claim conflates unique tokens with total training budget"**: REMOVED. The paper clearly states both numbers in the same sentence: "only ~2T tokens of high-quality data are sufficient, and pre-training with 4.2T tokens on the dataset resampled from these ~2T tokens." The claim is about data curation efficiency (identifying ~2T unique high-quality tokens), not about total training budget. The 4.2T training budget is stated transparently and explicitly. No misleading framing exists.

- **"Section 2.1 LOO analysis measures NLL, not final benchmark performance" (treated as an unsubstantiated assumption)**: REMOVED. The paper explicitly motivates this design choice: a brute-force end-to-end approach would be "computationally prohibitive and prone to overfitting to specific benchmarks." Using NLL on capability-probing datasets as a proxy is a standard and accepted approach in data curation research. The paper acknowledges the proxy nature throughout.

- **"Section 5 (Related Work) is thin"**: REMOVED per policy — missing related works should not be mentioned as weaknesses when the reviewer has no external knowledge to verify what works exist.

- **"Two prevailing assumptions framing is slightly misleading"**: REMOVED. The paper explicitly acknowledges that assumption (1) "has already been challenged by recent sub-billion-parameter reasoning models such as Qwen3-0.6B." The framing is accurate and tempered.

- **"No analysis of failure cases"**: REMOVED. The paper mentions specific failure modes (e.g., models below 400M struggle on LiveCodeBench) and provides extensive benchmark comparisons. A dedicated failure analysis section is nice-to-have but not a core weakness.

- **Formatting/parser-related complaints about garbled tables**: REMOVED as parser artifacts, not author errors.

## Novel Insights

The harsh critic's observation that the controlled SFT comparison (Table 2) is the strongest evidence for the pipeline's value is a useful distillation — the paper itself spends more narrative space on the Datamix method than on this experiment, yet Table 2 provides the cleanest causal evidence. The critic also correctly identifies that the LOO analysis finding about FineWeb-Edu acting as "cross-domain glue" is a genuinely nontrivial empirical result. Beyond these, no additional novel insights emerged from the review beyond the paper's own contributions.

## Suggestions

1. **Validate the Datamix method end-to-end** by training the full pipeline with (a) uniform sampling, (b) the proposed Datamix, and (c) a heuristic baseline (e.g., upweighting math/code based on LOO results), then comparing final benchmark accuracy. This would directly establish the marginal contribution of the influence-based mixing.

2. **Add variance estimates** (at minimum for the smaller 140M and 360M models) or discuss the stability of single-run results.

3. **Tone down the "closed-form solution" language** to accurately describe the weighted-averaging aggregation scheme.

4. **Discuss the data repetition rate** (~2x) and its implications for the reported token efficiency.

---

### Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `8QTpYC4smR.md` | 1.00 | R1 | No | Unrelated survey paper (strong reject band anchor) |
| `5kMwiMnUip.md` | 1.40 | R1 | No | Unrelated jailbreaking paper |
| `SaOxhcDCM3.md` | 3.20 | R1 | No | Self-consuming loop analysis; much narrower scope |
| `EOPLy80bBm.md` | 3.00 | R1 | No | Data pruning theory paper; not directly comparable |
| `bppG9srkpR.md` | 3.60 | R1 | No | LokiLM tech report; less rigorous |
| `Fq8tKtjACC.md` | 6.00 | R2 | Yes | "Textbooks Are All You Need" — similar in spirit (small model + curated data), but phi-1 had proprietary data and contamination concerns; this paper is more transparent and has more methodological novelty |
| `eNbA8Fqir4.md` | 6.00 | R2 | Yes | DataMan — data management for pretraining; our paper has stronger overall results but less complete validation of the specific contribution |
| `aP3OBwf8dk.md` | 6.00 | R2 | Yes | "Need a Small Specialized Language Model?" — similar topic but weaker results and writing |
| `3OyaXFQuDl.md` | 7.00 | R1 | Yes | "Smaller, Weaker, Yet Better" — stronger validation of its core claim, but narrower scope (math only, Gemma only) |
| `f4gF6AIHRy.md` | 8.00 | R1 | Yes | "Combatting Dimensional Collapse" — much stronger experimental validation (6 baselines, consistent wins), higher score reflects this |

### Score Rationale

Round 1 bracket: 6.0–7.0. Narrowing: the paper sits above phi-1 and DataMan (both 6.00) because it has more methodological novelty (LOO analysis + influence-based mixing + data-model co-evolution) and full openness, while the phi-1 paper's core method was obscured for proprietary reasons. However, it sits below "Smaller, Weaker, Yet Better" (7.00) because that paper's core contribution is fully validated through its experiments, whereas this paper's core Datamix method lacks end-to-end accuracy validation — a meaningful evidential gap. The paper's strongest evidence (Table 2) supports the *overall pipeline*, not the specific methodological novelty claimed. This places the paper solidly between 6 and 7.

## Score and Decision
MY FINAL SCORE: 6.5
MY FINAL DECISION: Accept