## Summary
This paper presents AdaSVD, an adaptive SVD-based LLM compression method that introduces two novel components: (1) **adaComp** — an adaptive compensation technique that alternately updates the singular matrices U and V^T after SVD truncation to minimize compression error, using Moore-Penrose pseudoinverse-based least squares and a stack-of-batch strategy for efficient calibration data usage; (2) **adaCR** — an adaptive compression ratio assignment method that allocates layer-specific retention ratios based on each layer's relative importance measured via cosine similarity between inputs and outputs.

The method is evaluated on LLaMA2-7B, OPT-6.7B, Mistral-7B, and Vicuna-7B across language modeling (WikiText-2, PTB, C4) and commonsense reasoning (MMLU, ARC-e, Winogrande, HellaSwag, PIQA) benchmarks at compression ratios from 40% to 80%. Results show consistent perplexity improvements over SVD-LLM (e.g., 50.33 vs 89.90 at 60% compression on WikiText-2) and better average accuracy on reasoning tasks. Ablation studies confirm the individual contributions of adaComp and adaCR. The method is also integrated with GPTQ quantization.

The paper's strengths include a well-motivated problem formulation, technically sound alternating update scheme with pseudoinverse stabilization, and comprehensive ablation analysis. Key weaknesses include lack of statistical significance reporting, an unsupported claim about smartphone/IoT deployment, a potential derivation gap in the V update equation (Eq 13), and insufficient novelty verification due to unavailable external literature search in this run. Overall, AdaSVD presents a meaningful incremental improvement over existing SVD-based LLM compression methods, with the alternating post-truncation compensation being the most distinctive technical contribution.

## Strengths
**1. Well-defined technical problem and motivation.** The paper clearly identifies two concrete limitations of existing SVD-based LLM compression: (a) insufficient compensation for truncation errors in singular matrices, and (b) uniform compression ratios ignoring layer-wise importance. The gap analysis is precise and directly leads to the proposed solutions (adaComp and adaCR).

**2. Technically sound adaptive compensation mechanism (adaComp).** The reformulation of the truncation error minimization as a least-squares problem and the use of Moore-Penrose pseudoinverse to avoid numerical instability is a principled approach. The alternating update scheme for U and V^T is well-motivated and Figure 3 provides convincing convergence evidence. The stack-of-batch strategy for efficient calibration data usage is a practical engineering contribution that addresses a real GPU memory bottleneck.

**3. Comprehensive experimental evaluation.** The paper evaluates on 4 LLM families (LLaMA2-7B, OPT-6.7B, Mistral-7B, Vicuna-7B) across 8 datasets covering both language modeling perplexity and commonsense reasoning accuracy, across a wide range of compression ratios (40%-80%). This is broader than typical SVD compression evaluations. The inclusion of VLM results (LLaVA on COCO captioning) adds generalizability evidence.

**4. Well-designed ablation studies.** Table 3 systematically isolates the contributions of adaComp (with/without), adaCR (adaptive vs. constant), iteration count, and minimum retention ratio. This allows readers to understand each component's impact and identify the overfitting risk at low compression ratios. The iteration ablation (Table 3c) is particularly informative, showing that even 1 iteration often outperforms SVD-LLM.

**5. Integration with weight quantization.** Demonstrating compatibility with GPTQ (Table 4) shows practical applicability and confirms the orthogonality claim. The results show AdaSVD + GPTQ consistently outperforms SVD-LLM + GPTQ, strengthening the case for AdaSVD as a building block in compression pipelines.

**6. Reproducibility-oriented writing.** The paper provides algorithm pseudocode (Algorithm 1), clear implementation details (calibration data size, hardware, framework), and commits to releasing code and models.

## Weaknesses
**W1. Missing statistical significance and variance reporting (Major).** All main results (Tables 1, 3, 4) report single-point estimates without standard deviations, confidence intervals, or multi-seed averaging. This is a significant weakness because: (a) at 40% compression on WikiText-2, the reported perplexity values are 14.76 (AdaSVD) vs 16.11 (SVD-LLM), an 8.5% difference, but without variance the reader cannot assess reliability; (b) the commonsense reasoning average accuracies differ by only 1-3 percentage points (e.g., 42.63% vs 40.69% at 40%), which could easily be within noise range; (c) the calibration data selection (256 random samples from WikiText-2) introduces randomness that should be quantified. **Recommendation**: Report mean ± std over ≥3 independent runs with different calibration subsets. Add statistical significance tests (paired bootstrap or Wilcoxon) for the main AdaSVD vs SVD-LLM comparisons.

**W2. Unsupported deployment claim for smartphones/IoT devices (Major).** Page 5, Section 4.2 states: "These results indicate that AdaSVD is more effective in compressing LLMs for more resource-constrained devices such as smartphones and IoT devices." However, no experiments on actual edge devices, no latency measurements, no peak memory profiling, and no throughput benchmarks are reported. The experiments only measure perplexity and accuracy on GPU-based benchmarks. This overclaim inflates practical significance beyond what the evidence supports. **Recommendation**: Remove the smartphone/IoT claim and replace with a bounded statement about memory reduction ratio. Alternatively, add at least one CPU/mobile inference benchmark showing actual speed or memory improvements.

**W3. Potential derivation gap in V update (Eq. 13) (Major).** The V_k^sigma update in Equation (13) is given as V_k^sigma = ((U_k^sigma)^†)^T W, derived from the objective min ||U_k^sigma V_k^sigma X - W X||_F^2. Full derivation shows that the optimal V_k^sigma should include an X^† term: V_k^sigma = (U_k^sigma)^† W X X^†. The simplified form in Eq. (13) is only valid if X has full row rank (i.e., X X^† = I), which is not stated as an assumption. The paper also has a transpose notation inconsistency (result should be ((U_k^sigma)^† W)^T or similar, depending on dimension conventions). **Recommendation**: Provide the complete derivation in the supplementary material, explicitly state the full row-rank assumption on X, or include the pseudoinverse of X in the update rule. Verify that the implementation matches the correct formula.

