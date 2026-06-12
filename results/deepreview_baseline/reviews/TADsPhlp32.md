## Summary

The paper proposes augmenting the AIDE detector for AI-generated images with structural features derived from a recursive (cuboidal) partitioning of the image. At each partition, the reduction in sum of squared errors is recorded, and the normalized cumulative gains form a 1024-dimensional structural feature vector. These features are concatenated with AIDE’s existing patchwise and semantic features, the entire extractor is frozen, and only the structural module and final MLP head are trained. Experiments on GenImage, AIGCDetect, and Chameleon benchmarks show state-of-the-art mean accuracy on GenImage (89.56%), second-best on AIGCDetect (91.85%), and second-best on Chameleon (58.91%/61.39%).

## Strengths

- **Clear problem motivation:** The paper correctly identifies that existing detectors often miss higher-level structural inconsistencies in generated images, and provides a qualitative example (Fig. 1) that illustrates a case where the addition helps.
- **GenImage state-of-the-art:** The method establishes a new SOTA mean accuracy on the challenging GenImage benchmark, outperforming AIDE by 2.68 points, with consistent gains across several individual generators (ADM, GLIDE, VQDM, Wukong).
- **Well-structured experimental protocol:** Training follows standard procedures (SD-v1.4 for GenImage, ProGAN for AIGCDetect), and results are compared against a wide range of existing detectors using published numbers, ensuring fairness.

## Weaknesses

### Fatal

None.

### Major

1. **Limited novelty and shallow characterization of “structural semantics”:** The core idea is to apply an existing deterministic partitioning algorithm (cuboidal partitioning, Ahmed et al. 2022) to compute a single fixed 1D cumulative-gain curve from RGB pixel statistics, then concatenate it with AIDE features. This is a straightforward feature injection rather than a novel learning framework or a deep treatment of image structure. The claim that these features capture “structural semantic” information (anatomy, physics violations) is not substantiated—the feature is purely a low-level statistical summary of RGB homogeneity.

2. **No end-to-end learnability and limited integration:** The partitioning and gain computation are non-differentiable; only a single FC layer after the fixed features is trainable. This means the structural features are static and cannot adapt to the detection task. In contrast, the other two AIDE branches are also frozen, so the only learned component is a small MLP head. The paper overstates the “trainable structural feature extraction” module.

3. **Performance is not universally superior:** On the more diverse AIGCDetect benchmark, the method is second-best (91.85% vs AIDE’s 93.02%). On the Chameleon dataset, it is also second-best. The paper acknowledges this but attributes it to context-dependence without deeper analysis. The claimed “robustness and generalizability” is weakened by the fact that the improvement is concentrated on specific generators and the overall gain in mean accuracy on GenImage is modest (2.68%).

4. **Lack of theoretical or empirical analysis of the feature:** No ablation studies are provided to show how the number of partitions \(N\), the feature dimension \(M\), or the choice of pixel-level feature (RGB vs. DCT vs. other) affect performance. The method is presented as a black-box addition; there is no insight into *why* the cumulative-gain curve should be discriminative for AI-generated images.

### Minor

- The paper uses the term “structural semantic features” but the feature is computed from RGB pixel values only—no semantics (e.g., object labels, scene graphs) are involved. This could mislead readers about the level of understanding the feature encodes.
- The explanation for performance degradation on some subsets (e.g., CycleGAN, WFIR in AIGCDetect) is plausible but not supported by any diagnostic evidence (e.g., visualizing the structural features of those images).

### Trivial

- Table 1: the “Mean” column for ResNet-50 is missing a value (appears as 72.09 but is not aligned correctly; the column entries are sparse and the mean is not clearly computed). This is a formatting issue but may confuse readers.

## Nice-to-Haves

- Ablation studies over the number of partitions \(N\) and the type of pixel feature (grayscale, RGB, edge maps, DCT coefficients) would clarify what the structural feature actually captures.
- Visualizing the partition boundaries on successfully reclassified images (e.g., the 13 examples in Fig. 3) would strengthen the qualitative argument.
- A discussion of computational overhead compared to the baseline AIDE.

## Novel Insights

None beyond the paper’s own contributions: the paper demonstrates that a simple, handcrafted recursive-partitioning histogram can complement existing hybrid detectors, but it does not provide new theoretical understanding of why AI-generated images exhibit different structural homogeneity patterns, nor does it reveal a previously unknown type of artifact.

## Suggestions

- Rename “structural semantic features” to something more precise, such as “hierarchical homogeneity features” or “recursive partition gain features,” to avoid overclaiming.
- Include an ablation study on the structural feature dimension and the number of partitions to justify the chosen \(N=1024\) and \(M=256\).
- Provide qualitative examples where the structural features *fail* to improve detection, to better characterize the contexts in which they are valuable.

## Score and Decision

Score: 4.5 — The paper addresses a relevant problem and reports a new SOTA on one benchmark, but the contribution is incremental: it attaches a pre-existing, non-learnable feature to a frozen backbone. The limited novelty, lack of in-depth analysis, and modest gains on other benchmarks make this borderline for a top venue.

MY FINAL SCORE: <score>4.5</score>  
MY FINAL DECISION: <decision>Reject</decision>