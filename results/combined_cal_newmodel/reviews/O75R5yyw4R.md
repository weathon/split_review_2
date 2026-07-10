Now I have all the information I need. Let me compile the final consolidated review.

**Calibration Summary:**

All anchors from the calibration rounds:

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| u1cQYxRI1H (IC-Light) | 0.50 | 1 | No | Completely different topic (illumination harmonization); score-anchor only |
| Uj0h13lVrR (Stochastic GFlowNets) | 1.00 | 1 | No | Different topic; very weak paper |
| 5lUdTogEL3 (Lifelong ReID) | 1.00 | 1 | No | Different topic |
| 5kMwiMnUip (Jailbreaking) | 1.40 | 1 | No | Different topic |
| W4djmqKZC6 (Pixel-Aware Diffusion) | 3.00 | 1 | No | Diffusion acceleration; weaker empirical validation |
| QKqWnkwPL (Self-distillation) | 3.00 | 1 | No | Diffusion distillation |
| MBkoYFftRa (Inner Loop Feedback) | 3.00 | 1 | No | Diffusion acceleration |
| **Ombm8S40zN (DDPP)** | **6.25** | **1,2,3** | **Yes** | **Most similar anchor — steering discrete diffusion models. DDPP had wider domain coverage (incl. proteins, wet-lab) but also more severe weaknesses (missing baselines at -3.71 favorability). IterRef is slightly weaker in breadth but cleaner in method.** |
| 4hFT4rfG40 (Plug-and-Play) | 3.75 | 1,2 | Yes | Discrete masked models control. Similar domain but weaker empirical work (protein only, no baselines). IterRef is clearly stronger. |
| **2fgzf8u5fP (SVDD)** | **3.80** | **1,2** | **Yes** | **Derivative-free guidance for discrete diffusion. SVDD had severe issues: unfair α settings, unverified assumptions (-2.59). IterRef is significantly stronger.** |
| Hpu3KIX8Am (Dreamguider) | 4.00 | 1 | No | Training-free conditional generation (continuous diffusion) |
| MBDH5zyxHM (C-Code) | 4.60 | 2 | No | Controlled denoising; similar domain but weaker |
| D7PQ54l5Q1 (DPMC) | 4.75 | 2 | No | Inverse problems with MCMC; related technique |
| **x1uv2gdjKV (DNO)** | **5.50** | **3** | **Yes** | **Inference-time alignment of diffusion models. Had more severe missing-baseline issues (-2.61). IterRef has broader evaluation and cleaner theory.** |
| MJNywBdSDy (DDPD) | 5.75 | 2,3 | Yes | Planned denoising for discrete diffusion; different goal (generation quality, not alignment) |
| peNgxpbdxB (Scalable Discrete) | 6.00 | 1 | No | Discrete diffusion for combinatorial optimization |
| **G328D1xt4W (DRAKES)** | **6.00** | **2,3** | **Yes** | **Discrete diffusion fine-tuning via RL. Had severe theory concerns (-3.79), but stronger biological validation. Comparable overall.** |
| b3CzCCCILJ (ICG) | 6.00 | 2 | No | Diffusion guidance (continuous) |
| 6p74UyAdLa (DNG) | 6.25 | 2 | No | Dynamic negative guidance |
| i5MrJ6g5G1 (UDLM) | 5.25 | 2,3 | Yes | Uniform discrete diffusion; accepted despite -1.08 to -3.59 weaknesses |
| 4w99NAikOE (IterComp) | 6.80 | 1 | No | Different topic (compositional T2I) |
| 8.00-range papers | 8.00 | 1 | No | Much stronger papers; not comparable |

**Round-1 bracket:** 3.5–7.5 (wide initial bracket)
**Round-2 narrowing:** 5.0–6.5 based on domain similarity
**Round-3 check of 5.5 anchor (DNO, Reject):** IterRef has comparable or less severe weaknesses

**Final score anchoring:** IterRef is stronger than SVDD (3.80) and DNO (5.50), comparable to UDLM (5.25, accepted) and weaker than DDPP (6.25, accepted). Its worst weakness (-1.41, undefined case study baselines) is less severe than the worst weaknesses of DDPP (-3.71), DRAKES (-3.79), UDLM (-3.59), and DNO (-2.61). Its strengths are comparable. This places IterRef in the 5.5–6.0 range. I assign **5.5** — borderline, with fixable issues.

Decision: I'll say Reject, because the Proposition 1 issue requires substantial reframing and the undefined baselines in the case study need fixing. But it's a borderline case that could become Accept with a strong rebuttal.

Actually, looking at UDLM which was accepted at 5.25... and DRAKES accepted at 6.00... I think with appropriate framing I could go either way. Let me just report 5.5 and Reject, since the issues are real and need addressing.

