Now let me compose the final review. Let me first record the draft items with proper structure, then write the final review.

Based on my analysis:

**Bracket from Round 1:** The paper sits comfortably in the 5.0-7.0 range - above RotRNN (4.00) and Feature-Sequence Twist (2.50), comparable to TS-LIF (6.00), ProbeGen (6.00), and Neural Functions (7.00). The weighted items show strong positive weights for all four strengths (8.45-11.83), while the most negative weaknesses are ICL scale (-1.29), ETT baselines (-0.96), and DSR baselines (-0.14). These are all mild negatives compared to RotRNN's -4.61 and Feature-Sequence Twist's -5.97.

**Narrowing:** The paper is most comparable to ProbeGen (6.00) and TS-LIF (6.00) in terms of novelty and evaluation thoroughness. However, the SCP2 factual error is a mark against it that these comparable papers don't have. The core idea is more novel than either ProbeGen or TS-LIF, but the evaluation has more issues. A fair score would be around 5.5-6.0.

Let me write the final review now.

Here's my assessment of the anchors:

| Anchor | Score | Round | Itemized | Comparison |
|--------|-------|-------|----------|------------|
| Feature-Seq Twist (I1484gDBr4) | 2.50 | R1 | Yes | Much weaker paper; our idea is more novel and evaluation more thorough |
| RotRNN (z6qmomJW91) | 4.00 | R1 | Yes | Similar type (linear RNN variant) but weaker results and less novel |
| TS-LIF (rDe9yQQYKt) | 6.00 | R1 | Yes | Comparable novelty, cleaner evaluation, no factual errors |
| Gradient-free RNN (vcJiPLeC48) | 6.00 | R1/R2 | Yes | Similar theme, comparable quality, but less broad evaluation |
| ProbeGen (XoYdD3m0mv) | 6.00 | R2 | Yes | Same weight-space learning domain, similar evaluation quality |
| Neural Functions (GCH5leffZp) | 7.00 | R2 | Yes | Stronger clarity, cleaner claims, narrower scope |
| Mamba (AL1fq05o7H) | 6.25 | R2 | No | More impactful architecture, mixed reviews |
| HadamRNN (amOpepqmSl) | 6.00 | R2 | No | Similar RNN architecture paper |
| HMM+SSM (EAkjVCtRO2) | 6.00 | R2 | No | Time series forecasting focus |**MY FINAL SCORE: <score>6.0</score>**
**MY FINAL DECISION: <decision>Accept</decision>**

---

## Summary

This paper introduces WARP (Weight-space Adaptive Recurrent Prediction), a novel sequence model that replaces the hidden state of a linear RNN with the flattened weights of an auxiliary MLP. The hidden state θ_t is updated via a learned linear recurrence on input differences (θ_t = Aθ_{t-1} + BΔx_t), and then self-decoded by reconstituting the MLP to produce outputs. This formulation unifies weight-space learning with linear recurrence, enabling non-linear decoding while retaining the parallelizability of linear RNNs. The paper evaluates WARP across image completion, multivariate time series forecasting, dynamical system reconstruction, classification, and in-context learning.

## Strengths

- **Genuinely novel core idea** (weight=8.45). Treating the parameters of an auxiliary MLP as the recurrent hidden state — and updating them via a learned linear recurrence on input differences — is a creative synthesis of weight-space learning and linear RNNs. The self-decoding property (θ_t is both hidden state and decoder parameters) distinguishes WARP from standard RNNs where the hidden state and decoder weights are separate.

- **Image completion results are competitive with proper baselines** (weight=11.83). Table 1 compares WARP against GRU, LSTM, S4, and ConvCNP at matched parameter counts (~1.68M for MNIST, ~2M for CelebA). WARP achieves the best or tied-best MSE across all context lengths on MNIST and clearly dominates on CelebA with dramatically better BPD (e.g., BPD -0.162 vs S4 not even competitive). This is the strongest experimental evidence in the paper.

- **WARP-Phys demonstrates valuable flexibility** (weight=10.00). Embedding known physical structure (sin(2πτ + φ̂)) into the root network and showing large improvements on MSD and SINE is a clean demonstration of what the weight-space formulation enables that standard RNNs cannot easily replicate.

