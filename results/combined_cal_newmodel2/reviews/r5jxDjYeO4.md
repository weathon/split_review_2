## Summary

This paper proposes ASPD (Adaptive Serial-Parallel Decoding), a framework that accelerates LLM inference by exploiting "intrinsic parallelism" in model responses. It has two main components: (1) a data transformation pipeline that rewrites serial responses into parallel-structured training data via LLM rewriting, independence verification, and integrity checks, and (2) an architectural modification (branch-invisible attention masks + shared position IDs) and hybrid decoding engine that enable the model to switch between serial and parallel modes during inference within a single forward pass. Experiments on Vicuna Bench, MT Bench, RAG, and math reasoning benchmarks (MATH500, AMC23, GPQA, AIME2024/2025) using Vicuna-1.3-7B, Qwen2.5-7B/32B-Instruct report 1.30–3.10× speedup over the original autoregressive model.

## Strengths

- **A well-motivated architectural design.** The combination of branch-invisible attention masks (Eq. 2–3) and shared position IDs (Eq. 4) is a clean, formalized way to enable parallel decoding within a single forward pass without external batching or threading. The formalism distinguishing the visibility function *S* and position function *pos* is clearly laid out in Section 3.2 and makes the design decisions explicit enough to be reproduced. This is the paper's strongest technical contribution.

- **The data pipeline is non-trivial and carefully constructed.** The four-stage pipeline (parallel rewriting → independence verification → integrity/answer verification → preference-based selection) in Section 3.1 addresses a real problem: automatic construction of parallel training data from naturally serial responses. The inclusion of both independence verification and integrity verification stages is a sensible guard against semantic degradation. The pipeline is a genuine engineering contribution that goes beyond simple heuristic rules.

- **Coverage across multiple domains and model architectures.** The evaluation spans general dialogue (Vicuna Bench, MT Bench), RAG, and several math reasoning benchmarks (MATH500, AMC23, GPQA, AIME2024/2025), and uses three different base models (Vicuna-1.3-7B, Qwen2.5-7B-Instruct, Qwen2.5-32B-Instruct). This breadth supports the claim of cross-domain and cross-architecture generalization, and the math experiments at 32B scale are particularly valuable.

## Weaknesses

### Fatal
None.

### Major

- **V-Seq speedup unexplained; parallel mechanism's incremental contribution not isolated.** V-Seq (the sequential model fine-tuned on the same processed data *without* any parallel decoding mechanism) also achieves significantly higher TPS than V-Ori (the original model). The paper never explains why V-Seq itself is faster — this could be due to shorter outputs, distribution shifts, or other training artifacts. More importantly, **V-ASPD vs V-Seq TPS ratios are not reported for the general-domain experiments** (Vicuna/MT Bench). This makes it impossible to isolate how much of the headline 1.82–3.10× speedup comes from the parallel mechanism vs. the data pipeline alone. For math reasoning (Table 3), where this comparison *is* provided, the parallel mechanism adds only 1.04–1.17× TPS over Seq. The paper should report these numbers for general tasks and analyze why V-Seq differs from V-Ori. (Source: Figure 4 caption describes "V-ASPD and V-Seq generally achieve higher scores and higher tokens-per-second than the baseline V-Ori method" but does not provide the cross-comparison; Section 4.2 reports speedups only relative to V-Ori.)

### Minor

- **The 44% Proportion of Parallel Data is suspiciously identical across all four datasets** in Figure 1 (ShareGPT Vicuna, MRC, RAG, Math-220K) despite showing very different Degree of Parallelism and Average Branch Number values. The paper defines PPD in Section 4.1 but does not explain how the detection threshold or methodology produces this exact uniformity. This may be a parser artifact from a figure image, but as presented it needs clarification. (Source: lines 28–31, Section 4.1 definitions.)

- **The "non-invasive" pipeline claim is overstated.** The paper calls the pipeline "non-invasive" and says it operates "without altering the response probability distribution" (Section 1, line 49). However, the pipeline uses an LLM (Qwen3-235B-A22B) to rewrite responses, imposing explicit `<branchgroup>`/`<branch>` markup structures that do not occur naturally. The rewritten responses are used as training data — the model is fine-tuned to generate a different kind of output with parallel markup tokens. The framing should be clarified to reflect that the pipeline is *automated* (no human annotation), not that it leaves the output distribution unchanged.

- **How the model decides when to enter parallel mode is underspecified.** Section 3.3 states "when the model determines that the current response can be parallelized, it generates several parallel titles" (line 147), but does not clarify whether this is a learned behavior (from the training data), a threshold-based rule, or an implicit capability. While the training data likely teaches this, a precise description is important for reproducibility.

- **The PASTA comparison in the ablation (Table 4, line 234) needs stronger justification.** PASTA† scores 4.98, which is dramatically worse than the V-Ori baseline of 6.21 (a 26% quality reduction). While the paper attributes this to PASTA's lack of independence verification, such a large degradation raises the question of whether PASTA is being evaluated outside its intended setting. The paper should verify that the adaptation is faithful and document what was changed.

