## Summary
IterRef proposes a test-time scaling method for discrete diffusion models that iteratively refines intermediate denoising states via Multiple-Try Metropolis (MTM). The key technical contribution is a noising-denoising transition kernel paired with a balancing function (Eq. 2) that collapses importance weights to uniform while concentrating all reward information in a simple Metropolis acceptance ratio, enabling principled in-situ refinement without the error-accumulation problems of sequential one-pass methods. Evaluation spans three backbones (MDLM, LLaDA-8B, MaskGIT), five reward functions, and both text and image modalities, with consistent improvements over baselines.

---

## Strengths
- **Elegant MTM simplification (Eq. 2–3):** The choice of balancing function λ causes the N importance weights to collapse to w_n = 1/N, reducing candidate selection to uniform sampling and the acceptance step to a standard Metropolis test on rewards. This halves practical cost while preserving MTM's theoretical guarantees — a non-obvious and clean contribution.
- **Non-trivial k vs. N finding (Table 3, Figure 4):** At equal compute, k=8,N=4 achieves Toxicity=54.0, CoLA=85.3 on LLaDA versus k=1,N=32 giving only 3.3 and 8.7. This dramatic gap across all three tasks directly validates the method's core thesis that iterative in-situ refinement outperforms broad one-step particle search.
- **Novel effective-timestep finding (Table 2):** Later denoising stages (0.1T) consistently dominate earlier ones for discrete diffusion — the opposite of continuous diffusion's early-step dominance. CoLA: 87.0 at 0.1T vs. 23.3 at 0.9T at equal budget. This is an actionable, independently interesting empirical result.
- **Breadth of evaluation:** Three backbones covering 1B-class (MDLM), 8B (LLaDA-8B), and image (MaskGIT) settings with five reward functions and consistent gains meaningfully strengthens the generalization claim.

---

## Weaknesses

### Fatal
None.

### Major
- **NFE metric conflation undermines headline efficiency claims (Section 3.3, Figures 1–2):** The "8× faster" headline on Figure 1(b) rests on aggregate NFE, which treats reward-model and diffusion-model calls equally. Section 3.3 explicitly acknowledges this is imperfect: for LLaDA-8B, diffusion-model calls dominate cost; for MDLM, both are comparable. IterRef and baselines such as BoN (which runs full T-step trajectories before calling reward once) have structurally different cost breakpoints at equal NFE. A wall-clock analysis is deferred to Appendix C.4 (unavailable to readers of the main submission). Without this, readers cannot independently verify the headline efficiency claim. This is an evidential gap rather than a structural flaw — if the wall-clock results in the appendix support the NFE results, the contribution stands — but the main text should summarize those results rather than leaving efficiency as an assertion.

### Minor
- **Table 2 setup description is ambiguous:** The caption states "applying IterRef evenly at every timestep under the same total cost," while Section 4.4 says "we fix the total computational budget by allocating 4T NFEs at each selected step." Under the most consistent reading, each single-step configuration and "Evenly" share the same 4T total NFE budget — but "Evenly" distributes that budget across all steps, receiving far less per timestep. This interpretation makes "Evenly" winning on three of four tasks more striking but changes how the CoLA result (87.0 at 0.1T, 83.0 evenly) should be read. The ambiguity weakens what is otherwise the paper's most interesting empirical finding.
- **Reversibility assumption in Proposition 1 not discussed practically:** The convergence guarantee requires "q and p_θ form a reversible Markov kernel." For a learned neural network denoiser approximating p_θ, this assumption is non-trivial and likely violated in practice. There is no discussion of how sensitive the guarantee is to this violation, leaving the theoretical contribution partially ungrounded.
- **No diversity or quality analysis as compute scales:** Reward scores increase monotonically with compute (Figure 2), but there is no analysis of output diversity or degradation in text quality. For the safety alignment use case (Section 4.5), this matters — reward over-optimization could produce low-toxicity but lexically monotone or incoherent outputs. The ethics statement mentions this issue ("diagnose reward over-optimization") but the paper does not empirically address it.

### Trivial
- **Figure 5(a) baseline labeling inconsistency:** The image labels methods as "SLP," "SR," and "SVTOD," while the main text and baselines section refer to BoN, SoP, SVDD, FK. Also, both "IterRef" and "Ours" appear as separate legend entries in the image description. These are likely image-labeling or parser artifacts that should be corrected for clarity.

---

## Nice-to-Haves
- A plot of the intermediate-state reward distribution after 1, 2, 4, 8 MTM iterations (on x_t, not x_0) would sharpen the mechanistic account of why k dominates N — separating "exploration via noising" from "MCMC acceptance" contributions.
- The timestep finding (Table 2) would be more principled with a brief mechanistic explanation linking it to the absorbing-state structure: at 0.1T, few tokens remain masked, making targeted refinement highly impactful; at 0.9T, most tokens are still masked and reward guidance has little structure to act on.
- A brief summary of wall-clock results in the main text (e.g., one table row or a single sentence in Section 4.2) would make the efficiency argument self-contained.
- An analysis of when IterRef is expected to underperform (e.g., the LLaDA CoLA case where BoN wins because LLaDA already generates well-formed text) would sharpen the method's practical scope.

