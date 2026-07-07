Now I have enough information. Let me draft the review.**Round 1 Bracket:** Based on calibration anchors, topically similar papers score around 4.67–6.67. This paper has stronger empirical breadth than the 4.67 paper but a significant methodological gap (missing confidence baseline) that prevents placement at 6+. Initial bracket: **4–6**.

**Round 2 Narrowing:** The paper's core Ceiling TTA finding and state-of-the-art results across 18 benchmarks are genuinely stronger than the rejected 4.67 paper (`lF9QXpfNHm`). However, the missing max-softmax baseline is a real evidential gap — unlike C-TPT (score 6.0) or DynaPrompt (score 6.25), which have clearly justified mechanisms. The unresolved question of whether regression adds anything beyond confidence ranking, combined with the potential data overlap with ImageVal-12k, keeps this below 6. I place it at **5.0** — credible work with a central ablation gap.

---

## Summary
RTA proposes replacing entropy-based view selection in CLIP test-time adaptation with a LightGBM regression model that predicts label cross-entropy loss from CLIP logits, trained once offline on ~1,000 pseudo-labeled samples. The key motivating finding ("Ceiling TTA") is that selecting views by true LCE outperforms entropy selection by 10–25 percentage points across five datasets, motivating a regression approach to approximate LCE without access to ground-truth labels.

## Strengths
- **Ceiling TTA analysis (Tables 1–2)** is a genuinely insightful empirical contribution: LCE-based view selection consistently dominates entropy selection by 10–25 pp across five datasets and two CLIP architectures (e.g., ViT-B/16 on IN-A: 90.2% with LCE vs. 64.3% with SE at 64 views). This motivational finding is valuable to the TTA community independent of the proposed solution.
- **Broad evaluation**: tested on 18 datasets spanning single-label, multi-label, and cross-domain settings with two CLIP backbones, achieving consistent improvements over recent CVPR 2025 baselines (BCA, TDA).
- **Efficiency**: a single offline training session on 1,000 samples requires no per-instance parameter updates, contrasting with prompt-tuning methods (TPT, DiffTPT, RLCF) that require per-sample optimization loops.

## Weaknesses

### Fatal
None.

### Major
- **Missing max-softmax confidence baseline** — The regression model is trained with inputs = CLIP logits $s$ and targets = $\mathcal{L}_{CE}(\hat{y}^{reg}|s^{reg}) = -\log(\text{softmax}(s)[\hat{y}])$, where $\hat{y} = \arg\max(s)$ since pseudo-labels come from samples with confidence ≥ 0.8 (Section 5.1). This target is therefore exactly $-\log(\max\text{softmax}(s))$ — a deterministic, analytically computable function of the inputs. This means the regression model is being trained to approximate a function already available in closed form. As a result, RTA's view-selection criterion at test time is *potentially identical* to sorting by maximum softmax confidence, requiring zero training. The paper provides no comparison against this obvious baseline. Without it, the paper cannot demonstrate that the regression mechanism contributes anything beyond "use confidence instead of entropy for view selection." This is not an optional ablation — it is the critical experiment for validating the method's core contribution. Equations (4)–(5) and the training description in Section 5.1 confirm this concern is grounded in the paper as written.

- **Potential training/test data overlap** — Section 5.1 states the regression model is trained on "ImageVal-12k," sampled from ImageNet's validation set with confidence ≥ 0.8. A primary test benchmark is ImageNet-1k. If ImageVal-12k shares images or is a subset of the ImageNet evaluation split, RTA's regression has been trained on the same distribution—or the same images—used for testing. No competing method uses any ImageNet-specific training data in this setup. The paper does not clarify the provenance of ImageVal-12k or its overlap with evaluation benchmarks.

### Minor
- **Confidence threshold mismatch**: The regression is trained only on high-confidence (≥ 0.8) CLIP predictions. At test time, augmented views of OOD images (e.g., ImageNet-A) may predominantly fall below this threshold, placing the regression in an extrapolation regime unseen during training. This is precisely the scenario where TTA matters most, and the paper does not analyze robustness to this mismatch.
- **Notation errors in Section 4.3**: Equations (8)–(10) use the superscript `x_i^{reg}` (regression) when describing test-time computation; Algorithm 2 correctly refers to test instances. The disconnect is confusing and one should use `x_i^{test}` throughout Section 4.3.
- **Undefined superscript in Eq (6)**: `\mathcal{L}_{CE}^w` appears in the leaf-value definition without defining what weighting $w$ represents.

