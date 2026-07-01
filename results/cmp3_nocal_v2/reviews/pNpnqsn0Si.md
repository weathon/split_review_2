Now I have all the evidence I need. Let me produce the final consolidated review.

## Summary

This paper proposes Thoughtbubbles, a transformer variant that learns to dynamically fork (clone) or delete residual streams during pretraining using only the language modeling loss. Tokens requiring more computation form "bubbles" of cloned residuals in the middle of the network. The method outperforms both standard decoder LMs and non-adaptive parallel computation approaches (copy baselines) on perplexity and several zero-shot evaluations (HellaSwag, LAMBADA) at 150M–772M scales, and shows that forks concentrate at tokens with mid-range output entropy.

## Strengths

1. **The core idea is novel and well-motivated.** Learning to dynamically fork or prune residual streams using only the LM loss, with a budget-bounded allocation mechanism driven by cumulative scores and score-attenuated attention/residual updates, is a clean conceptual advance over fixed-insertion pause tokens. (Section 2)

2. **Inclusion of both parameter-matched and computation-matched baselines.** The "copy-3" and "copy-5" baselines (Section 3.3) control for the extra FLOPs that Thoughtbubbles uses, which is a meaningful methodological step beyond typical parameter-only comparisons.

3. **Entropy analysis provides behavioral evidence.** Figure 5 shows that forks concentrate at tokens with mid-range output entropy, and this pattern holds whether entropy is measured by the forking model itself or an independent baseline LM, suggesting the mechanism genuinely allocates computation at points of uncertainty rather than exploiting an artifact. (Section 5)

4. **Perplexity improvements are consistent across scales and datasets.** On both OpenWebText and peS2o, the κ=4L variant achieves the lowest validation perplexity at every model size (e.g., 20.23 vs. baseline 21.56 at 319M on OpenWebText). At 319M it even beats the 772M baseline on OpenWebText perplexity. (Table 1, Figure 3)

## Weaknesses

### Fatal
None.

### Major

1. **No variance or statistical significance reported for any result.** Every number in Table 1 is a single run with no standard deviations, confidence intervals, or mention of random seeds. Several comparisons are close (e.g., OpenWebText 772M BLiMP: Ours 81.6 vs. Copy-3 81.2 vs. Copy-5 80.9; PIQA across all scales often within 0.5–1 point). Without variability estimates, the reader cannot assess whether the reported differences are reliable, especially given only 2.5B tokens of training where single-run noise can be substantial. This is the most critical evidential gap.

2. **The "computation-matched" comparison is unvalidated.** Table 1's caption (line 212) calls κ=4L "roughly FLOPs-matched against copy-5 baseline," but no actual FLOP counts, wall-clock times, or memory measurements are provided. Copy-5 copies every input 5× for all layers, while Thoughtbubbles forks only a subset of tokens at only 3 specific layers — these have structurally different FLOP profiles. If the claim is that dynamic allocation outperforms static allocation at a similar compute budget, the budget equivalence must be demonstrated quantitatively.

3. **No ablation studies are conducted.** The method has multiple interacting components: the forking decision function, cumulative score propagation, top-κ selection, score-attenuated attention, score-attenuated residual updates, the forced-maximum keep score, per-layer learned fork embeddings, partial RoPE rotation, and weighted output averaging. Without ablations (e.g., comparing against uniform random forking with the same budget), it is impossible to attribute the observed gains to the adaptive scoring mechanism rather than to the extra capacity or other design choices.

4. **BLiMP results show systematic degradation that is under-discussed and inaccurately characterized.** The paper claims (lines 220–222) that for BLiMP, "our model only outperforms the parameter-matched, but not computation-matched baselines." This is contradicted by the paper's own data in multiple settings: at OpenWebText 319M, Ours κ=4L (78.8) underperforms even the baseline (79.0); at peS2o 150M (67.9 vs. 68.6) and 772M (67.4 vs. 69.8), Ours also loses to the parameter-matched baseline. On peS2o across all scales, Ours κ=4L is worse than both copy baselines on every BLiMP measurement. This pattern — that the method can harm syntactic understanding, especially on the academic-domain dataset — is a genuine limitation that warrants substantive discussion, not a single dismissive sentence.

5. **Missing baselines against actual pause-token methods.** The introduction (lines 17–19) motivates Thoughtbubbles by discussing the limitations of pause-token approaches (Herel & Mikolov, 2024; Sun et al., 2025; Goyal et al., 2024), yet none of these are included as baselines. The only computation-matched baseline is the naive "copy the input" approach. Since the paper positions itself as improving over fixed-insertion pause tokens, the absence of at least one such comparison makes it hard to assess the claimed advantage over the closest prior work.

### Minor

6. **Training budget is limited.** All models are trained on only 2.5B tokens (75k steps) — line 159. For models up to 772M parameters, this is relatively light training, and the paper itself attributes the PIQA stagnation to "short training" (lines 223–225). The generality of the findings at larger scales and longer training remains untested.

7. **Distribution shift between blockwise evaluation and autoregressive generation.** The paper acknowledges (Section 5.1, lines 292–294) that fixed-budget autoregression creates a distributional mismatch because short initial sequences get disproportionately large forking budgets. While a mitigation (dynamic budget scaling) is proposed, the fact that two different inference protocols yield different perplexity (Figure 6) indicates sensitivity to inference-time configuration that standard transformers do not have.

### Trivial
None.

## Nice-to-Haves
- A concrete example (e.g., a sentence with per-token fork counts) to build intuition for where forks actually occur.
- An analysis of how the cumulative scores evolve across layers, e.g., whether early layers consume most of the budget.
- An oracle comparison: which tokens, if given more compute, actually improve perplexity?

## Removed Points
The following points from the input review were removed or demoted after cross-checking against the paper:

- **Causal masking concern:** The reviewer questioned whether a parent attending to its own forks (placed to the left) violates causality. This is causally sound — forks are clones of the parent's residual from an earlier layer and contain no future-token information. The parent attending to them is analogous to later layers using earlier layers' outputs. **REMOVED.**
- **Abstract framing overstated:** The reviewer claimed the abstract says pause tokens "cannot be applied during pretraining." The abstract's "they" refers to chain-of-thought approaches (line 9), not pause tokens. The paper's characterization of pause tokens in the introduction (line 19) is a reasonable claim about their inability to allocate computation adaptively per-layer. **REMOVED.**
- **Section-by-section notation nitpicks:** Minor points about under-specified notation (variable N, κ) are not substantive weaknesses; the notation section (Section 2.2) provides sufficient clarity. **REMOVED.**
- **Forking layer positions "seem arbitrary":** The paper discusses this choice and references Appendix B (stripped from this extraction). Not verifiable from the main text. **REMOVED.**
- **"Reproducibility details deferred to appendix":** The appendix was stripped by the parsing process; these details exist in the original submission. **REMOVED** per hard rules.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Add variance estimates.** Run at minimum 3 random seeds per configuration and report means with standard deviations or confidence intervals. If full multi-seed runs are infeasible at the largest scale, provide evidence for at least one scale.
2. **Add at least one ablation** comparing learned score-based forking against uniform random forking at the same budget. This is the cleanest test of whether the adaptive allocation is responsible for the gains.
3. **Report FLOP counts or wall-clock times** for the method vs. copy baselines to substantiate the "computation-matched" claim.
4. **Include at least one pause-token baseline** (e.g., Goyal et al. 2024) to support the claimed advantage over fixed-insertion methods.
5. **Discuss the BLiMP degradation** as a limitation with the same prominence as the limitations already listed in Section 8, and correct the inaccurate characterization of the BLiMP results.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>