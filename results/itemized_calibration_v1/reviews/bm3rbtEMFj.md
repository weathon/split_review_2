Now let me compile the final review.

## Summary

ELMUR proposes a transformer architecture augmented with layer-local external memory for long-horizon decision-making under partial observability. Each layer maintains persistent memory embeddings, interacts with tokens via dedicated bidirectional cross-attention (mem2tok read, tok2mem write), and updates them through an LRU-based mechanism with convex blending. Evaluated on T-Maze (100% success up to 1M steps), MIKASA-Robo (best on 21/23 tasks, ~70% aggregate improvement), and POPGym (best aggregate on 48 tasks), the paper demonstrates that structured per-layer external memory substantially extends effective retention horizons.

## Strengths

1. **Strong T-Maze result (Section 5.2, Figure 3).** ELMUR achieves 100% success on corridors up to one million steps with only L=10 context and S=3 training segments. Eight baselines (RMT, DT, BC-LSTM, RATE, TrXL, DMamba, BC-MLP, persistent/random) all degrade sharply. This cleanly validates the memory mechanism.

2. **Compelling MIKASA-Robo results (Table 1).** On TakeItBack-v0, ELMUR scores 0.78±0.03 vs. next-best RATE at 0.42±0.24. On RememberColor3-v0, 0.89±0.07 vs. 0.65±0.04. These are large, statistically clear improvements on visual robotic manipulation with sparse rewards.

3. **Clean architecture design (Section 3).** The separation into token and memory tracks, mem2tok/tok2mem cross-attention with reversed relative biases, and LRU management are well-motivated. Algorithms 1 and 2 provide sufficient detail for reproduction. Design decisions connect to specific failure modes in prior work (quadratic cost, truncation, forgetting).

4. **Informative ablation study (Table 3, Figure 6).** Removing LRU drops success from 1.00 to 0.43; shared memory drops to 0.45; removing both drops to 0.22. The M vs. N analysis shows the memory bottleneck is the binding constraint. MoE→MLP preserves performance (1.00), confirming the memory mechanism (not the FFN choice) drives gains.

## Weaknesses

### Fatal
None.

### Major

1. **MIKASA-Robo task-count inconsistency.** The abstract and main text state "21 out of 23 tasks" (lines 9, 27), while Table 1's caption says "See results for all 32 MIKASA-Robo tasks in Appendix, Table 8" (line 236). This is a concrete numerical inconsistency — 23 vs. 32 — that undermines confidence in the reported aggregate statistics. Without the appendix, it is unclear whether the "best on 21/23" and "~70% aggregate improvement" claims are computed over 23 or 32 tasks, or what the relationship between these two numbers is. The authors must clarify this.

2. **Detached-memory limitation not discussed (Section 3).** The paper correctly notes that memory is detached via `sg(m)` (line 82), meaning gradients from the current segment do not flow back through memory to previous segments. This prevents end-to-end credit assignment across segments — the model cannot learn to write better memory representations from supervision that spans segments. This is a known limitation shared with Transformer-XL, but the paper does not acknowledge it or analyze its practical impact. A probing analysis (e.g., decoding memory embeddings to predict stored information) would substantially strengthen the claim that memory is semantically meaningful rather than a learned residual connection.

### Minor

1. **The "100,000×" headline claim has a slightly inflated denominator.** The claim (1,000,000 / 10 = 100,000×) uses the per-segment context L=10, but the model processes S=3 segments during training (30 tokens total trajectory). Computing against the total-per-training-trajectory gives ~33,333×. The 100,000× figure is technically correct as "beyond the per-segment attention window," but using it as the headline number (abstract, introduction, conclusion) without clarifying the denominator is a misleading framing. (The 33,333× figure is still impressive and would not weaken the paper.)

2. **Theoretical analysis is elementary (Section 4).** Proposition 1 (exponential forgetting) is a direct arithmetic consequence of the convex update rule; Proposition 2 (memory boundedness) states that convex combinations of norm-bounded vectors stay within the same ball — a trivial property. The effective horizon formula H(ε) = M·L·ln(ε)/ln(1-λ) is practically useful but follows directly from exponential decay. These are correctly stated but presented with formal-theorem apparatus that oversells them. The paper would be stronger stating these as observations.

3. **POPGym framing is modestly optimistic.** ELMUR is first on 24 of 48 tasks (exactly half), not "more than half" as the abstract implies. The aggregate improvement over RATE is 10.4 vs. 9.5 — positive but modest. On reactive tasks (15 of 48), ELMUR ties with multiple baselines (9.2 vs. 9.3 for DT). The paper would be more credible acknowledging that POPGym results are competitive with moderate advantages rather than dominant.

