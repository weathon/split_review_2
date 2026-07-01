## Summary

This paper introduces Continuous Online Action Detection (COAD), a task formulation where models not only detect actions in real time but also continuously learn and adapt from streaming video under single-pass, no-storage constraints. The authors curate Ego-OAD, a large-scale egocentric OAD benchmark (87 classes, ~23k instances, 263h) derived from Ego4D, and propose training strategies (state continuity, orthogonal gradient projection, non-uniform loss) for the streaming setting. Results on Ego-OAD show improvements over a no-adaptation baseline, while results on EPIC-KITCHENS show more mixed patterns.

## Strengths

1. **Well-motivated task formulation.** The paper identifies a genuine gap: OAD models are trained offline but deployed in dynamic, user-specific environments on wearable devices. The single-pass, no-storage constraint follows cleanly from the egocentric wearable-device scenario (lines 15–21). This is a principled and clearly scoped problem definition.

2. **Ego-OAD dataset fills a real gap.** There is no large-scale egocentric OAD benchmark before this work. The dataset (87 classes, ~23k instances, 263h of video) is substantial, and the multi-label annotation strategy (union of passes) honestly captures ambiguity. The in-stream/out-of-stream split protocol appropriately disentangles adaptation from generalization.

3. **Ablation analysis is informative.** Table 3 systematically ablates each component (non-uniform loss, orthogonal gradient, state continuity) and shows the full configuration is needed for best out-of-stream generalization. This is the right structure of evidence for a methods paper.

## Weaknesses

### Major

- **Mixed EPIC-KITCHENS results weaken the generalization claim.** On EPIC-KITCHENS (Table 2), COAD underperforms the no-adaptation "Pretrained Only" baseline on in-stream Action mAP (7.9 vs. 9.6) and in-stream Action Top-5 Recall (20.5 vs. 22.9). While the paper acknowledges that "both COAD and the w/o COAD baseline struggle to adapt effectively" (line 188), a method whose stated purpose is continuous adaptation should not regress on in-stream metrics compared to a model that does no adaptation. On the positive side, COAD does consistently outperform Pretrained Only on all out-of-stream (generalization) metrics on EPIC-KITCHENS (Verb, Noun, Action), so the generalization claim is partially supported. The mixed picture reduces confidence in the method's general robustness.

- **Baseline comparison is insufficient to establish the method's relative value.** The comparison is only against (a) "Pretrained Only" (no adaptation) and (b) "w/o COAD" (adaptation without the proposed strategies). Missing are standard continual learning approaches (e.g., Elastic Weight Consolidation) that could operate under similar single-pass constraints. The "IID Training" upper bound is shown in Figure 4 but never reported numerically in the main tables, so the reader cannot assess how far COAD is from offline training. Without these anchors, the evaluation measures the method against ablated versions of itself rather than against external approaches.

- **Method novelty is overstated relative to prior work adoption.** Two of the three proposed "training strategies tailored to COAD" are directly adopted from prior work: orthogonal gradient projection from Han et al. (2025, line 128) and non-uniform loss from An et al. (2023, line 134). The third (state continuity, line 122) is a straightforward consequence of the streaming setting — not resetting the RNN hidden state. The paper's genuine novelty lies in the COAD task formulation and the Ego-OAD benchmark, but the presentation frames the method components as novel contributions (lines 116–138 and contribution bullet points).

### Minor

- **No variance or significance reporting.** Tables 1–4 do not report any measure of variability. Some claimed advantages are small (e.g., 26.0 vs. 25.5 mAP on Ego-OAD out-of-stream with egocentric pretraining). Without error bars or multiple seeds, it is unclear which differences are reproducible.

- **Abstract claim of "up to 20% improvement in top-5 accuracy" is imprecise.** The largest top-5 gain on Ego-OAD is 57.5 → 80.0 (22.5 percentage points, or ~39% relative). The abstract's "up to 20%" is ambiguous between absolute and relative, and the framing ("adaptation to the user's environment") primarily concerns in-stream data where the model sees the same data it trains on.

- **The "Adaptation" column in Table 1 is mislabeled.** The column marks whether "continuous adaptation is used," but the "w/o COAD" row also adapts — it simply does not use the proposed strategies. This could confuse readers into thinking w/o COAD does no adaptation at all.

- **Acronym inconsistency.** Line 66 introduces "Continuous OAD (CODA)" while the rest of the paper uses "COAD."

### Trivial

None.

## Nice-to-Haves

