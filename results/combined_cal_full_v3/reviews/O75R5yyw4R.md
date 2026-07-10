Now let me write the final review.

Let me compile all calibration anchors for the final report:

**All anchors retrieved:**
- Round 1:
  - Strong reject (<1.5): u1cQYxRI1H.md (0.50), bEgDEyy2Yk.md (1.00), Uj0h13lVrR.md (1.00), 5lUdTogEL3.md (1.00)
  - Reject (1.5-3.5): 46tjvA75h6.md (3.00), W4djmqKZC6.md (3.00), vK8C37eHXM.md (3.20), SEvJfuCtPY.md (3.00)
  - Middle (3.5-5.5): D7PQ54l5Q1.md (4.75), Qn4HEhezKW.md (5.00), 1hT2fsHbK9.md (5.25), nHESwXvxWK.md (4.00)
  - Stronger (5.5-7.5): pq1WUegkza.md (7.00), 0FbzC7B9xI.md (6.60), uZ5K4HeNwd.md (7.00), MJNywBdSDy.md (5.75)
  - Top (7.5-8.5): fV0t65OBUu.md (8.00), tyEyYT267x.md (8.00), xDrFWUmCne.md (8.00), EO8xpnW7aX.md (8.00)
- Round 2:
  - (5.0-6.5): FfIognyBee.md (5.25), iIGNrDwDuP.md (5.25), 1vmSEVL19f.md (6.00), Ombm8S40zN.md (6.25)
  - (3.5-5.5): Qn4HEhezKW.md (5.00), 2fgzf8u5fP.md (3.80), i5MrJ6g5G1.md (5.25), 4hFT4rfG40.md (3.75)

**Anchors itemized:** MJNywBdSDy.md (5.75), D7PQ54l5Q1.md (4.75), pq1WUegkza.md (7.00), Ombm8S40zN.md (6.25), sL2F9YCMXf.md (6.75), 2fgzf8u5fP.md (3.80), 1vmSEVL19f.md (6.00)

**Round-1 bracket:** 5.0 – 6.5
**Narrowing:** The closest comparable anchors are:
- DDPP (Ombm8S40zN.md, 6.25): Stronger empirical rigor (error bars, wet-lab validation), but IterRef has cleaner method and iteration insight. DDPP's weaknesses were mostly moderate (5.78, 7.59 favorability), while IterRef's weakness favorabilities are lower (2.61-3.82 range for major issues).
- DRaFT (1vmSEVL19f.md, 6.00): Much higher strength favorabilities (10.24-13.62) vs IterRef's (8.70-11.10). DRaFT's weakest concerns had similar low favorability.
- Planned Denoising (MJNywBdSDy.md, 5.75): Similar level of concerns. IterRef has broader empirical validation.

The key comparison: IterRef lacks error bars (fav 2.61) and has an unverified convergence assumption (fav 3.82). These low-favorability items push the paper below the 6.0-6.25 level of DDPP and DRaFT. The iteration-vs-particles insight (strength fav 8.70) is a genuinely distinctive finding that not all anchors share. The paper sits between the 5.25 anchors (rejected) and the 6.0-6.25 anchors (accepted). 

Final score: **5.5**, Decision: **Accept** (borderline/weak accept - the contribution is real and the method is well-designed, but substantial evidential gaps need addressing in revision).## Summary

This paper introduces IterRef, a test-time scaling method for discrete diffusion models that uses MCMC-based iterative refinement to steer intermediate states toward higher reward. The method frames reward-guided sampling within the Multiple-Try Metropolis (MTM) framework, with a carefully chosen transition kernel (noising-denoising) and balancing function that make importance weights uniform and the acceptance ratio collapse to a simple reward comparison. Experiments across text (MDLM, LLaDA-8B) and image (MaskGIT) domains with multiple reward functions show consistent improvements over baselines, and an insightful ablation demonstrates that increasing refinement iterations yields larger gains than increasing parallel particles.

## Strengths

- **Principled method design grounded in a well-established framework.** The paper correctly identifies that existing reward-guided sampling methods for discrete diffusion lack a mechanism for correcting intermediate states. Framing the solution within Multiple-Try Metropolis (MTM) and designing the transition kernel (noising-denoising via q and p_θ) and balancing function λ so that importance weights become uniform and the acceptance ratio collapses to a simple reward comparison (Eq. 3) is elegant and theoretically motivated. [favorability=9.64]

- **Consistent empirical advantage across modalities and backbones.** Figure 2 shows IterRef outperforming FK, SVDD, SoP, and BoN on both MDLM and LLaDA-8B across four reward functions. The gains at low compute budgets (e.g., 2T–4T NFEs matching or exceeding baselines at 32T on MDLM) are striking. Table 1 extends this to image generation (MaskGIT) with CLIPScore, and qualitative examples in Figure 3 support the quantitative results. [favorability=11.10]

