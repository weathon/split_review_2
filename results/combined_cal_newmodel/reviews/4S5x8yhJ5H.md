Now I have all the data I need. Let me compile the final review.

**Round 1 bracket:** Based on comparison with anchors, the paper sits between HiDF (avg 4.25, Reject) and EyeFairness (avg 5.50, Reject), likely in the 3.5–5.0 range.

**Narrowing analysis:** VIBEFACE's most damaging weakness (frame-level accuracy, favorability -1.59) is comparable to HiDF's worst (-1.84) and less severe than EyeFairness's (-2.21). VIBEFACE's strengths (ethical compliance, up to 11.61 favorability) are genuinely high but the four negatively-rated weaknesses (frame-level accuracy, fixed threshold, no eKYC-gap evidence, flash-reference confound) collectively pull the score down. The paper is a genuine dataset contribution with a well-designed acquisition protocol, but the evaluation methodology does not convincingly demonstrate why the eKYC scenarios matter, and the verification metrics are non-standard.

**Final score:** 4.0 (borderline reject).

## Summary

VIBEFACE introduces a new multimodal facial dataset (2,250 images, 1,550 videos from 50 subjects) explicitly targeting eKYC video-verification workflows, with strong demographic balance (50:50 gender, ~25% per racial group, ages 18–69) and rigorous ethical compliance (GDPR, informed consent, controlled-access licensing). The acquisition protocol spans five sessions across three consumer smartphones with varied lighting and occlusion conditions.

## Strengths
- **Targeted eKYC scenario design (Scenarios 12–18, §3.2):** The seven verification video actions (circular head rotation, tilting, blinking, expression change, mouth opening, face occlusion, face touching) are directly motivated by real eKYC procedures, not generic "person in front of camera" clips. This addresses a genuine gap — no existing public dataset targets this workflow.
- **Demographic balance across multiple axes (§3.1, Figure 1):** 50:50 gender split (25M, 25F), near-equal representation across four racial categories (26% African, 26% Caucasian, 24% East Asian, 24% South Asian), and age range 18–69 across three bands. The explicit metadata schema (Table 1 columns DD/GB/RB/AB) makes this compositional choice transparent and actionable.
- **Exemplary ethical and legal compliance (§3.4):** GDPR alignment, informed consent from all subjects, controlled-access licensing, and anonymization via randomized identifiers. Given the withdrawal of MS-Celeb-1M, VGGFace2, and MegaFace over consent issues, this is a meaningful differentiator.
- **Multi-device, multi-session acquisition protocol (§3.3, Table 2):** Five sessions (artificial light, flash, glasses, natural daylight, weak natural light) across three consumer smartphones (Xiaomi Redmi Note 13, iPhone 13, Samsung Galaxy A35). The zero-lens glasses session for non-wearers is a thoughtful design choice that controls for a confound often overlooked.

## Weaknesses

### Major
- **Non-standard verification metrics limit interpretability (§4.2, Table 4):** Performance is reported as frame-level accuracy with a fixed threshold of 0.5 applied uniformly to both ArcFace and MagFace. Standard practice in face verification is to report TAR@FAR (e.g., 1e-3, 1e-4), EER, or AUC — metrics that decouple discrimination from calibration and support comparison across models. Frame-level accuracy weights every frame equally (inflating easy frontal frames and obscuring hard profile views) rather than modeling per-video decisions, making the numbers in Table 4 difficult to interpret for real eKYC deployment.
- **Benchmark evaluation does not demonstrate the dataset's unique value (§4, Tables 3–4):** No experiment compares performance *with vs. without* eKYC-specific scenarios, no cross-dataset transfer analysis (train on MOBIO/SOTERIA, test on VIBEFACE, or vice versa), and no quantitative comparison with analogous scenarios from existing datasets to show distribution shift. The central claim — that existing datasets miss what VIBEFACE captures — is asserted without evidential support from the benchmarks.
- **Verification protocol introduces a systematic confound (§4.2, line 336):** A single flash-illuminated frontal image (Session B, Scenario 3) is used as the reference for all queries, which come from sessions with different lighting (artificial, natural, weak natural). This conflates illumination robustness with identity verification performance. The flash session also uses only the rear camera (standardized photos, no videos or selfies), limiting its modality overlap with other sessions.
- **Small subject pool (n=50) weakens demographic fairness framing (§3.1, Tables 3–4):** With ~12–13 subjects per racial group, subgroup-level differences reported in Tables 3–4 fall within the noise floor, and no confidence intervals or significance tests are provided. While the dataset's proportional balance is commendable, the absolute numbers do not support the framing of fairness evaluation as a core contribution.

