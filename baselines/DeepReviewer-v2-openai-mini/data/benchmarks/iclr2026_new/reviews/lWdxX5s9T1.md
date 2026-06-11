## Summary
# Final Review Report

## Summary

This paper presents RADAR, a neural framework that augments constructive neural VRP solvers with the ability to handle asymmetric distance matrices. The authors decompose the challenge of encoding asymmetry into two dimensions: *static asymmetry* (directional bias in the input cost matrix) and *dynamic asymmetry* (layer-dependent interaction imbalance in attention). To address static asymmetry, RADAR applies truncated SVD on the distance matrix to produce compact node embeddings that encode inbound/outbound cost structure. For dynamic asymmetry, it replaces standard softmax attention with Sinkhorn normalization to enforce joint row-column awareness in attention scores. The method is evaluated on 17 synthetic asymmetric VRP variants and 3 real-world benchmarks, consistently outperforming prior learning-based methods.

**Core strengths:** (1) The static/dynamic asymmetry decomposition is a useful conceptual contribution. (2) The SVD-based initialization is theoretically principled (via the asymmetry-aware embedding definition) and empirically effective. (3) The evaluation breadth (17+3 benchmarks) and zero-shot generalization tests are commendable. (4) Ablation studies cleanly isolate the contributions of each component.

**Core weaknesses:** (1) The paper omits critical reproducibility details: the decoder architecture, training objective/loss function, and training algorithm are not specified. (2) No measure of variance (standard deviation, confidence intervals, or multi-seed runs) is reported for any experiment, making it impossible to assess statistical significance of the claimed improvements. (3) A mathematical inconsistency exists between Definition 1 (W1,W2 in R^{k×k}) and the construction in Eq. (4) (W1,W2 in R^{2k×k}). (4) The SVD reconstruction quality claims (85%/93%/97%) are presented without defining "matrix information" or reporting variance across instances. (5) Real-world experiments reuse baseline results from prior papers without controlled re-evaluation under identical training protocols.

## Strengths
**S1 — Clear conceptual decomposition of asymmetry.** The paper's primary conceptual contribution is the separation of asymmetry into static (input-level directional cost discrepancies) and dynamic (learned interaction-level imbalances). This decomposition provides a clear framework for thinking about why existing methods struggle with asymmetric VRPs and motivates two complementary technical solutions. Definition 1 (asymmetry-aware embedding) formalizes the static asymmetry problem in terms compatible with the bilinear form used in attention, which is a theoretically sound foundation.

**S2 — SVD-based initialization is principled and effective.** Using truncated SVD to initialize node embeddings from the distance matrix is a well-motivated idea. The construction in Eq. (2)-(5) shows that the concatenated left/right singular vectors (scaled by sqrt of singular values) naturally satisfy the asymmetry-aware property through a simple bilinear projection. The ablation study (Table 6) confirms that SVD initialization alone (without Sinkhorn) reduces the gap from 2.08% to 1.19% on ATSP100, a substantial improvement, and the benefit persists at larger sizes. The theoretical connection to matrix factorization for node embedding is elegant.

**S3 — Extensive and well-designed experimental evaluation.** The paper evaluates on 17 synthetic VRP variants (including single-task ATSP/ACVRP and 16 multi-task variants) plus 3 real-world benchmarks. Training on N=100 and testing on N=200, 500, 1000 without finetuning demonstrates genuine zero-shot generalization. The real-world evaluation covering in-distribution, out-of-distribution (city), and out-of-distribution (cluster) is thorough and practically relevant. The inclusion of both traditional solvers (LKH3, HGS, PyVRP, OR-Tools) and multiple learning-based baselines (MatNet, ICAM, ReLD, ELG, RRNCO, etc.) provides a comprehensive comparison.

**S4 — Clean ablation isolating each component.** Table 6 is a strong ablation: it evaluates all four combinations of SVD (±) and Sinkhorn (±) and shows that each component contributes additive gains. On ATSP100, SVD alone reduces gap from 2.08%→1.19%, Sinkhorn alone reduces to 1.82%, and both together reach 0.72%. On ATSP1000 (extreme OOD), SVD alone achieves 7.24% gap vs 38.64% for the baseline, showing that the SVD initialization has a dramatic effect on generalization. This clean decomposition makes the contributions easily interpretable.