**W4. Lack of limitations discussion (Minor).** The conclusion does not discuss any limitations. The paper would benefit from acknowledging: (a) computational overhead of the alternating update (each iteration requires an SVD of A, increasing compression time); (b) sensitivity to calibration data size (only 256 samples from WikiText-2 used; performance on other calibration sources is not explored); (c) residual gap to original model (even at 40% compression, perplexity is 14.76 vs 5.68 for the original LLaMA2-7B); (d) potential overfitting at low compression ratios with many iterations (acknowledged in ablation but not in conclusion). **Recommendation**: Add a dedicated limitations paragraph in Section 5 covering these points.

**W5. Unclear comparison with alternative error compensation strategies (Minor).** The paper claims that "low-rank weight compensation after truncation has been largely overlooked," but does not discuss why simpler compensation strategies (e.g., fine-tuning the truncated matrices on the calibration data via gradient descent, or using SVD with re-factorization after truncation) would be inferior to the proposed Moore-Penrose approach. Figure 3(a) compares "naive update (NU)" vs "MPPU" but does not specify what NU is. **Recommendation**: Clarify what the "naive update" baseline in Figure 3(a) represents. Add a brief discussion of alternative compensation strategies and why the pseudoinverse approach is preferred.

**W6. Novelty verification deferred (Not a paper flaw, but a review limitation).** Due to the Retrieval-Disabled Mode in this run (external paper search unavailable), novelty claims cannot be independently verified against the literature. The paper claims to outperform "state-of-the-art SVD-based methods" but external confirmation of the SOTA status is pending manual literature verification. The residual novelty of adaComp's alternating update scheme relative to other post-training compression techniques (e.g., iterative pruning-and-finetuning, quantization-aware training) would benefit from broader contextualization. **Recommendation**: Authors should add a direct comparison table with recent SVD-based and low-rank compression methods, clearly stating differences in assumptions, calibration requirements, and compression-vs-performance tradeoffs.

## Score
**Final Score: 6/10**

**Rationale**: The final score prioritizes research value and novelty as primary dimensions. AdaSVD presents a meaningful incremental technical contribution (alternating post-truncation update via Moore-Penrose pseudoinverse) with solid empirical evaluation, but the score is constrained by: (a) missing statistical significance reporting that weakens the reliability of comparative claims (W1), (b) unsupported deployment overclaim (W2), (c) a potential derivation gap in Eq. 13 that requires author clarification (W3), and (d) the absence of a limitations section (W4). The core technical idea is sound and the ablation study is well-designed, which supports a score above the midpoint. However, the above weaknesses — particularly the lack of variance reporting and the derivation concern — prevent a higher score without revision. Novelty could not be independently verified due to Retrieval-Disabled Mode in this run, and the verdict is deferred for manual literature checks.

---

### ASCII Diagrams

```text
ASCII Diagram A — Paper Structure & Evidence Map

[Claim: AdaSVD improves SVD-based LLM compression]
    ├── [Subclaim 1: adaComp reduces truncation error]
    │   ├── Evidence: Figure 3 (MSE convergence), Table 3a (PPL w/ vs w/o adaComp)
    │   └── Gap: No comparison with other compensation strategies (finetuning, iterative SVD)
    ├── [Subclaim 2: adaCR improves per-layer compression]
    │   ├── Evidence: Figure 4 (layer importance varies), Table 3b (Adapt vs Const CR)
    │   └── Gap: Cosine similarity as importance measure not validated against alternatives
    └── [Subclaim 3: AdaSVD beats prior SVD methods (SVD-LLM, ASVD, FWSVD)]
        ├── Evidence: Table 1 (PPL on WikiText-2, PTB, C4), Table 2 (across LLMs)
        └── Gap: No variance/statistical significance reported; single-run results
```

```text
ASCII Diagram B — Revision Strategy Roadmap

[W1: No variance reporting]
    → Fix: Add mean±std over ≥3 runs + significance tests
    → Expected: Reliable comparison, increased confidence in claims
[W2: Smartphone/IoT overclaim]
    → Fix: Remove unsupported claim, add bounded memory reduction statement
    → Expected: Claim-evidence alignment, no reviewer pushback
[W3: Eq (13) derivation gap]
    → Fix: Provide full derivation with X^† term, clarify assumptions
    → Expected: Correct update rule, reproducible implementation
[W4: No limitations section]
    → Fix: Add limitations paragraph (overhead, calibration sensitivity, residual gap)
    → Expected: Improved scientific completeness and reviewer perception
```

```text
ASCII Diagram C — Related-Work Taxonomy Tree (Layered)

SVD-based LLM Compression (Root)
├── Branch 1: Pre-truncation compensation
│   ├── Leaf 1.1: Fisher-weighted scaling (FWSVD)
│   ├── Leaf 1.2: Activation-aware diagonal scaling (ASVD)
│   └── Leaf 1.3: Data whitening (SVD-LLM)
├── Branch 2: Post-truncation compensation (AdaSVD contribution)
│   └── Leaf 2.1: Alternating pseudoinverse update (adaComp)
└── Branch 3: Compression ratio strategy
    ├── Leaf 3.1: Uniform compression (FWSVD, ASVD, SVD-LLM)
    └── Leaf 3.2: Layer-adaptive compression (adaCR — AdaSVD contribution)

Note: External literature verification unavailable in this run. This taxonomy reflects
the paper's own positioning relative to cited baselines. Novelty/comparison conclusions
require manual verification against broader literature.
```