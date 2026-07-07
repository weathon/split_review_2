Now I have all the information needed. Here is the final consolidated review.

---

## Summary

Thoughtbubbles introduces a Transformer variant that learns to dynamically fork and prune residual streams during pretraining using only a language modeling loss. Tokens needing more computation form "bubbles" of cloned residuals that receive additional processing, which are later merged back. The method uses a score-attenuation mechanism that simultaneously trains the forking policy and the underlying model. Experiments across 150M–772M parameters show consistent perplexity improvements over standard transformers and non-adaptive parallel computation baselines on OpenWebText and peS2o, with the striking result that a 319M Thoughtbubbles model outperforms a 772M baseline.

## Strengths

- **Genuinely novel and well-motivated core idea.** Learning to dynamically fork and prune residual streams during pretraining — with only an LM loss and no supervision on when/where to allocate computation — is a clean formulation. The paper correctly identifies that existing pause-token approaches insert streams at fixed/pre-determined locations, whereas Thoughtbubbles can allocate extra computation at intermediate layers conditioned on learned token importance (Section 1, paragraph 4). This is a real conceptual contribution.

- **Elegant score-attenuation mechanism for learning the forking policy.** Using cumulative scores to attenuate both attention logits and residual updates (Eqs. 8–10) creates a clean training signal: tokens with low scores are effectively ignored, so the model learns to assign high scores to tokens where extra compute actually helps the loss. This avoids needing a separate RL or auxiliary loss function.

- **Consistent perplexity improvements across all scales and datasets.** In Table 1, Thoughtbubbles (κ=4L) achieves lower validation perplexity than all baselines at every scale (150M, 319M, 772M) on both OpenWebText and peS2o, without exception across all 12 rows. This consistency is notable and provides evidence that the method produces real gains.

- **The 319M-outperforms-772M result is striking.** A 319M Thoughtbubbles model (κ=4L, PPL 20.23) beats a 772M baseline (PPL 21.22) on OpenWebText — a result that, if robust, represents a significant finding about the efficiency gains available from adaptive parallel computation during pretraining.

## Weaknesses

### Fatal
None.

### Major

- **No FLOPs measurements to substantiate the "computation-matched" claim.** The Table 1 caption states that κ=4L is "roughly FLOPs-matched against copy-5 baseline," and Section 3.3 says copy-5 "allows us to slightly exceed the computation of our approach." Yet no FLOP counts, attention FLOPs, or any quantitative computation measurements are provided anywhere in the paper. Without these, the reader cannot determine whether Thoughtbubbles' perplexity improvements stem from better computation allocation or simply from using more (or less) total compute. The claim that the comparison is "computation-matched" is central to interpreting whether the gains come from adaptivity or from raw compute differences, and it is currently unsubstantiated.

- **No comparison against pause-token baselines, despite the paper's direct motivation against them.** The paper's motivation (Section 1) is built on the claimed limitations of pause-token approaches (Herel & Mikolov 2024, Sun et al. 2025, Goyal et al. 2024): they insert computation at fixed locations and require manual design. Yet none of these are used as experimental baselines. The copy baselines (which duplicate all tokens equally throughout all layers) do test non-adaptive vs. adaptive parallel computation, but they do not represent the current state of pause-token methods. Adding pause-token baselines at the same forking layers (3, 7, 11) with the same budget κ would directly test whether the gains come from adaptivity specifically — the paper's central claim — versus simply having more residual streams at carefully chosen fixed locations.

### Minor

- **No variance or statistical significance reporting.** Table 1 reports single numbers without standard deviations or information about the number of random seeds. Some downstream improvements are small (e.g., HellaSwag 26.9 baseline vs. 27.7 ours at 150M), and several BLiMP results show Thoughtbubbles underperforming copy baselines. Without variance estimates, it is impossible to assess whether claimed improvements are statistically significant. The perplexity improvements are consistent across settings, which partially mitigates this concern, but variance reporting is still needed for the downstream evaluations.

- **Evaluation misaligned with the "parallel thinking" framing.** The introduction and conclusion frame Thoughtbubbles as enabling "parallel thinking" for "multi-step reasoning" tasks. Yet evaluations are limited to perplexity, LAMBADA, HellaSwag, BLiMP, and PIQA — none of which measure multi-step reasoning. The paper acknowledges this limitation (Section 8, citing hardware constraints and the multi-billion-parameter scale needed for benchmarks like GSM8k), but the gap between the narrative and the evaluation is significant. Including a synthetic multi-step reasoning task (e.g., modular addition, parity) or a small-scale reasoning evaluation would better align the framing with the evidence.

- **How parameter-matching is achieved is not explained.** The paper claims all settings are "parameter-matched" but does not specify whether the baseline transformer has the same hidden size and layer count as Thoughtbubbles (which adds forking decision functions and fork embeddings), or whether it has more transformer parameters to compensate. This detail matters for interpreting the results and should be stated in the main text or a clearly referenced appendix section.

### Trivial
None.

## Nice-to-Haves

