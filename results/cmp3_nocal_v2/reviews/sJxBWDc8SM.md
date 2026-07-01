## Summary

This paper empirically investigates optimization and scaling differences between Transformers and modern recurrent models (Mamba, Hyena, Mamba2, DeltaNet) on two synthetic benchmarks—multi-query associative recall (MQAR) and copying. Its main finding is that SSMs succeed only within an extremely narrow learning-rate window (Fig. 1), which prior work may have missed, leading to overly pessimistic conclusions about SSM capabilities. The paper further demonstrates opposing scaling preferences (width for SSMs, depth for Transformers), identifies the 1D convolution as the driver of Mamba's 1-layer expressivity (Table 2), and evaluates DeltaNet as a more optimization-stable alternative.

## Strengths

1. **The central empirical finding is timely and well-supported.** The demonstration that Mamba and Hyena succeed only within a narrow learning-rate window (Fig. 1), and that this window can fall outside the grids used in prior work, is a concrete contribution that plausibly recontextualizes several prior negative results about SSMs. The replication in Fig. 2—showing that careful tuning lets Mamba solve MQAR at sequence lengths far exceeding hidden size—is the paper's strongest piece of evidence.

2. **The convolution ablation is clean and mechanistically informative.** Table 2 shows that removing the 1D convolution drops Mamba's 1-layer accuracy from 99% to 2% (same as a 1-layer Transformer), while adding a convolution to the 1-layer Transformer raises it to 99%. This is a crisp, controlled result that isolates a key architectural factor.

3. **The width-vs-depth scaling contrast is clearly illustrated.** Figures 3–4 and Table 1 show that SSMs benefit from width scaling while Transformers benefit from depth scaling. The copy-task results (Table 1) are particularly striking: a 24-layer narrow Mamba (150M params) achieves 16%, while a 12-layer wider Mamba (same 150M params) achieves 100%.

4. **The DeltaNet evaluation provides a constructive path forward.** Figure 7 and the connection to Householder updates (non-vanishing off-diagonals) identifies a concrete architectural direction for improving SSM optimization stability, going beyond critiquing existing models.

## Weaknesses

### Fatal
None.

### Major

1. **The central thesis is overstated relative to the evidence.** The paper claims: *"Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics"* (Sec. 1, p. 2, line 39 of the paper). Yet the paper's own results show that a 1-layer Transformer **cannot solve MQAR even with optimal tuning** (Fig. 3, Sec. 4)—this is itself an expressivity limitation, not an optimization one. The paper also acknowledges earlier that *"fundamental expressivity issues exist between such model classes"* (line 31), creating an internal inconsistency with the stronger claim. What the evidence actually shows is more nuanced: optimization instability *exacerbates* the apparent gap, but genuine architectural differences (induction-head requirements for Transformers, hidden-state bottlenecks for SSMs) also matter. The paper would be stronger by stating this precise finding rather than the broader "mainly optimization" framing.

### Minor

2. **The induction-head interpretation for 1-layer Transformers is speculative.** Section 6 observes a loss bump during 1-layer Transformer training and interprets it as an "attempt to form induction heads" (line 189). The paper uses hedging language ("resembles," "hypothesize") and acknowledges that induction heads normally require ≥2 layers. However, no attention-map analysis (e.g., prefix-matching scores) is provided to corroborate this claim, and the loss bump could equally be attributed to other training phase transitions. Given that this is presented as a listed finding (bullet 3 in the contributions, Sec. 1), the empirical basis is weaker than the prominence suggests.

3. **The LR grid comparison with Arora et al. (2023) is not quantified in the main text.** The paper's central argument that prior work reached overly pessimistic conclusions depends on the claim that Arora et al. used an LR grid that missed the optimal values. Yet the main text never states what LR values Arora et al. actually tested or what values the current finer grid covers. Figure 1 shows "dashed vertical lines" indicating Arora et al.'s values, but the numeric values are not labeled or enumerated in the text. The reader cannot evaluate whether the comparison is fair or whether other hyperparameter differences confound it.

4. **The claim that MQAR and copying are "highly correlated with language modeling performance" (abstract, line 9; Sec. 1, line 23) is stated without a supporting citation or evidence.** This claim is used to motivate the relevance of the synthetic benchmarks, but no reference is provided.

