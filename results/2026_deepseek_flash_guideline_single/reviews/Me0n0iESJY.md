Now I have sufficient calibration. Let me produce the final authoritative review.

## Summary

This paper introduces a benchmark for evaluating model merging methods on Multimodal LLMs (MLLMs), covering five capability-defined tasks (VQA, Geometry, Chart, OCR, Grounding) across two base models (InternVL2.5 full-finetune, Qwen2-VL LoRA) and extending to modality merging (vision, audio, video). It implements 10 merging algorithms on this benchmark and proposes OptMerge, a method combining SVD-based low-rank denoising, SGD optimization, and mean initialization on top of the WUDI optimization objective.

## Strengths

1. **Well-constructed benchmark with public release.** The paper curates five fine-grained capability categories, each with ≥100k training samples, across two training regimes (full fine-tuning and LoRA). The public release of trained expert checkpoints, evaluation code, and 10 pre-implemented merging baselines fills a genuine gap — prior work (AdaMMS, UQ-Merge) either merges only two models or lacks capability-wise categorization.

2. **Informative comparative analysis of merging methods.** Section 5.2 provides a clean categorization of how 10 algorithm families behave on this benchmark (linear methods are robust but weak, SVD methods are sensitive to spectral structure, Iso-C fails on LoRA models because averaged singular values destabilize LLMs, etc.). This practitioner-oriented analysis is grounded in the data and useful.

3. **Novel modality merging experiments.** Table 5 demonstrates a data-free path toward omni-modal models by merging vision-language, audio-language, and video-language models trained on a shared LLM backbone. The finding that merged models can outperform both individual modalities and online composing methods (NaiveMC, DAMC) on AVQA tasks is interesting and opens a credible research direction.

4. **Clean ablation isolating component contributions.** Table 4 decomposes OptMerge into its components and identifies mean initialization (+4.43%) and low-rank approximation (+4.65%) as the primary drivers of improvement over WUDI on Qwen2-VL, while showing that SGD alone hurts (−9.77%). This transparency is valuable even if the individual components are not novel.

## Weaknesses

### Fatal
None.

### Major

1. **The claim that model merging "outperforms mixture training" is contradicted by the paper's own evidence.** This claim appears in the abstract (line 32: "can even outperform ... mixture data training"), the contributions list (line 38), and the conclusion (line 341: "model merging potentially surpasses mixture training"). The only direct mixture-training comparison is Table 2 (InternVL2.5), where Mixture Training achieves **57.66** vs. OptMerge's **57.44** — mixture training wins by 0.22 points. For Qwen2-VL (Table 3), the paper substitutes Qwen2-VL-Instruct as "the upper bound for mixture training" (line 224), but this is not a controlled baseline — it was trained on different data with a different recipe. The body text hedges with "closely match or even surpass" (line 224), but the abstract and contributions make an unqualified claim that the evidence does not support. **This is a central empirical assertion that is not backed by the data.** The paper should replace this with the defensible claim that merging *approaches* mixture training at a fraction of the compute (Table 7: 0.22h vs. 25.38h, 2.62GB vs. 240GB).

2. **The "2.48% average performance gain" is unverifiable from presented data.** The abstract (line 9) and contributions (line 37) state this figure, but nowhere is the reference baseline and averaging procedure specified. The ablation study (Table 4) shows WUDI→OptMerge gains of +4.65 on Qwen2-VL and +2.35 on Vicuna-7B — averaging these gives 3.50, not 2.48. More critically, there is an **unexplained baseline inconsistency**: Table 3 reports WUDI at **63.65** on Qwen2-VL, but Table 4 (the ablation starting from "WUDI Merging") reports WUDI at **58.65** on the same model — a 5-point gap. Until this is reconciled, the quantitative improvement claim is not trustworthy.

3. **Missing comparative baselines in key experiments.** Table 9 (Qwen2.5-VL-32B) and Table 10 (general multimodal benchmarks) compare OptMerge only against individual expert models and the base instruct model. No other merging methods (Task Arithmetic, TIES, WUDI, etc.) are shown. This means: (a) the claim that OptMerge "scales to larger models" cannot be evaluated relative to alternatives, and (b) the "emergent integrated capabilities" in Table 10 may be a property of *any* merging method, not OptMerge specifically. Without baselines, these tables demonstrate that *merging helps*, but do not support claims about OptMerge's superiority.

### Minor

4. **Theoretical analysis (Theorem 3.1) is disconnected from the method.** The theorem provides an upper bound on merging loss but is never referenced in the Methodology section (Section 4) and does not inform any design choice in OptMerge — no use of η, T, or the bound's terms to set hyperparameters. The claim that this is "the first theoretical explanation" (line 90) is also imprecise: the bound follows from standard PL-condition gradient descent analysis, and the practical content (less fine-tuning helps merging) is already documented empirically by prior work cited in the paper itself (Yu et al., 2024; Li et al., 2025b). If the theorem cannot be connected to the method, it should be moved to related work with a brief note.

5. **No variance or statistical significance reported.** All results tables report single-point estimates with no standard deviations, number of runs, or error characterization. Given that differences between methods are often small (e.g., 57.00 vs. 57.44 on InternVL2.5; 66.70 vs. 66.58 on HuggingFace models), it is impossible to assess whether these differences are meaningful or within run-to-run noise.

6. **Only linear layers are optimized.** Footnote 1 (line 142) states that OptMerge is applied only to linear layers; all other layers are averaged. No analysis is provided of what fraction of total parameters this covers, nor an ablation testing whether including non-linear layers would improve results.

