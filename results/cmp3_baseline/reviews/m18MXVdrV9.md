## Summary

This paper introduces INFO-SEDD, a method for estimating information-theoretic quantities (KL divergence, mutual information, entropy) for high-dimensional discrete data using Continuous Time Markov Chains (CTMCs) and discrete diffusion models. The key insight is that by carefully designing the perturbation process (using an absorbing state), a single score model trained on the joint distribution can compute both joint and marginal scores, enabling scalable MI estimation without the "embedding trick" required by continuous estimators. The method is validated on synthetic benchmarks, text summarization model selection, and genomics motif discovery, consistently outperforming variational and embedding-based competitors.

## Strengths

- **Novel and principled theoretical framework**: The paper provides a rigorous derivation connecting CTMCs, Dynkin's formula, and KL divergence estimation, with a clear error bound decomposition showing consistency up to an exponentially decaying truncation bias. This is a genuine theoretical contribution that extends discrete diffusion models beyond generative modeling.

- **Elegant practical solution to a known problem**: The use of an absorbing-state transition matrix to compute marginal scores from a single joint-distribution model (Equation 6) is clever and addresses the key scalability bottleneck. This avoids training separate models for joint and marginal distributions, which would be computationally prohibitive.

- **Strong empirical validation across diverse domains**: The synthetic experiments (Table 1) show INFO-SEDD maintaining accurate estimates even at MI=50 with D=50, where all competitors fail catastrophically. The real-world applications (text summarization model selection with meaningful correlations to human metrics, TATA-box motif discovery in genomics) demonstrate practical utility beyond synthetic benchmarks.

- **Consistency tests with theoretically grounded references**: The paper constructs meaningful consistency tests (text scrambling, label randomization) with order-of-magnitude reference estimates derived from entropy rates and classifier accuracy, providing a principled way to evaluate estimators when ground truth is unavailable.

## Weaknesses

### Fatal
None.

### Major

- **Computational cost and scalability are not adequately characterized**: The paper claims INFO-SEDD is "lightweight and scalable" but provides no runtime comparisons, no analysis of how the method scales with sequence length D or vocabulary size |χ|, and no discussion of the computational overhead of the integral over time in Equation (5). For a method that requires training a discrete diffusion model (which itself is computationally intensive), this is a significant omission. The synthetic experiments use only D up to 50, which is modest for many real-world discrete data applications.

- **Limited comparison to discrete-specific baselines**: The paper compares primarily against continuous estimators (MINE, NWJ, SMILE, MINDE, F-DIME variants) that require the "embedding trick." However, there exist discrete-specific MI estimators (e.g., plug-in estimators with bias correction, the NSB estimator, or estimators based on compression) that are not compared against. The paper would be stronger by including at least one discrete-native baseline to demonstrate that the improvement comes from the discrete diffusion approach rather than simply from avoiding embeddings.

- **Theoretical error bound (Equation 7) is not empirically validated**: While the paper provides a theoretical decomposition of estimation error, there is no experimental validation of this bound. The constants C₁, C₂, εₚ, ε_q are not estimated or discussed in the experiments. The bound's practical tightness and whether it provides useful guidance for hyperparameter selection (e.g., choosing T) is unclear.

### Minor

- **The text summarization model selection analysis (Table 2) reports correlations but does not discuss statistical significance or confidence intervals**: Given the small number of models (15 with human metrics), the reported Pearson correlations (e.g., 0.740 for INFO-SEDD-C vs consistency) would benefit from p-values or confidence intervals to assess reliability.

- **The genomics consistency test (Figure 4) uses a "classifier-based MI" reference that itself is an approximation**: The paper approximates H(Y|X) using H_b(Acc.), which assumes the classifier's errors are uniformly distributed. This approximation's validity is not discussed, and the reference line should be treated as a rough guide rather than ground truth.

- **The paper does not discuss limitations of the absorbing-state approach**: The absorbing state increases the effective support size (adding one token), and the method requires that the perturbation process converges to a known reference distribution π. The practical implications of these choices (e.g., sensitivity to the choice of σ(t), the time horizon T) are not explored.

### Trivial
None.

## Nice-to-Haves

- An ablation study showing the impact of the time horizon T on estimation accuracy, to validate the theoretical claim that truncation bias decays exponentially.
- A comparison of INFO-SEDD's computational cost (training time, inference time) against the best-performing competitors on the synthetic benchmark.
- Discussion of how to choose between INFO-SEDD-J and INFO-SEDD-C in practice, beyond the dimensionality argument given for the genomics experiment.

## Novel Insights

The paper's core insight—that discrete diffusion models with absorbing-state processes can be repurposed for information estimation by exploiting the fact that marginal scores can be extracted from a joint-distribution model—is genuinely novel and opens a new direction for discrete MI estimation. The connection between Dynkin's formula and KL divergence estimation via CTMCs is also a theoretical contribution that may find applications beyond the specific estimator presented here. The paper demonstrates that the "embedding trick" commonly used for discrete data is not only unnecessary but actively harmful for high-MI scenarios, which is an important practical finding.

## Suggestions

- Add a computational cost analysis (training time, inference time, memory usage) comparing INFO-SEDD to the best-performing competitors on at least one synthetic and one real-world benchmark.
- Include at least one discrete-native MI estimator baseline (e.g., the Miller-Madow bias-corrected plug-in estimator or the NSB estimator) for the synthetic experiments with small D and |χ|.
- Provide confidence intervals or p-values for the correlation results in Table 2, and discuss the statistical significance of the observed correlations given the small sample size.

## Score and Decision

The paper presents a novel, theoretically grounded, and empirically validated method for a practically important problem (MI estimation for high-dimensional discrete data). The theoretical framework connecting CTMCs to KL divergence estimation is sound, and the experimental results convincingly demonstrate superiority over existing approaches that rely on continuous embeddings. The main weaknesses are the lack of computational cost characterization and the absence of discrete-native baselines, but these do not invalidate the core contribution. The paper is well-written, the experiments are thorough, and the applications are meaningful.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>