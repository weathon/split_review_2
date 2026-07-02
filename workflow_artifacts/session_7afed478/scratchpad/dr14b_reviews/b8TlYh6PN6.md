### Summary

The authors provide a graphical characterization of distributional equivalence for linear non-Gaussian latent-variable models. Based on it, they develop a constraint-based algorithm, glvLiNG, that recovers the underlying model up to equivalence from data without any structural assumptions.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

The authors introduce edge ranks, which contribute a missing piece to the broader toolbox for latent-variable causal discovery, with potential use across many settings.

The authors provide a procedure to traverse the whole equivalence class and develop an algorithm to recover causal structures from data up to such equivalence. To our knowledge, this is the first structural-assumption-free discovery method.

### Weaknesses

#### Some Related Works


#### comment

The real-world data example is too simple to demonstrate the proposed method's effectiveness.

The authors state that they focus on the case with the exact number of latent variables known. However, in real-world scenarios, this is often unknown. It would be beneficial to discuss the potential impact of mis-specifying the number of latent variables on the proposed method's performance and how one might choose the number of latent variables in practice.

The authors state that "the glvLiNG algorithm serves more as a proof of concept, showing that such equivalence is indeed recoverable without any structural assumption" and that "the main focus of this work is to characterize distributional equivalence". However, it is unclear how the provided characterization can be useful for testing the equality of two given causal models. Additionally, it seems that the algorithms for traversing the whole equivalence class and recovering causal structures from data are highly dependent on the exact number of latent variables. Thus, it appears that the practical usefulness of this work is limited.

### Suggestions

The paper's focus on characterizing distributional equivalence is a valuable theoretical contribution, but its practical implications need further clarification. The current presentation leaves the reader wondering how the established equivalence classes can be leveraged in real-world scenarios beyond simply identifying that two models are equivalent. For instance, it would be beneficial to discuss how one might use the characterized equivalence to guide the selection of appropriate causal models or to develop more robust inference methods. The authors should provide concrete examples of how this characterization can be used to test the equality of two given causal models, detailing the steps involved and the computational complexity of such a test. Furthermore, the paper should explore the potential of using the equivalence classes to develop algorithms that are robust to model misspecification, which is a common issue in practical applications.

While the glvLiNG algorithm is presented as a proof of concept, its dependence on the exact number of latent variables significantly limits its applicability. The authors should explore methods for relaxing this assumption, such as incorporating techniques for model selection or robust estimation that can handle uncertainty in the number of latent variables. It would be beneficial to investigate how the algorithm's performance degrades when the number of latent variables is mis-specified and to provide guidelines for choosing the number of latent variables in practice. For example, the authors could explore the use of information criteria or cross-validation techniques to select the number of latent variables. Additionally, the authors should discuss the computational cost of the proposed algorithm, especially in high-dimensional settings, and provide insights into how this cost can be reduced.

Finally, the paper should address the practical challenges of applying the proposed method to real-world data. The current real-world example is too simplistic and does not adequately demonstrate the method's effectiveness in complex scenarios. The authors should consider using more realistic datasets with a larger number of variables and more complex causal structures. It would also be beneficial to compare the proposed method with existing causal discovery algorithms on these datasets to highlight its strengths and weaknesses. The authors should also discuss the limitations of the proposed method and provide guidance on when it is appropriate to use it in practice. This would help to make the paper more accessible to a broader audience and increase its practical impact.

### Questions

1. The authors state that they focus on the case with the exact number of latent variables known. However, in real-world scenarios, this is often unknown. It would be beneficial to discuss the potential impact of mis-specifying the number of latent variables on the proposed method's performance and how one might choose the number of latent variables in practice.

2. The authors state that "the glvLiNG algorithm serves more as a proof of concept, showing that such equivalence is indeed recoverable without any structural assumption" and that "the main focus of this work is to characterize distributional equivalence". However, it is unclear how the provided characterization can be useful for testing the equality of two given causal models. Additionally, it seems that the algorithms for traversing the whole equivalence class and recovering causal structures from data are highly dependent on the exact number of latent variables. Thus, it appears that the practical usefulness of this work is limited.

### Rating

6

### Confidence

4

**********