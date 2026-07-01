Now I have all the information needed. Let me write the consolidated review.

## Summary

This paper introduces TNT (Two-stage Non-linear Training), a training paradigm for deep memory modules (e.g., Titans, TTT) that decouples training efficiency from inference performance. The core idea is a hierarchical memory: a global memory operating on large hardware-friendly chunks for long-range context, plus parallel local memories with periodic state resets that break sequential dependencies and enable context parallelism for non-linear RNNs. A second fine-tuning stage adapts local memories to smaller chunk sizes. Experiments on 150M-parameter Titans models show up to 17.37× training speedup while improving perplexity.

## Strengths

1. **The periodic reset mechanism is a clean, principled solution to a real bottleneck.** Deep memory modules (Titans, TTT) suffer from poor training throughput because small chunk sizes fail to saturate hardware. Breaking sequential dependencies by resetting local memory states to a shared learned \(W_{\text{init}}\) at shard boundaries (Eq. 6) is a simple idea that directly enables context parallelism for non-linear RNNs — something previously unavailable outside linear RNNs with parallel scans. The paper convincingly identifies and diagnoses the tension (Section 3, Challenges 1 and 3; Figure 2).

2. **Compelling speedup results with quality maintained.** Table 1 shows TNT reaching a target loss 17.37× faster than the Titans baseline (C=8), and 7.68× faster even with the *same* chunk size of 8. Figure 4 demonstrates linear wall-clock scaling with sequence length. Crucially, the speed improvements do not come at the cost of quality: TNT Stage 1 with a single local memory (N=1, C_L={8}) achieves 21.04 PPL vs. the best Titans configuration at 25.07 PPL (Table 2) — a meaningful gap.

3. **The hierarchical memory design is flexible and well-motivated.** Using a global memory (C_G=2048) for long-range context alongside local memories with periodic resets cleanly resolves the tension between hardware efficiency and fine-grained memorization. The ablation (Table 3) confirms that both the global memory (removal raises PPL from 21.04→25.60) and the Q-K Projection (removal raises PPL from 21.04→22.01) contribute positively.

## Weaknesses

### Major

1. **Stage 2 fine-tuning provides marginal improvements, undercutting the two-stage headline framing.** The paper presents the two-stage design as a key contribution (title, abstract, Section 4.2), with Stage 2 framed as resolving Challenge 3. However, the actual improvements are:
   - Best Stage 1 average perplexity: **23.13** → Best Stage 2: **23.09** (Δ = −0.04).
   - The absolute best per-dataset scores (C4: 20.15, FineWeb: 20.17, PG19: 29.08) are all from *Stage 1*, not Stage 2.
   - Common-sense reasoning accuracy is essentially identical (Stage 1 best 41.0% vs. Stage 2 best 40.9%).
   
   A 0.04-point perplexity improvement with no reported variance (see below) is within the noise of a single training run. The claim that Stage 2 "consistently lowers the average perplexity" is true in a narrow sense (all four Stage 2 configs are weakly better than Stage 1 counterparts), but the practical significance is minimal. This weakness is grounded in Table 2 data: the two blocks of TNT results simply do not show a meaningful gap.

### Minor

2. **No statistical variance or significance reported anywhere.** Every perplexity and accuracy number in Tables 1, 2, and 3 is a single value with no error bars, no mention of multiple seeds, and no discussion of training noise. This is especially problematic for:
   - The Stage 2 improvements (~0.04 PPL), which could easily be run-to-run variation.
   - The ablation results (e.g., Q-K Projection removal: 22.01 vs. 21.04 PPL), where the magnitude is sufficient to be meaningful but single-run evidence is weaker than it could be.
   - The downstream accuracy comparisons (Table 2), where 1–2% differences are presented as meaningful without quantification.

3. **Abstract claims evaluation on TTT models, but experiments only instantiate TNT on Titans.** The abstract states: "Evaluated on Titans and TTT models, TNT achieves a substantial acceleration…" However, Section 5.1 says: "we instantiate it with a strong deep memory model, Titans, to demonstrate its effectiveness." TTT appears only as a *baseline* in Table 2 (a standard TTT model, not TNT applied to TTT). No results show TNT applied to the TTT architecture. This is a discrepancy between the stated scope and the experimental validation, and should be corrected.

4. **The Q-K Projection mechanism lacks direct validation.** The paper argues (Challenge 2, Section 4.1.2) that during compression \(f(W,\cdot)\) learns to map keys to values, and at retrieval it is fed queries instead, causing a "domain mismatch." The proposed fix projects \(q_t\) onto the subspace spanned by keys in the current local chunk. However:
   - The projection is computed over only 8–16 tokens (the local chunk size \(C_L\)), which is a very small window — projecting onto such a tiny subspace seems unlikely to meaningfully bridge a learned representation gap.
   - The ablation (removing Q-K Projection: PPL 21.04→22.01) shows that *something* in this component helps, but does not isolate whether the benefit comes from the specific projection mechanism or from an incidental effect (e.g., local smoothing, an additional non-linear transform). The paper's theoretical motivation for this component is not backed by evidence that directly tests the claimed mechanism.