- A quantitative comparison to at least one continual learning baseline (e.g., EWC with the same single-pass constraint) would substantially strengthen the evaluation.
- Reporting the IID upper bound numerically in the main tables (rather than only in Figure 4) would help readers gauge the absolute gap to offline training.
- A discussion of compute cost (FLOPs or wall-clock time per frame during streaming updates) would substantiate the claim of suitability for resource-constrained devices.
- A small-scale comparison showing why Transformer-based OAD models cannot be used in the COAD setting (e.g., memory profiling) would justify the RNN architectural choice.

## Removed Points

These points were raised by the reviewers but are removed for the reasons stated below. Treat them with caution — they may reflect reviewer knowledge gaps or presentation issues rather than real problems with the paper.

1. **"No temporal localization metrics (e.g., edit distance)"** — The paper uses per-frame mAP and Top-5 Recall, which are standard OAD metrics used in the papers it cites (An et al., 2023; Zhao & Krähenbühl, 2022). Edit-distance-based metrics are architecture-specific and not a universal OAD requirement. (Removed as not a field-standard gap.)

2. **"The pretraining set is small, making comparisons less informative"** — This is a deliberate design choice (line 146: "providing a weak initialization under limited supervision") to simulate realistic deployment where limited pre-training data is available. (Removed as a design choice, not a flaw.)

3. **"Replace EPIC-KITCHENS results with a dataset where the method works"** — This would be cherry-picking and would weaken scientific honesty. The paper's approach of showing results on two datasets, including one where the setting is challenging, is more appropriate. (Removed as an inappropriate suggestion.)

4. **"Missing appendix contents (Appendix A)"** — The parser strips appendix content from all papers; the original submission includes it. (Removed per Hard Rule.)

5. **"Dataset is only partially released"** — Speculative; the paper references Ego4D MQ which exists and is publicly accessible. (Removed per Hard Rule.)

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add at least one continual learning baseline (e.g., EWC with the same single-pass constraint) to anchor the method's relative performance.
2. Report the IID upper bound numerically alongside Table 1.
3. Add variance estimates (multiple seeds or stream orderings) to the main results.
4. Sharpen the abstract's claims: specify what "20% improvement" refers to, and distinguish adaptation (in-stream) from generalization (out-of-stream) more clearly.
5. Rephrase the method contribution to honestly distinguish between the COAD formulation (new) and the adopted components (prior work).
6. Fix the CODA/COAD inconsistency on line 66.

---

### Calibration Report

**Calibration Anchors Retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `5lUdTogEL3.md` (Person Re-ID) | 1.00 | 1 | Not comparable (different task, score 1-1.5 band). |
| `WM5G2NWSYC.md` (Subnetwork CL) | 2.00 | 1,2 | Not comparable (continual learning but on different tasks with small models/datasets). |
| `BrqFB8Nl7e.md` (CL After Deployment) | 3.75 | 1 | Moderate relevance: introduces new CL setting (OWCL) with small datasets. Our paper has a larger benchmark and clearer motivation. **Our paper is stronger.** |
| `7L2bpe7lfm.md` (Video CL Compression) | 4.50 | 1,2 | High relevance: video continual learning with strong baselines but incremental method novelty. Comparable structure; our paper has better dataset contribution but weaker baselines. **Comparable quality.** |
| `4sJJixGIZX.md` (Online Continual Graph Learning) | 5.00 | 2 | Very high relevance: new task formulation (OCGL) + benchmarks + minimal method contribution (neighborhood sampling). Our paper has similar structure but weaker baselines and mixed results on one dataset. **Slightly weaker.** |
| `Y7jJN0VQ4y.md` (CL for Anomaly Detection) | 5.71 | 1,2 | High relevance: new task (CL-WSVAD) + method + benchmarks. Their baselines and method are stronger. **Our paper is weaker.** |
| `M8gXSFGkn2.md` (Ego Video-Language) | 7.00 | 2 | Egocentric benchmark paper, but different task. Stronger overall. **Our paper is significantly weaker.** |

**Initial bracket (Round 1):** 3.5 – 5.5, narrowing to 4.0 – 5.5

**Final score rationale:** The paper's genuine contributions — the COAD task formulation and the Ego-OAD benchmark — are useful and well-motivated. However, the method novelty is overstated (components adopted from prior work with minimal modification), the evaluation compares only against ablated versions of itself rather than external continual learning approaches, and the EPIC-KITCHENS results are mixed (in-stream regression). These weaknesses are significant but not fatal: the task and dataset contributions remain. The paper is most comparable to "Online Continual Graph Learning" (5.00, Rejected) and "Large Scale Video Continual Learning" (4.50, Rejected), which have similar strengths and weaknesses.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>