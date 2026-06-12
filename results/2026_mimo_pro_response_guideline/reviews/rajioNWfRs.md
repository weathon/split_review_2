Now I have enough information to calibrate. Let me finalize my review.

**Calibration Summary:**
- "Parallelizing non-linear sequential models" (6.0, Accept): Very similar topic — parallelizing non-linear RNNs. Accepted at 6.0 with similar limitations (limited scaling, practical importance unclear).
- "FlashRNN" (6.5, Accept): Hardware-optimized RNNs with 50× speedups over PyTorch. Accepted at 6.5.
- "Were RNNs All We Needed?" (5.0, Reject): Simplifying RNNs for parallel training. Rejected at 5.0 with limited scale experiments and insufficient comparisons.
- "Retentive Network" (4.75, Reject): Training parallelism + efficient inference. Rejected at 4.75 with novelty concerns.
- "Oscillatory SSMs" (8.0, Accept): Strong theoretical + broad empirical contribution.
- "SAD3-LM" (8.0, Accept): Strong empirical results on language modeling.

**Initial bracket:** TNT sits between 5.5 and 6.5. It has a cleaner story and better ablations than "Were RNNs All We Needed?" (5.0) but lacks the hardware-level optimization depth of FlashRNN (6.5) or the theoretical rigor of the 8.0 papers. The 150M limitation and abstract inconsistency hold it back. I place it at **6.0**, comparable to "Parallelizing non-linear sequential models."

---

## Summary
This paper introduces TNT (Two-stage Non-linear Training), a training paradigm for deep memory modules that resolves the tension between training efficiency and inference performance. Stage 1 uses hierarchical memory (global memory on large chunks + parallel local memory modules with periodic state resets) to maximize training throughput via context parallelism; Stage 2 fine-tunes with smaller chunksizes for optimal inference. A Q-K Projection mechanism addresses domain mismatch between memory compression and retrieval. TNT reports up to 17× training speedup over baseline Titans while improving perplexity, evaluated at 150M parameters.

## Strengths
- **Well-motivated problem decomposition with empirical grounding**: The paper identifies three specific challenges (compression-retrieval mismatch, chunksize efficiency-performance tradeoff, train-test chunksize mismatch), each illustrated with concrete evidence. Figure 2 clearly demonstrates that a 550M Titans model achieves optimal perplexity only when inference chunksize matches training (PPL 13.78 at C=64 vs. 36.45 at C=8).

- **Novel hierarchical memory with periodic state resets (Eq. 5-6)**: The core innovation — resetting local memory states to a shared learnable initialization at segment boundaries — breaks sequential dependencies, enabling context parallelization for non-linear recurrences. Ablation in Table 3 confirms: removing global memory increases PPL from 21.04 to 25.60; incrementally adding local modules shows consistent improvement (21.04 → 20.74 → 20.47 → 20.15).

- **Effective Q-K Projection mechanism (Eq. 7)**: Addresses the compression-retrieval domain mismatch with a constant-size running state (sum of rank-1 operators maintained as a running sum). Ablation shows removal increases PPL from 21.04 to 22.01 and drops common-sense accuracy from 40.6% to 36.4%.

- **Substantial speedup with simultaneous quality improvement**: TNT achieves up to 17.37× speedup over the best-performing Titans baseline (C=8, reaching target loss 3.20) while achieving lower perplexity (23.13 vs 25.07 avg PPL in Table 2). Runtime scales linearly with sequence length (Figure 4), outperforming even FlashAttention at 32k context (550ms vs ~1000ms for TNT C_L=128).

- **Clean, systematic ablation study (Table 3)**: Each component (global memory, local memory modules, Q-K projection, Stage 2 fine-tuning) is validated through controlled removal experiments, providing clear evidence of individual contributions.

## Weaknesses

### Fatal
None

### Major
- **150M-only evaluation limits scalability confidence**: All experiments use 150M-parameter models trained on 10B tokens (line 207). The paper makes strong scalability claims ("removes a critical scalability barrier," line 278) but provides zero evidence these results hold at larger scales. At 150M, training is fast regardless, and the relative benefits of context parallelism may behave differently at 1B+ where communication costs, optimizer state sizes, and memory bandwidth become dominant factors. Compared to the anchor "Parallelizing non-linear sequential models" (6.0), which had a similar limitation, this is the primary factor constraining the score.

- **Abstract misrepresents TTT evaluation scope**: The abstract (line 9) states "Evaluated on Titans and TTT models," but TTT only appears as a comparison baseline in Table 2 (line 252), not as a model enhanced by TNT. The contributions section (line 46) honestly states "We validate TNT on the Titans architecture," contradicting the abstract. This inconsistency overstates the scope of validation and could mislead readers.

