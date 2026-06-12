## Summary
This paper addresses the "copy-paste artifact" in identity-consistent image generation — the tendency of models to directly replicate reference faces rather than preserving identity across natural variations in pose, expression, or lighting. The authors contribute: (1) MultiID-2M, a large-scale paired dataset of ~500k group photos with matched celebrity references across diverse appearances; (2) MultiID-Bench, an evaluation benchmark with a novel Copy-Paste (CP) metric that measures angular bias of generated images toward reference vs. ground-truth; and (3) WithAnyone, a FLUX-based model trained with GT-aligned ID loss, contrastive identity loss with extended negatives, and a 4-phase curriculum that progressively moves from reconstruction to paired identity-preserving synthesis.

## Strengths
- **Novel and well-designed CP metric (Eq. 2, Section 4)**: Defines angular bias of generated images toward reference vs. ground-truth, paired with Sim(GT) as primary metric instead of the conventional Sim(Ref). Figure 5 demonstrates that 12 existing methods cluster tightly on a regression curve (higher similarity → higher copy-paste), while WithAnyone breaks away — achieving Sim(GT)=0.460 with CP=0.144 (Table 1). This metric directly targets the identified failure mode and is a genuine conceptual contribution likely to influence how the field evaluates identity-preserving generation.

- **Large-scale paired dataset fills a real data gap (Section 3)**: MultiID-2M provides ~500k group photos with ~3k identities averaging ~400 references each, plus 1.5M unpaired images. The FFHQ-only ablation (Table 3, Sim(GT)=0.224 vs. full 0.405) quantitatively demonstrates the dataset's importance. The construction pipeline is described in detail, with ethics considerations around CC licensing and anonymization.

- **GT-aligned landmark ID loss is practical and well-motivated (Eq. 4, Section 5.1)**: Using ground-truth landmarks for face alignment during training avoids noisy landmark extraction at all noise levels, unlike prior compromises (PortraitBooth's low-noise-only restriction or PuLID's full denoising cost). Figure 7 shows this yields lower ID loss and higher-variance gradients across all noise levels. Table 3 confirms: removing GT-align reduces Sim(GT) from 0.405 to 0.385.

- **External validation on OmniContext (Table 1b)**: WithAnyone scores 6.52 overall on OmniContext's single-character subset, outperforming all face-specific methods and several general models, confirming results are not overfitted to MultiID-Bench.

- **Coherent end-to-end narrative**: The paper identifies a problem (copy-paste), formalizes it (CP metric), builds infrastructure to study it (MultiID-2M, MultiID-Bench), and solves it (WithAnyone). Motivation, method, experiments, and conclusions are well-aligned throughout.

## Weaknesses

### Fatal
None.

### Major
- **Data vs. method contribution not disentangled in baselines**: WithAnyone is trained on an unprecedented scale of paired identity data (500k labeled paired images + 1.5M unlabeled + CelebA-HQ, FFHQ, FaceID-6M), while all 12+ baselines use their publicly released pretrained models. The FFHQ-only ablation (Table 3, Sim(GT)=0.224 vs. full 0.405) dramatically shows data's importance, yet no baseline is retrained on MultiID-2M to isolate method vs. data contribution. The ablation study (Table 3) ablates individual components of WithAnyone but does not include a "baselines retrained on MultiID-2M" comparison. Without even one such comparison, the headline claims about "breaking the trade-off" between fidelity and copy-paste remain entangled with a data advantage not available to prior work.

- **Multi-person results partially contradict the "trade-off breaking" claim**: In the single-ID setting (Table 1), WithAnyone does achieve a notably favorable position: near-best Sim(GT) (0.460 vs. best 0.464) with lowest CP (0.144). However, in the 3-4 person setting (Table 2b), GPT-4o achieves Sim(GT)=0.445 with CP=0.045, while WithAnyone gets Sim(GT)=0.414 with CP=0.171 — GPT-4o is better on *both* metrics. The paper attributes GPT-4o's high similarity to "prior knowledge of identities from TV series" (Table 2 footnote), but this only explains high similarity, not the very low CP=0.045. The paper does not clearly delineate where the trade-off breaking claim holds (single-ID, 2-person) versus where it does not (3-4 person).

### Minor
- **Small user study with limited statistical validation (Section 6.3)**: 10 participants ranking 230 groups is small for a ranking study. No variance, confidence intervals, or statistical significance tests are reported in the main text. The paper mentions "moderate positive correlation" between CP and human judgments but provides no correlation coefficient or p-value. Additionally, Figure 8 appears to compare only 5 of 13+ baselines (the parser-garbled names "Cure, UNO, iDetch, Uniformal, OmniGen" suggest WithAnyone, UNO, DreamO, UniPortrait, OmniGen), with no explanation of how these 5 were selected.

- **Extended negatives ablation produces a counterintuitive result that is unexplained (Table 3)**: Removing extended negatives (4096→63) causes CP to *drop* from 0.161 to 0.074 (lower = better for CP), while Sim(GT) drops from 0.405 to 0.368. The text states "the effectiveness of ID contrastive loss is greatly reduced" but does not explain why fewer negatives actually *improves* the copy-paste metric. This is confusing and deserves analysis — it suggests extended negatives may inadvertently increase copy-paste while improving identity fidelity, which would complicate the narrative.

### Trivial
None.

