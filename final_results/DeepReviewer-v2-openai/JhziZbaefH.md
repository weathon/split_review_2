## Summary
This paper tackles the problem of online multimodal learning (OML), where a model must continuously acquire new cross-modal concepts and associations from streaming data without catastrophic forgetting. The authors propose a brain-inspired hierarchical neural architecture with three neuron types (Feature Neurons, Unimodal Association Neurons, Multimodal Association Neurons) connected through ascending, descending, and lateral pathways. The architecture supports dynamic structural expansion for new concepts, a reference extraction mechanism that identifies which visual features a word refers to (e.g., color vs. shape), and conflict-driven human-in-the-loop interaction where the system asks questions when new input contradicts prior knowledge. Experiments on small-scale fruit-object datasets (Fruits, HomeF) and their augmented variants show that OML achieves 83–90% cross-modal retrieval accuracy, outperforming prior online methods (ART, AEN) by 2–5 points while maintaining stable performance under class-incremental shifts.

**Overall assessment**: The paper addresses an important and under-explored problem (online multimodal learning with human interaction) and introduces a structurally novel architecture. However, several major weaknesses limit its current impact: the experiments are conducted on small custom datasets without statistical significance measures, the conflict detection and human-in-the-loop claims are not rigorously evaluated, the mathematical formulation contains dimensional inconsistencies, and the comparison baseline setup has protocol asymmetries that complicate interpretation. The core ideas are promising but require substantially stronger empirical validation, clearer formalism, and more careful claim bounding before the contributions can be fully accepted.

## Strengths
1. **Important problem formulation**: The paper targets a genuinely underexplored problem—online multimodal learning with conflict-driven human interaction. The combination of continual concept acquisition, cross-modal grounding, and interactive disambiguation is well-motivated and relevant for lifelong learning agents operating in open environments.

2. **Novel architectural design**: The hierarchical three-layer architecture (FN → UAN → MAN) with ascending/descending/lateral pathways provides a structurally novel framework for cross-modal interaction. The separation of order-independent (visual) and order-dependent (auditory) activation modes is a thoughtful design choice that respects the different temporal characteristics of visual vs. linguistic processing.

3. **Reference extraction mechanism**: The use of variance-based feature attribution (coefficient of variation) to determine which visual features a word refers to is an elegant and computationally lightweight approach. The idea that color features will show lower variance than shape features across instances of the same color is intuitive, and the experiments (Table 2) provide initial support for this method working on color-referring words.

4. **Conflict detection and interaction**: The four-case recognition framework (Section 3.5) provides a systematic treatment of different learning scenarios based on whether each channel recognizes the input. The natural-language question templates, while simple, demonstrate a concrete mechanism for human-in-the-loop learning that goes beyond standard supervised learning paradigms.

5. **Modality extension capability**: The experiment extending a trained visual-auditory network with a taste channel (Table 3) demonstrates a practically useful capability—model reuse through structural expansion. This goes beyond most continual learning works that focus on class-incremental learning within a fixed modality.

## Weaknesses
### W1. Limited empirical validation and missing statistical rigor (Major)
**Evidence**: Tables 1-3 report accuracy as point estimates without standard deviations, confidence intervals, or significance tests. The paper states no variance measures across the 12 experimental conditions.

**Impact**: Without variance information, readers cannot assess whether observed differences (e.g., OML 89.2% vs. offline methods 92.3% on Fruits Close) are meaningful. The 2-5 point improvements of OML over other online methods may fall within noise range. This is a critical reproducibility and scientific validity concern.

**Required action**: Report mean ± std over ≥3 random seeds for all conditions. Add paired significance tests (e.g., bootstrap or t-test) between OML and the strongest baseline in each setting.

### W2. Dataset scale and generalizability concerns (Major)
**Evidence**: The two base datasets (Fruits, HomeF) contain only fruit images from small vocabularies (~dozens of classes, based on prior work). The features are hand-crafted (Fourier descriptors + mean color + MFCCs), not learned representations. Dataset statistics (class count, sample count, vocabulary size) are not reported.

**Impact**: Claims about "online multimodal learning" require demonstration on larger, more diverse concept vocabularies. The current evidence does not support scaling claims. The use of custom non-standard datasets prevents direct comparison with broader multimodal retrieval benchmarks.

**Required action**: Report exact dataset statistics (classes, samples/class, vocabulary). Evaluate on at least one standard multimodal benchmark (e.g., Flickr30k, MSCOCO) adapted for online/incremental learning. Test with learned visual features (e.g., CLIP, ResNet) as an alternative to Fourier descriptors.

### W3. Human-in-the-loop claim not properly evaluated (Major)
**Evidence**: (a) The paper states "if the question posed to the user remains unanswered for a certain period of time, we set the answer to be positive." (b) Conflict detection is claimed to work with "10% of word-image or word-taste data pairs with incorrect matches," but no precision/recall metrics are reported. (c) No user study or human evaluation protocol is conducted.

**Impact**: The core interactive contribution is effectively untested. The automatic positive-default policy means the system never experiences negative feedback, making it impossible to assess whether the interaction mechanism provides any benefit over passive acceptance. The quality of generated questions is not evaluated.