- **Demonstration that iteration matters more than parallel particles.** Table 3 shows that keeping N×k fixed, increasing k (iterations) at the expense of N (particles) yields substantially better results (e.g., k=8, N=4 gives Toxicity=54.0 vs. k=1, N=32 gives Toxicity=3.3), directly validating the paper's central thesis that iterative refinement is the mechanism driving improvement. [favorability=8.70]

- **Clean practical tricks.** The pool-reuse strategy (Section 3.3) that eliminates the need to regenerate backward proposals at each MTM iteration, and the reuse of rejected proposal pools, meaningfully reduce computational overhead. [favorability=9.05]

## Weaknesses

### Fatal

None.

### Major

- **No error bars or confidence intervals on language experiments.** The language evaluation uses 15 prompts × 20 samples = 300 generations per condition (Section 4.1), yet no variance estimates, confidence intervals, or standard errors are reported anywhere in the paper. Text generation with diffusion LMs is inherently variable; without error bars, the reader cannot assess whether reported margins (e.g., "IterRef achieves higher reward scores with only 2T NFEs than all baselines obtain with 32T NFEs") represent genuine improvement or sampling noise. This is a significant evidential gap for a paper making strong quantitative speedup claims. [favorability=2.61]

- **Convergence guarantee (Proposition 1) relies on an unverified reversibility assumption.** The proposition assumes that q (the forward noising process) and p_θ (the learned reverse denoising process) "form a reversible Markov kernel." For a masking-based discrete diffusion model, this requires p_θ(x_t'|x_s) q(x_s|x_t') = p_θ(x_t|x_s) q(x_s|x_t), which is not enforced by the standard ELBO training objective. Trained diffusion models do not generally satisfy detailed balance with the forward process. The paper states this assumption without discussing its plausibility or providing empirical diagnostics (e.g., trace plots, acceptance rates, convergence checks). The theoretical guarantee that distinguishes IterRef from heuristic methods may not apply in practice. [favorability=3.82]

- **Key hyperparameters (N, k, α, effective timestep set U) not reported for the main experiments.** Algorithm 2 lists these as inputs, and Table 2 shows the choice of U is highly consequential (e.g., Sentiment: 97.0 with "Evenly" vs. 37.6 at 0.1T). Yet the main text reports only denoising step counts (1000 for MDLM, 64 for LLaDA, 50 for MaskGIT) without specifying the actual values of N, k, α, or which timesteps were in U for each experiment. This makes it impossible to assess whether hyperparameters were tuned per task or to reproduce the results. [favorability=3.57]

### Minor

- **The NFE-based cost accounting conflates generative-model and reward-model calls, and the paper acknowledges this but does not fully address it in main results.** Section 3.3 states that "aggregating these into a single NFE value may obscure meaningful differences, and it is preferable to report generative-model calls and reward-model calls separately." Yet all main results (Figure 2, Table 1) use a unified NFE axis. While IterRef calls the reward model once per proposal per refinement step, baselines like BoN call it once per trajectory. If reward-model evaluations are substantially cheaper than diffusion model calls (which is typical), IterRef's NFE count may understate its true efficiency advantage. Wall-clock analysis is deferred to the appendix. [favorability=5.85]

- **Intermediate reward approximation is used without discussion of its impact.** The paper approximates r(x_t) by evaluating the reward on the diffusion model's prediction of x_0 from x_t (Section 3.1, citing prior work). The reward of a one-step x_0 prediction from a partially masked state may be a poor proxy for the expected reward over all completions of x_t. The paper does not analyze how this approximation affects the acceptance ratio β or the refinement loop. [favorability=4.02]

- **Adaptation of continuous-diffusion baselines (SoP, SVDD) to discrete diffusion is not explained.** SoP (Ma et al., 2025) and SVDD (Li et al., 2024) were originally designed for continuous diffusion, but the paper does not describe how they were adapted to discrete state spaces. FK Steering is the most directly relevant baseline and its comparison is informative, but the inclusion of SoP and SVDD without adaptation details is a gap. [favorability=2.29]

### Trivial

- **Typo in Eq. 3:** The acceptance rate is written as β = min(1, exp((r(x_t') - r(x_t)/α))). This is missing a parenthesis; it should be β = min(1, exp((r(x_t') - r(x_t))/α)). As written, only r(x_t) is divided by α, which would break the symmetry needed for detailed balance. [favorability=4.35]

- **Algorithm 2 notation inconsistency:** Line 7 selects variable "x_t'" while Line 9 references "x_t'^{cand}" — these appear to be the same variable. [favorability=2.44]

## Nice-to-Haves

- Report acceptance rates, trace plots of reward over refinement iterations, and other empirical MCMC mixing diagnostics to support the convergence claim.
- Include a wall-clock time version of Figure 2 in the main paper (currently only in the appendix).
- Discuss why BoN outperforms IterRef on CoLA with LLaDA-8B more thoroughly — this is a meaningful failure mode where refinement of already well-formed text may be counterproductive.

