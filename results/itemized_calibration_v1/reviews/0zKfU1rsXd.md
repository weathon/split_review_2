## Summary

This paper proposes AQER, an approximate quantum loader (AQL) that constructs loading circuits by progressively reducing entanglement. It contributes a unified framework for AQLs and an information-theoretic analysis (Theorem 3.1) connecting infidelity to an entanglement measure S. AQER consists of three steps: entanglement reduction via iterative addition of two-qubit gates (Step I), product state approximation via derived single-qubit rotations (Step II), and full parameter refinement (Step III). Experiments on classical datasets (MNIST, CIFAR-10, SST-2) and quantum datasets (S-RQC, GS-TFIM up to N=50) show AQER consistently outperforms existing AQL methods.

## Strengths

1. **Principled method design grounded in a theoretical link.** Theorem 3.1 provides a formal connection between infidelity and the entanglement measure S, showing infidelity scales linearly with S as S→0. AQER's Step I directly optimizes this quantity, giving a principled basis for circuit construction that goes beyond existing heuristic approaches. (Section 3.1, Theorem 3.1; Section 3.2, Step I)

2. **Consistent outperformance across diverse benchmarks.** Table 1 shows AQER achieves the lowest infidelity on all five datasets (MNIST, CIFAR-10, SST-2, S-RQC, GS-TFIM), often by large margins. On S-RQC at G≈80, AQER's infidelity is 0.067 vs. 0.367 for the next-best method (AQCE), a >5× improvement. On GS-TFIM at G≈80, AQER achieves 0.003 vs. 0.056 for AQCE. These are substantial, consistent improvements, not marginal gains. (Table 1)

3. **Scalability demonstrated up to 50 qubits on a physically relevant system.** The GS-TFIM experiments (Fig. 4b) show AQER maintains roughly constant infidelity across N=20–50 when T scales linearly as T=4N−40. The 50-qubit optimization curves (Fig. 4a) do not plateau at high infidelity, suggesting Step I's entanglement reduction places optimization in a favorable region of the parameter landscape. (Section 4.3, Fig. 4)

4. **Step II parameter derivation avoids a separate optimization loop.** Corollary 3.2 indicates single-qubit rotation parameters in Step II are explicitly computed rather than optimized, a practical efficiency advantage over methods that must train all parameters from scratch. (Section 3.2, Step II)

## Weaknesses

### Fatal
None.

### Major

1. **Theoretical bounds are quantitatively loose and their "information-theoretic" characterization is weaker than advertised.** Theorem 3.1's bounds have a factor-N gap: as S→0, the lower bound scales as (ln 2)/(2N)·S while the upper bound scales as (ln 2)/2·S. For N=50, the lower bound is near-zero for any plausible S while the upper bound predicts ≈ 0.35·S. This means the bounds cannot tightly constrain achievable infidelity for large systems — they are consistent with both excellent and poor performance for the same measured S. The paper's framing (contribution (i), lines 8–9, 22, 88) presents this as "information-theoretic bounds" and "fundamental limits," which overstates what the bounds deliver quantitatively. Furthermore, the bounds depend on S(U^†|ψ_target⟩), which involves the circuit U that AQER is trying to find — they are bounds on the relationship between a specific circuit's entanglement-reduction property and its resulting infidelity, not fundamental limits independent of the algorithm's output. The qualitative insight that "reducing S reduces infidelity" is useful and motivates the method well, but the quantitative bounds are too loose to be predictive. (Theorem 3.1, lines 86–88)

2. **Computational cost of Step I is opaque in the main text, undermining "scalable and efficient" claims.** At each iteration, AQER evaluates O(N²) qubit pairs, each requiring a Nelder–Mead optimization to minimize S. For N=50 and T=200, this is roughly 245,000 Nelder–Mead optimizations. The paper relegates time-complexity analysis to Appendix G (stripped by the parser) and only mentions that "evaluating and optimizing S is efficient" (line 116). Without a clear discussion of construction cost in the main text, readers cannot assess whether AQER's construction overhead is acceptable for its target use cases. The paper's claim of being "scalable and efficient" (title, abstract) is unsupported without this transparency. (Section 3.2, lines 116; Section 4.2, hyperparameter settings)

