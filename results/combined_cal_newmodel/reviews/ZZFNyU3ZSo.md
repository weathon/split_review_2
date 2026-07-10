## Summary

This paper introduces UniMoD, a task-aware token pruning method for unified multimodal transformers (models handling both generation and understanding). Through empirical analysis of attention weights, layer importance (ARank), and task interactions, the authors show that token redundancy varies significantly across tasks and layers. Based on these insights, they design separate Mixture-of-Depths (MoD) routers per task with specialized capacities, applying the method to Show-o (15% FLOPs reduction) and Emu3 (40% FLOPs reduction) while maintaining competitive performance on several benchmarks.

## Strengths

- **Genuinely informative empirical analysis (Secs 3.2–3.4).** The attention-weight analysis across four models (Fig 2), ARank comparisons across tasks and layers (Fig 3), and especially the competitive token-pruning experiment (Fig 4) collectively provide concrete evidence that token redundancy is task-dependent and layer-dependent. The competitive experiment is the most informative piece — it directly shows that a single router lets generation tokens dominate, which motivates the task-separate design. This kind of empirical grounding is uncommon in efficiency papers. **[favorability=12.75]**

- **Clean, interpretable method well-aligned with the observations.** Three specialized MoD blocks (T2I, MMU, Shared), task-specific capacities, and ARank-based layer selection each follow from a specific finding in the analysis. The method is not over-engineered, and the ablation in Table 5 validates that each component contributes. **[favorability=12.02]**

- **Two genuinely different testbeds.** Show-o (diffusion for generation, AR for understanding) and Emu3 (fully AR for both) represent the two dominant paradigms for unified transformers. Demonstrating the method on both architectures is a meaningful generality check. **[favorability=11.56]**

- **Non-trivial FLOPs savings** especially on Emu3 (40% reduction on an 8.5B model) with competitive performance. The savings also scale with model size (15% at 1.3B to 20% at 8B per the appendix). **[favorability=11.60]**

## Weaknesses

### Fatal
None.

### Major

- **Gap between FLOPs savings and wall-clock speedup is substantial and inadequately explained.** Table 4 shows: Show-o T2I achieves 10% FLOPs reduction but only 2.3% training-cost reduction; Show-o MMU achieves 20% FLOPs reduction but only 3.8% training-cost reduction. Emu3 fares better (40% FLOPs → 21% cost reduction) but still shows a large gap. The paper attributes this to memory bandwidth in one sentence and references the appendix, but provides no breakdown of how much of the theoretical FLOPs saving is lost to router computation, irregular memory access from variable-length sequences, or attention interactions between pruned and unpruned tokens. Since wall-clock speedup is the practically relevant metric, this gap substantially weakens the practical claims. **[favorability=-0.01]**

- **The main baselines in Table 3 (Interleaved Layer, Early Exit) consume roughly half the compute of UniMoD** (25.6 vs. 43.3 TFLOPs), making the comparison uninformative on its own. The paper acknowledges they use fewer FLOPs, but the headline comparison should be against a compute-matched baseline. The ablation's "w/o task-aware router" variant at 40.8 TFLOPs is closer to fair, and it reveals that the benefit of task-aware routing is concentrated on generation quality (GenEval 0.50→0.61), while understanding task scores are nearly identical to UniMoD. This pattern should be acknowledged more honestly in the paper's framing. **[favorability=3.19]**

### Minor

- **No variance or statistical significance reported anywhere.** Across nearly all comparisons, performance differences are small (1–3% on understanding benchmarks). Without error bars (multiple seeds or confidence intervals), the reader cannot assess whether observed drops (e.g., GQA 56.3→54.5, VQAv2 68.3→66.2) represent genuine degradation or run-to-run noise. This is especially problematic for the Emu3 results where differences are mixed in direction (GQA 46.0→45.2 down, GenEval 0.46→0.48 up, DSG 79.0→80.0 up) and likely within noise. **[favorability=1.35]**

- **ARank-based layer selection description is inconsistent with the implementation.** The method section (Sec 4.1) describes selecting "the half of layers with the lowest ARank values for each task," but the implementation (Sec 5.1) says "we transform the last 12 layers into MoD layers for both tasks." If the last 12 layers are indeed the ones with lowest ARank values (which Fig 3 suggests may be the case for Show-o), the paper should state this explicitly rather than leaving the reader to infer it. **[favorability=2.81]**

- **Pruning ratio selection is underspecified.** The implementation reports specific ratios (MMU capacity scaled from 1 down to 0.2; T2I prunes 20% of tokens in later layers), but it is unclear whether these numbers come from the ARank normalization procedure described in Sec 4.1 or from manual tuning. The paper should clarify the connection between ARank-derived estimates and the deployed pruning ratios. **[favorability=2.86]**

### Trivial
None.

