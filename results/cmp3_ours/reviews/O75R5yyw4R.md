Now I have a solid calibration. Let me write the final review.

## Summary
2-3 sentence summary of the paper's contribution.

This paper proposes IterRef, a test-time scaling method for discrete diffusion that uses Multiple-Try Metropolis (MTM) with a noising-denoising transition kernel to iteratively refine intermediate states toward reward alignment. The method is evaluated across text (MDLM, LLaDA-8B) and image (MaskGIT) domains, consistently outperforming baselines including Best-of-N, FK steering, and SoP. The paper also provides ablations showing that later-stage refinement is more effective and that increasing iterations (k) is more valuable than increasing particles (N).

## Strengths
- **Principled method design.** Combining Multiple-Try Metropolis with a noising-denoising transition kernel is a novel and well-motivated choice for discrete diffusion, where tokens are fixed once generated and gradients are unavailable. The custom balancing function λ (Equation 2) that yields uniform proposal weights and a simple closed-form Metropolis acceptance ratio (Equation 3) is elegant and computationally attractive. Section 3.1 is the strongest intellectual contribution of the paper.

- **Consistent cross-modal empirical gains.** Results in Figure 2 (MDLM and LLaDA-8B across four text tasks) and Table 1 (MaskGIT across compute budgets) show IterRef outperforming all baselines in nearly every setting, often by substantial margins — e.g., on MaskGIT CLIPScore at NFE=4, IterRef achieves 34.4 vs. 33.2 for the next-best method (FK). These gains hold across language and image modalities.

- **Informative ablation analyses.** Table 2 makes a non-obvious finding: unlike continuous diffusion where early steps dominate, IterRef is most effective at later denoising stages, revealing a genuine difference between discrete and continuous dynamics. Table 3 shows that iterating (k) is more valuable than generating more particles (N) under the same total compute — a practically useful insight for users of the method.

## Weaknesses

### Fatal
None.

### Major
1. **Unverified reversibility assumption in Proposition 1.** Proposition 1 states that the MTM chain converges to the optimal distribution p^*(x_t) under the assumption that "q and p_θ form a reversible Markov kernel" (line 146). All three evaluated models (MDLM, LLaDA-8B, MaskGIT) use the **absorbing-state** formulation of discrete diffusion (line 39), where the forward process q(x_s|x_t) for s > t only masks tokens and never unmasks them. The paper offers no argument or citation establishing that the composed kernel K(x_t, x_t') = Σ_s q(x_s|x_t) p_θ(x_t'|x_s) satisfies reversibility for such models. The abstract claims "proving convergence to the reward-aligned distribution" and the contribution list (line 35) states "IterRef leads to convergence to the target distribution... under certain assumptions" — but the critical assumption is neither justified nor discussed. The empirical results stand independently, but the theoretical framing overstates what is actually established. The authors should either justify the assumption for absorbing-state models or explicitly scope the convergence claim.

2. **NFE-based efficiency claims conflate generative and reward model calls.** The paper treats generative-model calls and reward-model calls on equal footing as "NFEs" (line 186), yet explicitly acknowledges that "aggregating these into a single NFE value may obscure meaningful differences, and it is preferable to report generative-model calls and reward-model calls separately" (line 174). The headline "8× faster" claim (Figure 1b, line 200) and the central efficiency comparisons (Figures 2 and 5, Table 1) all use this aggregated NFE metric. While the paper promises wall-clock analysis in Appendix C.4, this analysis is not in the main paper. The authors should present either wall-clock measurements or separate generative/reward NFE reporting in the main text to substantiate the efficiency claims.

### Minor
3. **No error bars or confidence intervals.** All quantitative results (Figures 2, 4, 5; Tables 1–3) are reported as point estimates without variance information. With 15 prompts × 20 samples = 300 generations per condition, the sample size is modest, and language generation quality is known to vary substantially across prompts. Some gaps between IterRef and baselines at specific NFE levels are small; without error bars it is difficult to assess whether the differences are meaningful.

