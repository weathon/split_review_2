Now let me read the remaining key sections to verify specific claims about the theoretical analysis and experiments.Now I have a thorough understanding of the paper. Let me draft the review.Now let me perform calibration. Round 1 — Bracketing:Let me read a few closely comparable anchors to calibrate properly.Now I have sufficient calibration data. Let me form my bracket and write the final review.

**Round 1 Bracket:**
Based on the anchors, the paper sits in the **4.5–6.0** range. It has a cleaner core idea than the rejected ZO papers (4.0–4.75) and is comparable to the accepted ZO+quantization paper (5.8), but its missing QLoRA comparison and narrow evaluation are significant gaps. It's clearly weaker than LOZO (7.0) which has stronger theory and broader evaluation. Initial bracket: **4.5–6.0**.

Now let me write the final consolidated review.

## Summary
QZO (Quantized Zeroth-Order Optimization) proposes perturbing continuous quantization scale parameters—rather than discrete quantized weights—for zeroth-order gradient estimation, enabling memory-efficient fine-tuning of quantized LLMs. Paired with a directional derivative clipping (DDC) stabilization technique, QZO achieves 18× memory reduction over AdamW and ~3× over MeZO, demonstrating results on OPT-6.7B, Llama-2-7B, Llama-3.1-8B (4-bit), and Llama-2-13B (2-bit) across five NLP benchmarks.

## Strengths

- **Clean, novel core idea.** Decomposing θ = Δ ⊙ θ̄ and perturbing only the continuous quantization scales Δ (Definition 3.3, Eq. 5) is a genuinely elegant solution to the incompatibility between zeroth-order perturbation and discrete weight representations. This is not a trivial engineering trick—it fundamentally rethinks how ZO optimization interfaces with quantization.

- **Orthogonality to quantization methods demonstrated empirically.** QZO works with both scalar-based GPTQ (4-bit, Table 1) and codebook-based AQLM (2-bit, Table 3), confirming plug-and-play compatibility. This is practically valuable and non-trivially achieved versus ZO-signSGD variants that require re-quantization per step (Section 2).

- **Memory reduction is substantial and well-documented.** Figure 1 and Tables 1–2 show 18× reduction vs AdamW and ~3× vs MeZO with consistent methodology (peak VRAM at batch size 1). Enabling Llama-2-13B fine-tuning within 5.78GB on a single 24GB GPU (Table 3) is a concrete, verifiable achievement.

- **DDC addresses a genuine, demonstrated failure mode.** Figure 2 shows training collapse at step 22 without DDC (NaN loss), and Figure 3 demonstrates robustness across clipping thresholds C ≥ 75. This is empirically grounded, not hypothetical.

## Weaknesses

### Fatal
None.

### Major

- **Missing QLoRA comparison.** QLoRA (Dettmers et al., 2023) is the dominant method for fine-tuning quantized LLMs and is cited in the references but never experimentally compared. Table 2 reveals QZO trains only ~50M parameters (<1% of the model), making it effectively a parameter-efficient method. The natural comparison class therefore includes QLoRA and other PEFT methods. Without this comparison, the reader cannot assess whether QZO's extreme memory savings come at an acceptable accuracy cost relative to the established approach. The paper acknowledges QZO sometimes lags fine-tuning by 5–8+ points (e.g., OPT-6.7B SST-2: 87.6 vs 95.4 in Table 1), but we cannot tell how this compares to QLoRA. This is the single most important missing piece of evidence for evaluating QZO's practical contribution.

- **QZO's nature as a parameter-efficient method is not acknowledged or fairly compared.** Table 2 shows QZO trains 5.03×10⁷ parameters vs 6.65×10⁹ for MeZO and fine-tuning—a 130× difference. The paper's Section 4.2 mentions this ("QZO uses only about 1% of the trainable parameters") but does not discuss its implications: QZO operates in a fundamentally different regime than MeZO, and the comparison framework should reflect this. The paper's framing implies QZO is comparable to full-model ZO optimization, obscuring its true positioning.

### Minor

- **Narrow evaluation scope.** Only five NLP tasks (SST-2, RTE, CB, BoolQ, SQuAD) from MeZO's evaluation with 1,000 training examples each. While following MeZO's setup is reasonable, more modern/challenging benchmarks (MMLU, instruction-following) would substantially strengthen confidence in QZO's generality, especially given the evolving landscape since MeZO's publication.

