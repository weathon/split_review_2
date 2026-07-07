Now I have enough to draft the review. Let me compile it and submit the draft.**Round 1 bracket: 5.5–7.0**

Based on calibration:
- CoTFormer (5.75, Accept): similar adaptive computation architecture, comparable scope and missing ablations
- Dynamic MoE (7.0, Accept): novel transformer variant with better ablations and stronger baselines
- TokenFormer (7.5, Accept): novel architecture with rigorous evaluation

ThoughtBubbles sits above CoTFormer (more original mechanism) but below Dynamic MoE (weaker ablations, weak baseline). The two major weaknesses (Copy-K baseline too weak to isolate adaptivity, missing attenuation-alone ablation) prevent a high score but the consistent perplexity gains and interpretable analysis are genuine contributions. **Final score: 6.0**

---

## Summary
ThoughtBubbles introduces an adaptive parallel computation architecture for transformer LMs that learns to fork or delete residual streams during standard language model pretraining, with no supervision beyond cross-entropy loss. Tokens that require more compute form "bubbles" of cloned residuals that receive additional transformer layers of processing and are merged via score-weighted averaging at the output. Experiments at 150M–772M scales on OpenWebText and peS2o show consistent perplexity improvements over parameter-matched and computation-matched baselines and gains on HellaSwag and LAMBADA.

## Strengths

- **Novel unsupervised forking mechanism** (Section 2.3, Eqs. 1–11): The combination of cumulative scoring, top-k selection, score-attenuated attention, and learned fork embeddings is architecturally original. Training with standard language modeling loss with no external supervision is a genuine contribution to adaptive computation research.

- **Consistent perplexity improvements across all six (scale × dataset) settings** (Table 1, Figure 3): ThoughtBubbles κ=4L achieves the lowest perplexity across every configuration tested, with the 319M model beating the 772M vanilla baseline on OpenWebText—a substantive empirical result, not cherry-picked.

- **Interpretable computation allocation validated against an independent reference** (Figure 5, Section 5): The model allocates more forks at moderate-to-high entropy tokens without explicit supervision, and this holds when entropy is measured with a separately trained baseline LM (right panel of Figure 5), removing the circularity concern.

## Weaknesses

### Fatal
None.

### Major

- **Computation-matched baseline (Copy-K) is too weak to validate the adaptivity claim.** The Copy-K baseline duplicates raw input residuals and lets them attend to each other, but provides no learned fork embeddings and no mechanism to develop useful separate representations. Table 1 confirms that Copy-3 and Copy-5 barely improve over the vanilla baseline (<0.3 perplexity points in most settings). The paper explicitly cites pause-token and thinking-token approaches (Goyal et al., Herel & Mikolov, Hao et al.) as direct competitors in Section 6 but compares against none of them. Consequently, the demonstrated advantage over Copy-K cannot be attributed to *adaptivity per se*—it may equally reflect the attenuation architecture (Eqs. 8–10), the learned fork embeddings, or both.

- **Missing ablation isolating adaptivity from the attenuation architecture.** Equations 8–10 modulate attention and residual writes for *all* tokens via their cumulative scores, independent of whether forking actually occurs. This is a standalone architectural change that could itself explain perplexity gains. No ablation disables adaptive fork/keep selection while retaining score attenuation, so it is impossible to attribute the observed gains to the adaptive forking mechanism specifically rather than to the attenuation architecture.

### Minor

- **FLOPs matching is stated qualitatively.** The Table 1 caption describes κ=4L as "roughly FLOPs-matched against Copy-5," but because forking is variable, actual average FLOPs depend on runtime fork rates, which are not measured or reported. This leaves the FLOPs comparison unverifiable.

- **BLiMP underperformance receives only a restatement, not an explanation.** At 319M/OpenWebText, ThoughtBubbles scores 78.3/78.8 vs. 80.5 for Copy-3. Section 4 attributes this to "pruned dynamic parallel computation may not be as helpful for syntax," which merely restates the observation. A minimal hypothesis about how score attenuation or forking placement interacts adversely with structural grammatical patterns (or an acknowledgment that it is an open failure mode) would strengthen the analysis.

### Trivial

- The abstract phrase "paving the way to unify train-time and test-time scaling behaviors" is aspirational; no test-time scaling experiments are conducted in this work.

