Now I have a thorough understanding of the paper. Let me draft my review before calibration.Now let me calibrate with Round 1 — Bracketing:Let me read a few key anchors to calibrate my score:Now I have enough context to finalize my review. Let me synthesize my findings.

---

## Summary
This paper empirically investigates the optimization dynamics of SSMs (Mamba, Hyena) versus Transformers on two synthetic benchmarks—multi-query associative recall (MQAR) and copying. The central finding is that SSMs are dramatically more sensitive to learning rate than Transformers, with success confined to an extremely narrow window. The paper argues that prior expressivity conclusions (Arora et al., 2023) may have been confounded by suboptimal tuning, and documents contrasting width-vs-depth scaling behaviors, a clean convolution ablation, and the relative optimization stability of DeltaNet.

## Strengths

- **Learning rate sensitivity finding is well-documented, reproducible, and actionable.** Figure 1 clearly demonstrates that Mamba and Hyena have dramatically narrower windows of effective learning rates compared to Transformers on MQAR, shown across multiple model dimensions (64, 512) and sequence lengths with 5 seeds per configuration. The dashed lines showing where Arora et al. (2023)'s grid falls outside the SSM optimal window is a particularly effective visualization that makes the confounding immediately apparent.

- **Productive recontextualization of Arora et al. (2023).** Figure 2 demonstrates that with proper learning rate tuning, Mamba solves MQAR at sequence length 512 with hidden dimension 64—directly contradicting the prior narrative that hidden dimension must roughly equal sequence length. This is a concrete, falsifiable correction to influential prior work.

- **Clean convolution ablation in Table 2.** The finding that adding a 1D convolution to 1-layer Attention enables MQAR (2% → 99%), while removing it from Mamba collapses performance to 2%, is a well-controlled experiment isolating the convolution's role. The further ablations (removing gating, replacing Mamba block with S6+MLP) systematically identify the S6 mixer as the root of expressivity.

- **DeltaNet stability finding (Figure 7, Section 7) points toward architectural design principles.** DeltaNet achieves Transformer-level learning rate robustness, and the hypothesis connecting this to Householder-based mixing matrices (avoiding vanishing gradients from decay-based $A_k$) is architecturally informative and forward-looking.

- **Substantial experimental effort.** Over 3,000 runs and approximately 20,000 GPU hours represent a thorough investigation at academic scale, with code made publicly available.

## Weaknesses

### Fatal
None

### Major

1. **Central thesis overclaims relative to evidence.** The paper states in Section 1: "Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics." This claim is about the architectures *in general*, but evidence comes exclusively from two synthetic benchmarks (MQAR and copying) at small scale (1–2 layers, up to 2048 hidden dim). The paper acknowledges in Section 8 that "our analysis is conducted on synthetic benchmarks," but the framing throughout—abstract, introduction, contributions, conclusion—treats findings as broadly generalizable. The paper cites Waleffe et al. (2024) as showing a downstream performance gap but does not verify whether learning rate tuning closes that gap in practice. Without any language modeling validation, the central thesis remains an interesting hypothesis rather than a supported conclusion. The word "mainly" is the crux: the evidence supports "in part" or "on these benchmarks," not "mainly."

2. **Only one optimization axis explored despite broad claims about "fundamental learnability."** The paper frames its findings as revealing "critical optimization instability" and "fundamental learnability properties," but only learning rate is varied. No other optimization hyperparameters are systematically tested: optimizer choice (only Adam), learning rate schedule (warmup, cosine decay), gradient clipping, initialization strategy, or normalization. The vanishing/exploding gradient hypothesis is invoked repeatedly (Sections 1, 7) but never directly measured—no gradient norm trajectories or loss landscape analyses are presented. This matters because, as the paper itself acknowledges by citing Zuchet & Orvieto (2024), SSM training dynamics depend on parameterization-specific gradient flow. The paper cannot distinguish between "SSMs have fundamentally brittle optimization" and "SSMs require different optimization recipes than those tested."

### Minor

1. **Induction head interpretation in Section 6 is speculative.** The paper observes a loss bump in 1-layer Transformers and interprets it as an "attempt to form induction heads." The paper appropriately hedges ("we hypothesize," italicized "attempts"), and acknowledges "a single-layer transformer lacks the expressivity needed to effectively leverage this mechanism." However, induction heads as defined by Olsson et al. (2022) are a two-layer circuit by construction. Without mechanistic analysis (examining attention patterns, probing representations during the bump), the identification of this loss bump with induction head formation—rather than any other phase transition—is unsupported. This is presented as a key contribution in the bullet points of Section 1.

