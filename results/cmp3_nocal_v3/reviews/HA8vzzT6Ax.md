## Summary

This paper revisits the trade-off between watermark strength and speculative sampling efficiency in LLMs. It introduces a continuous information-theoretic measure of watermark strength (expected KL divergence / mutual information), characterizes the trade-off as a Pareto curve, and proposes a pseudorandom acceptance mechanism for speculative sampling that theoretically achieves maximal watermark strength and maximal sampling efficiency simultaneously. Experiments with Gumbel-max and SynthID watermarks show improved detectability at matched efficiency.

## Strengths

- **Information-theoretic measure of watermark strength (Definition 3.1, Theorem 3.1).** Defining WS as $\mathbb{E}_\zeta[D_{\text{KL}}(P_\zeta\|P)]$ (equivalently $I(w;\zeta)$) is principled, and the connection to p-value decay rates in Theorem 3.1 provides theoretical grounding. The bound $\text{WS}(P_\zeta) \leq \text{Ent}(P)$ with equality iff $P_\zeta$ is degenerate (Theorem 3.2) is clean and interpretable.

- **Core insight of pseudorandom acceptance (Section 4.1, Algorithm 1).** The observation that the truly random acceptance coin flip in standard speculative sampling introduces randomness not coupled to $\zeta$, and that replacing it with a pseudorandom variable $\zeta^R$ makes the entire process a deterministic function of $\zeta$, is genuinely clever. Theorem 4.1—showing that under this mechanism, maximal watermark strength and maximal sampling efficiency can be simultaneously achieved—is the paper's strongest result and is non-obvious.

- **Trade-off curve formulation (Definition 3.2, Lemma 3.1).** Framing the trade-off as a Pareto frontier optimization problem provides a unifying language for comparing watermarking schemes. The reformulation reduces the problem to optimizing over $P_\zeta$ with $\mathcal{A}_\zeta$ set to $\mathcal{A}_{\text{spec}}$, which is clean and implementation-friendly.

## Weaknesses

### Fatal
None.

### Major

1. **The bonus step in Algorithm 1 creates a real gap between Theorem 4.1's guarantee and the practical algorithm, without empirical quantification.** Algorithm 1 (lines 15–17) includes a bonus step: when all $K$ draft tokens are accepted, an extra token is sampled from $P_{\zeta^T}$ *without* the pseudorandom acceptance mechanism. Theorem 4.1 explicitly "focus[es] on a single intermediate step $s$" and assumes all tokens are produced via pseudorandom acceptance. Footnote 3 acknowledges the gap but dismisses it as "negligible in practice" without any empirical quantification. For well-aligned draft/target model pairs and $K=2$ (tested in experiments), the probability of all $K$ tokens being accepted—and thus the bonus step triggering—can be substantial (e.g., with 0.8 per-token acceptance rate, $\approx 64\%$ of steps hit the bonus case). Each bonus-step token is generated without $\zeta^R$ coupling and therefore does not satisfy the conditions of Theorem 4.1(c). The paper should report bonus-step frequency and show detectability/WS separately for bonus vs. regular tokens, or modify the algorithm to eliminate the gap.

2. **The experiments operate under conditions that depart from the theory's assumptions, weakening the empirical support for the theoretical claims.** Specifically: (a) **SynthID is tested with $m=30$** (line 257), which the paper itself notes does *not* achieve maximal watermark strength (that requires $m\to\infty$, line 172). Theorem 4.1's optimality guarantee assumes a degenerate decoder (maximal WS). The SynthID experiments therefore test a regime outside Theorem 4.1's conditions, yet this distinction is not clearly marked. The improved detectability shown for SynthID may be due to the Bayes-MLP detection mechanism rather than pseudorandom acceptance achieving maximal WS. (b) **Lowered temperatures** (0.5 for Gumbel-max, 0.7 for SynthID) are used "to make the results more pronounced" (line 259). It is unclear whether the detectability improvements persist at temperature 1.0, which is the standard setting in prior watermarking work. Lower temperatures make distributions more peaked, which affects both watermark strength bounds and acceptance dynamics.

### Minor

