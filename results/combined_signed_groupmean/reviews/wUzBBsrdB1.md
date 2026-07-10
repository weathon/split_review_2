## Summary

This paper studies the effect of the L0 hyperparameter (average number of active latents per token) on sparse autoencoders (SAEs) trained on LLM activations. Using controlled toy-model experiments with ground-truth features, the authors show that when L0 is too low, SAEs "cheat" by mixing correlated features together to improve reconstruction at the cost of monosemanticity; when L0 is too high, they also mix features via degenerate solutions. They propose a proxy metric based on pairwise decoder cosine similarity (c_dec) that identifies the correct L0 in toy models, and present preliminary evidence that it transfers to real LLMs. The paper also finds that JumpReLU SAEs naturally "stick" near the correct L0 across a wide range of sparsity coefficients.

## Strengths

- **Clean toy-model demonstration of the low-L0 failure mode (Section 3.1).** The initialization experiment — starting a low-L0 SAE from the ground-truth solution and observing gradient descent drive it toward mixed features — is compelling and directly shows that gradient pressure, not initialization, causes feature hedging. This is the paper's most airtight piece of evidence.

- **Critique of sparsity-reconstruction tradeoff plots (Section 3.4, Figure 4).** Showing that a ground-truth SAE with perfectly correct latents achieves *worse* reconstruction than a "cheating" SAE at low L0 is a crisp, non-obvious point that challenges the standard evaluation protocol for SAE architectures. This observation alone could influence how SAEs are evaluated in future work.

- **JumpReLU "sticking" observation (Section 3.6, lines 185–187).** The finding that JumpReLU SAEs' L0 "sticks" near the correct value over a wide range of λ_s is interesting and practically useful, revealing a robustness property of this architecture that the SAE community should be aware of.

## Weaknesses

### Major

- **The LLM evidence is too thin to support the paper's broad claims about real models.** The paper's headline message — that L0 must be set correctly in real LLMs and that "most commonly used SAEs have an L0 that is too low" — goes far beyond what the experiments establish:
  - For Gemma-2-2b Layer 5, the c_dec curve drops sharply at L0≈250 then remains essentially flat out to L0=2000. The paper itself acknowledges (line 246) that "the metric can sometimes remain nearly flat for a wide range of L0." This does not identify a single "correct" L0 the way it does in toy models; it identifies a lower bound below which things get worse.
  - The validation signal (k=16 sparse probing F1) varies by only ~4% (0.78 to 0.82) across the entire L0 sweep, which is a weak signal for peak-picking.
  - Only two LLMs are tested (Gemma-2-2b and Llama-3.2-1b) with 1–2 layers each. This is insufficient to support sweeping claims about "most SAEs" in use today.
  - The paper's own Section 4.2 acknowledges that "there is no reason why every latent has the same firing threshold" and that L0 can be simultaneously too high for some latents and too low for others. This undercuts the premise that a single correct L0 exists for real LLMs in the first place.

- **The c_dec metric's theoretical grounding assumes orthogonal ground-truth features, but real LLM features are only "nearly orthogonal."** The paper's toy model uses perfectly orthogonal features (line 65), where c_dec works cleanly. The LRH states features are "nearly orthogonal" (lines 13, 59) — not perfectly so. If true LLM features have non-zero pairwise cosine similarity even when perfectly disentangled, then minimizing c_dec could push SAEs toward *incorrect* feature directions that are more orthogonal than the true features. The paper does not address this gap, nor does it test how c_dec behaves when features have controlled non-orthogonality.

- **The JumpReLU "sticking" finding substantially weakens the practical urgency of the paper's message, but this tension is not discussed.** The paper finds (lines 185–187) that JumpReLU SAEs — the SOTA architecture widely deployed by Anthropic and others — naturally find near-optimal L0 over a wide range of λ_s values. Yet the abstract and introduction state "most commonly used SAEs have an L0 that is too low" without qualifying that this problem may be largely mitigated for the most commonly used architecture. The conflict between the alarmist framing and the mitigating finding is not acknowledged or resolved.

### Minor

- **The JumpReLU "sticking" claim lacks quantitative characterization.** Figure 7 (left) shows scattered data points, and the paper describes the effect qualitatively ("sticks near the correct L0") without reporting what fraction of λ_s values produce L0 within a specified tolerance of the optimum.

- **The practical utility of c_dec is limited by its computational cost.** As the paper notes (line 248), using the metric requires training a sweep of SAEs at different L0 values, each on 500M tokens. This makes it more of an analysis tool than a practical method for avoiding hyperparameter sweeps.

- **The claim that "most commonly used SAEs have an L0 that is too low" lacks quantitative support in the main text.** It is attributed (line 240) to "a cursory search of open source SAEs on Neuronpedia" referenced to Appendix A.13. The main text provides only a brief mention that "L0 less than 100 is very common," without specifying how many SAEs were surveyed, what L0 ranges were found, or what threshold was used to determine "too low."

