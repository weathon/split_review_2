Now let me compile all the information and write the final review.

**Calibration Anchor Summary:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| u1cQYxRI1H.md | 0.50 | R1 | No | Completely unrelated (illumination harmonization) |
| 5lUdTogEL3.md | 1.00 | R1 | No | Unrelated (person re-ID) |
| 8QTpYC4smR.md | 1.00 | R1 | No | Unrelated (LLM survey) |
| FwkYeLovHk.md | 3.33 | R1 | No | Weak-to-strong gen. for CLIP; weaker results, not SSL focused |
| HfJxXbXlYJ.md | 3.00 | R1 | No | LLM2CLIP — extending CLIP via LLMs, different setting |
| 1rgMkDWfYV.md | 4.50 | R1 | Yes | **Cleaning label noise with CLIP** — similar unfair-comparison issue; rejected due to both unfair comparison and inferior results. CaPT avoids the "inferior results" problem and has stronger evaluation. |
| G9Ea7mlqGO.md | 3.80 | R1 | No | CLIP online continual learning; different setting |
| 97D725GJtQ.md | 5.80 | R1+R2 | Yes | **Semi-supervised CLIP training (SemiCLIP)** — most directly related. Accepted despite limited novelty. CaPT has more novel architecture and stronger experiments, but similar framing concerns. |
| 5BXWhVbHAK.md | 6.33 | R2 | Yes | **Cross-modal synergy without paired data** — similar asymmetric-modality theme. Accepted with strong theory. CaPT has stronger SSL-specific experiments but weaker theory. |
| ptCIlV24YZ.md | 5.80 | R1 | No | Image clustering with CLIP; related but different task |

**Bracket (R1):** 5.0–6.5

**Narrowing (R2):** CaPT's most negative item (evaluation framing, fav -0.83) is less severe than SemiCLIP's most negative (-2.80, -1.49) and the cross-modal synergy paper's (-2.45). CaPT's strengths have higher favorability (10.77, 9.99, 9.98) than either anchor's top strengths. The comparison-fairness weakness is real but not fatal (CaPT includes CLIP baselines in Table 1 and CLIP-based ablations in Table 6). The disconnected theorem (fav -0.73) is a minor blemish. Three of five weaknesses have *positive* favorability (labeled loss: 5.88, STL-10: 4.80, FGVCAircraft: 5.14), meaning the model considers them minor or informational rather than score-dragging. CaPT sits above SemiCLIP (5.80) due to stronger architecture and experiments, but below the cross-modal synergy paper (6.33) which had genuine theoretical depth.

**Final score: 6.0**

---

## Summary

This paper proposes CaPT, a framework that integrates CLIP into semi-supervised learning via asymmetric-modalities co-training between a unimodal ViT (fully fine-tuned) and CLIP (adapter-tuned). The key idea is that two vision-only ViTs suffer from a "pattern-homogeneity bottleneck" (similar representations), while CLIP's multimodal representations provide complementary information that enriches mutual learning. Co-pseudo labels with entropy-based weighting combine predictions from both branches. Experiments show strong results across USB benchmarks, ImageNet, extreme low-label regimes, and fine-grained datasets, with modest computational overhead.

## Strengths

- **Clean architectural concept (Section 3, Figure 2d).** The asymmetric-modalities co-training design (multimodal CLIP + unimodal ViT) is well-motivated. The pattern-homogeneity bottleneck argument — two vision-only ViTs converge to similar representations even with different initializations — is supported by attention-map evidence in Figure 3. Replacing one branch with a multimodal model incorporating textual context is a natural and effective fix for prior co-training limitations. **[favorability=10.77]**

- **Strong and consistent results on most benchmarks (Tables 1, 2, 3, 5).** On CIFAR-100 (2 labels/class), CaPT leads by 4.09% over RegMixMatch. On ImageNet (10 labels/class), it leads by 9.33% top-1. Under one-label-per-class (Table 3), the 21.38% gap on CIFAR-100 is striking. Results hold across three random seeds with lower variance than baselines. **[favorability=9.98]**