- Include at least one reasoning-focused evaluation (synthetic or small-scale) to align the evaluation with the paper's framing.
- Report results from multiple random seeds with standard deviations, especially for downstream tasks where improvements are small.
- Discuss or explore alternatives (e.g., straight-through estimators, soft top-k) for the hard top-k gradient bottleneck noted in Section 8.
- The BLiMP results where Thoughtbubbles underperforms copy baselines (e.g., 319M OpenWebText: Copy-3 80.5 vs. ours κ=4L 78.8) are acknowledged but could be discussed more prominently.

## Removed Points

These points from the input review were filtered:

1. **"Section 1 characterization of pause tokens is inaccurate"** — The paper's characterization is accurate: pause-token methods insert computation at predetermined locations, and the paper notes that Sun et al. (2025) themselves acknowledge the manual-design limitation. Removed as factually incorrect criticism.

2. **"Tension between forced keep score and cumulative score"** — The paper clearly explains this design choice (Eq. 4 forces the original token to physically survive for next-token prediction; line 109 states the cumulative score does not share this forced maximum). Removed as the paper already addresses this.

3. **"Dynamic forking confounds perplexity comparison"** — Dynamic forking maintains a fixed ratio of budget to input size; for fixed-length evaluation sequences, all sequences receive the same budget. Removed as a misunderstanding.

4. **"Figure 4 finding is circular / forced by architecture"** — The paper presents this analysis as validation that the mechanism behaves as designed, not as a surprising emergent finding. Removed as a misreading of the paper's intent.

5. **"Figure 5 entropy-fork relationship is predictable"** — Similarly, the paper presents this as confirmatory analysis, not as a surprising discovery. Removed.

6. **"Section 5.1 autoregression gap"** — The paper explicitly acknowledges this gap and describes the mitigation (dynamic forking), referenced to Appendix E.1 which exists in the original submission. Removed.

7. **"Architecture/training details missing from main text"** — Details of hidden dimension, layers, heads, and learning rate are standard to place in the appendix, which exists in the original submission. Removed.

8. **The reviewer's own FLOPs calculation** (146L² vs 300L²) — This is unverified reviewer analysis; if true it would strengthen the paper's claims. The actual issue (no FLOPs measurements provided by the paper) is retained as a Major weakness above.

## Novel Insights

None beyond the paper's own contributions. The reviews converge on the same picture: a genuinely novel core idea with clean mechanism design, supported by consistent perplexity results, but held back by evaluation gaps (no pause-token baselines, no FLOPs analysis, no variance reporting, no reasoning tasks).

## Suggestions

1. **Provide actual FLOPs or compute-time measurements** for all methods in Table 1 to substantiate or correct the "roughly FLOPs-matched" claim. This is the single most impactful improvement.

2. **Add at least one pause-token baseline** at the same forking layers (3, 7, 11) with the same budget κ. This directly tests whether adaptivity — rather than simply adding more residual streams — drives the gains.

3. **Report results from at least 2–3 random seeds** with standard deviations, especially for the downstream task evaluations where improvements are small.

4. **Include a multi-step reasoning evaluation** — even a simple synthetic one (modular addition, parity) or a small-scale GSM8k evaluation at 772M — to align the evaluation with the paper's framing.

5. **Clarify how parameter-matching is achieved** between the baseline transformer and Thoughtbubbles in the main paper or a clearly referenced appendix.

## Score and Decision

**Calibration anchors considered:**

| Anchor | File | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| CoTFormer | 7igPXQFupX.md | 5.75 | R1 | Yes | Similar weakness profile (FLOPs analysis, baseline comparison concerns). Our paper has stronger strengths (+5.28 vs +4.79) but also stronger weaknesses (-4.56 vs -3.35). |
| Learning How Hard to Think | 6qUUgw9bAZ.md | 6.50 | R1 | Yes | About adaptive test-time compute (different setting). Similar baseline weakness (-4.63). Our strengths are higher but evaluation scope is narrower. |
| Perplexed by Perplexity | 1GTARJhxtq.md | 5.75 | R1 | Yes | About data pruning, not architecture. Less relevant topically. |
| Adaptive & Modularity | tI3eqOV6Yt.md | 5.00 | R2 | No | About adaptive computation on synthetic tasks. Less strong empirical results. |
| Autoregressive Mamba Vision | PQpvhUrA1C.md | 5.75 | R2 | No | Different architecture domain (vision). |

**Bracket:** Round 1 established the plausible range as 4.5–6.5. Round 2 narrowed to 5.0–6.0.

**Weight comparison:** Our draft's strongest positive (+5.28 for the 319M-outperforms-772M result) exceeds the strongest positive of CoTFormer (+4.79) and Learning How Hard to Think (+4.62). However, our strongest negative (-4.56 for missing pause-token baselines) is comparable to Learning How Hard to Think's strongest negative (-4.63) and notably worse than CoTFormer's strongest negative (-3.35). The consistency of perplexity improvements across all 12 settings is a genuine strength that CoTFormer and similar papers do not match, but the evaluation gaps (particularly no FLOPs analysis and no pause-token baselines) prevent the paper from exceeding the 5.5–6.0 band. The paper sits between CoTFormer (5.75) and a mid-range paper; the novel mechanism and consistent perplexity results justify a borderline accept, but the evaluation gaps require addressing before the paper can be considered a strong accept.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>