Now I have sufficient information. Let me produce the final consolidated review.

## Summary

This paper introduces WARP (Weight-space Adaptive Recurrent Prediction), a novel family of sequence models where the hidden state of a linear RNN is the flattened weights and biases of an MLP, which is then decoded by reconstituting and evaluating that MLP on a coordinate system. This architectural idea — using weight-space as the hidden state representation — is genuinely creative and distinct from existing linear RNNs (S4, LRU, Mamba). The paper evaluates WARP across image completion, time series forecasting, dynamical system reconstruction, multivariate time series classification, and in-context learning. A physics-informed variant (WARP-Phys) achieves order-of-magnitude improvements on dynamical system reconstruction tasks.

## Strengths

- **Genuinely novel architectural idea (Section 2.2, Eq. 1).** Treating the hidden state of a linear RNN as the flattened weights of an MLP, then decoding via that MLP, is creative and distinct from existing work. Standard linear RNNs maintain a low-dimensional hidden state with a separate output projection; WARP makes the hidden state *be* the decoder parameters, reintroducing non-linear expressivity while preserving the parallelizable linear recurrence. This is not an incremental modification of an existing architecture.

- **Input-difference driving signal (Eq. 1).** Using Δxₜ rather than xₜ is well-motivated by the Neural CDE literature (Kidger et al.) and carries intuitive appeal for continual learning and adaptation. With identity-initialized A and zero-initialized B, the recurrence θₜ = θ₀ + B(xₜ − x₀) ensures weight updates are proportional to input changes and the weights do not diverge early in training.

- **WARP-Phys variant (Section 3.2).** A clean demonstration of the method's strength: because the hidden state is literally the weights of a function approximator, injecting physical priors is as simple as designing the root network's forward pass. Achieves an order-of-magnitude improvement on MSD (0.03 MSE vs WARP's 0.94 and GRU's 1.43). This is a genuinely impressive result.

- **Broad experimental validation.** The paper evaluates across image completion (MNIST, CelebA), time series forecasting (ETT, PEMS08), dynamical system reconstruction (MSD, MSD-Zero, LV, SINE), classification (6 UEA datasets), and in-context learning. This breadth is commendable for a first paper proposing a new architecture.

- **Acknowledged limitations (Section 4.2).** The paper transparently discusses the A matrix scaling bottleneck, lack of language modality experiments, and struggles on extremely long sequences, providing concrete directions for future work (low-rank parameterizations, block-diagonal decompositions).

## Weaknesses

### Fatal
None.

### Major

- **ETT experiment compares only against weak baselines (Section 3.1, Fig 3b).** The ETT forecasting results compare WARP only against GRU and LSTM — two architectures introduced in 1997 and 2014. The main competitors for a new linear RNN architecture are modern SSMs (S4, Mamba, S6, LRU), none of which appear in this comparison. This is the model's strongest negative-weighted item, as it limits the informativeness of a key forecasting experiment. Adding S4 and Mamba as baselines would be necessary to properly situate WARP among contemporary sequence models.

