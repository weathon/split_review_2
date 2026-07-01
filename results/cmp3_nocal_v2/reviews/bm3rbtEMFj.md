## Summary

ELMUR proposes a transformer architecture augmented with layer-local external memory that uses bidirectional cross-attention for read/write operations and an LRU-based update policy for bounded persistent storage. The method is evaluated across synthetic T-Maze tasks, robotic MIKASA-Robo manipulation tasks with visual observations, and the POPGym benchmark. It demonstrates 100% success on T-Maze corridors up to one million steps and achieves strong results on MIKASA-Robo, particularly on TakeItBack-v0 (0.78 vs. 0.42) and RememberColor3-v0 (0.89 vs. 0.65).

## Strengths

- **Clean, well-motivated architecture.** The design of layer-local persistent memory with dedicated `mem2tok` (read) and `tok2mem` (write) cross-attention paths, an LRU-based update mechanism, and segment-level recurrence is clearly explained (Algorithms 1 and 2). It avoids quadratic context extension costs while also avoiding the opacity of state compression in RNNs.

- **T-Maze results are compelling evidence for the core claim.** A 100% success rate up to corridors of one million steps with a context window of only L=10 and S=3 segments (Figure 3) cleanly demonstrates that the memory mechanism can retain information across extreme horizons under idealized conditions. This provides strong support for the paper's central claim about retention beyond the attention window.

- **MIKASA-Robo results provide meaningful robotic-domain evidence.** The results in Table 1 show clear improvements on TakeItBack-v0 (0.78 vs. 0.42 for RATE) and RememberColor3-v0 (0.89 vs. 0.65), both with non-overlapping error bars. These are the most convincing real-world results and show the architecture works with visual observations and continuous action spaces.

## Weaknesses

### Major

- **The theoretical analysis (Section 4) is overclaimed as a contribution.** Proposition 1 (Exponential Forgetting) simply unrolls the convex blending recurrence — it is an arithmetic consequence of the update rule without any structure specific to ELMUR. Proposition 2 (Memory Boundedness) states that convex combinations of vectors with norm ≤ C remain within the ball of radius C, which is a trivial property of convex sets. The paper lists this as a third contribution (line 33: "We provide a theoretical analysis … establishing formal bounds"), but the content is elementary and does not constitute a substantive theoretical contribution. The effective horizon formula (line 180) is a direct arithmetic consequence of the forgetting rate and the assumption that overwrites are evenly distributed — useful as a heuristic but not a theoretical result.

- **Transformer-XL is absent from the main comparison tables despite being the direct inspiration for the segment-level recurrence mechanism.** ELMUR's segment-level recurrence is explicitly compared to Transformer-XL (line 70: "Unlike architectures that simply cache hidden states (Dai et al., 2019)"), and TrXL appears in Figure 3 (T-Maze). However, TrXL is absent from the MIKASA-Robo and POPGym comparisons (Tables 1 and 2). Since the paper claims that *structured external memory* outperforms *cached hidden states*, omitting the method that represents the cached-hidden-state approach from the primary evaluation tables is a significant gap.

### Minor

- **Ablation study is conducted on a single task only (RememberColor3-v0, Table 3, Figure 6).** The key ablations (LRU removal, shared memory vs. layer-local, relative bias removal) are tested on one task with visual observations. Whether these component contributions generalize across the diversity of MIKASA-Robo or POPGym tasks is untested. This narrows the evidence for the design choices.

- **Full MIKASA-Robo results for the "21 of 23 tasks" and "70% aggregate improvement" claims are not in the main text.** The paper claims best results on 21 of 23 tasks and a 70% aggregate improvement over the previous best baseline, but only 4 of 23 tasks appear in Table 1. The remaining 19 tasks are relegated to the appendix (referenced as Table 8). A summary statistic (e.g., a bar chart, aggregate success row, or radar plot) in the main text would improve verifiability of these headline claims.

