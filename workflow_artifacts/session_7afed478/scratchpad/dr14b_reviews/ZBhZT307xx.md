### Summary

This paper studies the verifiers used in reinforcement learning for mathematical reasoning, which is an important component for policy learning. The authors conduct a comprehensive analysis of both rule-based and model-based verifiers. The findings reveal that while rule-based verifiers are highly precise, they often fail to recognize correct answers that deviate from expected formats, leading to lower recall rates. Although model-based verifiers exhibit better accuracy in static evaluations, they are vulnerable to reward hacking during RL training, where the policy model exploits patterns in the verifiers to obtain artificially high rewards.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The studied topic is important and interesting. Verifiers are essential components of reinforcement learning for mathematical reasoning, and the findings in this work provide valuable insights for future research.
2. The authors conduct comprehensive experiments to analyze the advantages and limitations of rule-based and model-based verifiers in both static evaluation and RL training scenarios.

### Weaknesses

#### Some Related Works

[1] Measuring and narrowing the compositionality gap in language models.
[2] Toolformer: Language models can teach themselves to use tools.
[3] Chain-of-thought prompting elicits reasoning in large language models.
[4] ReST-Math: A Resource and Study for Real-World Mathematical Work.

#### comment

1. The findings in this paper largely align with common knowledge. It is widely understood that rule-based verifiers struggle with generalizability and that model-based verifiers are vulnerable to reward hacking. More importantly, previous studies have already demonstrated that model-based verifiers can overcome some limitations of rule-based verifiers, such as handling more complex reasoning tasks [1,2]. This paper, however, does not provide substantial new insights to advance the field.
2. The authors only experiment with mathematical reasoning tasks, which are typically composed of a series of sub-operations that can be verified step by step using rule-based verifiers. In more complex reasoning tasks, rule-based verifiers are too brittle to be effective, and model-based verifiers have already been shown to be more effective [1,2]. By focusing on a domain where rule-based verifiers are relatively effective, the authors miss an opportunity to provide more insightful analyses and conclusions.
3. The authors do not propose any methods to address the challenges associated with model-based verifiers. While the findings are interesting, they do not offer solutions to the problems raised, thus limiting the paper's overall contribution.

An additional minor weakness is the clarity of the presentation. The authors do not provide a clear definition of the rule-based verifiers used in this paper, and it is unclear how the model-based verifiers are trained. Furthermore, the paper lacks a clear explanation of the RL training process, and the static evaluation methodology is not well-defined. The paper also does not adequately discuss the limitations of the study, such as the specific types of mathematical problems used and the potential impact of these choices on the results. The lack of detail in these areas makes it difficult to fully assess the validity and generalizability of the findings.

### Suggestions

The paper would benefit significantly from a more detailed exploration of the limitations of rule-based verifiers in more complex reasoning tasks, where their brittleness is more apparent. Instead of focusing solely on mathematical reasoning, which is somewhat amenable to rule-based verification, the authors should consider expanding their analysis to include tasks that require more nuanced understanding and reasoning. For example, tasks involving multi-step inference or common-sense reasoning would better highlight the advantages of model-based verifiers and the challenges they pose. This would also provide a more compelling context for the observed reward hacking phenomenon, making the findings more impactful and relevant to the broader research community. Furthermore, the authors should investigate the specific types of errors made by rule-based verifiers, providing a more granular analysis of their failure modes. This would help in understanding the specific limitations of rule-based approaches and how they can be mitigated.

To address the lack of solutions, the authors should consider proposing a framework for developing more robust verifiers. This could involve exploring techniques such as adversarial training, where the verifier is trained to resist manipulation by the policy model, or incorporating uncertainty estimation into the verification process, which could help to identify cases where the verifier is likely to be incorrect. Another promising direction would be to investigate hybrid approaches that combine the strengths of both rule-based and model-based verifiers. For example, a system could use rule-based verifiers for initial filtering and then use model-based verifiers for more complex cases, or vice versa. This would allow the system to leverage the precision of rule-based verifiers while also benefiting from the flexibility of model-based verifiers. The authors should also provide a more detailed explanation of the training process for the model-based verifiers, including the specific datasets used, the training objectives, and the hyperparameter settings. This would allow other researchers to reproduce their results and build upon their work.

Finally, the authors should provide a more thorough discussion of the limitations of their study. This should include a detailed analysis of the types of mathematical problems used, the potential impact of these choices on the results, and the generalizability of their findings to other domains. For example, the authors should discuss whether the mathematical problems used are representative of the broader range of mathematical reasoning tasks, and whether the observed reward hacking phenomenon is likely to occur in other domains. The authors should also discuss the potential impact of the choice of model architecture on the results, and whether their findings are likely to generalize to other types of models. By addressing these limitations, the authors can provide a more complete and nuanced understanding of the challenges associated with using verifiers in reinforcement learning for reasoning tasks.

### Questions

1. The authors mention that "In our subsequent RL training experiments, however, we observe that model-based verifiers introduce unique challenges and yield mixed outcomes" (Line 90). Could they elaborate on the specific challenges encountered and the reasons for these mixed outcomes?
2. The authors state that "the classification accuracy of a verifier does not necessarily reflect its resistance to reward hacking, and therefore may not be a reliable indicator of its effectiveness in RL training" (Line 96-97). Could they clarify why a model-based verifier's accuracy may not correlate with its susceptibility to reward hacking?
3. The authors mention that "the community is advancing increasingly powerful reasoning models, which in turn require stronger verifiers" (Line 173). Could they clarify why more powerful reasoning models would necessitate stronger verifiers?
4. The authors state that "the hybrid verifier consistently outperforms the rule-based verifier, and this performance gap does not diminish with additional computation" (Line 421). Could they specify the types of computation used in this context?
5. In Section 5, the authors mention "reward hacking persists across both domains" (Line 464). Could they clarify what these two domains are?

### Rating

5

### Confidence

4

**********