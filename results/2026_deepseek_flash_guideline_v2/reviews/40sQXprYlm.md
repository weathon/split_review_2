Now I have all the information I need. Let me produce the final consolidated review.

## Summary

This paper introduces Distributed Neural Architectures (DNA), a conditional-computation framework where each token learns its own trajectory through a pool of modules and routers — generalizing beyond MoE, MoD, and prior routing paradigms by allowing fully flexible per-token routing with identity (skip) modules. The framework is instantiated in both vision (ImageNet at ViT-small scale) and language (FineWeb-Edu language modeling at GPT-2 medium scale). The paper shows DNA models are competitive with dense baselines (top-1 DNA: 79.1% vs ViT-small: 79.8%; top-2 DNA matches/exceeds GPT-2 medium on 5/7 benchmarks) and analyzes emergent properties including power-law path distributions, interpretable routing specialization, and learned compute allocation. The paper explicitly frames itself as a feasibility-and-analysis contribution, not a SOTA pursuit.

## Strengths

1. **Novel architecture with cross-domain validation.** The DNA framework is a natural and ambitious generalization of conditional computation — fully flexible per-token routing through arbitrary modules with learnable skip operations. Applying the same framework to both ImageNet and language modeling with consistent methodology demonstrates domain-agnostic applicability. This is genuinely novel relative to MoE (single-layer expert selection) and MoD (uniform layer-skip decisions).

2. **Discovery of power-law path distributions with measured exponents.** Figure 1 reports specific quantitative exponents — exponent −1.2 for the trained language DNA and exponent −1 for random (untrained) models in both domains. The comparison to random initialization provides a rigorous control, and the finding that path distributions follow power-laws even in random models is a novel empirical observation about the combinatorics of routing.

3. **Multi-faceted interpretability analysis revealing emergent specialization.** The paper provides three complementary forms of evidence: (i) Figure 3 shows that patches sharing the same path correspond to semantically coherent concepts (edges, colors, brass instruments, puzzle pieces); (ii) Figure 4 uses deep-dream-style reconstruction tracing how routing decisions at different steps encode progressively higher-level features (texture/edges → lighting → object identity); (iii) Section 4.2 demonstrates that language-model routers consistently group semantically similar tokens (punctuation, verb variants, prepositions) across different input paragraphs. This depth of qualitative analysis is rare in conditional-computation papers.

4. **Emergent compute allocation with documented patterns.** The top-2 DNA (25% skip) maintains 78.8% accuracy while exhibiting learned content-appropriate compute budgets. Figure 5 shows compute follows a roughly Gaussian distribution across images, and the paper provides qualitative evidence linking compute usage to visual complexity — demonstrating that models learn to allocate compute without explicit per-image supervision.

5. **Honest scope and limitations.** The paper explicitly states it is "not focused on beating SOTA models" (line 38) and acknowledges that language models are "vastly underparametrized" for the data (line 154). It also reports negative findings honestly, such as language module reuse being "most likely random" (line 201).

## Weaknesses

### Major

1. **Parameter-count disparities in baselines are not discussed.** In vision, top-1 DNA has 34M total params vs ViT-small's 22M (55% more). In language, top-2 DNA has 603M total params (48% more than GPT-2 medium's 406M) and 433M active params (7% more). The paper compares on active parameters and labels DNA "competitive," but never addresses whether the comparison would hold with parameter-matched dense baselines (e.g., a ViT with 34M params or a GPT-2 with 433M active params). This gap weakens a central claim of the paper.

2. **No ablation studies.** Critical design choices are not ablated: backbone size ($N_b \in \{0,1,2\}$), router type (linear classifier), top-$k$ values (why only 1 and 2?), the skip-encouraging hyperparameters $r$ and $u$, and the residual formulation (Eq. 1). Since the paper acknowledges these are "purely empirical design choices" (line 60), ablations are essential to understand which choices drive performance and whether the framework is robust. Without them, the contribution reads as a single configuration report rather than a validated method.

3. **No statistical uncertainty.** Results are reported as single best-run values from hyperparameter grid searches. No multiple seeds, error bars, or confidence intervals are provided for any result. The gaps between DNA and dense baselines (e.g., 79.1% vs 79.8% in vision; 2.674 vs 2.720 loss in language) could be within noise, and there is no way to assess this from the presented data.

### Minor

1. **The claim that DNAs "subsume" MoE, MoD, early exit, etc. is overstated.** Line 28 states: "This construction includes feed-forward, MoE, MoD, weight sharing, early exit as particular cases that can emerge via optimization." The evidence shows path specialization and module reuse, but does not demonstrate that specific known methods (e.g., the expert specialization characteristic of MoE with load balancing, or the confidence-based early-stopping of early exit) actually emerge. The architectural constraints (backbone layers always active, sequential per-step routers) also limit how faithfully these methods could be expressed. The paper's actual contributions are strong enough without this overclaim.

2. **The language skip model's poor performance is presented without analysis.** Table 3 shows top-2 DNA (30% skip) is substantially worse than the uniformly shallower GPT-2 baseline (Wiki perplexity 52.6 vs 38.0, ARC-E 52.5 vs 58.0, HellaSwag 35.5 vs 37.9). This negative result undermines the efficiency motivation for language — learned token-level skipping underperforms simple uniform depth reduction — but the paper does not analyze why or what this implies about the method's viability.

3. **The compute efficiency proxy is not validated.** The paper measures "normalized compute" by counting modules used per token (a reasonable relative proxy), but never measures actual FLOPs, throughput, or wall-clock time for any configuration. The routing mechanism itself has computational overhead (routers are classifiers), and sparse attention patterns have data-dependent costs. Without any real-hardware measurement, the practical compute implications remain unclear.