### Minor
- Fitzpatrick skin type distribution is claimed (line 139: "reflect the whole spectrum of Fitzpatrick's scale") but never reported alongside the racial categories.
- No dedicated limitations section — the paper does not discuss its most obvious constraints (small sample size, controlled-studio setting versus fully in-the-wild eKYC conditions).
- Results in Tables 3 and 4 are reported only as point estimates without standard deviations, making per-demographic-group comparisons difficult to assess statistically.

### Trivial
None.

## Nice-to-Haves
- Adding a cross-dataset experiment (train on existing video datasets, test on VIBEFACE) would substantially strengthen the novelty claim.
- Replacing frame-level accuracy with per-video TAR@FAR and EER would make the results actionable for practitioners.
- Reporting the actual Fitzpatrick-type distribution (even with n=50) would substantiate the claim about skin tone coverage.

## Removed Points
These points from the input review were removed or demoted with justification:
- "Abstract/Introduction ordering is generic" → removed as a presentation nitpick (per formatting/style rule).
- "eKYC novelty overclaimed" → partially addressed: the paper defines eKYC scenarios explicitly in §3.2 but does not compare against existing datasets' content; remaining concern is now subsumed under Major weakness #2 (benchmark does not demonstrate value).
- "No cross-dataset image quality comparison" → removed as a nice-to-have beyond standard dataset paper scope.
- "PAD/deepfake applications unsupported" → conclusions clearly label these as future directions; removed as scope creep.
- "Missing related works" → removed per rule (cannot confirm existence of unreviewed works).

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Fix the verification evaluation protocol:** Replace frame-level accuracy with TAR@FAR (1e-2, 1e-3), EER, and AUC. Use per-video decision aggregation. Select model-specific thresholds or report ROC curves.
2. **Demonstrate why eKYC scenarios matter:** Add at least one experiment comparing eKYC-specific videos against matched generic videos, or a cross-dataset transfer evaluation.
3. **Report Fitzpatrick skin type distribution** to substantiate the claim about full-spectrum coverage.
4. **Add a limitations section** explicitly discussing the n=50 sample size and the controlled-studio setting.
5. **Include confidence intervals or standard deviations** in all per-demographic-subgroup results.

## Score and Decision

**Calibration anchors used across rounds:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| MDPE | EqCbc4wrzy.md | 2.50 (Reject) | R1 | Yes | Multimodal deception dataset with 193 subjects; evaluation weaknesses more severe than VIBEFACE's. VIBEFACE has stronger dataset design and ethical compliance. |
| HiDF | XhyCPEnlCa.md | 4.25 (Reject) | R1, R2 | Yes | Deepfake dataset (30K images, 4K videos). Similar weakness profile (evaluation too weak at -1.84 favorability vs VIBEFACE's -1.59). VIBEFACE has stronger demographic balance and ethics but smaller scale. |
| EyeFairness | Lv9KZ5qCSG.md | 5.50 (Reject) | R2 | Yes | Large-scale (30K subjects) medical fairness dataset. More severe single weakness (-2.21 favorability) from unfair baseline comparison, but overall stronger due to scale and method contribution. VIBEFACE below this. |
| UDC-VIT | DNBwlQYA90.md | 6.00 (Reject) | R1 | Yes | Real-world UDC video dataset with cross-dataset validation. VIBEFACE lacks this type of evidence, placing it below UDC-VIT. |
| Vec2Face | RoN6NnHjn4.md | 6.00 (Accept) | R1 | Yes | Synthetic face generation with strong method contribution and large-scale experiments. A substantially different paper class; not directly comparable. |
| Skin Tone PAD | dEGYODD6iU.md | 3.67 (Reject) | R2 | Yes | Mobile PAD fairness paper. Limited SOTA comparison and incremental contribution. VIBEFACE's dataset contribution is stronger. |

**Comparison-driven placement:** VIBEFACE's most damaging weakness (frame-level accuracy, favorability -1.59) is similar in severity to HiDF's worst (-1.84 for "evaluation too weak"), and its strengths (ethical compliance up to 11.61 favorability) are genuinely high. However, VIBEFACE has four negatively-rated items pulling the score down, while HiDF's negatives are fewer. VIBEFACE is stronger than MDPE (2.50) and the Skin Tone PAD paper (3.67), comparable to HiDF (4.25), and weaker than EyeFairness (5.50) which has both larger scale and a method contribution. The paper's core dataset contribution is real, but the evaluation methodology does not provide adequate evidence for the central novelty claim, and the non-standard metrics undermine the benchmark's informativeness.

**Final score: 4.0** — borderline reject. The dataset has genuine value (particularly the eKYC scenario design and ethical provenance), but the evaluation methodology and lack of demonstrated evidence for the eKYC gap are too significant in the current form. A substantively revised version addressing the verification protocol and adding cross-dataset evidence could move this to accept territory.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>