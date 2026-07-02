## Summary
# Final Review Report

## Summary

This paper addresses the computational inefficiency of training unified multimodal transformers (models that handle both generation and understanding tasks in a shared parameter space). The authors propose UniMoD, a task-aware token pruning method built on Mixture of Depths (MoD). Through empirical analysis of attention weights, layer importance via ARank, and task interactions, they identify that token redundancy varies substantially across tasks (generation vs. understanding) and across layers. Based on these observations, they design a method with three components: (1) task-specific routers that prune tokens separately for Text-to-Image generation (T2I) and Multi-Modal Understanding (MMU), (2) an ARank-guided layer switch module that selects which layers to prune, and (3) a Shared MoD block for cross-task pruning. Applied to Show-o and Emu3, the method reduces training FLOPs by approximately 15% and 40% respectively, while maintaining competitive performance on most benchmarks.

**Overall assessment:** The paper identifies a genuinely important problem — efficient training of unified transformers — and provides a well-motivated, empirically grounded solution. The key insight (task-specific token redundancy) is convincingly demonstrated through multiple analyses. However, the paper has several weaknesses that reduce its impact: (1) missing statistical significance reporting makes it impossible to assess whether performance changes are meaningful, (2) the Emu3 results use a non-standard re-implementation that limits comparability, (3) the ARank-based pruning ratio estimation is underspecified, (4) a potentially critical brittleness (layer 3 collapse at GQA=0.0) is underexplored, and (5) the "first work" novelty claim cannot be verified in this run. The paper would benefit from variance reporting, clearer specification of the pruning ratio formula, and a more balanced discussion of limitations.

```text
ASCII Diagram — Paper Structure & Evidence Map
[Problem: Unified transformers are computationally expensive to train]
    → [Root cause: Token redundancy + heavy attention]
    → [Prior approach: MoD prunes tokens uniformly, but fails]
    → [Key insight: Redundancy differs by task (generation vs understanding)]
    → [Analysis: Attention weights, ARank layer importance, task interactions]
    → [UniMoD: Task-specific routers + ARank-guided layer selection]
    → [Evidence: 15% FLOPs reduction (Show-o), 40% (Emu3)]
    → [Open issues: No variance reporting, Emu3 re-implementation caveat,
       underspecified pruning ratio, unverifiable 'first' claim]
```

## Strengths
1. **Well-motivated problem and clear empirical grounding.** The paper tackles an important and timely problem — the high training cost of unified multimodal transformers — and backs its solution with systematic empirical analysis (attention weight patterns, ARank token redundancy, task interaction experiments). The three-pronged analysis in Section 3 provides a solid foundation for the method design.

2. **Simple but effective core idea.** The task-specific router design is conceptually straightforward and naturally follows from the empirical observations. Rather than proposing an entirely new architecture, UniMoD makes a targeted modification to MoD (separate routers per task), which is easy to understand and likely easy to implement. This simplicity is a virtue for practical adoption.

3. **Demonstrated FLOPs reduction across diverse model types.** The method is tested on two fundamentally different unified transformer architectures: Show-o (hybrid diffusion+AR) and Emu3 (fully autoregressive). Achieving 15% and 40% FLOPs reduction respectively with minimal performance degradation demonstrates reasonable generality. The extension to pure diffusion models (DiT, PixArt) further strengthens this claim.

4. **Informative ablation study.** Table 5 cleanly isolates the contribution of each design component (Basic MoD, w/o layer switch, w/o task-aware router, full UniMoD). The ablation reveals an interesting asymmetry — understanding tasks are relatively robust to uniform pruning, while generation quality depends critically on task-specific routers — which provides nuanced insight beyond the headline results.

5. **Use of ARank as a principled redundancy metric.** Adopting the ARank metric from γ-MoD for layer selection is a principled approach that connects the analysis directly to the method design. The use of ARank for both layer selection and pruning ratio estimation creates a coherent design pipeline from analysis to implementation.

6. **Honest disclosure of Emu3 re-implementation caveat.** The paper explicitly states that Emu3 results differ from the original due to using alternative training datasets (line 184), which is commendable transparency. Many papers omit this detail.

