### Summary

The paper proposes a method for motion prediction and planning. An autoencoder is trained on the Waymo Open Motion Dataset to encode trajectories given the environment into discrete tokens and decode the trajectory given the tokens and the environment. During planning, a greedy search is performed on the latent space to find the tokens that minimize a given objective function.

### Soundness

2

### Presentation

3

### Contribution

2

### Strengths

- The paper explores a simple yet interesting idea of performing motion prediction and planning by performing search in the latent space of an autoencoder.
- The results on the WOMD dataset show that the proposed method can generate diverse behaviors and can be guided with different objectives.

### Weaknesses

#### Some Related Works


#### comment

 - The main weakness of the paper is the lack of quantitative results. The paper only shows ADE and FDE results for motion prediction, but does not benchmark the proposed method against the baselines for the planning tasks. There are no ADE/FDE results for the multi-agent token search experiments. There are no results for the speed reduction objective. Etc.
- The ADE/FDE results in Table 2 are not very strong. The paper should include ADE/FDE results for the "random" objective as well to show that the variance minimization objective is actually improving the prediction results. The "Decoder with variance minimization objective" does not seem to outperform the DriveGPT baseline. But this might be due to the fact that the proposed autoencoder is trained for reconstruction and not for prediction, and thus might be underfitting for the motion prediction task.
- The paper overclaims that the proposed method is a general motion planning framework and that the autoencoder latent space is highly structured. The experiments only show that the proposed method can perform motion prediction and single-agent/multi-agent token search on the WOMD dataset. There are no experiments on other datasets or other planning tasks. The paper should at least include additional results for other planning tasks (e.g., collision avoidance) or other datasets to show that the method can generalize.

### Suggestions

The paper needs to significantly expand its quantitative evaluation to support its claims. The lack of comprehensive benchmarks, especially for the planning tasks, makes it difficult to assess the true potential of the proposed method. For instance, the paper should include ADE/FDE results for the planning tasks, not just for the motion prediction task. Furthermore, the multi-agent token search experiments should also include ADE/FDE results to demonstrate the quality of the generated trajectories. The absence of results for the speed reduction objective is also a significant oversight. The paper should include a detailed analysis of the performance of the proposed method across different scenarios and compare it with relevant baselines. This would provide a more complete picture of the method's capabilities and limitations. The current results are insufficient to justify the claims made about the method's generality and effectiveness.

The ADE/FDE results presented in Table 2 are not compelling, and the paper needs to provide more evidence to support the effectiveness of the variance minimization objective. The fact that the "Decoder with variance minimization objective" does not outperform the DriveGPT baseline is concerning. The paper should include a comparison with a random objective to show that the variance minimization objective is indeed improving the prediction results. It is also important to investigate why the proposed autoencoder, trained for reconstruction, is not achieving better motion prediction results. The paper should explore alternative training objectives or architectures that are better suited for motion prediction. A more thorough analysis of the autoencoder's latent space is also needed to justify the claim that it is highly structured. The paper should provide quantitative evidence to support this claim, such as by showing that the latent space exhibits meaningful clustering or that the latent codes are interpretable.

To address the overclaiming issue, the paper should include additional experiments on other datasets and planning tasks. The current experiments are limited to the WOMD dataset and motion prediction, single-agent, and multi-agent token search. The paper should at least include results for other planning tasks, such as collision avoidance or navigation in complex environments. It would also be beneficial to evaluate the method on other datasets to demonstrate its generalization capabilities. The paper should also provide a more detailed analysis of the method's limitations and discuss potential avenues for future research. This would help to provide a more balanced and realistic assessment of the proposed method's contributions.

### Questions

- What are the ADE/FDE results for the "Decoder with random objective"? How much is the "Decoder with variance minimization objective" improving over the "Decoder with random objective"? 
- How does the "Decoder with variance minimization objective" compare with the DriveGPT baseline in Table 2?
- Is there a reason why the ADE/FDE results for the "Decoder with variance minimization objective" are much lower than the single-agent token search results in Table 3?
- Is there a reason why the ADE/FDE results for the "Decoder with variance minimization objective" are much lower than the single-agent token search results in Table 3?
- Are there any results for the speed reduction objective in Table 2/3?
- Are there any results on other datasets or other planning tasks?

### Rating

3

### Confidence

4

**********