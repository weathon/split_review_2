## Summary

TNT introduces a two-stage training framework for deep memory modules (like Titans) that decouples training efficiency from inference performance. Stage 1 uses a hierarchical memory architecture with a global memory (large chunks) and multiple parallel local memories (small chunks) with periodic resets (Eq. 6) to break sequential dependencies, enabling context parallelism for non-linear recurrences—a long-standing challenge. Stage 2 fine-tunes local memories to smaller chunk sizes for inference. On a 150M-parameter Titans model trained on 10B tokens, TNT achieves up to 17× faster training to target loss while improving perplexity over the Titans baseline (23.13 vs. 25.07).

## Strengths

1. **Well-motivated problem.** Section 3 clearly identifies the real bottleneck: deep memory modules require small chunk sizes for accuracy but achieve only 5–10% FLOPs utilization (Zhang et al., 2025). The paper correctly diagnoses the tension between training efficiency and inference performance.

2. **The periodic reset idea is clean and compelling.** Equation (6) formalizes a simple mechanism—reset to a learned $W_{\text{init}}$ every $S_L$ tokens—that genuinely breaks sequential dependency across shards, enabling true context parallelism for non-linear recurrences. This is a clever, practical solution to a well-documented open problem.

3. **Informative ablation study (Table 3).** The ablation separately isolates the effect of the global memory (removing it raises PPL from 21.04 to 25.60—worse than baseline Titans at 23.53), the Q-K projection (removing it raises PPL to 22.01), and Stage 2 fine-tuning. This provides transparent evidence about which components matter.

## Weaknesses

### Major

1. **Generality claim is unsubstantiated.** The abstract states "Evaluated on Titans and TTT models" (line 9) and the paper positions TNT as "a general training paradigm applicable to any deep memory module" (line 35). However, TNT is only instantiated on Titans (line 201: "we instantiate it with a strong deep memory model, Titans"). TTT appears only as a baseline in Table 2, not as a host architecture for TNT. This central claim of cross-architecture generality is unsupported by evidence. The paper should either add a TTT-on-TNT experiment or appropriately scope the claim.

2. **Stage 2 fine-tuning benefit is marginal and the $C'_L=1$ goal is not achieved.** The best Stage 2 perplexity (23.09, Table 2 line 264) improves over the best Stage 1 perplexity (23.13, line 259) by only 0.04—well within likely noise for a 150M model. More concerning, the stated goal of enabling $C'_L=1$ inference (line 197: "specializes the model for the ideal inference scenario: a local chunk size of one") yields PPL 23.99, which is *worse* than the Stage 1 best of 23.13. This undermines a stated objective of the framework.

### Minor

3. **Challenge 2 motivation is weakly supported.** The paper frames the query–key separation in deep memory modules as a "domain mismatch" (lines 92–112) that "violates the intended input domain of the learned function." However, query–key separation is standard across attention-based architectures and the network is trained end-to-end with both roles. The Q-K projection improves PPL (Table 3: 21.04 → 22.01 without it), but this improvement could reflect increased expressiveness from the additional linear transformation rather than specifically resolving a domain mismatch. The paper does not test a simpler alternative (e.g., a learned linear projection of $q$ without the $kk^\top$ form).

4. **Sensitivity to the reset interval $S_L$ is not explored.** The paper uses $S_L=2048$ or $S_L=4096$ (line 209) without justification or sensitivity analysis. This hyperparameter governs the core parallelism-vs-context-length trade-off of the key mechanism; a sweep across values would clarify its role.

5. **No variance or confidence intervals reported.** Table 2 reports single numbers per configuration. Given the small model size (150M) and known training variance, the 0.04 PPL difference between Stage 1 and Stage 2 best could easily fall within noise.

### Trivial

6. **Speedup framing.** The "up to 17.37×" speedup in Table 1 compares the fastest TNT ($C_L=64$, 1.12 hrs) against the slowest Titans configuration ($C=8$, 19.48 hrs). This is correctly labeled as "compared to the most accurate baseline configuration," but equal-chunk-size comparisons (e.g., $C_L=8$ vs $C=8$: 7.68×) give a more conservative picture.