## Weaknesses
### W1. Missing statistical significance and variance reporting (Major)
All results in Table 3 and Table 4 are reported as single numbers without variance, confidence intervals, or significance tests. This is a critical methodological gap for two reasons. First, several benchmarks show small regressions (e.g., GQA: 56.3→54.5, -3.2%; VQAv2: 68.3→66.2, -3.1% in Show-o; GQA: 46.0→45.2, POPE: 76.0→74.7 in Emu3) that could plausibly be within random seed variation. Without multi-seed reporting, readers cannot distinguish genuine degradation from noise. Second, the paper's central claim is "maintaining or improving performance" — but on multiple benchmarks the trend is downward, and without confidence intervals this claim is unsupported. **Action:** Report mean±std over ≥3 seeds for all main benchmarks and add paired significance tests comparing UniMoD vs. full computation.

### W2. Emu3 results use non-standard re-implementation (Major)
The Emu3 "Full Computation" baseline (Table 3, row 5) is not the original Emu3 (which shows MME ~1240+, GQA ~60+) but a re-implementation using LLaVA-v1.5-mix-665K (line 184). The re-implementation produces substantially lower scores (MME 881.3, GQA 46.0), indicating significant differences in training setup. This means: (a) the 40% FLOPs reduction claim is only validated under this re-implementation, not the original Emu3 training configuration; (b) a method that works well on a suboptimally trained model may not preserve performance on a fully trained original model. **Action:** (1) Explicitly state that Emu3 results are under a re-implementation and may not transfer to the original training setup. (2) If possible, compare with the original Emu3 published numbers and discuss the gap. (3) Train both full-computation and UniMod variants from scratch with identical data/ compute for a fair comparison.

### W3. Critical layer collapse at layer 3 not adequately explained (Major)
Table 1 shows that skipping layer 3 during inference causes GQA to drop to 0.0 (complete failure). This is an extreme result that suggests layer 3 performs a critical functional role that no other layer can substitute. The paper dismisses this as "early layers are more critical," but a drop to 0.0 is not normal degradation — it suggests either a genuine architectural brittleness or an experimental artifact (e.g., tensor shape mismatch when skipping this specific layer). This result could indicate that: (a) the model is not robust to even single-layer perturbations, (b) the skip-based analysis may have a confound (e.g., skipped layers causing hidden state dimension mismatch), (c) the model's redundancy profile has a critical singularity at layer 3 that is not discussed. **Action:** Investigate and explain the GQA=0.0 result at layer 3. Is it a genuine property, an artifact, or a bug? Report results for even-numbered skipped layers as well.

### W4. Formula ambiguity in MoD definition (Major)
Equation (2) defines the MoD update as $x_i^l = x_i^l + D^l(x_i^l) R^l(x_i^l)$ when the router score exceeds the threshold. This notation is ambiguous: $D^l$ is described as "the $l$-th layer of the Transformer" which outputs a transformed token vector, but the expression $D^l(x_i^l) R^l(x_i^l)$ implies multiplying a vector by a scalar router weight. If the intent is hard binary routing (pass/skip), the router weight should not appear as a multiplier. If the intent is soft gating, the threshold-based branch is contradictory. This ambiguity is repeated in Equation (4) for the task-specific router. **Action:** Adopt the standard MoD formulation: $x_i^{l+1} = \text{TransformerLayer}^l(x_i^l)$ if $R^l(x_i^l) \geq \delta_s^l$, else $x_i^{l+1} = x_i^l$, or clarify if a soft gating mechanism is intended instead.

### W5. Pruning ratio estimation is underspecified (Major)
The Layer Switch Module (Section 4.1) "approximate[s] each layer's pruning ratio by normalizing its ARank score by the sequence length." No exact formula is provided. This is a core design step — the pruning ratio determines how many tokens are retained per layer — yet the mapping from ARank to pruning ratio is left ambiguous. The ARank metric itself also has an ambiguity: $\text{rank}(A_h)$ in Equation (3) is not defined as numerical rank vs. effective rank. Since attention matrices are typically row-stochastic (softmax output), their numerical rank may be N for most layers due to numerical noise, which would make ARank uninformative. **Action:** (1) Provide the exact formula for pruning ratio from ARank: e.g., $p_l = 1 - \tau_l / N$. (2) Define $\text{rank}(A_h)$ explicitly, e.g., effective rank based on singular value threshold. (3) Report ARank stability across different data samples (currently 50 per task).