- **Efficiency analysis (Table 4).** The 8% memory and 11% time overhead over FreeMatch for a 6.23% accuracy gain on CIFAR-100 makes the practical case persuasively. CaPT is both faster and more accurate than RegMixMatch. **[favorability=9.99]**

- **Thorough ablation study (Table 6).** The ablations (CaPT-Ada, CaPT-Deb, CaPT-Uni, only UPM, only MPM, w/o feat aug., equal weights) systematically isolate each component's contribution. CaPT-Deb's 12.73% drop on EuroSAT cleanly demonstrates why naive CLIP integration fails, and the contrast between variants disentangles the sources of improvement. **[favorability=9.87]**

- **Clear problem motivation (Section 1, Figure 1).** The empirical analysis — SSL methods' sharp accuracy drop under one-label-per-class, the effect of labeled sample quality on pseudo-label accuracy, and the heatmap showing SSL's diminishing gain from unlabeled data as labels shrink — concretizes the problem CaPT addresses. **[favorability=7.18]**

## Weaknesses

### Fatal
None.

### Major

- **Evaluation framing conflates CLIP's external knowledge with CaPT's SSL innovation.** All 12 SSL baselines in Table 1 are pure vision models (pre-trained ViTs); CaPT additionally uses CLIP's 400M-image-text-pair pre-training. The headline 21.38% gap on CIFAR-100 is presented as "outperforming the second-best method" without highlighting that the comparison methods lack CLIP access. The ablation study (Table 6) provides CLIP-based comparisons (CaPT-Ada, CaPT-Deb, CaPT-Uni), but these are relegated to the ablation section rather than the main results tables. Furthermore, on STL-10 (Table 1), adapter-tuned CLIP alone (96.86%) and CLIP zero-shot (97.18%) both outperform CaPT's final unimodal network (96.07%), yet this is not discussed. A test-time ensemble of CLIP + FreeMatch is not evaluated as a baseline, which would help isolate the benefit of co-training from simpler alternatives. The paper would be strengthened by including CLIP-based SSL methods (DebiasPL, CLS) as primary comparators in the main tables and clearly separating gains from CLIP's prior vs. gains from the co-training mechanism. **[favorability=-0.83]**

### Minor

- **Theorem 1.1 is disconnected from the method and does not constitute a substantive theoretical contribution to CaPT.** The bound is for a nearest-prototype classifier on raw pixels under a Gaussian-mixture model — not for any modern SSL method with deep networks, augmentation, and consistency regularization. The theorem does not involve CLIP, co-training, or any aspect of CaPT. The $2^{d/2}$ term makes the bound vacuous for realistic image dimensions (e.g., $d=3072$ for CIFAR-100). The qualitative insight (pseudo-label error depends on labeled data quality/quantity) is already demonstrated empirically in Figure 1 and is well-understood in the SSL literature. **[favorability=-0.73]**

- **The training objective for labeled data is not specified in the main text.** The paper describes consistency losses on unlabeled samples (Equations 4, 15) but never states whether a supervised cross-entropy loss is also applied on the limited labeled samples. Standard SSL methods combine a supervised loss on labeled data with an unsupervised consistency loss on unlabeled data. If CaPT includes a supervised loss, this should be stated; if it does not, that is a noteworthy design choice relevant to the claim of "breaking label dependency." **[favorability=5.88]**

- **The STL-10 results show CaPT's final unimodal network underperforming both adapter-tuned CLIP and CLIP zero-shot (Table 1) without analysis.** With 4 labels/class, CaPT (96.07%) < adapter-tuned CLIP (96.86%) < CLIP zero-shot (97.18%). Since the method claims to "break label dependency," understanding why the co-trained ViT does not match CLIP's prior on this dataset would strengthen the paper. **[favorability=4.80]**

