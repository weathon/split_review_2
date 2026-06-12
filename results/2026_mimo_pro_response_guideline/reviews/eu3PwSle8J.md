Now I have enough calibration data. Let me finalize the review.

**Calibration analysis:**

- **ISE paper** (direct baseline in this paper): avg 6.0, Accept — tests IH injection with weaker attacks and less comprehensive evaluation. AIR is clearly stronger: more models, more training methods, stronger attacks (GCG, Astra), and demonstrates consistent improvement over ISE itself.
- **PFT** (prompt injection defense): avg 4.25, Reject — weaker problem definition, limited evaluation, weak baselines. AIR is clearly stronger.
- **ReFAT** (LLM defense): avg 5.75, Accept — interesting insight about refusal features but presentation issues and fewer experimental configurations.
- **Booster/Backtracking** (LLM safety, 8.0): More fundamental paradigm shifts. AIR is more incremental (applying RoPE-like distribution to IH injection).

**Round 1 bracket: 6.0–7.5**

AIR is clearly above ISE (6.0) given its stronger evaluation and consistent improvements. It's below the 8.0 papers due to more incremental novelty. Given the strong empirical results, clean experimental design, and minor weaknesses, I settle on **7.0**.

## Summary
This paper proposes Augmented Intermediate Representations (AIR), a defense against indirect prompt injection attacks that injects Instruction Hierarchy (IH) signals into every decoder layer of an LLM via per-layer trainable embedding tables, rather than only at the input layer as in prior defenses (Delim, ISE). The method adds minimal parameters (0.005% for 8B models) and is evaluated across 3 models (3B, 7B, 8B), 2 training methods (SFT, DPO), and multiple attack types including momentum-boosted GCG and Astra, demonstrating 1.6×–9.2× reductions in ASR for gradient-based attacks with negligible utility loss.

## Strengths
- **Consistent improvements across a comprehensive evaluation matrix**: AIR achieves the lowest GCG ASR across all 6 model×training-method combinations (Table 1), often by large margins (e.g., Llama-3.2-3B SFT: AIR 4.1% vs. Delim 38% vs. ISE 48.1%). The evaluation spans 3 models × 2 training methods × 3 injection mechanisms + None baselines = 18 configurations, providing strong evidence for the generality of the improvement.
- **Negligible utility degradation**: Figure 6 shows AIR maintains win rates comparable to non-adversarially trained baselines, with at most <2% degradation. On SEP (Figure 8), AIR-DPO achieves the best utility×separation tradeoff across all three models.
- **Minimal parameter overhead**: Section 4 quantifies the overhead precisely: for Llama-3.1-8B with 3 privilege levels, AIR adds only 0.4M parameters (0.005% increase), making it practical for deployment.
- **Clean ablation design**: By varying only the IH injection mechanism (Delim, ISE, AIR) while keeping the training pipeline identical across all methods, the paper isolates the effect of per-layer IH injection — a well-controlled comparison.
- **Direct evidence for the signal degradation hypothesis**: Figure 3 provides concrete cosine similarity measurements showing that AIR maintains better privilege-level separation (0.88 vs. 0.92 at layer 25 for AIR vs. ISE) across all decoder layers, directly supporting the paper's motivating observation.
- **Higher attacker loss throughout optimization**: Figure 7 shows AIR consistently maintains significantly higher average GCG attacker loss at every optimization step compared to all baselines, demonstrating the defense degrades gracefully under sustained attack pressure rather than only at a fixed step count.
- **Principled design analogy to RoPE**: The connection to positional embedding evolution (Section 4) provides clean architectural intuition for distributing IH signals across layers, grounding the method in established insights rather than presenting it as ad hoc.

## Weaknesses

### Fatal
None.

### Major
- **Unequal attack budgets between SFT and DPO**: The paper optimizes adversarial prefixes for 200 steps for DPO models but only 50 steps for SFT models (line 190: "200 (DPO models) or 50 (SFT models) steps"). This asymmetry makes direct cross-training-method comparisons misleading — SFT defenses may appear relatively stronger or weaker than they are under equal attack budgets. While within-training-method comparisons remain fair (all injection mechanisms face the same budget within each training method), the paper does not discuss this asymmetry or its implications for interpreting the results.

