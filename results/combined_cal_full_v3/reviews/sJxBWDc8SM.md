## Summary

This paper conducts an empirical analysis of SSMs versus Transformers on synthetic associative recall (MQAR) and copying tasks. It demonstrates that SSMs (Mamba, Hyena) succeed only within a narrow window of learning rates, while Transformers are robust across a wide range. The paper shows that this optimization sensitivity confounded prior expressivity comparisons, that SSMs and Transformers exhibit opposing width-vs-depth scaling preferences, and—through careful ablations—that the 1D convolution is a critical architectural component enabling Mamba's single-layer recall success. It also reports that a newer SSM variant, DeltaNet, achieves Transformer-like learning rate robustness.

## Strengths

- **Clear documentation of LR sensitivity in SSMs (favorability=9.74).** Figures 1, 5, and 7 convincingly show that Mamba and Hyena require a narrower window of learning rates than Transformers to succeed on MQAR and copying, across multiple model dimensions and sequence lengths. The comparison with the LR grid used by Arora et al. (2023) (dashed lines in Fig. 1) is effective in showing how the original evaluation could miss the optimal range entirely.

- **Ablation isolating the role of convolution (favorability=10.07).** The finding that removing the 1D convolution from 1-layer Mamba drops accuracy to 2% (matching the 1-layer Transformer's 2%), and that adding convolution to the 1-layer Transformer raises it to 99%, is clean and informative. It identifies a concrete architectural component responsible for Mamba's single-layer expressivity on this task.

- **Honest replication and re-interpretation of prior work (favorability=8.52).** The paper replicates the original Zoology codebase, shows where it matches reported results, and then demonstrates that finer LR tuning changes the conclusions. Figure 2 is well-designed for this purpose. This is a constructive re-examination rather than a dismissal of prior work.

- **DeltaNet stability result (favorability=9.50).** A newer SSM variant achieving Transformer-like LR robustness is the paper's most forward-looking result and provides a clear direction for future architecture design. The paper transparently notes its limitations (max dimension 256) and labels the mechanism as a hypothesis.

- **1-layer training dynamics analysis (favorability=9.42).** The observation that 1-layer Transformers show a loss bump resembling induction head formation without corresponding accuracy gains (Fig. 6) connects the paper to the mechanistic interpretability literature.

- **Scale of the study (favorability=9.24).** ~3,000 runs across multiple models, dimensions, sequence lengths, and learning rates provides enough breadth to make the central empirical patterns credible.

## Weaknesses

### Fatal
None.

### Major

- **Central thesis overreaches relative to the evidence (favorability=3.02).** The paper claims (line 39) "Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics," but its own results show genuine expressivity differences: (a) 1-layer Mamba can solve MQAR while 1-layer Transformer cannot at any width (Fig. 3), which is an expressivity/complexity difference favoring SSMs; (b) the convolution ablation (Table 2) shows convolution is an expressive component, and the paper itself acknowledges that "in terms of raw expressivity, a 1-layer Mamba without convolution performs approximately identically to a 1-layer Transformer." The more measured claim—that prior expressivity comparisons were *confounded* by optimization issues—is well-supported. But the strong formulation that the difference is "not in expressive power" is contradicted by the paper's own findings, which reveal a mixed picture: some differences are architectural/expressivity (1-layer success, convolution-dependence, width-vs-depth scaling) and some are optimization (LR sensitivity). This overclaiming undermines credibility and needs to be corrected.

- **"Critical optimization instability" is demonstrated only along the learning rate axis (favorability=1.18).** The paper repeatedly refers to "critical optimization instabilities" and a "fundamental mismatch in the loss landscape" (abstract), but the only hyperparameter systematically varied is the learning rate (with Adam as the fixed optimizer). The paper invokes vanishing/exploding gradients as a hypothesized mechanism (lines 23, 221) but never directly measures gradient statistics (norms, variance across layers) or landscape curvature to support this claim. Additionally, the paper does not test whether the LR sensitivity can be mitigated by complementary techniques such as gradient clipping, warmup schedules, or different optimizers. This does not invalidate the core LR sensitivity finding, but the evidence does not warrant the leap to claims about a *fundamentally* different loss landscape—the observed sensitivity could simply mean these models require more careful (but still standard) tuning.

### Minor

- **DeltaNet analysis is promising but underdeveloped (favorability=4.60).** DeltaNet (Fig. 7) is tested only up to model dimension 256, which the paper states was the "maximum size supported by the DeltaNet implementation." It is unclear whether the stability generalizes to the higher dimensions (512, 1024, 2048) where Mamba and Hyena are tested. The attribution to Householder matrices avoiding vanishing gradients (line 221) is stated as a hypothesis without supporting gradient analysis or ablation of DeltaNet's components. The paper is transparent about these limitations, but this limits the strength of the DeltaNet result.

- **Tension between text and Figure 6 regarding Mamba's training dynamics (favorability=4.90).** The text claims Mamba shows a "significant loss bump" (line 190) and describes its dynamics as "mixed" (line 189), yet Figure 6 (and its caption, lines 178-182) shows Mamba(64) with smooth learning dynamics and no bump. The paper does not clarify which Mamba configurations exhibit the bump or show supporting plots, creating an inconsistency between the textual claim and the visual evidence.

### Trivial
None.

## Nice-to-Haves

- Test whether standard mitigation techniques (gradient clipping, warmup, alternative optimizers) broaden the acceptable LR window for SSMs, which would strengthen or qualify the "critical instability" claim.
- Scale the DeltaNet analysis to match the model dimensions used for Mamba/Hyena, or clearly label it as a preliminary observation.
- Measure gradient statistics to directly support or refute the hypothesized vanishing-gradient mechanism.

## Removed Points

These points from the harsh critic input were removed as they do not meet the filtering criteria. Treat them with caution:

1. **Figure 3 heatmap description contradiction:** Removed — parser artifact from image alt text, not the paper's actual claims. The paper's main text correctly states that 1-layer Attention fails.
2. **"'3,000 runs' statistic clarification":** Removed — minor reporting nitpick, does not affect validity of findings.
3. **"MQAR correlation with LM performance questioned":** Removed — the paper cites established benchmarks from prior work (Arora et al. 2023, Olsson et al. 2022); this correlation is standard in the literature.
4. **"No exploration of mitigation strategies":** Removed — the paper explicitly studies DeltaNet as a mitigation; its stated scope is diagnostic, not prescriptive, and demanding mitigation solutions is scope creep.
5. **"No gradient analysis":** Subsumed by Major Weakness 2 (LR-only evidence).
6. **"Missing related works":** Removed per policy — the reviewer cannot verify existence of missing citations.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's analysis is thorough but surfaces no insight that the paper itself does not already contain or that would redirect interpretation of the results.

## Suggestions

1. **Pull back the central thesis.** Replace the abstract/introduction claim that the difference is "not in expressive power but mainly…optimization dynamics" with something like: "prior expressivity comparisons were substantially confounded by suboptimal optimization; we find the gap is partly architectural and partly due to optimization sensitivity." This would align the paper's framing with its actual evidence.

2. **Measure what you hypothesize about.** If the paper claims SSMs suffer from vanishing gradients or a fundamentally different loss landscape, measure gradient statistics (norms, variance across layers) directly.

3. **Resolve the Mamba dynamics inconsistency.** Clarify which Mamba configurations show the "significant loss bump" claimed in the text, or correct the text if Figure 6 is representative.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| `/home/.../8QTpYC4smR.md` | 1.00 | R1 | No | Survey paper, not comparable |
| `/home/.../P49gSPmrvN.md` | 1.00 | R1 | No | Time-dependent discourse, not comparable |
| `/home/.../b5lXUwZiD3.md` | 5.25 | R1 | Yes | Similar empirical architecture comparison on synthetic tasks; had sparser experimental details and more severe novelty concerns |
| `/home/.../pymXpl4qvi.md` | 6.00 | R2 | Yes | Empirical SSM bottleneck analysis; had very low-favorability items (-2.16, -1.43, 0.28) that our paper avoids |
| `/home/.../QFgbJOYJSE.md` | 5.75 | R2 | No | SSM-Transformer theoretical comparison; less comprehensive empirical study |
| `/home/.../DhdqML3FdM.md` | 7.00 | R2 | No | Theory-heavy SSM/Transformer limitations; different contribution type |
| `/home/.../PdaPky8MUn.md` | 8.00 | R1 | Yes | Very thematically similar (showing optimization confounds architecture comparisons); cleaner claims with no overreach |
| `/home/.../d8w0pmvXbZ.md` | 8.00 | R1 | Yes | LR sensitivity study for Transformers; extremely thorough with no framing issues |

**Round-1 bracket:** 5.5–7.5 (above the 5.25 HMM paper, below the 8.00 top anchors).

**Round-2 narrowing:** Comparing our draft's item favorability against **pymXpl4qvi.md** (6.00), our paper has comparable or higher strengths (all above 8.5 vs. that anchor's 6.36–10.40) and its lowest-favorability weaknesses (1.18, 3.02) are less severe than that anchor's most negative items (-2.16, -1.43, 0.28). Against **b5lXUwZiD3.md** (5.25), our experimental execution is substantially more thorough. Against **PdaPky8MUn.md** (8.00) and **d8w0pmvXbZ.md** (8.00), our paper's two Major weaknesses (favorability 1.18, 3.02) are significantly more negative than the weakest items in those 8.00 anchors (which bottomed out at 2.95 and -0.42 respectively, but had far higher strengths).

**Final placement:** The paper's empirical contributions are real and well-supported, placing it clearly above the 5.25 anchor. However, the central thesis overreach and the gap between LR-only evidence and "fundamental loss landscape" claims prevent it from reaching the 8.00 level. The appropriate score is **6.0** — borderline accept, contingent on the authors correcting the framing to match what the evidence actually supports.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>