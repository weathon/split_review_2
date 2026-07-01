## Summary

This paper identifies and formalizes Dual-level Noisy Correspondence (DNC) in Multi-Modal Entity Alignment (MMEA) — a practical problem where both intra-entity (entity-attribute) and inter-graph (entity-entity, attribute-attribute) correspondences contain misalignments. The authors propose RULE, a framework that: (1) estimates correspondence reliability via a two-fold principle (uncertainty from evidential deep learning + consensus), (2) uses robust training losses (DRL) and weighted attribute fusion (DRF) to mitigate noise, and (3) employs a Qwen2.5-VL-72B-based test-time reasoning module (TTR) to uncover latent attribute connections. Experiments on five benchmarks with seven baselines show strong improvements.

## Strengths

1. **Novel problem formulation with convincing practical grounding.** DNC is well-motivated — the paper shows real benchmarks contain >50% noisy correspondences (ICEWS) and demonstrates (Figure 1b) that DNC degrades both attribute fusion and cross-graph alignment. This reframes MMEA in a realistic setting that prior work assumed away.

2. **Principled two-fold reliability estimation.** The combination of uncertainty (via Dempster-Shafer theory, Eq. 2–3) and consensus (Eq. 5) is theoretically motivated by Theorem 1 (uncertainty alone is insufficient), leading to a clean three-way pair division (S_U, S_I, S_C). The Dirichlet formulation is well-connected to prior evidential learning work.

3. **Substantial training-time gains validated by ablation.** Even without the TTR module (w/o TTR in Table 3), RULE achieves 56.5 H@1 at 50% DNC on Non-name ICEWS-WIKI vs MEAformer's 42.4 — a 14-point gap attributable entirely to the training-time innovations (DRL + DRF). This demonstrates genuine methodological progress beyond the MLLM component.

4. **Comprehensive evaluation scope.** Five benchmarks, seven baselines, three noise levels (inherent, 20%, 50%), two evaluation protocols (Non-name, All-attributes), plus analysis studies (Figure 3: noise ratios 0.0–0.7, Figure 4: uncertainty vs consensus separation, Figure 5: reliability visualization).

## Weaknesses

### Fatal
None.

### Major

1. **The evaluation conflates training-time and test-time gains; the "fair comparisons" claim is overstated.** The main results (Tables 1–2) use RULE with the TTR module, which employs Qwen2.5-VL-72B-Instruct — a 72-billion parameter MLLM that none of the seven baselines have access to. The paper states "For fair comparisons, we adopt the same backbone (i.e., CLIP) for all baselines and our method" (Section 3.2), but this is true only for the attribute encoders, not the full system. While the ablation (Table 3) usefully shows that TTR contributes only a modest marginal gain (+1.7 H@1 on Non-name, +3.7 on All-attributes at 50% DNC) on top of the already-strong w/o-TTR version, this partial disentanglement does not fully resolve the issue because (a) no baseline is given access to the MLLM for even a simple comparison, and (b) the headline results in Tables 1–2 present the full system without clearly separating which gains come from the RULE framework vs the additional 72B model. An MLLM-augmented baseline (e.g., deploying Qwen2.5-VL-72B with a simple prompt on the same entity alignment task) is needed to attribute the gains properly.

### Minor

1. **Ablation study conducted on a single dataset.** The ablation experiments (Table 3) are performed only on ICEWS-WIKI (Section 3.3: "on the ICEWS-WIKI dataset"). Given that dataset characteristics vary (e.g., DBP15K datasets may have different noise structures), the generalizability of the ablation findings is untested.

2. **The joint similarity score in TTR makes a strong additive assumption without justification.** Eq. 15–16 compute s_i^{joint} = s_i + \hat{s}_i, simply adding the original and MLLM-refined scores. No analysis is provided on whether the two score sources are on the same scale, whether their distributions have comparable variance, or whether a weighted combination would be more appropriate.

3. **No discussion of computational cost or failure cases.** The TTR module uses a 72B-parameter model at inference time, which has substantial GPU memory and latency requirements. The paper provides no analysis of inference time per entity, total cost, or qualitative examples of when the MLLM reasoning succeeds or fails.

### Trivial

1. **Inconsistent baseline naming.** Table 1 uses "HHREA" while Table 2 and Section 3.2 use "HHEA" for the same baseline (Jiang et al., 2024). These should be harmonized.

2. **The greedy attribute selection strategy (Eq. 6–7) contains arbitrary design choices.** The initialization |π₀| = ⌊M/2 + 1⌋ and the value function v(π) = max(mean(...)) are presented without justification in the main text. The choices of max vs sum and mean vs other aggregations are not motivated.

3. **Attribute-attribute NC is logically derivative of entity-entity and entity-attribute NC.** The paper frames DNC as encompassing "three types of pairs" (line 40), but attribute-attribute NC follows deterministically from the other two noise types, making "dual-level" more precise than "three-type."

## Nice-to-Haves

- Add an MLLM-augmented baseline (e.g., Qwen2.5-VL-72B prompted directly for entity ranking without RULE training) to cleanly attribute the MLLM contribution.
- Run ablation studies on at least one additional dataset (e.g., ICEWS-YAGO or DBP15K_ZH-EN) to verify generalizability.
- Report inference-time cost (latency per entity, GPU memory) for the TTR module.
- Include a limitations paragraph discussing when/why the approach may struggle.
- Evaluate whether a smaller/cheaper alternative to Qwen2.5-VL-72B could substitute in the TTR module.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **TTR module is underspecified / prompt template not provided.** The reviewer criticized missing prompt details. This is removed because the prompt and CoT design details were placed in Appendix F.5 and Appendix I, which are stripped by the parser and exist in the original submission.

