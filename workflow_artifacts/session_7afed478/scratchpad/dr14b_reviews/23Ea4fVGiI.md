### Summary

This paper introduces the Task-Method-Knowledge (TMK) framework, which provides a structured approach to prompting language models for reasoning and planning tasks. The TMK framework decomposes problems into tasks, methods, and knowledge components, aiming to improve model performance by explicitly representing causal, teleological, and hierarchical reasoning structures. The paper evaluates the TMK framework on the PlanBench benchmark, specifically the Blocksworld domain, and shows that TMK-structured prompting significantly improves model accuracy, particularly in opaque, symbolic tasks. The authors argue that TMK acts as a symbolic steering mechanism, shifting models from linguistic approximation to formal, code-execution pathways.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

1. The TMK framework offers a novel approach to prompting that goes beyond existing methods like CoT by explicitly representing the "why" behind actions, which may improve model interpretability and reasoning depth.
2. The paper evaluates TMK on different Blocksworld variants (Classic, Mystery, Random) to test model reliance on semantic cues, providing insights into how TMK reduces semantic interference in symbolic tasks.
3. Results demonstrate substantial performance improvements, with accuracy gains of up to 65.8% in certain configurations, suggesting TMK's potential to enhance model performance in planning tasks.

### Weaknesses

#### Some Related Works


#### comment

1. The paper's experimental scope is limited to the Blocksworld domain, which restricts the generalizability of the findings. While Blocksworld is a well-established benchmark, it is a relatively constrained domain, and the hierarchical structures and action spaces are less complex than those encountered in real-world planning scenarios. The paper would benefit from demonstrating the effectiveness of the TMK framework on more diverse and complex domains, such as those involving spatial reasoning or multi-agent interactions, to better assess its broader applicability.
2. The TMK framework may introduce complexity in prompt design, especially for hierarchical tasks, which could limit its practicality for quick or simple prompts. The process of decomposing tasks into Method, Task, and Knowledge components, while conceptually sound, may become cumbersome and time-consuming for intricate planning problems. The paper does not provide a clear methodology or tools to streamline this process, which could hinder its adoption by practitioners.
3. The paper does not thoroughly analyze why TMK improves model performance. While the authors suggest that TMK acts as a symbolic steering mechanism, there is a lack of detailed analysis of the internal model representations or attention patterns to support this claim. The paper would benefit from a more in-depth investigation into how the TMK framework alters the model's reasoning process, such as through probing studies or visualization techniques.

### Suggestions

To strengthen the paper, the authors should expand their experimental evaluation to include more diverse and complex planning domains beyond Blocksworld. Specifically, they could consider domains that involve spatial reasoning, such as the logistics domain in PlanBench, or multi-agent scenarios to assess the generalizability of the TMK framework. This would involve not only demonstrating that the framework can achieve high accuracy in these domains but also analyzing the types of errors that occur and how they differ from those observed in Blocksworld. Furthermore, the authors should investigate the scalability of the TMK framework with respect to the complexity of the planning task, including the length of the planning horizon and the number of objects involved. This would provide a more comprehensive understanding of the framework's limitations and potential for real-world applications. The inclusion of such experiments would significantly enhance the paper's impact and credibility.

To address the practical challenges of prompt design, the authors should develop a more systematic approach for creating TMK prompts, especially for hierarchical tasks. This could involve providing a set of guidelines or a template that practitioners can use to decompose complex problems into Method, Task, and Knowledge components. Furthermore, the authors could explore the possibility of automating the TMK prompt generation process using a secondary model or a rule-based system. This would significantly reduce the burden on users and make the TMK framework more accessible. The paper should also include an analysis of the time and effort required to create TMK prompts for different types of planning tasks, comparing it to other prompting techniques. This would provide a more realistic assessment of the practicality of the TMK framework.

Finally, the authors should conduct a more thorough analysis of the underlying mechanisms through which the TMK framework improves model performance. This could involve techniques such as probing the model's internal representations to understand how the TMK structure affects its reasoning process. For example, the authors could analyze the attention patterns of the model when using TMK prompts versus standard prompts to see if there is a shift in focus towards more symbolic or code-related tokens. Additionally, the authors could perform ablation studies to determine the relative importance of the different components of the TMK framework (Task, Method, Knowledge) and how they interact to improve performance. Such analysis would provide a more solid foundation for the claims made in the paper and offer valuable insights into the nature of reasoning in language models.

### Questions

1. How well does the TMK framework generalize to other planning domains beyond Blocksworld? Would the same performance improvements hold in more complex or varied environments?
2. Could the authors provide more details on the process of designing TMK prompts? Is the framework easily adaptable for different types of planning tasks, or does it require extensive customization?
3. The paper suggests that TMK steering enables language models to engage code-execution pathways. Could the authors elaborate on this mechanism? How does TMK specifically shift the model from linguistic to symbolic reasoning?
4. Why did the o1-mini model perform worse in the Mystery domain with TMK prompting? Could this be due to limitations in model capacity or conflicts between semantic and symbolic cues?

### Rating

3

### Confidence

4

**********