- **No variance reporting.** No error bars or confidence intervals are reported anywhere despite the inherent stochasticity of zeroth-order methods (random perturbation vectors z, mini-batch sampling). This makes it difficult to assess the reliability of the reported results.

- **SGD used as fine-tuning upper bound.** Footnote 2 states fine-tuning uses SGD "due to limited budget." Since AdamW typically outperforms SGD, this artificially compresses the gap between QZO and true full fine-tuning, making QZO's relative performance appear better than it may be.

- **Theorem 1's unbiasedness claim is non-trivial and under-specified in the main text.** The directional derivative d = [L(Δ+εz) − L(Δ−εz)]/(2ε) is a function of z, and clipping it creates a z-dependent nonlinear coupling: E[clip(d(z))·z] ≠ E[d(z)·z] in general. The variance reduction guarantee (Eq. 8 → line 122) depends critically on this claim holding. The proof exists in Appendix A, but the main text states the result without qualifying conditions, which weakens reader confidence in the theoretical contribution. (Demoted from the harsh reviewer's "structural" assessment since the proof exists in the stripped appendix.)

- **No baselines beyond zero-shot for the 13B 2-bit experiment.** Table 3 only compares QZO against Zero-Shot-Q. Without any fine-tuning upper bound or MeZO comparison for Llama-2-13B, the headroom cannot be assessed. (This is partly understandable given hardware constraints, but even a reference number would help.)

### Trivial
None.

## Nice-to-Haves

- Explicit characterization of QZO's effective dimensionality (~50M scale parameters vs ~7B total) as a theoretical advantage for ZO optimization — this may be the key reason QZO works as well as it does and would strengthen the paper's narrative.
- Wall-clock training time comparison (Table 2 reports FLOPs but not actual time; quantized inference kernels have different throughput characteristics).
- Ablation on perturbation scale ε, which interacts with the clipping threshold C.
- Positioning QZO on the Pareto frontier of memory vs. accuracy alongside QLoRA and LoRA.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Claiming to enable Llama-2-13B on 24GB is misleading because QLoRA already does this."** — Removed. The paper claims memory reduction, not novelty of the capability itself. Different approaches achieving similar practical capability is expected.
- **Missing comparison with ZO-signSGD variants (Feng et al., 2024; Zhou et al., 2025; Bar & Giryes, 2025).** — Removed. These are concurrent/very recent works; the paper explains architectural differences in Section 2. Less critical than the QLoRA omission.
- **Missing ablation on ε.** — Moved to nice-to-have. The paper already ablates the more critical hyperparameter C (Figure 3). ε ablation would be informative but isn't a weakness per se.
- **Theorem 1 framed as "structural/fatal."** — Demoted to minor. The proof exists in Appendix A (stripped by parser). The mathematical concern is legitimate in principle but cannot be confirmed as fatal without seeing the proof, which may provide qualifying conditions.

## Novel Insights

The paper's central insight—that continuous quantization scale parameters form a natural, low-dimensional subspace for zeroth-order optimization—has implications beyond the specific QZO method. Since ZO methods suffer from the curse of dimensionality (gradient estimate variance scales with d), QZO's implicit dimensionality reduction (~50M vs ~7B parameters) may be the fundamental mechanism enabling competitive performance despite quantized weights. This connection between quantization structure and ZO optimization efficiency is hinted at in Table 2 but not explicitly analyzed. If formalized, it could provide a theoretical foundation for when and why ZO methods can work well on structured parameter spaces.

## Suggestions

1. **Add QLoRA and LoRA comparisons** to establish QZO's practical niche. Show the memory-vs-accuracy Pareto frontier. If QZO achieves lower memory than QLoRA (likely, since QLoRA stores LoRA adapters + their gradients), demonstrate this trade-off explicitly.
2. **Explicitly frame QZO as a parameter-efficient method** and discuss its relationship to other PEFT approaches. The paper underplays what may be its strongest differentiator: zero additional parameters beyond existing quantization scales.
3. **Report variance across at least 3 random seeds** for the main results (Table 1).
4. **State qualifying conditions for Theorem 1** in the main text, even if the full proof is in the appendix. The reader should know under what assumptions the claim holds.
5. **Analyze the effective dimensionality** of QZO's optimization landscape and connect it to the method's performance.

