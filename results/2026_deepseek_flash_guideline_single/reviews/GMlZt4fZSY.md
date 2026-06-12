Here is my final review with the complete calibration documentation.

---

## Summary

The paper introduces MobileLLM-R1, a data-centric framework for building sub-billion-parameter reasoning language models. It proposes: (1) leave-one-out analysis and influence-based data mixing for pre-training data curation, (2) a self-evolving mid-training compression strategy that iteratively filters samples based on influence scores, and (3) a staged post-training pipeline. The headline claim is that MobileLLM-R1-950M matches or surpasses Qwen3-0.6B using only 4.2T tokens (11.7% of Qwen3's 36T), challenging the belief that small reasoning models require massive data.

## Strengths

- **Leave-one-out analysis yields genuine empirical insights.** Section 2.1.2's finding that FineWeb-Edu acts as a cross-domain "bridge" corpus, and the observation that StarCoder benefits math more than OpenWebMath benefits code, are non-obvious and valuable results for the community regardless of the downstream numbers.

- **Mid-training data compression via iterative influence filtering (Section 3) is conceptually clean and well-motivated.** The idea of using the model itself to identify and retain only positively-influential samples, terminating when influence converges to zero, is principled. Figure 6's MMLU curves showing a clear advantage for subsampled data over the original mid-training set support the approach.

- **Commitment to openness is a genuine contribution.** Releasing all datasets, model weights, training recipes, and code enables verification and follow-up work, which is especially valuable for a paper whose thesis centers on data curation.

## Weaknesses

### Major

1. **The token-efficiency comparison is confounded by data repetition and unequal model sizes.** 
   The paper's headline claim — that MobileLLM-R1-950M achieves comparable performance to Qwen3-0.6B using "only 11.7% of the tokens" (4.2T vs 36T) — has two confounds that weaken the framing. First, the paper states that 4.2T tokens are drawn from "~2T curated open-source data" that is "resampled" (Abstract, line 9; Section 6, line 400), meaning ~2× repetition of the same unique tokens. Presenting 4.2T against Qwen3's 36T as if both represent comparable learning regimes is misleading — the known diminishing returns of repeated data (Muennighoff et al., 2024) mean these are not equivalent regimes. Second, the comparison uses unequal model sizes: 950M vs ~600M parameters (58% more). A model with 58% more parameters would be expected to outperform even with fewer tokens, and the paper never disentangles parameter-driven from data-driven gains. The paper does disclose the repetition, but the 11.7% framing does not account for it, and the central quantitative claim is presented as stronger than the evidence supports.

2. **No comparison to simpler data selection baselines.** 
   The paper shows that its influence-based mixture outperforms uniform sampling (Figure 4), but does not compare to simpler, cheaper alternatives — e.g., using FineWeb-Edu alone (which the LOO analysis identifies as the single most important dataset), standard heuristic mixing ratios from prior work, or perplexity-based filtering. Without such baselines, it is unclear whether the sophisticated influence framework provides marginal benefit over simpler recipes. Since the paper's core methodological contribution is the influence-based framework, this omission significantly limits what can be concluded from the experiments.

### Minor

3. **The post-training comparison in Table 2 does not control for starting checkpoint.** 
   Table 2 compares MobileLLM-R1* (using a Tulu-3-SFT intermediate checkpoint) against baseline models using their *instruct* checkpoints, all fine-tuned on a joint reasoning SFT corpus. Baseline instruct models have undergone their own instruction-tuning procedures (different data mixtures, hyperparameters, objectives), which may interact differently with subsequent reasoning SFT. This makes it difficult to fully attribute the performance differences solely to pre-training/mid-training quality. The experiment directionally supports the claim but is not a clean isolation of the pre-training contribution.

4. **Missing compute cost accounting for data curation procedures.** 
   The paper advocates for token efficiency during training but reports nothing about the computational cost of the data curation itself: training multiple models from scratch for the LOO analysis (one per excluded dataset, plus full), training three domain-specialized models to convergence for influence computation, extracting 10 checkpoints per model, and computing Hessian-vector products at scale. Since the paper's framing is about efficiency, the total compute (FLOPs/GPU-hours) for the full pipeline would inform whether the approach genuinely saves compute or merely shifts cost from training to data preparation.

### Trivial

None.

## Nice-to-Haves

- Report the unique-token ratio (2T / 36T ≈ 5.6%) alongside the total-token ratio, and explicitly discuss how data repetition and parameter-count differences affect the comparison with Qwen3.
- Add simpler data selection baselines to Figure 4 (FineWeb-Edu alone, heuristic mixing ratios) to establish the marginal benefit of the influence framework.
- Report total compute cost (FLOPs or GPU-hours) for the full pipeline including data curation.
- Report variance or significance estimates for benchmark results.
- Include a direct comparison of MobileLLM-R1-base (without post-training) against baseline base models to isolate pre-training quality.

## Removed Points

1. **"Benchmark-free" claim is overstated** — Removed. The paper's claim is technically accurate: capability-probing datasets are constructed from training corpora (not test benchmarks), and no benchmark data is exposed during optimization. The critic's suggestion that a genuinely benchmark-free approach requires generalization to untargeted domains is scope creep beyond what the paper claims.

2. **Base model results are uninterpretable due to garbled tables** — Removed. The garbled tables (lines 295-381) are parser artifacts from failed figure-to-text extraction. The actual paper contains Figures 8 and 9 as images. Per hard rules, formatting artifacts from PDF parsing are not author errors.

3. **Various section-by-section nits (abstract clarity concerns, LOO analysis reproducibility concerns, circularity about mid-training, lack of variance estimates)** — These are either minor enough to fold into Nice-to-Haves or address issues common to papers of this type rather than specific flaws in this paper.

## Novel Insights

The harsh review's most valuable observation beyond the paper's own contributions is the framing critique of the token-efficiency comparison. The paper's central quantitative claim (11.7% of tokens) conflates data repetition (~2×) and unequal model sizes (58% more parameters), making the comparison less clean than the framing suggests. This insight — that the efficiency claim mixes multiple factors — is not explicitly discussed in the paper, and addressing it would substantially strengthen the work.

## Suggestions

1. Reframe the efficiency comparison to acknowledge data repetition and unequal model sizes explicitly. Report the ratio of unique tokens (2T vs 36T = ~5.6%) alongside the total-token ratio (11.7%), and discuss how parameter count differences affect the comparison.
2. Add simpler data selection baselines (FineWeb-Edu only, heuristic ratios) to Figure 4 to establish the marginal benefit of the influence framework.
3. Report total compute cost for the full pipeline including data curation to support the efficiency thesis.

---

## Score and Decision

**Calibration procedure.** I performed two rounds of calibration search over 13k human-reviewed ICLR papers.

**Round 1 — Bracketing.** Six queries for topic "small language model reasoning data efficiency sub-billion" across score bands (0-1.5], (1.5-3.5], (3.5-5.5], (5.5-7.5], (7.5-8.5], (8.5+]. Key anchors retrieved:

| Path | Avg Score | Band | Relevance to current paper |
|------|-----------|------|---------------------------|
| Paramanu-Ganita (v3DwQlyGbv.md) | 2.33 | 1.5-3.5 | Small math LM from scratch; much weaker analysis than MobileLLM-R1 |
| Teaching Code Execution to Tiny LMs (JVJE5yZRxm.md) | 3.00 | 1.5-3.5 | Tiny LMs for reasoning; limited results |
| The Role of Task Complexity (OW5Gf4cse1.md) | 3.00 | 1.5-3.5 | Small model emergent abilities |
| LokiLM (bppG9srkpR.md) | 3.60 | 3.5-5.5 | Technical report style |
| 100 Instances is All You Need (UoWslU6hsX.md) | 4.33 | 3.5-5.5 | LLM performance prediction |
| Small-to-Large Generalization (79ZkWgY2FI.md) | 5.25 | 3.5-5.5 | Data influence across scales |
| Scaling Relationship on Math Reasoning (cijO0f8u35.md) | 5.25 | 3.5-5.5 | Data scaling for math reasoning |
| Textbooks Are All You Need (Fq8tKtjACC.md) | 6.00 | 5.5-7.5 | Small model + curated data; similar theme but cleaner claims |
| Need a Small Specialized LM? Plan Early! (aP3OBwf8dk.md) | 6.00 | 5.5-7.5 | Small specialized models |
| Smaller, Weaker, Yet Better (3OyaXFQuDl.md) | 7.00 | 5.5-7.5 | Strong reasoning paper; well-executed |
| DiSF: Submodular File Selection (f4gF6AIHRy.md) | 8.00 | 7.5-8.5 | Clean data selection paper |

**Round 1 bracket:** 3.5 - 6.5

**Round 2 — Narrowing.** One focused query "data curation efficient pre-training small language model data quality over quantity influence function" with range (3.5-6.5). Key additional anchors:

| Path | Avg Score | Relevance |
|------|-----------|-----------|
| Rethinking Data Selection at Scale (qUJsX3XMBH.md) | 4.40 | Data selection critique; similar quality level |
| Beyond Scale: Diversity Coefficient (506Sxc0Adp.md) | 4.00 | Data quality metric paper |
| Studying Effects of Training Data on Small LMs (4xBew7kuYB.md) | 5.50 | SLM data study |
| Programming Every Example (UNxCphTxWp.md) | 6.00 | Data refinement for pretraining |
| DataMan (eNbA8Fqir4.md) | 6.00 | Data management for pretraining |

**Round 2 bracket:** 4.0 - 5.5

**Final calibration.** The current paper sits between "Rethinking Data Selection at Scale" (4.40) and phi-1 (6.00). It has genuine contributions (LOO analysis, mid-training compression, open-source release) that exceed the former, but the central claim has structural framing issues (data repetition confound, unequal model sizes) that phi-1 did not have. The missing baselines for the influence framework and missing compute cost accounting further limit what can be concluded. The paper is borderline reject — it needs significant reframing and additional experiments to support its claims convincingly.

**Score:** 4.5  
**Decision:** Reject

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>