2. **Width/depth scaling finding limited to 1–2 layers.** The claim that "recurrent models benefit most from increased width" (Figures 3–4) is tested only for MQAR up to 2 layers. Real-world SSMs use dozens of layers; scaling dynamics at that depth may differ. While the finding is internally valid, the paper should be more explicit about its limited scope.

3. **Copy task learning rate sensitivity (Figure 5) shown only for Mamba vs. Transformer.** Including other architectures (Hyena, DeltaNet, Mamba2) on this task would strengthen the claim that learning rate sensitivity is a general SSM phenomenon, not Mamba-specific. The MQAR results include these models, but the copying results do not.

### Trivial
None

## Nice-to-Haves
- Direct gradient flow analysis (gradient norm trajectories for SSMs vs. Transformers at different learning rates) would transform the learning rate sensitivity finding from symptom to mechanistically explained phenomenon.
- Testing simple optimization interventions (gradient clipping, learning rate warmup, different optimizers) to establish whether the narrow window can be widened, which would either support or refine the thesis.
- Even a small-scale language modeling experiment demonstrating learning rate sensitivity persists would dramatically strengthen the paper's generalizability claims.
- Loss landscape visualization to provide geometric intuition for the narrow optimal region.
- Mechanistic analysis of the loss bump in Section 6 (attention pattern visualization during the transition) to support or refute the induction head interpretation.

## Removed Points
These points are flagged to be removed, treat them with caution.

1. **Statistical methodology (5 seeds, max-min error bars):** Reviewer argued this is insufficient for claims about optimization instability. While standard deviations would be more informative, max-min from 5 seeds is common in the field, and the core finding (narrow vs. wide LR window) is visually unambiguous in Figure 1 — the gap between SSM and Transformer robustness spans orders of magnitude of learning rate. Removed as a field-standard practice.

2. **DeltaNet limited to dim ≤ 256:** The paper already acknowledges this implementation constraint in the Figure 7 caption. This is a practical limitation of the DeltaNet codebase, not a methodological flaw of the paper. Removed as already acknowledged.

3. **Missing connection to practical language modeling:** The reviewer argued this is the "most important omission." While true that language modeling validation would strengthen the paper, demanding it changes the paper's scope from synthetic benchmark analysis to end-to-end architectural comparison. This concern is already captured in Major weakness #1 (overclaiming) and the Nice-to-Haves. Removing as a separate weakness to avoid duplication.

## Novel Insights
The paper's most novel insight is that prior expressivity comparisons between SSMs and Transformers on MQAR are confounded by a dramatic asymmetry in learning rate sensitivity — a simple observation with significant implications for how the community should interpret synthetic benchmark results. The convolution ablation (Table 2) establishing that 1-layer Mamba without conv1d ≈ 1-layer Transformer in performance is a clean mechanistic finding. The DeltaNet stability observation, connected to Householder-based mixing avoiding decay-induced vanishing gradients, is a forward-looking architectural insight.

## Suggestions
- Reframe the central thesis to match evidence scope: replace "mainly" with "in part" or explicitly scope to "on synthetic associative recall and copying benchmarks."
- Add gradient norm plots through training at different learning rates for SSMs vs. Transformers to directly support the vanishing gradient hypothesis.
- Test at least one additional optimizer or a simple intervention (gradient clipping, warmup) to probe whether learning rate sensitivity is fundamental or optimizer-specific.
- Expand Figure 5 (copy task) to include Hyena, Mamba2, and DeltaNet for consistency with MQAR analysis.
- Either add mechanistic analysis of the loss bump in Section 6 or reframe it as an unexplained phase transition rather than an induction head attempt.

## Score and Decision

### Calibration Anchors

