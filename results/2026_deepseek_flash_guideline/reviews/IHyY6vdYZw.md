## Summary

This paper introduces VisualPRM400K (~400K multimodal process supervision samples), VisualPRM (an 8B multimodal PRM), and VisualProcessBench (2,866 samples with 26,950 human-annotated step labels). The dataset fills an open gap—no multimodal PRM dataset of this scale existed—and the model demonstrates that a PRM trained on automatically-generated data can serve as an effective Best-of-N scorer across multiple MLLM families and scales, outperforming ORM and Self-Consistency. VisualProcessBench improves over prior benchmarks by requiring detection of all erroneous steps rather than just the first.

## Strengths

1. **First large-scale multimodal process supervision dataset** — VisualPRM400K fills an open gap. Evaluated across 3 model families and 6 model scales (MiniCPM-V2.6, Qwen2.5-VL-7B, InternVL2.5-8B/26B/38B/78B), every model shows improvement (+3.7 to +8.9 points overall in Table 2).

2. **PRM advantage over ORM and SC grows with N while ORM saturates** — Figure 4 shows PRM's gap over ORM and Self-Consistency widens as N increases from 8 to 128, while ORM performance declines from N=64 to N=128. This is a non-trivial empirical finding distinguishing process from outcome reward modeling under scaling.

3. **High-quality human-annotated benchmark with all-error detection** — VisualProcessBench requires detecting all erroneous steps (not just the first), uses 13 annotators for 39 person-days with documented quality control (10% author review per split, re-annotation of erroneous splits), and reveals open-source MLLMs cluster near random chance (50% F1) while VisualPRM achieves 62.0 (on par with Gemini-2.0-Flash, better than GPT-4o).

4. **Cross-modal transfer to text-only reasoning** — Table 5 shows VisualPRM, trained on multimodal data, improves text-only LLMs (Qwen2.5-7B/32B/72B) on MATH-500 and GPQA-Diamond (e.g., +6.1 and +5.0 for Qwen2.5-7B), demonstrating step-evaluation capability is not limited to the visual modality.

5. **Clean multi-turn chat formulation** — Section 3.2 formulates PRM training as a multi-turn chat task where each turn presents one new step and the model predicts correctness conditioned on all previous steps and the image, adapting standard MLLM architectures without requiring architectural modifications.

## Weaknesses

### Fatal

None.

### Major

- **Unverified question overlap between training data and evaluation benchmarks** — Training questions come from MMLR v1.1/MMPR (Wang et al., 2024c), but the paper never discloses what source benchmarks MMPR's questions draw from nor analyzes whether they overlap with any of the seven evaluation benchmarks (MMMU, MathVista, MathVision, MathVerse, DynaMath, WeMath, LogicVista). If overlap exists, the model may have been trained on step-level correctness annotations for questions it is later evaluated on, potentially inflating BoN results. The paper contains no deduplication analysis, overlap check, or mention of this risk. This is the most significant gap in the empirical evidence and must be resolved for the headline claims to be fully trustworthy.

### Minor

- **Base model for VisualPRM not specified** — The paper describes VisualPRM as an "8B" multimodal PRM (Section 3.2) but never states which specific model it is fine-tuned from. Since solutions are sampled from InternVL2.5 series models and the PRM is compared against InternVL2.5-8B in ablations, the base is plausibly InternVL2.5-8B, but this is never stated, creating a reproducibility gap.

- **No variance or confidence information** — All reported results (Tables 2, 3, 4, 5, Figure 4) lack standard deviations or confidence intervals. BoN evaluation with temperature 0.7 sampling has inherent variance. The observation that ORM's Best-of-128 underperforms Best-of-64 (Figure 4) further suggests variance that should be quantified to assess whether small margins (e.g., 1.5 points between PRM and ORM at N=8) are meaningful.

- **Text-only evaluation protocol unclear** — Table 5 evaluates VisualPRM on text-only LLMs (Qwen2.5 series) on text-only benchmarks. Since VisualPRM is a multimodal model, the paper should explain how it processes text-only inputs (e.g., blank image, no image, rendered text). Without this, the comparison cannot be properly assessed.

- **Step merging impact not analyzed** — When solutions exceed 12 steps, they are "evenly merged" (line 142). The paper provides no analysis of how merging affects annotation quality or whether merged "steps" containing multiple reasoning sub-steps make correctness labeling noisier.

- **Headline framing conflates BoN and PRM effects** — The abstract leads with gains of 8.0, 3.7, 8.4, and 5.9 points comparing BoN+PRM vs Pass@1. The controlled comparison (PRM vs ORM vs SC at equal N, Section 4.3) that isolates the PRM's contribution is relegated to later in the paper. While both comparisons are present, the framing makes it harder for readers to separate the effect of additional candidates from the PRM's scoring quality.