- **POPGym aggregate gains are modest and the "more than half" claim is borderline.** ELMUR scores 10.4 vs. RATE's 9.5 across all 48 tasks (a ~9% relative improvement). On the 15 reactive tasks, ELMUR (9.2) trails DT (9.3). The abstract states ELMUR "outperforms baselines on more than half of the tasks" (line 9), but the paper body says it "obtains the top score on 24 of 48 POPGym tasks" (line 27), which is exactly half. These results are positive but do not support a strong cross-domain robustness narrative.

- **Relative bias saturation for very distant memories is not discussed.** Offsets are clamped to \([-D_{\max}+1, D_{\max}-1]\) (line 118), so all memories older than the maximum bias range receive the same relative bias, losing temporal ordering information. For very long trajectories, this saturation could affect the model's ability to distinguish between old memories of different ages. The paper does not discuss this limitation or its practical impact.

### Trivial

- Line 29 says "Our contributions are twofold" but lists three bullet points immediately after. A minor inconsistency.

## Nice-to-Haves

- Include Transformer-XL (or a cached-hidden-state variant) in the MIKASA-Robo and POPGym comparisons to directly test whether the external memory design outperforms cached hidden states.
- Expand the ablation study to at least one additional MIKASA-Robo task (e.g., TakeItBack-v0) to confirm that the component contributions are not task-specific.
- Consider adding a summary row, bar chart, or radar plot in the main text for the full MIKASA-Robo leaderboard rather than sending all 19 remaining tasks to the appendix.

## Removed Points

These points were raised in the input review but are removed for the following reasons:

- **CQL/DP baseline fairness concern (Critique #1):** The critic speculates that CQL and Diffusion Policy are "likely operating outside their intended design regime" and that the "same data budgets" statement is "a red flag." The paper states that CQL is included as "a strong offline RL method" and DP as "a state-of-the-art generative policy" (line 202). The paper does not specify that they are trained with an IL-style loss — it only states they are trained under the same *data budgets and preprocessing*. Whether CQL and DP are appropriately tuned for this setting is a reasonable question for the authors, but the critic's framing of this as a likely misleading comparison is speculative and unsupported by evidence in the paper. **Removed.**

- **T-Maze being too simple to bear weight (Critique #5):** The critic argues T-Maze tests "only a single binary cue" and does not test multi-cue reasoning or interference. The paper uses T-Maze as a synthetic retention stress test for its stated purpose — measuring retention horizons — which it does directly and convincingly. The paper separately shows robotic results to demonstrate transfer to more complex settings. **Removed** — the T-Maze evaluation is appropriately scoped.

- **CartPole being too easy (Section-by-Section Notes):** The critic suggests a partially observable variant would be more informative. The paper uses CartPole as a sanity check that the memory mechanism does not break MDP performance, which is a reasonable and lightweight validation. **Removed** — this is a nice-to-have suggestion, not a weakness.

- **Missing code release verification (Missing Parts):** The paper references a URL (elmur-paper.github.io). Per guidelines, questioning the availability of cited resources is not a valid criticism. **Removed.**

## Novel Insights

The input review's observations can be summarized as: (i) the architecture is clean and well-motivated, (ii) the T-Maze results are the strongest evidence for the core retention claim, (iii) the theoretical analysis is elementary and overclaimed, and (iv) the Transformer-XL baseline omission is a meaningful gap given the paper's framing. Beyond what is already in the paper, no genuinely novel insight emerges from the reviews.

## Suggestions

1. Clarify the "nearly doubles" and "70% aggregate improvement" claims by including a full summary of MIKASA-Robo results (or at least a compact per-task leaderboard visualization) in the main text.
2. Add Transformer-XL (or an equivalent cached-hidden-state baseline) to the MIKASA-Robo and POPGym comparisons, or explicitly justify its exclusion.
3. Reframe the theoretical section (Section 4) honestly as an informal analysis of forgetting properties rather than claiming it as a "theoretical contribution" alongside the architecture and empirical results. Alternatively, expand it with non-trivial analysis (e.g., characterization of memory interference or capacity bounds under the LRU policy).
4. Expand the ablation to at least one additional task to improve generalizability of the component analysis.
5. Fix the "twofold" / three-item inconsistency in the contributions list.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>