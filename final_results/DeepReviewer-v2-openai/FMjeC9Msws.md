## Summary
This paper presents a large-scale empirical study (400,000+ GPU-hours) on reinforcement learning (RL) compute scaling for large language models (LLMs). The authors propose a sigmoidal compute-performance curve (Eq. 1) to model RL validation performance as a function of training compute, enabling extrapolation from smaller-scale runs. Through extensive ablations on an 8B dense model on math verification tasks, they identify which design choices affect asymptotic performance (A) versus compute efficiency (B). They consolidate their findings into SCALERL, a recipe combining existing components (PipelineRL, CISPO loss, FP32 precision, prompt-level averaging, batch-level normalization, zero-variance filtering, and No-Positive-Resampling). SCALERL is validated up to 100,000 GPU-hours, demonstrating predictable scaling that aligns with extrapolated curves, and achieves competitive asymptotic performance (A=0.61) with higher compute efficiency than compared baselines.

The paper's primary strength is its systematic methodology and the scale of compute invested. However, key weaknesses include: (1) overclaiming novelty ("first" framework) without external verification, (2) missing multi-seed variance estimates for all fitted scaling parameters, (3) undefined symbols in key equations (Eq. 4's T, Eq. 3's index typo) that harm reproducibility, (4) overgeneralized claims about design choices affecting efficiency vs. asymptote beyond the tested setting, and (5) no dedicated limitations section. External literature verification was unavailable in this run (Retrieval-Disabled Mode); novelty claims are deferred for manual verification.

## Strengths
**S1. Massive compute investment and systematic methodology.** The paper's primary strength is the unprecedented scale (400,000+ GPU-hours) and systematic approach to studying RL compute scaling. Rather than proposing a single novel algorithm, the authors conduct a principled, stage-wise empirical investigation: first ablating individual components at moderate scale (3.5k-4k GPU-hours), then validating the best combination through leave-one-out experiments at 16k GPU-hours per run, and finally scaling the winning recipe (SCALERL) to 100,000 GPU-hours. This staged methodology is a model for how to conduct empirical research on RL compute scaling.

**S2. Clear sigmoidal framework for RL compute scaling.** The parametric form in Eq. (1) — decomposing performance into asymptotic ceiling (A) and compute efficiency (B) — is well-motivated. Unlike power-law fits that can produce unbounded extrapolations, the sigmoid naturally captures saturating returns for bounded metrics such as pass rate. The framework gives practitioners a concrete tool to compare RL methods along two interpretable axes rather than at isolated compute budgets. The validation in Figure 1 (extrapolating from 50k to 100k GPU-hours) provides compelling evidence that the sigmoid fit works for stable recipes.

**S3. Transparent and well-validated component ablation.** The leave-one-out experiments (Figure 5) provide rigorous validation that each component of SCALERL contributes positively. This is significantly more informative than the common practice of reporting only aggregate gains over a baseline. The re-fit procedure (fixing A across runs to compare B values) is a thoughtful way to isolate efficiency differences when asymptotic performance is similar.

**S4. Honest treatment of generalization limitations.** The paper explicitly acknowledges (Section 7) that a full characterization of generalization is beyond its scope and that the primary results are on in-distribution validation. This transparency is commendable and should be preserved, though the abstract and introduction could better align with this bounded scope.

**S5. Reproducibility-oriented release.** The authors release a code repository for curve-fitting at www.devvrit.com/scalerl-curve-fitting, which facilitates future research on compute-performance scaling curves.

## Weaknesses
### W1. Missing statistical variance undermines parameter comparisons (Critical)

The entire scaling analysis — all fitted A and B parameters across all methods and ablations — is based on single-seed runs. No confidence intervals, standard errors, or significance tests are reported for any of the scaling parameters. This is a critical gap because:
- In the LOO comparison (Figure 5), SCALERL's B=2.01 vs LOO-prompt-lvl-adv-norm's B=1.82 — the difference of 0.19 could easily fall within the noise of a single run.
- The paper's central claim — that SCALERL has "the highest compute efficiency" — rests on B value comparisons without uncertainty quantification.
- The MiniMax recipe achieves the same asymptotic A=0.610 as SCALERL (Figure 2 table), so without error bars the reader cannot determine whether the observed efficiency differences are reliable.

**Required action:** Run at least 2-3 seeds for a representative subset (SCALERL, MiniMax, base DAPO, one LOO variant) and report mean ± std for fitted A and B. If multi-seed runs are infeasible at full scale, perform a bootstrap analysis on the existing validation trajectory to estimate parameter uncertainty.

### W2. Overclaimed novelty and scope (Major)

