### Summary

The paper proposes a new backpropagation algorithm based on the inverse sigmoid function to calculate the difference instead of the derivative. The authors claim that this method is more precise and can avoid gradient vanishing. The effectiveness of the proposed method is verified with basic examples.

### Soundness

2 fair

### Presentation

2 fair

### Contribution

2 fair

### Strengths

1. The paper is well-written and easy to follow.
2. The idea of using the inverse sigmoid function to calculate the difference is novel and interesting.

### Weaknesses

#### Some Related Works


#### comment

1. The experiments are too simple to demonstrate the effectiveness of the proposed method. The experiments are limited to a sine curve fitting and a basic transformer classification task. These experiments are insufficient to demonstrate the general applicability and effectiveness of DBP in more complex scenarios, such as large-scale image recognition or natural language processing tasks. The lack of experiments on standard benchmark datasets makes it difficult to assess the practical value of the proposed method.
2. The authors only compare the proposed method with the default back-propagation method. There is no comparison with other related methods. The absence of comparisons with other optimization techniques, such as adaptive gradient methods (e.g., Adam, RMSprop) or other variants of backpropagation, makes it difficult to ascertain the relative advantages and disadvantages of DBP. This lack of comparative analysis limits the impact of the paper.

### Suggestions

The paper needs to significantly expand its experimental validation to demonstrate the practical utility of the proposed Difference Back Propagation (DBP) method. The current experiments, limited to a sine curve fitting and a basic transformer classification task, are insufficient to establish the method's effectiveness in more complex and realistic scenarios. To address this, the authors should include experiments on standard benchmark datasets commonly used in the deep learning community, such as CIFAR-10 or ImageNet for image classification, and SST-2 or IMDB for natural language processing. These datasets are widely used and provide a clear benchmark for evaluating the performance of new optimization techniques. Furthermore, the experiments should include a variety of network architectures and hyperparameter settings to assess the robustness and generalizability of DBP. The authors should also provide a detailed analysis of the training dynamics, including convergence speed and final accuracy, to provide a comprehensive understanding of the method's behavior.

In addition to expanding the experimental scope, the paper should include a more thorough comparison with existing optimization methods. The current comparison with only the default backpropagation method is insufficient to demonstrate the advantages of DBP. The authors should compare DBP with other state-of-the-art optimization techniques, such as Adam, RMSprop, and other variants of backpropagation. This comparison should include a detailed analysis of the strengths and weaknesses of each method, as well as a discussion of the scenarios where DBP is most effective. The authors should also provide a theoretical analysis of the convergence properties of DBP, and compare it with the theoretical properties of other optimization methods. This would provide a more rigorous justification for the proposed method and help to understand its behavior in different scenarios. The comparison should also include a discussion of the computational cost of DBP compared to other methods, as this is an important factor in practical applications.

Finally, the paper should address the fundamental issue of applying DBP to ReLU activation functions more rigorously. The current approach of simply defining the derivative at x=0 as 1 is not mathematically sound and lacks a strong theoretical justification. A more thorough analysis of the behavior of DBP with ReLU, especially around the non-differentiable point, is needed. This could involve exploring alternative definitions of the derivative at x=0 or modifying the DBP method to better handle non-differentiable points. Furthermore, the authors should provide a theoretical analysis of the convergence properties of DBP, especially when applied to ReLU, to demonstrate its stability and reliability. Without a more rigorous treatment of this issue, the applicability of DBP to modern deep learning architectures, which heavily rely on ReLU, remains questionable.

### Questions

1. Can this method be applied to the most popular activation function ReLU?
2. Are there experiments on large-scale datasets?

### Rating

3: reject, not good enough

### Confidence

4: You are confident in your assessment, but not absolutely certain. It is unlikely, but not impossible, that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work.

**********