## Removed Points

**These points are flagged to be removed, treat them with caution:**

- *"Figure 5's caption appears garbled"* — The caption lists IterRef (blue) and Ours (red) separately. This appears to be a parser artifact from the embedded figure; it is not treated as an author error.
- *"The 8× faster claim is based on one comparison and may not generalize"* — The paper properly contextualizes this claim as specific to the Toxicity task with MDLM, and the abstract says "up to 8×." This is appropriately scoped.
- *"BoN outperforms IterRef on CoLA with LLaDA — deserves more discussion"* — The paper already acknowledges and briefly discusses this (Section 4.2): "on CoLA, Best-of-N (BoN) achieves larger gains, which can be attributed to the fact that LLaDA already generates a linguistically well-formed text."
- *"Strengthening the Paper on Its Own Terms" generic suggestions about reporting acceptance rates* — These are suggestions for improvement, not weaknesses identified in the paper as submitted.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add error bars or confidence intervals to all language-generation line plots (Figure 2). The 300-generation evaluation is sufficient to compute standard errors.
- Report hyperparameter values (N, k, α, U) for each main experiment in a table.
- Add empirical MCMC diagnostics (acceptance rates, reward traces over refinement steps) to support the convergence claim.
- Include a version of Figure 2 with disaggregated NFE (generative-model calls vs. reward-model calls) or wall-clock time in the main paper.

## Score and Decision

**Calibration anchors (all rounds):**

| Round | Path | Avg Score | Itemized | Comparison |
|-------|------|-----------|----------|------------|
| R1 | u1cQYxRI1H.md | 0.50 | No | Strong reject (unrelated topic) |
| R1 | bEgDEyy2Yk.md | 1.00 | No | Strong reject (unrelated topic) |
| R1 | 46tjvA75h6.md | 3.00 | No | Reject (MCMC + EBM, different subfield) |
| R1 | D7PQ54l5Q1.md | 4.75 | Yes | Reject — MCMC + diffusion for inverse problems; weaker contribution |
| R1 | 1hT2fsHbK9.md | 5.25 | No | Reject — diffusion samplers theory; weaker empirical work |
| R1 | MJNywBdSDy.md | 5.75 | Yes | Accept — discrete diffusion with planning; similar scope and quality |
| R1 | 0FbzC7B9xI.md | 6.60 | No | Accept — truncated diffusion sampling; different area |
| R1 | pq1WUegkza.md | 7.00 | Yes | Accept — discrete diffusion theory; stronger theoretical contribution |
| R1 | uZ5K4HeNwd.md | 7.00 | No | Accept — diffusion language models distillation |
| R1 | fV0t65OBUu.md | 8.00 | No | Accept — diffusion covariance matching; stronger theory |
| R2 | FfIognyBee.md | 5.25 | No | Reject — diffusion fine-tuning for text-to-image |
| R2 | 1vmSEVL19f.md | 6.00 | Yes | Accept — DRaFT diffusion fine-tuning; stronger empirical rigor |
| R2 | Ombm8S40zN.md | 6.25 | Yes | Accept — DDPP steering discrete diffusion; most directly comparable |
| R2 | sL2F9YCMXf.md | 6.75 | Yes | Accept — energy-based diffusion LMs |
| R2 | 2fgzf8u5fP.md | 3.80 | Yes | Reject — derivative-free guidance; fundamental flaws |
| R2 | 4hFT4rfG40.md | 3.75 | No | Reject — plug-and-play controllable generation |

**Round-1 bracket:** 5.0 – 6.5 (between the 5.25 papers that were rejected and the 6.0+ papers that were accepted). **Narrowing:** The DDPP anchor (6.25, accepted) is most directly comparable — both address reward-guided discrete diffusion. DDPP had stronger empirical rigor (including error bars and wet-lab validation) but greater novelty concerns. IterRef's weakness favorabilities (2.61, 3.82, 3.57 for the three major issues) are lower than DDPP's (5.78, 7.59), primarily due to the absence of error bars and the convergence assumption gap. The iteration-vs-particles insight (strength fav 8.70) is a genuinely distinctive finding. The paper sits between the 5.25 anchors (rejected) and the 6.0–6.25 anchors (accepted), slightly closer to the latter due to its clean method and consistent cross-modal evidence.

**Final score: 5.5** — The paper presents a well-designed, principled method with strong empirical results across modalities. The core contribution (iterative refinement via MTM with practical simplifications) is genuine. However, the absence of error bars on strong quantitative claims, the unverified convergence assumption, and unreported hyperparameters prevent the paper from reaching the 6.0+ level. These issues are fixable and do not threaten the core contribution.

**Decision: Accept** (borderline/weak accept — the method is valuable and the empirical results are broadly positive; the evidential gaps should be addressed in the camera-ready revision).

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>