## Nice-to-Haves

- The competitive token-pruning experiment (Fig 4) could be strengthened by showing results at multiple capacity levels (e.g., 0.25, 0.5, 0.75) to understand where task imbalance emerges.
- The Emu3 results, while internally valid, would be more compelling if the paper also reported the original published Emu3 scores alongside their re-implementation to help readers calibrate the data difference.
- The paper mentions scaling to more than two tasks (Sec A.12) — this is interesting and could be given more prominence.

## Removed Points

These points are flagged to be removed, treat them with caution:
1. **"Emu3 results cannot support headline claims"** — REMOVED. The comparison is internally valid (both baseline and UniMoD use the same re-implementation with the same data). The paper transparently states the data difference. The small/inconsistent differences are really about the lack of error bars (already covered under Minor weaknesses).
2. **"Baselines too weak as a fatal flaw"** — DEMOTED from fatal to major with nuance. The uneven compute is a real limitation but the ablation provides the needed controlled comparison. The critic's framing as fatal overstates the problem.
3. **Speculative concerns about pruning ratios at different capacity levels** — MOVED to Nice-to-Haves.
4. **Formatting/style nitpicks and missing related work concerns** — REMOVED per guidelines.

## Novel Insights

None beyond the paper's own contributions. The reviews largely affirm the paper's framing and do not surface unexpected findings that fundamentally reframe the contribution.

## Suggestions

1. Add a section analyzing the gap between FLOPs savings and wall-clock speedup: break down losses from router computation, attention sparsity patterns, and memory-bandwidth effects.
2. Report all main results (Table 3, Table 5) with at least 2–3 random seeds and standard deviations.
3. Clarify the relationship between ARank-based layer selection and the actual choice (last 12 layers), and how ARank normalization maps to the specific pruning ratios used.
4. Add a compute-matched single-router MoD baseline to Table 3 so the headline comparison is fair.
5. Frame the contribution more precisely: the primary benefit of task-aware routing is preserving generation quality under pruning, while on understanding tasks a single router performs nearly as well.

---

### Calibration Anchor Summary

| Path | Avg Human Score | Round | Itemized? | Comparison |
|------|----------------|-------|-----------|------------|
| γ-MoD (q44uq3tc2D) | 6.67 | Round 1 | Yes | Most topically similar (ARank+MoD for MLLMs). Accepted. UniMoD has comparable analysis but weaker practical evidence (wall-clock gap). |
| "Unreasonable Ineffectiveness" (ngmEcEer8a) | 6.50 | Round 1 | Yes | Layer pruning for LLMs. Accepted. Similar analysis-driven contribution but with fewer practical evaluation gaps. |
| "Looking Beyond Top-1" (SfNmgDqeEa) | 6.40 | Round 2 | No | Transformer analysis paper. Rejected despite high scores (split reviews). |
| MoH (VOVFvaxgD0) | 5.75 | Round 3 | No | Mixture-of-head attention. Rejected. |
| ECoFLaP (iIT02bAKzv) | 5.50 | Round 1 | Yes | Weight pruning for VLMs. Accepted. Similar score range — UniMoD has stronger analysis but also more significant concerns. |
| SparseVLM (1xG3MN1RRW) | 5.20 | Round 1 | Yes | Training-free token pruning for VLMs. Rejected. UniMoD has stronger empirical grounding and cleaner evaluation. |
| HiMAP (0eRJRbVG95) | 4.40 | Round 1 | Yes | MLLM visual token pruning. Rejected. UniMoD's analysis and novelty substantially stronger. |

**Round 1 bracket:** After filtering weaknesses and comparing against γ-MoD (6.67, Accept) and SparseVLM (5.20, Reject), the plausible range was 4.5–6.5.

**Round 2 narrowing:** Comparison with γ-MoD's itemized items showed that UniMoD shares γ-MoD's strength in empirical analysis but has a more damaging weakness (wall-clock gap, favorability -0.01 vs. γ-MoD's worst at -1.52). The wall-clock gap is practically more consequential than γ-MoD's clarity issues. This places UniMoD below γ-MoD.

**Round 3:** Inside the 5.5–6.5 bracket, comparing with ECoFLaP (5.50, Accept) and MoH (5.75, Reject) confirms that UniMoD sits at the lower end of this range. Its strengths are genuine but the evaluation gaps (especially the wall-clock speedup disparity) prevent it from reaching accept-level confidence.

**Final placement:** Just below γ-MoD (6.67) and above ECoFLaP (5.50). The shared strength with γ-MoD (ARank-based analysis) is offset by weaker practical evidence. The wall-clock gap item (favorability -0.01) is the decisive negative — γ-MoD's most negative item was at -1.52 but γ-MoD still reported real wall-clock speedups (31% training, 53% inference) unlike UniMoD's 4% on Show-o.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>