### Trivial

7. The λ search range [0.1, 0.3, 0.5, 0.7, 1.0, 1.5] has only 6 values; a finer-grained search could shift method rankings.

## Nice-to-Haves

- Run actual mixture training for Qwen2-VL on the same data for a fair comparison.
- Add variance estimates (mean ± std over ≥3 runs) to all main tables.
- Run other merging methods on the large-scale (Qwen2.5-VL-32B) and general-benchmark (Table 10) settings.
- Ablate the "linear layers only" constraint.
- Add a limitations section discussing when merging fails, scaling with number of tasks, and handling of conflicting task vectors.

## Removed Points

These points from the input review are removed with justification:

1. **"OptMerge is incremental combination of existing techniques"** — Removed. This is a subjective judgment about novelty level, not a specific factual error. The combination for MLLM merging is not previously demonstrated. Novelty assessments are best reflected in overall evaluation, not listed as a concrete weakness.

2. **"'No benchmark exists' claim is slightly overstated"** — Removed. The paper's actual claim (line 28) is "no benchmark exists for model merging research that *clearly divides the tasks* of MLLM training and evaluation." The qualifier is specific and distinguishes their contribution from AdaMMS/UQ-Merge. This is a reasonable scope description.

3. **"Mean initialization is a standard trick"** — Removed. The tone is dismissive without adding substance. The ablation honestly reports which components matter; the criticism adds no specific evidence or insight.

4. **"Iso-C fails on Qwen2-VL" criticism** — Removed. This is an observation about a baseline behavior, not a weakness of the paper.

5. **Criticisms about missing appendix content** — Removed. The appendix is stripped by the parser; it exists in the original submission.

6. **"No discussion of limitations"** — Moved to Nice-to-Haves.

7. **"The 'surpass mixture training' claim appears three times in the introduction"** — Already captured in Major weakness 1; counting rhetorical recurrences adds nothing.

## Novel Insights

The most striking pattern across the reviews is the asymmetry between the paper's strongest contribution (the benchmark — genuinely useful, fills a clear gap, publicly released) and its weakest framing (the method overclaim). The modality merging results (Table 5) are genuinely novel and suggest a promising data-free path to omnimodal models. The core issue is not experimental quality but framing integrity: the central empirical claim about surpassing mixture training is contradicted by the paper's own best evidence (Table 2), and the headline improvement (2.48%) cannot be traced. This suggests the paper would be substantially stronger if reframed as a benchmark-and-analysis paper. Interestingly, this is almost the inverse of a common problem — usually papers under-contribute experimentally relative to their claims; here the experimental work is solid but the claims overshoot what those experiments support.

## Suggestions

1. **Reframe the paper around the benchmark as the primary contribution.** Drop or substantially soften the "outperforms mixture training" claim — replace with the defensible finding that merging *approaches* mixture training at a fraction of the compute cost.

2. **Reconcile the inconsistent WUDI baselines** (63.65 in Table 3 vs. 58.65 in Table 4 for Qwen2-VL) or explicitly state that they come from different evaluation configurations.

3. **Clarify where "2.48%" comes from** or remove it from the abstract and contributions.

4. **Add comparative baselines to Tables 9 and 10** so the reader can evaluate OptMerge against alternatives, not just against individual models.

5. **Either connect Theorem 3.1 to concrete design choices in OptMerge** or move it to related work.

6. **Add variance estimates** (at minimum, state the number of runs) for all main results.

---

### Calibration Anchors

Retrieved anchors (all from `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/`):

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| `SO0manOwUF.md` (UQ-Merge) | 5.50 | Bracketing | MLLM merging paper; similar profile but this paper has a stronger benchmark and weaker claim support |
| `Bq3fEAGXUL.md` (Realistic Eval) | 5.33 | Bracketing | Model merging evaluation paper; similar benchmark-first framing but this paper adds a method |
| `fvUVe2gJh0.md` (What Matters) | 5.33 | Narrowing | Scale-focused merging evaluation; similar systematic comparison |
| `WjPK2gj0xu.md` (MMER) | 5.50 | Bracketing | MLLM parameter merging; similar training-free approach but more modality-focused |
| `lNtio1tdbL.md` (ATM) | 3.00 | Bracketing | Method-heavy merging paper with severe overclaiming issues; our paper has stronger experimental contributions |
| `8QTpYC4smR.md` (LLM Survey) | 1.00 | Bracketing | Survey paper with no experimental contribution; not comparable |
| `gZnBI7WS1K.md` (LLaVA-PruMerge) | 3.50 | Bracketing | MLLM efficiency paper, not model merging; less relevant |

**Round 1 bracket**: 4.0 – 6.0 (papers in this range include benchmark/evaluation contributions with some framing issues).

**Narrowing**: Comparing to UQ-Merge (5.50, rejected) — both papers have genuine contributions but the paper under review has a more severe central claim issue (the "outperforms mixture training" claim is directly contradicted by Table 2, whereas UQ-Merge's weaknesses were about model diversity and limited baselines). This places the paper below UQ-Merge.

**Final score**: 5.0. The benchmark contribution is genuine and will serve the community. However, the paper's central framing claim is unsupported, the headline quantitative figure is unverifiable, and the baseline numbers contain an unexplained 5-point inconsistency. These issues are fixable with revision, but as submitted the paper overreaches relative to its evidence.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>