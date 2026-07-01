Now let me read the paper in chunks to verify the reviewer's claims.Now let me read the remaining parts of the paper, including the limitations and conclusions more carefully.Now I have all the information I need to draft the review. Let me submit the draft first.Now let me do calibration. Round 1 — Bracketing:Let me read some of the most relevant anchor papers in detail to calibrate my score.Now let me read one more anchor for comparison — the RotRNN paper (score 4.0):Now I have enough calibration data. Let me synthesize the final review.

## Summary
WARP proposes a novel recurrent architecture where the hidden state of a linear RNN is parametrized as the flattened weights and biases of an auxiliary MLP ("root network"), updated via a linear recurrence driven by input differences. Decoding is performed by running the MLP's non-linear forward pass, yielding "self-decoding" that reintroduces non-linearity while retaining parallelizable linear state transitions. A physics-informed variant (WARP-Phys) embeds domain-specific structure into the root network. The paper evaluates across image completion, time series forecasting, dynamical system reconstruction, classification, and in-context learning.

## Strengths
- **The core architectural idea is genuinely novel and well-motivated.** Parametrizing the hidden state as the weights of an auxiliary MLP that "self-decodes" via its own forward pass (Eq. 1, Section 2.2) is a creative resolution of the tension between linear-RNN efficiency and expressivity. The self-decoding property — where θ_t serves simultaneously as hidden state and decoder parameters — is elegant and parameter-efficient (line 78). This idea has no direct precedent in the cited literature.

- **WARP-Phys demonstrates a distinctive capability unavailable to competing architectures.** Because the hidden state is interpretable as network weights, domain-specific physical structure can be directly embedded into the root network's forward pass. The >10× improvement on MSD and MSD-Zero (Table 3: 0.03 vs. 0.94 MSE on MSD) is compelling evidence that this is not merely a theoretical advantage.

- **Classification results (Table 4) are credible and competitive.** Using a broad, contemporary baseline set (LRU, S5, Mamba, LinOSS, FACTS, Griffin, Log-NCDE, etc.), WARP achieves SOTA on Ethanol (36.49%) and Heartbeat (80.65%), and top-3 on most datasets. This is the experiment with the fairest comparison, and the results hold up.

- **The connection to fast weights and test-time training is clearly articulated** (Section 2.3, line 108), with the slow/fast weight distinction — A, B, φ updated by gradient descent vs. θ_t updated T-1 times by Eq. (1) — cleanly presented.

## Weaknesses

### Fatal
None

### Major
1. **PEMS08 result (Table 2) is implausibly large and insufficiently scrutinized.** WARP reports MAE 6.59 vs. 13.45 for the best published baseline — a >50% reduction on a mature benchmark. The paper explicitly states it uses a "non-causal convolution" for preprocessing (line 180), with details deferred to Appendix D. In a forecasting task, non-causal convolution accesses future time steps, which is a potential form of data leakage. The baselines (GMAN, D²STGNN, STDCN) are causal spatio-temporal graph methods. No ablation isolates the contribution of this preprocessing from the WARP architecture itself, making the headline result uninterpretable. A 50% improvement over SOTA on a mature benchmark demands this level of scrutiny.

2. **Weak and inconsistent baselines inflate WARP's apparent performance on key experiments.** The ETT experiment (Fig. 3b) compares only against GRU and LSTM — baselines well-known to be weak on this benchmark. Contemporary methods (PatchTST, DLinear, iTransformer, or modern SSMs) are absent. The DSR experiment (Table 3) compares against GRU, LSTM, and a HuggingFace Transformer — omitting more natural comparisons like Neural ODEs. Notably, the classification experiment (Table 4), which uses a comprehensive baseline set, yields more mixed results. This pattern — strongest claims against weakest baselines — undermines the paper's headline assertion of matching/surpassing SOTA.

3. **Reporting "top performing models across three runs" (line 149) is cherry-picking.** For image completion (Table 1), the paper explicitly selects the best of three runs rather than reporting mean ± std. This inflates results and creates an unfair comparison. The DSR experiments (Table 3) appropriately report mean ± std, making the inconsistency conspicuous and deliberate.