Wait, the guidelines say "5.5" is the score. Let me look at the scoring scale:
1 - strong reject
3 - reject
4 - borderline reject
6 - borderline accept
8 - accept
10 - strong accept

So 5.5 is between borderline reject (4) and borderline accept (6). 

Hmm, let me just go with 5.5 and Reject. The paper needs revisions but has potential.## Summary

This paper introduces IterRef, an inference-time method for steering discrete diffusion models toward reward-aligned outputs. The core idea is to use noising-denoising transitions within the Multiple-Try Metropolis (MTM) framework to iteratively refine intermediate states during sampling, correcting tokens that existing particle-based methods (SMC, importance sampling) leave fixed once generated. The method is evaluated across three model backbones (MDLM, LLaDA-8B, MaskGIT) and five reward objectives, consistently outperforming baselines.

## Strengths

- **Well-motivated core idea.** The paper correctly identifies a genuine gap: discrete diffusion models lack gradient-based guidance, and existing particle-based methods (SMC, importance sampling) cannot correct tokens once generated. The proposal to use iterative noising-denoising as an MCMC refinement mechanism is a natural and principled response to this problem. Section 1 and Figure 1(a) make this contrast clearly.

- **Principled theoretical framing via Multiple-Try Metropolis (Section 3.1).** Casting the refinement process within the MTM framework provides a formal basis for what would otherwise be a heuristic resampling loop. The explicit design of the transition kernel K and balancing function λ (Eq. 2) to cancel intractable terms and yield a simple acceptance rule (Eq. 3) is theoretically elegant, and Algorithm 2 is cleanly specified.

- **Consistent empirical trends across models and tasks.** IterRef outperforms baselines across MDLM, LLaDA-8B, and MaskGIT, and across toxicity, sentiment, CoLA, perplexity, and CLIPScore — 4 language metrics + 1 image metric. This breadth across models and modalities is the paper's strongest empirical asset.

- **Effective-timestep analysis (Table 2) reveals an interesting structural finding.** Later-stage refinement matters more in discrete diffusion, contrasting with continuous diffusion where early steps dominate. This insight goes beyond "our method works" and contributes to understanding discrete diffusion dynamics.

## Weaknesses

### Major

- **Proposition 1's convergence guarantee rests on an unverified assumption.** The proposition (line 146) requires that "q and p_θ form a reversible Markov kernel." This assumption is stated without justification and is unlikely to hold for any learned discrete diffusion model: the forward process q is a fixed masking schedule, while p_θ is a learned approximation of the true reverse transitions. There is no reason they would jointly satisfy detailed balance with respect to any distribution. The paper frames this as a contribution ("explanation of its effectiveness under certain assumptions," line 35), but the central assumption is neither verified nor empirically discussed in any experiment. The stated guarantee is essentially conditional on an unverified condition. The paper would be stronger if it transparently acknowledged this gap and provided empirical convergence diagnostics (e.g., acceptance rates, trace plots) instead.

### Minor

- **The case study (Section 4.5, Figure 5(a)) uses undefined baseline acronyms.** The figure legend mentions SLP, SR, and SVTOD, none of which are defined in the paper. The four baselines listed in Section 4.1 are BoN, SoP, SVDD, and FK — none match SLP/SR/SVTOD. This makes the central detoxification comparison in Figure 5(a) uninterpretable as presented. (Note: the apparent "IterRef" vs "Ours" duplication is a parser artifact from the image alt-text.)

- **No error bars, confidence intervals, or variance reporting on any quantitative result.** Figures 2 and 4, and Tables 1, 2, and 3 all report only point estimates. The text notes each setting is "sampled 20 times" (line 182) but does not report the variance. Without this information, the reader cannot assess whether IterRef's consistent advantage over baselines is statistically significant. Standard practice in this literature (e.g., the cited FK Steering and SVDD papers) includes such reporting.

- **The NFE-based cost accounting aggregates reward-model calls and generative-model calls into a single metric** (line 186), which the paper itself acknowledges "may obscure meaningful differences" (line 175) since the relative costs differ across model scales. The paper references a wall-clock analysis in Appendix C.4, but the main paper's efficiency claims (including the "8× faster" headline) cannot be fully evaluated on NFE counts alone without this analysis being prominently presented.

- **The "Evenly" comparison in Table 2 is underspecified.** The caption says it applies IterRef at every timestep "under the same total cost" as a single selected step, but the paper does not explain how compute parity is achieved. This makes the comparison between applying refinement at a single timestep versus all timesteps hard to interpret.

- **The claim about Table 3 oversimplifies the pattern.** The text (line 287) states "increasing iterations is more effective than simply generating more particles." However, the best configuration is k=8, N=4 (not the highest k values k=16, N=2 and k=32, N=1, which perform worse), suggesting a more nuanced optimum than "more iterations is always better."