| Anchor | Avg Score | Round | Comparison to paper under review |
|--------|-----------|-------|----------------------------------|
| `8QTpYC4smR.md` (LLM Survey) | 1.00 | R1 | Fundamentally different — a survey paper with no research contribution. Paper under review is far superior. |
| `Uj0h13lVrR.md` (KL Div GFlowNets) | 1.00 | R1 | Broken/unsupported paper. Not comparable. |
| `5kMwiMnUip.md` (Nemesis Jailbreaking) | 1.40 | R1 | Minimal contribution. Not comparable. |
| `nSDOkm0SKo.md` (Financial NN) | 1.00 | R1 | Hypothetical scenario, no real contribution. Not comparable. |
| `VtP7CamOR5.md` (Mamba Neural Operator) | 3.00 | R1 | SSM-related but proposing a new model with more fundamental issues. Paper under review has cleaner empirical methodology. |
| `7eYmijcuqO.md` (RNN Dynamics) | 3.00 | R1 | RNN training dynamics on synthetic tasks, but more limited scope and findings. Paper under review is substantially stronger. |
| `q541p2YLt2.md` (Transformer Training Instability) | 2.50 | R1 | Transformer training instability study, but less thorough. Paper under review is much more rigorous. |
| `kkVTeMvC9D.md` (Training Jacobian) | 3.40 | R1 | Different focus (gradient descent geometry). Paper under review has more actionable findings. |
| `b5lXUwZiD3.md` (Transformer HMM Limitations) | 5.25 | R1 | Very similar spirit — empirical study of Transformer vs. RNN on synthetic tasks. Rejected for similar concerns (synthetic-only, limited scope). Paper under review is comparable in scope but has more diverse findings (convolution ablation, DeltaNet). |
| `XZhpS5Imzx.md` (Transformers ICL LDS) | 4.00 | R1 | Empirical study of Transformers on synthetic dynamics. Paper under review has broader scope. |
| `BwG8hwohU4.md` (StableSSM) | 5.33 | R1 | Addresses SSM training stability with reparameterization theory. Paper under review lacks theoretical depth but has broader empirical coverage. |
| `iVy7aRMb0K.md` (Mimetic Initialization) | 4.50 | R1 | Most directly comparable — argues SSM recall problems are training-based, not capacity-based. Rejected for limited novelty, scope restricted to Mamba, and no pretraining validation. Paper under review is broader and has cleaner findings, but shares the lack of language modeling validation. |
| `QFgbJOYJSE.md` (SSMs Provably Comparable) | 5.75 | R1 | Theoretical + empirical SSM-Transformer comparison. Has formal proofs the paper under review lacks. Accepted. |
| `pymXpl4qvi.md` (SSM Bottlenecks - Recency/Over-smoothing) | 6.00 | R1 | Accepted study of SSM limitations with theoretical backing + empirics. Paper under review has broader empirical scope but no theory. |
| `EGjvMcKrrl.md` (SSM Generalization Analysis) | 6.00 | R1 | Theoretical generalization bounds for SSMs with practical optimization improvements. More complete contribution. |
| `sZJNkorXMk.md` (Autocorrelation SSM Init) | 6.67 | R1 | Accepted with theory + practice. More complete contribution than paper under review. |
| `GRMfXcAAFh.md` (Oscillatory SSM) | 8.00 | R1 | Proposes new SSM architecture with theory (universality proof) + strong empirics. Much more complete contribution. |
| `PdaPky8MUn.md` (Never Train from Scratch) | 8.00 | R1 | Very related spirit (fair comparison requires proper training), but proposes SPT solution, validates on established benchmarks (LRA), demonstrates effectiveness broadly. More complete. |
| `d8w0pmvXbZ.md` (Small-scale Proxies) | 8.00 | R1 | Gold standard for training instability study: explores multiple optimization axes (warmup, weight decay, μParam), validates on real data (C4), directly measures instabilities. Paper under review's methodology falls significantly short. |

### Bracket and Scoring Rationale

**Round 1 bracket: 5.0–6.0**

The paper is clearly above the 3.0–4.5 reject range: it has a genuine, reproducible finding, substantial experimental effort, and clean ablations. It is better than `iVy7aRMb0K` (4.50, rejected) due to broader scope and more diverse findings. It is comparable to `b5lXUwZiD3` (5.25, rejected) — both are empirical studies on synthetic tasks with similar overclaiming concerns.

However, it falls short of the accepted papers at 6.0+ (`pymXpl4qvi`, `EGjvMcKrrl`, `sZJNkorXMk`), which all combine theoretical analysis with empirical findings. The paper under review is purely empirical and explores only one optimization axis while making broad claims about "fundamental learnability." Compared to `d8w0pmvXbZ` (8.00), which is the benchmark for training instability studies, the paper's methodology is notably narrower (single hyperparameter, synthetic-only, no gradient analysis).

The core learning rate sensitivity finding is valuable and the recontextualization of prior work is useful, but the gap between the scope of claims and the scope of evidence is the paper's primary liability. This places it in the 5.0–5.5 range: a useful empirical study that falls slightly short of the acceptance threshold due to overclaiming and limited methodological depth.

**Final Score: 5.5**

The paper makes a genuine empirical contribution — documenting SSM learning rate sensitivity and recontextualizing prior benchmarking results — that is actionable and well-supported within its scope. However, the central thesis ("mainly because of optimization dynamics") overclaims relative to the evidence (two synthetic benchmarks, one hyperparameter axis, no gradient analysis), and the lack of any language modeling validation or exploration of optimization interventions leaves the paper's broader implications unresolved. It is a solid but incomplete empirical study.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>