- **APAR* data quality enhancement is not described.** The paper uses APAR* (APAR with "enhanced training data quality using Qwen3-235B-A22B") but never explains what this enhancement entails, making it hard to assess fairness of comparison against the original APAR (Section 4.2, entry for Table 1).

- **The "state-of-the-art" claim in the conclusion (line 251) is too broad.** The paper does not compare against speculative decoding, Medusa, or other LLM acceleration methods that achieve 2–3× speedups. While speculative decoding operates at the token level and is described as "orthogonal," the SOTA claim should be qualified to the specific family of methods being compared (internal structural parallelization approaches).

### Trivial
- Missing Q-APAR and SoT baselines on the Qwen model in Table 1 weakens the cross-model generalization claim, since there is no competing method to compare against on that architecture.

## Nice-to-Haves

- Include speculative decoding as a baseline (or discuss more concretely why it is not comparable) to strengthen the SOTA claim.
- Add confidence intervals or standard deviations for speedup numbers, especially for math benchmarks where means across 8 random seeds are reported.
- Explain the "enhanced data quality" for APAR* in one sentence.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **"The PASTA comparison appears unfairly stacked … 26% quality reduction"** — The framing as "unfairly stacked" was removed because PASTA is only compared in the ablation study (not the main results), and the paper does attribute the failure to PASTA's lack of independence verification. The core concern (needing stronger justification) is preserved as a Minor weakness above.
- **"Speculative decoding baseline missing"** — Removed as a core weakness because the paper clearly positions speculative decoding as "orthogonal" and operating at the token level vs. structural parallelism. However, the SOTA claim overbreadth is retained as Minor.
- **"Table 4 hard to parse"** — Pure formatting issue; not a substantive weakness.
- **"Missing standard deviations/confidence intervals"** — Single-run inference speed evaluation is standard in this subfield.
- **"V-Seq undermines causal attribution … structural problem"** — Too strong a framing. The paper's full-system contribution (data pipeline + parallel architecture) is its actual claim; the V-Seq comparison is supplementary evidence, not structurally invalidating. The core empirical gap is retained as Major.

## Novel Insights

None beyond the paper's own contributions. The reviews surface a methodological insight that the paper should isolate the parallel mechanism's incremental contribution from the data pipeline's effect (via the V-Seq controlled comparison), which is a valid but standard experimental-design refinement.

## Suggestions

1. Report V-ASPD vs V-Seq TPS ratios and quality comparisons for all general-domain benchmarks (Vicuna, MT Bench), and analyze why V-Seq itself is faster than V-Ori (shorter outputs? different generation behavior?).
2. Explain how the 44% PPD value was computed and why it is uniform across four diverse datasets.
3. Clarify the "non-invasive" terminology and drop or rephrase the "without altering the response probability distribution" claim.
4. Specify how the model decides to enter parallel mode during inference — is this a learned behavior from the training data?
5. Provide more detail on what "enhanced training data quality" means for APAR*.
6. Justify the PASTA ablation comparison or include a note about adaptation challenges.
7. Qualify the "state-of-the-art" claim (e.g., "among single-sequence parallel decoding methods").

## Score and Decision

**Calibration Anchors Report:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| cf7NTWv1iW (Hardware-Aware PPD) | 4.25 | R1 | Yes | Similar concept (parallel decoding within a single model); weaker architectural novelty but stronger on memory/hardware analysis. ASPD is above this. |
| gfDbD1MRYk (Semi-autoregressive Decoding) | 4.50 | R1 | Yes | Similar contribution level; both have evaluation gaps. ASPD has stronger architectural novelty. |
| cJd1BgZ9CS (DSI) | 5.00 | R1 | Yes | Simulation-based but strong theory. ASPD has real implementation but weaker attribution analysis. Comparable tier. |
| QOXrVMiHGK (PEARL) | 5.75 | R2 | Yes | Stronger empirical validation (clear baselines, ablation); accepted despite one severe weakness. ASPD is below this due to V-Seq gap. |
| SXvb8PS4Ud (ParallelSpec) | 5.80 | R1 | Yes | Stronger empirical setup but novelty concerns. ASPD has better architectural novelty but weaker speedup attribution. |
| Yz7ts36V7A (Backoff Decoding) | 3.67 | R1 | Yes | Exaggerated claims, weak experiments. ASPD is clearly above this. |

**Round 1 bracket:** 4.5–5.5. **Round 2 narrowing:** Comparing item favorability profiles, ASPD shares with the 4.5–5.0 papers (Semi-auto, DSI) the pattern of having a genuine contribution undermined by an empirical gap. It lacks the stronger validation that pushed PEARL to 5.75. The V-Seq item (favorability 0.72) and SOTA claim item (favorability -2.12) create drags that place it below PEARL and ParallelSpec but clearly above Semi-autoregressive Decoding (4.50) and Hardware-Aware PPD (4.25). **Final score: 5.0.**

The paper presents a well-motivated architectural design and a non-trivial data pipeline, evaluated across diverse domains and model sizes. However, the failure to report V-ASPD vs V-Seq TPS comparisons for general-domain benchmarks means the headline speedup numbers cannot be cleanly attributed to the parallel mechanism. This is a resolvable gap, but in the current form the empirical evidence is insufficiently precise for acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>