Now let me write the final consolidated review.

## Summary

This paper presents a data-centric framework for building sub-billion-parameter reasoning language models. The contributions are: (1) a leave-one-out (LOO) analysis revealing cross-domain data interactions during pre-training, (2) an influence-based data mixing method for optimizing pre-training data mixtures without relying on benchmark data, (3) an iterative influence-based compression strategy for mid-training, and (4) a thorough post-training ablation. The authors release models, data, and training recipes. The central claim is that careful data curation enables strong reasoning in small models using only 4.2T training tokens.

## Strengths

1. **The LOO analysis (Section 2.1, Figure 3) provides genuinely useful qualitative insights.** The finding that FineWeb-Edu acts as cross-domain "glue" — its removal degrades code, math, and knowledge — and the observation that StarCoder benefits math more than OpenWebMath benefits code are non-obvious and practically informative. This is the cleanest and most compelling analysis in the paper.

2. **The controlled comparison on identical SFT data (Table 2) is the right experimental design.** By fine-tuning all baseline instruct models on the same reasoning SFT corpus, the paper isolates the contribution of pre-training and mid-training from post-training differences. MobileLLM-R1-950M* achieves 57.8 MATH / 68.5 GSM8K / 13.7 LCBv6 versus OLMo-2-1.48B's 53.0/58.8/11.4 and SmolLM2-1.7B's 41.4/50.5/7.4, despite being smaller (949M vs. 1.48B/1.71B). This is a clean and fair comparison.

3. **The post-training ablation (Table 1) is thorough and yields actionable findings.** The staged approach (Tulu-3 first, then reasoning data) consistently outperforms joint training. The honest acknowledgment that reasoning data trades off with factual knowledge retention (MMLU drops when math/code data is added) reflects careful experimentation and transparency.

4. **The paper tackles a genuinely important problem.** Building capable small reasoning models for on-device deployment is a pressing practical challenge, and the emphasis on data quality over brute-force scaling is a healthy direction.

5. **The paper commits to releasing models, data, and code,** which would be valuable to the community.

## Weaknesses

### Fatal
None.

### Major

1. **The influence-based data mixing method (Section 2.2) is validated only by perplexity on downstream benchmarks, not by accuracy.** This is the paper's central methodological contribution for pre-training. Figure 4 shows that the influence-based mixture ("Datamix") achieves lower perplexity than uniform sampling on benchmarks including MATH-500, GSM8K, and HumanEval. However, the paper never shows whether this perplexity improvement translates into better *accuracy* on these same benchmarks. The controlled comparison in Table 2 validates the *full pipeline* (pre-training + influence-based mixture + mid-training + post-training), but provides no ablation isolating whether the influence-based mixture specifically — as opposed to uniform sampling or a simpler heuristic — contributed to the accuracy gains. Without this, the central methodological contribution lacks a direct experimental demonstration of its value on the task performance the pipeline is designed to maximize.  
   *Evidence:* Figure 4 reports perplexity only; Table 2 compares full pipelines, not pre-training mixture strategies.

2. **The mid-training compression evaluation is limited to MMLU (Figure 6) and does not assess the effect on reasoning benchmarks.** Given that the paper's focus is reasoning (math and code), showing compression's effect only on MMLU (a knowledge benchmark) leaves an important gap. The effect on MATH, GSM8K, and HumanEval should be reported.  
   *Evidence:* Figure 6 and its table show only MMLU scores.

### Minor

3. **The actual data mixture ratios derived from influence scores are not reported.** Equations (4)–(5) describe how sampling weights are computed, but the numerical per-dataset weights (whether FineWeb-Edu was upweighted by 2× or 5×, whether Wikipedia was downweighted, etc.) are never shown. This information is critical for reproducibility and for understanding the method's practical impact.

4. **The Ask-LLM judge model used for constructing capability-probing datasets is not named.** Section 2.1.1 describes hierarchical rejection sampling using the Ask-LLM paradigm but never specifies which model was used as the judge. This matters because the judge's own capabilities and biases directly shape the probing datasets that drive the entire data curation pipeline.  
   *Evidence:* Section 2.1.1 (line 105) references only "the Ask-LLM paradigm (Sachdeva et al., 2024)" without naming the model.