- **On FGVCAircraft (Table 5), CaPT underperforms FreeMatch** (50.12% vs 51.43% with 5 labels/class, 64.33% vs 65.82% with 10 labels/class). The paper acknowledges this ("discussed in Appendix N") but provides no analysis in the main text. Since CLIP zero-shot is only 18.97% on this dataset, the failure pattern is informative — CaPT inherits CLIP's blind spots — and deserves main-text discussion. **[favorability=5.14]**

### Trivial
None.

## Nice-to-Haves

- Add a CLIP zero-shot row to Table 2 (ImageNet) so readers can assess how much SSL training on 10 or 100 labels/class improves over CLIP's pre-existing knowledge.
- Evaluate a simple test-time ensemble of FreeMatch + CLIP (weighted or unweighted) as a baseline to isolate the benefit of co-training from simpler alternatives.
- Include CLIP-based SSL methods (DebiasPL, CLS) as primary comparators in the main results tables alongside vision-only baselines.
- Add a plot of entropy weights $\Gamma^a$ and $\Gamma^b$ over training steps to support the qualitative claim about CLIP dominating early training and the unimodal network gradually taking over.
- Explicitly state whether a supervised loss is applied on labeled data, and if so, how it is incorporated into the training objective.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- "Paradoxically and unexpectedly phrasing overstates novelty" — Removed as a style nitpick.
- "Large variance of SSL baselines vs CaPT small variance on STL-10 is suspicious" — Removed as speculative without evidence.
- "Feature-level vs input-level augmentation asymmetry makes comparison less clean" — Removed as a minor design choice, not a substantive weakness.
- "Conclusion overstates generality" — Removed as subjective; the paper acknowledges FGVCAircraft limitations.
- Generic/duplicative strengths about "importance of the problem" — Removed as not specific to this paper.

## Novel Insights

The input reviews do not surface an insight that goes beyond what the paper itself contributes. The core insight — that asymmetric-modalities (multimodal vs unimodal) co-training avoids the pattern-homogeneity bottleneck of vision-only co-training — is the paper's own contribution, not a novel observation from the review process.

## Suggestions

1. Reframe the evaluation to primarily compare against other CLIP-integrating SSL methods (DebiasPL, CLS), with vision-only SSL baselines as an additional reference.
2. Discuss the STL-10 anomaly: why does the co-trained ViT not match CLIP zero-shot on this dataset?
3. Consider removing or substantially downplaying Theorem 1.1; it does not inform the method and is vacuous for realistic input dimensions.
4. Add a CLIP zero-shot row to Table 2 (ImageNet) and a simple CLIP+FreeMatch ensemble baseline.
5. Explicitly state whether a supervised loss on labeled data is used.

## Score and Decision

**Round 1 bracket:** 5.0–6.5. The paper sits well above the 4.50 noisy-label anchor (which was rejected due to unfair comparison *and* inferior results) and slightly above the 5.80 SemiCLIP anchor (directly comparable topic, accepted). The 6.33 cross-modal synergy anchor has stronger theory but weaker SSL-specific experiments.

**Narrowing:** CaPT's most negative item (evaluation framing, favorability -0.83) is less severe than the most negative items of both SemiCLIP (-2.80, -1.49) and the cross-modal synergy paper (-2.45). Three of five weaknesses have *positive* favorability (5.88, 4.80, 5.14), indicating they are minor concerns. The strengths have very high favorability (7.18–10.77). The evaluation framing issue is real but not fatal — CaPT includes CLIP baselines in Table 1 and CLIP-based ablations in Table 6 — and the architectural contribution (asymmetric-modalities co-training) is genuinely novel.

**Final score:** 6.0 — borderline accept. The paper presents a clean, well-motivated architecture with strong empirical results and modest overhead. It would benefit from revised framing that more clearly separates CLIP's contribution from the co-training innovation.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>