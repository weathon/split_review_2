## Summary

This paper proposes an active learning framework for flow matching generative models, targeting scenarios with continuous condition labels (e.g., shape design where labels come from expensive simulations). The authors analyze flow matching through a piecewise-linear neural network lens and a closed-form model, claiming that data with identical labels increase generation diversity while data with distinct labels improve accuracy. Based on this, they design two query strategies—one for diversity (Q_D) and one for accuracy (Q_A)—and a hybrid that trades off between them. Experiments on synthetic and three aerodynamic shape datasets show limited improvement over standard discriminative-model active learning baselines.

## Strengths

- The paper addresses a practically relevant and under-explored problem: active data selection for generative models, specifically flow matching, in domains with continuous labels and expensive annotation.
- The idea of decoupling the query strategy from the trained flow matching model (using only dataset-level computations and an auxiliary label predictor) is sensible from an efficiency standpoint.
- The experimental evaluation on real aerodynamic design datasets (airfoil, flying wing, starship) demonstrates the applicability of the proposed strategies to a niche but important domain.

## Weaknesses

### Fatal

- **The theoretical foundation is insufficient to support the claimed conclusions.**  
  The analysis relies on a chain of unvalidated and unrealistic assumptions: (i) that the neural network in the flow matching model behaves as a continuous piecewise-linear function that interpolates linearly between data points; (ii) that the closed-form flow matching vector field with optimal transport noise schedule leads to Eq. (2)–(3); (iii) that condensation (parameter reduction) occurs under the training conditions used. No evidence (theoretical or empirical) is provided that these assumptions hold for any practical flow matching model. The authors present Lemma 1 and Lemma 2 only as sketched claims (Lemma 2’s error bound is stated as an inequality without proof or justification). As a result, the core claims—that data with the same label increase diversity, that data with different labels increase accuracy, and that these two effects are necessarily conflicting—are not derived rigorously. The paper therefore does not establish the claimed “generalization mechanisms.”

- **The proposed query strategies lack novelty and are not convincingly shown to be better than existing active learning methods for generative models.**  
  Q_D is essentially a weighted combination of a label-similarity penalty, label entropy, and coreset-like distance in data space. Q_A is simply coreset in the label space. These are known heuristics (e.g., coreset, entropy sampling) dressed in new notation. The paper does not compare against any active learning method that was explicitly designed for generative models (e.g., VAAL, TAVAAL, GALISP mentioned in related work). The baselines chosen—“Committee” using SVR/RF/XGBoost/RBF, “Anchor” from GALISP (but only tested on anchor conditions), and “Coreset” in data space—are either weak or misaligned. Hence the experimental results do not support the claim that the proposed strategies outperform active learning for generative models. The “pilot study” framing is not an excuse for lack of proper baselines.

- **The experimental methodology and metrics are questionable.**  
  - The diversity score (Eq. 8) is a custom Vendi-score variant based on average pairwise Euclidean distance of generated samples. It does not measure mode coverage or sample variety in the standard sense (e.g., distinct modes, perceptual diversity).  
  - The accuracy score (Eq. 9) measures the MSE between the condition and the true label of the generated sample—but in an inverse design setting, this metric conflates generative model accuracy with the query strategy’s effect. It is not shown that the MSE reflects meaningful design quality.  
  - No standard generation quality metrics (e.g., FID, precision/recall for sets, coverage) are reported.  
  - Only 5 iterations of active learning are shown; it is unclear whether the trends continue.  
  - The baseline “Random” often performs competitively or better than the proposed Q_A in accuracy (Fig. 4b), contradicting the claim that Q_A improves accuracy.  
  - The ablation study (Fig. 9) only tests Q_D terms; there is no ablation for Q_A or for the hybrid.

### Major