### Minor
- **Claimed ASR reduction range includes one data point below the stated lower bound**: The paper claims "1.6× to 9.2× reduction in ASR" (Abstract, line 9; line 35; line 242). For Llama-3.1-8B with DPO, AIR (2.8%) vs. ISE (4.0%) yields only a ~1.4× reduction, below the stated 1.6× lower bound. Five of six model×method combinations fall within the claimed range, but the claim should be corrected or qualified.
- **No layer ablation to identify which layers contribute most**: The paper does not experiment with injecting IH signals at only a subset of layers (e.g., first K layers only, last K layers only, every other layer). Such an ablation would establish whether the benefit comes from uniform reinforcement or specific depth ranges, strengthening the mechanistic argument and providing practical guidance.
- **No variance or confidence intervals reported**: ASR numbers are reported as single-point values without bootstrapped confidence intervals or standard errors. Given the binary nature of attack success/failure per instance, reporting variance would strengthen statistical rigor.

### Trivial
None.

## Nice-to-Haves
- Analysis of which attention heads or residual stream components encode privilege information would deepen mechanistic understanding, though this is beyond the paper's stated scope.
- Evaluation against adaptive attackers that specifically target per-layer signals (e.g., with larger attack budgets or ensemble attacks) would further strengthen robustness claims.
- Discussion of failure cases or settings where AIR might not help would provide a more complete picture.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Harsh critic's concern that "the motivating mechanism is asserted, not analyzed"**: The paper explicitly frames this as an empirical contribution targeting the IH injection mechanism. Figure 3 provides direct measurement of the signal degradation phenomenon, and the consistent ASR improvements validate the approach. Demanding full mechanistic understanding of *why* degradation occurs (layer norm, attention mixing, etc.) is scope creep for this paper's contribution type — the paper identifies the phenomenon and proposes a fix, which is standard for empirical ML papers.
- **Harsh critic's concern about "not compared against defenses outside the IH paradigm"**: The paper explicitly scopes its contribution to comparing IH injection mechanisms within the same training pipeline (Section 5.3). Comparing against perplexity filtering, detection-based methods, or other fundamentally different paradigms is outside the stated scope.
- **Harsh critic's concern about "hyperparameter tuning may not be equalized"**: The paper uses identical training procedures for all methods (Section 5.2), which is the standard approach. Acknowledging that different mechanisms might benefit from different hyperparameters is a reasonable sensitivity analysis request but not a fundamental flaw.
- **Harsh critic's claim about "cherry-picking the 9.2× end"**: Table 1 reports all results transparently. The 1.6×–9.2× range accurately describes the spread across model×method combinations (with the minor exception noted above). The paper does not hide any numbers.
- **Strength finder's claim about "comprehensive evaluation matrix"** — kept as a strength (verified against Table 1).
- **Strength finder's claim about "higher attacker loss"** — kept as a strength (verified against Figure 7 description).

## Novel Insights
The paper's main novel insight — that IH signal degradation through decoder layers is a bottleneck for existing prompt injection defenses, and that per-layer reinjection addresses this — is well-supported by empirical evidence (Figure 3 + Table 1). The analogy to RoPE's evolution from input-only to distributed positional encoding is apt and provides clean architectural motivation. While the insight is incremental (applying a known architectural principle to a new domain), the empirical validation is thorough and the practical impact is clear given the consistent improvements across models and training methods. The paper also makes a useful contribution by systematically evaluating the full matrix of IH injection mechanisms × training methods, revealing that DPO generally outperforms SFT for adversarial robustness (corroborating SecAlign).

## Suggestions
- Equalize the GCG attack budget across SFT and DPO (e.g., use 200 steps for both), or at minimum report results at multiple step counts to enable fair cross-training-method comparison.
- Add a layer ablation experiment (e.g., inject IH at only the first/last/middle K layers) to identify which depth ranges contribute most to the defense.
- Correct or qualify the "1.6× to 9.2×" claim given the Llama-3.1-8B DPO case.
- Report bootstrapped confidence intervals for ASR values.

## Reporting