### Trivial

- **Duplicate "Step 1" in data example** — The example in Figure 2 (lines 60-62) shows two different reasoning sub-steps both labeled "Step 1," indicating a data quality or presentation issue.

## Nice-to-Haves

- Test VisualPRM on solutions from held-out model families to assess generalization of step-evaluation capability.
- Provide analysis of the relationship between step merging (>12 steps) and annotation quality.

## Removed Points

- **#Pwoll label undecipherable in Figure 1** — Removed. Garbled table labels and duplicate model entries are PDF parser artifacts, not author errors (per formatting-artifact rule).
- **"Overall" score as simple average across benchmarks** — Removed as a weakness. Simple averaging is standard practice for multi-benchmark evaluation in this community.
- **Policy model influence on BoN generalization** — Moved to Nice-to-Haves. Asks for experiments beyond the paper's stated scope.
- **Generic/superficial strengths from Strength Finder** — Removed strengths that were merely about the problem being "important" or generic praise without specific evidence of what the paper contributes.
- **Step-0/Step-1 overlap raised as a significant issue** — Demoted to Trivial. Could be a presentation artifact and does not threaten the paper's claims.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface any unexpected finding that the paper itself does not already present or discuss.

## Suggestions

1. **Disclose the source of MMLR v1.1/MMPR questions and perform an overlap analysis** with all evaluation benchmarks. Remove any overlapping questions from evaluation, or demonstrate consistent results on a guaranteed-disjoint held-out set. This is the single most important revision needed.
2. Explicitly state the base model used for VisualPRM initialization.
3. Report key results with variance (multiple seeds or bootstrap confidence intervals), particularly for the BoN comparisons where small margins carry the argument.
4. Clarify the protocol for text-only evaluation.
5. Foreground the controlled comparison (PRM vs ORM vs SC at equal N) more prominently in the abstract and introduction.

## Score and Decision

**Calibration anchors (all rounds):**

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| **OpenPRM** (fGIqGfmgkW) — building open-domain PRMs | 6.00, Accept | 1, 2 | Similar PRM paper with novelty concerns; accepted despite presentation issues. Current paper has stronger resource contributions but an unresolved contamination gap. |
| **ToolComp** (qHpfxfnIq3) — multi-tool process supervision benchmark | 5.40, Reject | 1 | Similar structure (benchmark + PRM/ORM comparison); rejected partly due to small dataset and missing details. Current paper has much larger scope. |
| **RM-Bench** (QEHrmQPBdd) — reward model benchmark | 8.00, Accept | 1 | Higher-quality benchmark with stronger validation. Current paper's benchmark is solid but less extensively validated. |
| **Inference-Aware BoN FT** (77gQUdQhE7) — BoN-aware fine-tuning | 5.67, Accept | 2 | BoN-focused method paper accepted at this range. Current paper has comparable quality but unresolved contamination concern. |
| **MMMU-Pro** (2jTdHYuguF) — robust multimodal benchmark | 5.80, Reject | 1 | Benchmark paper with mixed reviews. Current paper has broader contributions. |
| **Learning How Hard to Think** (6qUUgw9bAZ) — adaptive BoN | 6.50, Accept | 2 | Strong method paper; higher quality in terms of rigorous experimentation. |
| **Beyond Unimodal Learning** (Pa6SiS66p0) — multimodal continual learning benchmark | 4.33, Reject | 1 | Weaker benchmark paper with limited comparisons. Current paper has stronger contributions. |

**Bracket:** Round 1 placed the paper at 4.0–6.5. The most comparable anchor is OpenPRM (6.00, accepted), which has similar limitations (novelty concerns, missing details) but was accepted. The current paper has stronger resource contributions (dataset + benchmark + model) but the unresolved contamination concern pulls it down relative to OpenPRM. ToolComp (5.40, rejected) is a structural comparison but had a much smaller dataset. Round 2 narrowed the bracket to 5.0–6.5, with the BoN-aware FT paper (5.67, accepted) confirming that this score range can lead to acceptance.

**Final score: 5.5** — The paper makes real contributions (first multimodal PRM dataset, thorough benchmark, extensive evaluations across model families/scales) but has a significant unresolved gap (potential data contamination from unverified question overlap between training and evaluation sets). The controlled comparison (PRM > ORM > SC at equal N) is the strongest evidence and survives the contamination question, but the headline absolute gains require further verification. The paper is borderline: with the contamination issue resolved it would be a clear 6.5+ accept.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>