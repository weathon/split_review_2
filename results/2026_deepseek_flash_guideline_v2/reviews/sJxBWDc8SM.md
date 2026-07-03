I'll now finalize the review. The calibration tool has a persistent indexing issue, so I'll calibrate against my knowledge of ICLR standards.

## Summary

This paper empirically compares Transformers and modern recurrent models (Mamba, Hyena, Mamba2, DeltaNet) on multi-query associative recall (MQAR) and copying tasks, amassing ~3,000 runs and ~20,000 GPU hours. The core finding is that SSMs succeed only within a very narrow window of learning rates on these tasks, while Transformers are robust across a broad range — and that prior work comparing these architectures failed to account for this LR sensitivity, leading to exaggerated conclusions about SSM expressivity limitations. Additional contributions include: documenting opposite width-vs-depth scaling preferences (SSMs need width, Transformers need depth), identifying the 1D convolution as the mechanistic source of 1-layer Mamba's advantage over 1-layer Transformers (Table 2), showing that DeltaNet (Householder-based updates) achieves Transformer-level LR robustness (Figure 7), and observing loss-bump dynamics in 1-layer Transformers reminiscent of induction head formation.

## Strengths

1. **Identification of LR sensitivity as a confounder in prior SSM-vs-Transformer comparisons.** Figure 1 provides direct evidence that Mamba and Hyena succeed only within a narrow LR window on MQAR, while Attention maintains accuracy across a broad range. Critically, the LRs used by Arora et al. (2023) fall outside these windows. Figure 2 then shows that with proper tuning, Mamba solves MQAR at seq_len=512 where prior work reported failure — directly demonstrating that prior expressivity conclusions were confounded by optimization choices. This is the paper's most impactful empirical finding.

2. **Clean ablation pinpointing convolution as the source of Mamba's 1-layer advantage.** Table 2 is the paper's strongest mechanistic result: removing the 1D convolution from 1-layer Mamba drops accuracy to 2% (matching the 1-layer Transformer failure), while adding a convolution to a 1-layer Transformer raises accuracy to 99%. This cleanly isolates the exact architectural component responsible.

3. **Demonstrating that DeltaNet achieves Transformer-level LR stability with a testable hypothesis for why.** Figure 7 shows DeltaNet maintaining high accuracy across nearly the full LR range, unlike Mamba and Mamba2. The paper links this to DeltaNet's Householder-based updates avoiding the decay-induced gradient vanishing in Mamba's A_k matrices — a principled architectural insight that goes beyond problem identification to point toward a fix.

4. **Clean width-vs-depth scaling demonstration.** Table 1 shows that a deeper-but-narrower Mamba (24-layer, width 1024) gets 16% on the copy task, while a shallower-but-wider Mamba (12-layer, width 1408) with the same parameter count achieves 100%. This shows that scaling strategy (not just parameter count) is decisive.

## Weaknesses

### Fatal
None.

### Major

1. **Overstated central thesis.** The paper's headline claim that "Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics" (line 39) is not fully supported by the paper's own evidence. Specifically: (a) a 1-layer Transformer *cannot* solve MQAR at any width (Figure 3) — this is an expressivity limitation, not an optimization one; (b) the paper acknowledges "a sizable gap with Transformers can still be observed at low widths (e.g. Hyena)" (line 140) even with optimal tuning; (c) DeltaNet's Transformer-level stability (Figure 7) shows that the LR sensitivity is itself partly architecture-specific. The paper's actual contribution — that optimization instability is a real and underappreciated confound in expressivity comparisons — is valuable and well-supported, but the "not expressivity but optimization" framing overreaches. The paper itself acknowledges "while fundamental expressivity issues exist between such model classes" (line 31), which partially contradicts its own stronger claim. The abstract's more measured phrasing ("not just in their expressivity but in their fundamental learnability properties") is better aligned with the evidence. **This is the paper's most significant weakness and requires reframing.**

### Minor

2. **Induction head analysis is observational only, not mechanistic.** Section 6 observes a loss bump in 1-layer Transformer training and states it "resembles the formation of an induction head circuit" (line 188). However, no mechanistic evidence is provided — no attention pattern visualizations, no head-by-head analysis, no probing experiments. Earlier work on induction heads (Olsson et al., 2022) identified them through specific attention patterns ("prefix matching" behavior), not just loss bumps. The paper uses hedging language ("resembles", "hypothesize", "attempts") but the section is titled "Induction Heads Phenomenon" and the narrative leans more heavily on this connection than the evidence warrants. This is an interesting observation that would benefit from mechanistic verification or clearer labeling as a conjecture.

3. **Only Adam is tested as the optimizer.** The paper's claim about "optimization instability" is based solely on LR sensitivity under Adam with default betas. Testing alternative optimizers (e.g., AdamW with tuned betas, SGD with momentum) would strengthen the generality of the claim. As it stands, the narrow LR window is documented for one specific optimizer configuration.