- **PEMS08 non-causal preprocessing creates evaluation uncertainty (Section 3.1, Table 2).** The paper reports a remarkable 2× improvement over graph-aware baselines (MAE 6.59 vs STDCN's 13.45) but states the input is preprocessed with a "non-causal convolution." For a forecasting task predicting the next 12 steps from the past 12, non-causal preprocessing is unusual and requires explicit clarification that no future information leaks across the input/target boundary. The paper flags the setting as "significantly differ[ent] from the setting in Fig. 2" but does not resolve this concern in the main text. The result cannot be properly assessed without this clarification.

- **In-context learning experiment is weak (Section 3.4).** The ICL setup uses a synthetic toy task (random keys mapped through a shared linear vector w) with end-to-end training on that single task type. This does not convincingly demonstrate meta-learning-based ICL in the sense established by von Oswald et al. (2023), where a model learns to solve *new* regression problems from context alone. Here, WARP is trained on one type of linear mapping and evaluated on the same type. The experiment provides limited evidence for the ICL claim.

### Minor

- **Overclaimed classification framing (Abstract, Section 3.3, Table 4).** The abstract claims WARP "matches or surpasses state-of-the-art baselines" and features "top three in 4 out of 6" datasets. While technically true, WARP is 24 points behind SOTA on EigenWorms (70.93 vs LinOSS's 95.0) — the longest sequence in the benchmark by far (17,984 steps). The two datasets where WARP performs worst are the longest ones, an informative pattern that the current framing downplays. The paper's own limitations section acknowledges this, but the abstract does not reflect this nuance.

- **No standard deviations for PEMS08 result (Table 2).** While other tables report error bars, the headline PEMS08 result reports only point estimates (MAE 6.59, RMSE 10.10). For a result claiming a 2× improvement over published SOTA, showing variance across runs is important.

### Trivial

- **"Infinite-dimensional" hidden state claim (Conclusion, line 283).** θₜ is explicitly finite-dimensional (ℝ^{D_θ}). The claim that evaluating the decoded MLP at any τ yields "infinite-dimensional" states is misleading without qualification — this property is shared by any continuous-time model.

## Nice-to-Haves

- The paper mentions a self-decoding parameter savings (Section 2.2). While technically correct (the decoder parameters ARE the hidden state), it would strengthen the paper to provide a total parameter count comparison rather than focusing on decoder-specific savings.
- A comparison against Mamba/S6 on PEMS08 (non-graph-aware baselines) would make the traffic result more interpretable.
- An ablation varying D_θ (root network size) would help readers understand the performance/computation trade-off.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Gradient-free adaptation framing (Harsh Critic's Critical Issue 5).** The reviewer argued the term overstates novelty since all RNNs update hidden states without gradients. However, in WARP the hidden state IS the function approximator's weights, so updating it directly adapts the function — a distinction from standard RNNs. The claim is defensible as stated; this is a framing preference, not a genuine weakness.
- **WARP-Phys on LV (Harsh Critic's concern).** The paper clearly explains why WARP-Phys is incompatible with the repeat-copy protocol (artificial discontinuities in temporal sequences). This is a reasonable explanation, not a weakness.
- **S4 missing from ETT heatmap (Harsh Critic's concern).** The reviewer misread the caption. S4 appears in Fig 3(a) for MNIST, not Fig 3(b) for ETT. The (valid) point about weak ETT baselines is captured above.
- **Self-decoding parameter savings (Harsh Critic).** The claim is technically correct; the savings refer to decoder-specific parameters, not total parameters. Not a substantive weakness.
- **Non-causal convolution appendix concern (partially).** The criticism that "the appendix is stripped, so this cannot be verified" is removed per parser rules. The core concern about non-causal preprocessing in a forecasting setting is retained as a Major weakness.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Clarify whether the PEMS08 non-causal convolution respects the temporal split between input and forecast windows, and provide an ablation with causal convolution or without any preprocessing.
2. Add modern SSM baselines (S4, Mamba, LRU) to the ETT comparison to properly situate WARP among contemporary sequence models.
3. Adopt a factored or diagonal parameterization of A (even as an ablation) to demonstrate a path beyond the quadratic scaling bottleneck.
4. Reframe the classification results to acknowledge the performance gap on long sequences (EigenWorms) rather than emphasizing only the top-3 count.
5. Report standard deviations for the PEMS08 result.
6. Either strengthen the ICL experiment with a meta-learning setup (training on multiple random regression tasks) or retract the ICL framing.

## Score and Decision

**Calibration analysis.** I compared the weighted items of this draft against several anchors retrieved from the human review corpus:

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| RotRNN | z6qmomJW91.md | 4.00 | 1 | Yes | Similar scope (new linear RNN architecture). RotRNN has tighter experiments but less novel architecture. WARP has broader validation but weaker baselines. |
| "Were RNNs All We Needed?" | GrmFFxGnOR.md | 5.00 | 1,2 | Yes | Similar framing (challenging established views). That paper had severe novelty concerns (-11.72, -9.49) but strong speed results. WARP's strongest weakness (-6.73 for ETT baselines) is less severe. |
| Deep Linear Probe Generators | XoYdD3m0mv.md | 6.00 | 1 | Yes | Weight-space learning paper. Clearer, more focused experiments. WARP is less polished but architecturally more creative. |
| Retentive Network | UU9Icwbhin.md | 4.75 | 2 | Yes | New architecture paper with overclaiming and weak baselines concerns. WARP has broader task diversity but smaller-scale experiments. |
| Linear RNN Feature-Sequence Twist | I1484gDBr4.md | 2.50 | 1 | Yes | Linear RNN paper with very weak experiments and insufficient contribution. WARP is clearly stronger. |

**Round 1 bracket:** [3.5, 5.5]. After comparing weighted items, the most damaging weaknesses (ETT weak baselines at -6.73, ICL at -4.57, PEMS08 at -4.13) place this paper below the cleaner ProbeGen (6.0) and RetNet (4.75), but above the clearly incremental LRNN paper (2.50). The genuinely novel architecture and WARP-Phys results (+4.84 strength) push it above RotRNN (4.00). The final score of **4.0** reflects a paper with a creative core idea and broad experiments that is held back by significant evaluation issues (ETT baselines, PEMS08 preprocessing uncertainty, ICL weakness) that prevent acceptance in the current form.

**Score:** 4.0 — Borderline reject. The paper has a genuinely creative and novel architectural idea, but the evaluation has notable gaps that need resolution before acceptance.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>