## Score and Decision

**Anchor comparison (all papers retrieved):**

| Paper | Avg Score | Round | Comparison to QZO |
|---|---|---|---|
| `8QTpYC4smR` (LLM survey) | 1.0 | R1 | Not a research paper; irrelevant as quality anchor |
| `5kMwiMnUip` (NEMESIS jailbreaking) | 1.4 | R1 | Far weaker; no methodology |
| `gwZ90hFSL2` (Chinese NLP robots) | 1.0 | R1 | Far weaker; irrelevant topic |
| `Uj0h13lVrR` (KL GFlowNets) | 1.0 | R1 | Far weaker; very different domain |
| `6Mdvq0bPyG` (EfficientQAT) | 3.0 | R1 | Similar domain (quantized LLM training); QZO has cleaner idea and better scope |
| `0T8vCKa7yu` (CVXQ compression) | 3.0 | R1 | Similar domain; QZO is more practical |
| `vw0NurJ7UX` (PrefixQuant) | 3.0 | R1 | Different approach (activation quantization); QZO is better positioned |
| `E4Fk3YuG56` (Cut Cross-Entropy) | 2.67 (mismatch - actually 8.5) | R1 | Much stronger paper with cleaner contribution |
| **`vqJZb9SX1T` (LeZO/Computation-efficient ZO)** | **4.0** | **R1** | **Closest rejected ZO paper. QZO has a cleaner core idea, more model architectures, but similar evaluation limitations** |
| **`FK6T0U4Mg1` (SubZero)** | **4.25** | **R1** | **ZO with low-rank perturbation; rejected for narrow evaluation and incremental contribution. QZO is more novel** |
| `zcx6rIMbbR` (3-stage quantized FT) | 5.4 | R1 | Different approach; QZO has cleaner methodology |
| **`OBIuFjZzmp` (MeZO-A3dam)** | **4.75** | **R1** | **MeZO variant; rejected. QZO has more novelty but similar evaluation scope** |
| **`myYzr50xBh` (SensZOQ — ZO + sparsity + quantization)** | **5.8** | **R1** | **Most directly comparable accepted paper. Also combines ZO+quantization, accepted with 5,6,6,6,6. QZO has a cleaner idea but worse evaluation (missing QLoRA)** |
| **`9BiVepgmWW` (LOZO — low-rank ZO)** | **7.0** | **R1** | **Stronger ZO paper with better theory, convergence guarantees, and momentum extension. QZO doesn't reach this level** |
| `bEqI61iBue` (HiZOO) | 5.67 | R1 | ZO + Hessian; similar quality range, better theoretical grounding |
| `xw29VvOMmU` (LQ-LoRA) | 6.75 | R1 | Quantized + low-rank; cleaner evaluation and positioning |
| `wg1PCg3CUP` (Scaling Laws for Precision) | 8.0 | R1 | Much stronger, different scope |
| `OOxotBmGol` (LLAMBO) | 8.0 | R1 | Different domain; much stronger |
| `SPS6HzVzyt` (Context-Parametric Inversion) | 8.0 | R1 | Different domain; much stronger |
| `TwJrTz9cRS` (HiRA) | 8.0 | R1 | PEFT method; stronger evaluation and positioning |

**Round 1 bracket: 4.5–6.0.**

QZO's core idea (perturbing quantization scales for ZO) is genuinely novel and cleaner than the rejected ZO papers (4.0–4.75). However, the missing QLoRA comparison is a more critical gap than the issues in the accepted SensZOQ paper (5.8), which despite its own weaknesses had clearer practical positioning. QZO also lacks variance reporting and uses SGD as the upper bound. The paper falls between the rejected ZO variants and the borderline-accepted ones.

**Final calibrated score: 5.0.** The core idea is sound, novel, and practically valuable, but the evaluation does not adequately establish QZO's practical niche relative to the dominant alternative (QLoRA). The paper is above the level of rejected ZO papers (4.0–4.75) due to its cleaner contribution, but below the accepted ZO+quantization paper (5.8) due to its missing critical baseline and underdeveloped positioning. With QLoRA comparisons, PEFT framing, and error bars, this paper could be strong — but in its current form, the evidence is insufficient for a top venue.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>