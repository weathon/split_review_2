## Summary
This paper introduces GMD-25, a benchmark for evaluating compositional generalization in Machine Learning Force Fields (MLFFs). It defines four tasks—length extrapolation, functional group composition, functional group duplication, and functional group combination—where training and test molecules share underlying components but are structurally distinct. Evaluation of five representative MLFFs (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2) reveals that all models suffer significant OOD performance degradation, often 1–2 orders of magnitude worse than ID performance.

## Strengths
- **Well-motivated benchmark design.** Each of the four tasks probes a specific, clearly articulated aspect of compositional generalization (length generalization, systematic composition, motif duplication, asymmetric recombination). The training-test splits are carefully constructed so that models *should* be able to generalize if they capture the right physical principles—a sharp and useful contrast with standard benchmarks that only test interpolation.
- **Comprehensive and diverse model evaluation.** The paper evaluates five models spanning invariant GNNs (SchNet), equivariant message-passing (PAINN), geometric-angle models (DimeNet++, GemNet), and equivariant transformers (EquiFormerV2), giving a broad cross-section of the field. The finding that the best-ID model is not always the best-OOD model (e.g., EquiFormerV2 for forces vs. SchNet/DimeNet++ for energy in length extrapolation) is a genuinely useful insight.
- **Clear presentation and reproducibility infrastructure.** The paper is well-organized with informative figures, and the authors commit to releasing the dataset, toolkit, and training framework. The workflow (initial geometry → FlashMD → GFN2-xTB recalculation) is described clearly enough to be reproducible.
- **Useful augmented task variants.** The base and augmented variants provide a nuanced view: e.g., for length extrapolation, the augmented variant demonstrates that seeing all chain lengths during training (with different functional groups) helps energy prediction but not forces, revealing an interesting asymmetry.

## Weaknesses
### Fatal
None.

### Major
- **Lack of diagnostic depth beyond error reporting.** The paper's analysis stops at "models fail" with error magnitudes. There is no investigation into *why* models fail—for example, analyzing attention patterns, learned representations, per-atom error breakdowns, or sensitivity to specific molecular features. This limits the paper's value as a tool for driving model improvements. A benchmark that only diagnoses failure without offering explanatory insight risks being a speedbump rather than a signpost.
- **No exploration of potential mitigations.** The paper does not experiment with any interventions (e.g., data augmentation strategies, regularization, architectural modifications) to understand what might improve compositional generalization. Even a negative result on a simple baseline intervention would significantly strengthen the contribution by moving from "here's a problem" toward "here's what we know about the problem."
- **Semi-empirical labels (GFN2-xTB) may limit practical relevance.** While GFN2-xTB is computationally efficient, its accuracy is notably lower than DFT for many chemical properties. The generalization gaps observed might partly reflect the noisiness or systematic biases of the labels themselves rather than (or in addition to) architectural limitations. Without at least a small-scale DFT validation or a discussion of how label quality affects the observed generalization gaps, the external validity of the findings is uncertain.

### Minor
- **Relatively small and narrow molecular domain.** The benchmark contains 118 molecules from linear alkyl chains with a few functional groups. While this is adequate for the controlled evaluation goal, it raises questions about how findings generalize to more diverse chemical spaces (branched chains, ring systems, heteroatom-heavy molecules). The paper could acknowledge this limitation more explicitly.
- **The augmented variants' framing is somewhat confusing.** They are described as potentially "easier" due to broader training coverage, yet the results do not uniformly show improvement. The naming and motivation could be sharpened—for instance, explicitly defining what hypothesis each augmented variant tests.
- **Foundation model exclusion limits practical conclusions.** The justification for excluding pre-trained foundation models is understandable but means the benchmark misses the most practically relevant comparison point for current MLFF deployment. A brief discussion of how pre-training might interact with the compositional generalization tasks would be valuable.

### Trivial
None.

## Nice-to-Haves
- A brief error analysis for a representative task (e.g., per-atom energy decomposition in the duplication task) to provide mechanistic insight into failure modes.
- Results on at least one DFT-level dataset (even a subset) to validate that the generalization gaps persist at higher label fidelity.
- Comparison with a simple data augmentation baseline (e.g., random molecular fragments) to establish whether the generalization gap is reducible with more training data of the right kind.

## Novel Insights
Beyond the paper's own contributions, a notable observation emerges from the pattern of results: the architectural features that best support ID accuracy (e.g., EquiFormerV2's equivariant transformer design) do not straightforwardly translate to compositional generalization, and in some cases simpler invariant models (SchNet) show more stable behavior OOD. This suggests a possible tension between expressiveness for interpolation and robustness for extrapolation—a finding that connects to the broader algorithmic alignment literature cited in the paper, and which the authors could have highlighted more forcefully.

## Suggestions
- Add a diagnostic section investigating *what* models fail to learn: e.g., do they fail to capture long-range interactions in the length task? Do they fail to decompose functional group contributions in the composition task?
- Include at least one mitigation experiment (even a simple one) to move beyond diagnosis toward actionable guidance.
- Validate key findings on a small DFT subset to increase confidence that the generalization gaps are not artifacts of GFN2-xTB.
- Strengthen the discussion of the augmented variants by being more precise about what each one tests and why the results do or don't match expectations.

## Score and Decision
The benchmark fills a genuine and well-articulated gap in MLFF evaluation, the task designs are thoughtful, and the empirical findings are clear and reproducible. However, the paper remains at the diagnostic level—it reveals that models fail at compositional generalization but provides limited insight into why or how to fix it. As a benchmark paper, the contribution is solid and useful for the community, but the shallow analytical depth and lack of mitigation experiments prevent it from being a strong contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: Accept