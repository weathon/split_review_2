### Summary

This paper presents a detailed re-analysis of the paper “Turning Up the Heat: MIN-P Sampling for Creative and Coherent LLM Outputs” (Nguyen et al., 2024), which introduced a new method for sampling from language models called `min-p`. The authors find that the original paper’s conclusions are not supported by its own data. They show that the original human evaluations omitted one-third of the collected data, applied statistical tests incorrectly, and inaccurately described qualitative feedback. They also find that extensive hyperparameter sweeps on NLP benchmarks show `min-p`’s claimed superiority vanishes when controlling for the volume of hyperparameter tuning. Furthermore, the LLM-as-a-Judge evaluations suffered from methodological ambiguity and appear to have reported results inconsistently, favoring `min-p`. Finally, claims of widespread community adoption were found to be unsubstantiated and were retracted. From this case study, the authors derive a blueprint for more rigorous research.

### Soundness

4

### Presentation

4

### Contribution

4

### Strengths

1. The paper is well-written and easy to follow.
2. The paper provides a detailed and comprehensive re-analysis of the original paper, including a thorough examination of the data, methodology, and results.
3. The paper identifies several significant flaws in the original paper, including omitted data, incorrect statistical tests, methodological ambiguities, and unsubstantiated claims.
4. The paper provides a valuable blueprint for more rigorous research, highlighting the importance of fair comparisons, correct statistical practices, data transparency, and careful qualitative analysis.

### Weaknesses

#### Some Related Works


#### comment

1. The paper focuses on a single case study, which may limit the generalizability of its findings and conclusions. However, I think the lessons derived from this detailed analysis are still valuable for improving research practices in empirical machine learning.
2. While the paper excels in critical analysis, it would be more impactful if it also proposed new solutions or best practice guidelines for addressing the identified issues in empirical machine learning research.

### Suggestions

The paper provides a valuable critique of the original work, but it could be strengthened by offering more concrete guidance for the community. For example, the authors could propose a checklist of methodological requirements that should be met when introducing new sampling methods, or any empirical method in machine learning. This checklist could include items such as: ensuring that all relevant data is included in the analysis, using appropriate statistical tests and correcting for multiple comparisons, providing clear and unambiguous descriptions of all methods and evaluation procedures, and avoiding selective reporting of results. Such a checklist would provide a practical tool for researchers to use when designing and evaluating their own studies, and would help to prevent the kinds of methodological flaws that the authors have identified in the min-p paper. Furthermore, the checklist could be expanded to include specific recommendations for qualitative analysis, such as the use of inter-rater reliability measures and the inclusion of representative quotes to support claims. This would help to ensure that qualitative feedback is analyzed rigorously and systematically, rather than being mischaracterized or selectively reported.

Furthermore, the paper could delve deeper into the specific statistical issues it identifies. While the authors mention the incorrect application of statistical tests, they could provide more detail on what constitutes correct practice in this context. For example, they could discuss the importance of checking the assumptions of statistical tests, and the consequences of violating these assumptions. They could also elaborate on the proper use of multiple comparison corrections, and why these are necessary when conducting multiple statistical tests. Providing concrete examples of how these statistical principles should be applied in the context of evaluating sampling methods would greatly enhance the paper's practical value. This would help researchers understand not just what the problems are, but also how to avoid them in their own work. For instance, the authors could provide a step-by-step guide on how to perform a Bonferroni correction or other appropriate methods for controlling the family-wise error rate, and explain why these methods are necessary when comparing multiple sampling techniques.

Finally, the paper could explore the issue of qualitative analysis in more detail. The authors mention that the original paper mischaracterized qualitative feedback, but they could provide more guidance on how to conduct proper qualitative analysis. This could include discussing the importance of using systematic coding schemes, ensuring inter-rater reliability, and avoiding selective reporting of qualitative data. The authors could also discuss the limitations of relying solely on qualitative data, and the importance of triangulating qualitative findings with quantitative results. By providing more detailed guidance on these aspects, the paper could serve as a valuable resource for researchers who are looking to improve the rigor of their empirical studies. For example, the authors could suggest using software tools for qualitative data analysis, and provide examples of how to use these tools to ensure a systematic and rigorous approach.

### Questions

1. What are the scientific conclusions of your study? Do you find that min-p is entirely without merit, or are there specific conditions under which it might be beneficial?
2. Could you elaborate on how you controlled for hyperparameter volume when comparing min-p to other sampling methods? What specific metrics or methods did you used to ensure a fair comparison?
3. How did you verify the claims regarding community adoption of min-p? What methods or sources did you used to assess the actual level of adoption in the open-source community?
4. Could you clarify the distinction between your re-analysis of existing evidence and the introduction of new evidence? How do you ensure that the conclusions drawn from the re-analysis are not influenced by the new data?
5. What do you consider to be the most critical lesson for researchers based on your findings? How can the community better guard against flawed or misleading claims in empirical machine learning research?

### Rating

8

### Confidence

4

**********