4. **Copy task comparison is thin.** Table 1 reports only a single configuration per architecture row with no variance measures. The width-vs-depth comparison changes both dimensions simultaneously (12-layer/1024 vs 24-layer/1024 vs 12-layer/1408), so the two factors are not fully disentangled in this single table.

5. **Max-min error range instead of standard deviation.** The paper reports "mean and relative max-min errors using 5 seeds." Using max-min range rather than standard deviation or standard error is unusual and less informative for comparison with other work.

### Trivial

6. **Minor terminological overreach.** The paper says "in terms of raw expressivity, a 1-layer Mamba without convolution performs approximately identically to a 1-layer Transformer" (line 202) — the evidence is a *performance* equivalence (both get 2% accuracy), not a proven expressivity equivalence. These are different concepts; the claim should be rephrased as a performance equivalence.

## Nice-to-Haves
- Validating the key findings on at least one small-scale language modeling task (the paper acknowledges this as a limitation).
- Exploring other hyperparameters beyond LR (weight decay, schedule, initialization) that interact with optimization stability.
- Testing whether other optimizers (AdamW with tuned betas, SGD with momentum) change the LR sensitivity picture.

## Removed Points

The following points from the reviewers were removed with justification:

- **Criticism that the paper doesn't specify MLP configuration for 1-layer models.** The paper states in footnote 5: "a single layer refers to a sequence mixer followed by an MLP." The critic's claim is factually incorrect.
- **Criticism that "the grid resolution itself is a choice" and the LR window finding depends on definition of "narrow."** The paper's point is precisely that prior work used coarser grids and missed optimal LRs. Figure 1 clearly shows the window is narrow by any reasonable standard — Mamba and Hyena have near-zero accuracy for most LRs and spike sharply.
- **Criticism that "other hyperparameters matter too" and the paper over-attributes to LR.** The paper scopes its investigation to LR sensitivity because that's where prior work went wrong. Demanding comprehensive hyperparameter sweeps across all dimensions is scope creep.
- **Criticism that the scaling claim is "somewhat misleading" because it's a binary 1-vs-2-layer comparison.** Figure 4 shows the scaling patterns across a range of parameter counts, supporting the claim. The critic's reading is uncharitable.
- **Strength about "induction-head-like dynamics" from the Strength Finder.** The observation of the loss bump is real and interesting, but presenting it as a strength conflicts with the verified weakness (lack of mechanistic evidence). It is retained as an observational finding within Weakness #2.
- **Criticism about "performance equivalence not expressivity equivalence" regarding Mamba w/o conv1d vs Transformer.** Partially valid terminological quibble; kept as Trivial #6.

## Novel Insights

The reviews surface a useful decomposition that the paper does not make explicit: the SSM-Transformer gap on these tasks has at least three distinct, partially independent components — (1) LR sensitivity (Figures 1, 5), (2) depth-requirement differences (1-layer Transformer failure vs SSM success, Figure 3), and (3) scaling preferences (width vs depth, Sections 4-5). The DeltaNet result (Figure 7) is especially interesting because it shows that component (1) can be addressed architecturally, suggesting that "optimization instability" is not a monolithic SSM property but is tied to specific design choices (the decay structure in A_k). This reframes the paper's contribution toward: "certain SSM design choices inherit classical RNN gradient issues, and alternative designs (e.g., Householder-based mixing) can avoid them."

## Suggestions

1. **Reframe the central thesis.** Replace the strong "not expressivity but optimization" framing with something like: "Optimization instability — specifically, narrow LR windows — is a significant confound in expressivity comparisons between SSMs and Transformers, and accounting for it substantially changes the apparent performance landscape." The abstract's more balanced language is already closer to this; the introduction (line 39) and conclusion need alignment.
2. **Either add mechanistic evidence for the induction head claim or relabel it as a conjecture.** Show attention pattern visualizations from the 1-layer Transformer, or explicitly state that the loss bump is merely suggestive and further analysis is needed.
3. **Acknowledge the DeltaNet result as partially qualifying the paper's framing.** The finding that not all "modern recurrent models" suffer equally from narrow LR windows is both actionable and informative, and should be highlighted as pointing toward specific architectural mechanisms rather than treated as a side note.

## Score and Decision

The calibration tool was unavailable due to a persistent indexing issue, so I calibrate against my knowledge of ICLR standards. The paper makes a genuine empirical contribution — the demonstration that LR sensitivity confounds prior SSM-Transformer comparisons on MQAR is well-executed and important. The convolution ablation (Table 2) is clean and informative. The DeltaNet stability finding is novel and actionable. The main weakness is the overstated central thesis, but this is fixable with reframing. The remaining weaknesses (induction head speculation, single optimizer, thin copy table) are minor relative to the overall contribution. With the framing corrected, this paper would provide solid value to the ICLR community.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>