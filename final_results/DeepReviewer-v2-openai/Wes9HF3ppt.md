## Summary
This paper introduces Insertion Language Models (ILMs), a new sequence generation paradigm that generates tokens one at a time by jointly predicting a token and its insertion position within the current partial sequence. The key technical contribution is a denoising training objective that avoids the high-variance Monte Carlo marginalization over insertion trajectories by instead predicting normalized token-count distributions between visible tokens. The model uses a standard transformer encoder with a position-wise insertion head and a dedicated stopping classifier.

The empirical evaluation covers planning tasks (star graph path generation and zebra puzzles) and text generation (LM1B and TinyStories datasets). On planning, ILM significantly outperforms both autoregressive models (ARMs) and masked diffusion models (MDMs), achieving 99.1% exact-match accuracy on the hardest star graph variant versus 21% for MDM, and 90% on zebra puzzles versus 81.2% for ARM. On text, ILM is competitive with ARMs on Stories data (2.14 vs 2.11 NLL) but underperforms on LM1B (4.67 vs 3.94 NLL), while exceeding MDM on both.

The work has several strengths — a well-motivated research question, strong planning results, and a clean formulation — but also faces notable weaknesses: training-inference mismatch in the stopping classifier, notation inconsistencies in the loss and parameterization equations, insufficient statistical reporting (no variance estimates), and a questionable causal explanation for MDM failure on star graphs. Novelty is moderate; the insertion-based generation framing builds on prior work (Stern et al., Ruis et al.) while the denoising formulation is new. External literature verification was unavailable in this run (Retrieval-Disabled Mode).

## Strengths
**S1 — Well-motivated research question.** The paper identifies a genuine limitation of both ARMs (fixed generation order) and MDMs (simultaneous unmasking, fixed-length constraint) and proposes insertion-based generation as a principled alternative. The motivation examples (chef/dessert, conference infilling) are concrete and persuasive.

**S2 — Clean technical formulation.** The training objective (Eq. 2) is conceptually simple: drop tokens randomly, then predict the count distribution of missing tokens between each visible-pair gap. The parameterization uses a standard transformer with minimal modifications, making the method easy to adopt.

**S3 — Impressive planning results.** On star graph path generation with variable arm lengths, ILM achieves 99.1% exact-match accuracy versus 21% for MDM and 23% for ARM (left-to-right). This is a large and convincing margin, particularly given the task's requirement for iterative reasoning. On zebra puzzles, ILM reaches 90% accuracy, outperforming both ARM (81.2%) and MDM (82.6%) and approaching the oracle-decomposed ARM baseline (91.2%).