---

## Removed Points
*These points are flagged as removed; treat with caution.*

- **Pool reuse theoretical concern (Harsh Critic, Section 3.3):** Critic claimed reusing rejected candidates holds only under "specific conditions." However, Section 3.3 states: "the candidates were already drawn i.i.d. from the same transition kernel, the pool remains a valid proposal set." Within the MTM framework this is correct — rejected proposals maintain the same distributional validity for the next step. REMOVED: not a valid weakness.
- **BoN CoLA failure analysis incomplete:** The paper explicitly acknowledges: "on CoLA, Best-of-N (BoN) achieves larger gains, which can be attributed to the fact that LLaDA already generates a linguistically well-formed text." The paper provides a clear explanation. REMOVED: paper adequately addresses this.

---

## Novel Insights
The most genuinely novel scientific observation is the effective-timestep asymmetry (Table 2): discrete diffusion benefits most from reward guidance at *late* denoising stages (0.1T), while continuous diffusion's analogous guidance concentrates at early stages. This asymmetry likely traces to the absorbing-state formulation — at 0.1T, the sequence has mostly converged with only a few masked positions remaining, so reward-guided refinement of those positions has maximal discriminative power; at 0.9T, the state is still largely masked and reward evaluation is dominated by denoising variance. This has direct practical implications: practitioners can concentrate IterRef's compute budget near the end of the denoising trajectory rather than distributing it uniformly, achieving nearly equivalent gains at a fraction of the cost (CoLA: "Evenly"=83.0 vs 0.1T=87.0 at the same total budget).

---

## Suggestions
1. **Add a brief wall-clock summary to the main text** (even a single sentence or one table row) to make the efficiency claim independently verifiable without relying on the appendix.
2. **Separate NFE into diffusion-model calls and reward-model calls** in a supplementary table to resolve the metric conflation structurally without changing the main presentation.
3. **Clarify Table 2 setup:** explicitly state whether each single-step configuration uses the same total budget as "Evenly," and if so, note that "Evenly" receives far less budget per timestep.
4. **Add a brief discussion of Proposition 1's reversibility assumption** and its practical implications (e.g., empirical MCMC mixing approximation in practice).
5. **Add a diversity metric** (e.g., self-BLEU or distinct-n) alongside reward scores in Figure 2 to address reward over-optimization concerns, particularly for the safety alignment case study.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Ombm8S40zN (Steering Masked Discrete Diffusion / DDPP) | 6.25 | R1 | Directly comparable; requires training; narrower evaluation |
| pq1WUegkza (Convergence of Score-Based Discrete Diffusion) | 7.00 | R1 | Theory-focused, fewer experiments; comparable rigor |
| peNgxpbdxB (Scalable Discrete Diffusion Samplers) | 6.00 | R1 | New training methods; narrower scope |
| XsgHl54yO7 (Unlocking Guidance for Discrete State-Space) | 6.50 | R1 | Principled guidance for discrete diffusion; narrower modality |
| 2fgzf8u5fP (SVDD derivative-free guidance) | 3.80 | R1 | Closely related baseline, weaker evaluation, rejected |
| 4hFT4rfG40 (Plug-and-Play Controllable Generation for Discrete Masked) | 3.75 | R1 | Closely related; weaker formalism and evaluation |
| shgx0eqdw6 (ARGS: Alignment as Reward-Guided Search) | 7.00 | R2 | Reward-guided generation, autoregressive; similar breadth |
| G328D1xt4W (Fine-Tuning Discrete Diffusion via Reward Optimization) | 6.00 | R2 | Training-based; narrower scope; same domain |
| 1vmSEVL19F (DRaFT) | 6.00 | R2 | Fine-tuning approach; comparable evaluation breadth |
| 4w99NAikOE (IterComp) | 6.80 | R2 | Iterative feedback learning; broader composition task |
| OlzB6LnXcS (Shortcut Models) | 8.00 | R1 | Diffusion acceleration; different problem but high quality |

**Round 1 bracket:** 6.0–7.5, based on closest analogues (DDPP at 6.25, Convergence paper at 7.0, Unlocking Guidance at 6.5).

**Round 2 narrowing:** IterRef is training-free (stronger practical utility than DDPP or G328D1xt4W), has broader evaluation (3 backbones, 5 rewards, 2 modalities), and includes a novel empirical discovery (timestep asymmetry) alongside the method. The NFE metric conflation is a real but evidential weakness. The contribution is meaningfully stronger than the 6.0 cluster; the cleanliness of the formulation and breadth of evidence bring it closer to 7.0.

**Final score: 7.0 — Accept.** The method is principled, the simplification is technically clean, the empirical evidence is unusually broad for this type of paper, and the timestep finding has independent scientific value. The main weakness (NFE conflation without a main-text wall-clock summary) is evidential rather than structural and should be resolved in camera-ready revision.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>