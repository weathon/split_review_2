## Summary

This paper introduces a benchmark for model merging in Multimodal LLMs (MLLMs), covering five task categories (VQA, Geometry, Chart, OCR, Grounding) across two base architectures and two fine-tuning regimes (full FT and LoRA). It also proposes OptMerge, a method that applies low-rank denoising and optimization refinements to improve over the WUDI Merging baseline. Additionally, it explores modality merging (vision+audio+video) and validates on real Hugging Face checkpoints.

---

## Strengths

1. **The benchmark fills a genuine gap in structured MLLM merging evaluation.** Prior work (AdaMMS, UQ-Merge) either merges only two models at a time or lacks capability categorization. This paper provides a structured benchmark with five task categories, two architectures (InternVL2.5, Qwen2-VL), both full FT and LoRA, expert models trained on ≥100k samples each, and evaluation across 10+ metrics. This is useful infrastructure for the model merging community.

2. **Modality merging (vision + audio + video) is an underexplored and interesting direction.** Table 5 shows that merging single-modality models into one outperforms individual modalities and is competitive with online composition methods (NaiveMC, DAMC) that require 3× parameter storage. The finding that "the best merging method even outperforms these online composition methods" (Table 5) is a meaningful result regardless of which specific merging algorithm wins.

3. **Practical validation on real Hugging Face community checkpoints (Table 6).** The paper merges four diverse community models (math GRPO, Pokemon domain, OCR, Vietnamese VQA) and shows improvement over individual models, demonstrating real-world applicability beyond the authors' own fine-tuned models.

4. **Public release of code and checkpoints** is provided, which is essential for a benchmark paper and supports reproducibility.

---

## Weaknesses

### Fatal
None.

### Major

1. **Unexplained numerical discrepancy between the main results (Table 3) and the ablation (Table 4) undermines the claimed improvement on Qwen2-VL.** Table 3 reports WUDI Merging's average on Qwen2-VL (LoRA) as **63.65**, while Table 4 (ablation) reports WUDI Merging's average on the same setting as **58.65** — a gap of 5.00 points. The paper states both tables refer to "LoRA model merging (Qwen2-VL)" and provides no explanation for this discrepancy. Critically, OptMerge's Qwen2-VL score is **63.30** in both tables, meaning:
   - If Table 3's baseline (63.65) is correct, OptMerge (63.30) *underperforms* WUDI Merging by 0.35 points.
   - If Table 4's baseline (58.65) is correct, OptMerge shows a meaningful 4.65-point gain.
   
   The claimed "average performance gain of 2.48%" (abstract) and "significant 4.43% improvement" (Section 5.2) depend on the Table 4 baseline. Without resolving this contradiction, the method's headline performance claim on the Qwen2-VL setting is unsupported.

2. **The claim that model merging "can outperform mixture training" is not supported by the paper's own controlled experiment.** For InternVL2.5 (Table 2), where a properly controlled mixture training baseline is provided, Mixture Training (57.66) *outperforms* OptMerge (57.44). The paper hedges with "closely match or even surpass" (line 224), but the abstract and contribution list state the conclusion more broadly ("model merging can outperform mixture training," line 38). For Qwen2-VL (Table 3), the "mixture training upper bound" is Qwen2-VL-Instruct (62.23), which is a separately trained model by a different organization — not a controlled comparison. The only controlled experiment contradicts the general claim.

3. **OptMerge's advantage over WUDI Merging is marginal or inconsistent across settings, even ignoring the Table 3/4 discrepancy.** 
   - **Table 2 (InternVL2.5 full FT):** OptMerge (57.44) vs. WUDI (57.00) — a difference of 0.44 points. No variance or significance is reported, so this could easily be within evaluation noise.
   - **Table 5 (modality merging):** TSV Merging (67.34) outperforms OptMerge (67.00). OptMerge is not the best method on this setting.
   - **Table 6 (Hugging Face):** OptMerge (66.70) vs. TIES w/ DARE (66.58) — a 0.12-point difference, again within noise range.
   
   The paper's claim of "superior average results across various scenarios" (line 226) overstates what the data show. The method shows a pattern of marginal gains on some settings and losses on others.

