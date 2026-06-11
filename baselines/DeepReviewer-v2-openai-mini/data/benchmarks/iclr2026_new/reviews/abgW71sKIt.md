## Summary
This paper investigates the failure modes of output alignment in 1-bit post-training quantization (PTQ) for large language models (LLMs). The authors identify three specific limitations of naive layer-wise output matching (as implemented in ARB-X): (i) it does not guarantee block-level loss reduction, (ii) quantization errors accumulate across layers because the optimization objective conditions on quantized activations $\hat{X}$ rather than full-precision inputs $X$, and (iii) indiscriminate output alignment degrades attention mechanisms by distorting token-similarity matrices, especially in RMSNorm-based architectures like LLaMA. To address these issues, the paper proposes: (a) replacing the activation-conditioned error $\|\hat{X}W - \hat{X}\hat{W}\|$ with the true output error $\|XW - \hat{X}\hat{W}\|$, (b) restricting output alignment to the last fully-connected layer of each block, and (c) introducing Attention Matrix Preservation (AMP) which uses gradient-sign masking to prevent token-similarity drift during quantization. Experiments on OPT (1.3B–30B) and LLaMA-2/3 (7B–13B) show consistent perplexity improvements over prior 1-bit PTQ methods (PB-LLM, BiLLM, ARB-RC, ARB-X), with up to 4.85 points reduction on OPT-1.3B. The analysis of output-vs-activation error divergence and the AMP mechanism provide useful diagnostic insights for the 1-bit LLM quantization community. However, the paper's novelty claims cannot be fully verified due to the unavailability of external literature search in this run, several mathematical presentation issues (notably a typo in Eq. 2 and an unused variable K in Eq. 6), and the absence of key reproducibility details (calibration setup, convergence criteria, compute budget). The PTB evaluation yields perplexities exceeding 3000, which the text itself acknowledges as meaningless, raising questions about inclusion criteria.

## Strengths
1. **Diagnostic clarity.** The paper provides a systematic diagnostic of why naive output alignment fails for 1-bit LLM quantization. The three identified issues (block-level mismatch, error accumulation, attention degradation) are well-motivated through controlled experiments (Figures 1 and 2). The distinction between Activation-conditioned Error and true Output Error is a clean conceptual contribution that clarifies a previously under-explored aspect of 1-bit PTQ.

2. **Attention Matrix Preservation (AMP) is a principled fix.** The idea of preserving the token-similarity matrix during quantization via gradient-sign masking is technically sound and addresses a real problem (attention degradation in RMSNorm-based architectures). The ablation study (Table 3) shows that AMP provides dramatic improvements for LLaMA (>10 perplexity points), confirming that attention degradation is a previously unaddressed bottleneck in 1-bit LLM quantization.

3. **Comprehensive evaluation scope.** The experiments cover two major model families (OPT 1.3B–30B and LLaMA-2/3 7B–13B), three language modeling benchmarks (C4, WikiText2, PTB), and zero-shot QA evaluations across seven datasets. This breadth supports the generalizability claims better than many prior 1-bit PTQ papers that focus on a single model family.

4. **Closed-form optimization efficiency.** The derivation of closed-form solutions for $\alpha_c$, $\alpha_r$, and row-wise $B$ (Eqs. 5–8) avoids iterative gradient descent, promising practical efficiency for deployment scenarios. The paper explicitly mentions using `torch.linalg.lstsq` for numerical stability, which is a practical engineering consideration that aids reproducibility.

5. **Honest limitation disclosure.** The paper acknowledges that PTB perplexity values are too high to be meaningful, which demonstrates scientific integrity. The RMSNorm hypothesis for LLaMA's sensitivity is presented as a hypothesis rather than a confirmed finding (though this could be strengthened).

## Weaknesses
The weaknesses are organized by severity, starting with the most impactful issues.

### W1. Mathematical errors and notation issues in the method section (Major)

**Location**: Page 1 — Section 4, Equations (2), (6)

**Evidence**: Eq. (2) is written as $\|\hat{X}\hat{W} - \hat{X}\hat{W}\|_F^2$, which is identically zero because both terms are identical. The surrounding text describes ARB-X as minimizing $\|\hat{X}W - \hat{X}\hat{W}\|$, so this is clearly a typo, but it undermines mathematical credibility. Additionally, variable $K = \text{diag}(\alpha_c \odot \alpha_c)$ is defined before Eq. (6) but never used in that equation or anywhere else—suggesting the derivation may have been carried over from a different formulation without full verification.

