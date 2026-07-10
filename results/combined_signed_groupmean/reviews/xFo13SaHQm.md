## Summary

This paper addresses the "copy-paste artifact" in identity-consistent image generation, where models replicate the reference face rather than generating natural variations. It makes three contributions: (1) **MultiID-2M**, a large-scale paired dataset of 500k multi-person images with multiple references per identity; (2) **MultiID-Bench**, a benchmark with a Copy-Paste (CP) metric that measures the relative bias of generated images toward reference vs. ground truth; and (3) **WithAnyone**, a FLUX-based model using paired training, a GT-aligned ID loss, and a contrastive ID loss with extended negatives. Results show WithAnyone achieves competitive identity fidelity (Sim(GT)) while substantially reducing copy-paste artifacts compared to existing face customization models.

## Strengths

- **Problem identification is clear and well-motivated (§1, Fig. 2):** The "copy-paste artifact" — where ID-consistent models replicate the reference image rather than generating variations — is a genuine and underappreciated failure mode. The paper convincingly shows (Fig. 2) that real face-pair similarity scores range from 0.30–0.77, while models like InstantID produce an artifact peak near 1.0.

- **MultiID-2M is a large-scale, genuinely useful dataset:** 500k paired multi-person images across ~3k identities with hundreds of references each, plus 1.5M unpaired images, fills a real gap that has forced the field to rely on reconstruction-based training. The data construction pipeline is sensible and well-documented.

- **The CP metric (Eq. 2) is a principled formalism:** It measures the relative bias of the generated image toward the reference vs. ground truth, normalized by their distance. The paper is honest about its limitation (low Sim(GT) can trivially achieve low CP) and introduces a Sim(GT) threshold filter to address this.

- **WithAnyone's GT-aligned ID loss (§5.1) is a clean engineering insight:** Using GT landmarks to align the generated image for ArcFace feature extraction avoids noisy landmark detection on generated images without expensive full denoising (PuLID) or discarding supervision at high noise (PortraitBooth). Fig. 7 confirms its effectiveness across noise levels.

## Weaknesses

### Major

1. **The automated aesthetics gap is unaddressed.** WithAnyone achieves the lowest aesthetics score (Aes=4.783) among all 14 methods in Table 1 — well below the second-lowest (UMO at 4.850), and far below general models like GPT-4o (5.344) and FLUX.1 Kontext (5.319). Phase 4 ("Quality tuning") was specifically designed to "enhance perceptual fidelity" but did not close this gap. The paper then claims "superior visual quality" based on a user study (Fig. 8) that compares only 5 methods — a different, non-representative subset that excludes most of the strong aesthetic performers. The discrepancy between the automated metric (WithAnyone is worst) and the user study (WithAnyone is best on a limited set) is not discussed, and the aesthetic trade-off is never acknowledged. This is the paper's most significant unaddressed weakness.

### Minor

2. **The "breaking the trade-off" framing (§1, conclusion) overstates the result.** WithAnyone achieves a better Pareto point — it is off the regression curve in Fig. 5, which is a real achievement. But the trade-off still exists: methods with lower Sim(GT) still achieve lower CP (e.g., DreamID at CP=0.079 with Sim(GT)=0.389). This is advancing the Pareto frontier, not "breaking" the trade-off.

3. **The user study (Fig. 8) has presentation and rigor issues.** The method names differ from the main evaluation ("Cure" vs. "Ours", "iDetch" vs. "ID-Patch", "Uniformal" vs. "UniPortrait"), which is confusing. The study does not report inter-rater reliability or statistical significance of the ranking differences, making it hard to assess the robustness of the rankings.

4. **No failure cases or limitation discussion is included.** The qualitative results (Fig. 6) are uniformly positive. Showing examples where WithAnyone struggles — poor identity preservation, aesthetic degradation, or failure to produce sufficient variation — would increase trust and help users understand the method's limitations.

5. **The paper does not discuss generalization to non-celebrity faces.** Since MultiID-2M consists entirely of celebrities clustered by name, the data construction pipeline may not transfer to non-public figures. This is a natural limitation worth acknowledging.

6. **The embedding matching threshold of 0.4 for identity assignment is stated without justification.** Given the paper's own observation that real face pairs can have similarities as low as 0.30 (Fig. 2), a 0.4 threshold may miss legitimate same-identity pairs.

### Trivial

7. DreamO (Table 1, single-person evaluation) and DreamID (Table 2, multi-person evaluation) appear to be different methods but this naming distinction is not clarified.

## Nice-to-Haves

- A human evaluation of identity correctness using **only the reference image** (the inference setting) would help disentangle whether WithAnyone's lower Sim(Ref) reflects genuinely reduced copying or reduced identity preservation relative to methods like InstantID and PuLID.
- A sensitivity analysis for the CP filtering thresholds (0.40 for single-person, 0.35 for multi-person) would increase confidence in the metric.
- Clarifying whether the Sim(GT) threshold filter was applied to the CP values in the ablation table (Table 3). Without this, the "w/o Ext. Neg." row's lower CP (0.074 vs. 0.161) may simply reflect lower identity similarity rather than reduced copy-paste.