## Nice-to-Haves
- Error analysis of the ArcFace-based identity matching pipeline (Section 3, threshold 0.4) to quantify false positive/negative rates in web-scraped group photos, which could affect dataset quality.
- Ablation of the dual-encoder architecture (ArcFace + SigLIP branches) to clarify the architectural contribution.
- Ablation of loss weight choices (λ_ID = λ_CL = 0.1 held constant across all phases without discussion of sensitivity).
- Explicit verification methodology for test-train identity non-overlap, since both sets use celebrity web images.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Criticisms about parser artifacts in Figure 8 method names — these are PDF parser issues, not paper problems.
- Generic concerns about missing related works — cannot verify their existence.
- Any criticism about typos, formatting, or other presentation artifacts.

## Novel Insights
The most novel insight is the conceptual framing: prior work's reliance on Sim(Ref) as primary metric has inadvertently rewarded copy-paste behavior, creating a hidden incentive structure where the field has been optimizing for a failure mode. The CP metric (Eq. 2) formalizes this in a principled way, and Figure 5's demonstration that 12 existing methods fall along a single regression curve while WithAnyone breaks away is a compelling visual that will likely influence future evaluation practices. The shift from Sim(Ref) to Sim(GT) as the primary identity metric is a meaningful methodological advance, and the GT-aligned landmark loss (Eq. 4) is a simple but effective innovation for enabling identity supervision at all noise levels.

## Suggestions
- Retrain at least one strong baseline (e.g., PuLID or UniPortrait) on MultiID-2M with the authors' training infrastructure to disentangle data vs. method contribution.
- Expand the user study to 30+ participants with proper statistical tests and clarify which baselines are compared.
- Add a brief explanation for the counterintuitive extended-negatives ablation result.
- Restrict the strongest "trade-off breaking" claims to single-ID, or explicitly address why the multi-person gap doesn't undermine the narrative.

---

## Scoring Report

**Retrieved anchors across all rounds:**

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| ID-Booth | NWvsm2VxAM.md | 3.00 | 1 | Identity-consistent generation, rejected for limited novelty and weak results. WithAnyone is clearly much stronger. |
| Text To Stealthy Face Masks | 12iSWNLDzj.md | 3.00 | 1 | Face adversarial attacks, off-topic reject. |
| KAN See Your Face | razAcpFapu.md | 3.00 | 1 | Face privacy attack, off-topic reject. |
| MagicTailor | GwSL33Qx42.md | 4.33 | 1 | Component-controllable personalization, rejected. Less comprehensive than WithAnyone. |
| Event-Customized | 88Qm4fGWzX.md | 5.00 | 1 | New task + benchmark, rejected. WithAnyone has stronger results and more contributions. |
| Rethinking Attentions | kn2OZa8rOf.md | 5.00 | 1 | Zero-shot image editing, accepted. Less directly relevant. |
| Refine-by-Align | D9CRb1KZQc.md | 5.75 | 1 | Reference-guided refinement, accepted. Similar contribution level. |
| DreamBench++ | 4GSOESJrk6.md | 6.00 | 2 | Benchmark for personalized generation, accepted. WithAnyone is more comprehensive (benchmark + method + dataset). |
| UIFace | riieAeQBJm.md | 6.00 | 2 | Synthetic face recognition, accepted. Similar spirit, WithAnyone more ambitious. |
| Vec2Face | RoN6NnHjn4.md | 6.00 | 1 | Face dataset generation, accepted. WithAnyone contributes dataset + metric + method. |
| ILLUSION | qnlG3zPQUy.md | 6.00 | 2 | Deepfake dataset, accepted. Less relevant. |
| Cross-Modal Contextualized Diffusion | nFMS6wF2xq.md | 6.25 | 2 | Text-guided generation, accepted. Different scope. |
| InstantPortrait | ZkFMe3OPfw.md | 6.67 | 1 | Portrait editing with identity preservation, accepted. WithAnyone has more comprehensive contributions. |
| Commuting OD Flow | WeJEidTzff.md | 6.75 | 2 | Urban flow generation, off-topic. |
| One Slice Not Enough | Im2neAMlre.md | 7.33 | 2 | T2I evaluation methodology, accepted. Strong benchmarking paper. |
| NoiseDiffusion | 6O3Q6AFUTu.md | 8.00 | 1 | Image interpolation, accepted. Stronger but different domain. |
| One Step Diffusion | OlzB6LnXcS.md | 8.00 | 1 | Shortcut models, accepted. Stronger but different domain. |
| Detecting Memorization | 84n3UwkH7b.md | 8.00 | 1 | Memorization detection, accepted. Stronger but different domain. |

**Round 1 bracket: 5.5 – 7.5.** WithAnyone is clearly above the 5.0–6.0 reject/borderline range (ID-Booth at 3.0, Event-Customized at 5.0) and clearly below the 8.0+ strong-accept range. The conceptual contributions (CP metric, benchmark) and dataset place it above DreamBench++ (6.0) and UIFace (6.0), and it is comparable to or slightly above InstantPortrait (6.67).

**Round 2 narrowing: 6.5 – 7.0.** DreamBench++ (6.0, all 6s) is a pure benchmark paper; WithAnyone contributes benchmark + method + dataset. InstantPortrait (6.67) contributes a method + dataset for portrait editing; WithAnyone adds a novel metric and more comprehensive evaluation. The data/method entanglement and multi-person issues keep it from 7.5+.

**Final score: 7.0.** The paper's multi-faceted contributions (novel CP metric that reframes evaluation, large-scale paired dataset, comprehensive benchmark, working method with external validation on OmniContext) substantially outweigh its weaknesses. The data/method entanglement is the most significant concern but is addressable (retrain one baseline on MultiID-2M), and the conceptual contributions are valuable regardless.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>