### Trivial
- **Table 4 duplicate row**: Two rows are labeled "TDA [CVPR 2024]" in the ViT-B/16 section of Table 4 with different values (e.g., 88.63 vs. 88.24 on Pets). One appears to be a copy-paste error, likely replacing MTA or another method.

## Nice-to-Haves
- Characterize what the LightGBM tree actually learns (e.g., does it weight the top-1 logit vs. secondary logits, or does it essentially threshold on max-softmax?). The Spearman analysis in Figure 3 is a start but does not inspect the learned tree structure.
- Sensitivity analysis: how sensitive are results to the pseudo-label confidence threshold (currently fixed at 0.8)?
- Ablation on cross-dataset generalization of the regression: train on one domain (e.g., ImageVal-12k) and test on a clearly disjoint domain (e.g., EuroSAT) to validate that the regression is truly domain-agnostic.

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **T-SNE and Spearman analyses are "uninformative"** (harsh critic): The critic argues these analyses trivially show correlation since LCE is computed from logits. While the mathematical point is correct, the visualizations serve to motivate the non-linearity of the mapping. This is a minor presentational judgment call, not a substantive weakness. Removed.

- **Distribution mismatch as separate weakness** (merged into Minor): Retained in condensed form above.

## Novel Insights
The Ceiling TTA analysis (Tables 1–2) constitutes the paper's most original contribution: a systematic, large-scale demonstration that entropy is a fundamentally suboptimal proxy for view quality in TTA, with true LCE offering 10–25 pp headroom. This exposes a longstanding structural limitation of entropy minimization as the de facto TTA criterion and motivates a new research direction — approximating LCE without labels — regardless of whether the specific regression mechanism is the right solution. The key unresolved question is whether the performance gap is closed by learning a regression or by simply switching from entropy to max-softmax confidence.

## Suggestions
1. **Add the max-softmax confidence baseline** (select top-k views by $\max_l \text{softmax}(s)_l$, no training required). If RTA beats this baseline, the regression mechanism is validated. If not, reframe the paper's contribution as "confidence-based selection outperforms entropy-based selection," which is still a valid but simpler contribution.
2. Clarify the provenance of ImageVal-12k and confirm whether it overlaps with ImageNet evaluation images.
3. Fix Table 4 (duplicate TDA row) and Section 4.3 notation.

## Score and Decision

**Anchor papers:**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `lF9QXpfNHm.md` | 4.67 | R1 | TTA for VLMs (borderline reject); less experimental breadth than RTA but clearer mechanism |
| `Rc3RP9OoEJ.md` | 5.00 | R1 | In-context TTPT for CLIP (rejected 5); comparable scope, also has missing ablations |
| `O4LoPhRSfb.md` | 5.17 | R1 | Text-augmented VLM (borderline reject); narrower scope |
| `jzzEHTBFOT.md` | 6.00 | R1 | C-TPT for CLIP TTA (accepted 6); a cited baseline in RTA itself, well-justified mechanism |
| `EFZEdHB3Mp.md` | 6.25 | R1 | DynaPrompt TTPT (accepted 6.25); clearly justified contribution, comparable empirical scope |
| `kIP0duasBb.md` | 6.67 | R1 | CLIP reward TTA (accepted 6.67); well-justified mechanism with CLIP as reward model |
| `pdzHpQbGrn.md` | 2.50 | R1 | Active TTPT (rejected 2.5); much weaker paper with less experimental validation |
| `TPZRq4FALB.md` | 8.00 | R1 | Multi-modal TTA (strong accept); clearly stronger problem setup and contribution |

**Round 1 bracket**: 4–6. RTA's empirical breadth and Ceiling TTA finding are stronger than the rejected 4.67/5.0 papers. However, the missing max-softmax baseline is a meaningful gap that prevents placement at 6+ alongside methods with clearly justified mechanisms (C-TPT, DynaPrompt, RLCF).

**Round 2**: The paper falls squarely between the 5.0 rejected and 6.0 accepted papers. Its empirical work is more comprehensive than typical rejects in this range, but the central mechanism question (regression vs. confidence) is unresolved — a gap that reviewers of papers like C-TPT (6.0) and DynaPrompt (6.25) would note as disqualifying at the current form. Score: **5.0**.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>