**W2a. "First" claims unverifiable without retrieval.** The abstract claims "the first large-scale systematic study" and "first principled framework." Due to Retrieval-Disabled Mode, external literature verification is unavailable. However, even assuming these claims hold for the exact formulation, the wording should be qualified: "To our knowledge, the first systematic study that defines a parametric compute-performance curve for RL in LLMs."

**W2b. SOTA claim is partially inconsistent with reported data.** Figure 2 shows SCALERL (A=0.610) and MiniMax (A=0.610) achieving identical asymptotic pass rates. The claim "SCALERL surpasses all other methods" and "establishes a new state-of-the-art" conflates efficiency (B) with asymptotic performance (A). SCALERL has higher compute efficiency (B=1.97 vs 1.77) but the same asymptote. The text should clearly separate these two dimensions rather than claiming general superiority.

**W2c. "Embracing the Bitter Lesson" claim is conceptually mismatched.** The Bitter Lesson (Sutton, 2019) refers to general methods (search, learning) outperforming hand-crafted domain knowledge at scale. The paper applies this label to the observation that some RL recipes that appear better at small compute become worse at large compute. This is a valid observation but is qualitatively different from the Bitter Lesson, which is about the *nature* of scalable methods, not about comparing different fixed recipes. Using this framing overstates the paper's theoretical contribution.

### W3. Reproducibility gaps in method description (Major)

**W3a. Undefined symbol in Eq. (4).** The CISPO loss uses a normalization factor 1/T where T is never defined. The reader cannot determine whether T is total tokens, per-prompt tokens, or another quantity. This directly prevents exact reproduction.

**W3b. Summation index error in Eq. (3).** The outer sum uses index t over G (number of completions) while the inner sum also uses t over |y_i| (token positions per completion). The outer sum should use i, not t. While the intended meaning can be inferred, this error reduces confidence in the mathematical rigor.

**W3c. Missing hyperparameter values.** The SCALERL loss uses `min(ρ_{i,t}, ε)` where ε is never specified in the main text. The interruption length threshold (14,336 tokens for the base configuration) is specified in the Training Regimen paragraph, but the ε value for importance sampling truncation, the clipping thresholds (ε⁻, ε⁺), and the batch-level advantage normalization constant ε in Eq. (2) are not given.

**W3d. Instability conditions not disclosed.** Section 3 mentions that "some experimental choices destabilize beyond this scale" but does not name which choices or describe the failure mode. This information is critical for practitioners building on this work.

### W4. Generalizability limitations understated (Major)

The paper's experiments are confined to:
- One model family (Llama-based 8B dense, one MoE variant)
- One task domain (verifiable math, with preliminary multi-task results)
- One reward type (binary pass/fail from ground-truth answers)
- One training data distribution (Polaris-53k)
- Single seed runs

The three key principles listed in the introduction ("RL Performance Ceilings are Not Universal," "Embracing the Bitter Lesson," "Re-evaluating Common Wisdom") are presented as general findings but are derived entirely from the math 8B setting. The paper acknowledges generalization limitations in the conclusion but the headline claims in the introduction do not carry these caveats. The principles should state "In our setting (8B math verification tasks)" or be hedged accordingly.

### W5. Lack of dedicated limitations section (Minor)

The conclusion discusses generalization but does not have a structured limitations section. Readers must extract limitations from scattered paragraphs. A dedicated "Limitations" subsection should be added covering: single-seed results, single-task domain, unknown applicability to dense/learned reward models, sensitivity of the sigmoid fit to the early-data exclusion rule, and the fact that validation is in-distribution (not out-of-distribution generalization).

### W6. Related work positioning is unnecessarily dismissive (Minor)

The claim that "none of these work study scaling properties" is too categorical. ProRL's prolonged training analysis does study compute scaling effects (16K GPU-hours), and LitePPO's ablation framework is directly relevant to the methodology. The paper should engage more constructively with these works by: (a) explaining why a parametric sigmoid fit provides value beyond the analyses in ProRL/LitePPO, and (b) discussing points of agreement or disagreement on specific design choices.

### W7. Figure 1's AIME-24 downstream trend (Verification needed)

Figure 1b shows AIME-24 pass rate following a similar scaling trend as the in-distribution validation. However, the AIME-24 evaluation appears to use the same checkpoints as the validation curve. Since the model is trained on math problems (Polaris-53k), and AIME competition problems come from a similar distribution, this may overestimate generalization to truly out-of-distribution tasks. The authors should clarify whether the AIME-24 results are from the same evaluation pipeline and whether any AIME problems overlap with Polaris-53k training data.

### W8. Inference cost and practical value not discussed (Minor)

