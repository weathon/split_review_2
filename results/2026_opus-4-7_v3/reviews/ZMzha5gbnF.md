Now let me read the remaining portions of the paper to verify all claims thoroughly.Now I have thoroughly read the paper. Let me draft the review.Now let me calibrate with Round 1 bracketing:Let me read a few key anchor papers for comparison.Now I have good calibration data. Let me form my initial bracket based on the anchors.

**Round 1 Bracket Analysis:**

The most relevant comparisons are:
- **Backtracking (Bo62NeU6VF, 8.00)**: Very similar concept — recovery from unsafe generation. For ARMs, introduces [RESET] token. Scores 8,8,8,8. But addresses ARMs (much broader ecosystem), and includes adaptive attack testing.
- **Safety Alignment Should be More Than Just a Few Tokens Deep (6Mxhg9PtDE, 9.50)**: The ARM analog of this paper. Identifies shallow alignment, proposes deepening. Scores 10,10,8,10. Much broader narrative scope and impact.
- **Catastrophic Jailbreak via Generation Exploitation (r42tSSCHPh, 7.00)**: Identifies new vulnerability (decoding manipulation), proposes defense. Scores 6,6,8,8. Similar structure (attack + defense) but narrower theory.
- **Diffusion Attacker (u08UxVNdIo, 4.75)**: Uses diffusion for jailbreaking but has weak baselines and design. Scores 3,5,6,5. The paper under review is clearly superior.
- **Simple Adaptive Attacks (hXA8wqRdyV, 6.14)**: Attack-only paper, comprehensive but no defense. Scores 6,8,6,6,6,5,6.

**Initial bracket: 6.5 – 8.0**

The paper is clearly above the borderline-reject range (4-5), has genuine novel contributions comparable to the 7.0 anchor, but the over-refusal gap and somewhat oversold theorem prevent it from reaching the 8.0 tier. Let me now write the final review.

---

## Summary
This paper identifies a "priming vulnerability" in Masked Diffusion Language Models (MDLMs): even a single affirmative token appearing at an intermediate denoising step can steer a safety-aligned model toward generating harmful responses, bypassing alignment. The authors formalize this through an anchoring attack (diagnostic) and First-Step GCG (practical, 20× faster than MC GCG), supported by a theoretical lower bound (Theorem 4.1). They propose Recovery Alignment (RA), which trains the model to recover safe responses from contaminated intermediate states via GRPO with a linear curriculum schedule over intervention steps.

## Strengths
- **Novel, well-characterized vulnerability with strong empirical evidence.** Figure 2 and Table 2 show that even a single injected token at $t_\text{inter}=1$ raises ASR from 2% to 21% on LLaDA Instruct (Section 4.1, line 110). The paper carefully distinguishes this from ARM prefilling attacks: MDLMs' non-causal, parallel denoising creates a structurally different attack surface where tokens at *any position* in an intermediate state influence the entire output.

- **First-Step GCG is a clean, practically useful technical contribution.** Table 1 shows 20× speedup (0.2h vs. 4.3h per prompt) and up to 4× higher ASR (58% vs. 20% on LLaDA Instruct, 49.5% vs. 12.5% on LLaDA 1.5) compared to Monte Carlo GCG. The transformation from an intractable stochastic multi-step optimization to a single differentiable forward pass is elegant.

- **Defense is tightly motivated by the vulnerability analysis.** The paper's diagnosis—standard alignment only trains from fully masked initial states, never from contaminated intermediate states (Eq. 5-6, Section 5)—directly and logically motivates Recovery Alignment. The ablation (RA w/o inter) in Table 2 validates that training on contaminated states is the critical ingredient: without it, ASR remains ≥20% at $t_\text{inter}=4$.

- **Thorough experimental coverage.** Three MDLMs, two benchmarks, three evaluation metrics, seven attack methods (four priming, three conventional), four baselines, and eleven capability benchmarks. Results are reported with standard deviations over three runs. Ablation studies on scheduling strategy (Figure 3b) and $t_\text{max}$ (Figure 3a) provide useful engineering guidance.

- **Minimal capability degradation verified across eleven benchmarks.** Table 4 shows average accuracy essentially unchanged (52.2→52.6 on LLaDA Instruct, 52.7→52.8 on LLaDA 1.5), with no systematic performance drop.

## Weaknesses

### Fatal
None

### Major
- **Missing over-refusal evaluation.** The paper evaluates capability preservation on eleven benchmarks (Table 4), but these are predominantly multiple-choice tasks that would not detect a model that achieves low ASR by refusing benign open-ended requests more aggressively. Over-refusal measurement (e.g., via XSTest or OR-Bench) is a standard evaluation dimension for safety alignment methods. Without it, one cannot determine whether RA's low ASR comes partly at the cost of excessive refusal of benign queries, which would undermine practical utility.