- **Broad evaluation scope** (weight=9.47). The paper tests across pixel-by-pixel image completion, multivariate forecasting (ETT, PEMS08), dynamical system reconstruction, multivariate classification (6 UEA datasets), and in-context learning. This breadth shows the authors are thinking about generality rather than cherry-picking one favorable setting.

## Weaknesses

### Fatal
None.

### Major

- **Factual error in the SCP2 state-of-the-art claim (line 243).** The paper states it "establish[es] new state-of-the-art accuracies on the SCP2 Ethanol and Heartbeat datasets." However, in the paper's own Table 4, FACTS achieves 70.3% on SCP2 while WARP achieves 57.89% — WARP is 3rd place on SCP2, not state-of-the-art. The claim is correct for Ethanol (36.49, best) and Heartbeat (80.65, best), but including SCP2 is an unambiguous factual error that undermines the credibility of the reported results. This must be corrected.

- **ETT evaluation (Figure 3b) uses only GRU and LSTM as baselines** — architectures that are ~25 years old. Modern SSMs (S4, Mamba, S5, Mamba-2), linear attention models, and Transformer-based time series forecasters (PatchTST, TimesNet, etc.) are absent. The paper cites using TSLib (line 167), a library that contains modern methods, making this omission conspicuous. Without contemporary baselines, the claim of "superiority" (line 169) on ETT is uninformative.

- **PEMS08 comparison (Table 2) is insufficiently controlled.** The baseline numbers (GMAN, D²STGNN, STDCN) are taken from another paper [62], so data splits, preprocessing, and evaluation protocols are not independently verified to be identical. WARP uses a non-causal convolution preprocessing step (line 180) that provides access to future information — a structural advantage over the causal GNN baselines. The ~50% MAE reduction (6.59 vs 13.45) is suspiciously large for a cross-paper comparison and likely reflects protocol differences rather than genuine model superiority.

- **The A matrix creates a significant scaling bottleneck** that conflicts with the paper's framing. A ∈ ℝ^{D_θ × D_θ} where D_θ is the total parameter count of the root MLP. For the 1.68M-parameter MNIST model, A alone accounts for virtually all parameters, meaning the root MLP has roughly D_θ ≈ 1296 parameters (~35 hidden units per layer). The paper acknowledges this in Section 4.2 ("the size of the matrix A limits scaling to huge root neural networks") but the abstract and introduction describe the hidden state as "high-resolution" and "infinite-dimensional," which is misleading given how tiny the actual MLP must be.

### Minor

- **Dynamical system reconstruction baselines (Table 3) are weak.** Only GRU, LSTM, and a vanilla Transformer are included. Modern SSMs (S4, Mamba), Neural ODEs, and NCDEs — all natural competitors for a DSR benchmark in 2025/2026 — are absent.

- **The "gradient-free adaptation" framing overstates what is standard behavior.** During test-time, every RNN updates its hidden state without gradients — this is simply the forward pass. WARP's genuine novelty is that the hidden state IS the decoder weights (unlike standard RNNs where decoder parameters are fixed), but framing this as "gradient-free adaptation" as if it were a special capability inflates a standard property of recurrent computation.

- **The in-context learning experiment is very small-scale** (N+1=32 total steps, D_s ∈ {2, 8}). The existing ICL literature on linear regression typically uses much larger N and higher dimensions. This demonstration does not establish WARP as a general ICL architecture.

- **The WARP-Phys "10x" framing compares a model given the correct physical formula against a model without it.** While this validly demonstrates architectural flexibility, the "more than 10x" headline (abstract) could mislead readers into thinking this is a general-purpose improvement rather than an expected result of hardcoding the correct dynamics.

### Trivial
None.

## Nice-to-Haves

- Explore low-rank, diagonal, or block-diagonal parametrizations of A (as the paper mentions in Section 4.2) to enable larger root MLPs and test whether performance scales.
- Add at least one recent SSM or Transformer-based forecaster to the ETT experiments.
- Demonstrate genuine test-time adaptation under distribution shift to substantiate the "gradient-free adaptation" narrative.
- Report wall-clock times and memory usage, particularly given the D_θ² cost of the recurrence.