5. **No analysis of influence score reliability.** Influence functions are known to be sensitive to Hessian approximation quality, model convergence, and checkpoint selection. The paper trains three domain-specialized models and computes influence at 10 checkpoints each, but provides no validation or diagnostic of the reliability of these estimates (e.g., variance across checkpoints, sensitivity to the approximation method).  
   *Evidence:* Section 2.2 describes computation (Eqs. 2–5) but no reliability analysis.

6. **No dedicated limitations section.** The abstract promises to "share both the insights and the pitfalls encountered along the way," but the main text does not deliver on this — the only mention of "pitfall" is a reference to Bender & Koller (2020). The paper would benefit from a frank discussion of potential limitations (e.g., computational overhead of influence computation, sensitivity to probing dataset construction, generalization beyond studied model sizes).

### Trivial
None.

## Nice-to-Haves

- **Ablate the influence-based mixture on accuracy.** The single highest-leverage experiment would be to compare the full pipeline (influence-based pre-training mixture → mid-training → post-training) against a pipeline with uniform pre-training sampling (everything else held constant) on accuracy metrics (MATH, GSM8K, HumanEval). This would directly validate the core claimed contribution.
- The paper could report confidence intervals or run-to-run variance, although single-run evaluation is standard at this scale.
- Reporting the total compute budget (GPU-hours or FLOPs) for the full pipeline, including the overhead of influence computation, would strengthen the efficiency claims.

## Removed Points

These points were raised in the input review but are removed with justification:

- **"11.7% token framing is rhetorically deceptive"** — Removed. The abstract explicitly states "4.2T tokens on the dataset resampled from these ~2T tokens." The 11.7% compares trained tokens to trained tokens, which is standard. There is no evidence that Qwen3's 36T tokens are unique versus trained tokens. The paper is transparent about the resampling.
- **"Garbled results tables prevent verification of core claims"** — Removed per instructions (formatting artifacts are parser issues, not paper problems). The original PDF tables and figures convey the correct data; the extracted text corruption does not reflect on the paper.
- **"Closed-form solution is never shown"** — Removed as factually incorrect. Equations (4)–(5) in Section 2.2 mathematically specify the closed-form solution for computing dataset sampling weights.
- **"Missing appendix content" / "Table 5 is in the appendix"** — Removed per instructions (parser strips appendix sections from all papers).
- **"AIME score not shown in tables"** — Removed per parser artifact rule. The garbled tables do not reflect the original paper structure.
- **"Missing related works"** — Removed per instructions (do not mention missing related works).
- **"No error bars"** — Demoted to Nice-to-have; single-run evaluation is standard for large-scale pre-training experiments.

## Novel Insights

The most insightful observation from the reviews concerns the fundamental evidential gap in the paper: although the paper presents an elaborate influence-based data mixing methodology as its core contribution, the experimental validation is misaligned with the claimed contribution. The LOO analysis (Section 2.1) is convincingly validated with clear cross-domain insights. The influence-based mixing (Section 2.2) is validated only on perplexity — a proxy that, while suggestive, falls short of establishing the method's value for downstream task accuracy. The paper's strongest empirical evidence (Table 2) validates the full pipeline but, by design, does not isolate the influence-based mixing. This creates a disconnect between the paper's claimed contribution and its experimental support. This observation is not a fatal flaw — the paper still demonstrates that its overall pipeline produces strong models — but it is a structural weakness that the authors should address directly rather than relying on the perplexity proxy as sufficient validation.

## Suggestions

1. Add an ablation comparing influence-based pre-training mixture vs. uniform pre-training sampling (all else equal) on accuracy metrics for MATH, GSM8K, and HumanEval. This single experiment would close the central evidential gap.
2. Report the actual numerical mixture ratios (per-dataset sampling weights) derived from the influence scores.
3. Extend the mid-training compression evaluation (Figure 6) to include reasoning benchmarks (MATH, GSM8K, HumanEval) in addition to MMLU.
4. Name the Ask-LLM judge model used for probing dataset construction.
5. Add a limitations section that discusses computational overhead, sensitivity of influence estimates, and scope of generalization.
6. Make explicit which specific model the "DeepSeek-R1-Distill-Qwen-1.5B" comparison refers to and provide the actual numbers.

## Score and Decision

<score>6</score>
<decision>Borderline Accept</decision>