- **The paper does not clearly define the active learning setup for generative models.**  
  In a standard pool-based active learning loop, the model is retrained after each query round. The authors state that their query strategies “operate directly on the dataset for data selection” and avoid “repeated training of the flow matching model” (Section 2.4). This suggests that the flow matching model is trained only once at the end after all queries? Or is it trained iteratively? The experimental section does not specify whether the flow matching model is retrained after each round of data addition. If it is not retrained, then the comparison to methods like Coreset (which assume iterative retraining) is unfair. This ambiguity invalidates the interpretation of results.

- **The piecewise-linear framework is not connected to the actual flow matching training process.**  
  The authors use the closed-form expression of the vector field under a specific noise schedule (optimal transport) but do not show that iterative training of a neural network approximates this closed-form. For real flow matching models, the network learns a denoising field that is not guaranteed to exhibit linear interpolation in the condition space. The entire theoretical derivation therefore applies only to an idealized and unrealistic regime, and no attempt is made to justify its relevance.

### Minor

- The paper uses “continuous condition dataset” as a key term but never formally defines it beyond saying labels are continuous (e.g., ℝ¹, ℝ³, ℝ⁴). The distinction between “categorical” and “continuous” labels is important for the claim that existing active learning methods designed for discriminative models with categorical labels are inadequate, but this is not used to derive the proposed strategies. In fact, the proposed Q_D and Q_A are formulated without any explicit handling of continuous label structure (e.g., using clustering for entropy, Euclidean distances for labels).

- The method for predicting labels of unlabeled data uses RBF neural networks, but no justification is given for this choice over other regressors, and the accuracy of these predictions is not reported. If the label predictions are poor, the query selection will be unreliable.

- Writing clarity is below the ICLR standard: many equations are not explained (e.g., the derivation of Eq. 1, the meaning of p_{t,i}, the definition of “entropy” in Eq. 4 is vague), Figure captions are duplicated and incomplete, and Section 2.2 is hard to follow.

### Trivial

- The claim that “acquiring high-fidelity numerical simulation results entails substantially greater effort and expense” is repeated multiple times without quantitative evidence.
- Reference “Scardelis et al. (2023)” appears as a probable misspelling of “Scarvelis et al. (2023)”; the reference list does not include this work.

## Nice-to-Haves

- A comparison with at least one active learning method specifically designed for generative models (e.g., VAAL, TAVAAL) would strengthen the claims.
- An analysis of how the choice of label predictor affects the query selection quality.
- Experiments on a standard generative benchmark (e.g., class-conditional image generation) to show broader applicability of the proposed strategies.

## Novel Insights

None beyond the paper’s own contributions. The observation that data with similar labels increase interpolation diversity and that data with diverse labels reduce interpolation error is a direct consequence of the assumed piecewise-linear interpolation mechanism, not a new empirical or theoretical finding. The proposed query strategies are straightforward operationalizations of this observation.

## Suggestions

1. Provide a rigorous theoretical derivation of Lemma 1 and Lemma 2, including the assumptions under which they hold, and validate those assumptions on real flow matching models (e.g., by checking linearity of the learned vector field in condition space).
2. Clarify the active learning loop: state explicitly whether the flow matching model is retrained after each query round. If it is not, argue why this is acceptable and compare to methods that also do not retrain.
3. Include at least one baseline specifically designed for active learning in generative models (e.g., VAAL).
4. Use standard evaluation metrics for generation quality (FID, precision/recall, coverage) in addition to the custom diversity/accuracy metrics.
5. Report the accuracy of the RBF label predictor and discuss how label prediction errors affect the query selection.
6. Conduct more than 5 active learning rounds to demonstrate the trend stabilizes.

## Score and Decision

The paper attempts to bridge two interesting areas (active learning and generative modeling) but the theoretical foundation is unsubstantiated, the proposed strategies are not convincingly novel, and the experimental evaluation lacks appropriate baselines and rigorous metrics. The fatal weaknesses—particularly the reliance on unrealistic assumptions without validation and the failure to compare against proper baselines—prevent the paper from making a sound contribution.

**Score: 3** (reject)

MY FINAL SCORE: <score>3</score>  
MY FINAL DECISION: <decision>Reject</decision>