### Minor
1. **The "gradient-free adaptation" framing overstates the contribution.** The paper repeatedly claims "gradient-free adaptation" (Abstract, Section 1, Section 2.3, Section 4.1), but the operation θ_t = Aθ_{t-1} + BΔx_t is simply a linear RNN forward pass — every RNN updates its hidden state without computing gradients during inference. The novel aspect is the weight-space *interpretation*, not the absence of gradients. The TTT connection (Section 2.3) is stated but not demonstrated: TTT methods actually minimize a loss at test time, while WARP applies a fixed linear transformation.

2. **The A matrix creates a scalability bottleneck that is underplayed.** A ∈ ℝ^{D_θ × D_θ} is a full dense matrix with O(D_θ²) parameters and per-step computation, far worse than O(D_h) diagonal SSMs. While acknowledged in Section 4.2 (line 275), the paper's language elsewhere — "high-dimensional weight space," "infinite-dimensional RNN hidden states" (Section 4.3) — gives the opposite impression. In practice, the root network must remain tiny, directly limiting the expressivity that the paper's central argument depends on.

3. **Rhetorical overclaiming.** The abstract asserts WARP "redefine[s] sequence modeling" and constitutes "a transformative paradigm for adaptive machine intelligence." Section 4.3 claims the work leads "a step further towards human-level artificial intelligence." These are not commensurate with a new RNN architecture showing promising but mixed results on moderate-scale benchmarks. This undermines credibility.

4. **WARP-Phys has limited applicability.** It is inapplicable to Lotka-Volterra (marked ✗ in Table 3), indicating it requires precise knowledge of the governing functional form. While this is a natural limitation, it constrains the generality of what is arguably the paper's strongest practical contribution.

### Trivial
None noted.

## Nice-to-Haves
- Ablation isolating the contribution of input differences (Δx_t vs. x_t) in the discrete-time setting — a central architectural choice (Section 2.2) whose benefit is not empirically verified in the main text.
- Characterization of how performance scales with root network size (D_θ), turning the acknowledged A matrix limitation into a rigorous empirical study.
- Exploration of intermediate physical priors (partial structural knowledge, symmetry constraints) for WARP-Phys beyond full functional form embedding.
- Sensitivity analysis for the coordinate system τ — a significant task-specific design choice that the paper does not analyze.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **CelebA BPD anomalies in baselines.** The reviewer noted GRU BPD of 24.14 (L=100) and ConvCNP BPD increasing dramatically with context (1.498→39.91→248.1). While unusual, this may reflect genuine baseline instability or variance, and does not directly invalidate WARP's own results.
- **Missing p_forcing values and D_θ values.** These are reproducibility nitpicks about undisclosed hyperparameters and architecture sizes, likely present in the appendix.
- **ICL cumulative sum preprocessing.** The cumulative sum transformation (line 247) is clearly described and motivated in the paper; calling it "non-trivial" is an overstatement. The ICL demonstration is narrow but functional.
- **DSR baselines should include Neural ODEs.** While natural, this is a baseline-expansion request that goes beyond the paper's stated comparison framework. The paper compares against established recurrent baselines, which is its stated scope.

## Novel Insights
The core insight — that the hidden state of a linear RNN can be meaningfully interpreted as the weights of an auxiliary neural network, enabling physics-informed decoding and non-linear self-decoding while preserving linear parallelizability — is genuinely novel. The WARP-Phys extension, which embeds known physical structure into the root network, represents a distinctive capability not easily available in other sequence model families. The observation that input differences drive weight updates (analogous to synaptic plasticity) is a suggestive connection, though more speculative.

## Suggestions
- **Add contemporary baselines to ETT and PEMS08.** Even 2-3 modern methods (e.g., PatchTST, DLinear, a modern SSM) would dramatically clarify where WARP actually stands on forecasting.
- **Ablate the non-causal convolution on PEMS08** to disentangle preprocessing gains from architectural gains. This is essential for credibility of the headline result.
- **Report mean ± std consistently** across all experiments, including image completion. Replace "top performing models across three runs" with standard statistical reporting.
- **Tone down rhetorical claims** to match the evidence. The contribution is real; overclaiming undermines it.
- **Report D_θ and A matrix sizes** for each experiment so readers can assess practical expressivity.