## Nice-to-Haves
- Implement one fixed-position learned-embedding filler token baseline (non-adaptive but architecturally richer than raw-residual Copy-K) to test whether adaptivity or learned fork embeddings drives the gains.
- Add a single ablation: attenuation-only (Eqs. 8–10) without any forking, to partition the contribution of each component.
- Quantify mean active sequence length and/or actual average FLOPs at runtime to support the "roughly FLOPs-matched" claim.
- Show which *types* of tokens receive the most forks (e.g., rare words, clause boundaries) rather than only entropy-binned statistics in Figure 5—this would make the interpretability claim more concrete and checkable.

## Removed Points
*These points are flagged for removal; treat with caution.*

- **Abstract overclaims zero-shot superiority (REMOVED):** The harsh critic states the abstract makes an unqualified claim of zero-shot superiority. On re-reading, the abstract says "zero-shot evaluations *such as* HellaSwag and LAMBADA"—not all tasks. Contribution 2 in the body honestly says "we additionally perform *competitively* against BLiMP and PIQA." This is not an overclaim. Removed.

- **Figure 4 y-axis scale comparison (REMOVED):** Flagged as making magnitude comparisons misleading, but the paper's claim ("more than an order of magnitude higher") is about relative ordering, which is apparent from the box plots. Removed as a presentation nitpick.

- **Autoregression distribution shift as a "significant practical limitation" (REMOVED):** Section 5.1 and Appendix E.1 acknowledge this and provide dynamic budget scaling that restores parity with blockwise forward pass (Figure 6). The issue is disclosed with a working mitigation. Removed as a weakness.

- **Abstract "test-time scaling" framing (REMOVED from major; retained as trivial):** The paper does not claim to have demonstrated test-time scaling, only that the method "paves the way." Demoted to trivial.

## Novel Insights
The concave relationship between token entropy and fork allocation (Figure 5) is a noteworthy emergent finding: the model allocates *less* computation at the very highest-entropy tokens, not more. The authors hypothesize that extremely high-entropy positions (clause edges, coreferences) are irreducibly uncertain, so additional computation offers no marginal benefit. This is a specific, falsifiable observation about how adaptive computation distributes across the uncertainty spectrum and deserves follow-up in future work.

## Suggestions
- Implement one stronger non-adaptive baseline with learned fork embeddings at fixed positions to directly test the adaptivity hypothesis.
- Ablate: attenuation (Eqs. 8–10) alone vs. attenuation+forking, to partition gains.
- Measure and report mean active sequence length per forward pass.
- Provide a mechanistic hypothesis for BLiMP underperformance (e.g., whether score attenuation suppresses sensitivity to function-word agreements).

## Score and Decision

**Anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 7igPXQFupX (CoTFormer) | 5.75 | R1 | Similar scope—adaptive computation architecture; ThoughtBubbles has more original mechanism but comparable ablation gaps |
| tI3eqOV6Yt (Adaptivity/Modularity) | 5.00 | R1 | Smaller-scale adaptive transformer study; weaker contribution |
| uAtDga3q0r (RaNA adapters) | 6.00 | R1 | Adaptive rank allocation; less novel architecturally |
| Y5LjYI4N6P (Stagewise pretraining) | 6.75 | R1 | Novel pretraining architecture; solid evaluation; comparable scope |
| T26f9z2rEe (Dynamic MoE) | 7.00 | R2 | Novel adaptive transformer with better ablations and baselines |
| oQ4igHyh3N (TokenFormer) | 7.50 | R2 | Novel scalable transformer architecture; rigorous evaluation |
| OvoCm1gGhN (Diff Transformer) | 8.00 | R1 | Novel attention mechanism; strong evaluation; higher bar |

**Round 1 bracket:** 5.5–7.0

**Narrowing:** ThoughtBubbles exceeds CoTFormer (5.75) in originality (true unsupervised dynamic forking vs. CoT-mimicry architecture) and empirical breadth (6 scale×dataset combinations vs. smaller scale). It falls short of Dynamic MoE (7.0) and TokenFormer (7.5) because its central comparative claim (adaptive > non-adaptive) lacks the ablation and baseline rigor those papers exhibit. The two Major weaknesses together prevent a 7+ score. The consistent perplexity results and genuinely novel mechanism justify sitting above 5.75. **Final score: 6.0.**

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>