The paper focuses on training compute (GPU-hours) but does not discuss inference cost, which is critical for practical deployment. SCALERL uses 16 generations per prompt for evaluation and 8-16 generations during training. The total compute includes both training and generation. A breakdown of training vs. generation compute would help practitioners understand the true cost of the recipe.

## Score
**Final Score: 6/10**

**Rationale:** The paper makes a strong empirical contribution through its systematic methodology, massive compute investment (400,000+ GPU-hours), and clear sigmoidal framework for analyzing RL compute scaling. However, the score is constrained by: (1) the absence of multi-seed statistical variance for all scaling parameters, which undermines the reliability of the central efficiency comparisons, (2) overclaimed novelty and scope in the framing, (3) reproducibility gaps in key equations and missing hyperparameters, and (4) the unknown generalizability beyond the tested setting (8B dense math tasks). The paper's primary value is as a methodological template and empirical demonstration; its scientific conclusions about specific parameter values would be strengthened significantly by adding variance estimates and broader validation. External literature verification was unavailable in this run (Retrieval-Disabled Mode), so novelty claims require manual verification before final acceptance.

---

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: No predictive scaling methodology for RL in LLMs]
     |
     v
[Approach: Sigmoidal compute-performance framework (Eq. 1)]
     |   R_C = R_0 + (A - R_0) / (1 + (C_mid / C)^B)
     |   A = asymptotic performance ceiling
     |   B = compute efficiency (scaling exponent)
     |   C_mid = midpoint compute
     |
     v
[Empirical Study: 400K+ GPU-hours on 8B dense, math verification]
     |
     |--- Stage 1: Ablate design choices (3.5k-4k GPU-hr each)
     |       |--- Loss type (DAPO vs GSPO vs CISPO)
     |       |--- FP32 precision for logits
     |       |--- Loss aggregation (sample vs prompt vs token)
     |       |--- Advantage normalization (prompt vs batch vs none)
     |       |--- Zero-variance filtering
     |       |--- Adaptive prompt filtering (No-Positive-Resampling)
     |
     |--- Stage 2: Consolidate into SCALERL, LOO ablation (16k GPU-hr each)
     |       |--- SCALERL: PipelineRL-8 + CISPO + FP32 + prompt-avg +
     |       |             batch-norm + zero-var filter + No-Pos-Resampling
     |       |--- LOO variants (revert one component at a time)
     |
     |--- Stage 3: Scaling validation (50k-100k GPU-hr)
     |       |--- 8B dense to 100k GPU-hr ✓ fit aligns with extrapolation
     |       |--- 17Bx16 MoE to 50k GPU-hr ✓ fit aligns
     |       |--- Longer contexts (32k tokens) ✓
     |       |--- Larger batches (2k prompts) ✓
     |       |--- Multi-task (math + code) ✓ preliminary
     |
     v
[Claim: SCALERL scales predictably and achieves SOTA efficiency]
     |
     |--- Evidence: Figure 1 extrapolation (50k->100k) ✓
     |--- Evidence: Figure 2 cross-recipe comparison (B=1.97) ✓
     |--- Evidence: Figure 5 LOO comparison (highest B=2.01) ✓
     |
     v
[Key Gaps]
     |--- No multi-seed variance for A/B parameters ⚠
     |--- Single setting (8B math) for most claims ⚠
     |--- In-distribution validation only ⚠
     |--- Unverified novelty claims (Retrieval-Disabled Mode) ❓
