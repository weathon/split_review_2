## Summary

This paper introduces a theoretical framework for *controlled sequential social learning*, in which an information-mediating planner (e.g., an LLM) strategically selects the precision of agents' private signals while those agents also learn by observing each other's decisions. The planner can be altruistic (maximizing social welfare) or biased (inducing a specific action). The paper proves convexity of the value function and characterizes optimal policies via multi-phase threshold structures (three phases for the altruistic planner, five for the biased). The key qualitative insight is that a biased planner may intentionally obfuscate signals in certain belief regions—providing precision *below* the level that would make private signals informative—to prevent agents from acting against the planner's preferred action. LLM-based simulations complement the theory.

---

## Strengths

1. **Novel theoretical formalization of a timely problem.** The paper is the first to model a planner who dynamically controls signal precision in a sequential social learning environment, cleanly combining a dynamic MDP (the planner) with decentralized Bayesian agents who learn socially. The positioning relative to Wei & Anastasopoulos (2022) and Smith et al. (2021) is precise: the paper correctly distinguishes itself by avoiding two-way communication or direct manipulation of agents' choice rules.

2. **Convexity result (Theorem 2) is technically substantive.** The paper identifies why standard linearity arguments (Nyarko 1994) fail—agents' actions depend on public belief, breaking the linearity—and states the proof is "quite involved" (p. 5, lines 137–141). If correct, this is a non-trivial technical enabler for the subsequent policy characterizations.

3. **Policy characterizations reveal non-obvious strategic structure.** The three-phase altruistic policy (Theorem 3) and the five-phase biased policy (Theorem 5) go well beyond myopic thresholds. The biased planner's obfuscation result—choosing precision *below* the level that would make private signals informative—is the paper's most striking qualitative insight (p. 7, lines 200–201, "the risk of a private signal overturning the favorable public belief outweighs both the cost of decreasing precision and the potential for public belief to increase further").

4. **Transparent assumptions and clear writing.** Remark 2 (p. 5, line 117) explicitly acknowledges the three main modeling constraints—information parity, binary symmetric channel, full observability—and discusses when each is or is not restrictive. This intellectual honesty helps readers calibrate the scope of the claims.

---

## Weaknesses

### Fatal
None.

### Major

1. **LLM simulation methodology is critically underspecified in the main text.** The paper states it "employ[s] LLMs in three roles" (p. 8, line 206) but never names the specific model—GPT-4, Claude, Llama, Gemini—in the main text. The oracle mechanism is described as generating "a private signal of desired precision tailored to an agent" (p. 8, line 212) without any explanation of how an LLM can reliably produce a binary signal with a *specific controlled accuracy* (e.g., q=0.73). No sample sizes, confidence intervals, or statistical tests are reported for any of the simulation results; the quantitative claims about "less than 10% deviation" (p. 8, line 242) and "40 to 50%" welfare decrease (p. 9, line 252) are presented without replication information or variance measures. These are basic experimental design details that should appear in the main text, not only in the (stripped) appendix.

2. **Evidence for "emergent strategic behavior" lacks baselines.** The paper claims LLM planners exhibit "sophisticated emergent strategic behavior" (p. 8, line 218) and that their policies show "remarkable structural similarity" (p. 8, line 240) to the analytically optimal policies, but provides no comparison to null models. Key baselines are absent: a planner choosing random precisions, a planner using a simple heuristic (always select baseline p), or a planner using only myopic optimization. Without such comparisons, the visual alignment in Figure 2a could reflect the theoretical predictions being broad enough to match many plausible policies rather than genuine strategic adaptation by the LLM.

3. **The comparison between LLM planners and analytically optimal policies uses mismatched agent models.** The analytically optimal policies are computed for Bayesian agents, but the LLM planner interacts with LLM agents who exhibit documented non-Bayesian biases (NB1–NB3). The paper acknowledges this mismatch through the "hybrid" setting (p. 9, line 250–251), but then still interprets the similarity between the LLM policy and the Bayesian-optimal policy as evidence of "robustness." The more informative comparison—between the LLM planner's performance and the optimal policy under the *actual* (non-Bayesian) agent model—is not provided, making it difficult to assess whether the similarity is meaningful or coincidental.

### Minor

