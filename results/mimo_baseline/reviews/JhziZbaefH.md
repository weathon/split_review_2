## Summary

This paper proposes OML, a brain-inspired hierarchical modular neural network for online multimodal learning that can continuously learn new concepts and associations across modalities without forgetting previously learned ones. The system includes a reference extraction algorithm that identifies which specific features a word refers to, and a human-in-the-loop conflict detection mechanism that asks the user questions when input conflicts with prior knowledge. Experiments on small-scale fruit/object datasets with vision and audition (plus taste extension) demonstrate competitive or superior performance compared to both offline and online baselines.

## Strengths

- **Interesting problem formulation**: The paper addresses the underexplored intersection of online continual learning, multimodal learning, and interactive human-in-the-loop learning. The combination of these capabilities is a genuinely valuable research direction that few prior works tackle together.

- **Reference extraction algorithm (Section 3.4)**: The idea of using the coefficient of variation across successive samples to identify which feature dimensions a word refers to is clever and well-motivated by the example of learning color words versus object names. This is a genuinely novel contribution that addresses a real problem in multimodal grounding.

- **Systematic experimental design**: The experiments are structured around four key capabilities: (1) baseline multimodal retrieval, (2) precise referring with color words, (3) modal extension to taste, and (4) conflict detection. Each experiment isolates a specific claimed capability, and the open/close environment protocol tests for catastrophic forgetting. The coverage of multiple tasks (V→A, A→V, V→T, T→V, etc.) is thorough.

## Weaknesses

### Fatal

None.

### Major

- **Severely limited experimental scale**: The experiments use only two small, domain-specific datasets (Fruits and HomeF) containing common fruits/objects with Chinese names. These are essentially toy problems with very limited vocabulary and object diversity. There are no experiments on standard continual learning benchmarks (e.g., Split-MNIST variants, CORe50), standard multimodal retrieval benchmarks (e.g., Flickr30k, MS-COCO), or any dataset with modern deep feature representations. It is impossible to assess whether the method scales beyond identifying ~10 types of fruits. This fundamentally limits the paper's contribution to the community.

- **No ablation studies**: The method has many interacting components—frequency encoding, lateral connections, reference extraction, conflict detection, ascending/descending pathways—and numerous hyperparameters (θ, T, ϑ, r). Without ablation studies, it is unclear which components are essential for performance. For example: how much does the reference extraction algorithm contribute vs. the conflict detection mechanism? Is the frequency encoding necessary, or would simpler feature routing suffice?

- **Unfair baseline comparisons**: The offline methods (DAE, DBM, DJSRH, NRCH, FUME) are designed for batch training and are fundamentally misaligned with the online evaluation protocol. The paper acknowledges that these methods can be "iteratively optimized multiple times" yet forces them to learn each sample once. This setup inherently disadvantages batch methods and makes the open-environment comparison misleading. The meaningful comparisons are with ART and AEN, but these are not analyzed separately with appropriate framing.

- **Excessive reliance on human-in-the-loop without analysis**: The paper states that "if the question posed to the user by OML remains unanswered for a certain period of time, we set the answer to be positive." This default-accept policy could significantly inflate accuracy and undermines the conflict detection contribution. There is no analysis of how frequently questions are asked, what fraction receive answers, or the sensitivity of results to this default policy.

### Minor

- **No hyperparameter sensitivity analysis**: The method uses fixed values (θ = quarter of 2-norm, T = 150, ϑ = 0.8, r = 0.5) without any sensitivity analysis. Given that the method relies on threshold-based decisions throughout, understanding sensitivity is important.

- **No scalability discussion**: The computational complexity of the growing network, the reference extraction across many feature dimensions, and the conflict detection across all learned concepts is not analyzed. As the number of learned concepts grows, the pairwise comparisons could become expensive.

- **Feature extraction is hand-engineered**: The visual features (Fourier descriptors of SAM-segmented boundaries, mean color) and auditory features (MFCCs) are fully hand-designed. The method's performance is therefore entangled with these specific feature choices, and it is unclear how it would perform with learned representations.

### Trivial

None.

## Nice-to-Haves

- A pseudocode or algorithm box summarizing the full learning procedure would greatly improve readability and reproducibility.
- Experiments on at least one larger-scale dataset with modern feature representations would substantially strengthen the claims.
- Analysis of the number of neurons created over time and memory growth.

## Novel Insights

The reference extraction algorithm (Section 3.4) is the paper's most novel contribution. The observation that repeated exposure to a word paired with varying objects reveals which feature dimensions the word refers to (via low coefficient of variation) is a genuinely elegant idea that connects statistical stability to semantic grounding. This could have broader applications beyond the specific architecture presented. The frequency-based routing mechanism (using λ parameters to direct signals to correct channels) is also an interesting design choice for preventing cross-modal interference, though its necessity is not demonstrated.

## Suggestions

- Add ablation studies removing each major component (reference extraction, conflict detection, lateral connections, frequency encoding) to understand their individual contributions.
- Replace or supplement the small fruit datasets with at least one experiment on a standard continual learning or multimodal retrieval benchmark.
- Analyze the conflict detection mechanism more rigorously: frequency of questions, accuracy of detected conflicts, and impact of the default-accept policy.
- Provide a clean algorithmic summary (pseudocode) of the complete learning procedure.

## Score and Decision

The paper tackles an important and underexplored problem, and the reference extraction idea is genuinely novel. However, the experimental validation is far too limited—small toy datasets with hand-crafted features, no ablation studies, no scalability analysis, and comparisons that unfairly disadvantage offline baselines. These issues make it impossible to assess whether the proposed method would work in realistic settings, which significantly undermines the contribution.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>