**Impact**: A reader attempting to re-implement from the equations would be confused by a zero-valued loss. The unused $K$ signals incomplete derivation cleanup. While these issues are individually fixable, they collectively reduce confidence in the mathematical presentation and suggest the need for careful proofreading.

**Required fix**: Correct Eq. (2) to $\|\hat{X}W - \hat{X}\hat{W}\|_F^2$. Remove $K$ if unused, or explain its role in the derivation.

### W2. Missing reproducibility-critical details (Major)

**Location**: Page 1 — Section 5.1 Experiment Setup

**Evidence**: The calibration protocol is described only as "C4 calibration set" without specifying: (a) number of calibration samples, (b) sequence length, (c) selection strategy (random vs stratified), (d) convergence criterion or iteration budget for the joint optimization. No compute budget (GPU type, memory, wall-clock time) is reported in the main text—the "Overhead Analysis" is deferred entirely to Appendix D. Furthermore, the reported "Weight Bits" are 1.06–1.11 (Tables 1 and 2), which means the methods are not strictly 1-bit; they allocate additional bits for scaling factors $\alpha_r, \alpha_c$. The paper's title and abstract claim "1-bit quantization" but the actual implementation uses mixed precision (binary weights + floating-point scaling factors).

**Impact**: These omissions make it impossible for independent researchers to reproduce the results without guessing key hyperparameters. The 1-bit framing is technically imprecise: the method uses binary weights with row/column scaling factors, yielding >1 bit on average.

**Required fix**: Add a calibration details paragraph (sample count, sequence length, selection strategy). Report quantization time and peak GPU memory for at least LLaMA-2-7B. Clarify in the abstract or introduction that "1-bit" refers to the weight matrix being binarized while scaling factors are stored at higher precision.

### W3. PTB evaluation results are scientifically uninformative (Major)

**Location**: Page 1 — Section 5.2, Table 2

**Evidence**: On PTB, the proposed method yields perplexity 3166 for LLaMA-2-7B (vs 37.91 full-precision), ARB-RC yields 763, and BiLLM yields 5243. The paper itself admits: "However, the large perplexity indicates that the metric cannot provide a meaningful evaluation." Yet these numbers are displayed prominently in the main comparison table alongside meaningful results from C4 and WikiText2.

**Impact**: Including uninformative metrics in the main table creates two problems: (a) it dilutes the impact of valid results, and (b) it risks misleading readers who do not read the caveat into believing that the relative rankings are meaningful. The near-random perplexities (5243 is essentially a uniform distribution over a vocabulary of ~50k tokens) do not support any conclusion about method quality.

**Required fix**: Move PTB results to the appendix as a stress test. Replace with a more robust evaluation (e.g., accuracy on downstream tasks, or percentage of sequences with PPL below a threshold) if the authors wish to keep PTB in the main paper.

### W4. Section 3.1's evidence scope does not fully support the claim (Minor)

**Location**: Page 1 — Section 3.1

**Evidence**: The key motivating claim is that "layer-wise output matching does not necessarily lead to block-level loss reduction." The supporting experiment quantizes only one layer per block while keeping all others at full precision. This is a clean experimental setting, but it does not reflect the full quantization scenario where all layers are quantized simultaneously. The interaction effects under joint quantization could either amplify or cancel the observed phenomenon.

**Impact**: The claim is supported as an existence proof but not as a general statement about full quantization. While this does not invalidate the overall approach, the authors should explicitly note this scope limitation and ideally provide a supplementary experiment under full quantization.

**Required fix**: Add either (a) a follow-up experiment with all layers quantized simultaneously, or (b) an explicit caveat that the analysis isolates single-layer effects and that joint quantization may exhibit different behavior.

### W5. RMSNorm hypothesis for AMP effectiveness is unverified (Minor)

**Location**: Page 1 — Section 5.3 Ablation Study

**Evidence**: The paper hypothesizes that LLaMA's severe AMP degradation (perplexity increase >10 without AMP) arises from RMSNorm because "RMSNorm normalizes each token to unit norm before applying a learned scale, making the model more dependent on the direction of representations." No controlled experiment is conducted to verify this: e.g., replacing RMSNorm with LayerNorm in LLaMA (or vice versa in OPT) and measuring AMP's effect.