4. **Central convexity proof deferred with only a brief intuition.** Theorem 2 is the linchpin of the theoretical analysis. The paper provides a two-sentence intuition (p. 5, lines 139–141: the standard linearity approach fails because agents' actions depend on public belief) but does not sketch the proof strategy—what operator is used, how convexity is propagated, what assumptions on the cost function are required. For a theory paper, this creates unresolved uncertainty about the central technical result.

5. **Non-Bayesian agent patterns (NB1–NB3) lack quantitative support.** The three identified patterns (p. 8, lines 232–234) are supported only by the visual trends in Figure 1b. No effect sizes, variance bands, or statistical significance tests are reported, making it impossible to assess whether the deviations from Bayesian updating are real or within noise.

6. **Welfare quantification methodology is unclear.** The claim that biased planners "decreased social welfare by 40 to 50% when misaligned" (p. 9, line 252) is presented without specifying how social welfare is normalized, what constitutes the "no-control baseline," or what fraction of the decrease is attributable to the planner's bias versus suboptimal optimization.

### Trivial
None.

---

## Removed Points

These points were flagged as weaknesses in the input but are removed with justification:

- *"No sketch or intuition for Theorem 2"* — The paper *does* provide a 2-sentence intuition (lines 139–141). The underlying concern about insufficient detail is retained as a minor weakness (point 4 above), but the categorical claim of absence is removed.
- *"The paper does not discuss whether the planner can learn from experience"* — This asks the paper to address a problem (online learning under unknown parameters) that it explicitly scopes out (p. 3, line 53: "our model does not require the planner to learn unknown parameters"). Scope creep.
- *"The title's 'Steering the Herd' does not analyze herding dynamics specifically"* — While the paper could analyze cascade timing, this is a feature request, not a flaw in the presented analysis.
- *"Notation ambiguity in Section 3.1"* — Minor presentation point that does not affect the paper's substance.

---

## Nice-to-Haves

- Provide a proof sketch for Theorem 2 (e.g., what Bellman operator is used and why it preserves convexity). This would dramatically increase confidence in the central result.
- Compare the LLM planner against the optimal policy computed for the *actual* non-Bayesian agent model, not just the Bayesian model. This would cleanly isolate how much the LLM planner's deviations reflect genuine adaptation.
- Compare the optimal policy to simple baselines (always-q=p, always-q=1, myopic policy) to quantify how much "accounting for social learning" buys.

---

## Novel Insights

The reviews surface a clear tension that the paper itself does not fully resolve: the strength of the paper is its clean theoretical model, but the empirical component is positioned as a core contribution ("emergent strategic behavior," "robustness") while lacking the experimental rigor to support those claims. The most interesting unresolved question is whether the visual similarity between LLM and optimal policies reflects genuine strategic reasoning or simply the fact that the optimal policy's shape (high investment near 0.5, low at extremes) is intuitive enough that any reasonable policy would look similar. This is not a fatal flaw—the theory stands on its own—but it means the empirical claims need to be substantially scaled back or strengthened.

---

## Suggestions

1. Either remove the LLM model name from the appendix into the main text, or state the experimental details (model, n, precision control method) explicitly in Section 6.
2. Add a simple baseline to the LLM planner evaluation: a planner that chooses fixed precision p (no control) and a planner that chooses precision 1 always. Show that the LLM planner outperforms both.
3. Tone down the "emergent strategic behavior" and "corresponds to real behavior" language in the abstract and contributions, or provide the additional experiments needed to support it.

---

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| `JJ46kIfPio.md` ("Steer a Crowd") | 4.00 | R1 | Similar topic (information design with agents); rejected. Paper under review has stronger theoretical novelty. |
| `DGjzxNRbKU.md` ("Markov Persuasion Processes") | 4.20 | R1 | Sequential persuasion; rejected primarily for limited novelty. Paper under review has a more distinct model. |
| `40BTVvYQWZ.md` ("Learning and Steering Game Dynamics") | 4.60 | R1 | Steering game dynamics; rejected for limited theory. Paper under review has stronger theory. |
| `LqTz13JS2P.md` ("Generalized Principal-Agent") | 7.25 | R1 | Top-tier principal-agent theory; accepted. Paper under review has weaker empirical validation. |
| `99tKiMVJhY.md` ("Dec-POMFC") | 6.33 | R2 | Mean field control theory; accepted. Stronger empirical component than paper under review. |
| `tfO07iz0b9.md` ("SemiSGD for MFGs") | 6.25 | R2 | Mean field game theory; accepted. Stronger experimental methodology. |

**Round 1 bracket:** The paper's theory is clearly stronger than the 4.0–4.6 papers (which were rejected primarily for limited novelty), but the empirical validation is weaker than in accepted papers at 6.0+.

**Narrowed range:** [5.0, 6.0]. The theory is genuinely novel and the policy characterizations are non-obvious, pushing above the rejection threshold. However, the underspecified LLM experiments, lack of baselines for the "emergent strategic behavior" claim, and the deferred central proof keep the paper from scoring higher.

**Final score: 5.5** — Borderline Accept. The theoretical framework is a genuine contribution and the policy characterizations are insightful, but the empirical claims outstrip the evidence presented, and the deferred central proof creates unresolved uncertainty about the paper's linchpin result.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>