3. **Barren plateau claim is tested only on low-entanglement target states.** The paper claims AQER "mitigates barren plateau effects" (lines 24, 116, 183) and presents evidence from GS-TFIM at N=50 (Fig. 4a). However, 1D TFIM ground states obey an area law — they are low-entanglement by construction, and even standard variational circuits often avoid barren plateaus on such states. To support the claimed advantage, the method should be tested on genuinely entangled targets (e.g., volume-law random states or deeper RQC states). The S-RQC dataset uses only N=10 with relatively shallow circuits (W=40 CZ gates), which likely also have modest entanglement. This gap weakens an advertised advantage of the method. (Section 4.3, lines 183; Fig. 4a)

### Minor

4. **Table 1 uses unmatched gate counts and several entries have high variance.** AQER uses G ∈ {20, 40, 80} while baselines use G ∈ {36, 54, 90}, {30, 60, 90}, etc. due to "feasibility constraints" (Appendix E.2). While AQER wins with equal or fewer gates (directional conclusion is robust), the magnitude of improvement is not precisely quantifiable. Additionally, several entries have standard deviations comparable to or exceeding the mean (e.g., S-RQC at G=81, AQER: 0.067 ± 0.069; AQCE: 0.367 ± 0.110). No statistical significance tests are reported. (Table 1)

5. **Small sample size for GS-TFIM scalability trends.** The GS-TFIM dataset uses M=5 per configuration (g/J values) for each N ∈ {10,20,30,40,50} (line 140). Drawing scalability conclusions from 5 samples per setting weakens the statistical basis of the scalability claims. (Section 4.1, line 140)

### Trivial

6. **Fidelity definition for mixed states is imprecise.** The paper states "fidelity defined as F = Tr[ρ₁ρ₂]" (line 40), which is the Hilbert-Schmidt inner product, not the standard fidelity measure Tr[√(√ρ₁ ρ₂ √ρ₁)]². These coincide only for pure states. Since the paper only evaluates pure target states, this does not affect results, but the definition is technically imprecise. (Section 2, line 40)

## Nice-to-Haves

- **Ablation study of the three steps.** The paper does not ablate AQER's components (does Step II provide meaningful improvement beyond Step I alone? Does Step III mainly fine-tune or qualitatively change results?). An ablation would directly test whether the entanglement-reduction principle is the key driver.
- **Statistical significance testing.** With M=5–50 samples per condition, reporting confidence intervals or significance tests (e.g., paired bootstrap) for the headline comparisons in Table 1 would strengthen quantitative claims.
- **Discussion of SST-2 results.** All methods achieve infidelity > 0.4 even at G=90 on SST-2. A brief discussion of whether this level of approximation is practically useful for downstream tasks would be helpful for readers.
- **Comparison with exact loading cost.** Reporting the exact state preparation gate cost (e.g., via QR decomposition) would contextualize AQER's G values and strengthen the motivation.

## Removed Points

These points were raised by the harsh critic but are removed for the reasons stated:

- **"S is not a standard entanglement measure"**: The paper clearly defines S = Σᵢ S_{i} (sum of single-qubit Rényi-2 entropies). This is a design choice suitable for the authors' purpose; non-standardness is not a weakness.
- **"S depends on U, so bounds are not fundamental limits"**: The bounds are universal — they hold for any circuit U produced by any AQL algorithm. The dependence on U is natural because the bounds characterize the relationship between a circuit's entanglement-reduction property and its infidelity. This is correctly framed in the paper (line 88: "S depends on both |v_target⟩ and the circuit U").
- **Various presentation/formatting nits**: Removed per filtering rules (parser artifacts, not author errors).
- **"Missing related works"**: Removed per meta-reviewer instructions (cannot confirm existence of unlisted works).
- **"Missing appendix content"**: Removed per meta-reviewer instructions — the parser strips appendices from all papers.

## Novel Insights

The reviews' main novel observation beyond the paper's own contributions is the factor-N looseness of Theorem 3.1's bounds for large N, which the paper's framing underemphasizes. The reviewer also insightfully notes that the barren-plateau claim needs testing on genuinely entangled targets rather than area-law states to be convincing. The high variance in several Table 1 entries (std > mean for some conditions) is a precision concern that the paper's presentation glosses over.

## Suggestions