### Trivial

- **Eq. 3 has a minor parentheses mismatch.** The expression `exp((r(x_t') - r(x_t)/α))` should read `exp((r(x_t') - r(x_t))/α)` — the closing parenthesis for the numerator is misplaced.

## Nice-to-Haves

- Include a comparison with PG-DLM (Dang et al., 2025, cited in Related Work), which also uses MCMC-based refinement for discrete diffusion and is the closest methodological relative.
- Report empirical acceptance rates of the MTM proposals in practice — this would help readers understand when and why the method works.
- Refine the "selective refinement" claim (Section 3.3) to acknowledge that SMC methods can also be designed to allocate compute adaptively.

## Removed Points

The following points from the input review were removed after fact-checking against the paper:

1. **"Both [noising and denoising] operations are counted equally as NFEs."** — Factually incorrect. The paper counts "diffusion-model calls" (line 174), meaning p_θ denoising calls. The noising step q(x_s|x_t) is a cheap random masking operation that is NOT counted as an NFE.

2. **"Algorithm 1 may not be present."** — Algorithm 1 is present in the paper (lines 91–100, formatted as a code block).

3. **"Without [wall-clock analysis], the central efficiency claim cannot be evaluated."** — The wall-clock analysis is in Appendix C.4, which was stripped by the parser (all appendices are removed from every paper). Speculating about absent appendix content is not a valid criticism.

4. **"The claim that test-time scaling is 'comparatively less explored' is overstated."** — The paper uses "comparatively less explored" and acknowledges existing methods in its Related Work. Too subjective and minor to retain.

5. **"Missing comparison with PG-DLM."** — Requesting an additional baseline is a nice-to-have suggestion, not a weakness. The paper already compares against four baselines across three models and five tasks.

6. **"Overstated selective-refinement advantage over SMC."** — A subjective scope-creep argument about what SMC can or cannot do.

## Novel Insights

None beyond the paper's own contributions. The review confirms the paper's claimed strengths (principled MTM framing, consistent empirical gains) and sharpens the weaknesses that the authors should address, but does not surface any unexpected finding about the method.

## Suggestions

- Reframe Proposition 1 transparently: state the convergence result as a property of the MTM framework under idealized conditions (when q and p_θ form a reversible kernel), acknowledge that learned p_θ only approximately satisfies this, and provide empirical diagnostics (acceptance rates, distributional convergence checks) to demonstrate practical behavior.
- Define all baseline acronyms used in Figure 5(a) explicitly in the main text, or align them with the four baselines defined in Section 4.1.
- Add error bars or confidence intervals to all quantitative results (Figures 2, 4; Tables 1–3).
- Clarify how the "Evenly" condition in Table 2 achieves compute parity when refinement is applied at every timestep versus a single selected step.
- Move the wall-clock comparison to the main paper (not only the appendix) to substantiate the "8× faster" efficiency claim, or replace NFE-based accounting with honest time-based comparisons.

## Score and Decision

**Calibration anchoring:** The paper was compared against 22 calibration anchors across all score bands. The most topically similar anchors are:
- **DDPP** (Ombm8S40zN, avg 6.25, Accept): Steering discrete diffusion models. Had wider domain coverage (incl. proteins, wet-lab) but also more severe weaknesses (missing baselines at -3.71 favorability). IterRef has a cleaner inference-time method but narrower domain scope.
- **DRAKES** (G328D1xt4W, avg 6.00, Accept): Fine-tuning discrete diffusion with RL. Had severe theory concerns (-3.79 favorability) but strong biological validation.
- **DNO** (x1uv2gdjKV, avg 5.50, Reject): Inference-time alignment. Had more severe missing-baseline issues (-2.61) and evaluation gaps.
- **UDLM** (i5MrJ6g5G1, avg 5.25, Accept): Uniform discrete diffusion. Had overclaimed contributions (-1.08) and novelty concerns (-3.59).
- **SVDD** (2fgzf8u5fP, avg 3.80, Reject): Derivative-free guidance. Had unfair comparisons and unverified theoretical approximations.

IterRef's worst weakness (undefined case-study baselines, favorability -1.41) is less severe than the worst weaknesses of DDPP (-3.71), DRAKES (-3.79), UDLM (-3.59), and DNO (-2.61). However, IterRef lacks the wet-lab validation of DDPP/DRAKES and the modality breadth of DDPP. The paper's strengths (MTM framing at 13.00 favorability, consistent empirical trends) are comparable to these anchors' strengths.

Round-1 bracket: 3.5–7.5 → Round-2 bracket: 5.0–6.5 → Final: **5.5**

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>