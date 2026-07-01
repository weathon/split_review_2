## Summary

This paper presents a large-scale empirical study (1T token pretraining, 8B parameter models, trained from scratch on 512 H100s) that systematically investigates *when* and *what kind* of reasoning data should be introduced across the LLM training pipeline (pretraining, SFT, RL). The core experimental design crosses 4 pretraining conditions (base, diverse-LDQ, high-quality-SHQ, mixed-LMQ) with 3 SFT recipes, producing 12 SFT models plus RL comparisons. The paper's central finding is an asymmetric principle: pretraining benefits most from diverse reasoning data at scale, while SFT is dominated by data quality. The paper also reports that front-loading reasoning data into pretraining creates advantages that SFT alone cannot recover, that high-quality data in pretraining has a "latent" effect unlocked during SFT, and that naively scaling SFT data can be harmful.

---

## Strengths

1. **Large-scale, controlled pretraining from scratch (1T tokens, 8B params).** This is rare and computationally expensive. Most work on reasoning data studies only the SFT or mid-training phase on top of existing pretrained models. The paper's ability to run *from-scratch* pretraining with controlled data injection is its central methodological asset, and the results from this investment are genuinely informative.

2. **Crossed experimental design (4 base models × 3 SFT recipes = 12 SFT models plus RL comparison).** This allows the paper to separate the effects of pretraining data choice from SFT data choice and to study their interaction. It is exactly the right design for answering the questions the paper poses.

3. **The asymmetric principle — diversity in pretraining, quality in SFT — is a nontrivial and actionable finding.** The evidence is reasonably clear: M_LDQ (diverse) massively outperforms M_SHQ (narrow but high-quality) at the pretraining stage (+9.09%, Table 1), and D_SHQ (high-quality) massively outperforms D_LDQ (diverse but noisy) at the SFT stage (M_res + SFT_SHQ = 44.99 vs M_res + SFT_LDQ = 31.54, Table 5). This heuristic has practical value for data allocation.

---

## Weaknesses

### Fatal

None.

### Major

1. **No measure of experimental variance.** Every experimental condition (each base model, each SFT recipe) is a single training run. The paper reports zero measures of variance — no confidence intervals, no standard deviations from the multi-run evaluations it does perform (16 runs for AIME, 4 runs for other benchmarks), no statistical significance tests. For a study that reports precise percentage claims ("+19% average gain," "+11% average gain," "+15% average gain," "+4.25% latent effect," "9.09% average gain") to two decimal places, the reader has no way of knowing whether any of these differences are within training noise. With the compute requirements of this study, multiple training runs are genuinely expensive, but the paper should (a) report evaluation variance from the multiple evaluation runs already conducted, (b) acknowledge this limitation explicitly, and (c) soften its quantitative claims to reflect the absence of uncertainty estimates.

### Minor

2. **The "19% average gain" headline conflates timing with data composition.** The headline figure (abstract: "front-loading reasoning data into pretraining is critical (19% average gain)") comes from Table 3: M_base + SFT_SHQ + RL (37.92%) vs M_LMQ + SFT_SHQ + RL (56.66%). M_LMQ differs from M_base in having 80B tokens of a *specific* reasoning data mixture (LDQ + SHQ) during pretraining, not just in timing. The +19% is the composite effect of adding reasoning data to pretraining, including the specific properties of the LMQ mix. A cleaner test of pure "timing" would hold the data composition constant and vary only the phase. The catch-up experiment (Table 4) partially addresses this, but the headline number is presented as if entirely attributable to timing.

3. **The "latent effect" mechanism is underspecified.** The paper claims that high-quality pretraining data has a "latent effect" unlocked by SFT, citing the +4.25% gain of M_LMQ over M_LDQ after SFT_SHQ (Table 4). However, M_LMQ = M_LDQ + 1.2M SHQ samples. Both models see 80B reasoning tokens during pretraining, but M_LMQ's distribution includes SHQ-style long-CoT data that M_LDQ does not contain at all. The post-SFT advantage could simply reflect that M_LMQ was exposed to SHQ-like data during pretraining, making it better prepared to absorb SHQ SFT data — i.e., data distribution overlap rather than a "latent" property of high-quality data per se. The empirical finding is valid and interesting; the causal framing is stronger than the evidence supports.

4. **Ambiguity in the "naive scaling" experiment (Table 8).** The comparison M_LDQ + SFT_LDQ (32.84) vs M_LDQ + SFT_{2×LDQ} (32.99) is described as "doubling the amount of diverse but mixed-quality data." The paper explicitly writes "(2×epochs)" in Table 4 for the epoch-doubling catch-up experiment, but uses "2×LDQ" (without "epochs") in Table 8 — suggesting this is about data volume, not epochs. However, the SFT description states models are "finetuned on 4.8M reasoning samples from D_res," and it is unclear how 9.6M distinct samples would be drawn from D_LDQ or whether this instead means 2 epochs on 4.8M samples. The distinction matters for the paper's claim that "SFT is a phase of targeted refinement, not broad data absorption."

