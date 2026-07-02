### Summary

This paper proposes a novel backdoor attack, TrojanTO, against Trajectory Optimization (TO) models in offline reinforcement learning. TrojanTO is a post-training attack that forges a strong connection between triggers and target actions through alternating training. It ensures stealthiness by preserving benign performance with trajectory filtering and maintaining trigger consistency via batch poisoning. Extensive evaluations show TrojanTO's effectiveness across various tasks and TO model architectures with a low attack budget.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. This paper is a pioneer work to investigate backdoor attacks on Trajectory Optimization (TO) models.
2. TrojanTO is a post-training attack, which is more practical than previous training-time attacks.
3. TrojanTO shows effectiveness on diverse tasks and TO model architectures.

### Weaknesses

#### Some Related Works

[1] Input-level backdoor attacks against deep reinforcement learning agents.
[2] Baffle: A backdoor attack against offline reinforcement learning.
[3] Trojdr: A data poisoning backdoor attack against deep reinforcement learning agents.
[4] Trojan-bandit: A backdoor attack against deep reinforcement learning with limited information.
[5] Rethinking the backdoor attacks in deep reinforcement learning.
[6] Rlbench: A benchmark for reinforcement learning agents.

#### comment

1. The literature review and comparison with existing backdoor attacks in DRL are not comprehensive. There are many existing backdoor attacks targeting DRL models that are not discussed in this paper, such as [1,2,3,4,5]. Specifically, the authors should clarify why these existing methods cannot be directly applied to TO models, given that they are also sequence-based models. The current explanation lacks a detailed analysis of the architectural and training differences that make these attacks ineffective.
2. The paper lacks comparisons with existing backdoor attack methods. Although the authors argue that existing methods cannot be directly applied to TO models, they should at least show the performance of these methods on TO models and compare them with TrojanTO. This would provide a more concrete understanding of the relative effectiveness of the proposed attack and the limitations of existing approaches in the context of TO models. The absence of such comparisons makes it difficult to assess the true novelty and impact of TrojanTO.
3. The paper lacks experiments on more complex and diverse benchmarks, such as RLbench [6]. The current evaluation is limited to relatively simple environments, which may not fully capture the challenges of applying backdoor attacks in more realistic scenarios. Testing on more complex benchmarks would provide a more robust evaluation of the proposed method.
4. The paper does not analyze the transferability of the backdoor attack. It is unclear whether the backdoor injected into a TO model can be transferred to other models or environments. This is an important aspect of backdoor attacks that should be investigated to fully understand the potential risks.
5. The paper lacks defense methods to mitigate backdoor attacks on TO models. The authors should at least analyze some existing defense methods to discuss the challenges of defending against backdoor attacks on TO models. This would provide a more complete picture of the security landscape and highlight the need for further research in this area.

### Suggestions

The paper needs a more thorough discussion of why existing backdoor attacks on sequential models cannot be directly applied to Trajectory Optimization (TO) models. While the authors mention that TO models are sequence-based, they do not provide a detailed analysis of the architectural and training differences that make these attacks ineffective. For example, many existing backdoor attacks rely on manipulating the reward function or the state transitions, which may not be directly applicable to TO models that optimize trajectories directly. The authors should provide a concrete explanation of these differences, possibly by analyzing the internal mechanisms of TO models and how they differ from traditional reinforcement learning models. This analysis should include a discussion of how the direct trajectory optimization process in TO models affects the attack surface and the types of vulnerabilities that are unique to these models. Furthermore, the authors should clarify why the specific trigger design used in existing attacks, such as those based on specific state patterns, are not effective in the context of TO models, given that TO models also process sequences of states and actions.

To strengthen the evaluation, the authors should include a comparative analysis of TrojanTO with existing backdoor attack methods, even if those methods are not directly designed for TO models. This would involve adapting existing methods to the TO setting and evaluating their performance. For instance, the authors could try to apply reward manipulation techniques or data poisoning strategies from existing backdoor attacks to TO models and compare the resulting attack success rate (ASR) and benign task performance (BTP) with TrojanTO. This would provide a more concrete understanding of the relative effectiveness of the proposed attack and the limitations of existing approaches in the context of TO models. The comparison should also include a discussion of the stealthiness of different attacks, as measured by the impact on benign performance. This would help to highlight the advantages of TrojanTO over existing methods and provide a more comprehensive evaluation of the proposed attack. The authors should also consider comparing against methods that use different types of triggers, such as those based on specific action sequences or reward patterns.

Finally, the paper should include a more detailed analysis of the transferability of the backdoor attack. The authors should investigate whether the backdoor injected into a TO model can be transferred to other models or environments. This would involve testing the triggered performance of a model trained with TrojanTO in different environments or with different model architectures. The authors should also analyze the robustness of the backdoor to variations in the trigger, such as changes in its magnitude or dimension. This analysis should include a discussion of the potential risks associated with transferable backdoors and the implications for the security of TO models. Furthermore, the authors should explore the possibility of using existing defense methods to mitigate backdoor attacks on TO models. This would involve testing the effectiveness of methods such as input sanitization, adversarial training, or model pruning against TrojanTO. The authors should also discuss the challenges of defending against backdoor attacks on TO models and highlight the need for further research in this area.

### Questions

Please see the weaknesses.

### Rating

5

### Confidence

4

**********