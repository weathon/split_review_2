## Summary

This paper introduces **IterRef**, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) with noising-denoising transitions to iteratively refine intermediate states toward reward-aligned distributions. The method is evaluated across two language backbones (MDLM, LLaDA-8B) and one image backbone (MaskGIT) with multiple reward functions, showing consistent improvements over baselines.

---

## Strengths

1. **Principled method design (Section 3).** The framing of test-time refinement for discrete diffusion as a Multiple-Try Metropolis chain with noising-denoising transitions is genuinely novel and well-motivated. The transition kernel $K(x_t, x_t') = \sum_{x_s} q(x_s|x_t)p_\theta(x_t'|x_s)$ captures the correct intuition — add noise to explore, denoise to restore consistency, and use reward information to steer selection. This is the paper's core intellectual contribution and it is sound.

2. **Theoretical grounding (Proposition 1).** The paper provides a convergence guarantee — the Markov chain satisfies detailed balance and converges to $p^*(x_t)$ as $k \to \infty$. Even though the proof relies on assumptions that may not hold exactly in practice, providing this formal framework is a significant step beyond purely heuristic approaches.

3. **Broad empirical evaluation (Sections 4.2–4.3).** The method is tested across two language backbones (MDLM, LLaDA-8B) and one image backbone (MaskGIT) with 4–5 different reward functions. This is substantially more comprehensive than most inference-time guidance papers, which typically focus on a single modality or backbone.

4. **Interesting finding about timestep dynamics (Section 4.4, Table 2).** The observation that later denoising stages matter more for discrete diffusion — in contrast to continuous diffusion where early stages dominate — is a genuinely useful insight for future work, regardless of IterRef's own performance.

---

## Weaknesses

### Fatal

None.

### Major