5. **No decontamination analysis.** The paper trains on reasoning QA datasets (Nemotron-Pretraining-SFT-v1, long-CoT traces from math, code, science sources) and evaluates on standard reasoning benchmarks (GSM8K, MATH-500, AIME24/25, MMLU, MMLU-Pro, GPQA-Diamond, HumanEval, MBPP, LiveCodeBench). For a study that draws conclusions about data scaling effects — including degradation when training on more diverse SFT data — the absence of any discussion of potential benchmark contamination is a notable gap that could affect the credibility of the results.

6. **Unspecified sampling distribution for D_LMQ during pretraining.** D_LMQ = D_LDQ (268M samples) ∪ D_SHQ (1.2M samples). When drawing 80B reasoning tokens from this 269.2M-sample pool, the paper does not specify the sampling distribution across the two constituent datasets. If sampling is uniform over samples, D_SHQ (0.45% of samples) would contribute negligibly. If weighted otherwise, that should be stated. This matters for interpreting the latent effect and the combined-data results.

### Trivial

None.

---

## Nice-to-Haves

- **RL phase coverage:** Only two models (M_base and M_LMQ, both with SFT_SHQ) are compared at the RL stage. Including M_LDQ and M_SHQ would help distinguish whether the RL advantage comes from the specific LMQ recipe or from any reasoning-rich pretraining.
- **Ratio sensitivity for D_LDQ alone:** The ratio sensitivity experiments (Tables 6, 7) are performed only on M_LMQ. Testing D_LDQ alone would clarify whether the 60/40 ratio benefits come from diversity or from the combined recipe.
- **"First systematic study" framing:** The paper makes this claim in the abstract and conclusion while citing several related works (Cheng et al. 2024, Liang et al. 2025, Wang et al. 2025, Ai et al. 2025, Gandhi et al. 2025) that study similar questions. The paper's novelty is in the *scope and systematic control* of the design, not in being the first to ask the question. The framing should be more precise.

---

## Removed Points

These points were raised in the input review but are removed after verification:

- **"The 19% claim conflates several interventions" (partially):** The critic argued the 19% figure results from three confounded differences. However, the paper controls total token budget (1T for all models), so M_LMQ has 920B base + 80B reasoning vs M_base's 1T base. The comparison is a substitution of 80B general tokens with 80B reasoning tokens — a clean test of adding reasoning data to pretraining. The retained weakness (Minor point 2 above) notes only that the *timing* attribution is imprecise, which is a narrower and more justified criticism.
- **"Single training run" framed as structural/fatal:** The critic called this "the most significant weakness." While real, it is standard practice for large-scale pretraining experiments (1T tokens on 512 GPUs) and should be acknowledged rather than treated as a fatal flaw. Retained as Major with softened framing.
- **"First systematic study" as a weakness:** The critic treated this as a "minor issue" about precise framing. This is better placed under Nice-to-Haves. The paper's claim is defensible given the scope of its experimental design.
- **"Missing related works":** The critic did not claim missing works; rather noted the "first" framing is imprecise given the works cited. This is a framing issue, not a related-work gap.
- **"Base vs SFT evaluation discontinuity":** The critic noted that base models use easier benchmarks and SFT models use harder ones, making it hard to track improvement. This is a standard and necessary design choice — base models cannot solve AIME — and is not a weakness.
- **Section-by-section notes about Section 2.3 and Section 3:** These are presentation-level observations, not substantive weaknesses.

---

## Novel Insights

The harsh critic's main novel insight beyond what the paper itself provides is the observation that the "latent effect" could be explained by simple data distribution overlap (M_LMQ sees SHQ-style long-CoT data during pretraining, M_LDQ does not) rather than a deeper "latent" property of high-quality data. This is a valid alternative explanation that the paper's current framing does not adequately address or rule out. The critic also correctly flags that SFT_{2×LDQ} needs disambiguation, which the paper's inconsistent notation (using "(2×epochs)" in Table 4 but "2×LDQ" in Table 8) creates.

---

## Suggestions

1. Add a limitations paragraph that explicitly acknowledges the single-training-run design, reports evaluation variance from the multi-run evaluations already conducted, and softens precise percentage claims to reflect uncertainty.
2. Clarify Table 8: specify whether SFT_{2×LDQ} means 9.6M distinct samples or 2 epochs on 4.8M samples.
3. Provide the sampling distribution used for D_LMQ during pretraining (how the union of D_LDQ and D_SHQ is sampled to produce the 80B token budget).
4. Add a brief discussion of potential data contamination / benchmark leakage.
5. Reframe the "latent effect" narrative to acknowledge the alternative explanation of data distribution overlap, or provide evidence that distinguishes the two mechanisms.

---

MY FINAL SCORE: <score>7.5</score>
MY FINAL DECISION: <decision>Accept</decision>