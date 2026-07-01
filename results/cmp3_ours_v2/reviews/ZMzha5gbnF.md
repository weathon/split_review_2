Here is the final consolidated review.

---

## Summary

This paper identifies and characterizes the "priming vulnerability" in Masked Diffusion Language Models (MDLMs): when an affirmative token for a harmful query appears at an intermediate denoising step, subsequent generation can be steered toward a harmful response even in safety-aligned models. The authors design two attacks (Anchoring Attack and First-Step GCG) to expose the vulnerability, derive a theoretical lower bound (Theorem 4.1) that enables tractable optimization-based attacks without Monte Carlo sampling, and propose Recovery Alignment (RA)—an RLHF-style method that trains models to generate safe responses from contaminated intermediate states. Experiments on three MDLMs show that RA substantially reduces attack success rates while maintaining general capability on 11 benchmarks.

## Strengths

1. **Novel, MDLM-specific vulnerability with a clear mechanistic explanation.** The discovery that affirmative tokens at intermediate denoising steps bypass safety guardrails follows directly from how MDLMs' iterative re-masking works—it is not a repackaged ARM vulnerability (Section 4). The causal link is traced to a specific training-distribution issue: the model is trained only from the fully masked start state (r₀) and never from contaminated intermediate states. This explanation is formalized in Equation 6 and validated by the "RA w/o inter" ablation, which trains only from r₀ and indeed fails to mitigate the vulnerability (Table 2: ~22% ASR vs RA's ~1% on LLaDA at t_inter=4).

2. **Theorem 4.1 is a genuine technical contribution.** Deriving a tractable lower bound on the MDLM generation likelihood that avoids Monte Carlo sampling enables the First-Step GCG attack, which is 20× faster and achieves up to 4× ASR improvement over the MC baseline (Table 1). The theorem's structure—leveraging the priming vulnerability itself to construct the attack—creates a satisfying symmetry between the vulnerability analysis and the attack design.

3. **Defense results are unusually strong for the anchoring attack.** On LLaDA, RA reduces anchoring-attack ASR from 17.3% to 0.0% at t_inter=1, from 44.0% to 1.3% at t_inter=4, and from 68.7% to 3.0% at t_inter=8 (Table 2). The curriculum-based linear scheduling of t_inter is shown to be crucial (Figure 3b), and the ablation study confirms that training on contaminated states drives the improvement. General capability is preserved across 11 benchmarks (Table 4: RA 52.6% vs original 52.2% average).

4. **Thorough evaluation.** Experiments span three MDLM architectures (LLaDA Instruct, LLaDA 1.5, MMaDA MixCoT), multiple attack methods (Anchoring Attack, First-Step GCG, PAD, DiJA, PAIR, ReNeLLM, Crescendo), three evaluation metrics (GPT-4o, LLaMA Guard 3, keyword matching), and 11 capability benchmarks.

## Weaknesses

### Fatal
None.

### Major

1. **Internal inconsistency in ASR numbers for the anchoring attack.** The paper reports three different ASR values for what appears to be the same experimental condition (LLaDA Instruct / LLaDA Original, anchoring attack at the first intervention step):
   - Abstract (line 9, repeated line 35) and Section 4.1 (line 110): **21%**
   - Table 2, "LLaDA Original / Anchoring t_min=1": **17.3 ± 4.6%**
   - Figure 2 data table (line 95, "LLaDA Instruct at 1/128"): **40%**

   Additionally, the "No Attack" baseline is 0% in Figure 2's table (intervention step 0) but 2.0% in Table 2. These discrepancies are not explained. While the qualitative trend (ASR rises sharply with early intervention) is robust across all three numbers, the inconsistency undermines trust in the paper's quantitative reporting and must be resolved before acceptance.

2. **No evaluation of over-refusal on benign queries.** A standard concern in safety alignment is that models may achieve low ASR by refusing benign requests. The paper evaluates general capability using knowledge/completion benchmarks (Table 4), but these do not measure whether RA causes the model to refuse innocuous instructions. An over-refusal rate (e.g., fraction of benign queries from AlpacaEval or a similar benchmark that trigger a refusal in RA vs. the original model) is needed to substantiate the claim that safety improves "without clear degradation."

### Minor

1. **Reward model checkpoint is under-specified.** The paper states it uses "DeBERTaV3... without additional fine-tuning" and cites Köpf et al. (2023; UltraFeedback). It is unclear whether this is the UltraFeedback reward model (trained to score safety/usefulness) or a raw DeBERTaV3 encoder (which would not encode safety preferences). Since RA's entire training signal comes from this reward model, the exact checkpoint must be specified.

2. **First-Step GCG defense results are more modest than the headline numbers imply.** The abstract and introduction highlight the anchoring-attack results (2% → 21%), but for the more realistic non-intervention threat model (First-Step GCG), RA reduces ASR from 58.0% to 11.3% on LLaDA and from 92.7% to 45.7% on MMaDA (Table 2). While the paper briefly acknowledges this (lines 301-302), the presentation is tilted toward the stronger but less realistic threat model. The residual ASR on MMaDA (45.7%) deserves more prominent discussion.

3. **MMaDA's high baseline ASR (79.7% No Attack) is not adequately discussed.** MMaDA is fundamentally unsafe even without any attack, making it qualitatively different from LLaDA and LLaDA 1.5. RA's large absolute improvement on MMaDA partly reflects this high baseline. The paper should explicitly discuss how this affects across-model comparisons.