**Impact**: The RMSNorm explanation is plausible but remains speculative. The observed correlation (LLaMA uses RMSNorm and suffers more) does not rule out other architectural differences (activation functions, attention design, training data) as the true cause. This weakens the scientific contribution of the AMP analysis.

**Required fix**: Either run a controlled normalization ablation (LayerNorm vs RMSNorm in the same architecture), or downgrade the claim to a conjecture and explicitly list alternative explanations.

### W6. AMP optimization direction is ambiguously specified (Minor)

**Location**: Page 1 — Section 4.1, Equations (9)–(11)

**Evidence**: Eq. (9) states "max $\mathcal{L}_{AMP}$" but the update Eq. (11) uses a mask-based replacement that selects between the current value and the closed-form optimum based on the sign of the gradient. The semantics are not explained: does $M=1$ mean "preserve this parameter's current value" or "use the closed-form update"? The relationship between maximizing $\mathcal{L}_{AMP}$ and the masking operation is not derived.

**Impact**: An independent implementation would require the reader to reverse-engineer the intended logic from the equations, increasing the risk of implementation errors.

**Required fix**: Add a sentence explaining the AMP mechanism: "The AMP mask $M$ indicates parameters for which the token-similarity gradient direction agrees with preservation of attention structure; parameters with $M=1$ are updated to their closed-form optimum, while those with $M=0$ retain their current value."

### W7. No ablation isolating the selective layer-wise strategy from AMP (Minor)

**Location**: Page 1 — Section 5.3

**Evidence**: The method has three components: (a) output error objective, (b) selective layer-wise strategy (output alignment only on last block layer), and (c) AMP. The ablations test (a) vs activation-conditioned error (Table 4) and (c) with/without AMP (Table 3), but component (b)—the selective layer strategy—is never independently ablated. Without this ablation, the individual contribution of (b) is unknown.

**Impact**: Readers cannot tell how much of the gain comes from the output error objective vs the selective layer selection vs AMP. A three-factor ablation would strengthen the paper.

**Required fix**: Add an ablation where (i) output error objective without selective layers, (ii) output error + selective layers, (iii) output error + selective layers + AMP are compared.

### W8. Novelty and literature positioning are deferred (Deferred)

**Location**: Entire paper

**Evidence**: Due to Retrieval-Disabled Mode in this review run (external paper search unavailable), novelty and literature positioning cannot be independently verified. The paper claims to be the first to identify the output-vs-activation error distinction and to propose AMP, but these claims require manual literature verification against prior 1-bit PTQ methods (ARB-X, BiLLM, STB-LLM, etc.) and attention-preservation techniques in quantization more broadly.

**Impact**: The paper's contribution could be partially overlapping with concurrent or prior work not discussed in the manuscript. This is a deferred judgment call.

## Score
**Final Score: 6/10**

**Rationale.** The paper addresses a timely problem (1-bit PTQ for LLMs) and contributes a clear diagnostic framework (output error vs activation-conditioned error) plus a targeted mitigation (AMP) that proves highly effective for LLaMA models. The diagnostic insights alone—especially the demonstration that attention mechanisms degrade under naive output alignment—are valuable for the PTQ community. The experimental evaluation is broad in model coverage and shows consistent improvements across multiple benchmarks.

However, the score is constrained by the following factors:

- **Mathematical presentation issues (W1)** — Eq. (2) contains a zero-valued typo, and an unused variable $K$ appears in the derivation. While individually fixable, these errors reduce confidence in the technical execution.
- **Reproducibility gaps (W2)** — Missing calibration details, convergence criteria, and compute budget hinder independent verification. The >1-bit average precision (1.06-1.11 bits) is not consistently framed as "binary weights + scaling factors."
- **Uninformative PTB results (W3)** — Including perplexity values >3000 in the main table without clear exclusion criteria creates a misleading presentation.
- **Incomplete ablation (W7)** — The selective layer strategy (component b) is never ablated independently, preventing assessment of each component's contribution.
- **Novelty unverifiable in this run (W8)** — All novelty claims are deferred for manual verification due to external literature search being unavailable.

These weaknesses are fixable with targeted revisions (correcting equations, adding ablation and reproducibility details, removing uninformative results). The core technical contribution—identifying and addressing the output-vs-activation error gap in 1-bit PTQ—is sound and well-motivated. The score reflects a solid paper with good diagnostic insights that needs cleaning before publication. If the mathematical issues are corrected, required details are added, and the PTB reporting is fixed, the paper could reach 7-7.5/10 in a revised version.