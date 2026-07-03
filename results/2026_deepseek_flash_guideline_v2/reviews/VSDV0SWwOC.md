Now I have all the information I need. Let me compile the final consolidated review.

**Note on calibration:** The calibration_search tool failed due to missing underlying file paths in the corpus. I proceeded with manual calibration against my knowledge of ICLR standards.

---

## Summary

LS-Merge proposes a novel framework that shifts LLM model merging from weight space to a learned latent space. The approach uses a transformer-based VAE to encode model parameters, performs merging operations (interpolation, soup, OT alignment) in the latent space, and decodes back to weights. It aims to support both homogeneous merges (same architecture) and heterogeneous merges (cross-architecture, cross-family). The paper's key contributions are a distributional analysis of LLM weights motivating encoder design, a two-stage curriculum for training weight-space VAEs, OT-based alignment for heterogeneous merging, and experiments showing latent-space merging can outperform weight-space baselines.

## Strengths

- **PCA vs. VAE comparison (Table 8, Section 5.3) is the paper's strongest evidence.** PCA-reconstructed weights collapse to near-random MMLU accuracy (~25.5%) even at the mildest compression ratio of 1.6×, while the VAE preserves ~96% of the original model's performance and remains stable at 4× compression. This cleanly demonstrates that the pretrained-weight manifold is non-linear and that non-linear encoders are a geometric necessity — a result that stands independently of the merging application.

- **Distributional characterization of LLM weights (Table 1, Section 3.1) grounds the architecture choices.** The paper reports excess kurtosis of 5–15 across early layers, directly contradicting Gaussian assumptions made in prior weight-space learning work (Si et al., 2025). This observation is explicitly tied to the two-stage training curriculum and provides a concrete rationale for design decisions that are often made heuristically.

- **Strong expert-merging results (Table 3).** LS-Merge(soup) achieves the best score on 6 of 8 benchmarks (MMLU 56.0, HellaSwag 60.1, NLQGraph 56.1) against competitive weight-space baselines including SLERP, Greedy Soup, and Dare-Ties. LS-Merge(lerp) wins on 3 of 8. The consistent improvement suggests latent-space composition adds genuine value beyond weight-space operations.

- **Honest characterization of VAE generalization limits (Table 7, Section 5.2).** The paper trains a VAE on Gemma-3-4B-it and tests zero-shot on unseen models at three compression ratios. At r=1.6 generalization is strong (MMLU drops ~0.8 points for Gemma-1B); at r=4 it degrades substantially (~25 MMLU). Rather than selectively reporting only the favorable low-compression result, the paper surfaces this trade-off transparently and acknowledges mode collapse as a limitation (Section 6).

## Weaknesses

### Major

- **Heterogeneous merging — the paper's most differentiating claim — rests on thin evidence.** The intra-family result (Gemma-3-4B → Gemma-3-1B) is shown only in a bar chart (Figure 4a) with no numerical table and no standard errors. The cross-family result (Table 5) covers only three datasets (WinoGrande, ARC-C, HellaSwag) with modest margins (e.g., HellaSwag: 49.07 base → 50.10 merged). The "OT only" condition substantially degrades performance (WinoGrande: 56.83→51.13), indicating the alignment introduces geometric distortion that interpolation only partially masks. The paper characterizes heterogeneous merging as overcoming "a fundamental limitation of prior weight-space techniques," but the experimental support is too narrow and too fragile to sustain this strength of claim.

- **Compression ratio is not consistently reported across experiments.** Section 4.1 explicitly states r=2 for self-merging, but the compression ratios used in Tables 3 (expert merging), 4 (representation-method comparison), and 5 (cross-family) are not stated. Since Table 7 shows that VAE reconstruction quality degrades substantially at r=2 (e.g., MMLU drops from ~40 to ~32 for Gemma-3-1B) and at r=4 (to ~25), readers cannot assess whether the reported merging improvements are relative to a faithful encoding or a significantly degraded baseline. This is critical information for interpreting the magnitude of the results.

### Minor

