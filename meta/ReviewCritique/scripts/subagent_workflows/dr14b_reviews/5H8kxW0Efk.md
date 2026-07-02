### Summary

This paper proposes a new data-driven neural approach to combinatorial optimization. The authors learn the parameters of an iterative dynamical system, parameterized by a small neural network, which efficiently samples good solutions for typical instances of the NP-hard Max-Cut/Ising problem. The proposed algorithm is tested on some problem instances and compared with some existing algorithms.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

The proposed algorithm is new and the authors do some numerical experiments to test the performance.

### Weaknesses

#### Some Related Works


#### comment

The proposed algorithm is quite complicated, so is the presentation. It is hard to get the idea of the algorithm. The authors do some numerical experiments to test the performance of the proposed algorithm but without further discussion. The algorithm has many hyperparameters, which makes it hard to understand the role of each part of the algorithm. The authors do some numerical experiments to test the performance of the proposed algorithm but without further discussion. In particular, there is no discussion about why the proposed algorithm performs well, given that it is not clear what the algorithm is doing.

### Suggestions

The paper would benefit significantly from a more intuitive explanation of the proposed algorithm. Currently, the description is dense and difficult to follow, making it challenging to grasp the core idea behind the approach. The authors should consider breaking down the algorithm into its fundamental components and explaining the purpose of each part in simpler terms. For example, instead of immediately presenting the mathematical formulation, they could start with a high-level overview of the iterative dynamical system and how it relates to the Max-Cut/Ising problem. A clear analogy or a step-by-step walkthrough of a simple example could greatly improve the reader's understanding. Furthermore, the role of the neural network in parameterizing the system needs to be clarified. What specific aspects of the iterative process is the neural network controlling, and how does this contribute to finding better solutions? A more pedagogical approach to explaining the algorithm is crucial for the paper's accessibility and impact.

In addition to a clearer explanation of the algorithm, the paper needs a more thorough discussion of the numerical results. While the authors present performance comparisons with existing algorithms, they fail to provide any insights into why the proposed algorithm achieves the observed results. It is not sufficient to simply state that the algorithm performs well; the authors need to analyze the underlying mechanisms that lead to its success. For instance, do the learned parameters exhibit any specific patterns or structures? How do these parameters influence the search process? A deeper analysis of the learned parameters and their impact on the algorithm's behavior is essential. Furthermore, the authors should investigate the sensitivity of the algorithm to its hyperparameters. While they mention that the algorithm is not very sensitive, this claim needs to be supported by more detailed experiments and analysis. A systematic study of how different hyperparameter settings affect the performance would provide valuable insights into the algorithm's robustness and limitations.

Finally, the paper should include a more detailed comparison with existing algorithms, focusing on the specific strengths and weaknesses of each approach. The current comparison is rather superficial, and it is not clear what advantages the proposed algorithm offers over existing methods. A more in-depth analysis of the algorithm's performance on different types of problem instances would be beneficial. For example, are there specific problem structures for which the proposed algorithm is particularly well-suited? Are there any limitations in terms of problem size or complexity? A more comprehensive evaluation of the algorithm's performance, along with a detailed discussion of its advantages and disadvantages, would greatly enhance the paper's contribution.

### Questions

1. Could the authors explain why the proposed algorithm performs well? What are the underlying mechanisms that lead to its success? 
2. The proposed algorithm has many hyperparameters. What is the role of each part of the algorithm? How do they influence the performance of the algorithm? 
3. The authors should discuss the strengths and weaknesses of the proposed algorithm compared to existing algorithms.

### Rating

3

### Confidence

3

**********