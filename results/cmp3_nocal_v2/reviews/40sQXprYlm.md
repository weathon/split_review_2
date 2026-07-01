## Summary

This paper introduces Distributed Neural Architectures (DNAs), a framework where tokens/paths dynamically choose their own computational paths through a collection of modules (transformers, MLPs, attention blocks). DNAs generalize Mixture-of-Experts, Mixture-of-Depths, layer skipping, and parameter sharing under a single routing-based design. The authors demonstrate trainability in both vision (ImageNet, at ViT-small scale) and language (FineWeb-Edu, at GPT-2 medium scale), and analyze emergent properties including power-law path distributions, module/path specialization, and interpretable compute allocation.

## Strengths

1. **Conceptually novel and well-motivated framework.** The unification of MoE, MoD, layer skipping, and weight sharing into a single routing-based design where connectivity emerges from training is a genuine conceptual contribution. The paper correctly identifies that existing conditional computation methods are special cases and shows such a design is trainable end-to-end.

2. **Cross-domain demonstration is substantive.** Showing feasibility in both vision (ImageNet, discriminative) and language (FineWeb-Edu, generative) with the same framework—using consistent design principles—provides real evidence that the method generalizes. Most conditional computation papers operate in only one domain.

3. **Interpretability analysis is thorough and yields genuinely interesting findings.** Specific results that stand out: (a) paths through the model follow power-law distributions (Fig. 1c,d); (b) different paths specialize for different visual features (edges, objects, background in Fig. 3) and linguistic functions (linking verbs, sentence boundaries, adjectives in Fig. 8); (c) the reconstruction visualizations (Fig. 4) show that routing decisions encode meaningful hierarchical representations. The honest reporting that language DNAs' parameter sharing appears random rather than meaningful (Section 4.3) adds credibility.

4. **Honest framing of scope and limitations.** The authors state explicitly that they are not trying to beat SOTA, that improvements are "left on the table," and that their models are "way too small" for the language domain. This framing is appropriate for a feasibility-and-analysis paper.

## Weaknesses

### Fatal
None.

### Major

1. **The "competitive with dense baselines" claim is oversold and the language comparison is structurally uneven.**

   - **Vision (Table 1, Fig. 2):** ViT-small achieves 79.8% vs. top-1 DNA at 79.1% and top-2 DNA at 78.8%. The gap is 0.7–1.0% (DNA is behind). Only the best run from a grid search is reported with no variance estimates, making it impossible to assess significance.
   - **Language (Table 3):** The top-2 DNA model (433M active params, 603M total) beats GPT-2 medium (406M) on most metrics, but it has **6.6% more active parameters** and **48% more total parameters** (603M vs. 406M). The top-1 DNA model (406M active params, matching GPT-2) performs *worse* than GPT-2 on most metrics (val loss 2.754 vs. 2.720, ARC-E 56.9 vs. 58.9, HellaS 38.6 vs. 40.5). So with matched active parameters, DNA is worse; with a parameter advantage, it roughly matches. The paper does not discuss this asymmetry.

2. **The compute efficiency experiment undercuts the efficiency narrative, and the paper does not address this.**

   Table 3 compares a "top-2 (30% skip)" DNA model against "GPT-2 (30% shallower)" — a simple truncated model with the same effective compute. The shallower GPT-2 decisively beats the DNA skip model on **every single metric** (val loss: 2.772 vs. 2.784; ARC-E: 58.0 vs. 52.5; BoolQ: 54.9 vs. 52.9; HellaS: 37.9 vs. 35.5; PIQA: 65.9 vs. 64.2). This means the learned conditional compute allocation of DNA is strictly worse than a fixed shallower model at the same compute budget. The paper presents this result in the table but offers no explicit discussion or analysis of why the routing-based approach underperforms a trivial static baseline. For a paper claiming models "learn to allocate compute intelligently" and that compute efficiency "can be learnt from data," this is direct counterevidence that demands explanation.

3. **No statistical rigor in any reported result.**

   There are no multiple seeds, standard deviations, or confidence intervals for any experiment. Vision models report "the best run of each model" from a grid search (line 116). Language models similarly (line 160). Without variance estimates, the 0.7–1.0% vision gap and the language results (which flip depending on which DNA model is considered) cannot be interpreted. A single favorable run could account for the top-2 DNA's lead over GPT-2 on several benchmarks.

### Minor

4. **No ablation studies for a new architecture with many design choices.** The paper introduces a multi-component architecture and makes non-trivial design decisions: (a) hard-coded "backbone" layers (N_b = 1–2) that process all tokens without routing; (b) the specific residual formulation in Eq. 1; (c) Pre-LN transformer blocks as the only module type; (d) linear token-choice routers; (e) the number of modules (18–72). None of these choices are ablated. For a paper whose contribution is a new architectural framework and whose analysis focuses on emergent properties, the reader cannot distinguish which observed phenomena (power-law distributions, path specialization) are properties of the DNA framework and which are artifacts of specific implementation choices.

