### Summary

This paper presents an audio codec designed to learn decoupled representations for speech and background sound, and within speech, it further separates semantic and paralinguistic components. The proposed model achieves promising results on multiple downstream tasks.

### Soundness

2

### Presentation

2

### Contribution

3

### Strengths

1. The proposed audio codec can learn decoupled representations for speech and background sounds, as well as semantic and paralinguistic components within speech.
2. The proposed model achieves promising results on multiple downstream tasks.

### Weaknesses

#### Some Related Works


#### comment

1. The experiments are not sufficient. The authors should compare their model with more speech tokenizers on tasks such as ASR and TTS, and provide more examples of voice conversion.
2. The authors should explain the advantages of the proposed model over speech separation followed by a speech tokenizer in downstream tasks.
3. The authors should explain the motivation for using different RVQs in the background sound and speech branches, and provide results when the background sound RVQ is applied to the speech branch and vice versa.
4. The authors should explain the motivation for using different codebooks in the speech and background sound branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
5. The authors should explain the motivation for using different codebook sizes in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
6. The authors should explain the motivation for using different codebook dimensions in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
7. The authors should explain the motivation for using different codebook numbers in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
8. The authors should explain the motivation for using different codebook dimensions in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
9. The authors should explain the motivation for using different codebook strides in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
10. The authors should explain the motivation for using different codebook lengths in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
11. The authors should explain the motivation for using different codebook channel in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
12. The authors should explain the motivation for using different codebook channel in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
13. The authors should explain the motivation for using different codebook channel in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
14. The authors should explain the motivation for using different codebook channel in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
15. The authors should explain the motivation for using different codebook channel in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
16. The authors should explain the motivation for using different codebook channel in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
17. The authors should explain the motivation for using different codebook channel in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
18. The authors should explain the motivation for using different codebook channel in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
19. The authors should explain the motivation for using different codebook channel in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.
20. The authors should explain the motivation for using different codebook channel in the two branches, and provide results when the background sound codebook is applied to the speech branch and vice versa.

### Suggestions

The paper introduces an interesting approach to audio codec design by aiming to disentangle speech and background sound representations, further dividing speech into semantic and paralinguistic components. However, the experimental validation needs significant expansion to fully support the claims. Specifically, the authors should compare their model against a wider range of speech tokenizers, not just a single baseline, on downstream tasks like ASR and TTS. This would provide a more comprehensive understanding of the model's performance relative to the state-of-the-art. Furthermore, the paper would benefit from more qualitative examples, particularly for the voice conversion task, to better illustrate the model's capabilities in a perceptual context. The current evaluation lacks sufficient detail to fully assess the practical impact of the proposed method.

Furthermore, the paper needs a more thorough investigation into the architectural choices, particularly regarding the use of different RVQs and codebooks in the speech and background sound branches. The authors should provide a clear rationale for these design decisions and conduct ablation studies to demonstrate their effectiveness. For instance, swapping the RVQs between the two branches would help to understand if the observed performance is due to the specific design or simply the inherent characteristics of the data. Similarly, the impact of using different codebook sizes, dimensions, numbers, strides, lengths, and channel sizes should be explored through systematic experiments. This would help to determine the optimal configuration for each branch and provide a deeper understanding of the model's behavior. Without these detailed analyses, it is difficult to ascertain the true contribution of the proposed architecture.

Finally, the paper should address the potential benefits of using a speech separation module followed by a speech tokenizer as an alternative approach. The authors need to provide a clear explanation of why their proposed method is superior to this more straightforward pipeline, especially in terms of computational efficiency and performance. This comparison is crucial for justifying the complexity of the proposed model. The current lack of such a comparison leaves a significant gap in the evaluation. The authors should also consider exploring the impact of different speech separation techniques on the overall performance, which would provide a more complete picture of the model's strengths and weaknesses. Addressing these points would significantly strengthen the paper and make a more compelling case for the proposed approach.

### Questions

Please see weaknesses.

### Rating

6

### Confidence

3

**********