- **Theorem 4.1 framing overstates its explanatory power.** The bound is $\frac{1}{T}\log \pi_\theta(\tilde{r}_1 = r \mid q, r_0)$ with $T=128$, meaning the bound divides the first-step log-likelihood by 128—extremely loose. The paper partially acknowledges this ("this effect helps compensate for the looseness of the lower bound," Section 4.2), but the real reason First-Step GCG works is the *empirical priming phenomenon* (affirmative tokens steer subsequent steps), not the bound's tightness. The theorem correctly justifies the surrogate objective formally, but the paper's framing suggests it explains why First-Step GCG is effective, when in fact the priming vulnerability (an empirical observation) is the operative mechanism.

### Minor
- **Remaining vulnerability under strong attacks limits practical significance of the defense.** At $t_\text{inter}=32$, ASR remains 43–79% even with RA (Table 2). Under ReNeLLM, RA still permits 72% ASR on LLaDA Instruct (Table 3). The paper honestly acknowledges this ("RA remains imperfect against strong attacks"), but it constrains the practical scope of the defense claim.

- **Out-of-distribution generalization of RA untested.** RA trains on contaminated states derived from BeaverTails harmful responses. Whether it generalizes to harmful patterns not represented in BeaverTails (or to naturally-occurring contamination from stochastic sampling noise) is not evaluated. Even a small OOD evaluation would address concerns that RA learns BeaverTails-specific refusal patterns rather than general recovery capability.

- **Monotonicity assumption in Theorem 4.1 is strong.** The assumption requires that *no* intermediate state ever makes the model less likely to predict the target response than the fully masked state ($\log \pi_\theta(\tilde{r}_{t+1} = r \mid q, r_t) \geq \log \pi_\theta(\tilde{r}_1 = r \mid q, r_0)$ for all $t$). While empirically validated in Appendix C.2, edge cases (e.g., intermediate states containing conflicting harmful tokens) could violate this. The paper should flag this as a limitation more prominently.

### Trivial
None

## Nice-to-Haves
- Measure tightness of Theorem 4.1's bound empirically by comparing $\frac{1}{T}\log \pi_\theta(\tilde{r}_1 = r \mid q, r_0)$ to MC-estimated $\log p_{\pi, m_t}(r_T = r \mid q, r_0)$, clarifying whether the theorem functions as a bound or as a heuristic motivation.
- Evaluate RA's interaction with alternative masking strategies (e.g., confidence-based unmasking), since the vulnerability arises from the denoising process and different masking strategies might naturally mitigate or exacerbate it.
- Consider adaptive attacks that specifically target RA's recovery mechanism (e.g., optimizing suffixes to defeat the recovery behavior directly).

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **L=128 generation length limitation.** The reviewer raised concern that all main experiments use L=T=128 tokens and results may not hold at longer lengths. However, the paper explicitly states "we report the impact of generation length in Appendix C.5" (Section 6.1). Since the appendix is stripped by the parser, this concern cannot be verified and may already be addressed. Removed per appendix rule.

- **MMaDA as poor testbed.** MMaDA starts at 79.7% ASR with no attack, meaning it is essentially unaligned. While this is true, the paper uses MMaDA as one of *three* models—the primary vulnerability analysis focuses on the aligned LLaDA models where the vulnerability is more meaningful (ASR goes from 2% to 21%). MMaDA serves as a useful additional data point.

- **Strong threat model for anchoring attack/PAD/DiJA.** The paper correctly labels the anchoring attack as "hypothetical" (Section 4.1) and uses it for controlled diagnostic analysis. The practical threat model (First-Step GCG, query-only modification) is properly separated. The reviewer acknowledged this distinction themselves.

- **Abstract overstating mitigation.** The abstract says RA "significantly mitigates the vulnerability." While Table 2 shows ASR remains ~50% at $t_\text{inter}=32$, for $t_\text{inter} \leq 16$ ASR drops dramatically (e.g., from 68.7% to 3.0% at $t_\text{inter}=8$ on LLaDA Instruct). The word "significantly" is reasonable for the primary operating regime.

## Novel Insights
The paper's key novel insight is that MDLM safety has a structurally different failure mode than ARM safety. In ARMs, prefilling attacks exploit sequential left-to-right prediction, so the first few tokens dominate. In MDLMs, the iterative parallel denoising creates a vulnerability where tokens at *any position* in an *intermediate state* can anchor subsequent generation toward harm—and standard alignment, which only trains from fully masked initial states, never exposes the model to this failure mode. The tight coupling between this diagnosis and the Recovery Alignment defense (training from contaminated intermediate states) is the paper's most coherent contribution. The First-Step GCG optimization, which converts an intractable stochastic objective into a single differentiable forward pass, is a practically valuable technical insight for the MDLM attack research community.