4. **Theorem 4.1's monotonicity assumption lacks a formal proof.** The assumption (log π_θ(r̃_{t+1}=r | q, r_t) ≥ log π_θ(r̃₁=r | q, r₀) for all t) is stated without proof; the paper appeals to empirical validation in Appendix C.2 and intuitive reasoning about probability mass concentration. While the empirical success of First-Step GCG provides indirect support, a formal justification would strengthen the theoretical contribution.

### Trivial

1. **Scope is narrower than the title suggests.** The paper studies only MDLMs (discrete masked diffusion models), not continuous DLMs (e.g., Diffusion-LM, SSD-LM). The priming vulnerability may not transfer, and this boundary is not discussed.

## Nice-to-Haves

- Add an ablation on how much BeaverTails data is needed for RA's effectiveness (only "2,500 steps" is given without data volume or saturation analysis).
- Clarify whether the anchoring attack injects the *same* harmful response used for evaluation or a different one (Section 4.1)—this distinction matters for interpreting whether the attack direction matches the evaluation target.
- Report results using LLaMA Guard 3 and keyword matching in the main text rather than deferring entirely to the appendix.

## Removed Points

- "Missing appendix content (proofs, empirical validation of monotonicity)" — removed because the parser strips appendices; these exist in the original submission.
- "Abstract's claim about improving robustness against conventional jailbreak attacks papers the nuance on ReNeLLM" — the claim is verifiably true on average (Table 3: RA reduces ASR on all three conventional attacks for both LLaDA models), and ReNeLLM results are honestly reported.
- "Missing comparison with PAD/DiJA as defenses" — these are attack papers, not defense proposals.
- "Speculative concern that reward model is weak and training might optimize a different mechanism" — kept only the checkpoint under-specification point; removed the speculative mechanism since the general capability results (Table 4) provide some reassurance.
- "Criticism that the paper doesn't specify rewards assigned to safe vs. harmful responses" — this is standard practice in RLHF papers; the reward model provides a scalar score, and the paper clearly describes training on safety-usefulness scoring.

## Novel Insights

The reviews surface a meta-insight not stated in the paper: the priming vulnerability has the unusual property that the theoretical lower bound exploit (Theorem 4.1) and the proposed defense (RA) target exactly the same mechanism—the model's behavior at intermediate denoising states. Most attack-defense pairs are asymmetric (the attack exploits one weakness while the defense patches a different one). Here, the attack amplifies the priming vulnerability via a formal lower bound and the defense trains against contaminated states directly. This symmetry is elegant but also means the paper cannot simultaneously claim that the attack is a powerful exploit and that the defense fully closes the gap, because both depend on the same phenomenon—a tension the paper does not fully discuss.

## Suggestions

1. **Resolve the ASR discrepancy**: Clarify which number (21%, 17.3%, or 40%) is correct for the anchoring attack at t_inter=1 on LLaDA Instruct, and explain why the others differ. Also clarify why Figure 2 shows 0% ASR at intervention step 0 while Table 2 shows 2.0% "No Attack."
2. **Add over-refusal evaluation**: Measure the fraction of benign queries (e.g., from AlpacaEval or SafeRLHF) that trigger a refusal in RA vs. the original model.
3. **Specify the exact reward model checkpoint**: Provide a HuggingFace model identifier (e.g., `OpenAssistant/reward-model-deberta-v3-large-v2` or similar).
4. **Discuss the First-Step GCG residual ASR** on MMaDA (45.7%) more prominently, and clarify why the defense is less effective there than on LLaDA.
5. **Add a formal justification** (or stronger citation) for the monotonicity assumption in Theorem 4.1.

## Anchor Papers Consulted

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| /home/.../5kMwiMnUip.md | 1.40 | R1 | Weak survey paper; much lower quality |
| /home/.../BeOEmnmyFu.md | 2.50 | R1 | Simple jailbreak paper; less technical depth |
| /home/.../6Mxhg9PtDE.md | 9.50 | R1 | "Safety Alignment Should be Made..." — far more polished unification paper |
| /home/.../u08UxVNdIo.md | 4.75 | R1 | "Diffusion Attacker" — weaker method, significant flaws |
| /home/.../j7ZWfqCYCY.md | 5.00 | R1 | VLM jailbreak paper; comparable novelty but weaker evaluation |
| /home/.../hXA8wqRdyV.md | 6.14 | R1 | Broad-coverage attack paper; less novelty but extensive model scope |
| /home/.../8Rov0fjpOL.md | 5.80 | R1 | Novel threat model framework; limited model coverage |
| /home/.../Bo62NeU6VF.md | 8.00 | R1 | "Backtracking Improves Generation Safety" — similar concept, cleaner presentation |
| /home/.../G7gvaoX9AW.md | 5.80 | R2 | Safety alignment debiasing paper; rejected despite 5.80 |
| /home/.../r42tSSCHPh.md | 7.00 | R2 | "Catastrophic Jailbreak" — vulnerability discovery paper; cleaner reporting |
| /home/.../F64wTvQBum.md | 6.75 | R2 | Domain certification paper; comparable theoretical contribution |
| /home/.../xP1radUi32.md | 6.25 | R2 | "Endless Jailbreaks" — creative attack, mixed scores |

**Bracket (R1)**: 5.5 – 7.0  
**Narrowed to**: 6.0 — the paper's solid contributions (novel vulnerability, Theorem 4.1, effective defense) are weighed against the concrete ASR reporting inconsistency and the missing over-refusal evaluation.

## Score and Decision

<score>6.0</score>
<decision>Accept</decision>