**S5 — Practical motivation and real-world applicability.** The paper addresses a genuine bottleneck in neural VRP deployment: real-world routing problems inherently involve asymmetric costs. By providing a method that works directly from distance matrices (without requiring coordinates), RADAR opens up NCO methods to many practical applications where only pairwise cost tables are available.

## Weaknesses
**W1 — Reproducibility: missing decoder and training details. [Major]**
*Evidence:* Page 1 - Section 4 Methodology. The paper describes the encoder architecture (5 layers, multi-head attention, Sinkhorn normalization) and initialization scheme, but completely omits the decoder architecture, training objective, loss function, and optimization algorithm. The reader cannot determine whether a POMO-style shared decoder, a non-autoregressive decoder, or something else is used. The training algorithm (REINFORCE with rollout baseline? A2C? PPO?) is not specified.
*Impact:* This is a critical omission for a methods paper. Without these details, independent implementation is impossible without reverse-engineering the released code, which undermines the scientific contribution.
*Required action:* Add a "Training and Decoder" subsection specifying: (a) decoder architecture (query construction, compatibility computation, masking), (b) training objective and baseline formulation, (c) optimizer, learning rate schedule, batch size, and number of epochs, (d) handling of cases with no node features (e.g., ATSP).

**W2 — No statistical significance or variance reporting. [Major]**
*Evidence:* Page 1 - Table 1 and all subsequent experimental tables. None of the reported results include standard deviation, confidence intervals, or multi-seed training. On ATSP100, RADAR achieves 0.72% gap vs ReLD's 1.64% — a difference of approximately 1% of the objective, which could easily lie within training noise if multi-seed variance is high.
*Impact:* The central claim that RADAR "consistently outperforms" baselines is not statistically substantiated. Without variance information, readers cannot assess whether the reported margins are robust or artifacts of a single training run.
*Required action:* Report mean ± std over at least 3 training seeds for all neural methods in the main tables. Add a paired significance test (e.g., Wilcoxon signed-rank) comparing RADAR against the strongest baseline on each task. If resource constraints prevent full multi-seed retraining of all baselines, at minimum report RADAR's own multi-seed variance.

**W3 — Mathematical inconsistency in Definition 1. [Major]**
*Evidence:* Page 1 - Lines 37-39 and Lines 45-48. Definition 1 states: X ∈ R^{n×k}, W1, W2 ∈ R^{k×k} with ||XW1(XW2)^T - D||_F^2 ≈ 0. However, the constructive proof uses X ∈ R^{n×2k} (concatenated left/right components from Eq. 3) and W1=[I_k|0]^T ∈ R^{2k×k}, W2=[0|I_k]^T ∈ R^{2k×k}. The dimensions of W1, W2 in the definition (k×k) do not match the construction (2k×k). Additionally, the target "≈ 0" is not formally bounded.
*Impact:* The core theoretical definition of the paper's first contribution is mathematically imprecise. This inconsistency will be flagged by mathematically-oriented reviewers and undermines the rigor of the theoretical framing.
*Required action:* (a) Correct Definition 1 to either state W1, W2 ∈ R^{m×k} where m is the embedding dimension, or change the definition to use X ∈ R^{n×2k} directly. (b) Replace "≈ 0" with a precise bound involving the best rank-k approximation error.

**W4 — SVD reconstruction quality claims lack rigor. [Major]**
*Evidence:* Page 1 - Line 49. "The top 10 singular values could capture around 85% of the matrix information, while 20 and 30 singular values improves the retention to about 93% and 97%, respectively." The term "matrix information" is undefined, no variance across instances is reported, and the connection between 85% reconstruction and downstream generalization is not explained.
*Impact:* The choice of truncation rank k=10 is a critical hyperparameter that controls the capacity of the node embeddings. Without rigorous evidence linking reconstruction fidelity to task performance, this choice appears heuristic.
*Required action:* (a) Define "information retention" as the cumulative energy ratio (normalized sum of squared singular values). (b) Report mean ± std across test instances. (c) Provide a brief theoretical justification for why moderate truncation aids generalization. (d) Include the k-sensitivity analysis from Appendix D.3 in the main text.

