Now I have verified all the key claims in the paper. Here is the final consolidated review.

---

## Summary

This paper presents an empirical study comparing optimization dynamics of Transformers and modern recurrent models (Mamba, Hyena, Mamba2, DeltaNet) on two synthetic benchmarks (MQAR and copying). It documents that SSMs succeed only within a narrow window of learning rates while Transformers maintain high accuracy across roughly two orders of magnitude, demonstrating that optimization instability is a significant confounder in prior architecture comparisons. It further identifies the 1D convolution as a critical architectural component enabling single-layer SSM recall performance.

## Strengths

- **Large-scale, well-motivated empirical investigation.** The paper reports ~3,000 runs and ~20,000 GPU hours on two well-justified synthetic benchmarks (MQAR and copying) that are established proxies for in-context learning capabilities. This scale enables thorough, controlled ablations that would be infeasible at full LM scale.

- **Striking and practically important finding about LR sensitivity.** Figures 1 and 5 convincingly demonstrate that Transformers maintain high accuracy across roughly two orders of magnitude of learning rates, while Mamba and Hyena succeed only within a narrow window (~0.5–1 order of magnitude). This is a real result that practitioners and researchers should be aware of when comparing architectures.

- **Clean ablation identifying the 1D convolution as a critical architectural component (Table 2).** Removing the 1D convolution from 1-layer Mamba drops accuracy to 2% (same as a 1-layer Transformer), and adding a convolution to a 1-layer Transformer raises its accuracy to 99%. This reciprocal ablation provides a clear mechanistic link and is more informative than many typical "contribution" experiments.

- **Useful re-contextualization of prior work.** Figure 2's comparison of Zoology results (with a sparse LR grid) against the paper's finer-tuning results makes a concrete point that prior expressivity comparisons may have been confounded by optimization choices.

- **Forward-looking DeltaNet result.** Figure 7 shows DeltaNet achieves Transformer-like stability (broad LR tolerance) while Mamba and Mamba2 do not, providing practical guidance for architecture design.

## Weaknesses

### Fatal
None.

### Major

- **Central thesis overreach at line 39.** The paper states: *"Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics."* This contradicts the paper's own acknowledgment two paragraphs earlier that "fundamental expressivity issues exist between such model classes" (line 31). It also conflicts with the paper's own evidence: (a) Table 2 shows a 1-layer Mamba without its 1D convolution performs at 2% accuracy, identically to a 1-layer Transformer — the convolution adds expressivity, not just learnability; (b) Section 3 reports residual performance gaps at low widths even after optimal tuning (e.g., Hyena). The paper's more measured framing elsewhere (abstract: *"not just in their expressivity but in their fundamental learnability properties"*; conclusion: *"modern recurrent models can be as expressive as Transformers on these tasks but are harder to train"*) is better supported. This overreach does not invalidate the empirical results but requires a reframing of the paper's central thesis. The strongest defensible claim is that *optimization instability significantly confounds prior expressivity comparisons, and accounting for it reveals SSMs are substantially more capable on these tasks than previously reported.*

### Minor

- **Induction head claim (Section 6) is under-evidenced.** The paper observes a loss bump in a single-layer Transformer and states it "resembles the formation of an induction head circuit." However, induction heads were originally defined as a two-layer circuit (Olsson et al., 2022); no mechanistic analysis (attention pattern visualizations, head importance analysis, causal interventions) is provided to support the attribution. The paper hedges ("we hypothesize," "to the best of our knowledge"), yet lists it as a contribution (line 45). The observation of a phase transition is valid, but the specific attribution to induction heads needs stronger evidence or should be stated more cautiously (e.g., "a phase transition whose origin is unknown").

- **The Zoology comparison (Figure 2) may have confounds beyond the LR grid.** The three curves ("Zoology original," "Zoology replication" with the original LR grid, and "Our" with a finer grid) sometimes differ between the original and replication curves (e.g., Mamba at sequence length 512), suggesting implementation differences beyond just LR grid spacing (different code versions, random seeds, or training configurations). The paper attributes all improvement to the finer LR grid, but the gap between the two control conditions complicates this interpretation.

- **Asymmetric parameter counts in Table 1 (copy task).** A 12-layer 1024-width Mamba has only 80M parameters vs. 150M for a 12-layer 1024-width Transformer at the same width. The paper's core point about width-vs-depth scaling is well-supported (12-layer 1408-width Mamba at 150M achieves 100%), but the initial asymmetry deserves more explicit acknowledgment.

### Trivial

- **The metric "relative max-min error" is used throughout (Figures 1–3, 7) but never defined in the main text.** Standard deviation or confidence intervals would be more interpretable.

- **The claim that Transformers "benefit from scaling in depth" (line 138) is based on comparing only 1-layer vs. 2-layer configurations.** This is a binary finding (2-layer works, 1-layer does not), not a scaling trend per se. Testing 3+ layers would be needed to establish a trend.

