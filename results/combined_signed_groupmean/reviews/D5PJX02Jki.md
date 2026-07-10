Now I have all the information I need. Let me produce the final review.

**Round 1 bracket:** 4.5–6.5, based on the initial banded search showing the most relevant anchors (Scaling Laws of RoPE, Wavelet-based PE, Round and Round RoPE, STRING) clustering between 4.75 and 6.67.

**Narrowing via itemized comparison:** My paper's two decisive weakness items are EH mixed results (−9.97) and EC confound (−5.64). These parallel the most impactful weaknesses of the 5.0–5.25 anchors (Scaling Laws: "missing comparison with YaRN" −9.55, "only ppl without real benchmarks" −9.51; Wavelet PE: "marginally empirical improvement" −10.00). My paper's strongest strengths (+9.99 core observation, +9.83 derivation, +9.94 combinability) are comparable to the Scaling Laws anchor's strongest strengths (+9.92 theorems, +9.75 critical dimensions, +10.00 strong analysis). However, my paper lacks the Scaling Laws paper's theoretical depth (unified scaling framework) and works at smaller scale. The 6.0+ anchors (Round and Round at 6.20, STRING at 6.50) have either stronger theoretical contributions on real 7B-scale models or cleaner experimental designs with large-scale validation — my paper does not match those. Therefore the paper sits at the lower end of the bracket: **5.0**.

---

## Summary

This paper observes that when RoPE is expressed in complex-multiplication form, the standard attention computation uses only the real (cosine-weighted) part, discarding the imaginary (sine-weighted) part. The authors identify that sine-weighted attention has different positional properties (the sine-integral decays more slowly than the cosine-integral) and propose RoPE++, which computes both "real" and "imaginary" attention as separate heads. Two configurations are introduced: RoPE++_EC (same KV cache as RoPE but doubled attention heads) and RoPE++_EH (same head count but halved KV cache and QKV parameters). Experiments at 376M and 776M scales on RULER, BABILong, and short-context benchmarks show that RoPE++_EC substantially outperforms vanilla RoPE, while RoPE++_EH shows comparable or mixed results.

## Strengths

- **Core observation is genuinely novel and non-trivial.** Identifying that the complex-multiplication form of RoPE yields both cosine (real) and sine (imaginary) terms with complementary positional properties, and that the sine-weighted signal preferentially captures longer-range dependencies, is a genuinely insightful finding. The idea of exploiting both as separate attention channels is, to my knowledge, novel. [impact +9.99]

- **Clean mathematical derivation.** Sections 3.1–3.2 show that the imaginary attention is equivalent to a −π/2 rotation of the query followed by standard RoPE (Equation 4). The derivation preserves RoPE's absolute–relative dual interpretation elegantly. [impact +9.83]

- **Demonstrated compatibility with other long-context techniques.** Table 3 shows that RoPE++ can be combined with Linear PI and YaRN and still yields benefits over vanilla RoPE under those schemes, confirming general applicability beyond the base NTK scaling setup. [impact +9.94]

- **Two thoughtful efficiency configurations.** The EC (same cache, doubled heads) and EH (same heads, halved cache) framings fold the extra attention into GQA at different cost–benefit tradeoffs. Figure 4 validates that EH reduces memory and improves TPOT as context grows. [impact +6.19]

## Weaknesses

### Major

- **RoPE++_EH shows decidedly mixed long-context results that undercut the central claim.** At 776M, RoPE++_EH (19.4) is substantially *worse* than vanilla RoPE (22.8) on BABILong average (Table 2). At 376M, EH (18.2) is slightly worse than RoPE (18.8) on RULER average. On short-context tasks (Table 1), EH margins over RoPE are tiny (0.2–0.5 avg points) and within noise for models of this scale. The paper's claim that "RoPE++_EH surpasses standard RoPE with only half the KV-cache and QKV parameters" (Section 4.2) is not supported by the long-context data, and the claim is at best weakly supported for short-context. Since EH is the variant that *controls* for attention-head count (equal heads to vanilla RoPE), these mixed results raise the question of whether the imaginary mechanism itself — rather than extra capacity — drives the gains seen in EC. [impact –9.97]

- **RoPE++_EC is not compared to a parameter-matched or compute-matched baseline.** The EC variant has doubled attention heads and a doubled output projection \(W_o\) relative to vanilla RoPE, meaning roughly double the attention FLOPs. The paper frames the comparison as "same cache cost" (true), but the strong gains of EC over RoPE (e.g., RULER avg 25.0 vs 18.8 at 376M, Table 2) cannot be cleanly attributed to the imaginary mechanism versus the extra capacity/compute. Without a vanilla RoPE baseline matched to EC's head count and parameter count, the paper's most impressive results remain confounded. [impact –5.64]

### Minor

- **No statistical significance or variance is reported.** All tables report single scores without error bars, confidence intervals, or multiple-seed runs. Given that many claimed improvements are small (0.2–0.9 points on short-context tasks) and model sizes are moderate (376M, 776M), training noise cannot be dismissed as negligible. [impact –5.33]

- **The attention-pattern noise ablation (Section 5.2) conflates functional importance with sensitivity.** Adding Gaussian noise to imaginary heads degrades RULER performance more than adding noise to real heads, but this asymmetry could simply indicate that imaginary heads are more sensitive to perturbation — not that they specifically capture long-context information. A head-ablation study (zeroing out each set) would provide cleaner evidence. [impact –0.00]

- **Factual discrepancy in training tokens.** Section 4.1 (line 121) states 10B tokens for long-context training, while the Table 2 caption (line 176) says 5B tokens. This needs clarification. [impact –0.00]

