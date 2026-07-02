### Summary

The paper introduces BadDet+, an advanced framework for backdoor attacks on object detection models, addressing limitations in prior approaches. It unifies region misclassification (RMA) and object disappearance (ODA) through a log-barrier penalty, enhancing robustness and real-world applicability. BadDet+ demonstrates superior performance in synthetic-to-physical transfer and includes a theoretical analysis to support its effectiveness.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper proposes a unified framework that effectively combines RMA and ODA, simplifying the attack mechanism while increasing its applicability.
2. It introduces new evaluation metrics, such as True Detection Rate (TDR) for RMA and instance-level ASR for ODA, providing a more accurate assessment of attack success.
3. BadDet+ shows strong performance in real-world scenarios, outperforming existing methods in terms of robustness to physical triggers and maintaining clean-task performance.

### Weaknesses

#### Some Related Works


#### comment

1. The paper assumes a strong adversarial setting where the attacker can manipulate the training process, which might not always be realistic. This assumption limits the applicability of the attack in scenarios where the training data or process is more secure or monitored. The framework's effectiveness could be significantly reduced if the attacker does not have full control over the training pipeline, such as in federated learning settings or when using pre-trained models with limited fine-tuning capabilities.
2. The defense evaluation is limited to fine-tuning-based methods and does not explore other defense strategies, such as pruning-based defenses or test-time detection methods. This narrow focus on fine-tuning defenses leaves a gap in understanding the robustness of BadDet+ against a broader range of defense mechanisms. Specifically, the paper does not address how BadDet+ would perform against defenses that modify the model architecture or detection pipeline, which could be more effective than simple fine-tuning.
3. The paper does not provide a detailed analysis of the computational overhead introduced by the log-barrier penalty, which could be a concern for resource-constrained environments. The lack of a thorough analysis of the computational cost makes it difficult to assess the practical feasibility of deploying BadDet+ in real-world applications, especially those with limited computational resources. The paper should include a breakdown of the time and memory costs associated with the log-barrier penalty, as well as how these costs scale with the size of the model and the input data.

### Suggestions

The paper should explore the performance of BadDet+ under more realistic threat models, such as those where the attacker has limited access to the training data or process. For example, the authors could investigate the effectiveness of BadDet+ in a federated learning setting, where the attacker only has access to a subset of the training data, or in a scenario where the attacker can only inject a small number of poisoned samples into the training set. This would provide a more comprehensive understanding of the practical limitations of the attack and its potential impact in real-world scenarios. Additionally, the authors should consider the impact of using pre-trained models and limited fine-tuning, as this is a common practice in many applications. Evaluating the attack's effectiveness under these constraints would provide valuable insights into its robustness and applicability.

To address the limited defense evaluation, the authors should expand their analysis to include a wider range of defense strategies. Specifically, they should investigate the performance of BadDet+ against pruning-based defenses, which can remove redundant connections in the model and potentially disrupt the backdoor. Furthermore, the authors should evaluate the attack's robustness against test-time detection methods, such as anomaly detection or input sanitization techniques. This would provide a more comprehensive understanding of the attack's vulnerabilities and its potential impact in the presence of more sophisticated defenses. The paper should also discuss the trade-offs between different defense strategies and their impact on the performance of the object detection model. This would provide valuable insights for practitioners who need to choose the most appropriate defense strategy for their specific application.

Finally, the paper should provide a detailed analysis of the computational overhead introduced by the log-barrier penalty. This analysis should include a breakdown of the time and memory costs associated with the penalty term, as well as how these costs scale with the size of the model and the input data. The authors should also investigate potential optimizations that could reduce the computational overhead of the attack. For example, they could explore the use of more efficient numerical methods for computing the log-barrier penalty or investigate the possibility of approximating the penalty term using a simpler function. This would make the attack more practical for deployment in resource-constrained environments and would increase the overall impact of the paper.

### Questions

1. How does the computational overhead of the log-barrier penalty impact the scalability of BadDet+ in resource-constrained environments?
2. Can the authors provide more insights into how BadDet+ might perform under different threat models, such as those with limited access to the training process?
3. Are there any potential optimizations that could reduce the computational overhead of the log-barrier penalty without compromising attack effectiveness?

### Rating

6

### Confidence

4

**********