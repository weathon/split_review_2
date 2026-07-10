Now I have the scoring model's assessment. All four strengths score 1.00 (strongly positive), and the weaknesses range from 0.00 (theoretical overclaim) to 0.37 (encoder details). The model confirms that the theoretical overclaim and MoE inconsistency are the most damaging points, while the strengths are uniformly strong. This paper has a real contribution but needs honest reframing.

Let me compose the final review.

---

## Summary

ELMUR proposes a transformer architecture augmented with per-layer external memory, using bidirectional token-memory cross-attention and an LRU-based update rule with convex blending. The method is evaluated on T-Maze (long-horizon synthetic), MIKASA-Robo (visual manipulation), and POPGym (puzzles/control), achieving 100% success on T-Maze corridors up to 1M steps and strong results on several robotics and puzzle benchmarks.

## Strengths

- **Clean architecture with well-motivated design.** The separation into token track and memory track per layer with dedicated cross-attention for read (mem2tok) and write (tok2mem) is conceptually simple. The LRU-based memory management with convex blending (full replacement while slots are empty, blending afterward) is a natural and practical policy, clearly described in Algorithm 1 and Figures 1–2.

- **100% success on T-Maze at 1M steps (Figure 3).** This result is clean and unambiguous. With only L=10 tokens of attention and S=3 segments during training, ELMUR achieves perfect retention across corridors up to one million steps — 100,000× beyond its attention window. Even RATE (which also has memory) drops to ~0.7.

- **Strong generalization across sequence lengths (Figure 4).** The heatmap showing perfect transfer across all 7 training × 11 validation length combinations — including extrapolation to sequences much longer than training — rules out the concern that the model simply memorizes fixed-length patterns.

- **Thorough ablation study (Table 3, Figure 6).** The ablation cleanly isolates the contribution of each component: removing LRU drops performance to 0.43±0.22 (high variance), removing both LRU and relative bias to 0.22±0.11, while replacing MoE with MLP has zero effect on accuracy. The analysis of memory capacity (M ≥ N vs. M < N) in Figure 6 is informative and practically useful.

## Weaknesses

### Fatal
None.

### Major

- **Overclaimed theoretical contribution (Section 4).** The paper lists "We provide a theoretical analysis of LRU-based memory dynamics, establishing formal bounds on forgetting, retention horizons, and stability" as a contribution. In reality, Proposition 1 is simply the closed-form expansion of the convex blending update (exponential moving average), and Proposition 2 shows that convex combinations of bounded vectors remain bounded. Both are straightforward consequences of the update rule's definition. This is basic algebra, not a theoretical analysis. The section should be renamed to "Properties of the LRU Update Rule" and the results honestly characterized as basic algebraic consequences. The half-life and boundedness results are useful sanity checks, not theorems. This does not invalidate the empirical contributions but the mismatch between claim and content is significant.

### Minor

- **Selective framing in the abstract and introduction.** The "nearly doubles" claim on MIKASA-Robo is driven heavily by TakeItBack (0.78 vs 0.42, ~1.86×) and RememberColor3 (0.89 vs 0.65, ~1.37×), but on harder tasks (RememberColor5: 0.19 vs 0.13; RememberColor9: 0.23 vs 0.17) the advantage narrows to 6 percentage points with overlapping error bars. The paper honestly reports these numbers in Table 1, but the abstract selects the most impressive comparison point. Similarly, ELMUR is slightly below DT on POPGym reactive tasks (9.2 vs 9.3) and ranks first on only 24 of 48 tasks — meaning not-first on the other 24. The paper would be stronger if it presented a more balanced summary up front.

- **Observation encoder not specified in the main text.** Algorithm 1 says `h ← ObsEncoder(o)` with no architecture, input resolution, or pretraining details. For vision-based manipulation (MIKASA-Robo), the encoder choice heavily influences results, and parameter counts of ~2.1M seem very small for a transformer processing pixel inputs. This leaves the robotics results incompletely reproducible from the main text. (The details likely exist in the appendix, but the encoder architecture is central enough to warrant inclusion in the main paper.)

- **MoE motivation inconsistent with ablation findings.** The method section (line 92) motivates the DeepSeek-MoE FFN over a standard MLP, claiming improvements in parameter efficiency and specialization. However, the ablation (Table 3) shows MoE→MLP yields identical accuracy (1.00±0.00 in both cases). The paper acknowledges this in the ablation section but does not reconcile it with the earlier motivation. If MLP works identically, the MoE choice should be presented as an efficiency decision, not a performance one.

### Trivial
None.

## Nice-to-Haves

- Explain why λ ≈ 0.4–0.6 is unstable (Figure 6a). This is potentially the most practically useful finding in the ablation — does this range produce writes that are neither fully replacing nor sufficiently preserving, creating interference?
- Provide qualitative analysis of what individual memory slots store and whether different layers specialize to different types of information.

## Removed Points

These points were flagged by the input reviewer but are removed for the following reasons:

1. *"Effective horizon formula assumes uniform random selection vs. deterministic LRU"* — Factually incorrect. With LRU deterministically selecting the oldest slot, each slot IS overwritten exactly once per M segments. The formula is exact, not approximate.
2. *"Only 4 of 23 MIKASA-Robo tasks in main paper"* — The full table is referenced to the appendix (standard practice); this is a complaint about appendix-stripped content.
3. *"No comparison to TrXL on MIKASA-Robo"* — RATE is a more recent and relevant memory-augmented baseline; TrXL is included on T-Maze. Not a critical omission.
4. *"No analysis of what memory stores"* — Nice-to-have qualitative analysis, not a required weakness.
5. *"Algorithm ordering not ablated"* — Design choice; no evidence presented that alternative orderings would be better.
6. *"CartPole ceiling effect"* — Ceiling effect on a simple sanity check is trivially acknowledged by the paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Rewrite Section 4 to honestly characterize the algebraic properties as basic consequences of the convex blending rule, not as a "theoretical analysis."
2. Add the visual encoder specification (architecture, resolution, pretraining) to the main paper.
3. Present a more balanced summary in the abstract that acknowledges the narrow lead on harder MIKASA-Robo tasks and the mixed POPGym reactive results.
4. Reconcile the MoE motivation in Section 3 with the ablation finding that MLP-FFN achieves identical accuracy.
5. Offer a hypothesis for the λ ≈ 0.4–0.6 instability observed in Figure 6a.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>