## Summary

This paper identifies a "priming vulnerability" in masked diffusion language models (MDLMs) where affirmative tokens appearing at intermediate denoising steps can steer generation toward harmful responses, bypassing safety guardrails. The authors propose "Recovery Alignment" (RA), which trains MDLMs to recover safe responses from adversarially contaminated intermediate states, and demonstrate its effectiveness across three MDLMs and multiple attack types while preserving general capability.

## Strengths

- **Novel and well-motivated vulnerability identification.** The paper clearly articulates why MDLMs' iterative denoising mechanism creates a distinct safety risk compared to autoregressive models. The anchoring attack experiments (Figure 2) provide compelling evidence that even a single injected token at step 1 significantly raises ASR (e.g., 2% → 21% for LLaDA Instruct), and the effect scales sharply with intervention timing.

- **Theoretical contribution with practical impact.** Theorem 4.1 provides a principled lower bound on the full denoising objective, enabling First-Step GCG—a tractable, efficient surrogate for GCG attacks on MDLMs. This is both a theoretical insight and a practical attack that is ~20× faster than Monte Carlo GCG while achieving up to 4× higher ASR (Table 1), directly motivating the need for RA.

- **Comprehensive experimental evaluation.** The paper evaluates RA across three MDLMs (LLaDA Instruct, LLaDA 1.5, MMaDA MixCoT), two datasets (JBB-Behaviors, AdvBench), multiple attack families (anchoring, GCG, PAD, DiJA, PAIR, ReNeLLM, Crescendo), three evaluation metrics (GPT-4o, LLaMA Guard 3, keyword matching), and eleven capability benchmarks. This breadth strengthens confidence in the results.

- **Significant robustness improvements with minimal utility cost.** RA reduces ASR dramatically on priming attacks (e.g., LLaDA Instruct anchoring at t=8: 68.7% → 1.3%) and also improves robustness against conventional jailbreaks (Table 3: PAIR ASR drops from 44.3% to 10.0% on LLaDA). Table 4 shows general capability is preserved or even slightly improved across 11 benchmarks.

- **Well-designed ablation studies.** The ablations on intervention step scheduling (linear vs. uniform vs. constant, Figure 3b) and max intervention step (Figure 3a) provide actionable insights into the training dynamics and validate the linear curriculum design.

## Weaknesses

### Fatal
None.

### Major

- **Reliance on a single reward model without exploration of alternatives.** RA uses DeBERTaV3 as the reward model without fine-tuning or comparison to alternatives. The quality of the reward model is central to RA's effectiveness—reward hacking is mentioned as a concern with large t_max. A brief exploration of reward model choice or a discussion of sensitivity would strengthen the paper.

- **The monotonicity assumption (Theorem 4.1) deserves more justification.** The core theoretical result rests on log π_θ(r̃_{t+1}=r|q,r_t) ≥ log π_θ(r̃_1=r|q,r_0). While the paper references empirical validation in the appendix and provides intuitive reasoning (later steps have more context, concentrating probability mass), this assumption is not universally guaranteed and underpins the entire lower bound. The paper should more explicitly discuss when this assumption might fail (e.g., for adversarial or unusual inputs) and its implications for the tightness of the bound.

### Minor

- **MMaDA MixCoT has extremely high baseline ASR (79.7% without any attack).** This model appears poorly safety-aligned from the start, which makes it difficult to distinguish RA's benefit specifically for the priming vulnerability from general safety alignment benefits. The paper acknowledges this implicitly but could more clearly frame the MMaDA results as demonstrating RA's value as a general alignment method rather than purely a priming-vulnerability mitigation.

- **The generalization claim for conventional jailbreaks (Section 6.2) is somewhat speculative.** The proposed mechanism—that harmful tokens appear at intermediate steps regardless of attack type and RA-trained models can recover—is plausible but not directly validated. A targeted experiment measuring whether conventional attacks actually produce harmful intermediate tokens would strengthen this claim.

- **Training cost is not compared across methods.** RA requires 2,500 steps of RLHF-style training with multiple denoising rollouts per step. Comparing wall-clock training time and computational cost against DPO, SFT, and MOSA baselines would help practitioners assess the practical tradeoffs.

### Trivial
None.

## Nice-to-Haves

- An analysis of how RA interacts with different masking schedules or numbers of denoising steps T, which would clarify whether the vulnerability and mitigation are robust to MDLM design choices.
- Visualization of how RA changes the intermediate denoising trajectories (e.g., do contaminated states recover to safe states faster than in unaligned models?).
- Discussion of whether RA could be combined with existing methods (e.g., MOSA) for additive benefit.

## Novel Insights

The paper's central novel insight is that MDLMs' iterative denoising creates a distinct attack surface absent in autoregressive models: the appearance of affirmative tokens at intermediate steps can irreversibly steer generation toward harmful outputs because standard training (from fully masked sequences) never exposes the model to such contaminated states. This is a genuinely architecture-specific finding that does not simply transfer from ARM safety research. The practical consequence—that training on contaminated intermediate states (Recovery Alignment) both mitigates the specific vulnerability and improves robustness against conventional attacks—suggests a useful principle for diffusion model safety: robustness requires exposure to adversarial trajectories, not just adversarial inputs.

## Suggestions

- Add a controlled experiment verifying that conventional jailbreak attacks (PAIR, Crescendo) actually produce harmful tokens at intermediate MDLM steps, directly testing the proposed generalization mechanism.
- Include at least one alternative reward model (e.g., a different safety classifier or a custom-trained reward model) and report sensitivity of RA to reward model quality.
- Provide a comparison table of training costs (wall-clock time, GPU hours) across all methods to aid practical adoption decisions.
- Discuss the interaction between RA and MDLM design hyperparameters (T, masking schedule) to clarify the scope of the vulnerability.

## Score and Decision

This paper makes a novel and important contribution by identifying and systematically analyzing a previously unrecognized safety vulnerability specific to masked diffusion language models, and by proposing an effective, practical mitigation. The experimental evaluation is thorough across multiple models, attacks, and baselines, and the results convincingly support the claims. The theoretical contribution (First-Step GCG lower bound) adds rigor and practical value. While the reliance on a single reward model and the somewhat speculative generalization claim are real weaknesses, they do not undermine the paper's core contributions. The paper fills an important gap as MDLMs transition from research to deployment.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>