4. **D_max not reported.** The relative bias mechanism (Eq. 6–7) uses a learned embedding table of size (2D_max−1)×H, but D_max is never specified. This makes it impossible to assess the size of this table relative to the model.

5. **Generalization experiment (RQ2, Figure 4) lacks baselines.** The experiment shows ELMUR generalizes across lengths (100% on all train/test pairs), but no baselines are evaluated in the same setup. We cannot tell whether this property is unique to ELMUR or shared by other methods.

### Trivial
- The MoE FFN is used but the ablation shows MoE→MLP gives identical performance (1.00). The paper acknowledges this, but the design choice is not justified for the RL setting.
- σ (memory initialization) sensitivity is only evaluated in one ablation plot (Figure 6b).

## Nice-to-Haves
- Add a memory-probing analysis (e.g., linear probes on memory embeddings to predict stored task-relevant information).
- Include baselines in the RQ2 generalization experiment.
- Provide cost-vs-sequence-length scaling analysis for computational efficiency claims.
- Compare against memory only at the final layer to isolate whether per-layer memory is needed.

## Removed Points
These points are flagged to be removed; treat them with caution:
- **MoE design choice nitpick** — The reviewer criticized the MoE choice for being unjustified, but the paper's ablation shows it does not hurt performance, and this is acknowledged in the paper.
- **"No comparison with a simple baseline: memory only at the final layer"** — This is a nice-to-have rather than a weakness; the ablation already tests "shared memory" and per-layer memory shows clear benefits.
- **"Computational efficiency comparison lacks scaling analysis"** — This is a reasonable suggestion but not a core weakness; the paper reports wall-clock time for the main configuration tested.
- **"No analysis of σ beyond one ablation plot"** — The paper does include one ablation; this is a minor point that could be expanded but is not a weakness per se.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Resolve the 23 vs. 32 inconsistency — clarify the task count and which tasks are included in the aggregate statistics.
2. Clarify the 100,000× denominator in the abstract and introduction.
3. Add a discussion of the detached-memory limitation and its implications for cross-segment credit assignment.
4. Tone down the theoretical section — present formulas as useful observations rather than formal theorems.
5. Adjust the POPGym framing to accurately describe the mixed results.
6. Report D_max in the hyperparameter table.

## Score and Decision

**Calibration anchor summary:**

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| Foundation Policies with Memory | 3.00 | R1 | Yes | Much weaker; trivial architecture, weak baselines, overclaimed. ELMUR is clearly stronger. |
| Recurrent Action Transformer (RATE) | 4.75 | R1 | Yes | This is ELMUR's baseline. ELMUR has a more novel architecture and stronger results across the board. |
| Recurrent Linear Transformers | 4.75 | R2 | Yes | Different paper type (model efficiency). Missing baselines, unclear motivation. ELMUR is stronger empirically. |
| Think Before You Act (DT-Mem) | 5.75 | R1 | Yes | Similar topic (memory-augmented DT). ELMUR has stronger T-Maze and MIKASA results but similar-level POPGym gains. Comparable quality. |
| POMDP Theory (OSI) | 5.75 | R2 | No | Different paper type (theory). Not directly comparable. |
| Stable Hadamard Memory (SHM) | 6.50 | R1 | Yes | Most comparable. Accepted paper with strong theory and results. ELMUR has stronger T-Maze/MIKASA results but weaker theory and a concrete data inconsistency (23 vs. 32) that SHM did not have. |

**Bracket reasoning:** Round 1 bracketing placed ELMUR well above the 3.00–4.75 range (RATE and Foundation Policies are clearly weaker) and in the 5.75–6.50 range alongside DT-Mem and SHM. The weighted-item comparison shows ELMUR shares the "strong empirical results" and "informative ablations" high-weight positives with SHM (weight +4 each), but also shares the "incremental novelty concerns" negatives. The key differentiator is the concrete 23/32 data inconsistency, which is a higher-weight negative than any single weakness in SHM (SHM's heaviest negatives were -2 for novelty). This anchors ELMUR below SHM (6.50) but firmly above RATE (4.75) and DT-Mem (5.75) given the stronger T-Maze and MIKASA evidence.

**Final score: 6.0.** This is a borderline accept. The core contribution — per-layer external memory with dedicated cross-attention and LRU management — is well-designed and convincingly validated on T-Maze and MIKASA-Robo. The weaknesses (data inconsistency, framing issues, elementary theory) are addressable and do not invalidate the core claims, but they reduce the paper's rigor and need to be resolved in a revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>