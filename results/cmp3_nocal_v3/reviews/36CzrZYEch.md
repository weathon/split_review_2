Now I have sufficient understanding of the paper. Let me write the final consolidated review.

---

## Summary

IRIS proposes using Negative Self-Certainty (NSC = -KL(U || π_θ)) as an intrinsic reward signal to fine-tune autoregressive text-to-image models via GRPO, requiring no external reward models, human annotations, or domain-specific verifiers. The key empirical finding is that minimizing self-certainty (unlike in text-domain reasoning where maximizing it helps) improves image generation. On Janus-Pro 1B/7B, IRIS achieves results within ~1–4% of the external-reward-based method T2I-R1 on GenEval, T2I-CompBench, and WISE — a concrete demonstration that intrinsic signals can substitute for external supervision in T2I alignment.

## Strengths

1. **A genuinely non-obvious and well-supported empirical finding.** The observation that minimizing self-certainty helps T2I generation while maximizing it helps text-domain reasoning (Zhao et al., 2025b) is interesting. Figure 2 — showing that externally-rewarded training drives text self-certainty up but image self-certainty down — provides compelling motivation for the paper's central direction. The ablations in Sec. 4.3 (Figs. 6–7) independently confirm this: maximizing image self-certainty degrades performance while minimizing it improves it, and the same holds for text tokens in the T2I setting.

2. **Clean, minimal method.** The reward signal is simply NSC = -KL(U || π_θ) applied to all tokens. No external models, no human labels, no task-specific engineering. Given how complex T2I alignment pipelines have become (external reward models, detector-based verification, VQA-based scoring), this simplicity is a genuine virtue and makes the method widely applicable.

3. **Comprehensive ablation study (Sec. 4.3).** The ablations separately test the role of text vs. image token uncertainty (Figs. 6 & 7), forward vs. backward KL (Fig. 8), semantic CoTs (Fig. 5), and direct optimization vs. RL (Fig. 9). Each ablation isolates a clear question and answers it decisively. Figure 9 alone (showing that direct NSC optimization collapses whereas GRPO works) is a useful methodological finding.

4. **Reproducibility-aware baseline correction.** The identification of the chat-template bug in T2I-R1's official implementation (line 120) is a useful service to the community, even though it makes direct comparison with previously published numbers impossible.

## Weaknesses

### Fatal

None.

### Major

None. The paper's core claim — that an intrinsic reward (NSC) can produce competitive T2I results without external supervision — is supported by the evidence.

### Minor

1. **Human-preferences framing without human evaluation.** The abstract and introduction describe the observed improvement as producing images "better aligned with human preferences" and "more preferred by humans" (Fig. 1 caption, line 27), but the paper provides no human evaluation. All evidence comes from automated benchmarks (GenEval, T2I-CompBench, WISE) and, in the ablations, from the same external reward models (HPSv2, DINO, GIT, ORM) that the paper is arguing against using for training. The paper's listed contributions (lines 48–50) do *not* include a human-preference claim, so this is a framing mismatch rather than an invalidated contribution — the paper would benefit from either adding a small human study or tempering the "human preferences" language to match what is actually measured (benchmark performance).

2. **Figure 2 confounds model architecture and task.** The comparison plots self-certainty during training for Qwen2.5-1.5B-Instruct on math reasoning (text tokens) versus Janus-Pro-1B on T2I (image tokens). This varies two factors at once (model + task), so the diverging trajectories could reflect architectural properties or token-type differences (VQVAE codes vs. natural-language tokens) rather than a modality-specific property of T2I. The paper would benefit from tracking self-certainty on both text and image tokens within the same multimodal model trained on a single task.

3. **"Competitive with or superior to" slightly overstates the comparison.** In Table 1, IRIS consistently scores slightly *below* T2I-R1 on overall benchmarks (GenEval 1B: 0.72 vs. 0.75; 7B: 0.77 vs. 0.78; WISE 1B: 0.37 vs. 0.38; 7B: 0.48 vs. 0.50). The picture on T2I-CompBench is more mixed (IRIS wins on Color, Texture, and Non-Spatial for 1B), and Fig. 3 shows IRIS exceeding T2I-R1 during training. The paper's specificity about improvements (9.1%, 13.3%, 28.8%) is correctly attributed to gains *over the base model*, not T2I-R1, and "competitive" is fair. But "superior to external rewards" (abstract) overstates the aggregate evidence from Table 1.

