### Summary

This paper is concerned with geodesic principal component analysis (GPCA) of probability distributions, i.e. the identification of geodesic curves in Wasserstein space that best describe the variation of a dataset. The authors propose methods for Gaussian distributions and a general approach for absolutely continuous distributions, which are based on a parametrization of geodesics using neural networks. The methods are demonstrated on real-world datasets.

### Soundness

2

### Presentation

2

### Contribution

2

### Strengths

The paper is mathematically well written and provides a good introduction to the Wasserstein metric, the related Bures-Wasserstein and Otto-Wasserstein geometries, as well as geodesic PCA. The proposed algorithm to solve the exact GPCA problem in the Wasserstein space is novel. The paper contains a large number of background material and additional experiments in the appendix.

### Weaknesses

#### Some Related Works


#### comment

The main contribution of the paper is the proposed algorithm to solve the exact GPCA problem in the Wasserstein space. However, there is no mathematical analysis of the proposed algorithm, e.g. convergence analysis or computational complexity analysis. The algorithm's performance is demonstrated on real-world datasets, but there is no systematic evaluation of its robustness or sensitivity to hyperparameter choices. The lack of theoretical guarantees makes it difficult to assess the reliability of the method in different scenarios. Furthermore, the computational cost of the algorithm is not thoroughly investigated, which is a crucial aspect for practical applications, especially when dealing with large datasets. The paper would benefit from a more rigorous analysis of the algorithm's properties beyond empirical demonstrations.

### Suggestions

The paper would significantly benefit from a more in-depth analysis of the proposed algorithm's properties. Specifically, a convergence analysis is needed to ensure that the algorithm reaches a stable solution, and this analysis should not only consider the convergence of the loss function but also the convergence of the geodesic parameters. This could involve examining the properties of the optimization landscape, such as the existence of saddle points or local minima, and how the proposed optimization method navigates these challenges. Furthermore, a theoretical analysis of the computational complexity of the algorithm is essential to understand its scalability. This should include an analysis of the time and memory requirements as a function of the dataset size and the dimensionality of the probability distributions. Such an analysis would provide valuable insights into the practical applicability of the method.

In addition to the theoretical analysis, a more systematic evaluation of the algorithm's performance is needed. This should include a sensitivity analysis to hyperparameter choices, such as the learning rate, the number of neurons in the MLP, and the regularization parameters. The paper should also explore the robustness of the algorithm to different types of noise and outliers in the data. This could involve adding Gaussian noise to the data or introducing adversarial examples to test the algorithm's resilience. Furthermore, it would be beneficial to compare the proposed method with other existing approaches for geodesic PCA or related problems, not only in terms of performance but also in terms of computational cost and robustness. This would provide a more comprehensive understanding of the strengths and weaknesses of the proposed algorithm.

Finally, the paper should provide more details on the practical implementation of the algorithm. This includes a discussion of the choice of optimization algorithm, the initialization of the neural network parameters, and the stopping criteria. The authors should also provide guidelines for selecting appropriate hyperparameters for different datasets. Furthermore, the paper should include a more detailed discussion of the limitations of the proposed method and potential directions for future research. This would help to put the contribution of the paper in a broader context and guide future work in this area. The inclusion of such details would greatly enhance the practical value and impact of the paper.

### Questions

- What is the computational complexity of the proposed algorithm?
- What is the convergence of the proposed algorithm?

### Rating

6

### Confidence

2

**********