**W5 — Real-world comparison fairness concerns. [Major]**
*Evidence:* Page 1 - Section 5.3. The real-world experiments reuse GCN and MatNet results "reported in their paper" (RRNCO). RADAR was trained with Min-Max normalization, but it is unclear whether GCN/MatNet used the same normalization, training protocol, and data splits in their original paper.
*Impact:* Cross-paper comparisons conflate algorithmic improvements with differences in training setup. The claimed advantages on real-world datasets may partially reflect different training protocols rather than RADAR's design.
*Required action:* Re-evaluate all baselines under the identical training setup (same optimizer, epochs, normalization, augmentation, seeds). If not feasible, add an explicit caveat: "Results for GCN and MatNet are taken from [Son et al., 2026] without re-running; training setups may differ."

**W6 — Missing runtime parity information for baselines. [Minor]**
*Evidence:* Page 1 - Section 5.1. The training time of RADAR is reported (39.31h for ATSP, 54.74h for ACVRP), but no training times are reported for MatNet, ICAM, ReLD, ELG, etc. Inference times in Table 1 show RADAR is comparable or slightly slower (0.04m vs 0.03m for MatNet on ATSP100), but the inference time differences are small in absolute terms.
*Impact:* Readers cannot assess the computational overhead of SVD + Sinkhorn relative to baseline methods for training.
*Required action:* Add a table comparing training GPU-hours and inference FLOPS across all neural methods under the same hardware.

**W7 — Sinkhorn normalization analysis is incomplete. [Minor]**
*Evidence:* Page 1 - Algorithm 2 and Section 4.2. The paper proposes Sinkhorn normalization for attention but does not discuss: (a) the difference between doubly stochastic (Sinkhorn) and row-stochastic (softmax) attention and why this matters for asymmetry, (b) gradient stability through Sinkhorn iterations, (c) how the number of iterations T affects convergence and attention sparsity.
*Impact:* As one of two core technical contributions, the Sinkhorn component is under-analyzed. Reviewers may question whether the benefit comes from the doubly stochastic constraint specifically or simply from added nonlinearity.
*Required action:* Add a paragraph explaining the mathematical distinction between softmax and Sinkhorn normalization in the context of attention, gradient flow considerations, and empirical convergence of the iterative process with varying T.

## Score
**Final Score: 6/10**

**Rationale:** The paper presents a conceptually clean and practically motivated approach (SVD-based embeddings + Sinkhorn attention) for a genuine problem in neural VRP. The strengths include a well-decomposed problem framing, extensive evaluation across 17+3 benchmarks, and clear ablation isolating each component's contribution. However, several major weaknesses prevent a higher score:

- **Reproducibility gap (W1):** The paper omits training objective, decoder architecture, and optimization details, making independent re-implementation impossible without code reverse-engineering. For a methods paper, this is a significant deficiency.
- **No statistical rigor (W2):** Without variance reporting or multi-seed experiments across any of the 14+ tables, the core claim of "consistent outperformance" is not statistically verified. The margins (e.g., 0.72% vs 1.64% on ATSP100) could be within training noise.
- **Mathematical imprecision (W3):** The dimensional inconsistency in Definition 1 weakens the theoretical foundation of the first contribution.
- **Comparison fairness on real-world data (W5):** Reusing baseline numbers from prior papers without controlled re-evaluation introduces potential confounds.
- **Novelty verification deferred:** Due to Retrieval-Disabled Mode, external literature comparison was not possible in this run. The conceptual contributions (SVD-based embedding + Sinkhorn attention for asymmetric VRPs) appear incrementally novel relative to the methods cited in the paper (MatNet, ICAM, ReLD, RRNCO), but a definitive novelty assessment requires manual literature verification.

The paper is technically sound and the experiments are broad, but the reproducibility and statistical rigor issues are significant. With careful revisions addressing W1-W5, the paper could reach 7-8/10.

**Novelty and research value note:** The research value is moderate-to-high: asymmetric VRP is an underexplored yet practically important setting. The static/dynamic asymmetry decomposition provides a useful conceptual framework. However, since external retrieval was unavailable in this run, all novelty claims above rely on the in-paper comparison with cited prior work and should be treated as provisional pending manual literature verification.