1. **The "breaking the trade-off" framing is stronger than what the paper technically delivers.** The paper explicitly states (line 24) that Hu & Huang (2024) use a binary definition of watermark strength and that replacing it with a continuous measure is the path forward. This is a legitimate contribution. However, the rhetorical framing throughout (e.g., "breaking the trade-off" in Section 4.1's title, "overcome" in the abstract) suggests a refutation of the impossibility result on its own terms, whereas the paper actually replaces the target quantity and then resolves the trade-off under the new definition. Since the paper acknowledges this distinction, the criticism is limited—but a reader could come away believing the original impossibility result was wrong, which is not the case.

2. **Limited experimental scope in the main text.** Results for only one dataset (EL15) and one model pair (Llama-68M → Llama-7B) appear in the main body. Gemma model results and C4 dataset results are deferred to the appendix. For a paper making both theoretical and empirical claims, showing at least two settings in the main text would substantially strengthen the generalizability claim.

3. **The relationship between the calibrated threshold $\tau$ and Algorithm 1's acceptance condition is unclearly explained.** Equation (11) uses $\tau$ as a decision threshold, and the text (line 229) says "w_t comes from the draft model iff $u_t = G(\zeta_t^R) \leq \tau$ (see line 9 in Alg. 1)." However, Algorithm 1 line 9 uses the condition $u_t < \min\{1, P/Q\}$, which is the actual acceptance threshold. The paper should clarify that $\tau$ is a calibrated *proxy* for the unknown $\min\{1, P/Q\}$ and describe how the calibration bridges this gap.

### Trivial

- The derivation from formula (8) to (10) in Section 3.2 is too compressed ("with the transition kernel in (5) and the identity $\sum_w \min\{P_w, Q_w\} = 1 - \frac{1}{2}\|P-Q\|_1$"). While the appendix likely fills this in, a slightly more expanded main-text derivation would help readability.

## Nice-to-Haves

- **Quantify the gap between WS and practical detection.** The paper correctly notes in Remark 3.1 that WS measures "ideal detectability assuming the true token distributions are known," and Section 4.2 acknowledges that Theorem 4.1's optimality does not guarantee optimal detection efficiency. The practical detection methods ($\tau$ calibration and MLP) are heuristic. A brief theoretical analysis connecting pseudorandom acceptance to improved *detectability* (beyond WS) would strengthen the paper, though the empirical evidence already supports the claim.

- **Ablation study.** An ablation comparing detection under Algorithm 1 against a detector with access to $\zeta^R$ but where acceptance is still truly random would isolate whether the improvement comes from pseudorandom acceptance per se or from the improved detection method (Ars-$\tau$/Bayes-MLP).

- **Security/information leakage discussion.** Making acceptance decisions pseudorandom means they are deterministic given $\zeta^R$. An adversary who partially reconstructs $\zeta^R$ could predict acceptance decisions. A brief acknowledgment of this would be appropriate.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *AATPS baseline comparison is ambiguous* — REMOVED. The paper clearly describes "Standard Speculative Sampling (Std. SpecSAMPL)" as the standard unwatermarked baseline (Section 2). The comparison shows the watermarked algorithm matches unwatermarked efficiency, which is a positive result. No ambiguity exists.
- *"Human-written" data question* — REMOVED. EL15 (ELI5) is a known human-written QA dataset. The paper's description ("human-written texts from EL15") is accurate, and this is standard practice for null-distribution estimation.
- *"Theorem 3.1 appears to be a known large-deviations result"* — REMOVED. Restating a known result in the paper's notation to connect it to their framework is standard practice and not a weakness.
- *Computational overhead of detection* — REMOVED as a weakness; moved to nice-to-have. The overhead of training an MLP or calibrating $\tau$ is a practical consideration, not a flaw in the paper's claims.

## Novel Insights

The key novel insight from this review is the **bonus-step gap**: Theorem 4.1's guarantee of maximal watermark strength applies only to tokens accepted via the pseudorandom mechanism, but Algorithm 1 includes bonus-step tokens (standard in speculative decoding when all $K$ draft tokens are accepted) that are generated without $\zeta^R$ coupling and therefore fall outside the theorem's scope. The paper dismisses this in a footnote without quantification, but for well-aligned model pairs and $K=2$, bonus steps can be frequent, making this a substantive gap between the theoretical claim and the actual algorithm. A second insight is that the experiments on SynthID with $m=30$ test a regime where Theorem 4.1's optimality guarantee does not apply (since $m=30$ does not achieve a degenerate decoder), meaning the SynthID experimental results demonstrate practical detection improvement but do not directly validate the theoretical claim of maximal WS.

## Suggestions

1. Quantify bonus-step frequency for each model pair and $K$ value tested, and report WS/detectability separately for bonus-step vs. regular tokens.
2. Include results at temperature 1.0 in the main text, or clearly justify why lowered temperatures are the appropriate evaluation setting.
3. Clarify the relationship between the calibrated threshold $\tau$ and the actual acceptance threshold $\min\{1, P/Q\}$ in Section 4.2.
4. Move at least one additional model pair or dataset to the main text to support the generalizability claim.
5. Tone down the "breaking" rhetoric to match the technical scope: "resolving the trade-off under a continuous measure" rather than "breaking the trade-off."

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>