## Nice-to-Haves

- Test c_dec on additional LLMs and layers where sparse probing benchmarks already exist to broaden the empirical basis.
- Address the non-orthogonal feature case explicitly in toy models (e.g., features at controlled angular separations) to test whether c_dec remains reliable when the orthogonality assumption is relaxed.
- Report the sensitivity of sparse probing results to the choice of k (currently fixed at k=16).
- Analyze c_dec's sensitivity to the number of latents h under a null model of random unit vectors.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:
- The criticism about the ground-truth SAE construction in Section 3.4 being "somewhat unusual" and not corresponding to real SAE evaluation: REMOVED because this is a deliberately simplified conceptual experiment designed to isolate a specific effect, not a claim about real SAE evaluation pipelines.
- The comment about the paper being "incremental" over Chanin et al. (2025): REMOVED because the paper explicitly cites Chanin et al. and frames its contribution as a refinement ("We consider our work a version of feature hedging due to low L0"). This is appropriately modest in the paper itself.
- The note about equation (3) omitting the reconstruction loss coefficient: REMOVED as a formatting-level observation with no substantive weight.
- The comment about c_dec values (0.02–0.03) not being close to zero in LLMs: This concern is already subsumed by the orthogonal-features weakness above.
- Various section-by-section notes that amount to "this could be done differently" rather than identifying actual flaws.

## Novel Insights

None beyond the paper's own contributions. The paper correctly identifies a genuine failure mode of SAEs (feature mixing due to L0 mismatch) and proposes a diagnostic metric. The reviews do not surface any novel synthesis beyond what the paper already presents.

## Suggestions

- Restructure the paper to present the toy-model demonstration and the sparsity-reconstruction critique as the primary contributions, with the LLM experiments framed as preliminary evidence of transfer rather than definitive validation.
- Add quantitative characterization of the JumpReLU sticking effect (e.g., the fraction of λ_s values producing L0 within a tolerance of the c_dec-determined optimum).
- Explicitly discuss the tension between the JumpReLU sticking finding and the claim that "most SAEs have L0 too low."
- Address the non-orthogonal feature case in toy models to clarify the scope of c_dec's applicability.

## Score and Decision

**Calibration summary.** Calibration anchors were retrieved from /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration:

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Scaling and evaluating sparse autoencoders (TopK SAE paper) | tcsZt9ZNKD.md | 8.20 | 2 | Yes | Much stronger LLM validation (GPT-4, scaling laws, many metrics); weaknesses are near-0 impact. Our paper has comparable toy-model strengths but much weaker LLM evidence. |
| Sparse Autoencoders Find Highly Interpretable Features | F76bwRSLeK.md | 4.80 | 2,3 | Yes | Similar pattern: strong conceptual contribution but thin experimentation. Negative reviewer gave -10.00 for weak experiments. |
| Compute Optimal Inference and Provable Amortisation Gap in SAEs | ghH6YYDs15.md | 4.67 | 3 | Yes | Similar weakness profile: synthetic-only experiments (-9.83), limited LLM validation (-6.39), theoretical claims questioned (-10.00). Rejected. |
| Towards Principled Evaluations of Sparse Autoencoders | 1Njl73JKjB.md | 7.00 | 2,3 | Yes | Well-scoped contribution with clear limitations stated. Stronger empirical grounding for its claims. |
| Sparse Autoencoders Do Not Find Canonical Units of Analysis | 9ca9eHNrdH.md | 7.00 | 2,3 | Yes | Strong methods paper with thorough experimentation across multiple dimensions. |

**Bracket reasoning.** Round 1 bracket: 4.0–6.5. Round 2 narrowed: the paper's strengths (toy model initialization experiment, sparsity-reconstruction critique) score at +9.97 to +10.00 — comparable to strengths of the 7.00–8.20 anchors. However, its top weaknesses (thin LLM evidence, unsupported "most SAEs" claim, questionable applicability of single-L0 concept) score at -9.92 to -10.00 — comparable to the decisive weaknesses of the rejected 4.67 anchor. Unlike the 7.00+ anchors, the paper lacks a clear acknowledgment of its LLM evidence's limitations and does not properly scope its claims. Unlike the rejected 4.67 anchor, it has genuinely compelling toy-model results that the SAE community should take seriously.

**Final score and decision.** The toy-model core is solid and the sparsity-reconstruction critique is a meaningful community contribution. But the paper overreaches in its LLM claims and the evidence does not support the broad statements in the title and abstract. With restructuring and toned-down claims, this could be a strong paper. In its current form, it sits between borderline reject and borderline accept.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>