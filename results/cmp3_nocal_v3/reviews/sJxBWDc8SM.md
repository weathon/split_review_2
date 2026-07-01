## Summary

This paper presents an empirical study comparing the learning dynamics of state-space models (SSMs like Mamba, Hyena) and Transformers on multi-query associative recall (MQAR) and copying tasks. Through over 3,000 runs (~20,000 GPU hours), it shows that SSMs have a critically narrow window of working learning rates on these tasks, while Transformers are robust across orders of magnitude. This narrow LR sensitivity can confound prior evaluations and expressivity conclusions. The paper further demonstrates that a 1D convolution explains much of the 1-layer performance gap, that scaling strategies differ (width for SSMs vs. depth for Transformers), and that newer architectures like DeltaNet can improve optimization stability. The core claim is that the SSM-Transformer gap on these tasks stems from learnability/optimization difficulties rather than fundamental expressivity limitations.

## Strengths

1. **The LR sensitivity finding is the paper's strongest and most practically useful contribution.** Figure 1 demonstrates convincingly that Mamba and Hyena have extremely narrow windows of working learning rates on MQAR, while Transformers are robust across orders of magnitude. The direct comparison to the grid used by Arora et al. (2023) (dashed vertical lines) provides concrete evidence that prior evaluations may have been confounded by insufficient tuning.

2. **The convolution ablation is clean and mechanistically informative.** Table 2 shows that removing the 1D convolution from 1-layer Mamba collapses accuracy to 2% (matching the 1-layer Transformer), and adding a convolution to the 1-layer Transformer boosts it to 99%. This precisely pins down what enables 1-layer SSM performance on MQAR.

3. **Large-scale and systematic empirical effort.** The paper reports over 3,000 runs spanning multiple sequence lengths, model dimensions, architectural ablations, and two distinct tasks. The scope is appropriate for a study of this kind and provides a useful reference dataset for the community.

4. **The DeltaNet comparison provides a forward-looking datapoint.** Showing that DeltaNet maintains high accuracy across a wide LR range while Mamba and Mamba2 do not (Figure 7) links architectural design (Householder-based updates without decaying off-diagonal terms) to optimization stability, pointing toward concrete design principles.

## Weaknesses

### Fatal
None.

### Major

1. **"Loss landscape" claim is not supported by any landscape analysis.** The abstract claims the paper reveals "a fundamental mismatch in the loss landscape of modern recurrent models compared to Transformers" (line 9), and the introduction refers to "severe mismatches in the landscape geometry" (line 45). The paper performs no formal loss landscape analysis — no Hessian eigenvalue computation, no sharpness measures, no loss surface visualization. The only evidence is the observed LR sensitivity, which is consistent with many alternative explanations (gradient explosion at the SSM recurrence, poor parameter scaling, initialization issues, etc.). This language overstates what the evidence supports. The paper's actual contribution (documenting LR sensitivity) is valuable without this overclaim.

2. **Central thesis is stated in broader terms than the evidence supports.** The abstract states that "a crucial differentiator between these architectures lies not just in their expressivity but in their fundamental learnability properties," and line 39 presents the central thesis as: "*Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics.*" All evidence comes from two synthetic benchmarks (MQAR and copying). While the conclusion acknowledges that "validating these dynamics on downstream language modeling tasks is a critical next step" (line 235), the abstract and introduction do not carry this qualification, and the broad framing ("Transformers differ from SSMs not in terms of expressive power") could mislead readers into thinking the paper has resolved a debate about real-world language model capabilities.

### Minor

3. **The induction head interpretation in Section 6 is speculative with thin evidence.** The paper observes a loss bump in the 1-layer Transformer's training curve and states it "resembles the formation of an induction head circuit" (line 188), and hypothesizes that the Attention mechanism "attempts to form induction heads" (line 189). The only evidence is the loss bump itself; there is no mechanistic analysis — no attention pattern visualization, no head-by-head analysis, no ablation confirming the pattern. The paper uses cautious hedging language ("resembles," "hypothesize"), which partially mitigates this, but the induction head framing still gives the observation more narrative weight than the evidence can bear. This is especially notable given that the paper is otherwise rigorous in its empirical methodology.