**S4 — Explicit addressing of the stopping problem.** The dedicated stopping classifier (L_stop) is a principled departure from prior insertion-based models (e.g., Insertion Transformer's EOS-based termination), which the paper demonstrates leads to more reliable length control.

**S5 — Multi-domain evaluation.** The paper evaluates on planning (synthetic) and language modeling (LM1B, TinyStories), covering both structured reasoning and open-ended generation. The inclusion of LLM-judge metrics (Prometheus 2) beyond NLL is a strength for assessing generation quality.

**S6 — Honest limitations section.** The paper acknowledges key limitations — worse NLL than ARMs, lack of KV caching, computational overhead — which helps readers assess practical trade-offs.

## Weaknesses
### W1 — Training-Inference Mismatch in the Stopping Classifier (Major, Validity Risk)
The stop loss $\mathcal{L}_{\text{stop}}^{\text{ilm}}$ is trained with $n \sim U[L]$ where $n \in \{1, \dots, L\}$ (uniform over the number of dropped tokens, $n \ge 1$). The $\delta(\mathbf{b}, \mathbf{0})$ term that triggers the stop-positive signal ($S=1$) requires the bit vector $b$ to be all zeros, i.e., $n=0$. However, $n=0$ is never sampled under $U[L]$ as defined (uniform over $\{1,\dots,L\}$). This means the model never sees a positive stop example during training and must learn to predict "sequence complete" purely from the absence of dropped-token features — a weak and potentially unreliable signal. This likely contributes to the Insertion Transformer's poor length control and may affect ILM even with the dedicated classifier. **Recommendation:** Include the intact sequence ($n=0$) as a stop-positive example with small probability during training, or modify the stop loss to use a held-out completion detection mechanism.

### W2 — Questionable Causal Explanation for MDM Failure on Star Graphs (Major, Credibility Risk)
The paper claims MDM fails on variable arm lengths because it "work[s] with absolute token positions" (Page 5 - Star Graphs). However, the MDM implementation uses RoPE (rotary position encoding), which is a *relative* position encoding — not absolute. The additional AdaLN layers condition on diffusion time, not token position. Therefore, the "absolute token positions" attribution is factually inaccurate. The actual failure cause is likely the simultaneous unmasking constraint (MDM must predict all tokens in large batches, preventing iterative resolution of interdependent constraints) or the fixed-length masking (which prevents adapting to variable-length solutions). **Recommendation:** Replace the position-encoding-based explanation with a mechanism grounded in MDM's parallel decoding limitation. A controlled ablation comparing RoPE vs. learned absolute position embeddings in MDM would clarify the real cause.

### W3 — Notation Inconsistencies and Underspecified Ranges in Training Objective (Major, Reproducibility Risk)
The training objective (Eq. 2) has two interrelated issues:
(a) The sum $\sum_{k \in [L-n]}$ lacks an explicit sum over vocabulary items $v$, making it ambiguous whether $c_{i_k,i_{k+1}}(v;\mathbf{x})$ is multiplied by $\log p$ for each $v$ or the sum over $v$ is implicit. A proper cross-entropy requires $\sum_k \sum_v c(\dots) \log p(\dots)$.
(b) The logit function $s_\theta(k,v|x[b])$ in Eq. (3) defines insertion "between $k$ and $k+1$" but the joint distribution (Eq. 4) sums over only $L-n$ positions (excluding insertion before the first token or after the last token). This potentially limits the model's ability to generate prefixes or suffixes.
**Recommendation:** Make the sum over $v$ explicit in Eq. (2) and clarify the insertion position range: there should be $L-n+1$ possible insertion gaps, not $L-n$.

### W4 — Insufficient Statistical Reporting (Major, Evidence Quality)
All experimental results (Tables 1, 2, 3, Figure 5) are reported as single numbers without confidence intervals, standard deviations, or significance tests. The unconditional generation NLL gap between ARM (2.11) and ILM (2.14) on Stories is only 0.03 — potentially within noise range. On zebra puzzles, the 1.2% gap between ILM (90.0%) and ARMO (91.2%) may or may not be significant. The zebra puzzle results lack multi-seed variance entirely despite known training instability in transformer-based models. **Recommendation:** Report all metrics as mean ± std over at least 3 random seeds (training from scratch each time). Add a statistical significance test (e.g., paired bootstrap) for key comparisons.

### W5 — Unsupported NLL Gap Analysis for LM1B Text Generation (Major, Claim Credibility)
The paper claims ILMs are "competitive with ARMs" on text generation, but on LM1B the NLL gap is substantial: ARM 3.94 vs ILM 4.67 (0.73 points, a ~19% relative increase). The paper briefly attributes this to "training token efficiency and scaling laws" (citing Nie et al., 2024) without deeper analysis. This gap is closer to MDM (4.81) than to ARM, suggesting ILM may fundamentally struggle with short-sequences-large-vocabulary settings. **Recommendation:** Provide a more detailed analysis of the LM1B gap. Candidate factors to investigate: (a) sparsity of the target insertion distribution in short contexts, (b) vocabulary size effects on the insertion prediction problem, (c) potential improvements from data-dependent noising schedules.

### W6 — Potential Confound in Infilling Evaluation (Moderate, Evidence Quality)
The infilling evaluation uses $\Delta\text{NLL}_{\text{gt}}$ and $\Delta\text{NLL}_{\text{inp}}$ as metrics. When computing NLL under Llama for $\mathbf{x}^{\text{inp}}$ (input with missing segments), the LLM conditions on incomplete context for positions *adjacent* to the removed segment. This can systematically bias the NLL comparison in ways that differ between MDM and ILM (e.g., if they fill different-length segments). The paper does not discuss this confound. **Recommendation:** Add a controlled evaluation where the reference model's NLL is computed only on the filled segment (not the full sequence) to reduce context-bias artifacts.

### W7 — Lower Diversity and Potential Over-Conservatism (Moderate, Practical Impact)
ILM's entropy on Stories (3.76) is notably lower than both ARM (4.06) and the training data (4.19), indicating less diverse generation. The paper notes this but treats it as secondary. Lower diversity may reflect a systematic bias toward inserting common/safe tokens, which could limit practical usefulness in creative applications. **Recommendation:** Analyze the token distribution of ILM generations vs. training data to identify specific diversity gaps. If bias exists, consider modifying the sampling procedure (e.g., temperature scaling during insertion) to increase diversity.

### W8 — Limited Related-Work Positioning (Minor, Presentation)
The Related Work section organizes literature by model type (MDM improvements, order-agnostic models, ARM infilling) but does not explicitly compare ILM's training objective with the closest prior work (Insertion Transformer, Stern et al. 2019). The reader must infer differences from later experimental results. Additionally, the claim "All these approaches rely on inference time techniques" is immediately contradicted by the next sentence about Ye et al. (2025) modifying training. **Recommendation:** Add a direct comparison paragraph: "Compared to the Insertion Transformer (Stern et al., 2019), ILM replaces the token-prediction objective with a denoising formulation and a dedicated stopping classifier, overcoming the length-control issues we document in Section 5."

## Score
**Final Score: 6/10**

### Rationale

The paper addresses a well-motivated research question and delivers convincing results on planning tasks. The technical formulation is clean and the empirical evaluation is multi-faceted. However, several issues prevent a higher score:

1. **Research value (moderate).** The core idea — insertion-based generation via denoising — is a meaningful contribution, but it builds directly on established insertion-based generation work (Stern et al., Ruis et al.) and MDMs. The novelty lies primarily in the training objective formulation rather than the generation paradigm itself.

2. **Validity risks (significant).** The training-inference mismatch in the stopping classifier (W1), the questionable causal explanation for MDM failure (W2), and the notation inconsistencies in the loss equations (W3) raise concerns about whether the method as described is correctly specified and reproducible.

3. **Evidence quality (moderate).** The planning results are strong but lack statistical grounding (no variance estimates, no significance tests). The text generation results show a large NLL gap on LM1B that is not adequately analyzed (W5).

4. **Reproducibility (moderate).** The notation issues (Eq. 2, Eq. 4) and the underspecified insertion position range make exact reproduction harder than necessary. The anonymized code release mitigates this, but the paper text should be self-contained.

The weaknesses are fixable with moderate effort (clarifying notation, adding multi-seed experiments, correcting causal explanations), and the core planning results are likely to hold with proper statistical validation.

---

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: ARMs fail at non-sequential dependencies, MDMs fail at variable-length infilling]
    |
    ├── Claim C1: ILM learns to insert tokens at arbitrary positions
    │   └── Evidence: Star graph (99.1%) and zebra puzzle (90%) results
    │       └── Gap: No analysis of insertion position dynamics during generation
    ├── Claim C2: Transformer param + denoising objective enable training
    │   └── Evidence: Eq. (2)-(4), Algorithm 1
    │       └── Gap: Notation inconsistencies (W3), stop-classifier mismatch (W1)
    └── Claim C3: ILM competitive with ARM, better than MDM on text + infilling
        └── Evidence: Tables 2, 3, Figure 5
            └── Gap: Large LM1B NLL gap unanalyzed (W5), no variance (W4)
