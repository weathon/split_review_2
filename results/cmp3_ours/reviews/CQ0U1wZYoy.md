## Summary

PRISM proposes a conditional diffusion framework for compound degradation restoration with controllability for scientific imaging. Its key technical contribution is a weighted contrastive loss (Jaccard-weighted) that embeds a compositional latent structure — where images degraded by overlapping distortions are positioned closer to their constituent primitives in embedding space — enabling both joint removal of compound distortions and selective, prompt-guided restoration. The paper contributes a mixed-degradations benchmark (MDB, including the new Rooftop Cityscapes dataset), a downstream-task evaluation protocol across four scientific domains, and demonstrates state-of-the-art results on compound and zero-shot restoration.

## Strengths

- **The weighted contrastive loss (Eq. 1, line 96) with Jaccard weighting is a genuine and principled technical contribution.** The idea that an image with haze+rain should be closer in latent space to a haze-only image than to a noise-only image directly encodes compositional structure. This goes beyond standard contrastive losses that treat all negatives equally, and the ablation (Fig. 4) suggests it works.

- **The downstream-task evaluation protocol ( §4.2.1 ) is novel and important.** Evaluating restoration by its effect on off-the-shelf task models (landcover classification, species recognition, pit segmentation, panoptic segmentation) is the right approach for scientific applications. The microscopy example (Fig. 6) showing that super-resolution helps segmentation but denoising hurts it is a compelling demonstration of why blanket restoration is the wrong goal.

- **Strong empirical results across multiple benchmarks.** PRISM leads on PSNR (22.08) and SSIM (0.842) on MDB (Table 1) and dominates zero-shot results across three real-world datasets (Table 2) with margins of 1–2 dB in PSNR over the next best methods. These are not marginal improvements.

- **Well-motivated framing.** The three principles in §1 (simultaneous over sequential, precision over aesthetics, control over automation) provide a coherent thesis that the method and evaluation choices execute against.

## Weaknesses

### Major

1. **The selective-restoration protocol in Table 3 is described but not formalized.** The paper states what selective restoration means for each domain ("restoring only contrast" for camera traps, "removing haze" for urban scenes, super-resolution alone for microscopy — lines 242, 255–267), and even explains the scientific reasoning. However, it never states *how these choices were arrived at* — whether by domain-expert judgment, validation-set optimization, or exhaustive subset search. Since Table 3 is the primary evidence for the paper's claim that "controllability is not a convenience but a necessity" (contribution 3), this methodological ambiguity weakens the conclusion. If the selection was arrived at by trying all subsets, the comparison should be framed as an upper bound; if by fixed expert rule, that rule should be stated explicitly. **This does not invalidate the paper's core method or its other results, but it must be clarified for the third contribution to be properly evaluated.**

2. **Controllability is claimed as a key contribution but is never quantitatively evaluated.** The paper trains on *partial* prompts (remove a subset of distortions) and *negative* prompts (remove a non-present distortion) — line 76 — yet never measures whether the model correctly follows these instructions. The evaluation (§3.4 line 135) uses "manual restoration with predefined distortion types" — i.e., full restoration. There is no experiment that: (a) verifies that prompting to remove distortion A while leaving B leaves B largely unchanged; (b) measures partial-prompt accuracy; or (c) tests negative-prompt behavior. The microscopy example (Fig. 6) is qualitative. A central architectural claim — that the compositional latent space supports predictable selective intervention — therefore rests on indirect evidence.

### Minor

3. **The quality-aware regularizer (Eq. 2, line 106) is under-specified.** The loss uses $\hat{p}(c \mid e_{\text{clean}})$, "the predicted probability of distortion $c$ from $e_{\text{clean}}$." The paper does not describe how this classifier $\hat{p}$ is trained (loss function, architecture, data), whether it is the same MLP used for automated restoration (line 129), or how many classes it predicts. This is a methodological gap that prevents reproduction and leaves open the question of whether the regularizer functions as intended.

4. **Baseline training conditions are stated ambiguously.** Line 120 says "all baselines are trained on the fixed set of primitive distortions," but line 175 says "OneRestore is trained on composite datasets like PRISM." If the All-in-One and Diffusion baselines were trained only on single-distortion data while PRISM and OneRestore see compound data, then part of PRISM's advantage in Table 1 could stem from this training-data asymmetry. The paper needs to clarify what training data each baseline used.

5. **The automated MLP classifier is not evaluated.** The automated restoration pipeline (line 129) depends on a lightweight MLP that predicts multi-label distortion sets from image embeddings. No accuracy, precision/recall, or confusion analysis is reported for this component. (This does not affect the manual-prompting results, which use predefined types — but automated restoration is presented as a mode of use.)

