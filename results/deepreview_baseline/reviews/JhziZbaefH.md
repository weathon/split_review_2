## Summary

This paper proposes an online multimodal learning (OML) framework with a brain-inspired hierarchical and modular neural network architecture. The key contributions are a reference extraction algorithm that autonomously identifies which features a word refers to, and a human-in-the-loop conflict detection mechanism that allows the network to ask questions when new input contradicts previously learned knowledge. The method is evaluated on image-word association tasks, including color-referring words and modality extension to taste, showing competitive or superior performance compared to both offline and online baselines.

## Strengths

- **Novel problem framing with human-in-the-loop interaction**: The paper tackles an important and underexplored aspect of online multimodal learning—the ability to detect conflicts and interact with users to resolve them. This goes beyond standard continual learning and addresses a key limitation of existing online multimodal methods.
- **Comprehensive experimental design**: The experiments cover multiple challenging scenarios: baseline image-word association, precise referring (color words), modality extension (adding a taste channel), and both close and open environments to test catastrophic forgetting. The inclusion of conflict detection verification (10% incorrect pairs) is a strong validation of the claimed capability.
- **Clear architectural motivation**: The hierarchical design with ascending, descending, and lateral pathways is well-motivated by biological learning principles, and the distinction between order-independent (visual) and order-dependent (auditory) association neurons is a thoughtful design choice.

## Weaknesses

### Major

1. **Insufficient comparison with modern baselines**: The offline baselines (DAE, DBM, DJSRH, NRCH, FUME) are from 2011-2025, but the online baselines (ART, AEN) are from 2019-2025. The paper does not compare against any modern transformer-based multimodal models (e.g., CLIP, ALIGN, or any vision-language model) that could be adapted for online learning. Given that CLIP-like models are the current standard for multimodal representation learning, their absence weakens the claim of effectiveness.

2. **Limited evaluation of the human-in-the-loop component**: The paper claims the network can "ask appropriate questions" and learn from user answers, but the experiments default to positive answers when questions are unanswered. There is no systematic evaluation of different user response patterns (e.g., mixed positive/negative answers, noisy answers), nor any ablation study showing the impact of the interaction mechanism on final performance. The claim that OML "is able to detect all conflicts and raise appropriate questions" is stated but not rigorously quantified in a table or figure.

3. **Unclear scalability and computational cost**: The architecture involves multiple neuron types, complex activation functions with Fourier transforms, and dynamic addition of neurons and connections. There is no discussion of computational complexity, memory usage, or scalability to larger datasets (e.g., ImageNet-scale). The experiments are limited to small, controlled datasets (fruits and home objects), making it unclear whether the method would work at scale.

### Minor

1. **The reference extraction algorithm relies on a heuristic threshold**: The coefficient of variation threshold \( r \) is set to 0.5 without sensitivity analysis. The method's robustness to this hyperparameter is not explored.

2. **Limited ablation studies**: The paper does not ablate key components (e.g., lateral connections, the Fourier transform in MANs, the reference extraction mechanism) to show their individual contributions to performance.

3. **The "open environment" setup is somewhat artificial**: Dividing the dataset into four equal parts with different classes is a reasonable test of catastrophic forgetting, but it does not simulate the truly open-ended, lifelong learning scenario the paper motivates (e.g., learning new objects, colors, and associations over an extended period with no predefined task boundaries).

### Trivial

- The paper uses "OML" both as the method name and the problem name, which can cause minor confusion.

## Nice-to-Haves

- An ablation study showing the contribution of the human-in-the-loop interaction (e.g., comparing OML with and without the question-asking mechanism).
- Sensitivity analysis for the threshold parameters (\(\theta\), \(\vartheta\), \(r\)).
- A discussion of failure cases or limitations of the reference extraction algorithm (e.g., when features are not separable by variance).

## Novel Insights

None beyond the paper's own contributions. The core ideas—hierarchical modular architecture, reference extraction via variance analysis, and conflict-driven human-in-the-loop learning—are novel in the context of online multimodal learning, but the paper does not synthesize a broader insight that transcends its specific method.

## Suggestions

- Add comparisons with modern vision-language models (e.g., CLIP) adapted for online learning, or at least discuss why such comparisons are not feasible.
- Provide a quantitative evaluation of the conflict detection and question-asking mechanism, including precision/recall of conflict detection and the impact of different user response patterns.
- Include an ablation study to isolate the contribution of the reference extraction algorithm, lateral connections, and the Fourier transform in MANs.
- Discuss computational complexity and memory requirements, especially as the network grows with new neurons and connections.

## Score and Decision

The paper addresses a genuinely important and underexplored problem (online multimodal learning with human-in-the-loop interaction) and proposes a novel, biologically-inspired architecture. The experimental results are consistent and show clear advantages over existing online methods. However, the lack of comparison with modern transformer-based baselines, the limited evaluation of the human-in-the-loop component, and the absence of scalability analysis prevent the paper from being a strong accept. The contribution is solid but not transformative.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>