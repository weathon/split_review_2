Now let me compose the final review based on the draft and impact scores.

## Summary

This paper introduces Visuo-Tactile World Models (VT-WM), the first multi-task world model that integrates fingertip tactile sensing (Digit 360) with exocentric vision for contact-rich robot manipulation. The model uses frozen pretrained encoders (Cosmos for vision, Sparsh-X for touch) with a factorized spatio-temporal transformer predictor trained via a combination of teacher forcing and autoregressive sampling. The paper evaluates VT-WM against a vision-only baseline (V-WM) on imagination quality (object permanence, causal compliance), zero-shot planning on a real robot, and data efficiency for a new task.

## Strengths

- **Well-motivated direction.** The paper correctly identifies that vision-only world models hallucinate contact interactions (objects disappearing, teleporting, moving without forces) because exocentric cameras cannot observe forces, grasp states, or contact onset. Integrating tactile sensing is a genuine and timely contribution to grounding these interactions. (Sections 1, 3.1)

- **Real-robot evaluation.** Testing zero-shot planned trajectories on a physical robot across tasks with varying contact complexity (reaching, pushing, wiping, stacking) gives the evaluation more credibility than simulation-only or pixel-metric-only studies. The tasks span a reasonable range of contact complexity. (Sections 4.2–4.3)

- **Sound architecture design.** The factorized spatio-temporal self-attention with action cross-attention is a reasonable design for the multimodal setting. Using frozen pretrained encoders (Cosmos for vision, Sparsh-X for touch) is pragmatic and follows what the community is converging toward. The training objective combining teacher forcing with autoregressive sampling is sensible for balancing stability and long-horizon coherence. (Section 3.2.1)

## Weaknesses

### Fatal
None.

### Major

**1. Data efficiency experiment conflates multi-task pre-training with tactile grounding (Section 4.3).** VT-WM is fine-tuned from a multi-task model trained on many prior demonstrations, while the BC policy (ACT) is trained from scratch on just 20 demonstrations. The 3.5× improvement could be entirely due to multi-task pre-training rather than to tactile sensing — the BC policy simply starts with far less data. Critically, the BC policy also receives tactile inputs (line 245: "receives the latest RGB and tactile inputs"), so the comparison is not even isolating tactile grounding. The paper's abstract and conclusion frame this as "VT-WM shows data efficiency" and "its ability to efficiently adapt to new tasks with limited data," implying VT-WM-specific advantages, but the experiment cannot attribute the gains to the tactile modality. A valid comparison would require either pre-training the BC policy on the same multi-task data and then fine-tuning, or training VT-WM from scratch on the 20 demos.

**2. Planning comparison is structurally confounded (Section 4.2, lines 235–239).** The paper states: "To initialize planning consistently, the initial RGB and tactile embeddings are passed as context to the world model." Both VT-WM and V-WM are then tested. However, V-WM is described throughout as a vision-only model; it cannot accept tactile embeddings. Therefore, V-WM's planner is initialized with strictly less information about the current contact state than VT-WM's planner. When VT-WM shows higher task success (up to 35% improvement), this confound alone could explain the gap: the V-WM may plan correctly but from an impoverished initial condition. The paper frames planning gains as evidence that "improvements in imagination enable more reliable zero-shot planning" (Abstract), but the experiment does not isolate improved imagination from improved conditioning. The paper also never specifies how the V-WM baseline is architecturally constructed (e.g., same transformer with tactile tokens removed, or a separate smaller model), leaving the reader unable to assess whether capacity differences contribute.

**3. Very small sample sizes with reporting ambiguity for real-robot planning (Section 4.2).** Success rates are reported as "averaged over five trials per task" (line 239), but the percentages (69%, 75%, 83%, 92%, 93%) are not multiples of 20% (1/5). This suggests either misreporting or unexplained cross-seed/condition aggregation. No confidence intervals or significance tests are reported for planning results, in contrast to the imagination evaluation where t-tests are provided. With n=5 per task and binary outcomes, the detectable effect size is very large, and most of the reported gains could be within the noise of random seed variation.

### Minor

**4. Latent-to-pixel mapping for CoTracker evaluation is underspecified (Section 4.1, lines 144–146).** CoTracker operates on RGB video frames to track keypoints, but the model predicts future latents (s_{k+1}, t_{k+1}), not pixels. The paper mentions the Cosmos encoder but never mentions using its decoder to map latents back to pixels. If the latents are decoded, the decoder's reconstruction quality interacts with CoTracker results; if not, the procedure is unreproducible. This gap in description should be clarified.

**5. Scribble task degradation unexplained (Section 4.1, Figure 6).** For causal compliance, VT-WM achieves a *worse* normalized Fréchet distance than V-WM on the scribble task (0.50 vs. 0.35, t=−1.22, p=0.23). The paper notes this in passing but offers no explanation. This is the only task where touch hurts; understanding why is important for assessing boundary conditions of tactile grounding.

**6. What constitutes an observation in the paired t-tests is unspecified (Section 4.1).** It is unclear whether individual rollout frames, entire trajectories, or something else comprise a single observation. The degrees of freedom implied by the t-values suggest trajectory-level comparisons, but this should be explicit for reproducibility.

### Trivial
None.

## Nice-to-Haves
- Discuss failure modes of VT-WM qualitatively (the paper describes V-WM failures but not what VT-WM gets wrong, e.g., the 17% failures on cube stacking).
- Clarify whether the 3–5 step sampling horizon during training limits planning quality over longer horizons.

## Removed Points
These points were flagged for removal. Treat them with caution:
- Criticism about "number of training demos deferred to appendix" — removed per rule: missing appendix content is a parser artifact, not a paper flaw.
- Criticism about CEM using L2 distance in visual latent space only — the paper explicitly acknowledges this (line 125), so it is not a missed issue.
- Pure formatting/style nitpicks — removed per hard rules.

## Novel Insights
The key structural insight that emerges from the review is that the zero-shot planning comparison contains a confound that the paper does not address: because V-WM is vision-only, it cannot receive tactile context during planning initialization. This means the planning results cannot cleanly separate the value of tactile information *in the learned dynamics* (from training) from the value of tactile information *in the conditioning input* (at inference time). This is a subtle experimental design issue that prevents the planning experiments from supporting the paper's core thesis as cleanly as claimed. The data efficiency comparison suffers from a different confound (multi-task pre-training vs. from-scratch BC), and the fact that BC also receives tactile inputs makes the "tactile grounding" attribution even less supportable.

## Suggestions
- Fix the planning comparison by giving V-WM equivalent access to contact-state information during planning initialization (e.g., a binary contact flag or a learned embedding from a separate contact classifier), isolating the role of tactile information in the learned dynamics from conditioning differences.
- For data efficiency, compare VT-WM and V-WM both fine-tuned from the same multi-task checkpoint, or train VT-WM from scratch on 20 demos, to isolate the contribution of the tactile modality.
- Report exact trial counts, confidence intervals, and the aggregation procedure for planning results. Explain the non-integer percentages.
- Clarify the latent-to-pixel decoding pipeline used for CoTracker evaluation.
- Discuss why the scribble task degrades with tactile input, as this may reveal important boundary conditions.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>