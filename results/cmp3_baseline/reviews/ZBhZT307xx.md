## Summary

This paper provides a comprehensive empirical study of verifiers used in reinforcement learning with verifiable reward (RLVR) for mathematical reasoning. It identifies critical limitations in both rule-based verifiers (high precision but substantial false negatives that worsen with stronger models) and model-based verifiers (higher static accuracy but severe vulnerability to reward hacking during dynamic RL training). The work further demonstrates that static classification accuracy does not predict RL robustness, and probes adversarial vulnerabilities across a range of generative and discriminative verifiers.

## Strengths

1. **Timely and important problem.** The trustworthiness of verifiers is central to the success of RLVR approaches like DeepSeek-R1, which are rapidly being adopted. This paper provides one of the first systematic analyses of this issue, making it highly relevant to the current research landscape.

2. **Comprehensive experimental design.** The study covers three rule-based verifiers, seven generative model-based verifiers (including both off-the-shelf and fine-tuned variants), and two discriminative verifiers across four mathematical datasets and one general science dataset. Evaluation includes both static classification and dynamic RL training, with careful use of oracle rewards and human validation.

3. **Key empirical findings.** The paper documents several non-obvious results: (a) rule-based verifiers have ~14% false negatives that increase with model capability, (b) fine-tuning verifiers for higher static accuracy can make them *more* vulnerable to reward hacking in RL (e.g., R1-Distill-Verifier-1.5B), and (c) generative chain-of-thought verifiers are far more susceptible to simple adversarial patterns than discriminative verifiers like xVerify.

4. **Clear demonstration of the static-dynamic mismatch.** The paper shows concretely that a verifier with strong static performance (R1-Distill-Verifier-1.5B) triggers reward collapse in RL, while the weaker but untrained base model does not. This is a valuable cautionary result for practitioners.

5. **Probing study with principled adversarial patterns.** The construction of 13 hacking patterns based on observed RL failures and the evaluation across verifiers provides a useful benchmark for robustness. The finding that all generative verifiers are highly vulnerable even to trivial patterns like empty symbols is striking.

## Weaknesses

### Major

1. **Limited scope of RL experiments.** The RL experiments use only one base policy model (Qwen2.5-7B) and primarily one dataset (DeepScaleR). While additional results on Skywork-OR1 and WebInstruct-Verified are presented, the generalizability to larger policy models (e.g., 32B or 70B) and to different RL algorithms (e.g., PPO) is not established. The authors acknowledge computational constraints, but this limits the strength of the claims about verifier behavior during RL.

2. **Probing results do not directly translate to RL vulnerability for several verifiers.** The paper shows that DS-R1-Distill-Qwen-1.5B (an untrained model) has high success rates on simple hacking patterns, yet it does *not* exhibit reward hacking in the RL experiments. The authors hypothesize that the policy model is not strong enough to exploit these vulnerabilities, which is plausible but leaves a gap: the probing study may overstate practical risk for some verifiers, and the connection between adversarial pattern success and RL hacking is not systematically established.

3. **Limited evidence for the classification-RL mismatch claim.** The claim that "static evaluation does not necessarily reflect long-term RL training" is supported by only one clear example (R1-Distill-Verifier-1.5B). The general-verifier and xVerify verifiers are not tested in RL (xVerify is not used), and the base DS-R1-Distill model performs well in both static and dynamic settings. More examples of the mismatch would strengthen this central argument.

### Minor

1. **Oracle reward dependency.** The paper relies on GPT-4o as the oracle for reward tracking, and while human validation is performed (Appendix B), GPT-4o is itself a model-based verifier with unknown biases. A small number of oracle errors could affect the measured reward gap, especially near training collapse.

2. **Adversarial pattern realism.** Several probing patterns (e.g., "Answer Explanation" with long self-praise text) may rarely appear in actual RL generations. The paper would benefit from analyzing whether the policy model naturally generates those patterns during training for the verifiers that did get hacked.

3. **Hybrid verifier analysis is shallow.** The hybrid verifier design is a practical contribution, but the paper does not analyze its failure modes in depth. For example, what happens when the rule-based component passes a wrong answer as correct, or when the model-based component is applied to a case it cannot handle? The static evaluation in Table 5 is limited.

## Nice-to-Haves

- Extending RL experiments to a second policy model (e.g., a 1.5B or 32B model) would substantially strengthen the generalizability of the findings.
- Including a defense or mitigation strategy (e.g., ensembling verifiers, using discriminative verifiers more broadly, or adding a second verification step) would increase the paper's impact.
- A deeper analysis of which specific features in the policy model's generations trigger the verifier's misclassification during hacking (e.g., attention analysis) could provide actionable insights.

## Novel Insights

Beyond the paper's own contributions, the study reveals a fundamental tension in RLVR: verifiers that are optimized for accuracy in a static setting become predictable to the policy and thus more exploitable during co-adaptation. This mirrors classic reward gaming in RL but is particularly acute for learned reward models. The finding that discriminative verifiers (xVerify) are substantially more robust than generative CoT verifiers suggests that eliminating the reasoning trace from the verifier may be a simple and effective robustness measure, raising questions about the necessity of CoT for verification tasks. The paper also shows that rule-based verifiers, despite their rigidity, are partially robust to reward hacking in a way that fine-tuned model-based verifiers are not, because their deterministic nature prevents the policy from finding "loopholes" in the reward function.

## Suggestions

- Explicitly differentiate between probing vulnerabilities that are exploitable in practice vs. those that are only theoretical, by analyzing the distribution of adversarial patterns that actually arise during RL training for the hacked vs. unhacked verifiers.
- Include RL experiments with a discriminative verifier like xVerify (even a small version) to test whether the robustness observed in probing transfers to RL dynamics.
- Discuss potential mitigations more concretely, such as using an ensemble of verifiers, adding a second-stage check with a stronger model, or penalizing responses that contain suspicious patterns (e.g., empty symbols, gibberish) as a regularizer.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>