1. **Add computational cost discussion to the main text.** A brief statement such as "per iteration, AQER evaluates O(N²) qubit pairs, each requiring a Nelder–Mead optimization; total cost scales as O(T·N²·C_S) where C_S is the cost of computing S" would allow readers to assess the scalability claims directly.
2. **Test the barren-plateau claim on genuinely entangled targets**, such as volume-law random states or deeper RQC states at larger N.
3. **Report matched-G comparisons or interpolated estimates** and add confidence intervals or significance tests for the headline comparisons in Table 1.
4. **Temper the framing of the theoretical contribution** to accurately reflect the factor-N gap and acknowledge that the bounds provide qualitative guidance rather than tight quantitative predictions for large N.
5. **Conduct an ablation** of AQER's three steps to verify that entanglement reduction (Step I) is the key driver of performance.

## Score and Decision

**Calibration Anchors (all retrieved across Rounds 1 and 2):**

| Path | Avg Score | Round | Itemized | Comparison to Paper Under Review |
|------|-----------|-------|----------|----------------------------------|
| bEgDEyy2Yk.md | 1.00 | R1 | No | Unrelated (minimax paths) |
| Uj0h13lVrR.md | 1.00 | R1 | No | Unrelated (GFlowNets) |
| 5kMwiMnUip.md | 1.40 | R1 | No | Unrelated (LLM jailbreaking) |
| nSDOkm0SKo.md | 1.00 | R1 | No | Unrelated (finance neural nets) |
| hqxzi4d3Ws.md | 3.00 | R1 | No | Less related (noise-resilient PQC training); AQER stronger |
| TgTxJALwDz.md | 2.33 | R1 | No | Unrelated (quantum comm + BERT) |
| wgnMdxS2nZ.md | 3.40 | R1 | No | Unrelated (quantum FL) |
| m9BiWVTJDx.md | 3.00 | R1 | No | Unrelated (MRI optimization) |
| **un9Gzm0BZb.md** | **4.75** | **R1** | **Yes** | **Most similar (ER-AAE, entropy reduction for state preparation). AQER is clearly stronger** |
| XrwsdcgWKc.md | 4.25 | R1 | No | Less related (GFlowNets for ansatz design) |
| 3jRzJVf3OQ.md | 4.50 | R1 | No | Different topic (entanglement for attention) |
| 8WtBrv2k2b.md | 5.00 | R1 | No | Different topic (RL for scheduling) |
| **bB0OKNpznp.md** | **6.00** | **R1** | **Yes** | **Comparable quality; AQER slightly stronger on experiments** |
| **SL7djdVpde.md** | **6.75** | **R1** | **Yes** | **Stronger theory (DLA, overparameterization); comparable experimental breadth** |
| KbvKjpqYQR.md | 6.00 | R1 | No | Different topic (equivariant quantum GNN) |
| rINBD8jPoP.md | 5.60 | R1 | No | Comparable quality (RL for QAS) |
| vrBVFXwAmi.md | 8.00 | R1 | No | Stronger paper (LLM4QPE) |
| dLrhRIMVmB.md | 8.00 | R1 | No | Stronger paper (QTDA) |
| bH6T0Jjw5y.md | 8.00 | R1 | No | Unrelated (T-IB) |
| CxXGvKRDnL.md | 8.00 | R1 | No | Unrelated (diffusion compression) |
| tmSWFGpBb8.md | 6.00 | R2 | No | Different topic (learning complexity) |

**Round 1 bracket**: 5.5–6.5 (based on comparison to ER-AAE at 4.75 and SL7djdVpde at 6.75).

**Round 2 narrowing**: The second pass confirmed the 5.5–7.0 range with comparable papers at 5.60 (rINBD8jPoP), 6.00 (bB0OKNpznp), and 6.75 (SL7djdVpde).

**Weighted-item comparison**: AQER shares heavy-weight positives with the 6.0–6.75 anchors (strong experimental validation + well-motivated method + practical relevance) and is clearly above ER-AAE (4.75) which had fatal weaknesses (exponential classical cost, unclear algorithmic setup) that AQER avoids. AQER's negatives (loose bounds, opaque cost discussion, insufficient barren-plateau evidence) are meaningful but not fatal, and none of its core claims are invalidated. The paper lacks the heavier theoretical depth of SL7djdVpde (6.75) but has stronger comparative baselines and cleaner experimental framing. This places it at 6.0.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>