- **Inconsistent variance reporting across experiments.** Tables 2 and 8 report standard deviations; Tables 3, 4, 5, 6, and 7 do not. Since many improvements are modest (1–3 points), the absence of variance estimates makes it difficult to distinguish signal from noise. For example, in Table 4 LS-Merge and AIM are within 1–2 points on most benchmarks — without error bars it is unclear if these differences are meaningful.

- **Self-merging improvement conflates two effects.** The self-merging experiment (Table 2) compares LS-Merge (multiple latent samples averaged in latent space) against "VAE" (single latent sample). The gain could partly reflect noise reduction from averaging multiple stochastic decodings rather than a genuine benefit of latent-space composition. An additional control — averaging multiple VAE decodings in weight space — would clarify whether the latent-space operation provides specific value beyond ensembling. This does not invalidate the result but weakens the mechanistic interpretation.

- **No ablation of the two-stage curriculum.** The paper motivates the two-stage training (deterministic AE first, then KL) as critical for handling heavy-tailed weights, but no experiment demonstrates that standard VAE training (KL from the start) collapses while the curriculum avoids it. Without this, the connection between the weight-statistics analysis and the design choice, while plausible, remains circumstantial.

### Trivial

None.

## Nice-to-Haves

- Report computational cost (GPU-hours) of VAE training and the inference overhead of decoding the merged model. The paper claims "scalable" and "efficient" but provides no runtime numbers.
- Add an analysis of what structural information is lost when 2D weight matrices are flattened into 1D sequences, which is a strong preprocessing choice that could discard spatial structure.

## Removed Points

These points appeared in reviewer inputs but are removed with justification:

1. **"Paper's Gaussian prior contradicts non-Gaussian weight claim"** — Removed. This confuses the weight-space distribution (heavy-tailed, Section 3.1) with the latent-space prior (Gaussian). The VAE's prior operates on latents, not weights. The two-stage curriculum explicitly addresses the weight-space statistics.

2. **"Data Merge footnote missing"** — Removed as a parser artifact (appendix stripped by PDF extraction; the footnote exists in the original submission).

3. **"Evaluation frameworks vary between sections"** — Removed because the paper explicitly explains this choice ("Contrarily to the previous experiments, in this setting we use lm-eval tool for fair comparison with the baselines").

4. **"OT Gaussian approximation is a convenience assumption"** — Removed because the paper clearly states this is an approximation and provides the closed-form solution under standard assumptions. This is accepted practice.

5. **"No heterogeneous baseline exists"** — Removed because comparing to the base model is a valid (and necessary) lower bound for a new capability. The paper cannot be faulted for lacking baselines that no prior work provides.

6. **Generic formatting/style complaints** — Removed per instructions.

## Novel Insights

The most interesting observation emerging from the cross-review synthesis is that the VAE reconstruction occasionally improves over the base model (e.g., Gemma-3-4B-it MMLU: 53.10 base → 54.10 VAE; Gemma-3-1B-it MMLU: 32.20 base → 32.60 VAE). This suggests the VAE may act as a denoiser on learned weights, potentially regularizing away idiosyncratic noise from pretraining. Neither the paper nor the reviewers discuss this phenomenon, but it is a potentially significant finding for weight-space learning that merits investigation: if latent-space encoding can consistently improve over the original weights, the VAE is not merely a compression tool but a performance-enhancing component.

## Suggestions

1. **Report the compression ratio in every experimental table** (Tables 3, 4, 5). Without this, it is impossible to assess whether results are computed at a favorable or unfavorable operating point.

2. **Provide numerical results with error bars for intra-family heterogeneous merging** (Figure 4a), replacing or supplementing the bar chart with a table.

3. **Add a control experiment for self-merging**: compare (a) single VAE reconstruction, (b) average of multiple VAE reconstructions in weight space, and (c) latent averaging of multiple samples (LS-Merge). If (c) > (b), the latent space provides non-trivial composition value beyond noise reduction.

4. **Add an ablation showing the necessity of the two-stage curriculum**, e.g., training a VAE with KL divergence enabled from the start and demonstrating collapse or degraded performance.

5. **Provide standard deviations or confidence intervals across all main-result tables** to help readers assess the significance of reported improvements.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>