### W6. Unverifiable "first work" novelty claim (Minor, deferred)
Contribution 3 states "To the best of our knowledge, we are the first work to propose a task-aware token pruning method for unified transformers." This claim cannot be verified in this run because external literature retrieval is disabled. The related work section cites MoMa (Lin et al., 2024b) which combines MoE+MoD in a unified transformer (Chameleon) but "lacks results on generation tasks." Whether MoMa's MoD application already constitutes task-aware pruning is unclear without deeper reading. **Action:** Either (a) provide explicit side-by-side technical comparison with MoMa showing what design elements are unique to UniMoD, or (b) soften the claim to "a task-aware token pruning method for unified transformers."

### W7. Introduction narrative needs sharper gap framing (Minor)
The introduction paragraphs 1-3 (lines 8-10) describe unified transformers and MoD but lack a concrete, reader-engaging problem statement. The key gap ("different tasks have different redundancy") appears only in paragraph 3 with limited specificity. A more effective opening would: (1) establish why efficient training of unified transformers matters concretely (cost, time, accessibility), (2) state the specific bottleneck (task-dependent token redundancy), (3) preview the solution (task-specific routers). The current version reads as a literature-survey listing rather than a motivated argument.

### W8. Conclusion lacks limitations and future work (Minor)
The conclusion (Section 6) is a single short paragraph that restates the method without any critical reflection, limitations, or future directions. This is a missed opportunity: acknowledging the slight performance regressions on GQA/VQAv2, the Emu3 re-implementation caveat, and the need for ARank validation would strengthen scientific credibility and provide readers with an honest assessment of the method's boundaries.

### W9. Related Work section is a list rather than structured comparison (Minor)
Section 2.1 cites 18+ papers in a single paragraph with one-sentence descriptions, without grouping by approach type or comparison dimension. A structured organization (e.g., fully autoregressive vs. hybrid models, with explicit differentiation per group) would help readers position the paper's contribution more easily.

```text
ASCII Diagram — Revision Strategy Roadmap
[W1: No variance/significance] → [Add ≥3 seeds + std + paired t-test]
    → [Expected: Support or qualify "maintaining performance" claim]
[W2: Emu3 re-implementation] → [Acknowledge non-standard setup; bound claims]
    → [Expected: Honest assessment of generalization]
[W3: Layer 3 GQA=0.0] → [Investigate root cause; report full analysis]
    → [Expected: Either fix artifact or document genuine brittleness]
[W4: MoD formula ambiguity] → [Adopt standard MoD or clarify gating]
    → [Expected: Reproducible notation]
[W5: Pruning ratio underspecified] → [Exact formula + ARank definition]
    → [Expected: Reproducible method description]
[W6: 'First work' claim] → [Compare with MoMa explicitly or soften]
    → [Expected: Verifiable novelty or bounded claim]
[W7-W9: Writing polish] → [Restructure intro, related work, conclusion]
    → [Expected: Improved narrative and scientific transparency]
```

## Score
**Final Score: 6/10**

**Scoring rationale:** The paper addresses an important problem (efficient training of unified multimodal transformers) with a well-motivated, empirically grounded approach. The core idea of task-specific token routing is clean and directly follows from the analysis. The FLOPs reductions (15-40%) are practically meaningful. However, the score is limited by several factors that reduce the paper's current impact and reliability:

- **Research value (primary):** The paper identifies a genuine bottleneck and provides a practical solution. The empirical analysis connecting task type, layer depth, and token redundancy is valuable for the community. However, the value is somewhat diminished because the method is tested on only two models with substantial caveats in one (Emu3 re-implementation).
- **Novelty (primary):** The task-aware router design is a reasonable incremental improvement over MoD, but the "first work" claim cannot be verified in this run. The main contribution is more empirical (analysis of redundancy patterns) than methodological, which is valuable but not groundbreaking.
- **Validity/soundness:** Several weaknesses affect validity — missing variance reporting, underspecified pruning ratio, ambiguous MoD formula, and the unexamined GQA=0.0 collapse at layer 3. These are fixable but currently reduce confidence in the results.
- **Reproducibility:** The method section has critical gaps (exact pruning ratio formula, ARank rank definition, task-specific capacity settings) that would make independent reproduction difficult without guessing.

**Post-Revision Target:** [7, 8]/10 — achievable if the authors address W1-W5 (variance reporting, Emu3 caveat clarification, formula correction, pruning ratio specification, layer 3 analysis) and provide a balanced discussion of limitations.