## Score and Decision

**Anchor papers and comparisons:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| nSDOkm0SKo (Financial markets NN) | 1.0 | R1 | Fundamentally flawed; WARP is far superior |
| gwZ90hFSL2 (Cross-lingual robots) | 1.0 | R1 | Not a real ML contribution; irrelevant comparison |
| 8QTpYC4smR (LLM survey) | 1.0 | R1 | Survey, not a contribution; WARP is far superior |
| P49gSPmrvN (Scientific discourse UMAP) | 1.0 | R1 | Trivial method; WARP is far superior |
| I1484gDBr4 (Linear RNN Feature-Sequence Twist) | 2.5 | R1 | Incremental, poor writing, limited experiments; WARP is substantially more novel and better executed |
| 4ymHtDAlBv (FSFC RNN) | 2.33 | R1 | Limited novelty and experiments; WARP is clearly stronger |
| 7eYmijcuqO (RNN dynamics/timed automata) | 3.0 | R1 | Narrow theoretical focus; WARP has broader contribution |
| fnO5h1CFyh (Hebbian temporal memory) | 3.0 | R1 | Different approach; less novel than WARP |
| HEcbGXzIHK (Episodic Memory Theory for RNNs) | 4.25 | R1 | Interesting theory but limited empirical validation; comparable execution issues to WARP |
| z6qmomJW91 (RotRNN) | 4.0 | R1 | Limited novelty (close to LRU), weak results; WARP has more distinctive contribution |
| GrmFFxGnOR (Were RNNs All We Needed?) | 5.0 | R1 | Novel simplification but prior work overlap, limited scale; comparable to WARP in novelty but WARP has more methodological concerns |
| iVy7aRMb0K (Mimetic Init for SSMs) | 4.5 | R1 | Focused contribution with clear experiments; similar caliber to WARP |
| vcJiPLeC48 (Gradient-free training of RNNs) | 6.0 | R1 | Interesting idea with clarity issues; WARP has more novel core idea but more experimental concerns |
| amOpepqmSl (HadamRNN) | 6.0 | R1 | Focused, correct contribution; WARP is more ambitious but less rigorous |
| yC2waD70Vj (Inverse Approx Theory for RNNs) | 7.25 | R1 | Strong theoretical work; WARP lacks comparable rigor |
| GRMfXcAAFh (LinOSS) | 8.0 | R1 | Strong theory + strong experiments + broad fair baselines; WARP is far below this standard |
| PdaPky8MUn (Never Train from Scratch) | 8.0 | R1 | Rigorous methodology, fair comparisons; WARP's execution falls well short |
| cmfyMV45XO (Feedback Neural ODEs) | 8.0 | R1 | Strong contribution with theoretical backing; WARP doesn't match this quality |

**Round 1 Bracket:** 4.0–5.5

**Reasoning:** WARP's core idea is more novel and distinctive than the 3.0–4.0 papers (RotRNN, RNN dynamics), which tend to be incremental or narrow. It clearly sits above the 2.5 paper (Feature-Sequence Twist). However, WARP falls well short of the 6.0+ papers in experimental rigor and methodological soundness. The three major weaknesses (potentially confounded PEMS08, cherry-picked reporting, systematically weak baselines on key experiments) are more concerning than the issues in "Were RNNs All We Needed?" (5.0), which had prior work overlap but cleaner methodology. WARP's novel idea pushes it above 4.0, but its execution gaps prevent it from reaching 6.0. The classification experiment (Table 4) is the most credible, showing competitive but not dominant results.

**Final calibrated score: 4.5**

The paper presents a genuinely novel architectural idea with the weight-space hidden state and a distinctive WARP-Phys extension. However, three major methodological issues — a potentially confounded headline result (PEMS08), systematically weak baselines on key experiments (ETT, DSR), and cherry-picked reporting (image completion) — create a substantial gap between the paper's claims and its evidence. The classification experiment, which uses fair baselines, shows competitiveness but not the dominance claimed elsewhere. The overblown rhetoric further undermines credibility. With contemporary baselines, proper statistical reporting, and a PEMS08 ablation, this could be a strong paper. As written, the evidential base does not support the claims.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>