4. **Language module reuse is found to be random but not discussed.** Section 4.3 concludes that module reuse in language is "most likely random," which is a significant negative finding for the "emergent specialization" thesis. The paper notes this briefly but does not reflect on what it implies about the method's scalability or whether different architectural choices might be needed for language.

### Trivial

1. **"~ inf" for random model Wiki perplexity (Table 3) is imprecise.** A loss of 10.825 corresponds to perplexity ≈ 50,000, not infinity. Minor presentational issue.

## Nice-to-Haves

- Include parameter-matched dense baselines (e.g., ViT with 34M params, GPT-2 with 433M active params) for fairer comparison.
- Validate the module-count proxy against actual FLOPs or wall-clock time for at least one configuration.
- Quantify the interpretability claims (e.g., measure consistency of patch groupings with ImageNet class labels).
- Ablate backbone size ($N_b$) and its effect on the emergence of distributed routing.
- Report results over 3+ random seeds with error bars for primary comparisons.

## Removed Points

*These points were raised by reviewers but removed after verification against the paper. They are retained here in case the AC finds them useful.*

1. **"No actual efficiency measurement — FLOPs/wall-clock never measured"** (from Harsh Critic as "Critical Issue #1"). → **Downgraded from Fatal to Minor (weakness #3 above).** The paper's claims are about learning to *allocate* compute (demonstrated with module-count proxy showing content-adaptive allocation), not about runtime speed benchmarks. The criticism was disproportionately severe given the paper's stated scope. However, the lack of any absolute efficiency measurement is retained as a minor weakness.

2. **Missing technical details (s_max, router initialization, gradient estimation through discrete top-k, bias values).** → **Removed.** The paper states these are in the appendix (line 102: "The values of hyperparameters, initialization scheme, etc can be found in the Fig. A"). The appendix was stripped by the PDF parser. Per guidelines, missing appendix content should not be flagged as a weakness.

3. **"Abstract claims broader than demonstrated (transformer, MLP, attention, etc.)"** → **Removed.** The paper explicitly notes "We have not yet experimented with including other modules" (line 36), honestly limiting its scope.

4. **"Wiki perplexity values implausible"** (Harsh Critic's question about Table 3). → **Removed.** The comparison is against GPT-2 medium *retrained on the same 21B tokens of FineWeb-Edu*, not the original GPT-2 medium. Perplexity of 33.7 for this training setup and 31.5 for the larger (433M active param) model are entirely plausible.

5. **Typos, formatting issues, and grammar nitpicks.** → **Removed.** These are parser artifacts, not author errors.

6. **Strength Finder's generic strengths** (e.g., "this paper addressed an important problem"). → **Removed.** Generic praise without specific evidence anchored in the paper's content.

7. **Strength Finder's "emergent compute efficiency with documented allocation patterns"** → Merged into Strength #4 after verifying against the paper's actual evidence.

## Novel Insights

The most valuable observation emerging from the cross-review synthesis is a tension the paper does not fully engage with: the vision domain shows clear, interpretable emergent specialization (paths correspond to object parts, boundaries, backgrounds) while the language domain shows routing that is "most likely random" for module reuse, with routers grouping tokens only at very superficial levels (punctuation, verb forms). This asymmetry — which the paper honestly reports but does not analyze — raises a fundamental question about whether fully flexible token-level routing is a better fit for spatially-structured inputs (images) than for sequentially-structured ones (text). If this gap persists at scale, it would suggest that the DNA framework's strengths (interpretable specialization, content-adaptive compute) may be domain-dependent. The paper would be significantly stronger if it discussed this possibility and proposed testable hypotheses for follow-up work.

## Suggestions

1. **Add parameter-matched dense baselines** (ViT with 34M params, GPT-2 with 433M active params) to the main comparison tables, or explicitly discuss why the parameter-count asymmetry does not affect the "competitive" claim.

2. **Add ablation studies for at least** backbone size ($N_b$), top-$k$ values (1, 2, 3, 4), and the skip-encouraging hyperparameters ($r$, $u$) to establish which design choices matter.

3. **Report results over at least 3 random seeds** with error bars for the primary comparisons (Table 1 and Table 3 results).

4. **Discuss the language skip model's underperformance** relative to uniform depth reduction — this is informative for the community even as a negative result.

5. **Measure actual FLOPs or throughput** for at least one DNA configuration vs. its dense baseline to validate whether the module-count proxy translates to real compute savings.

6. **Recalibrate the "subsumes MoE/MoD/early-exit" claim** to "is a generalization that can express behaviors reminiscent of these methods" and provide targeted evidence or remove the claim.

## Score and Decision

**Score: 5.0** — Borderline. The paper introduces a genuinely novel architecture with interesting emergent properties and provides a depth of interpretability analysis rare in this area. However, the lack of ablation studies, absence of statistical uncertainty, and parameter-count disparities in the baseline comparisons prevent it from being a clear accept. The core ideas are solid and the analysis is insightful, but the empirical rigor needs substantial strengthening to match the strength of the claims.

**Decision: Reject** — The paper should not be accepted in its current form. The major weaknesses (no ablations, no error bars, parameter comparison issues) are addressable, and a revised version with these gaps filled could be accept-quality. The contributions (novel architecture, power-law finding, interpretability analysis) are strong enough to warrant further development, but the current empirical presentation does not meet ICLR's standards for rigor.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>