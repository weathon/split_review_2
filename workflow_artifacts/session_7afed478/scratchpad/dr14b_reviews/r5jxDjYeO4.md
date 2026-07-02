### Summary

This paper proposes an adaptive serial-parallel decoding framework to accelerate the inference speed of LLMs. The authors first propose a non-invasive pipeline to automatically extract parallelizable data. Then, they introduce a hybrid decoding engine to seamlessly switch between serial and parallel decoding modes. The experimental results demonstrate that the proposed method achieves a good balance between effectiveness and efficiency.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The proposed method is novel and effective. The proposed method achieves a good balance between effectiveness and efficiency.
2. The paper is well-written and easy to follow.

### Weaknesses

#### Some Related Works


#### comment

1. The proposed method requires fine-tuning the model on the parallelized corpus. This may be time-consuming and resource-intensive.
2. The proposed method is specific to parallel decoding. It may not be applicable to other decoding methods such as speculative decoding.

### Suggestions

The paper introduces an interesting approach to accelerate LLM inference through adaptive serial-parallel decoding. However, the practical applicability of the method could be significantly enhanced by addressing the fine-tuning requirement. The authors should explore techniques to mitigate the computational cost of fine-tuning, such as parameter-efficient fine-tuning methods or knowledge distillation. Furthermore, a detailed analysis of the trade-off between fine-tuning time and inference speedup would be valuable. It would also be beneficial to investigate the sensitivity of the method to the amount of parallelized data used for fine-tuning. For example, how does the performance vary when using different percentages of the parallelized corpus? This would provide a more comprehensive understanding of the method's practical limitations and potential for real-world deployment.

To broaden the applicability of the proposed method, the authors should investigate its compatibility with other decoding techniques, particularly speculative decoding. While the current approach focuses on parallel decoding, many practical applications may benefit from a hybrid approach that combines the strengths of different decoding methods. For instance, speculative decoding could be used to generate draft sequences, which are then refined using the proposed parallel decoding method. This would require careful consideration of how to integrate the two methods, including the management of the KV-cache and the synchronization of the decoding process. The authors should also explore the potential for adapting the proposed method to other parallelization strategies, such as model parallelism or pipeline parallelism, to further improve its scalability and efficiency.

Finally, the paper would benefit from a more detailed analysis of the types of tasks and sequences that are suitable for parallel decoding. While the authors mention that tasks with clear sub-tasks are more amenable to parallelization, they should provide a more concrete characterization of these tasks. For example, what are the key features of a task that make it suitable for parallel decoding? How does the performance of the proposed method vary across different types of tasks? A more thorough investigation of these questions would help to clarify the scope of the proposed method and provide guidance for its practical application. Additionally, the authors should explore the potential for automatically identifying parallelizable segments within a sequence, which would further enhance the usability of the method.

### Questions

1. What is the computational overhead of the proposed method? How does it compare to the baselines in terms of memory usage, latency, and throughput?
2. How does the proposed method perform on other datasets and tasks? How does it generalize to different domains and modalities?
3. How does the proposed method handle errors and failures in the parallel branches? How does it ensure the robustness and reliability of the decoding process?
4. What are the limitations and challenges of the proposed method? What are the future directions and potential improvements?

### Rating

6

### Confidence

3

**********