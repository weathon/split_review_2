## Summary
# Final Review Report

## Summary

This paper proposes **Continuous Online Action Detection (COAD)**, a task formulation that extends standard Online Action Detection (OAD) by enabling models to adapt incrementally from streaming egocentric video using single-pass training, without storing past data. The authors also introduce **Ego-OAD**, a large-scale egocentric OAD benchmark with 87 action classes and 22,991 instances derived from the Ego4D Moment Queries split, and develop three training strategies — state continuity, orthogonal gradient projection, and non-uniform loss — to balance in-stream adaptation with out-of-stream generalization. Experiments on Ego-OAD show Top-5 Recall improvements of up to 16% on in-stream data and 6.9% on out-of-stream data over a pretrained-only baseline, while EPIC-KITCHENS results are mixed.

**Core contributions:**

- **C1 (Task Formulation):** COAD unifies online inference and online training under strict causal, single-pass constraints — a timely problem for on-device egocentric AI.
- **C2 (Ego-OAD Benchmark):** A diverse multi-label egocentric OAD dataset with realistic label ambiguity, filling a gap in OAD evaluation resources.
- **C3 (Training Strategies):** Adaptation of orthogonal gradient projection and non-uniform loss to the OAD setting, with systematic ablation analysis.

**Key strengths:** The problem motivation is compelling, the dataset addresses a genuine need, and the ablation study is thorough. **Key weaknesses:** (1) The evaluation design conflates continuous adaptation gains with simply having more training data, since the pretraining set is only ~14% the size of the in-stream set; (2) EPIC-KITCHENS results show tangible regressions that are explained away without sufficient analysis; (3) Several methodological details (gradient definition, numerical stability of orthogonal projection, full pretraining requirements) are underspecified; (4) The conclusion omits any limitations discussion. Novelty verification is deferred due to unavailable literature search in this run.

**Score: 6/10** — A well-motivated incremental contribution with good empirical breadth but with unresolved evaluation confounds and scope overclaim issues that need remediation. With proper controls, clearer failure analysis, and bounded claims, the paper could be a solid contribution to the egocentric vision and online learning communities.

## Strengths
1. **Well-motivated problem formulation.** The paper identifies a genuine gap in OAD research — most models are trained offline and cannot adapt after deployment — and proposes COAD as a principled extension. The alignment of training-time and inference-time constraints (causal, single-pass, no replay) is a clean formulation that reflects real-world deployment on wearable devices.

2. **Useful benchmark contribution (Ego-OAD).** Deriving an OAD benchmark from Ego4D MQ with 87 classes, 22,991 instances, and 263 hours of video fills a concrete gap in egocentric OAD evaluation. The multi-label annotation strategy capturing annotator disagreement is a realistic design choice, and the public release (implied) would benefit the community.

3. **Thorough ablation study.** Table 3 provides a systematic decomposition of COAD's components (state continuity, orthogonal gradient, non-uniform loss), with in-stream and out-of-stream metrics for each combination. This is above-average empirical rigor and allows readers to assess the marginal contribution of each component.

4. **Honest accounting of label noise in dataset curation.** Section 3 explicitly discusses the tension between merging annotation passes (richer coverage) and amplifying label ambiguity. The 36% overlap statistic is informative and helps calibrate the difficulty of the benchmark.

5. **Transparent trade-off analysis.** Figure 3 maps the in-stream vs. out-of-stream performance trade-off across stride and learning rate settings, which is directly useful for practitioners deploying COAD in resource-constrained scenarios. The observation that at stride 128 the model still learns effectively with labels approximately every 68 seconds is a practically valuable insight.

6. **Dual-dataset evaluation.** Testing on both Ego-OAD (diverse scenarios) and EPIC-KITCHENS (specialized cooking actions) provides a reasonable breadth check, even though the EPIC-KITCHENS results are mixed.

## Weaknesses
### W1 (Major) — Evaluation design conflates data quantity with adaptation effectiveness

The paper adopts the three-split protocol from Carreira et al. (2024a), but the split sizes are highly imbalanced: Ego-OAD uses only 186 videos for pretraining vs. 1,177 for in-stream training (a 6.3× disparity). The "Pretrained Only" baseline is therefore severely undertrained, meaning the large gains reported for COAD (and even for w/o COAD) reflect not only the continuous adaptation mechanism but also the effect of simply training on more data. The w/o COAD baseline partially controls for this, but without an "IID in-stream" baseline (shuffled offline training on the same in-stream data with multiple epochs), readers cannot distinguish the benefit of continuous adaptation from the benefit of increased training data. This directly affects the headline claims of "up to 20% improvement."

**Required fix:** Add an IID in-stream baseline (standard offline training on the combined pretraining + in-stream sets with multiple passes) to isolate the cost of the single-pass constraint. Report the gap between COAD and this IID baseline as the true measure of continuous learning efficiency.

### W2 (Major) — EPIC-KITCHENS regression dismissed without rigorous analysis

On EPIC-KITCHENS, COAD underperforms the pretrained-only baseline on Action mAP (in-stream) and shows marginal gains on Verb/Noun metrics. The paper attributes this to "the fine-grained nature of the actions and annotations" — an untested post-hoc hypothesis. No per-class analysis, confusion matrices, annotation granularity statistics, or ablation of label frequency effects are provided to support this claim. This is a significant omission because EPIC-KITCHENS is one of only two evaluation datasets; a failure case on a key benchmark should be a first-class finding, not a footnote.

**Required fix:** (a) Add per-class performance breakdown on EPIC-KITCHENS and examine the relationship between class frequency/granularity and COAD's relative gain/loss. (b) Report results across at least 3 random seeds with variance. (c) If the fine-grained hypothesis is correct, provide concrete evidence (e.g., confusion matrices showing systematic misclassification between fine-grained verb classes). (d) Bound the method's claims in the abstract and conclusion to acknowledge this limitation.