**All anchor papers retrieved:**

| Round | Path | Avg Score | Comparison |
|-------|------|-----------|------------|
| 1 | 5kMwiMnUip.md | 1.40 | Jailbreaking survey — clearly weaker, no technical depth |
| 1 | 8QTpYC4smR.md | 1.00 | LLM survey — no contribution |
| 1 | gwZ90hFSL2.md | 1.00 | Cross-lingual robots — off-topic, no substance |
| 1 | u1cQYxRI1H.md | 0.50 | Illumination harmonization — off-topic |
| 1 | 3MDmM0rMPQ.md | 3.00 | IPE task-specific safety — weak evaluation, rejected |
| 1 | MV5j4Qpq7N.md | 2.33 | System-prompt attention defense — weak, rejected |
| 1 | KyKTjRtyNG.md | 3.00 | Multi-round jailbreaking — rejected attack paper |
| 1 | lUyYX9VFgA.md | 3.00 | Code-of-thought safety probing — rejected |
| 1 | l3bUmPn6u5.md | 4.25 | PFT position-enhanced finetuning — similar topic but weaker evaluation, rejected |
| 1 | 2VmB01D9Ef.md | 4.25 | AutoHijacker black-box attack — attack paper, rejected |
| 1 | V01FPV3SNY.md | 5.33 | RA-LLM robust alignment — defense paper, rejected |
| 1 | 0VZP2Dr9KX.md | 5.25 | Baseline defenses for adversarial attacks — rejected |
| 1 | sjWG7B8dvt.md | 6.00 | **ISE paper** — direct baseline in this paper, same topic. AIR clearly stronger: more comprehensive evaluation, stronger attacks, demonstrates improvement over ISE |
| 1 | iKgQOAtvsD.md | 5.75 | Adversarial prompt translation attack — rejected |
| 1 | rnJxelIZrq.md | 6.50 | Hypergraph defense for social engineering — accepted but different approach |
| 1 | fsW7wJGLBd.md | 7.00 | Tensor Trust prompt injection dataset — accepted, dataset/benchmark contribution |
| 1 | tTPHgb0EtV.md | 8.00 | Booster harmful fine-tuning defense — accepted, more fundamental contribution |
| 1 | Bo62NeU6VF.md | 8.00 | Backtracking safety — accepted, novel paradigm |
| 1 | SPS6HzVzyt.md | 8.00 | Context-parametric inversion — accepted, fundamental analysis |
| 1 | oZtt0pRnOl.md | 8.00 | DP few-shot generation — accepted, different domain |
| 2 | s5orchdb33.md | 5.75 | ReFAT refusal feature adversarial training — LLM defense, simpler scope than AIR |
| 2 | eC4WlSZc4H.md | 6.75 | Robustness over time longitudinal study — rejected, different focus |
| 2 | 4FIjRodbW6.md | 5.83 | TAR tamper-resistant safeguards — accepted |
| 2 | V892sBHUbN.md | 5.75 | Rapid response jailbreak defense — rejected |
| 2 | g9diuvxN6D.md | 7.50 | Zero-shot robustness of instruction-tuned LMs — accepted, strong evaluation |
| 2 | sULAwlAWc1.md | 7.00 | ArrAttack robust jailbreak generation — accepted attack paper |
| 2 | hXA8wqRdyV.md | 6.14 | Simple adaptive jailbreak attacks — accepted |

**Round 1 bracket: 6.0–7.5.** AIR is clearly above ISE (6.0) and comparable defense papers (5.5–6.5), but below the strongest safety papers (8.0) which introduce more fundamental paradigm shifts. Round 2 confirmed this bracket, with papers like Tensor Trust (7.0) and zero-shot robustness (7.5) as nearby anchors for well-evaluated security contributions.

**Final score: 7.0.** AIR is a solid, well-executed paper that does what it claims — a clean empirical contribution with strong results, comprehensive evaluation, and practical relevance. Its main limitation is incremental novelty (applying the known RoPE-like principle of distributed signals to IH injection). The minor weaknesses (attack budget asymmetry, one numerical inaccuracy in the claimed range, no layer ablation) are addressable but do not undermine the core contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>