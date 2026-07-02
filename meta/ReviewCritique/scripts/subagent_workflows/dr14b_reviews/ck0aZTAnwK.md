### Summary

This paper studies the problem of pre-training language models under fixed data and no compute constraints. The authors first show that existing data-constrained approaches of increasing epoch count and parameter count overfit, and they improve upon such recipes by tuning regularization, finding that the optimal weight decay is 30× larger than standard practice. Since their regularized recipe monotonically decreases loss following a power law in parameter count, they estimate its best possible performance via the asymptote of its scaling law rather than the performance at a fixed compute budget. They then identify that ensembling independently trained models achieves a significantly lower loss asymptote than the regularized recipe. Their best intervention combining epoching, regularization, parameter scaling, and ensemble scaling achieves an asymptote at 200M tokens using 5.17× less data than their baseline, and their data scaling laws predict that this improvement persists at higher token budgets. They find that their data efficiency gains can be realized at smaller parameter counts as they can distill an ensemble into a student model that is 8× smaller and retains 83% of the ensembling benefit. Finally, their interventions designed for validation loss generalize to downstream benchmarks, achieving a 9% improvement for pre-training evals.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

* The paper is well-written and easy to follow. 
* The paper studies an important problem: pre-training language models under fixed data and no compute constraints. 
* The paper provides a good set of experiments to show the effectiveness of the proposed methods.

### Weaknesses

#### Some Related Works


#### comment

 * The paper only evaluates on DCLM. It would be better if the paper could evaluate on more datasets.

* The paper only evaluates on a small set of models (300M, 600M, 1.4B). It would be better if the paper could evaluate on a larger set of models.

### Suggestions

The paper's focus on data efficiency in language model pre-training is valuable, but the limited scope of the experimental evaluation raises concerns about the generalizability of the findings. Specifically, the exclusive use of the DCLM dataset makes it difficult to ascertain whether the observed improvements in data efficiency are specific to this dataset's characteristics or if they hold across diverse text corpora. To strengthen the paper, the authors should consider including experiments on other datasets, such as C4 or a subset of the Pile, which are commonly used in language model research. This would provide a more robust assessment of the proposed methods and their applicability to different types of text data. Furthermore, it would be beneficial to analyze the performance of the proposed techniques on datasets with varying levels of noise and domain specificity to understand their limitations and potential for broader application.

In addition to the dataset limitation, the paper's evaluation on a narrow range of model sizes (300M, 600M, 1.4B parameters) also restricts the conclusions that can be drawn about the scalability of the proposed methods. While the chosen model sizes are representative of a certain range, it is important to investigate whether the observed data efficiency gains hold for both smaller and larger models. For instance, it would be valuable to evaluate the proposed techniques on models with fewer than 300 million parameters, as well as models with significantly more parameters, such as 1.7B or 3B, to determine if the benefits of regularization, ensembling, and distillation persist across a wider range of model capacities. This would provide a more comprehensive understanding of the practical implications of the proposed methods and their potential for use in different scenarios. The authors should also consider analyzing the computational cost of their methods, especially the ensembling and distillation techniques, as these might become prohibitive for very large models.

Finally, the paper would benefit from a more detailed analysis of the hyperparameter tuning process. While the authors mention that they tuned regularization parameters, it is not clear how this tuning was performed and what range of values were explored. Providing more details about the hyperparameter search, including the specific optimization algorithm used and the criteria for selecting the best parameters, would enhance the reproducibility of the results and allow other researchers to build upon this work. Furthermore, it would be useful to investigate the sensitivity of the proposed methods to different hyperparameter settings, as this could provide insights into the robustness of the approach. A more thorough analysis of the hyperparameter space would also help to identify potential limitations and areas for future improvement.

### Questions

* Can the proposed methods be applied to other datasets? 
* Can the proposed methods be applied to other models?

### Rating

6

### Confidence

2

**********