4. **Non-standard statistical reporting.** The paper reports "mean and relative max-min errors using 5 seeds" throughout. The "relative max-min error" is a non-standard metric that is difficult to interpret. With only 5 seeds, standard deviations (or individual point plots) would be more informative, particularly when comparing models whose variance may differ substantially across tuning conditions — which is exactly the setting of this paper's main claim.

5. **"Opposite scaling" claim is context-dependent but stated as a general finding.** Line 151 states "Attention and recurrent models exhibit opposite scaling behaviors in width and depth." This observation holds only in the 1-layer setting (where attention fails regardless of width, while SSMs improve with width). In the paper's main 2-layer setting (Section 3), both architectures solve the task and no opposite scaling is observed. The claim should be qualified to the shallow (1-layer) regime, which the experiments actually cover.

### Trivial
None.

## Nice-to-Haves

- A cross-task LR transfer experiment (taking the LR that works on MQAR and verifying it does not impair performance on the copy task, or vice versa) would strengthen the claim that the narrow LR window is architectural rather than task-specific.
- Testing other optimizers beyond Adam (e.g., SGD with momentum, or optimizers designed for recurrent architectures) would be a natural follow-up given the paper's thesis about optimization instability.
- Extending the DeltaNet comparison to larger dimensions beyond 256 would strengthen that finding (the authors acknowledge the current limitation).
- A mechanistic analysis to support the induction head interpretation (attention pattern visualization, head-by-head metrics) would turn a speculative observation into a substantive finding.

## Removed Points

- **Criticisms about LR grid values not being stated in the main text** (Section 3 note). Removed because the paper references Appendix A.2 for full experimental details, and the appendix was stripped by the parser. Per guidelines, appendix content is assumed to exist in the original submission.
- **Claim that the narrow LR window after convolution removal is "stated but not shown quantitatively"** (Section 7 note). Removed because this may be addressed in the appendix (referenced as "full details in Appendix A.1"), which was stripped.
- **Criticism that the DeltaNet comparison is limited to dimension 256.** Removed because the paper explicitly acknowledges this limitation ("which was the maximum size supported by the DeltaNet implementation") — the authors already addressed it.
- **Comment that "Only Adam is tested"** as a weakness. Demoted to Nice-to-Haves because testing other optimizers extends beyond the paper's stated scope and is not a flaw in what is presented.
- **Various Section-by-Section observations** (Section 2 comment about math not being used analytically, Section 4 comment about the finding being "well-known," Section 5 comment about Table 1 having only four rows). These are editorial observations, not structural weaknesses, and do not threaten the paper's claims.

## Novel Insights

The most interesting observation that emerges across the reviews — beyond what the paper itself foregrounds — is the asymmetry between what drives performance in SSMs vs. Transformers. The convolution ablation (Table 2) reveals that the Mamba-Transformer gap at 1 layer is essentially a convolution/no-convolution gap, not an SSM-vs-attention gap. This cleanly decouples two confounded factors in prior comparisons and suggests that the "expressivity vs. learnability" debate may itself be a red herring: the relevant architectural distinction for these recall tasks is local preprocessing (convolution/mixing) rather than the core sequence mixer. The DeltaNet result further sharpens this by showing that the SSM learning rate brittleness can be mitigated through architectural changes to the recurrence mechanism itself, pointing toward a design space where optimization stability is a first-class architectural consideration rather than merely a tuning problem.

## Suggestions

1. Tone down the "loss landscape" language in the abstract and introduction; replace with direct descriptions of the observed LR sensitivity and its implications.
2. Qualify the central thesis ("Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics") to explicitly reference the tasks studied, or move the limitation statement from the conclusion into the abstract.
3. Report standard deviations alongside (or instead of) the non-standard "relative max-min error" metric.
4. Either provide mechanistic evidence for the induction head interpretation (attention maps, head-by-head metrics) or remove the induction head framing and simply report the loss bump as an unexplained empirical observation.
5. Clarify that the "opposite scaling" finding applies specifically to the 1-layer setting.

## Score and Decision

This is a solid empirical study with genuine, practically useful contributions (the LR sensitivity finding and convolution ablation are particularly clean and informative). The main weaknesses are framing overclaims and a few methodological quibbles — none of which undermine the core findings. The paper's contributions would benefit from more precise scoping but are real and worth publishing.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>