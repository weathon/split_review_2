## Summary

This paper identifies a critical vulnerability in Masked Diffusion Language Models (MDLMs) called the "priming vulnerability," where affirmative tokens appearing at intermediate steps of the denoising process can steer the model toward generating harmful responses, even in safety-aligned models. The authors demonstrate this vulnerability through both intervention-based attacks (anchoring attack) and non-intervention attacks (First-Step GCG), and propose "Recovery Alignment" (RA), a safety alignment method that trains models to generate safe responses from contaminated intermediate states containing affirmative tokens. Experiments across three MDLMs show that RA significantly mitigates the priming vulnerability while maintaining general task performance and improving robustness against conventional jailbreak attacks.

## Strengths

- **Novel and important problem identification**: The paper identifies a previously unexplored vulnerability that is fundamentally specific to MDLMs' iterative denoising process, distinguishing it from ARMs' vulnerabilities. This opens a new research direction for DLM-specific safety research, which is timely given the growing interest in diffusion language models.

- **Rigorous characterization of the vulnerability**: The paper provides a thorough analysis across two threat models (with and without intervention in the denoising process), including a theoretical lower bound (Theorem 4.1) that enables efficient gradient-based attacks. The anchoring attack provides clean, controlled quantification of how early affirmative tokens can hijack generation.

- **Effective and well-motivated mitigation**: Recovery Alignment directly addresses the root cause of the vulnerability by training on contaminated intermediate states, rather than relying on ad-hoc defenses. The curriculum-based scheduling of intervention steps is principled and empirically validated. Comprehensive experiments show RA significantly outperforms existing alignment methods (SFT, DPO, MOSA) and maintains general capability across 11 benchmarks.

## Weaknesses

### Major
- **Limited theoretical grounding**: The monotonicity assumption in Theorem 4.1 is critical for the First-Step GCG attack but is not rigorously justified. The authors provide empirical validation in Appendix C.2, but the assumption that log-likelihood of the mask predictor is monotonically non-decreasing with denoising steps may not hold universally, especially near convergence when the model is highly confident. A more formal analysis of when this assumption breaks would strengthen the theoretical contribution.

- **Weak no-attack baseline for MMaDA**: MMaDA's original ASR is 79.7% even without any attack, meaning it is essentially already compromised. RA reduces this to 3.3%, which is impressive, but this model choice makes the evaluation less convincing because the model is not safety-aligned to begin with. The conclusions would be stronger if focused primarily on the LLaDA models that have pre-existing safety alignment.

- **Limited analysis of recovery alignment failure modes**: While the paper acknowledges that RA struggles with late intervention steps (t_inter=32) and strong attacks like ReNeLLM, there is no analysis of what causes these failures or how they might be addressed. Are these fundamental limitations of the approach, or could larger models or different training strategies overcome them?

- **Potential reward hacking concerns**: The paper mentions reward hacking with large t_max values in ablation studies, but does not provide systematic analysis of how reward model quality affects RA's effectiveness or how to detect/prevent reward hacking in practice.

### Minor
- **Scalability questions**: RA requires the same denoising process during training, which could be computationally expensive for larger models. The paper does not discuss computational overhead of training compared to baselines.

- **Limited evaluation of multi-turn attacks**: The paper evaluates conversational attacks (PAIR, ReNeLLM, Crescendo) but these are single-turn attacks adapted from ARMs. There is no evaluation of attacks specifically designed to exploit the iterative denoising process across multiple interactions.

### Trivial
- The term "priming vulnerability" is somewhat overloaded; the paper should clarify how it differs from input-level priming in ARMs (which they do, but the naming could cause confusion).

## Nice-to-Haves

- Explore DPO-style supervised variants of RA as mentioned in the limitations section
- Analyze how the priming vulnerability scales with model size and dataset composition
- Investigate whether similar vulnerabilities exist in continuous diffusion language models
- Provide guidance on selecting optimal t_max and total training steps S for practitioners

## Novel Insights

The paper's key insight—that the iterative denoising process of MDLMs creates a unique attack surface where intermediate affirmative tokens act as anchors that bias subsequent generation—is genuinely novel and extends beyond simple analogy to ARM vulnerabilities. The observation that conventional alignment (training only from fully masked sequences) provides no guarantee about behavior from contaminated intermediate states (Equation 6) is a theoretically grounded explanation for why existing safety methods fail. The recovery approach (training to recover from contaminated states) is conceptually elegant and differs fundamentally from adversarial training, as it teaches the model a "self-correction" capability rather than merely hardening against specific perturbations. This insight may have broader implications for other iterative generative models beyond MDLMs.

## Suggestions

1. Provide a more rigorous analysis of the monotonicity assumption in Theorem 4.1, including when it might fail and how sensitive the First-Step GCG attack is to violations of this assumption.

2. Include experiments on a safety-aligned variant of MMaDA (if available) to make the evaluation more consistent, or clearly separate results for models with and without pre-existing safety alignment.

3. Add analysis of what types of intermediate state contamination are most difficult for RA to recover from, potentially providing guidance for practitioners on expected robustness levels.

4. Consider evaluating on VLLMs or other multimodal diffusion models to test the generality of the priming vulnerability beyond text-only MDLMs.

## Score and Decision

This paper makes a solid contribution by identifying and characterizing a novel vulnerability specific to an emerging class of generative models (MDLMs), providing both theoretical and empirical analysis, and proposing an effective mitigation. The experiments are comprehensive across multiple models, benchmarks, and attack methods. While the theoretical analysis has some limitations, the empirical results strongly support the claims, and the practical impact is clear. The paper is well-structured and clearly written. I recommend acceptance.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>