### Minor

1. **No statistical significance or variance reported.** Given that the margins between OptMerge and the best baselines are very small (0.44 on InternVL2.5, 0.12 on Hugging Face, 0.35 against WUDI on Qwen2-VL per Table 3), single-run results without standard deviations or confidence intervals make it impossible to assess whether these differences are meaningful. While single-run evaluation is common in large-scale benchmark reporting, the paper's contribution claims hinge on these narrow margins.

2. **The rank parameter *k* for the LoRA scenario is not specified.** Section 4.2 describes a low-rank approximation for LoRA tuning but never states what *k* ratio was used in the main Qwen2-VL experiments. The merging details section (5.1) defines *k* only for full FT (rank divided by number of tasks). The ablation on *k* (Table 8) is conducted on InternVL2.5, not Qwen2-VL, so it does not clarify this.

3. **The ablation study (Table 4) has a minor issue with the "+ Low-rank" step on Vicuna-7B:** adding low-rank approximation *decreases* performance from 67.07 to 67.00. This is not discussed in the paper. While the decrease is tiny, it is inconsistent with the narrative that each component incrementally helps.

### Trivial

- The λ search range [0.1, 0.3, 0.5, 0.7, 1.0, 1.5] is coarse. The choice of λ can interact with optimization-based methods like WUDI and OptMerge, but this is not discussed.

---

## Nice-to-Haves

- Clarify whether the Table 3 vs. Table 4 baseline discrepancy is due to different λ values, different task subsets, or an error. If there is a legitimate reason (e.g., Table 4 evaluates on a subset or uses a different λ), state it explicitly.
- Train a proper mixture model for Qwen2-VL (matching what was done for InternVL2.5) to enable a controlled comparison for the "model merging vs. mixture training" claim, or explicitly qualify that the comparison against Qwen2-VL-Instruct is not controlled.

---

## Removed Points (filtered out as invalid or parser artifacts)

- *"The source models are only identified by name in footnotes (stripped from this version)"* — Removed. This is a parser artifact; the footnotes exist in the original submission.
- *"The paper's claim that OptMerge is 'clearly best on exactly zero of them'"* — Removed as an overstatement. OptMerge is top-ranked on InternVL2.5 (Table 2) and Hugging Face (Table 6), though margins are small.
- *"No benchmark exists" framing is too absolute"* — Not raised by the harsh critic; not present in the input.

---

## Novel Insights

None beyond the paper's own contributions. The harsh critic's primary novel observation is the numerical discrepancy between Tables 3 and 4, which is a valid finding about the paper itself, not about the research area.

---

## Suggestions

1. **Resolve the Table 3 / Table 4 baseline discrepancy.** This is the single most important issue. If the ablation uses a different evaluation protocol or λ value, state it. If the main table contains an error, correct it.
2. **Reframe the contribution language.** The paper would be better served by honestly characterizing OptMerge as providing marginal gains on full FT settings with mixed results on LoRA, rather than claiming "superior results across various scenarios."
3. **Report variance across at least a few random seeds** for the key comparisons where margins are narrow (Table 2, Table 6), to establish whether the reported differences are meaningful.
4. **Specify the rank *k* ratio used for the LoRA experiments** in Section 4.2 or the merging details.

---

## Score and Decision

The benchmark contribution is solid and fills a real gap. However, the method claims are significantly undermined by (a) an unexplained 5-point baseline discrepancy between Tables 3 and 4 that makes it impossible to assess OptMerge's true performance on a key setting, and (b) overclaimed results about "surpassing mixture training" that are contradicted by the paper's own controlled experiment. The method's advantage over baselines is marginal and inconsistent across settings. As a combined benchmark+method paper, these issues substantially weaken the core claims. A revision that resolves the discrepancy and honestly reframes the method's performance could make this a stronger submission.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>