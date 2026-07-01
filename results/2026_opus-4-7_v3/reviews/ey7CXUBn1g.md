Now let me read the rest of the paper to check for Table 2 and any additional sections:Now I have thoroughly read the paper. Let me draft the review before calibration.Now let me proceed with calibration Round 1 — bracketing:Let me read the most relevant anchors to calibrate:Now let me read the AutoTrunc paper more closely (it's the most directly comparable anchor):Now I have sufficient calibration data. Let me compose the final review.

---

## Summary
AdaSVD proposes two enhancements for SVD-based LLM compression: (1) **adaComp**, which compensates for SVD truncation error by alternately updating the U and V^T factors using pseudoinverse-based least squares, and (2) **adaCR**, which assigns layer-specific compression ratios based on cosine similarity between layer inputs and outputs. The method consistently improves over SVD-LLM on 7B-scale models across compression ratios from 40% to 80%.

## Strengths
- **Clean mathematical reformulation of the SVD truncation error objective (Eqs. 4–13)**: The paper correctly identifies that standard SVD minimizes weight-space Frobenius norm rather than activation-space output error. The use of the Moore-Penrose pseudoinverse to stabilize updates is concretely demonstrated in Figure 3(a), where naive inversion oscillates while pseudoinverse converges monotonically. This is a sound and well-motivated derivation.

- **Consistent improvements across all tested compression ratios on the primary benchmark (Table 1)**: On WikiText-2 for LLaMA2-7B, AdaSVD outperforms SVD-LLM at every ratio from 40% to 60%, with relative PPL improvements of 8% (40%), 6% (50%), and 44% (60%). The common-sense reasoning results also show consistent accuracy gains (e.g., average accuracy 42.63% vs. 40.69% at 40%).

- **Thorough ablation study (Table 3)**: Four sub-tables systematically examine adaComp, adaCR, iteration count, and minimum retention ratio, providing good transparency about each component's contribution and limitations.

- **Orthogonality with quantization (Table 4)**: The integration with GPTQ shows AdaSVD + GPTQ-INT4 outperforms SVD-LLM alone at 60%+ compression, demonstrating practical combinability with other compression methods.

## Weaknesses

### Fatal
None.

### Major

- **Iterative optimization framing contradicted by results (Table 3c)** — The paper presents adaComp as an iterative convergence procedure (Eq. 16, Figure 3), but Table 3c shows that **1 iteration is optimal on WikiText-2 at every tested compression ratio**: 40% (14.76 vs. 15.47 at 3 iters), 50% (25.58 vs. 27.11 at 3 iters), 60% (50.33 vs. 64.12 at 3 iters). More iterations consistently degrade performance. The paper acknowledges overfitting (Section 4.3: "increasing the number of iterations may lead to overfitting due to the limited calibration data") but provides no principled stopping criterion, regularization, or selection guidance. This means the method is effectively a single-pass correction, not the iterative optimization portrayed in the presentation. While this doesn't invalidate the results, it significantly overclaims the algorithmic contribution.

- **Neither component alone consistently beats SVD-LLM (Tables 3a, 3b)** — At 50% compression, Table 3b shows adaComp alone (without adaCR) yields WikiText-2 PPL of 27.33 vs. SVD-LLM's 27.19 — slightly *worse*. Table 3a shows adaCR alone (without adaComp) yields 30.00 vs. SVD-LLM's 27.19 — substantially worse on both WikiText-2 and C4 (166.02 vs. 129.66). The paper's claim "AdaSVD already outperforms SVD-LLM without using adaCR" (Section 4.3) is contradicted at 50% on WikiText-2. This inconsistency is not acknowledged and suggests the two components interact synergistically rather than contributing independently, which complicates the clean modular narrative.

- **Evaluation limited to 7B-scale models** — All four tested models (LLaMA2-7B, OPT-6.7B, Vicuna-7B, Mistral-7B) are ~7B parameters. Figure 4 shows the authors computed layer importance for LLaMA-13B, OPT-1.3B, and OPT-2.7B, suggesting access to other scales. SVD compression is most practically relevant for large models on constrained hardware; showing only 7B leaves scalability claims unsupported.

- **No computational cost analysis** — The paper reports no wall-clock time or FLOPs. adaComp requires computing matrix products V_k^σ · X, performing SVD of A = X^T V_k^σ (Eq. 9), and pseudoinverse calculations for every weight matrix. Without timing data, the practical trade-off between compression quality and compression time cannot be assessed. This omission is particularly important given the comparison with SVD-LLM, which also reports no timing — a fair comparison requires knowing the additional overhead.

### Minor

- **adaCR importance metric lacks theoretical justification (Eq. 17)** — The cosine similarity between input X and output WX is used to measure layer importance, with high similarity interpreted as "more important." However, high cosine similarity between input and output means the layer acts approximately as an identity/scaling operation, which could equally be interpreted as the layer being *less* important (removing it changes the signal less). The paper does not discuss this ambiguity or compare against alternative allocation strategies (e.g., sensitivity-based metrics from the pruning literature, or singular value spectral analysis).

- **Overclaimed novelty for adaComp** — Alternating least squares (ALS) with pseudoinverse solutions is a long-established technique in matrix factorization (standard in NMF, collaborative filtering, tensor decomposition). The paper frames this as novel ("we propose a two-fold strategy to enhance the update quality," Section 3.1) without acknowledging the existing ALS lineage. The application to activation-weighted low-rank reconstruction in LLMs is a valid contribution, but the framing overstates methodological novelty.

- **Anomalous PTB results unexplained (Table 1)** — At 40% compression, SVD-LLM shows WikiText-2 PPL of 16.11 but PTB PPL of 719.44 — a 45× discrepancy. AdaSVD improves PTB to 304.62, but these catastrophic values are not discussed. This extreme divergence between evaluation datasets raises questions about the evaluation protocol for PTB specifically.

### Trivial
None noted.

## Nice-to-Haves
- A gradient-based fine-tuning baseline for the low-rank factors would contextualize whether the specific ALS approach matters, or whether any post-hoc adjustment yields similar gains.
- Discussion of absolute model usability at high compression ratios (at 60%, average reasoning accuracy drops from 68.85% to 36.87%, a 46% relative decline).
- Experiments at 13B+ scale, ideally 70B, to demonstrate practical relevance of SVD compression.
- Comparison of adaCR's cosine-similarity metric with at least one alternative layer-importance metric.

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **"Absolute quality of compressed models is poor and practical utility is questionable"** — This applies equally to all SVD-based compression methods at high ratios, not specifically to AdaSVD. The paper's contribution is relative improvement within this paradigm. Removed as scope creep.
- **"Stack-of-batch loses information about activation distribution"** — While theoretically the averaging in Eqs. 14–15 collapses multiple samples, Figure 3(b) empirically shows SoBC reduces compression error more effectively than naive calibration. The criticism is speculative without counter-evidence.
- **"Missing comparison with other compression families (quantization, pruning)"** — The paper explicitly scopes itself to SVD-based compression and shows orthogonality with quantization (Table 4). Demanding full comparison across all compression paradigms is scope creep.

## Novel Insights
The finding that a single pass of alternating factor updates consistently outperforms multiple iterations across all compression ratios (Table 3c) is a genuinely useful observation. It suggests that the calibration signal from 256 samples is exhausted after one correction step, and that the benefit of adaComp comes from a one-shot adjustment rather than iterative refinement. This has practical implications: future work in this space should invest in expanding the effective calibration signal (more data, better data selection) rather than in more sophisticated optimization procedures.

## Suggestions
- Reposition adaComp honestly as a single-pass ALS correction for activation-weighted low-rank reconstruction, acknowledging the classical ALS lineage and focusing novelty on the LLM-specific contributions (stack-of-batch, interaction with data whitening, empirical finding that k=1 suffices).
- Correct the overclaimed ablation results: explicitly note that at 50% compression, neither component alone beats SVD-LLM on WikiText-2, and discuss the synergistic interaction.
- Add wall-clock timing comparisons against SVD-LLM.
- Test on at least one model at 13B+ scale to support scalability claims.
- Compare adaCR with at least one alternative importance metric (e.g., layer sensitivity via perturbation analysis).

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to AdaSVD |
|-------|------|-----------|-------|---------------------|
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Pure survey, not comparable — AdaSVD is far stronger |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.00 | R1 | Irrelevant topic, pseudoscience-adjacent — AdaSVD is far stronger |
| UMAP Scientific Discourse | P49gSPmrvN | 1.00 | R1 | Irrelevant topic — AdaSVD is far stronger |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | R1 | Different topic, minimal contribution — AdaSVD is far stronger |
| Implicit Bias in Matrix Factorization | ZTvUT49JjL | 3.40 | R1 | Theoretical matrix factorization; more ambitious but poorly supported. AdaSVD is more empirically grounded |
| CVXQ: LLM Compression via Convex Opt | 0T8vCKa7yu | 3.00 | R1 | LLM compression paper rejected for limited novelty; AdaSVD has broader evaluation |
| FeDeRA | GtlRN48XYA | 3.00 | R1 | Federated learning + SVD; different application. Similar novelty concerns |
| PrefixQuant | vw0NurJ7UX | 3.00 | R1 | LLM quantization; rejected for limited novelty. Different compression family |
| **MoE-SVD** | ho7ZUS1z8A | **5.00** | R1 | **Most comparable: SVD for MoE LLMs. MoE-SVD targets a novel problem space (MoE) and tests on larger models. AdaSVD has better ablations but similar scope limitations. Comparable quality.** |
| **AutoTrunc** | 3KEwJGYNzH | **4.00** | R1 | **Very similar contribution: layer-specific SVD truncation for LLMs. AutoTrunc had poor presentation and fewer experiments. AdaSVD is stronger due to broader evaluation and cleaner formulation.** |
| TensorGPT | FVgizbs3o2 | 3.75 | R1 | Tensor decomposition for LLM compression; rejected for limited practical utility |
| **Low-Rank Correction for Quantized LLMs** | FA3iYp1y6z | **5.00** | R1 | **Rejected for "stitching well-known building blocks." Similar criticism applies to AdaSVD (ALS is classical). Comparable quality.** |
| **ASVD** | HyPofygOCT | **6.25** | R1 | **AdaSVD's own baseline. ASVD was rejected despite 6.25 avg. ASVD introduced a more genuinely novel concept (activation-aware SVD). AdaSVD provides an incremental improvement over this rejected work.** |
| **Basis Sharing** | gp32jvUquq | **6.50** | R1 | **Accepted SVD compression paper with genuinely novel cross-layer sharing idea. Reported throughput. AdaSVD is weaker in both novelty and evaluation breadth.** |
| OATS | DLDuVbxORA | 6.25 | R1 | Accepted; combines sparse and low-rank decomposition. More novel approach |
| Double Sparse Factorization | DwiwOcK1B7 | 6.33 | R1 | Accepted; novel factorization into two sparse matrices. Stronger novelty |
| HiRA | TwJrTz9cRS | 8.00 | R1 | Accepted; novel Hadamard-based adaptation. Much stronger contribution |
| Data selection via submodular | f4gF6AIHRy | 8.00 | R1 | Different topic. Much stronger paper |
| Scaling Laws for Precision | wg1PCg3CUP | 8.00 | R1 | Different topic. Much stronger paper |
| DEPT | vf5aUZT0Fz | 8.00 | R1 | Different topic. Much stronger paper |

**Round 1 bracket: 4.0–5.0**

AdaSVD is clearly stronger than AutoTrunc (4.00) due to broader evaluation and cleaner presentation. It is comparable to MoE-SVD (5.00) and Low-Rank Correction (5.00), which were both rejected for limited novelty with well-known techniques. It is weaker than ASVD (6.25, rejected) and Basis Sharing (6.50, accepted) in terms of novelty. The fact that ASVD — AdaSVD's own baseline which introduced a more novel concept — was itself rejected at 6.25 reinforces that an incremental improvement faces a high bar.

**Final reasoning**: AdaSVD applies a classical optimization technique (ALS) to a specific setting (SVD-based LLM compression) and pairs it with a simple layer-wise CR allocation. The improvements are consistent but modest, the evaluation is limited to 7B models with no timing data, and several evidential concerns (overfitting with iterations, overclaimed component effectiveness) weaken the contribution. The method is sound and the execution is reasonable, but the combination of limited novelty, bounded experimental scope, and presentation overclaims places it in the borderline reject range. Anchoring against the most comparable papers — AutoTrunc (4.0), MoE-SVD (5.0), Low-Rank Correction (5.0), and the rejected ASVD baseline (6.25) — I score this at **4.5**.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>