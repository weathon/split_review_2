## Summary

AUTO-RT is a reinforcement learning framework for automatic jailbreak strategy exploration that decomposes attack prompt generation into a strategy generation model and a strategy rephrasing model. It introduces Dynamic Strategy Pruning (DSP) to eliminate redundant exploration branches early, and Progressive Reward Tracking (PRT) that uses downgrade target models with a novel First Inverse Rate (FIR) metric to shape sparse rewards and guide strategy learning. Experiments across 18 LLMs in white-box and black-box settings demonstrate improvements in attack success rate, semantic diversity, and defense generalization diversity over several baselines.

## Strengths

- **Well-motivated decomposition of the red-teaming problem.** The paper convincingly argues that existing automated red-teaming methods operate at the query level within fixed strategy templates, missing the broader strategy space. The decomposition into strategy generation and strategy rephrasing (Equation 2) is a clean and principled formulation that enables strategy-level exploration, which is a meaningful conceptual advance.

- **Strong empirical validation across diverse settings.** The paper evaluates on 18 models spanning Llama 2/3, Mistral, Yi, Gemma 2, Qwen 1.5/2.5, and R2D2 in white-box settings, plus Llama 3 70B and Qwen 2.5 72B in black-box settings. AUTO-RT consistently achieves the highest ASR in most configurations in Table 1 (e.g., 56.40% on Vicuna 7B vs. 36.90% for IL, 48.15% on Gemma 2 2B vs. 7.49% for IL), and the ablation in Table 2 cleanly demonstrates that DSP and PRT contribute independently and complementarily.

- **FIR metric provides a practical and principled method for downgrade model selection.** Figure 4 demonstrates across six target models that selecting the last model before the sharp FIR increase consistently yields optimal attack performance. This addresses a genuine practical challenge—how to choose an appropriately calibrated intermediate model for reward shaping—and the empirical consistency of this heuristic is convincing.

- **Defense Generalization Diversity (DeD) results are particularly compelling.** AUTO-RT maintains substantially higher second-round attack success rates compared to all baselines (e.g., 46.80% vs. 20.10% for RL on Vicuna 7B), indicating that the discovered strategies are not brittle one-offs but rather represent genuine coverage of the vulnerability space. This directly supports the paper's central claim about strategy-level exploration.

- **Black-box extension via ICL is practical.** Table 4 shows meaningful improvements (e.g., 14.88% vs. 6.80% for IL on Llama 3 70B) even when model weights are inaccessible, broadening the method's applicability.

## Weaknesses

### Fatal
None.

### Major

- **Baseline comparison strength is mixed, and the gap with human-based methods is not fully addressed.** Table 3 shows that AutoDAN achieves ASR of 55.23% versus AUTO-RT's 38.38% averaged across 16 models. While AUTO-RT wins on DeD (38.19% vs. 17.88%), the paper does not adequately discuss why first-round effectiveness is lower than a genetic-algorithm-based method that uses handcrafted templates. This weakens the narrative that strategy-level RL exploration is superior to template-based approaches. A deeper analysis of this tradeoff would strengthen the paper.

- **The reward shaping in PRT is not potential-based, with limited theoretical justification for policy preservation.** The paper acknowledges this directly (Section 2.3.3), noting that the selection of the downgrade model is "critical" because the shaped reward does not follow the potential-based structure (Ng et al., 1999). While the FIR heuristic works empirically, there is no analysis of when or why it might fail—for instance, what happens if the safety distribution of the target model doesn't have a monotonic relationship with the downgrade models, or if multiple "inverse" points exist? The paper would benefit from a more careful analysis of the conditions under which PRT preserves or improves the optimal policy.

- **Single evaluator dependency.** All safety evaluations rely on Llama-Guard2-8B. If this classifier has systematic blind spots or biases, the entire RL optimization could converge to exploit classifier weaknesses rather than find genuinely harmful outputs. Given that the paper's contribution is about discovering "truly" effective strategies, validation with an additional independent safety evaluator would significantly strengthen the claims.

### Minor

- **The DeD defense construction methodology is underspecified.** The paper states defenses are "constructed based on the successful attacks" but does not describe what form these defenses take (e.g., system prompt modifications, input filters, fine-tuning). The specifics matter substantially for interpreting the DeD metric—different defense types could yield very different conclusions about strategy robustness.

- **Table 3 is incomplete.** AUTO-RT's SeD value is missing from the table, making a full three-way comparison impossible. Additionally, the set of target models used for this comparison is not specified, making it hard to interpret the gap with Table 1 results.

- **Downgrade model construction details are sparse.** The paper mentions "progressively weaken the target model with toxic data" but the practical process for creating a calibrated spectrum of M1–M6 models (e.g., varying amounts of toxic data, different fine-tuning schedules) is not well documented, which limits reproducibility.

### Trivial
None.

## Nice-to-Haves

- Analysis of what types of strategies AUTO-RT discovers qualitatively (e.g., examples of novel strategy patterns), beyond aggregate metrics, would make the contribution more tangible.
- A discussion of computational cost comparison between AUTO-RT and baselines would be informative, since the method requires constructing multiple downgrade models and training an RL agent over 9,000 episodes.
- Exploration of whether strategies transfer across model families (e.g., strategies discovered on Llama working on Qwen) would be valuable for understanding generalizability.

## Novel Insights

The First Inverse Rate (FIR) concept is a genuinely novel contribution. The idea that the optimal downgrade model for reward shaping lies at the boundary where a model's safety distribution begins to sharply degrade—the point where internal safety boundaries become unstable rather than simply weaker—offers a principled heuristic that could extend beyond red-teaming to other sparse-reward settings where intermediate difficulty curriculum is needed. The empirical consistency of this heuristic across six different target models (Figure 4) suggests it captures a real structural property of how safety alignment degrades under adversarial pressure.

## Suggestions

- Add a comparison with stronger automated baselines such as Rainbow-Teaming or AutoDAN-turbo to contextualize AUTO-RT's position relative to state-of-the-art automated red-teaming methods, not just basic FS/IL/RL baselines.
- Provide qualitative examples of strategies discovered by AUTO-RT that are genuinely novel, to demonstrate that the framework is not merely optimizing existing templates but finding new attack paradigms.
- Include a secondary safety evaluator to cross-validate results and assess vulnerability to classifier exploitation.

## Score and Decision

AUTO-RT makes a solid contribution to the important problem of automated LLM red-teaming. The decomposition into strategy generation and rephrasing is well-motivated, DSP and PRT are complementary and individually effective (as shown by ablation), the FIR metric is novel and practical, and experiments are broad across 18 models. However, the baselines are somewhat basic, the gap with template-based methods like AutoDAN on first-round ASR is not well explained, and the theoretical underpinning of the non-potential-based reward shaping deserves deeper treatment. The DeD results are the paper's strongest empirical argument and demonstrate genuine value in strategy-level exploration.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>