### Minor
- **17× headline speedup is Stage 1 only**: Table 1 reports Stage 1-only speedups. Stage 2 fine-tuning adds ~5% overhead (referenced Table 4 in appendix). The conclusion's "17× speedup compared to the most accurate RNN baselines" (line 278) blends speed and accuracy across different TNT configurations — the speed-optimized config (C_L={64}) and accuracy-optimized config (C_L={4,8,16,32}) are different setups.

- **Generality claim unsubstantiated beyond Titans**: Line 35 claims TNT is "applicable to any deep memory module" but validation is restricted to Titans only. Without results on at least one other architecture (e.g., Atlas, TTT-MLP), the generality claim remains theoretical.

- **Downstream task accuracy differences are small with no error bars**: At 150M, accuracy differences between models are modest (e.g., 41.0% vs 39.7% average) and the paper itself acknowledges "downstream task accuracy can be subject to higher variance" (line 238). Without error bars or significance tests, it's unclear if TNT's reasoning improvements are statistically meaningful.

### Trivial
None

## Nice-to-Haves
- Sensitivity analysis for shard size $S_L$ and learned initialization $W_{init}$, key hyperparameters of the reset mechanism.
- Analysis of information loss from periodic resets — how much does the model depend on global vs. local memory in the final output?
- Apply Q-K projection to global memory as well and compare, since the paper applies it only locally claiming local memory is "more sensitive to the mismatch" (line 160) but provides no evidence for this specific claim.
- Comparison against other parallelization approaches for non-linear RNNs (e.g., Gonzalez et al., 2024, which is cited but not compared to).

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Harsh critic's Q-K projection terminology nitpick**: The critic notes the projection "is not a proper orthogonal projection" but rather "an unnormalized sum of rank-1 projection operators." The mechanism is clearly defined in Eq. 7 and well-understood — each term $k_\tau k_\tau^\top / \|k_\tau\|^2$ is indeed a projection onto the key direction. The paper's description is slightly loose but not materially misleading.
- **Harsh critic's Transformer comparison framing**: The critic calls the Transformer comparison "somewhat unfair," but the paper explicitly acknowledges the kernel gap (line 233: "TNT currently lacks a custom kernel, which we leave for future work"). The comparison is informative and honestly presented.
- **Harsh critic's sensitivity analysis for $W_{init}$**: This is a nice-to-have, not a substantive weakness. The paper demonstrates the mechanism works; sensitivity analysis would strengthen understanding but doesn't undermine the contribution.

## Novel Insights
The periodic state reset mechanism for enabling context parallelism in non-linear recurrences is a genuinely novel and elegant contribution. The key insight — that a global memory module can compensate for the long-range information lost during resets — is non-obvious and well-executed. The identification of compression-retrieval domain mismatch (Challenge 2) as a fundamental issue in deep memory modules is also a valuable observation worth highlighting.

## Suggestions
- Add at least one experiment at 1B+ scale, even a single scaling point, to substantiate scalability claims.
- Apply TNT to a second deep memory module to validate the generality claim.
- Report error bars for downstream task accuracy.
- Clarify the 17× headline to include Stage 2 cost and distinguish speed-optimized from accuracy-optimized configurations.
- Reconcile the abstract's TTT evaluation claim with the actual scope (either add TTT experiments to the main paper or correct the abstract).

## Score and Decision

**Retrieved anchors across all rounds:**
| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| "Parallelizing non-linear sequential models" | 6.0 | 1 | Very similar topic; TNT has better ablations but similar scaling limitation |
| "FlashRNN" | 6.5 | 1 | Hardware-level optimization; TNT is higher-level training paradigm |
| "Were RNNs All We Needed?" | 5.0 | 1 | Similar RNN parallelization; TNT has cleaner story and better evidence |
| "Retentive Network" | 4.75 | 1 | Architecture paper; TNT has more focused contribution |
| "Oscillatory SSMs" | 8.0 | 1 | Strong theory + broad empirical validation; TNT lacks this depth |
| "SAD3-LM" | 8.0 | 1 | Strong empirical results; TNT limited to 150M scale |
| "ChunkKV" | 5.25 | 1 | Different topic; rejected at 5.25 |
| "ChunkAttention" | 4.50 | 1 | Different topic; rejected at 4.50 |
| "AutoChunk" | 6.33 | 1 | Memory optimization; accepted at 6.33 |

**Bracket:** 5.5–6.5, settling at **6.0**. TNT has a cleaner ablation story and more complete experimental design than papers rejected at 5.0, comparable technical depth to papers accepted at 6.0, but lacks the broader validation or theoretical depth of the 6.5+ papers. The 150M limitation and abstract inconsistency are the primary factors preventing a higher score.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>