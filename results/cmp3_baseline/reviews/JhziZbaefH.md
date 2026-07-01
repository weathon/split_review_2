## Summary
This paper proposes an online multimodal learning (OML) framework inspired by brain architecture, featuring a hierarchical modular network with ascending, descending, and lateral pathways. The method enables continuous learning of new multimodal concepts without catastrophic forgetting, includes a reference extraction algorithm to identify which features a word refers to, and incorporates human-in-the-loop conflict detection and resolution through interactive questioning.

## Strengths
- **Novel problem formulation**: The paper addresses an important and underexplored challenge—online multimodal learning with human-in-the-loop interaction—combining continual learning, multimodal association, and interactive conflict resolution in a single framework.
- **Biologically-inspired architecture**: The hierarchical modular design with distinct neuron types (feature, unimodal association, multimodal association) and multiple pathways (ascending, descending, lateral) is well-motivated and provides a principled approach to multimodal learning.
- **Comprehensive experimental evaluation**: The authors evaluate across multiple datasets (Fruits, HomeF, E-Fruits, E-HomeF, VAT, VAT-HomeF), multiple environments (close/open), multiple tasks (V→A, A→V, T→V, etc.), and compare against both offline and online methods, demonstrating consistent advantages in open environments.

## Weaknesses
### Fatal
None.

### Major
- **Lack of clarity and reproducibility**: The mathematical formulation (Eqs. 1-8) is extremely complex and poorly explained. Key design choices (e.g., why Fourier transforms are used in Eq. 6, how frequency parameters λ are assigned, the exact meaning of "signal" transmission) are not justified. The paper would be very difficult to reproduce without significant additional detail.
- **Limited baseline comparisons**: The online methods compared (ART, AEN) are from 2019-2025 and appear to be relatively obscure. No comparison with modern continual learning methods (e.g., Elastic Weight Consolidation, Progressive Neural Networks, or experience replay approaches) or modern multimodal models (e.g., CLIP-based approaches adapted for online learning) is provided. This makes it difficult to assess the true significance of the results.
- **Unclear conflict detection mechanism**: The conflict detection logic (Section 3.5) is described procedurally but lacks formal analysis. It is unclear how the network determines which question to ask, how it handles ambiguous cases, or what guarantees exist about the correctness of the interaction protocol.

### Minor
- **Limited scale of experiments**: The datasets appear to be small-scale (fruits, home objects) with limited classes. It is unclear how the method would scale to larger, more realistic multimodal datasets.
- **The human-in-the-loop evaluation is weak**: In experiments, unanswered questions default to positive answers, which undermines the claimed interactive capability. No evaluation of the quality or appropriateness of the questions asked is provided.
- **No ablation studies**: The paper does not ablate key components (e.g., reference extraction, lateral connections, conflict detection) to understand their individual contributions to performance.

### Trivial
- The paper uses "OML" both as the method name and the problem name, which can be confusing.

## Nice-to-Haves
- An ablation study isolating the contribution of each component (reference extraction, conflict detection, lateral pathways) would strengthen the paper.
- Evaluation on larger-scale datasets (e.g., MS-COCO, AudioSet) or with more modalities would improve generalizability claims.
- A formal analysis of the convergence properties or capacity of the network would be valuable.

## Novel Insights
The paper's key insight is that online multimodal learning requires not just associative memory but also the ability to detect and resolve conflicts through interaction, and to learn precise feature-level references for words (e.g., distinguishing that "red" refers to color features while "apple" refers to shape+color). The reference extraction algorithm using coefficient of variation to identify stable feature dimensions across examples is a clever and biologically plausible mechanism for word-referent mapping.

## Suggestions
- Provide a clearer, more accessible explanation of the core algorithm, perhaps with pseudocode or a step-by-step example.
- Add comparisons with modern continual learning methods adapted for multimodal settings.
- Include an ablation study to demonstrate the importance of each component.
- Evaluate the quality of the human-in-the-loop interaction (e.g., what fraction of questions are appropriate, how often does the user need to intervene).

## Score and Decision
The paper addresses a genuinely important and novel problem with a well-motivated architecture. However, the lack of clarity in the mathematical formulation, limited baseline comparisons, and absence of ablation studies significantly weaken the contribution. The experimental results are promising but not yet convincing enough for acceptance at a top venue.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>