- **Computational cost of RoPE++_EC is never quantified.** The paper says "the only cost is an additional imaginary attention" (Section 3.3) but does not report FLOPs, wall-clock time, or throughput for the EC variant, which doubles attention heads and \(W_o\). [impact –0.00]

### Trivial

- **The "discarded imaginary information" framing is rhetorically overstated.** Standard RoPE operates on real vectors; the complex representation is a notational convenience, and the imaginary part is not "lost" but was never part of the standard dot product. The contribution is better framed as adding a complementary sine-weighted signal. This does not affect the technical validity of the method. [impact –1.42]

## Nice-to-Haves

- Train a vanilla RoPE model matched to RoPE++_EC's head count and parameter count as a controlled baseline.
- Replace the noise ablation with a proper head-ablation study (zero out imaginary/real heads separately).
- Report results from multiple seeds or provide confidence intervals for key comparisons.
- Clarify the 5B vs 10B token discrepancy.
- Measure the actual FLOPs and runtime overhead of the EC variant.

## Removed Points

These points are flagged to be removed, treat them with caution:
1. "Section 3.2 sine integral argument is fuzzy" — removed. The paper correctly describes the characteristic curve as approximating a sine integral Si(Δt), which decays as ~1/Δt. The critic confused the raw sine function with its average over frequencies.
2. "Section 3.4 length-extrapolation argument is weak" — removed. The paper's claim that RoPE++ exposes dimensions to both positive/negative cos/sin values during training is mathematically sound.
3. "Section 3.3 75/25 split limitation" — removed. The paper adequately explains why allocating distinct head subsets would collapse back to standard RoPE.
4. "Missing standard long-context QA benchmarks" — removed. RULER and BABILong are standard synthetic benchmarks; demanding real-document tasks is scope creep.
5. "Missing architectural details" — removed. These are in the appendix (stripped by parser).
6. "Related work claims overstatement" — removed. The paper correctly says "few work revisits RoPE's intrinsic computation" and cites the few (Hua et al., Dai et al.) — the critic misread this.
7. Several Section-by-Section notes are factual misunderstandings or scope creep.

## Novel Insights

None beyond the paper's own contributions — the core insight about sine-weighted attention as complementary to cosine-weighted RoPE, and the derivation showing it is equivalent to a −π/2 query rotation, constitute the paper's novel contribution. The reviews do not surface additional insight beyond this.

## Suggestions

1. **Run a controlled EC baseline**: Train a vanilla RoPE model with doubled attention heads and doubled \(W_o\) (matching EC's capacity) to isolate whether EC's gains come from the imaginary mechanism or simply from extra parameters/compute.
2. **Provide multiple seeds**: Report at least 2–3 seeds for the key comparisons (especially EH vs RoPE on long-context) to establish statistical credibility.
3. **Improve the ablation**: Replace or complement the Gaussian-noise experiment with a direct head-ablation (zeroing out imaginary or real heads) to test functional importance rather than noise sensitivity.
4. **Resolve the 5B vs 10B token discrepancy** and report all hyperparameters needed to reproduce the results.

## Score and Decision

All anchors retrieved across rounds (excluding complete irrelevants):

| Path | Score | Round | Itemized | Comparison |
|------|-------|-------|----------|------------|
| jp4pxKqCRW.md | 2.50 | R1 | No | Periodic extension paper, much weaker empirical scope |
| 5dDYhvt6dY.md | 3.00 | R1 | No | Reinforced PE for translation, different domain |
| JO7k0SJ5V6.md | 5.00 | R1,R2 | **Yes** | Scaling Laws: similar quality tier, stronger theory but ppl-only eval criticized |
| sIGWTd1DcW.md | 5.25 | R1 | No | Contextual PE: similar scope but different approach |
| OhauMUNW8T.md | 5.25 | R1,R2 | **Yes** | Wavelet PE: similar quality tier, criticized for marginal empirical gains (−10.00) |
| t717joHHSc.md | 4.75 | R1 | No | Position bias mitigation: similar score range |
| GtvuNrk58a.md | 6.20 | R2 | **Yes** | Round and Round: stronger theory on Gemma 7B, higher score |
| xHMMt7r3GW.md | 5.33 | R2 | No | LieRE: higher-dim RoPE generalization |
| Us1RXG1Ji2.md | 6.00 | R2 | No | Contextualized equivariant PE, higher score |
| 1Iq1qIsc2s.md | 6.33 | R2 | No | Revisiting positional info, higher score |
| wXpSidPpc5.md | 6.50 | R2 | No | CLEX: strong continuous extrapolation |
| eoln5WgrPx.md | 6.50 | R2 | **Yes** | STRING: large-scale, training-free, cleaner empirical design |
| rR03qFesqk.md | 6.67 | R2 | No | FIRE: strong functional interpolation |

**Round-1 bracket:** 4.5–6.5. **Narrowing:** The paper shares decisive-magnitude weaknesses with the 5.00–5.25 anchors (EH mixed results −9.97 parallels Scaling Laws' "missing comparison" −9.55 and Wavelet's "marginal improvement" −10.00), and its strongest strengths match those anchors' top strengths. It does not match the 6.0+ anchors' scale (7B+ models), theoretical depth, or experimental cleanliness. **Final score:** 5.0.

**Rationale:** The paper contributes a genuinely novel and mathematically clean idea. However, the experimental validation has a structural issue: the variant showing the strongest gains (EC) is confounded with extra capacity, and the controlled variant (EH) produces mixed results — including notable underperformance on BABILong at 776M — that do not convincingly support the central claim. The paper's potential is clear, but the evidence as presented is insufficient to confirm that the imaginary mechanism, rather than increased model capacity, drives the observed improvements.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>