## Nice-to-Haves

- Evaluate TNT on at least one additional deep memory architecture (e.g., TTT) to substantiate the generality claim, or scope the claim to Titans.
- Report inference throughput/latency for the $C'_L=1$ scenario, since the paper claims this is the "ideal inference scenario" (line 197).
- Analyze the $O(d^2)$ computational overhead of the Q-K projection (Eq. 7) for large $d$, as this matrix grows quadratically with hidden dimension.

## Removed Points

- **Capacity confound (Issue 1 from Harsh Critic).** The critic claimed TNT has "strictly more parameters" than Titans. This is factually incorrect: the paper explicitly states all models are 150M parameters (line 207, Table 2 header). Both TNT and Titans baselines are controlled at equal total parameter count. The critic's sub-point about FLOPs differences from Q-K projection is retained as a Nice-to-Have.
- **Criticism that "w/o global memory" being worse than baseline Titans.** The paper already acknowledges this transparently (line 270: "confirming its critical role"). This is honest reporting, not a weakness.
- **All appendix-related criticisms removed per hard rules** (the parser strips appendices; they exist in the original submission).
- **All formatting, typography, and readability nitpicks removed per hard rules** (parser artifacts).

## Novel Insights

The periodic reset mechanism for local memory states (Eq. 6) combined with a compensating global memory module provides a clean, practical solution to parallelizing non-linear recurrences during training. Unlike prior work that either circumvents the problem with local attention (Zhang et al., 2025) or restricts to linear recurrences (Guo et al., 2025), TNT directly breaks sequential dependencies while recovering long-range context through the global module. The ablation confirms that this design is internally consistent: without the global memory the reset mechanism destroys performance (25.60 PPL), but with it the full system substantially outperforms the baseline. This internal coherence strengthens the paper's credibility despite its evaluation limitations.

## Suggestions

1. Correct the abstract: replace "Evaluated on Titans and TTT models" with "Evaluated on Titans" unless TTT experiments are added.
2. Provide a sensitivity analysis of $S_L$ (e.g., 512, 1024, 2048, 4096, 8192) to clarify the parallelism-vs-context-length trade-off.
3. Add confidence intervals or standard errors for key perplexity numbers, especially for Stage 2 comparisons against Stage 1.
4. Acknowledge the marginal Stage 2 improvement and the failure to achieve $C'_L=1$ without accuracy loss, or provide evidence that addresses these gaps.

## Score and Decision

**Round-1 bracket:** 5.5 – 7.5 (based on calibration against similar papers on parallelizing sequential models and hierarchical memory).

**Anchor papers used in calibration:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `Parallelizing non-linear sequential models...` (E34AlVLN0v) | 6.00 | R1 | Similar problem (parallelizing non-linear sequential models). TNT has cleaner architectural solution and larger-scale evaluation. |
| `FlashRNN: I/O-Aware Optimization...` (l0ZzTvPfTw) | 6.50 | R1 | Hardware optimization for RNNs. Different approach but comparable contribution quality. |
| `Were RNNs All We Needed?` (GrmFFxGnOR) | 5.00 | R1 | Less novel (known parallelization technique), smaller experiments. TNT is stronger in both novelty and evaluation scale. |
| `AutoChunk: Automated Activation Chunk...` (GQGNLEHmdl) | 6.33 | R1 | Different domain (activation memory for inference) but comparable paper quality. |
| `MELODI: Exploring Memory Compression...` (TvGPP8i18S) | 6.25 | R1 | Hierarchical memory compression, similar architectural philosophy. Comparable quality. |
| `Hierarchical Context Merging...` (ulaUJFd96G) | 6.25 | R1 | Hierarchical chunk-based processing for LLM context. Comparable quality. |

The paper sits above "Were RNNs All We Needed?" (5.0) due to genuine novelty and larger-scale evaluation, and is comparable to "Parallelizing non-linear sequential models" (6.0) and "FlashRNN" (6.5). The overclaimed generality and marginal Stage 2 benefits prevent a score at the "accept" level (8.0), but the core periodic-reset contribution is valuable enough to warrant publication.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>