## Suggestions
- **Add over-refusal evaluation** using XSTest or OR-Bench. This is the single most impactful addition for strengthening the defense contribution.
- **Reframe Theorem 4.1** more precisely: distinguish between its formal role (justifying the surrogate objective) and the empirical priming vulnerability (the operative mechanism explaining *why* First-Step GCG works).
- **Include a small out-of-distribution test** for RA, evaluating on harmful patterns not drawn from BeaverTails, to demonstrate generalization.
- **Report the empirical gap** between the first-step lower bound and the actual multi-step log-likelihood to clarify the theorem's practical relevance.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | R1 | Far below: basic jailbreak listing with no novel contribution |
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Far below: literature review, no original research |
| Playing Language Game | BeOEmnmyFu | 2.50 | R1 | Below: limited novelty and weaker execution |
| Leveraging System-Prompt Attention | MV5j4Qpq7N | 2.33 | R1 | Below: weak defense with questionable methodology |
| Incremental Exploits | KyKTjRtyNG | 3.00 | R1 | Below: multi-round jailbreak with limited novelty |
| Diffusion Attacker | u08UxVNdIo | 4.75 | R1 | Below: uses diffusion for jailbreaking but weak baselines, questionable design |
| Information-Theoretical Trade-off | j7ZWfqCYCY | 5.00 | R1 | Below: trade-off analysis, limited experimental rigor |
| Breaking Free (EvoSeed) | 6qeCyvlJUJ | 3.67 | R1 | Below: adversarial image generation, limited scope |
| Testing Limits (Purple Problem) | FD9sPyS8ve | 4.75 | R1 | Below: interesting but narrow definitional exercise |
| Simple Adaptive Attacks | hXA8wqRdyV | 6.14 | R1 | Comparable but below: attack-only paper, no defense, no theoretical contribution |
| Compositional Adversarial Attacks | plmBsXHxgR | 6.25 | R1 | Comparable: cross-modality attacks, but paper under review has tighter attack-defense coupling |
| Breach By A Thousand Leaks | 8Rov0fjpOL | 5.80 | R1 | Below: information leakage framework, different scope |
| Catastrophic Jailbreak via Generation | r42tSSCHPh | 7.00 | R1 | Comparable: similar structure (novel vulnerability + defense), paper under review has stronger theory |
| SAR Diffusion Models | tyEyYT267x | 8.00 | R1 | Above: strong DLM contribution but different focus (modeling, not safety) |
| Robust Diffusion Classifier | I5lcjmFmlc | 8.00 | R1 | Above: different domain (image classification), high technical depth |
| Backtracking Improves Safety | Bo62NeU6VF | 8.00 | R1 | Slightly above: very similar concept (recovery from unsafe generation) but for broader ARM ecosystem, simpler mechanism |
| Detecting Memorization | 84n3UwkH7b | 8.00 | R1 | Above: different topic, high execution quality |
| Safety Alignment Few Tokens Deep | 6Mxhg9PtDE | 9.50 | R1 | Above: ARM analog with broader narrative and impact |
| IC-Light | u1cQYxRI1H | 10.00 | R1 | Not comparable: different domain entirely |
| Chinese NLP Robots | gwZ90hFSL2 | 1.00 | R1 | Not comparable: completely different topic |

**Round 1 bracket: 6.5 – 8.0**

The paper is clearly above the borderline-reject band (4-5 range), where papers have weaker novelty and execution. It sits in the same space as jailbreak attack+defense papers scoring 6-7 (Simple Adaptive Attacks at 6.14, Catastrophic Jailbreak at 7.00), but with stronger theoretical grounding and more comprehensive experiments. However, it falls short of the 8.0 tier (Backtracking) primarily because: (1) the over-refusal evaluation gap is a genuine evidential hole for a defense paper, (2) the theoretical contribution (Theorem 4.1) is somewhat oversold given its looseness, and (3) MDLMs are a niche model class compared to ARMs, limiting immediate impact.

The paper's genuine novelty (priming vulnerability as a structurally distinct attack surface), the clean First-Step GCG contribution (20× faster, 3-4× more effective), and thorough experimental design push it above borderline accept. But the missing over-refusal measurement, the remaining vulnerabilities at high intervention steps, and the untested OOD generalization prevent it from reaching the solid accept range.

**Final score: 7.0**

This paper makes a solid, novel contribution to an emerging and important area (MDLM safety). It identifies a genuine vulnerability, provides a practical attack, and proposes an effective defense—all supported by thorough experiments. The over-refusal gap and theorem framing are real weaknesses but do not invalidate the core contribution. It is comparable to the Catastrophic Jailbreak paper (7.00) in overall quality: both identify new vulnerabilities, propose defenses, and have some evaluation gaps. The paper merits acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>