1. **Temperature parameter $\alpha$ is never reported, despite being central to the method.** The hyperparameter $\alpha$ controls the KL/reward trade-off (Eq. 2, line 57) and directly enters the acceptance probability $\beta = \min(1, \exp((r(x_t') - r(x_t))/\alpha))$ (Eq. 3). This determines how aggressively the method optimizes reward versus staying close to the pretrained distribution. The paper never reports what value(s) of $\alpha$ were used, nor whether it was tuned separately per backbone, per task, or per baseline. Without this information, the reader cannot assess whether the comparison is fair — a tiny $\alpha$ could achieve high reward while generating degenerate text that perplexity/CoLA metrics might not fully capture, especially since CoLA and Perplexity themselves are used as reward signals in some experiments. This is a structural gap.

2. **NFE metric used despite the paper's own acknowledgment of its inadequacy.** Section 3.3 (line 174) states: *"aggregating these into a single NFE value may obscure meaningful differences, and it is preferable to report generative-model calls and reward-model calls separately."* Yet Section 4.1 (line 186) does the opposite: *"treat the reward model and the generative model on equal footing."* This matters because IterRef makes proportionally more reward-model calls per generative-model call than some baselines. For MDLM, the paper acknowledges the two have "comparable computational footprints," so NFE may systematically favor IterRef by undercounting the cost of generative-model-heavy baselines. Wall-clock analysis is promised in Appendix C.4 but absent from the main paper.

3. **No variance estimates, confidence intervals, or error bars anywhere.** All plots (Figures 2, 4, 5) and tables (Tables 1–3) report only point estimates with no indication of variability. The paper uses 20 samples per prompt for language tasks (300 generations per condition) and 50k conditional generations for images — these sample sizes are modest enough that variance matters. Without it, the reader cannot assess whether IterRef's reported gains over the strongest baselines are statistically significant, whether the method is stable across runs (MCMC methods can have high variance with finite $k$), or whether claims like "8× faster" would hold with confidence intervals.

4. **Contradiction between Algorithm 2 and Section 3.3 regarding backward proposals.** Algorithm 2, line 8 explicitly states: *"Propose $N-1$ auxiliary samples $\{x_t''^{(n)}\} \sim K(x_t', \cdot)$"* — the standard MTM backward resampling step. The accompanying text (line 156) also describes generating auxiliary proposals. However, Section 3.3 (line 164) claims: *"the acceptance rate can be evaluated without the need for resampled proposals $x_t''$... Consequently, the practical implementation eliminates the resampling step and reduces the per-iteration cost by nearly half."* Either the algorithm generates backward proposals (in which case the "nearly half" cost saving is a misstatement) or it does not (in which case the pseudocode is wrong and detailed balance may be violated). This needs to be resolved.

5. **"8× faster" claim in Figure 1 is not supported for the setting it depicts.** Figure 1(b) and its caption (line 27) claim IterRef is "up to 8× faster than baselines with safety reward on LLaDA-8B (See §4.5 for details)." However, the only quantitative 8× claim in the text (line 200–201) is for *MDLM on Toxicity* — a different model and setting. Section 4.5 (LLaDA-8B detoxification) does not make an 8× claim; it reports toxicity reduction below 10% "starting from 4× computational budget." The visual headline and the textual evidence are inconsistent. Either the quantitative support for LLaDA-8B should be provided, or the claim should be restricted to the setting where it is actually demonstrated.

### Minor

1. **The reversibility assumption in Proposition 1 is non-trivial for absorbing-state diffusion.** Proposition 1 assumes $q$ and $p_\theta$ form a *reversible* Markov kernel. In the absorbing-state (masking) formulation used by all three backbones (MDLM, LLaDA, MaskGIT), the forward masking process destroys information (tokens become masks) and is not reversible. The learned denoising process is only an approximation. The convergence guarantee therefore rests on an assumption that is not satisfied by any of the evaluated models. The paper should explicitly acknowledge this and discuss the practical implications.

2. **Intermediate reward approximation is stated but not discussed.** The paper defines $r(x_t) = \alpha \log \mathbb{E}[\exp(r(x_0)/\alpha) \mid x_t]$ (line 61) and states it "can approximate by evaluating the reward function on the diffusion model's prediction of $x_0$" (line 117). This approximation is central to the method's practical correctness — the convergence guarantee in Proposition 1 applies to the distribution defined via this *approximated* intermediate reward, not the truly optimal distribution. The paper does not discuss the quality of this approximation or its potential impact on the guarantees.

### Trivial

None.

---

## Nice-to-Haves

- A sweep showing sensitivity to $\alpha$ would be the single most valuable addition. It would also help contextualize the method's robustness.
- Reporting wall-clock time for at least one representative setting (e.g., LLaDA-8B and MDLM) in the main paper would resolve the NFE tension.
- Adding confidence intervals or error bars to the main figures and tables would significantly strengthen the empirical claims.
- Including FID or similar quality metrics for the image experiment (Table 1) alongside CLIPScore would help assess whether IterRef maintains image quality while improving alignment.

---

## Removed Points

These points appeared in the input review but were removed after verification against the paper:

- **"Detoxification baselines (SLP, SR, SVTOD) differ from main experiment baselines"** — The image alt text listing these names is a parser artifact (it also lists "IterRef" and "Ours" as separate methods, which is nonsensical); the actual paper consistently uses FK, SVDD, SoP, BoN as baselines.
- **"Abstract claim unfair to SMC methods"** — A judgment call about rhetorical framing, not a factual error.
- **"No comparison to PG-DLM"** — The paper already includes 4 strong baselines; comparing every related method is not required.
- **"No discussion of failure modes or reward over-optimization"** — A generic criticism not specifically grounded in evidence from the paper.
- **"Ethics statement mentions increasing toxicity but main paper shows reduction"** — These experiments may be in the stripped appendix; the criticism is speculative.
- **"Evenly row wins 3/4 metrics in Table 2, undermining the finding"** — The "Evenly" result is consistent with the paper's presented findings and does not undermine them; it's a descriptive observation, not a weakness.

---

## Novel Insights

The input review correctly identifies that the unreported $\alpha$ parameter is not just a missing implementation detail but a structural gap that affects the interpretability of every result in the paper. Since $\alpha$ controls the acceptance probability $\beta = \min(1, \exp((r(x_t') - r(x_t))/\alpha))$, without its value the reader cannot distinguish between a method that genuinely improves alignment and one that simply accepts any proposal with slightly higher reward (small $\alpha$) and may be generating degenerate text. This is a more serious issue than a typical hyperparameter omission.

---

## Suggestions

1. Report the value(s) of $\alpha$ used for each experiment, and ideally include a sensitivity analysis showing how performance varies with $\alpha$.
2. Resolve the contradiction between Algorithm 2 and Section 3.3: either update the pseudocode to match the claimed efficient implementation, or remove the efficiency claim.
3. Harmonize the "8× faster" claim: either provide quantitative evidence for LLaDA-8B, or restrict the claim to MDLM-Toxicity.
4. Add wall-clock measurements (or at minimum break down generative-model calls vs. reward-model calls) for the main results.
5. Add error bars or confidence intervals to all figures and tables reporting results.

---

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>