## Removed Points

These points were removed from the input review with justification:

- **"Inference-time identity signal depends entirely on Sim(Ref)"** — This is inherent to the evaluation setting and the paper already acknowledges Sim(Ref) rewards copying. The suggested extra human evaluation is a nice-to-have, not a weakness.
- **"DreamID/DreamO naming inconsistency in §2"** — The paper does not mention either method in §2; DreamO and DreamID appear in different tables (single vs. multi-person) and are likely distinct methods. The criticism is factually inaccurate.
- **Reproducibility concerns about missing training durations, batch sizes, hardware** — These details were likely in the appendix (stripped by parser). Per rules, removed.
- **Generic/superficial strengths** (e.g., "addressing an important problem") — removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The synthesis of reviews confirms that the core contributions (copy-paste artifact identification, CP metric, MultiID-2M dataset, GT-aligned ID loss) are solid, while the aesthetic quality gap is the primary unresolved concern.

## Suggestions

1. Add a **Limitations** paragraph discussing the aesthetic trade-off, generalization to non-celebrity faces, and the train-test mismatch in GT-aligned ID loss (GT landmarks used at training but unavailable at inference).
2. Apply the Sim(GT) threshold filter to all CP values in Table 3 and report both filtered and unfiltered numbers. Clarify whether the contrastive loss is primarily responsible for identity fidelity (Sim(G)) or copy-paste reduction (CP).
3. Rename user study methods ("Cure" → "Ours", "iDetch" → "ID-Patch", "Uniformal" → "UniPortrait") to match the main evaluation. Report inter-rater reliability and statistical significance.
4. Show at least one representative failure case in the qualitative results.
5. Tone down "breaking the trade-off" to language about advancing the Pareto frontier.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| IC-Light | 0.50 | R1 | No | Irrelevant topic |
| L-ReID | 1.00 | R1 | No | Irrelevant topic |
| Cross-Lingual Robots | 1.00 | R1 | No | Irrelevant topic |
| ID-Booth | 3.00 | R1 | Yes | Similar topic; much weaker results & limited novelty. This paper is clearly stronger. |
| Adv Face Masks | 3.00 | R1 | No | Different topic |
| Chinese Ancient Buildings | 3.00 | R1 | No | Different topic |
| Event-Customized | 5.00 | R1 | No | Somewhat similar but different sub-area |
| DiffDeID | 4.40 | R1 | No | Face de-identification, different task |
| **Subject-Diffusion** | **5.00** | **R1** | **Yes** | **Most similar scope (personalized gen + dataset + benchmark). Weaker on novelty (dataset scale vs. algorithmic insight). This paper is stronger.** |
| Personalized Repr. | 5.60 | R2 | No | Different sub-area (representation learning) |
| **Vec2Face** | **6.00** | **R1** | **Yes** | **Face dataset generation. Stronger on empirical results. Accepted.** |
| UIFace | 6.00 | R2 | No | Synthetic face recognition; different task |
| **DreamBench++** | **6.00** | **R2** | **Yes** | **Benchmark paper; comparable contribution scope but this paper adds method.** |
| **DisEnvisioner** | **6.00** | **R2** | **Yes** | **Customized image generation. Had similar weakness profile (not SOTA on all metrics). Accepted.** |
| CADS | 8.00 | R1 | No | Different topic |
| Dataset Bias | 8.00 | R1 | No | Different topic |
| Shortcut Models | 8.00 | R1 | No | Different topic |

**Round-1 bracket:** 5.0–6.5, anchored by Subject-Diffusion (5.0, rejected) at the lower end and Vec2Face / DisEnvisioner (6.0, accepted) at the upper end.

**Round-2 narrowing:** Compared against DisEnvisioner (6.0, accepted), which shared weaknesses about not being SOTA on all metrics (impact -9.76) but was accepted. The current paper shares a similar profile: strong contributions but one notable weakness (aesthetics gap). The scored items show strengths in the +9.5–10.0 range (problem identification, dataset, GT-aligned ID loss) comparable to DisEnvisioner's strongest strengths, with one decisive negative (aesthetics: -10.00) similar to DisEnvisioner's "-9.76 not SOTA on all metrics". The aesthetics concern is genuine but bounded: the user study (even on a limited set) shows WithAnyone winning on aesthetics among 5 methods, and the automated metric may not capture all aspects of visual quality. The paper is clearly stronger than Subject-Diffusion (5.0), which was rejected primarily for insufficient novelty.

**Final score: 6.0** — Borderline accept. The contributions (dataset, benchmark with principled CP metric, and a method with clean evidence of copy-paste reduction) are solid and fill real gaps. The aesthetic quality gap is the primary concern and should be addressed, but it does not invalidate the core claims about copy-paste reduction and identity fidelity.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>