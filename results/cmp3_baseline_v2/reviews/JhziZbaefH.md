## Summary

This paper proposes OML, a brain-inspired hierarchical modular neural network for online multimodal learning with human-in-the-loop. The network uses ascending, descending, and lateral pathways across feature, unimodal association, and multimodal association layers. It includes a reference extraction algorithm to determine which features a word refers to, conflict detection between current and previously learned knowledge, and the ability to ask the user questions when conflicts arise. Experiments on small fruit/home object datasets with vision and audition (plus taste extension) show competitive accuracy against online and some offline methods, particularly in open-environment (continual learning) settings.

## Strengths

- **Addresses a relevant and underexplored problem**: Online multimodal learning with interactive conflict resolution and human-in-the-loop is an important direction that goes beyond standard static multimodal models.
- **Novel architectural components**: The combination of a hierarchical structure with ascending/descending/lateral pathways, reference extraction, and conflict-driven questioning is arguably novel in the online multimodal learning literature.
- **Experiments cover multiple scenarios**: The evaluation includes baseline comparisons, precise referring, modality extension, and both close/open environments, providing a broad view of the method's behavior.

## Weaknesses

### Major

1. **Severe clarity and reproducibility issues**: The model description is extremely dense, notation-heavy, and lacks intuitive explanation. Key equations are poorly motivated (e.g., the cosine-frequency activation in Eq. 1, Fourier transforms in MANs). The learning algorithm is not described as a coherent procedure—it reads like a collection of conditionals. A reader would have great difficulty reimplementing the method or understanding why the design choices are necessary.

2. **Weak experimental evaluation**:
   - Only two very small datasets (Fruits, HomeF) are used, with accuracy metrics in a narrow range (80–92%). No standard large-scale benchmarks (e.g., MS-COCO, Flickr30K, AudioSet) are tested.
   - No error bars, confidence intervals, or statistical significance tests are reported. It is impossible to assess whether differences between methods are reliable.
   - The human-in-the-loop interaction is simulated by automatically answering "yes" if no response arrives, effectively bypassing the claimed core contribution. Real human studies or at least a more realistic simulation are absent.
   - Offline methods are reported with *decreased* accuracy in the open environment (expected), but the paper does not analyze whether these methods were given the same amount of data sequentially or trained from scratch on each split. The comparison is therefore potentially unfair.

3. **Questionable evaluation of the "precise referring" capability**: The paper states that for competing methods (ART, AEN) it *counts as correct* when they return all features (shape+color) for a color word. This is a generous reinterpretation that artificially inflates their scores and undermines the claimed advantage. A proper evaluation would measure whether the model retrieves the correct *attribute* (color only), not just any match.

4. **Limited justification of design choices**: The paper introduces many parameters (thresholds, frequency assignments, Fourier transforms, lateral connection criteria) without ablation studies or sensitivity analysis. It is unclear which components are essential and how robust the method is to parameter variation.

### Minor

- The related work section is brief and does not deeply explore prior online learning methods (e.g., expanding networks, continual learning, lifelong learning) beyond a few references.
- The model's scalability to more modalities, larger vocabularies, or real-world noise is not discussed.
- The "brain-inspired" claim is superficial; the architecture has little demonstrated connection to neuroscience beyond pathway naming.

### Trivial

- Figure captions are redundant and overly long.
- Some sentences are awkward or contain minor inconsistencies (e.g., "OML" is used both as the method name and an abbreviation for Online Multimodal Learning).

## Nice-to-Haves

- Add ablation experiments to isolate the contribution of each architectural component (e.g., reference extraction, lateral connections, conflict detection).
- Run experiments on standard large-scale multimodal datasets to demonstrate scalability.
- Include a real human-in-the-loop user study or a more principled simulation with randomized teacher answers.

## Novel Insights

None beyond the paper's own contributions — the architecture itself is the primary contribution, and no deeper theoretical insight (e.g., convergence guarantees, memory bounds, or biological plausibility) emerges from the analysis.

## Suggestions

- Rewrite the method section to be more accessible: start with a clear algorithmic pseudocode, reduce notational clutter, and add high-level intuition for why each mechanism (e.g., frequency-based signal, Fourier transform) is needed.
- Perform ablation studies to show the impact of conflict detection, reference extraction, and lateral connections on final accuracy.
- Report all results with confidence intervals or error bars (e.g., over multiple runs).
- Evaluate on a larger, publicly available multimodal dataset (e.g., Conceptual Captions + AudioSet) to establish generalizability.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>