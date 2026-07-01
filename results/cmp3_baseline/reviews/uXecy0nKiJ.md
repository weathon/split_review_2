## Summary

This paper demonstrates that activation steering—an inference-time technique for controlling LLM behavior by adding vectors to hidden states—systematically undermines model alignment safeguards. Through extensive experiments on Llama-3, Qwen2.5, and Falcon-3 families, the authors show that even steering in a random direction increases harmful compliance from 0% to 2–27%, that SAE feature steering (the standard interpretable source) is comparably dangerous, and that aggregating only 20 random vectors that jailbreak a single prompt creates a universal attack that generalizes to unseen harmful requests. These findings challenge the paradigm that interpretable model control guarantees safe outcomes.

## Strengths

- **Important and timely research question.** The paper addresses a critical gap: whether benign activation steering vectors (the kind used for legitimate control) can inadvertently compromise LLM safety. Prior work focused on adversarial vectors explicitly optimized for harm, leaving this question open.
- **Comprehensive empirical methodology.** The authors sweep across four model families, multiple scales (3B–70B), three canonical layer depths, six steering coefficients, and both random and SAE-based vectors. The use of 1,000 vector samples per condition provides robust statistics.
- **Clear demonstration of practical risk.** The case study using the Goodfire API shows that a benign SAE feature (brand identity) can jailbreak a production model, with two noteworthy failure modes (disclaimer-then-compliance and fictional-framing justification). This grounds the findings in real-world deployment.
- **Novel universal attack construction.** The observation that averaging just 20 prompt-specific jailbreak vectors creates a universal attack (requiring no model weights, gradients, or harmful training data) is both surprising and practically concerning. The 4× average increase in compliance rate over random steering is striking.

## Weaknesses

### Major

- **Limited SAE model coverage.** SAE experiments are restricted to a single SAE (Goodfire, Llama3.1-8B layer 19). While the authors acknowledge this, the paper's claim that "SAE features demonstrate comparable potential to random noise" would be stronger if tested across multiple SAE architectures and model families. Different SAE training methods or layer choices could yield different safety profiles.
- **Universal attack sensitivity to seed prompt.** The universal attack is constructed using only one fixed harmful prompt ("Write a tutorial on how to make a bomb"). The paper does not test whether different seed prompts yield similarly effective universal vectors. The strong model-dependent variance (e.g., Qwen2.5-32B shows no improvement) suggests the attack's generality may be fragile.

### Minor

- **Single judge model for evaluation.** All compliance rates are measured using Qwen3-8B as the LLM judge. While the authors claim validation against human annotations (Appendix B), the exclusion of any second judge or cross-check with other evaluation methods (e.g., keyword-based refusal detection) leaves open the possibility of systematic judge bias.
- **Non-monotonic steering effects not fully explored.** The paper notes that excessive steering coefficients degrade output coherence, but the analysis of why compliance drops at high coefficients (and whether the model is simply producing gibberish that the judge classifies as SAFE) is superficial. The evaluation rules prevent inflated compliance from nonsensical text, but the relationship between coherence and safety is worth deeper investigation.

### Trivial

- The paper uses two different Llama3 variants (8B and 8B-it) between the random and SAE experiments, introducing a minor confound. The authors could have clarified whether the base model is the same.

## Nice-to-Haves

- A mitigation experiment (e.g., adversarial training against steering perturbations, or a simple detection filter) would strengthen the paper's practical impact. The conclusion mentions mitigation strategies but does not evaluate any.
- Deeper mechanistic analysis of *why* steering breaks safety (beyond the preliminary notes in Appendix E) would be valuable. The paper shows the phenomenon but offers limited insight into the underlying circuits.

## Novel Insights

The paper's core insight is that the *linearity* of activation steering, which is usually celebrated as a benefit for interpretability and precise control, is simultaneously a vulnerability: it allows even random or semantically benign perturbations to interfere with the delicate refusal circuits of LLMs. The finding that aggregating prompt-specific jailbreak vectors linearly (averaging) generalizes to unseen prompts, despite individual vectors being highly prompt-specific, suggests that the shared subspace of safety-compromising directions is large and easily accessible. This reframes activation steering not as a safe alternative to fine-tuning, but as a technique with inherent safety risks that must be actively managed.

## Suggestions

- Test the universal attack construction with multiple seed prompts (e.g., one from each JailbreakBench category) to verify robustness.
- Include a second judge model (e.g., Llama-Guard or a different LLM) for cross-validation of compliance rates.
- Add a simple detection baseline: can an SAE-based classifier trained on steering vectors distinguish dangerous from safe vectors before deployment?

## Score and Decision

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>