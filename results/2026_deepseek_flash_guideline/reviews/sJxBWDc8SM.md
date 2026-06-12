Here is the final consolidated review.

---

## Summary

This paper empirically investigates why modern recurrent models (SSMs like Mamba, Hyena, Mamba2, DeltaNet) underperform Transformers on associative recall (MQAR) and copying tasks. Through extensive experiments (3000+ runs), it shows that SSMs have critically narrow learning rate windows — prior comparisons used suboptimal LRs, confounding expressivity conclusions. The paper also reveals contrasting scaling behaviors (SSMs favor width, Transformers favor depth), identifies the 1D convolution as the source of Mamba's 1-layer advantage, and shows that newer architectures like DeltaNet can achieve Transformer-level LR robustness.

## Strengths

- **Systematic demonstration that prior SSM evaluations were confounded by LR sensitivity** (Figure 1): Shows that Mamba and Hyena achieve near-chance performance at the LRs used by prior work (Arora et al., 2023) while achieving near-perfect accuracy at slightly different rates. This directly demonstrates that prior head-to-head comparisons inadvertently evaluated optimizer behavior rather than model capability.

- **Causal ablation isolating the 1D convolution as the mechanistic source of Mamba's 1-layer expressivity** (Table 2): Clean, symmetric result — removing conv1d from 1-layer Mamba drops accuracy from 99% to 2%; adding convolution to 1-layer Transformer's QKV raises accuracy from 2% to 99%. This is a concrete architectural-level finding that cleanly isolates the role of a specific component.

- **Contrasting scaling evidence with matched parameter counts** (Table 1): At equal parameter counts (150M), Mamba with 12 layers/1408 width achieves 100% accuracy on copy task while Mamba with 24 layers/1024 width (same params) achieves only 16%. Cleanly demonstrates that scaling strategy — not parameter count — determines success.

- **Cross-benchmark validation** (Figure 5): Reproduces the narrow-LR-window phenomenon on a second task (copying), showing the finding is not dataset-specific.

- **DeltaNet stability analysis with mechanistic hypothesis** (Figure 7): Shows DeltaNet maintains high accuracy across wide LR ranges, and connects this to Householder-based updates avoiding the multiplicative decay that causes vanishing gradients in Mamba's A matrix — providing a testable mechanistic explanation.

## Weaknesses

### Major

- **Central thesis stated more strongly than the evidence supports.** The paper's headline claim (Line 39: *"Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics"*) oversimplifies the empirical picture. The 1-layer experiments (Section 4, Table 2) show that a properly tuned 1-layer Mamba solves MQAR while a properly tuned 1-layer Transformer fails — this is an expressivity difference at fixed depth, driven by the 1D convolution. The paper's own ablations show Mamba w/o conv1d = 2%, Transformer + Conv = 99%, cleanly isolating an architectural (expressivity) factor. While Section 7 (Line 202: *"in terms of raw expressivity, a 1-layer Mamba without convolution performs approximately identically to a 1-layer Transformer"*) acknowledges this nuance in passing, the abstract and introduction retain a stronger "optimization not expressivity" framing. The actual picture is more nuanced and more interesting: **at 2+ layers, optimization stability is the dominant differentiator; at 1 layer, architectural expressivity differences (the convolution) dominate.** Recalibrating the central thesis to match the full evidence would strengthen the paper.

### Minor

- **Induction head interpretation is speculative.** The paper observes a loss bump in 1-layer Transformer training (Figure 6) and interprets it as an "attempt to form induction heads" (Line 188), listing this as a contribution finding (Line 45: *"a 1-layer Transformer also exhibits a loss drop reminiscent of induction head formation"*). The evidence is solely a visible bump in the loss curve — no attention pattern analysis, head probing, or mechanistic verification is provided. While the paper uses hedging language ("resembles", "hypothesize"), the interpretation goes beyond what the data show. The paper would be stronger by either providing attention-pattern evidence or presenting the bump as an unexplained observation.