## Removed Points

These points were flagged for removal; they are listed for completeness but should be treated with caution:

- Critic's claim that the A matrix problem is "fatal" or "structural" to the degree of invalidating the paper — Demoted from Fatal to Major because the paper explicitly acknowledges the limitation (Sec 4.2) and suggests future mitigations. The root MLP, while small, still provides non-linear decoding that standard linear RNNs lack, so the core contribution is not invalidated.

- Critic's claim that "no computational complexity analysis" is provided — The paper references Appendix E.3 for wall-clock and memory benchmarks; since appendix sections are stripped by the parser, this concern cannot be verified.

- Critic's claim that Neural ODEs and NCDEs are missing from all experiments — NCDEs and NRDEs actually appear in Table 4 (classification), so this claim is partially incorrect.

- Critic's claim about "Variance of results" being uneven — Classification results have stds; image completion reports best-of-three without stds. This is uneven but common practice in this literature and not a decisive weakness.

- Critic's speculation about the SCP2 claim being misread — VERIFIED: the paper indeed claims SOTA on SCP2 when its own table shows WARP is 3rd. This is a real factual error, not a misreading.

- Critic's point about PEMS08 being "staged, not genuinely informative" — The concern is valid, but the paper is transparent about the non-causal preprocessing and the cross-paper nature of the baselines. Modified the criticism to be more measured.

- Critic's "Missing related works" criticism — Removed as per rules.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct the SCP2 factual error** — Change line 243 to say that WARP achieves SOTA on Ethanol and Heartbeat, and is competitive (3rd) on SCP2.
2. **Strengthen ETT baselines** — Add at least S4 or Mamba (or another modern SSM) to the ETT comparison. Since the paper uses TSLib, these should be readily available.
3. **Add explicit caveats for PEMS08** — Clearly state that baseline numbers are from a different paper, the non-causal preprocessing is an advantage, and the results should be interpreted with caution.
4. **Consider a diagonal/low-rank A** — Even a small-scale ablation showing whether a diagonal A maintains performance would substantially address the scaling concern and strengthen the paper.
5. **Rethink the "gradient-free adaptation" framing** — Position this as "the decoder is updated via the recurrence at test time" rather than implying it is a unique capability.

## Calibration Anchors

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| I1484gDBr4 (Feature-Seq Twist) | 2.50 | R1 | Yes | Much weaker paper; incremental idea, poor writing. Our paper is substantially more novel. |
| z6qmomJW91 (RotRNN) | 4.00 | R1 | Yes | Similar type (linear RNN variant) but comparably limited evaluation. Our idea is more novel. |
| rDe9yQQYKt (TS-LIF) | 6.00 | R1 | Yes | Similar novelty level, cleaner evaluation, no factual errors. Our paper has broader scope. |
| vcJiPLeC48 (Gradient-free RNN) | 6.00 | R1/R2 | Yes | Similar attempt at gradient-free recurrent computation. Comparable quality. |
| XoYdD3m0mv (ProbeGen) | 6.00 | R2 | Yes | Weight-space learning domain. Similar evaluation quality and limitations. |
| GCH5leffZp (Neural Functions) | 7.00 | R2 | Yes | Stronger clarity and cleaner claims, but narrower scope. |
| AL1fq05o7H (Mamba) | 6.25 | R2 | No | More impactful architecture with broader evaluation. |
| amOpepqmSl (HadamRNN) | 6.00 | R2 | No | Comparable RNN architecture paper. |

**Round-1 bracket**: 5.0–7.0 (well above RotRNN at 4.00, comparable to TS-LIF at 6.00 and ProbeGen at 6.00)

**Round-2 narrowing**: Compared weighted items against ProbeGen (6.00) and Neural Functions (7.00). Our paper shares ProbeGen's limitation of imperfect evaluation but has a more novel core idea. Our weighted strengths (8.45–11.83) are strong, and the most negative weakness weights are mild (-0.14 to -1.29). However, the SCP2 factual error is a concrete flaw that ProbeGen and TS-LIF do not have. This places the paper at 6.0 — solid borderline accept territory — reflecting a genuinely novel contribution held back by clear but addressable evaluation issues.