5. **The "power-law path distribution" finding is weakened by the random baseline, and the paper does not quantify the difference.** The paper reports (Fig. 1 caption) that "the distribution of paths through the random model also follows power-law with exponent -1." The trained language model has exponent -1.2 (a modest change). The paper notes this but does not quantify how much the trained distribution differs from the random one (e.g., via KL divergence, tail-behavior change, or per-path analysis). The headline claim about power-law distributions remains equivocal: a significant fraction of the observed structure may be a property of the routing mechanism itself, not of learned computation.

6. **The evidence for path specialization in vision relies on visual inspection of selected examples.** Figures 3 and 8 show cherry-picked paths and manually interpreted categories. A quantitative analysis (e.g., measuring path purity with respect to class labels or image-region annotations) would substantially strengthen the specialization claims.

7. **No comparison against standard MoE or MoD baselines at comparable scale.** The paper positions DNA as a generalization of MoE and MoD, but the baselines are dense ViT and GPT-2. A standard top-2 MoE transformer or Mixture-of-Depths model at the same scale would be far more informative for understanding whether the added generality of DNA provides any empirical benefit over existing conditional computation methods.

8. **The claim that parameter sharing "relies on similar features" (Section 3.3) is supported only by aggregate correlation.** The paper states "different models exhibit similar amount of parameter sharing on the same images" and concludes this means sharing relies on similar features. This is a weak form of evidence — correlation of aggregate statistics does not demonstrate that the *same* modules are shared for the *same* features. The paper's own finding that language parameter sharing is random (Section 4.3) further suggests caution.

### Trivial
- The superscript \(t\) on \(M_i^t\) in Eq. 1 is explained as denoting "the \(t^{\text{th}}\) component of the output" (line 78), but readers may initially confuse it with a time/index step. A minor clarification would help.

## Nice-to-Haves
- A discussion of the computational overhead of the routers themselves (linear classifiers applied at every step), which is not accounted for in the efficiency analysis.
- An ablation of the backbone layers (\(N_b = 0\)) to test whether fully distributed routing from the start is trainable.
- An ablation of the number of modules \(N_m\) to test sensitivity to this hyperparameter.
- Reporting error bars from at least 3 runs to support the comparative claims.

## Removed Points
These points were removed from the input review for the reasons stated:
1. **Notation issue with \(M_i^t\)**: The paper explicitly states "the t superscript on M denotes the t^th component of the output" (line 78). The reviewer's concern is based on a misreading — the notation is explained. *Removed as factually incorrect.*
2. **Dynamic attention sparsity not explicitly stated**: The paper states in the Fig. 1 caption: "When a module that contains attention operation acts on several tokens simultaneously the attention pattern is computed *only* between these tokens." This is stated clearly enough; the follow-up (whether this applies to all attention modules) is implicitly answered — all modules in the DNA are modules. *Removed as the paper does address this.*
3. **Table 3 is confusing due to inclusion of skip/shallower models**: This is a formatting/presentation preference, not a substantive weakness. *Removed as a style nitpick.*
4. **Missing MoE/MoD baselines**: Moved to Nice-to-Haves since the paper is a feasibility study, not a SOTA comparison. The paper does not claim to outperform MoE/MoD.

## Novel Insights
The input review accurately identifies the core tension in the paper: the framework is genuinely novel and the interpretability analysis reveals genuinely interesting emergent structure (path specialization, power-law distributions, hierarchical feature encoding in routing decisions), but the evidential support for downstream claims ("competitive performance," "intelligent compute allocation") is weaker than the paper's framing suggests. The most novel observation from the review is the decisive failure of the DNA skip model against a simple shallower GPT-2 — this is a structural result in the review that the paper itself does not confront. Had the paper explicitly discussed *why* routing-based compute savings underperform static truncation (e.g., routing overhead, attention sparsity limiting information flow, difficulty of learning good skipping decisions), this could have been a genuinely useful negative result for the community. The review also surfaces the tension between the "feasibility" framing and the paper's implied positive claims about the method's utility — a calibration issue worth resolving.

## Suggestions
1. Confront the efficiency experiment head-on: explicitly discuss why the skip model underperforms the shallower baseline, and what this implies about the practical utility of routing-based compute allocation. This negative result, properly analyzed, could be a genuine contribution.
2. Report results with multiple seeds and variance estimates, or at minimum acknowledge the limitation of single-run reporting.
3. Add ablations of the backbone layers (\(N_b\)) and number of modules (\(N_m\)) to distinguish framework-level properties from implementation-specific artifacts.
4. Calibrate the language used to describe results: "competitive" is reasonable for vision (within 1% with matched active params) but strained for language (requires parameter advantage to match). A more precise characterization would strengthen the paper's credibility.

## Score and Decision

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>