- **DeltaNet stability partially undermines the class-level "SSM" framing.** Figure 7 shows DeltaNet achieves Transformer-level LR robustness — a recurrent model that does NOT exhibit the narrow-LR-window pathology the paper characterizes as characteristic of "modern recurrent models." The paper's abstract and introduction retain a class-level framing ("SSMs are brittle") when the evidence shows architecture-specific variation (Mamba/Hyena have narrow windows; DeltaNet does not). The paper handles this partially in Section 7 but the high-level narrative should be more precise.

### Trivial

- **"Relative max-min errors" is not defined.** The paper consistently reports this in figure captions (e.g., Line 25) without defining the metric. Standard deviation or confidence intervals across seeds would be more interpretable.

- **DeltaNet results limited to dimension 256.** The paper notes (Line 231) that DeltaNet experiments were capped at dimension 256 due to implementation constraints, leaving it unclear whether the stability advantage holds at larger scales where Mamba's peak is sharpest (e.g., dimension 512 in Figure 1).

## Nice-to-Haves

- A sweep across widths and depths for the copy task (analogous to Figures 3–4 for MQAR) would strengthen the generalizability claim, though the current copy-task results already serve as useful validation.
- An explicit mathematical comparison of DeltaNet's Householder update vs. Mamba's A matrix update would more directly explain why DeltaNet avoids vanishing gradients.

## Removed Points

- *"Heatmap description is contradictory"* — This refers to figure alt-text, a parser artifact; removed per Hard Rules.
- *"Positional encoding results (Table 4) not shown in main text"* — The appendix is stripped by the parser; removed per Hard Rules.
- *"Copy task only one configuration"* — The copy task is a validation/generalization experiment; this is scope creep.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Recalibrate the central framing to explicitly separate depth-dependent findings: state clearly that at 2+ layers, optimization stability is the key differentiator, while at 1 layer, architectural (convolution-driven) expressivity differences dominate.
2. Either provide mechanistic evidence (attention-pattern analysis around the loss bump) for the induction head claim, or present it as an unexplained observation rather than a finding.
3. Define "relative max-min errors" explicitly, or replace with standard deviations.
4. Note more prominently in the abstract/intro that DeltaNet bucks the trend, making the instability architecture-specific rather than class-level.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Never Train from Scratch (PdaPky8MUn) | 8.0 | R1 | Similar theme (confounded SSM vs Transformer eval) but broader scope (LRA benchmarks), no framing issues; our paper is weaker |
| Zoology (LY3ukUANko) | 6.33 | R1 | Direct predecessor introducing MQAR; our paper provides deeper optimization analysis |
| Understanding Bottlenecks of SSMs (pymXpl4qvi) | 6.0 | R2 | Similar empirical analysis of SSM limitations; our paper is more comprehensive with cleaner ablations |
| Linear attention is (maybe) all you need (0uI5415ry7) | 6.5 | R2 | Similar empirical study of optimization dynamics; comparable quality |
| On Limitation of Transformer for Learning HMMs (b5lXUwZiD3) | 5.25 | R1 | Similar empirical comparison of architectures; our paper is more rigorous |
| Mimetic Initialization (iVy7aRMb0K) | 4.5 | R1 | Similar topic (SSM recall challenges); our paper is more comprehensive and has no novelty concerns |
| Deconstructing What Makes a Good Optimizer (zfeso8ceqr) | 6.0 | R1 | Empirical optimization study; similar rigor |
| Understanding Factual Recall (hwSmPOAmhk) | 7.33 | R2 | Theoretical+empirical on recall; stronger theory but narrower scope |

**Bracket:** Round 1 bracket = 6.0–7.5. Our paper sits above the 5–6 tier (more comprehensive, cleaner ablations) and below the 8.0 "Never Train from Scratch" anchor (narrower synthetic-only scope, framing issues). It is most comparable to 6.0–6.5 range papers (Zoology, Understanding Bottlenecks of SSMs) but with stronger empirical design (symmetric ablations, more architectures, more runs). The framing issue prevents it from reaching the 8.0 level but does not undermine the core empirical contributions.

**Final score: 7.0**

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>