### Summary

The paper studies the problem of detecting and controlling deception in LLMs. The authors propose a testbed called "Secret Agenda" to induce deception in LLMs and analyze the effectiveness of current interpretability tools in detecting and controlling such behaviors. They find that while Sparse Autoencoder (SAE) features labeled as "deception-related" fail to activate or prevent lying, aggregate unlabeled activations can differentiate between deceptive and compliant responses in scenarios like insider trading. The study highlights the limitations of current interpretability approaches and suggests that population-level patterns may be more useful for risk assessment than labeled features.

### Soundness

1

### Presentation

1

### Contribution

1

### Strengths

The paper addresses a timely and important topic: the safety and interpretability of large language models.

### Weaknesses

#### Some Related Works


#### comment

The paper is largely incomprehensible to me. It reads more like a blog post than a scientific paper. It lacks a clear structure and often jumps between ideas without proper transitions. For example, Section 6.1 suddenly starts discussing deception features without adequately introducing the topic or explaining its relevance to the previous sections. The methodology is poorly described, making it difficult to understand how the experiments were conducted. For instance, the "Secret Agenda" testbed is mentioned, but its design and implementation are not explained in sufficient detail. The use of SAEs is also not clearly articulated, leaving the reader unsure about how these were applied to analyze deceptive behaviors. The Insider Trading scenario is introduced without any context or explanation of how it relates to the overall study. Furthermore, the paper lacks a clear explanation of the experimental setup, including the specific prompts used, the number of trials, and the statistical methods used to analyze the results. The figures are not well-integrated into the text, and their purpose is often unclear. For example, Figure 1 is mentioned but not described in the text, making it difficult to understand its relevance. The paper also lacks a clear definition of what constitutes "deception" in the context of LLMs, which makes it difficult to evaluate the claims made by the authors. The lack of rigorous scientific methodology and the absence of detailed experimental descriptions make it hard to reproduce the results.

### Suggestions

The paper needs a significant restructuring to improve its clarity and scientific rigor. The authors should begin by providing a clear and concise definition of deception in the context of LLMs. This definition should be grounded in existing literature and should serve as a basis for the experimental design. The introduction should clearly state the research question and the motivation behind the study. The methodology section needs a complete overhaul. The authors should provide a detailed description of the "Secret Agenda" testbed, including its design, implementation, and the specific scenarios used. They should also explain how the SAEs were trained and used to analyze the model's internal representations. The Insider Trading scenario should be introduced with a clear explanation of its purpose and how it relates to the overall study. The experimental setup should be described in detail, including the specific prompts used, the number of trials, and the statistical methods used to analyze the results. The figures should be well-integrated into the text, and their purpose should be clearly explained. For example, Figure 1 should be described in detail, and its relevance to the study should be made clear. The authors should also provide a more detailed analysis of the results, including a discussion of the limitations of their approach. The paper should also include a thorough literature review, citing relevant works in the field of LLM interpretability and safety. The authors should also discuss the ethical implications of their findings and suggest future research directions. The paper should be written in a more formal and scientific style, avoiding the use of vague language and blog-like expressions. The authors should also ensure that the paper is well-organized and that the different sections flow logically from one another. The paper should be peer-reviewed by other researchers in the field before submission.

### Questions

N/A

### Rating

1

### Confidence

5

**********