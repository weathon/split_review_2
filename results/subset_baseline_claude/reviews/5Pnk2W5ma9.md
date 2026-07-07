## Summary

The paper introduces ONNX-Bench, a unified dataset of ~650k (architecture, accuracy) pairs drawn from six NAS benchmarks (NAS-Bench-101/201/301, NATS-Bench, hNAS-Bench-201, einspace) stored in a common ONNX format and evaluated on CIFAR-10. Building on this, the authors propose ONNX-Net, a text-based architecture encoding that converts ONNX computation graphs into natural language strings and fine-tunes an encoder LLM (ModernBERT) for cross-space performance prediction. The central claim is that this representation is search-space-agnostic, captures operator-level parameters (unlike graph encodings), and enables competitive zero-shot transfer.

---

## Strengths

- **Genuinely useful community resource.** ONNX-Bench consolidates six diverse NAS benchmarks—spanning cell-based, hierarchical, and grammar-based search spaces—into one consistent format with 649k entries. The diversity analysis (JSD metrics in Fig. 2) concretely characterizes distributional differences between spaces, providing a principled foundation for cross-space NAS research.

- **Well-motivated encoding choice.** The paper's argument that graph-bundle encodings are blind to operator hyperparameters (e.g., identical topology but different kernel sizes) is compelling and concretely illustrated. The ONNX-to-text encoding that includes operation name, input shapes, parameter values, and output shapes directly addresses this gap with a concrete ablation (Table 6) confirming that "+Inputs" and "+Parameters" components both contribute.

- **Competitive performance with low data.** In the zero-shot NB101→NB201 benchmark (Table 3, Fig. 5), ONNX-Net achieves ρ=0.747, outperforming all FLAN variants (including FLAN+Arch2Vec at 0.741, FLAN+ZCP at 0.646, CAZ at 0.685) across all training set sizes, and does so with lower variance. The low-data regime advantage (200 training samples) is especially noteworthy.

- **Cross-dataset generalization experiment.** The UnseenNAS evaluation (Table 5) tests a genuinely harder problem—predicting architecture rankings on unseen tasks—and reveals that including the einspace data is critical, showing the benchmark's value for coverage.

---

## Weaknesses

### Fatal
None.

### Major

- **Gap versus GENNAPE not adequately addressed.** GENNAPE achieves ρ=0.815 while ONNX-Net reaches ρ=0.747 on the primary benchmark (NB101→NB201). The paper attributes this to GENNAPE using an ensemble of two pairwise classifiers, but does not explore whether ensembling or a ranking loss would close the gap. Given that cross-space generality is the paper's central claim, the inability to match the performance of an ensemble method on even the simplest transfer task (NB101→NB201, JSD only 0.23) leaves the headline claim partially unsupported.

- **Weak transfer across highly distinct spaces.** Table 4 shows that transferring between einspace and NAS-Bench-101/201 yields very low Spearman correlations (0.155–0.351), which the authors explain by the high JSD (0.61). However, this outcome reveals that the text encoding does not provide the general cross-space generalization the paper claims—it works well when spaces are similar but fails when they are structurally diverse. This is the most challenging regime for any claimed "universal" predictor, and no solution is proposed.

### Minor

- **CIFAR-10 only.** The benchmark is restricted to CIFAR-10 accuracy labels. The discussion acknowledges this but it means the benchmark cannot currently be used to study multi-task or dataset-conditioned surrogate models. The cross-dataset experiment in Section 5.3 only tests architectures from einspace trained on CIFAR-10 and transferred to UnseenNAS tasks—a different kind of generalization than what would come from diverse training datasets.

- **Negative transfer is unexplained.** Table 2 shows that leaving out hNAS-Bench-201 improves transfer to it (0.533 → 0.565). This is a meaningful finding about negative transfer but receives only two sentences of commentary without analysis of why it occurs, which limits its utility for practitioners selecting data mixtures.

### Trivial

- The diagram in Figure 4 is slightly inconsistent with the description (it shows the Computational Graph feeding into the LLM directly, but Section 4 only describes the text path being used for the predictor).

---

## Nice-to-Haves

- Exploring ranking losses (e.g., ListMLE or pairwise losses) in place of MSE to check whether the gap with GENNAPE's pairwise classifier approach is recoverable.
- An analysis of text sequence length vs. prediction quality, since context length is identified as a bottleneck but no empirical characterization is given.
- Investigation of whether a small amount of in-domain fine-tuning (few-shot rather than zero-shot) closes the gap for the high-JSD transfer cases.

---

## Novel Insights

The paper's most novel observation is that including diverse search spaces in pretraining (particularly einspace, the most structurally distinct) critically improves zero-shot transfer to new datasets (Table 5), but simultaneously the encoding struggles precisely in regimes of high inter-space divergence (Table 4). This suggests a fundamental tension: diversity in pretraining is necessary for generalization but insufficient when test-time architectures are drawn from a substantially different structural distribution—a finding that motivates future work on structural domain adaptation for architecture representations.

---

## Suggestions

- Provide a direct ablation comparing ONNX-Net with and without an ensemble pairwise classifier to isolate whether GENNAPE's advantage is architectural or stems purely from the ensemble strategy.
- Add a short quantitative analysis of token sequence length distributions across search spaces, and report whether truncation during fine-tuning was ever triggered for large einspace graphs (node counts up to 3503).
- Consider reporting in-domain (within-space) performance alongside zero-shot numbers to give a clearer picture of the surrogate's ceiling when target data is available.

---

## Score and Decision

ONNX-Bench is a valuable, openly released dataset unifying six NAS benchmarks that will serve the community regardless of the predictor results. ONNX-Net provides a principled text encoding that outperforms competitive baselines in the low-data regime. The major weaknesses (gap vs. GENNAPE, weak transfer at high JSD) are real but not paper-invalidating—the authors acknowledge them honestly and the work represents a meaningful step toward search-space-agnostic NAS. The contribution is primarily a benchmark + encoding paper rather than a performance-record paper, and should be judged as such.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>