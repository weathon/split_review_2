## Summary

This paper empirically compares SSMs (Mamba, Hyena) and Transformers on synthetic recall (MQAR) and copying tasks, finding that SSMs succeed only within a narrow learning rate window while Transformers are robust across orders of magnitude. Through ~3,000 runs and ablations, it shows that prior expressivity comparisons were confounded by this optimization sensitivity, that SSMs scale with width while Transformers need depth, and that the 1D convolution is a critical architectural component that bridges the 1-layer performance gap between architectures.

## Strengths

1. **Clean, large-scale LR sensitivity analysis (Figure 1).** The extensive LR grid (5 seeds, multiple model sizes) cleanly demonstrates that Mamba and Hyena succeed only within a narrow LR window, while Transformers are robust across orders of magnitude. Dashed vertical lines showing prior work's LRs make the practical point concrete and reproducible. This is the paper's strongest contribution.

2. **Compelling convolution ablation (Table 2).** Removing conv1d from 1-layer Mamba drops accuracy from 99% to 2%; adding convolution to 1-layer Transformer raises accuracy from 2% to 99%. This is a clean mechanistic link that isolates what each architecture needs to solve the task. The symmetry is elegant and informative.

3. **Contrasting scaling behaviors (Figures 3, 4, Table 1).** SSMs scale with width while Transformers need depth. This has practical relevance for practitioners choosing how to allocate parameters and contextualizes prior theoretical results about linear hidden-state memory bottlenecks.

4. **DeltaNet analysis (Figure 7).** Shows that DeltaNet achieves Transformer-level LR robustness, with a hypothesized connection to Householder matrices vs. decay-based A matrices causing vanishing off-diagonal gradients. This provides a concrete lead for future work on stable SSM architectures.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Tension in the central framing between expressivity and optimization.** Line 39 states: "Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics." However, the paper's own results show a genuine expressivity gap at 1-layer (1-layer Transformer gets 2% while 1-layer Mamba gets 99%, Table 2). The paper then resolves this by showing that convolution bridges the gap (Attention+Conv achieves 99%, Mamba w/o conv gets 2%). This is an important finding, but it means the difference is partially architectural/expressivity-driven, not purely optimization-driven. The findings are more precisely summarized as "when controlling for components, the remaining gap is optimization-driven." The abstract's version ("not just in their expressivity but in their fundamental learnability") is more accurate than line 39. This imprecision does not undermine the core empirical contributions but should be corrected.

2. **Speculative induction head interpretation (Section 6).** The claim that the 1-layer Transformer's loss bump "resembles the formation of an induction head circuit" (line 188) — a phenomenon previously observed only in multi-layer Transformers — is presented as a key contribution ("Divergent Single-Layer Dynamics" in the intro bullets) but lacks mechanistic evidence. The observation is a loss-curve non-monotonicity, which could arise from many causes (LR schedule effects, saturation in specific attention heads, gradient noise). The paper hedges with "resembles" and "hypothesize," but connecting this to the specific circuit identified by Olsson et al. (2022) without attention map visualization or head-level probing is thin for a claimed contribution.

3. **Copying task analysis is thin (Section 5).** Unlike the thorough MQAR analysis spanning Sections 3, 4, 6, and 7, the copying analysis consists of one LR curve (Figure 5), one table with 4 rows (Table 1), and a few paragraphs. The claim that "attempts to provide fair comparisons by matching parameter counts through increased depth in SSMs are misguided" rests largely on a single comparison (12-layer Mamba at 1024 width gets 0% vs. 12-layer Mamba at 1408 width gets 100%). More evidence is needed for a claim of this strength.

4. **Over-interpretation of scaling claim (Figure 4 caption).** Claiming "the scaling strategy, rather than the total number of parameters, is what primarily impacts performance" goes beyond what the data supports. Figure 4 compares accuracy vs. parameters for a limited set of configurations (1-layer vs. 2-layer at varying widths). The data supports that width vs. depth matters differently per architecture, but the strong "rather than" framing is not fully justified by the number of points shown.

### Trivial
None.

## Nice-to-Haves

- **Gradient analysis.** The paper identifies an optimization instability but does not characterize it directly. Gradient norm plots, analysis of A-matrix eigenvalue evolution across LRs, or loss landscape visualization would deepen the contribution.
- **Downstream validation.** A small-scale language modeling experiment (e.g., controlled LR sweep on 1B tokens) would validate whether the synthetic-task findings transfer to real pretraining. The paper acknowledges this as a limitation.

## Removed Points

- Missing optimizer hyperparameters (beta1, beta2, weight decay): The paper states these are in Appendix A.2, which is stripped by the parser. Per rules, appendix content is assumed present.
- Missing discussion of how LR window changes with depth: Paper references Appendix A.6 for deeper networks. Same appendix-stripping issue.
- "No downstream validation" as a fatal gap: The paper is scoped as a synthetic analysis and explicitly acknowledges the limitation. Moved to Nice-to-Haves.
- General reproducibility nitpicks: Paper states code is publicly available.
- Formatting/presentation nitpicks: These are parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Reconcile the framing: replace "not in terms of expressive power" (line 39) with a more precise statement like "when controlling for architectural components (convolution), the remaining gap is optimization-driven."
2. Either strengthen Section 6 with mechanistic evidence (attention map visualization, probing) or downgrade the induction head interpretation from a claimed contribution to a secondary observation.
3. Expand the copying analysis with at least a limited LR × width sweep to match the thoroughness of the MQAR analysis.

## Score and Decision

**Calibration Anchors** (all rounds):

| Anchor | Score | Round | Comparison to this paper |
|--------|-------|-------|--------------------------|
| Never Train from Scratch (PdaPky8MUn) | 8.00 | R1 | Similar theme (improper setup confounds comparisons) but cleaner narrative, more thorough eval, no speculative section → current paper weaker |
| Zoology (LY3ukUANko) | 6.33 | R1 | Same MQAR task. Zoology has real LM experiments; current paper has more thorough LR sweep. Similar quality. |
| From generalization analysis to optimization for SSMs (EGjvMcKrrl) | 6.00 | R1 | Both study SSM optimization. Current paper has stronger empirical work but no theory. Slightly higher quality. |
| Understanding Synthetic Context Extension (hUD9ugK2OH) | 5.75 | R2 | Both use synthetic benchmarks. Current paper has cleaner experimental design. Higher quality. |
| MambaPEFT (UAKnJMIBwf) | 6.00 | R2 | Practical methods paper. Current paper is more principled with cleaner empirical finding. Slightly higher. |
| Mamba Neural Operator (VtP7CamOR5) | 3.00 | R1 | Poor presentation, unclear methodology → current paper much stronger. |

**Round 1 bracket**: 5.5–7.5  
**Narrowing to 6.0–7.0**: The paper is cleaner than Zoology and more empirically thorough than the 6.0 SSM theory paper, but lacks the downstream validation and crisp narrative of the 8.0 "Never Train from Scratch" paper. The absence of fatal or major weaknesses lifts it into the accept range, while the framing imprecision, speculative induction head section, and thin copying analysis prevent it from reaching the 8.0 tier.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>