6. **PRISM is second-best on FID (48.97 vs. MPerceiver's 48.18) in Table 1 without discussion.** For a method emphasizing fidelity, being outperformed on perceptual quality by a baseline warrants at least a brief comment — especially since one of the paper's three principles is "precision over aesthetics."

### Trivial

7. "DiffPlusGin" in Table 2 (line 214) appears to be a typo for "DiffPlugin" (correctly spelled in Table 1). Should be corrected for consistency.

## Nice-to-Haves

- Add a quantitative controllability evaluation: for images with distortions {A, B, C}, measure restoration quality when prompting to remove only {A}, only {B}, {A, B}, etc., and verify that non-targeted distortions remain largely unchanged. This would directly validate the core architectural claim.
- Include the microscopy tradeoff table (Table 4) in the main paper — it is one of the best illustrations of why controllability matters.
- Clarify whether the training data sources (e.g., Sen12MS, iWildCam, BioSR) have any overlap with the downstream evaluation sets (i.e., are clean images from the same datasets used for both training and testing, even if held-out).

## Removed Points

- "The expert-in-the-loop scenario is not quantitatively evaluated" — folded into weakness 2 (controllability not quantitatively evaluated). The original framing as a separate fatal issue was redundant.
- Critic's concern that the SCPM borrowed from AutoDIR might be frozen/transferred — the paper explicitly says "following Jiang et al. (2024)" and "full architectural details... in Appendix E." Without seeing the appendix, this is speculation about content that exists. Removed.
- "Prompt variability analysis deferred to appendix" — the paper states this is in Appendix E; appendix content is stripped but exists. Removed.
- "Missing Table 4 in main text" — table is referenced as existing in the paper; it is likely in the stripped appendix. Removed.
- Critic's speculation that selection might be oracle-based — the paper describes domain-specific reasoning for each choice, making this speculation rather than a verified flaw. The weakness (lack of formal protocol) is retained as Major weakness 1; the stronger accusation of oracle-based cherry-picking is removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Specify the selective-restoration protocol explicitly.** State: "For each domain, a domain expert selected the distortion subset to remove based on task requirements, blinded to the downstream test results." Or, if different rules were used across domains, report each rule and justify it.
2. **Add a simple controllability experiment** measuring how well PRISM preserves non-targeted distortions when performing partial restoration (e.g., prompt to remove haze only and measure whether rain distortions remain at their original severity).
3. **Clarify the quality-aware regularizer implementation** — how $\hat{p}$ is trained, its architecture, and whether it is shared with the automated-restoration MLP.
4. **Disambiguate baseline training conditions.** State explicitly which baselines were retrained by the authors, on which data, and which were used as originally published.

## Score and Decision

Round 1 bracket: between 5.5 and 7.5 (calibration search against strong-reject, reject, borderline, accept, and strong-accept bands in the human-review corpus).

Round 2 narrowing: the paper compares favorably to the DCPT paper (avg 6.25, accepted — similar scope, comparable clarity issues, but PRISM has stronger novelty), the diffusion-based dehazing paper (avg 5.60, rejected — narrower scope, weaker results), but falls short of the face-restoration paper (avg 7.33, accepted — cleaner exposition, more complete evaluation of the key claim). The selective-restoration protocol gap and missing controllability evaluation prevent a score above 7.0.

**Anchors retrieved across all rounds:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/u1cQYxRI1H.md` — score 0.50, round 1 strong-reject band. Completely different topic; no meaningful comparison.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5lUdTogEL3.md` — score 1.00, round 1 strong-reject band. Different topic; no meaningful comparison.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/P49gSPmrvN.md` — score 1.00, round 1 strong-reject band. Different topic; no meaningful comparison.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/kKXIYUi8ff.md` — score 3.00, round 2. Different domain; PRISM is stronger.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/vK8C37eHXM.md` — score 3.20, round 2. Different domain; PRISM is stronger.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/JmGEZXkCH3.md` — score 3.67, round 2. Image SR augmentation; narrower scope, weaker results than PRISM.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/dUTwqiEked.md` — score 4.25, round 2. Different domain.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rwmWd2rjP1.md` — score 4.75, round 2. Different domain.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/YOKnEkIuoi.md` — score 5.80, round 2. Conditional diffusion for inverse problems. Comparable scope; PRISM has stronger novelty and broader evaluation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/f4aMqhYG7z.md` — score 5.60, round 2. Diffusion-based dehazing. Narrower scope; PRISM has stronger results.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/PacBhLzeGO.md` — score 6.25, round 2. Degradation classification pre-training. Comparable; PRISM has stronger novelty but weaker exposition.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/JkCJBoNUcU.md` — score 6.00, round 2. Realistic data generation for SR. Different framing; comparable technical quality.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ePOjNlOjLC.md` — score 6.25, round 2. Diffusion conditioning. Different topic.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/m9RNBZewW2.md` — score 7.33, round 2. Multi-modal face restoration. Stronger exposition and more complete evaluation of the core claim.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9UGfOJBuL8.md` — score 7.33, round 1. Longitudinal data generation. Different domain.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6O3Q6AFUTu.md` — score 8.00, round 1. Diffusion interpolation. Different topic.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/zMoNrajk2X.md` — score 8.00, round 1. Condition-annealed sampling. Cleaner, more complete.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/I5lcjmFmlc.md` — score 8.00, round 1. Robust classification. Different topic.

**Final determination:** The paper has genuine technical contributions (weighted contrastive loss, downstream evaluation protocol) and strong results. The two Major weaknesses — the unspecified selective-restoration protocol and the missing quantitative evaluation of controllability — are addressable in revision but currently prevent the paper's central claims from being fully verifiable. Score reflects a paper that is above the borderline threshold in core merit but needs revision on key exposition and evaluation points.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>