4. **Mechanism is underspecified.** The paper explains *that* minimizing self-certainty helps but not *why*. The observed improvement could reflect (a) diverse token sampling enabling better exploration during RL, (b) reduced mode collapse, or (c) added stochasticity that makes images look more visually complex without improving semantic alignment. The ablations confirm the effect but do not distinguish these mechanisms. A simple experiment tracking per-token entropy changes over training, or analyzing whether NSC-trained models generate more diverse outputs for the same prompt, would help.

### Trivial

None.

## Nice-to-Haves

- A small-scale human evaluation study (e.g., 200 head-to-head comparisons between IRIS and the base model, and IRIS vs. T2I-R1) would directly address the framing weakness and strengthen the paper considerably.
- A controlled version of Figure 2 (tracking self-certainty on both text and image tokens in the same model on the same task) would cleanly separate the modality explanation from architecture confounds.
- A qualitative failure-case analysis would increase trust — do NSC-trained models hallucinate objects or generate incoherent scenes that nevertheless score well on automated metrics?
- Generalization to at least one other autoregressive T2I architecture (e.g., Show-o, SEED-X) would broaden the paper's impact; the paper acknowledges this limitation (Sec. 4.4) but provides no evidence of transfer.

## Removed Points

These points from the input review were removed with justification:

- **"Issue 1 (Evidential): No human evaluation, despite the central claim being about human preferences" — moved from "fatal/critical" to Minor.** The paper's listed contributions (lines 48–50) do not include a human-preference claim; the "human preferences" language in the abstract and intro is framing/motivation, not the paper's central claim. The core contribution is about intrinsic-reward-based T2I training working without external supervision, which is supported by three established automated benchmarks. The absence of human evaluation is a framing gap, not a claim-invalidating flaw.

- **Critic's claim about "all four evaluation metrics in the ablation (HPSv2, DINO, GIT, ORM) are the same models used to train T2I-R1, which might introduce an indirect bias" — removed.** The paper explicitly addresses this (line 211): "in our ablation studies on IRIS, we never use these reward models in the training objectives, so they can be simple and unbiased metrics to evaluate the performance." The concern is reasonable but the paper's justification is adequate for an ablation study.

- **Critic's claim that "IRIS scores comparably to or slightly below T2I-R1 on this metric (e.g., Fig. 5-9)" — removed as imprecise.** Figures 5–9 are ablation studies comparing IRIS variants, not IRIS vs. T2I-R1. The T2I-R1 comparison is in Fig. 3 and Table 1.

- **Critic's claim that IRIS is "slightly below on most sub-scores" on T2I-CompBench — partially inaccurate.** On T2I-CompBench 1B, IRIS actually wins on 3 of 6 sub-scores (Color, Texture, Non-Spatial). On WISE 1B, IRIS ties or exceeds T2I-R1 on Physics and several categories. The picture is more mixed than the critic suggests.

- **"Strengthening the Paper on Its Own Terms" suggestions about controlled Figure 2, mechanistic analysis, failure cases, and generalization — moved to Nice-to-Haves.** These are valid suggestions for strengthening the paper but are not weaknesses of the current submission.

## Novel Insights

The most interesting synthesis from the reviews is that the paper's main evidential gap (no human evaluation) is a framing issue rather than a methodological one. Multiple reviewers independently noted that the paper uses "human preferences" language without direct human evaluation, yet the paper's formal contributions avoid this claim. This suggests the authors could substantially improve the paper's reception simply by aligning the narrative framing with what the evidence actually supports — competitive benchmark performance without external supervision — rather than adding new experiments. The cross-model confound in Figure 2 was also independently flagged and shares a common root cause: the paper's motivational evidence (Fig. 2) is weaker than its direct empirical evidence (the ablations), and the paper would benefit from acknowledging this disparity explicitly.

## Suggestions

- **Tighten the narrative framing.** Replace "better aligned with human preferences" with "improves scores on established automated benchmarks (GenEval, T2I-CompBench, WISE)" throughout the abstract, introduction, and figure captions. This removes the evidential gap between what is claimed and what is measured.
- **Acknowledge the cross-model confound in Figure 2 explicitly.** Add a sentence noting that the comparison varies both model and task, and point readers to the controlled ablation study (Sec. 4.3) as cleaner evidence for the claim.
- **Add a brief mechanistic discussion.** Even a few sentences analyzing whether the improvement comes from increased output diversity, reduced mode collapse, or other factors would substantially deepen the paper. Tracking per-token distributional entropy across training steps would be informative.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>