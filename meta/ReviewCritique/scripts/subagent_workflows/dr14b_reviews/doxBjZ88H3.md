### Summary

The paper addresses the problem of distinguishing two neural coding hypotheses, namely whether a sensory neuron encodes the likelihood function $p(x | \theta)$ (where $\theta$ is the external stimulus and $x$ is the neuron's response) or the posterior distribution $p(\theta | x)$ (which incorporates prior information). The authors propose a method based on evaluating the performance of decoding algorithms trained to decode either the likelihood or the posterior from neural responses. They show that the difference in performance between the two approaches can be quantified by the so-called "information gap", and that this quantity can be used to identify the correct neural coding hypothesis. They also propose a method for optimizing stimulus distributions to maximize the information gap, thus making it easier to distinguish between the two hypotheses.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The paper addresses a very important problem in neuroscience, namely how to distinguish between different neural coding hypotheses. The proposed method is well-motivated and theoretically grounded, and the authors provide a clear and detailed derivation of their results. The use of an information-theoretic framework is particularly appealing, as it provides a principled way of quantifying the differences between the two coding hypotheses. The paper is also very well-written and easy to follow, even for readers who are not experts in the field. The figures and diagrams are clear and informative, and the authors do a great job of explaining complex concepts in a simple and intuitive way.

### Weaknesses

#### Some Related Works


#### comment

One potential weakness of the paper is that the proposed method relies on several assumptions about the neural coding process, such as the form of the likelihood function and the prior distribution. It is not clear how robust the method is to violations of these assumptions. Additionally, the paper focuses primarily on theoretical results and simulations, and it would be nice to see some experimental data to validate the proposed method. Another potential limitation is that the method requires access to both the neural responses and the external stimuli, which may not always be available in practice.

It is not clear to what extent the proposed method can be generalized to other neural coding problems beyond the specific case of likelihood vs. posterior coding. For example, can it be used to distinguish between different models of population coding or to analyze the neural code for more complex types of stimuli? The authors could discuss the potential limitations and challenges of applying their method to other settings, and suggest directions for future research.

### Suggestions

The authors should more thoroughly address the limitations imposed by their assumptions regarding the likelihood function and prior distribution. While the paper focuses on a comparison between likelihood and posterior coding, the specific forms of these functions are crucial to the method's performance. For instance, the likelihood function is often assumed to be Gaussian, but in reality, it could have more complex shapes, such as heavy-tailed or multimodal distributions. Similarly, the prior is often assumed to be a simple distribution like a Gaussian or uniform, but real-world priors could be more complex and context-dependent. The authors should investigate how deviations from these assumptions affect the information gap and the ability to distinguish between the two coding schemes. This could involve simulations with different likelihood and prior distributions, or a theoretical analysis of the robustness of the information gap to such variations. Furthermore, it would be beneficial to explore how the method performs when the number of neurons is limited, as this is often the case in experimental settings. 

To strengthen the paper, the authors should also consider the practical challenges of applying their method to real-world data. The requirement of having access to both neural responses and external stimuli is a significant limitation. In many experimental paradigms, the stimulus is not directly controlled or measured, making it difficult to apply the proposed method. The authors should discuss alternative approaches that could be used in such cases, or suggest experimental designs that would allow for the collection of the necessary data. For example, they could explore the use of naturalistic stimuli or consider methods that rely on weaker assumptions about the stimulus. Additionally, the authors should discuss the computational cost of their method, especially when dealing with large datasets. The optimization of stimulus distributions to maximize the information gap could be computationally expensive, and the authors should provide some guidance on how to address this issue. 

Finally, the authors should expand on the potential generalizations of their method to other neural coding problems. While the current focus is on likelihood versus posterior coding, the information-theoretic framework could potentially be applied to other scenarios, such as population coding or the neural code for more complex stimuli. The authors should discuss the challenges and limitations of applying their method to these settings, and suggest directions for future research. For example, they could explore how the information gap could be used to distinguish between different models of population coding, or how it could be adapted to analyze the neural code for temporal stimuli. This would help to broaden the impact of their work and make it more relevant to a wider audience.

### Questions

1. How does the choice of the optimization algorithm affect the results? Are there any specific considerations that need to be taken into account when applying the proposed method to different datasets or experimental settings?

2. How does the proposed method compare to other approaches for distinguishing between different neural coding hypotheses? Are there any advantages or disadvantages of using the information gap compared to other measures?

3. How does the method deal with noise in the neural responses? Is there a way to quantify the uncertainty in the estimates of the information gap?

4. How does the method scale with the number of neurons and the complexity of the stimulus distribution? Are there any computational bottlenecks that need to be addressed?

5. How does the method perform when the true neural coding scheme is somewhere between the likelihood and posterior extremes? Is there a way to quantify the degree to which a neural population encodes likelihood versus posterior information?

### Rating

6

### Confidence

4

**********