### Trivial

5. **The 1.3× speedup claim against FlashAttention doesn't cleanly match Figure 4.** The text says "with \(C_L = \{128\}\), TNT is \(1.3\times\) faster than the highly optimized FlashAttention kernel." From the Figure 4 table: at 32K, FlashAttention ≈1000ms vs TNT(C_L=128) ≈550ms → ~1.82×; at 16K, ~600ms vs ~500ms → ~1.2×. The claimed 1.3× does not correspond to any row. The text should specify which sequence length this refers to, or the numbers should be reconciled.

## Nice-to-Haves

- **A breakdown of where the speedup comes from.** The 17× end-to-end speedup (Table 1) could be decomposed into contributions from context parallelism vs. the larger global chunk size vs. other factors. This would help readers understand which architectural decisions drive the gains.
- **Results at a larger model scale (e.g., 1B+).** The paper's claims about resolving training bottlenecks for "truly long sequences" would be strengthened by showing the method works at scales beyond 150M. This is not a core flaw — the experiments are well-executed at the chosen scale — but scaling results would substantially raise impact.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Parameter-matched comparison is unfair"**: The reviewer argued that TNT's use of multiple memory modules (1 global + N local) vs. Titans' single memory module constitutes "more capacity" at the same 150M parameter count. However, at a fixed total parameter budget, adding memory modules means each module is individually smaller — it is a different allocation, not unambiguously "more capacity." Moreover, the N=1 TNT comparison (21.04 vs. 25.07 PPL, Table 2) already supports the core claim, and the reviewer acknowledges this. This criticism does not hold up as a weakness.
- **"Challenge 2 is not clearly distinguished from standard encoder-decoder setups"**: The reviewer's comparison to standard attention is not directly applicable. In this architecture, the function \(f(W,\cdot)\) is trained during compression to map *keys* to values, and then during retrieval it receives *queries* as input. This is architecturally specific and different from attention, where both q and k are used together in the score computation.
- **Q-K Projection computational cost**: The paper already explains the constant-size running-sum state (d×d). This is not a genuine weakness.
- **"No scaling study"**: Requesting 1B+ experiments is scope creep for a well-executed 150M study.
- **"No results on TTT architecture"**: This was merged into Minor Weakness #3 above as an abstract claim discrepancy, not a missing experiment.
- **Generic formatting/style nitpicks**: Removed per filtering rules.

## Novel Insights

None beyond the paper's own contributions. The harsh reviewer's insights essentially mirror what the paper itself demonstrates: the periodic reset mechanism works, the speedups are large, and Stage 2 is weak. The Q-K Projection concern (weak mechanism validation) is the one genuinely novel critical observation not fully surfaced by the paper's own narrative.

## Suggestions

1. **Either strengthen Stage 2 or reframe the contribution.** If Stage 2 cannot be shown to produce clearly beyond-noise improvements (e.g., with error bars across multiple seeds), consider presenting it as a practical suggestion rather than a headline contribution. The current two-stage framing overpromises relative to the evidence in Table 2.

2. **Add statistical grounding.** Report results with at least 2–3 seeds, or provide error bars for the main experiments. This is especially important for the Stage 2 results and the ablation study.

3. **Correct the abstract.** Change "Evaluated on Titans and TTT models" to reflect that TNT is instantiated on Titans, with TTT as a baseline (unless TNT-on-TTT experiments are added).

4. **Provide direct evidence for the Q-K Projection mechanism.** Either measure the distributional mismatch between q and k (e.g., cosine similarity), or add an ablation that controls for incidental effects (e.g., replacing the projection with a simple learned linear layer) to isolate the specific benefit of projecting onto the key subspace.

5. **Reconcile the 1.3× speedup claim** with the Figure 4 table values, or specify which sequence length is being referenced.

## Score and Decision

The core contribution — hierarchical memory with periodic state resets enabling context parallelism for non-linear deep memory modules — is well-motivated, cleanly implemented, and convincingly supported by the speedup results (Table 1, Figure 4) and quality metrics (Table 2, N=1 comparison). This is a genuine advance. However, the paper overclaims in two important ways: Stage 2 is treated as a headline contribution when its improvements are marginal and within noise range, and the abstract overstates the architectural scope of the evaluation. The Q-K Projection mechanism is empirically helpful but its stated motivation is not directly validated. These issues are addressable but lower the paper's overall strength.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>