```

### ASCII Diagram — Revision Strategy Roadmap

```text
Stage 1 (Must-fix, 1-2 days):
├── Fix stop classifier: include n=0 examples during training (W1)
├── Correct MDM failure explanation to cite parallel decoding, not position encoding (W2)
└── Make Eq. (2) sum over v explicit, clarify insertion range in Eq. (4) (W3)

Stage 2 (Should-fix, 1 week):
├── Re-run all experiments with 3+ seeds, report mean±std (W4)
├── Add detailed analysis of LM1B NLL gap (W5)
├── Acknowledge infilling evaluation confound (W6)
└── Analyze and discuss entropy/diversity gap (W7)

Stage 3 (Nice-to-have, before final submission):
├── Add FiM baseline for infilling
├── Expand Related Work with direct IT comparison (W8)
└── Provide quantitative analysis of insertion position dynamics on star graphs
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
Sequence Generation Paradigms (Root)
├── Branch 1: Fixed-order generation
│   ├── Leaf 1.1: Autoregressive (left-to-right) [Brown, Grattafiori]
│   └── Leaf 1.2: Fill-in-the-Middle (prefix-suffix) [Bavarian]
├── Branch 2: Flexible-order generation with masking
│   ├── Leaf 2.1: Masked Diffusion Models [Sahoo, Lou, Austin, Campbell, Shi]
│   ├── Leaf 2.2: Order-agnostic autoregressive [Yang, Hoogeboom]
│   └── Leaf 2.3: Adaptive MDM training [Ye]
└── Branch 3: Insertion-based generation ← ILM (This paper)
    ├── Leaf 3.1: Insertion Transformer [Stern, Ruis]
    └── Leaf 3.2: Denoising insertion models [ILM - no prior equivalent]
```

**Value positioning:** ILM occupies a previously empty niche — insertion-based generation with a principled denoising objective, capable of both arbitrary-order generation and variable-length infilling without placeholder tokens. Its comparative advantage over MDMs is clearest on tasks requiring iterative constraint resolution (star graphs), while its advantage over ARMs is clearest on tasks where generation order matters (both planning tasks). On standard text generation, the advantage is less clear.

### Novelty Verification Note

External literature verification was not available in this run (Retrieval-Disabled Mode — paper_search unavailable due to missing API token). All novelty assessments above are based on the manuscript's self-citations and internal evidence. A thorough prior-art comparison with insertion-based generation methods, MDM variants, and order-agnostic models should be conducted manually before publication. The claim that ILM is the first insertion-based model with a denoising objective is plausible but requires external verification.

### Page Coverage Audit

| Page | Annotation Count | Coverage Status | Skip Reason (if skipped) |
|------|-----------------|-----------------|-------------------------|
| 1 (Title/Abstract/Intro/Method/Related Work/Experiments/Conclusion) | 14 | Covered | N/A — all substantive paragraphs covered |
| Appendix (removed from provided text) | 0 | Not reviewed | Content not available in provided manuscript |

**Note:** The manuscript file contains pages 0-8 in a single continuous text block (page markers `{0}------------------------------------------------` to `{8}------------------------------------------------`). All content is on page 1 in pdf_read_lines. All substantive sections (Abstract, Introduction, Preliminaries, ILM Method, Related Work, Experiments, Conclusion) have been annotated.