## Nice-to-Haves

- **Gradient analysis to diagnose the cause of LR instability.** The paper hypothesizes that SSMs inherit vanishing/exploding gradient issues from classical RNNs, but offers no gradient statistics (norms, variance, spectra) to support this. Measuring these would raise the contribution from "documentation" to "diagnosis."

- **More seeds for key configurations.** 5 seeds is standard for this scale of study, but claims about stability windows would be more convincing with 10–20 seeds for the anchor experiments (e.g., Figure 1 LR sweeps).

## Removed Points

These points were raised in the input review but are removed for the following reasons:

- *LR grid values missing from main text*: The paper states details are in Appendix A.2, which is stripped by the parser. Per review guidelines, appendix content is assumed to exist in the original submission.
- *No comparison with linear attention variants*: The paper scopes itself to Transformers vs. modern recurrent models (SSMs). Requesting additional model families is scope creep.
- *Lack of gradient analysis as a fatal methodological gap*: The paper explicitly acknowledges that "a formal theoretical explanation for the optimization brittleness we empirically observe remains an important open question" (Section 8). Documenting a phenomenon without fully explaining it is a legitimate contribution.
- *The 1D convolution ablation undermines the thesis*: This misreads the paper — Table 2 shows convolution adds expressivity to 1-layer models (an expressivity finding), while the LR sensitivity finding is about optimization. The paper's more nuanced framing (abstract/conclusion) acknowledges both.
- *The paper claims general expressive equivalence*: The conclusion explicitly limits the claim to "on these tasks" (line 235).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the central thesis.** Replace the line-39 assertion with what the evidence actually supports: "Optimization instability significantly confounds prior expressivity comparisons, and accounting for it reveals SSMs are substantially more capable on recall/copy tasks than previously reported." This would make every result in the paper support the thesis rather than contradict it.

2. **Either strengthen or downgrade the induction head claim.** Add attention visualizations, head ablation, and comparison with the known 2-layer induction head signature. If not provided, state it as a speculative observation rather than a contribution.

3. **Clarify the Zoology comparison.** Document what differs between the "Zoology replication" and "Our" setups beyond the LR grid (seeds, training configurations, codebase differences).

4. **Define "relative max-min error"** in the main text and consider using standard deviation or bootstrapped confidence intervals instead.

## Score and Decision

**Score: 5.5**

**Decision: Reject**

**Calibration summary across all anchors retrieved:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| iVy7aRMb0K (Mimetic Init.) | 4.50 | R1 | Yes | Lower: weaker empirical support, incremental novelty issues |
| b5lXUwZiD3 (Transformer-HMM) | 5.25 | R1 | Yes | Comparable: similar synthetic-only empirical study, comparable strength |
| BwG8hwohU4 (StableSSM) | 5.33 | R1 | Yes | Comparable: similar scope, but has theory-experiment disconnect this paper avoids |
| pymXpl4qvi (SSM Recency) | 6.00 | R1 | Yes | Higher: has theoretical backing this paper lacks |
| LY3ukUANko (Zoology) | 6.33 | R1 | Yes | Higher: includes real LM pretraining and theory |
| aN4Jf6Cx69 (Induction head) | 4.50 | R2 | No | Lower: narrower focus |
| lkRjnNW0gb (Stable Transformer) | 5.67 | R2 | No | Comparable: empirical study of training stability |
| d8w0pmvXbZ (Small-scale instab.) | 8.00 | R1 | Yes | Higher: much more thorough, practical recommendations, clean scope |
| Tzh6xAJSll (Scaling Associative) | 7.60 | R2 | No | Higher: includes theory and scaling laws |

**Bracket:** Round 1 placed the paper at 5.0–6.5. Round 2 narrowed by comparing itemized anchor weaknesses. The paper sits below pymXpl4qvi (6.00) and Zoology (6.33) because it lacks both theoretical backing and real-LM validation, and above Mimetic Init. (4.50) and StableSSM (5.33) because its core finding is cleaner and its execution more focused. The decisive factor pulling it below the 6.0 acceptance bar is the framing overclaim (line 39), which creates a contradiction with the paper's own evidence and requires significant reframing. The empirical work is valuable and should be revised for resubmission.

**Score rationale:** The paper's strengths are genuine and well-supported: the LR sensitivity finding, the convolution ablation, and the DeltaNet result each provide actionable insight. However, the central thesis overreach (claiming the gap is "not expressivity" when the paper's own evidence shows expressivity differences) and the weakly-supported induction head claim prevent the paper from meeting the acceptance bar in its current form. A revision that reframes the thesis, tempers the induction head speculation, and clarifies the experimental confounds would substantially strengthen the paper.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>