2. **Claim about vanilla prompts vs CoT being unsubstantiated (line 216).** The reviewer noted this claim is asserted without evidence in the main paper. Removed because the comparison may appear in the stripped appendix.

3. **Missing comparison with noise-robust methods from related fields.** The reviewer suggested baselines from noisy correspondence/label learning. This is scope creep — the paper compares with the seven standard MMEA methods used in the field, which is appropriate for the venue.

4. **Near-ceiling performance in All-attributes setting is a weakness.** The reviewer noted baselines are near-ceiling. This is an observation about the evaluation protocol, not a weakness of the method. The Non-name setting (where gaps are large and meaningful) is the more challenging protocol.

5. **The data-dependent nature of the greedy consensus strategy.** The reviewer characterized the greedy attribute selection as a "heuristic" without deeper justification. This is merged into Trivial point 2 above.

## Novel Insights

The most noteworthy observation from the review process is the structural tension between the paper's genuine training-time contribution (which is substantial and well-evidenced) and the evaluation framing that partially obscures it by bundling it with a large MLLM at test time. The w/o-TTR ablation results (56.5 H@1 vs MEAformer 42.4 at 50% DNC) tell a clean story of robust training: the uncertainty+consensus reliability estimation, three-way pair division, and tailored loss functions are a meaningful advance. The TTR module adds modest gains (+1.7 H@1 Non-name) but creates an unnecessary attribution problem. This pattern — a novel method combined with a large off-the-shelf model, where the pure methodological signal gets diluted — is a recurring challenge in the field.

## Suggestions

1. Restructure the paper to present w/o-TTR results as the primary comparison; include both variants in Tables 1–2 with the main comparison being against baselines without TTR.
2. Add a simple MLLM-augmented baseline to demonstrate that the RULE framework provides gains beyond what the MLLM alone offers.
3. Run the ablation study on at least one additional benchmark dataset for generalizability.
4. Add a brief computational cost analysis and a limitations discussion.
5. Standardize the baseline name to "HHEA" throughout.

## Score and Decision

**Calibration Anchor Summary:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gwZ90hFSL2.md | 1.00 | R1 (<1.5) | Unrelated topic, strong reject |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/a4O528mek9.md | 3.00 | R1 (1.5–3.5) | Multi-modal learning under incomplete data; less clear methodology, weaker experiments |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/jy6Lj3JaOf.md | 4.50 | R1 (3.5–5.5) | Multimodal graph benchmark; different contribution type |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NNUiUwQWx6.md | 5.75 | R2 (5.0–7.0) | Neuro-symbolic entity alignment; rejected despite SOTA, had clarity and complexity issues |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/z3dfuRcGAK.md | 6.67 | R2 (6.0–8.0) | Entity alignment via generative models; accepted with scores 6,6,8. Comparable contribution scope and evaluation depth |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/wfgZc3IMqo.md | 6.00 | R1 (5.5–7.5) | Robust classification with noisy labels; accepted 6,8,5,5. Similar robustness framing but simpler evaluation |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/LuVulfPgZN.md | 6.00 | R1 (5.5–7.5) | Out-of-modal generalization; accepted 6,6,6,6,6. Novel problem framing, similar score tier |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9Cu8MRmhq2.md | 8.00 | R1 (7.5–8.5) | Multi-granularity noisy correspondence in video; top-tier, clean evaluation without MLLM fairness issues |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/vJ0axKTh7t.md | 6.25 | R2 (6.0–8.0) | MLLM association benchmarking; accepted 6,6,5,8 |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OTGM_6w2HEMxzq7.md | 5.50 | R2 (5.0–7.0) | Graph matching with noisy correspondence via optimal transport; rejected 5,5,6,6 |

**Round 1 bracket:** [6.0, 7.0] — The paper is clearly stronger than the reject-tier entity alignment papers (~3–5.75) due to its well-motivated problem and comprehensive evaluation. The training-time results are competitive with papers scoring 6–7. However, the TTR evaluation conflation prevents it from reaching the 8.0 tier (e.g., Norton paper) which had cleaner evaluations and no MLLM fairness concerns.

**Narrowing (Round 2):** Compared to z3dfuRcGAK (avg 6.67, entity alignment with generative models, accepted), our paper has a stronger problem motivation but a more significant evaluation weakness. Compared to NNUiUwQWx6 (avg 5.75, neuro-symbolic EA, rejected), our paper has clearer methodology and more comprehensive experiments. The 6.5 score reflects a genuine contribution (DNC problem + robust training framework) tempered by the fixable but real evaluation framing issue.

**Final Score: 6.5 — Accept** — The core contribution (robust MMEA training against dual-level noisy correspondence) is solid, well-motivated, and experimentally supported even without the TTR module. The evaluation conflation with the 72B MLLM is a real concern that should be addressed through clearer presentation and additional baselines, but it does not invalidate the training-time innovations. The paper is publishable and the main weakness is structural/ presentational, not fundamental.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>