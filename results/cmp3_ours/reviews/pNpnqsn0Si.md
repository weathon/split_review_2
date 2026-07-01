Here is my final consolidated review.

---

## Summary

Thoughtbubbles introduces a transformer variant that learns to fork (duplicate) and delete residual streams during pretraining using only the language modeling loss, enabling dynamic parallel computation in latent space. The method uses learned scoring functions to decide which residual streams to duplicate or prune, with scores propagated through attention and residual attenuation to create a self-supervised allocation mechanism. Experiments at 150M–772M scales on OpenWebText and peS2o show consistent perplexity improvements (1–1.5 PPL points) and gains on LAMBADA and HellaSwag against parameter-matched and computation-matched baselines.

## Strengths

- **Genuinely novel architectural contribution.** The idea of learning to fork residual streams dynamically during pretraining — with scores propagated through attention and residual attenuation, trained using only the LM loss — is creative, internally coherent, and directly addresses a real limitation of existing inference-time scaling methods (which require token-level supervision or manual placement of thinking tokens). The mechanism connecting forking decisions to the model's own utility (Eq. 8–10) is conceptually clean.
- **Computation-matched baselines (Copy-3, Copy-5) are a meaningful design choice.** Many adaptive-computation papers compare only against parameter-matched models, implicitly benefiting from using more FLOPs. By including baselines that control for the increased computation used by Thoughtbubbles (due to larger block sizes), the paper makes a more honest comparison than is typical.
- **Consistent perplexity improvements across all scales and datasets.** Table 1 shows Thoughtbubbles (κ=4L) achieves the lowest perplexity in all 8 dataset×scale settings. The magnitude (1–1.5 PPL points) is non-trivial for models at this scale. The LAMBADA improvements are particularly striking (e.g., 18.2→25.5 for 150M OpenWebText; 8.1→10.3 for 150M peS2o).
- **Clear limitations section.** The paper honestly acknowledges key weaknesses: no time-matched evaluations, the top-k gradient bottleneck, and the inability to evaluate on hard reasoning tasks (GSM8k) at this scale.

## Weaknesses

### Fatal
None.

### Major

- **No variance or statistical significance reported anywhere.** Table 1 reports every number as a single point estimate with no standard deviation, confidence intervals, or multiple seeds. Several downstream improvements are small (e.g., HellaSwag 27.3→27.6 on 772M peS2o; HellaSwag 29.0→29.3 on 319M OpenWebText). Without uncertainty estimates, the reader cannot assess whether these gaps are meaningful or within the noise floor of zero-shot evaluation, which is known to exhibit non-trivial variance due to prompt sensitivity and dataset subsampling.

- **Analysis is correlational and lacks causal controls.** The entropy analysis (Figure 5) shows fork count correlates with output distribution entropy in a concave relationship, and the attention analysis (Figure 4) confirms parent tokens attend to their forks more than to unrelated tokens. Both are descriptive but do not establish that *learned adaptive* allocation causes the performance improvement. A minimal causal ablation — comparing learned forking against random forking matched on the same marginal fork-count distribution — would directly validate the adaptive mechanism. Without it, the paper cannot rule out that the benefit comes primarily from having *more* residual streams rather than from allocating them intelligently.

- **The Copy-N baselines use a weaker decoding protocol than Thoughtbubbles.** The Copy-3/Copy-5 baselines "take the rightmost residual for decoding" (line 170), discarding all other copied residuals at the output layer. Thoughtbubbles uses score-weighted averaging of all residuals (Eq. 11). This asymmetry means the baselines are weaker than a truly FLOPs-matched comparison would require — a fairer baseline would also average or learn to weight the copied residuals. This is acknowledged in the paper's structure but not addressed as a limitation.

### Minor

- **319M-vs-772M scaling claim lacks FLOPs context in the main text.** Line 214 states: "our approach at a 319M parameter scale has lower perplexity on OpenWebText than the baseline approach at the 772M scale." While technically true (20.23 vs 21.22) and the FLOPs issue is mentioned in the Table 1 caption, the specific claim as stated in the main text could mislead readers into thinking this is a pure parameter-efficiency result. The 319M Thoughtbubbles model uses κ=4L (substantially more FLOPs than a standard 319M model), so the comparison mixes parameter scale with computation budget.

- **Mixed results on BLiMP and PIQA are acknowledged but could be framed more carefully.** The paper honestly notes that BLiMP results trail Copy baselines and PIQA is comparable. However, the abstract and claim (line 34) say the method "performs competitively" on these metrics. In several settings Thoughtbubbles is *worse* than baselines on these tasks (e.g., PIQA 61.9 vs 62.3 Baseline on 772M OWT; BLiMP 67.4 vs 73.3 Copy-3 on 772M peS2o). The framing could be more precise about which task families benefit most.

- **No qualitative analysis of forking decisions.** The paper shows aggregate statistics (entropy correlation in Figure 5) but never presents concrete examples of which tokens get forked. Qualitative examples would substantially strengthen the interpretability claim.