**Required action**: (i) Report conflict detection precision, recall, and F1 on a held-out test set. (ii) Compare three interaction policies: always-accept, always-reject, and ground-truth-based answers. (iii) Conduct a small user study (or simulation with held-out answers) to measure the impact of human feedback on learning accuracy.

### W4. Mathematical inconsistency in Eq. (1) (Major)
**Evidence**: The ascending activation function in Eq. (1) produces a scalar output $y^{\alpha_k}$, but Eq. (3) treats $\mathbf{y}^{\alpha_k}$ as a vector that is summed across feature types. The temporal summation $\sum_{t=1}^T$ with parameter $T$ that "does not affect the algorithm" is present but unexplained, making it unclear whether the output depends on $T$.

**Impact**: The dimensional mismatch between scalar and vector signal representations creates ambiguity for reproducibility. Readers implementing from the description may produce incorrect architectures.

**Required action**: Clarify whether $y^{\alpha_k}$ is a scalar per neuron or a vector per feature type. If scalar, revise Eq. (3) accordingly. If vector, specify the mapping. Remove the temporal summation or explain its purpose; if $T$ does not affect the algorithm, simplify the formulation.

### W5. Related work lacks structured comparison and misses key literature (Major)
**Evidence**: The related work section is a citation-dense list (13 papers in one paragraph) organized only by broad category (joint vs. coordinated representation). It does not engage with the continual learning literature (e.g., EWC, SI, GEM, MAS, rehearsal methods) that addresses the "catastrophic forgetting" problem central to the paper's motivation. Modern multimodal models (CLIP, ALIGN) are not discussed.

**Impact**: Readers cannot assess how OML compares to established continual learning techniques or understand why those techniques cannot be directly applied to multimodal settings. The novelty positioning is weaker as a result.

**Required action**: Add a dedicated paragraph on continual learning methods, explaining why they are insufficient for multimodal online learning. Discuss the relationship to modern multimodal foundation models. Restructure the section around decision-relevant comparison axes (e.g., online capability, reference grounding, conflict detection, human interaction).

### W6. Reference extraction threshold sensitivity unexamined (Major)
**Evidence**: The reference extraction method uses a hard threshold $\tau$ (called $r$ in the paper, creating notation conflict with the coefficient-of-variation variable) set to 0.5. No sensitivity analysis is provided. The coefficient of variation $r = \sigma \oslash \mu$ risks division by zero when $\mu$ has near-zero entries.

**Impact**: The method's robustness to threshold choice is unknown. If performance varies significantly with threshold, the practical utility decreases. The division-by-zero issue means the method could fail silently on certain feature dimensions.

**Required action**: Report reference extraction accuracy across threshold values {0.2, 0.35, 0.5, 0.65, 0.8}. Add $\epsilon$ to the denominator: $\mathbf{cv} = \sigma \oslash (\mu + \epsilon)$. Test on additional attribute types (texture, material, size) beyond color.

### W7. Unfair comparison baseline protocol (Moderate)
**Evidence**: Offline methods (DAE, DBM, DJSRH, NRCH, FUME) are "iteratively optimized multiple times on the dataset," while online methods (ART, AEN, OML) learn "each sample only once." In the open environment, offline methods are tested without any continual learning techniques (rehearsal, regularization).

**Impact**: The large accuracy drops for offline methods in open environments (e.g., DAE: 67.0→52.3 on Fruits V→A) may partly reflect the absence of basic continual learning mitigations rather than inherent superiority of the OML architecture. A fairer comparison would equip offline methods with rehearsal buffers or regularization.

**Required action**: Add two additional baselines: (i) best offline method + replay buffer, (ii) best offline method + elastic weight consolidation (EWC), to provide a more meaningful comparison of online learning capability.

### W8. Conclusion lacks limitations discussion (Minor)
**Evidence**: The conclusion (Section 5) contains no discussion of limitations, failure cases, or future work directions. It repeats the abstract's claims without critical reflection.

**Impact**: This weakens scientific credibility and gives readers an incomplete picture of the method's boundaries.

**Required action**: Add a limitations paragraph covering dataset scale, feature engineering dependency, threshold sensitivity, interaction protocol limitations, and directions for improvement.

## Score
**Final Score: 5/10**

**Rationale**: The paper targets an important and under-explored problem (online multimodal learning with human-in-the-loop interaction) and proposes a structurally novel architecture with appealing design features (hierarchical pathways, frequency-based signaling, variance-driven reference extraction). However, the current evaluation has significant limitations that prevent higher confidence in the claimed contributions: (1) experiments lack statistical rigor (no variance measures, no significance tests across all conditions), (2) the human-in-the-loop component is not properly evaluated (automatic positive-default answer, no precision/recall for conflict detection), (3) datasets are small-scale with unclear statistics, making generalization claims unsupported, (4) the mathematical formulation in Eq. (1) contains dimensional inconsistencies that affect reproducibility, (5) comparison protocols are asymmetric (offline methods without continual learning mitigations), and (6) novelty verification is deferred due to external literature being unavailable this run. The core ideas have merit and the architecture has several novel design elements, but substantially stronger empirical evidence, clearer formalism, and bounded claims are needed before the work meets the bar for publication.

The score prioritizes research value (the problem is important) and novelty (the architecture is structurally new) as primary dimensions, but is tempered by the insufficient empirical support and unresolved methodological concerns. With major revisions addressing the weaknesses outlined above, the paper could potentially reach 6-7/10.