5. **The claim that "increasing the number of layers to more than 2 does not provide any further improvement in MQAR performance" (Sec. 4, line 140) for Transformers is stated without supporting evidence.** No figure, table, or citation accompanies this assertion.

6. **DeltaNet's "Transformer-level robustness" is overstated.** Section 7 (line 221) states that "Transformer-level robustness is only achieved by DeltaNet." However, Fig. 7 shows DeltaNet peaking at ~0.9 accuracy, while Transformers achieve 1.0. DeltaNet matches Transformers in LR *stability* but falls short in peak *accuracy*—a distinction the paper should make explicitly.

7. **Seed sensitivity of the optimal learning rate is not analyzed.** The paper reports mean and relative max-min error across 5 seeds, but does not examine whether the *specific LR value at which the maximum accuracy occurs* is stable across seeds. If the optimal LR shifts between runs, the "narrow window" becomes even harder to exploit in practice than the paper suggests.

### Trivial

8. **"Mamba becomes capable of solving MQAR at relatively small hidden model sizes" (Sec. 3, line 105) is imprecise.** Figure 2 shows that Mamba's improvement at sequence length 512 is clearest at hidden size 256+; at hidden size 64, performance remains moderate (~0.6–0.7). The claim should be quantified.

## Nice-to-Haves

- Standard error bars or confidence intervals would be more informative than the "relative max-min error" metric currently used, especially for the LR-accuracy curves.
- In Table 1, the paper could lead with the cleanest comparison: 24-layer-1024 (150M, 16%) vs. 12-layer-1408 (150M, 100%), which controls for parameter count while varying width vs. depth. The current presentation leads with the confounded 12-layer-1024 (80M) vs. 12-layer-1408 (150M) comparison.

## Removed Points

The following points from the input review were filtered:
- **"Induction head speculation" framed as fatal/dressed-as-analysis**: Kept but downgraded to Minor because the paper clearly uses hedging language ("resembles," "hypothesize") and acknowledges the 2-layer requirement. The criticism is valid but does not reflect an error in the paper—only an insufficiently supported claim.
- **General evaluation/scope concerns** (e.g., "evaluation lacks rigor"): These were general-area sweep statements without concrete anchor in the paper text and were removed.
- **Missing appendix references**: The parser strips the appendix; criticisms about appendix-deferred information are treated as parser artifacts.
- **Presentation suggestions about Table 1**: Moved to Nice-to-Haves.

## Novel Insights

The most incisive observation emerging from the reviews is the tension between the paper's strongest evidence and its broadest claim. The narrow-LR-window finding (Fig. 1), the convolution ablation (Table 2), and the width-vs-depth scaling analysis (Figs. 3–4) are solid, well-controlled experiments that collectively show optimization stability is a *major overlooked factor* in SSM-Transformer comparisons. But they do not show it is the *only* or even *main* factor—the 1-layer Transformer failure is a clear counterexample. The review process highlights that the paper's real contribution (documenting an optimization confound) is stronger than its attempted contribution (claiming the gap is mainly about optimization), and that the induction-head speculation, while interesting, detracts from the rigor of the empirical core.

## Suggestions

1. **Revise the central thesis** to state: *"Optimization instability systematically disadvantages SSMs in standard evaluation protocols, and accounting for it closes much—but not all—of the gap with Transformers. Genuine architectural differences in induction-head requirements and scaling preferences also play a role."* This is at least as impactful and is fully supported by the evidence.

2. **Quantify the LR grid specifics** in the main text: what LR values did Arora et al. (2023) test, what values did this paper test, and what fraction of configurations were affected by the grid mismatch?

3. **Either provide mechanistic evidence for the induction-head interpretation** (attention-pattern analysis showing prefix-matching behavior) or reframe the observation as a neutral description of loss dynamics without the induction-head label.

4. **Add a citation or evidence** for the claim that MQAR/copying are "highly correlated with language modeling performance."

5. **Provide evidence** for the claim that increasing Transformer layers beyond 2 does not improve MQAR performance, or explicitly cite prior work that established this.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>