### Trivial

- **No training loss curves.** Showing convergence behavior over the course of pretraining would strengthen the evidence that Thoughtbubbles consistently learns better representations.

## Nice-to-Haves

- Comparison against at least one pause-token or thinking-token method (e.g., Goyal et al., 2024; Herel & Mikolov, 2024) would better validate the paper's framing in the introduction. The paper motivates the problem by criticizing these methods but does not test against them.
- An ablation of forking layer placement and count (currently deferred to appendix B, which was stripped by the parser).
- Analysis of what the fork embedding $v_\theta^{(k)}$ learns — whether it carries semantic meaning or is merely a discriminator signal.

## Removed Points

These points from the input review are removed with justification:

1. **"Baselines do not include actual prior methods (structural weakness)"** — Removed. The paper's experimental framing compares against parameter-matched and computation-matched baselines (standard transformer + Copy-N), which are reasonable for demonstrating that adaptive forking outperforms non-adaptive parallel computation. The paper does *not* claim to have compared against pause-token methods empirically; it motivates the problem by discussing their limitations conceptually. Claiming uncompetitive baselines confuses "not the strongest possible baselines" with "not competitive."

2. **"Autoregression perplexity discrepancy (~30 vs ~21)"** — Removed. The Figure 6 caption explicitly states: "over a smaller subset of OpenWebText dev set." Different evaluation set yields a different value; this is explained.

3. **"Missing gradient handling for top-k implementation detail"** — Removed. The Limitations section (line 320–321) explicitly acknowledges the top-k gradient bottleneck. The paper is not required to describe the gradient approximation mechanism in full detail for a conference paper.

4. **"Forks influencing parent tokens is nearly tautological"** — Removed. The attention analysis (Figure 4) empirically verifies that the model actually *uses* the forks it creates, which is a non-trivial sanity check. The claim is that forks "meaningfully influence" the parent token, not that this is surprising.

5. **"Missing sensitivity analysis on forking layer placement"** — Removed. The paper states layers 3, 7, and 11 and references appendix B for further discussion. The appendix was stripped by the parser but exists in the original submission.

6. **"Copy-3 better than Copy-5 unexplained"** — Removed. The paper does not claim to explain this phenomenon. It is a baseline behavior that does not undermine the core claims.

## Novel Insights

The reviews converge on a genuine gap that the paper's own analysis does not fully address: the paper shows that learned forking correlates with entropy and that forks attend to their parents, but no experiment isolates whether the *adaptive allocation* itself drives the performance gains as opposed to simply having more residual streams. A causal ablation (learned vs. random forking) would directly test the paper's central thesis. Additionally, the Copy-N baseline decoding asymmetry (rightmost residual only vs. score-weighted averaging) is a real methodological concern that weakens the comparison.

## Suggestions

- Report variance (standard deviations or confidence intervals from multiple evaluation seeds) for all metrics in Table 1.
- Add a causal ablation: compare learned forking against random forking matched on marginal fork-count distribution to isolate the benefit of adaptive allocation.
- Either average all copied residuals in Copy-N baselines (making them truly FLOPs-matched) or explicitly frame the decoding asymmetry as a favorable comparison for the proposed method.
- Frame the 319M-vs-772M comparison with explicit mention of the FLOPs difference in the main text, not just the table caption.
- Add qualitative examples of which tokens receive forks to strengthen the interpretability claim.
- Be more precise in the abstract about which evaluations the method excels on vs. where results are mixed.

## Score and Decision

**Calibration.** I compared this paper against several human-reviewed anchors from the calibration corpus:

| Anchor Paper | Avg Score | Decision | How It Compares |
|---|---|---|---|
| *CoTFormer* (5.75) | 6,5,6,6 | Accept | Also a novel adaptive-computation transformer architecture. Thoughtbubbles has more consistent perplexity gains but shares the weakness of no variance reporting. Comparable contribution level. |
| *Learning How Hard to Think* (6.50) | 6,8,6,6 | Accept | Adaptive computation allocation for decoding. Stronger empirical validation (multiple seeds, confidence intervals) but less architectural novelty. Thoughtbubbles is slightly weaker on empirical rigor. |
| *Hyper-Connections* (6.25) | 6,6,8,5 | Accept | Architectural improvement to residual connections. Thorough analysis and ablations. Thoughtbubbles has comparable novelty but less thorough empirical validation. |
| *FiRST* (3.00) | 3,3,3,3 | Reject | Input-adaptive layer skipping. Rejected for limited novelty and weak evaluation. Thoughtbubbles has substantially more architectural novelty. |

**Round 1 bracket:** 5.0–6.0. After narrowing against the CoTFormer anchor (5.75, Accept), which is the closest topical match: Thoughtbubbles has a more novel architecture but weaker empirical methodology (no variance, no causal ablation). I set the score at 5.5, reflecting a solidly novel contribution whose evidential support is not yet as strong as its strongest peers.

**Score**: 5.5

**Decision**: Accept

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>