4. **Figure 5 legend confusion.** The detoxification results in Figure 5(a) list both "IterRef" (blue) and "Ours" (red) as separate methods when they should be the same. The baselines SLP, SR, and SVTOD are not defined anywhere in the main paper — only BoN, SoP, SVDD, and FK are introduced in Section 4.1. This makes the figure difficult to interpret without consulting the appendix.

5. **The effective timestep analysis (Table 2) conflates two variables.** The "Evenly" condition distributes IterRef across all timesteps under the same total compute budget, meaning each individual timestep receives fewer refinement iterations than the focused conditions (e.g., 0.1T). The comparison therefore conflates refinement density per step with the timestep at which refinement is applied.

6. **No limitations section.** The paper does not discuss when IterRef might underperform (despite one such case appearing in the results: LLaDA+CoLA where BoN outperforms, line 202), hyperparameter sensitivity (k, N, α), or the approximation error in the intermediate reward r(x_t) (mentioned in passing at line 117 but not analyzed).

7. **The transition kernel's noising step is underspecified.** The kernel is defined as K(x_t, x_t') = Σ_s q(x_s|x_t) p_θ(x_t'|x_s) with t < s, but the paper does not specify how s is chosen — a key implementation detail affecting both computational cost and refinement behavior.

### Trivial
- The acceptance rate in Equation 3 (line 113) has a potential parenthesis issue: exp((r(x_t') - r(x_t)/α)) should likely be exp((r(x_t') - r(x_t))/α). This may be a parser artifact.
- CoLA is described as "linguistic acceptability" but is a binary classifier; how its output is converted to a continuous scalar reward is not explained.

## Nice-to-Haves
- The comparison with Wang et al. (2025), who use re-masking in masked models — a closely related approach — could be expanded beyond the single sentence in the related work section (line 305).
- The claim that the practical implementation "eliminates the resampling step" (line 164) while Algorithm 2 still generates N-1 auxiliary proposals (line 136) should be clarified — the current text creates confusion about what is done in theory versus in practice.

## Removed Points
These points from the input review are removed:
1. **"The '8× faster' claim may be substantially inflated."** — Downgraded from the original framing. For LLaDA-8B, where the paper states diffusion-model calls dominate cost (line 174), treating 1 reward call = 1 diffusion call (equal footing) would *overcount* IterRef's cost relative to actual wall-clock time, making the NFE-based claim potentially *conservative*, not inflated. The concern about conflating different cost types is valid and kept as Major weakness #2, but the claim of "inflation" is not supported by the paper's own cost description.
2. **"Algorithm 1 vs Algorithm 2 discrepancy about resampling."** — This is a legitimate point about unclear writing that should be clarified, but it does not affect the correctness of the method. Moved to Nice-to-Haves.
3. **"The theoretical guarantee depends on a reversibility assumption that almost certainly does not hold."** — Not removed. The core concern about the unverified assumption is retained as Major weakness #1. The phrase "almost certainly does not hold" is speculative; the paper's failure to address the assumption at all is the concrete problem.
4. **"Intermediate reward approximation not formally analyzed."** — The paper mentions this approximation (line 117) and cites prior work that uses the same approach. Requesting formal analysis beyond what is standard in the field is scope creep; folded into weakness #6 (no limitations section).
5. **Missing appendix content and missing related works.** — Removed per hard rules (parser strips appendices; cannot verify missing related works claim without external sources).
6. **Formatting/typo nitpicks.** — Removed per hard rules (parser artifacts).
7. **Reproducibility concerns about undisclosed hyperparameters.** — Removed per hard rules.

## Novel Insights
The harsh critic identifies a tension the paper itself does not address: Proposition 1's convergence guarantee depends on a reversibility assumption that the absorbing-state formulation of discrete diffusion — used by all three evaluated models — likely does not satisfy. This is not a fatal flaw (the empirical results stand), but it creates a mismatch between the paper's theoretical claims ("proving convergence") and what is actually established. Additionally, the critic correctly notes that the paper's own admission of NFE conflation (line 174) puts the headline "8× faster" claim on shaky ground — though the direction of bias is not as clear-cut as the critic asserts, since diffusion calls dominate the total cost for the large model (LLaDA-8B) where the claim is made.

## Suggestions
1. **Address the reversibility gap.** Either (a) justify why the reversibility assumption is reasonable for absorbing-state models, or (b) explicitly scope the convergence claim: "assuming the composed kernel satisfies detailed balance, the chain converges to p^*(x_t)" — and remove "proving convergence" from the abstract.
2. **Add wall-clock measurements** or separate generative/reward NFE reporting to the main results to substantiate the "8× faster" claim.
3. **Add error bars** to at least the key comparisons in Figures 2 and Table 1.
4. **Fix Figure 5** — resolve the "IterRef" vs. "Ours" duplication and define SLP, SR, SVTOD in the main text.
5. **Add a limitations section** discussing the CoLA/BoN underperformance case, hyperparameter sensitivity, and intermediate reward approximation error.

## Score and Decision

**Bracket (Round 1):** Based on calibration search across 6 bands, the most plausible range is [5.5, 7.5]. Papers in the 3.0–3.5 range (DynamicsDiffusion, Feynman-Kac Estimator) are substantially weaker — they lack clear novelty or have fundamental flaws. Papers in the 5.25–5.75 range (Universal Guidance, Multi-Task Diffusion) have simpler contributions or questionable improvement sources. Papers at 6.5–7.0 (Gaussian Mixture Priors, Reverse Diffusion Monte Carlo) have stronger theoretical foundations or more rigorous evaluations. Our paper sits between these: it has a genuinely novel method and strong cross-modal results, but the theoretical framing gap and NFE metric concern prevent it from reaching the 7.0 level.

**Anchors consulted:**
- `u1cQYxRI1H` (10.0): Not topically similar; illumination harmonization paper.
- `Uj0h13lVrR` (1.0): GFlowNets optimization — substantially weaker paper with fundamental issues.
- `kKXIYUi8ff` (3.0): Molecular dynamics diffusion — lacks novelty, missing essential parts.
- `46tjvA75h6` (3.0): EBM + diffusion — similar quality issues.
- `vK8C37eHXM` (3.2): Autoencoder + diffusion — mixed reviews, several weaknesses.
- `5sPgOyyjG5` (3.0): Feynman-Kac estimator — limited novelty.
- `pzpWBbnwiJ` (5.25): Universal Guidance — clean method but limited baselines comparison.
- `Hpu3KIX8Am` (4.0): Dreamguider — limited novelty, small improvements.
- `i8bdPSmOwk` (5.33): Momentum-driven guidance — limited novelty and improvement.
- `Y4kJp8GQmV` (4.25): Rectified CFG — theoretical contribution but limited experimental validation.
- `iXbUquaWbl` (6.50): Gaussian mixture priors — sound theory, comprehensive experiments.
- `cbv0sBIZh9` (5.75): Multi-task diffusion — questionable source of improvement.
- `kIPEyMSdFV` (7.00): Reverse diffusion MC — strong theory, but unclear writing and unsupported claims.
- `Q1QTxFm0Is` (6.80): Underdamped diffusion bridges — strong theoretical framework.
- `OlzB6LnXcS` (8.00): Shortcut models — one-step diffusion with strong results.
- `xDrFWUmCne` (8.00): Learning to discretize ODEs — well-executed, practical contribution.

**Final assessment:** The paper proposes a genuinely novel method (IterRef) with consistent cross-modal empirical gains and insightful ablations. However, the theoretical convergence guarantee relies on an unverified reversibility assumption for the absorbing-state models used in all experiments, and the headline efficiency claims depend on an NFE metric that the paper itself acknowledges conflates different cost types. These issues are fixable but make the paper a borderline accept rather than a clear accept.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>