```

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority 0 (Must fix before acceptance)
┌─────────────────────────────────────────────────────────────────┐
│ W1: Missing variance estimates                                 │
│ Problem: All A/B values from single-seed runs, no error bars    │
│ Fix: Add 2-3 seeds for subset + bootstrap analysis on existing  │
│       trajectories                                              │
│ Expected gain: Statistical credibility for efficiency ranking   │
└─────────────────────────────────────────────────────────────────┘
         │
         v
Priority 1 (Must fix)
┌─────────────────────────────────────────────────────────────────┐
│ W3: Reproducibility gaps                                        │
│ Problems: Eq.(4) undefined T, Eq.(3) index typo, missing ε     │
│ Fix: Define T, correct Eq.(3), specify all hyperparameters      │
│ Expected gain: Implementable by independent researchers          │
└─────────────────────────────────────────────────────────────────┘
         │
         v
Priority 2 (Strongly recommended)
┌─────────────────────────────────────────────────────────────────┐
│ W2: Overclaimed novelty/scope                                   │
│ Problems: "First" claims, conflated SOTA, Bitter Lesson misuse  │
│ Fix: Add qualifiers, separate efficiency from asymptotic claims │
│ Expected gain: Aligned claims with evidence; less reviewer pushback│
└─────────────────────────────────────────────────────────────────┘
         │
         v
Priority 3 (Recommended)
┌─────────────────────────────────────────────────────────────────┐
│ W4+W5: Generalizability bounds and limitations section          │
│ Fix: Add "In our setting" caveats to headline principles;       │
│       add dedicated limitations subsection                      │
│ Expected gain: Honest scope prevents misuse of findings         │
└─────────────────────────────────────────────────────────────────┘
         │
         v
Priority 4 (Quality improvement)
┌─────────────────────────────────────────────────────────────────┐
│ W6+W7+W8: Related work, AIME clarification, inference cost      │
│ Fix: More constructive related work, AIME distribution note,    │
│       training/inference compute breakdown                      │
└─────────────────────────────────────────────────────────────────┘
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
RL Compute Scaling for LLMs (Root)
│
├── Branch 1: Predictive Scaling Frameworks
│   ├── Leaf 1.1: Parametric scaling curves (this paper)
│   │   └── Sigmoidal compute-performance fit (Eq. 1)
│   │   └── A/B parameter decomposition
│   │   └── Early-data exclusion for fit stability
│   │
│   ├── Leaf 1.2: Pre-training scaling laws
│   │   └── Kaplan et al. 2020 — Power-law scaling
│   │   └── Hoffmann et al. 2022 — Chinchilla scaling
│   │   └── Owen 2024 — Compute-optimal frontier
│   │
│   └── Leaf 1.3: Empirical RL scaling studies
│       └── ProRL (Liu et al. 2025a) — Prolonged RL fine-tuning
│       └── LitePPO (Liu et al. 2025c) — Ablation framework
│       └── Vattikonda et al. 2026 — Statistical diagnosis
│
├── Branch 2: RL Algorithms for LLMs
│   ├── Leaf 2.1: Group/off-policy methods
│   │   └── GRPO (Shao et al. 2024) — Group-relative advantages
│   │   └── DAPO (Yu et al. 2025) — Asymmetric clipping
│   │   └── CISPO (MiniMax et al. 2025) — Truncated IS + PG
│   │   └── GSPO (Zheng et al. 2025a) — Sequence-level IS
│   │
│   ├── Leaf 2.2: Asynchronous training setups
│   │   └── PPO-off-policy-k (used by Qwen3, ProRL)
│   │   └── PipelineRL-k (Piche et al. 2025, Magistral)
│   │
│   └── Leaf 2.3: Stability & efficiency techniques
│       ├── FP32 precision at LM head (MiniMax et al. 2025)
│       ├── Zero-variance filtering (Seed et al. 2025)
│       ├── No-Positive-Resampling (An et al. 2025)
│       └── Forced interruption length control
│
└── Branch 3: Evaluation & Generalization
    ├── Leaf 3.1: In-distribution validation (this paper)
    │   └── Held-out prompts from training distribution
    │   └── Pass rate at mean@16
    │
    └── Leaf 3.2: Downstream benchmarks
        ├── AIME-24 (this paper)
        └── Math reasoning benchmarks (broader literature)
```

### Novelty Verification & Deferred Claims

Due to Retrieval-Disabled Mode in this run (external paper search unavailable after the configured provider returned missing_api_token), the following critical novelty-related assessments are **deferred for manual verification**:

| Claim | Status | Required Verification |
|-------|--------|---------------------|
| "First large-scale systematic study of RL compute scaling in LLMs" | Deferred | Check ProRL, DeepSeek-R1 technical report, and concurrent work for overlap |
| "First principled framework with sigmoidal compute-performance curves" | Deferred | Check whether any prior work proposes similar parametric forms for RL |
| "SCALERL establishes new state-of-the-art" | Partially verifiable from reported data | MiniMax achieves same A=0.610; efficiency advantage (B=1.97 vs 1.77) needs variance to confirm |
| "None of these work study scaling properties" | Deferred | Requires reading ProRL and LitePPO for their claims about scaling |

**Recommendation for authors:** Add a comparison table with ProRL, LitePPO, and DeepSeek-R1 covering: compute budget, model size, task type, performance metric, whether a parametric scaling curve is reported, and whether in-distribution validation vs. downstream evaluation is used. This will make the novelty claim self-contained and verifiable without external retrieval.

---

**Post-Revision Target:** [7, 8]/10 — achievable by addressing W1 (multi-seed variance for representative subset), W3 (reproducibility fixes), and W2 (claim qualification). The core empirical contribution is solid and the scaling framework is valuable; the main barriers to a higher score are the missing statistical rigor and overclaimed framing.