### W3 (Moderate) — Under-specified methodological details

Several technical aspects of COAD are insufficiently specified for reproducibility or scientific scrutiny:

a) **Gradient definition (Eq. 5):** The paper uses gradient $g_t$ without specifying which loss it is taken with respect to, or which parameters it covers. Since the backbone $\Phi$ is frozen, only the detection head parameters are updated — but this is never stated explicitly. 
b) **Numerical stability of orthogonal projection:** The denominator $\|g_{t-1}\|^2$ can approach zero when gradients vanish, yet no epsilon regularization or gradient clipping is mentioned.
c) **Single-step decorrelation justification:** The orthogonal projection targets only $g_{t-1}$, but accumulated drift over many windows could still bias optimization. The paper does not justify why single-step decorrelation is sufficient or compare against multi-step variants.
d) **Hyperparameter sensitivity:** Only one learning rate (2e-5) and window stride (16) are used for the main results. While Figure 3 varies these, the core results in Table 1 use a single configuration, leaving uncertainty about sensitivity.

**Required fix:** Add explicit gradient definitions, epsilon stabilization, and a brief hyperparameter sensitivity table in the appendix.

### W4 (Moderate) — Unquantified label noise in Ego-OAD benchmark

Section 3 honestly acknowledges label ambiguity from merging multiple annotation passes and the subsequent manual grouping procedure. However, the impact of this noise is not quantified. Without knowing the inter-annotator agreement after grouping, or the label noise floor, readers cannot determine whether improvements of a few mAP points are meaningful. The benchmark's utility for future research depends on this calibration.

**Required fix:** Report inter-annotator agreement (before and after manual grouping), the number of raw free-form descriptions reduced to 87 classes, and an empirical noise-floor estimate (e.g., human performance on a held-out subset or the agreement ceiling).

### W5 (Moderate) — Unfair backbone comparison in Feature Extractors (Table 4)

The comparison between TSN (frame-based) and TimeSformer (clip-based) is confounded by unequal pretraining. TimeSformer uses EgoVLP (large-scale external egocentric pretraining), while TSN's egocentric variant is pretrained on Ego-OAD itself (only 186 pretraining videos). The 10.5 mAP gap may largely reflect data scale and quality rather than architectural superiority.

**Required fix:** Add a controlled comparison where both backbones are pretrained on identical data (or acknowledge the confound explicitly in the text).

### W6 (Minor) — Conclusion lacks limitations discussion

The 4-sentence conclusion recites contributions without acknowledging any limitations, failure modes, or future directions. Given the EPIC-KITCHENS regression and the evaluation confound (W1), this omission reduces scientific credibility. Including a brief limitations paragraph is now standard practice at top venues.

**Required fix:** Append a 2-3 sentence limitations paragraph covering the EPIC-KITCHENS generalization gap, the reliance on offline-pretrained backbones, and the single-stream evaluation scope.

### W7 (Minor) — Typographical and acronym issues

- **"Countinuous"** in the contribution list (line 15) should be **"Continuous"**.
- **"CODA"** (line 36, Section 4) conflicts with the paper's chosen acronym **"COAD"** used everywhere else.
- Line 28 contains a stray closing parenthesis: "online action detection)".
- Line 36 says "enable the model to continuous video streams" — missing verb ("adapt to").

### Novelty & Comparison (Deferred)

Due to unavailable literature search infrastructure in this review run, external novelty verification and related-work comparison are deferred. The following claims require manual verification by the authors or an additional reviewer with literature access:
- Claim C1 (COAD as a new task formulation): Whether prior OAD methods with online fine-tuning (e.g., test-time adaptation approaches) already cover this setting.
- Claim C3 (orthogonal gradient projection for OAD): Whether Han et al. (2025) already introduced this technique for continuous video learning and how much adaptation is needed for the OAD setting.
- Whether existing egocentric OAD datasets (e.g., EPIC-KITCHENS-based OAD splits) already provide similar evaluation platforms.

**Recommendation for authors:** Please clearly differentiate from the closest works on test-time adaptation for video action recognition and on-device continual learning, and cite the most related baselines with a discussion of residual differences.

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a timely and well-motivated problem (online adaptation for egocentric OAD), contributes a useful benchmark (Ego-OAD), and presents a clean ablation study. However, two major weaknesses prevent a higher score: (1) the evaluation design conflates continuous adaptation gains with increased training data quantity, undermining the headline performance claims, and (2) the EPIC-KITCHENS regression is dismissed without rigorous analysis. Additionally, several methodological details are underspecified, and novelty cannot be verified without literature access in this run. The contributions are incremental (adapting existing techniques — orthogonal gradient projection from Han et al. (2025) and non-uniform loss from An et al. (2023) — to the OAD setting) rather than fundamentally new. With proper controls, bounded claims, and a candid limitations discussion, the paper could reach 7-8/10 in a revised submission.

**Scoring breakdown:**
- **Research value & novelty (primary dimension):** 5/10 — Well-motivated but incremental technique adaptation; novelty deferral required.
- **Validity & soundness:** 6/10 — Careful ablation but evaluation confound (W1) and unexplained regression (W2) reduce confidence.
- **Reproducibility:** 6/10 — Reasonable implementation details but missing gradient definitions and numerical stability specifications (W3).
- **Presentation & clarity:** 7/10 — Generally well-written, some typos, conclusion lacks limitations.

**External literature verification status:** Novelty/comparison conclusions are deferred due to unavailable literature search infrastructure in this run. The authors should verify that COAD is not already covered by prior test-time adaptation or continual learning methods for video action recognition.