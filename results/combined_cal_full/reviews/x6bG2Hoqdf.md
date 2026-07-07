Now I have everything needed. Let me compile the final review.

## Summary

This paper proposes CALM, a framework for automatic heuristic design (AHD) that fine-tunes a language model via GRPO reinforcement learning during evolutionary search, rather than keeping the LLM frozen as in prior work. It combines "verbal gradients" (prompt manipulation via evolutionary operators) with "numerical gradients" (RL-based weight updates). CALM runs entirely on a single 24GB GPU using an INT4-quantized 7B model, and its results on Online Bin Packing (OBP), TSP, CVRP, and Orienteering Problem (OP) show that the RL-fine-tuned local model can match or exceed API-dependent baselines using GPT-4o-mini.

## Strengths

- **Conceptually novel integration of RL fine-tuning into LLM-based AHD.** Prior work (EoH, ReEvo, MCTS-AHD, FunSearch) keeps the LLM frozen and only manipulates prompts. CALM adds a second feedback loop: the LLM's weights are updated via GRPO using the performance of generated heuristics as reward. This unlocks "numerical gradients" alongside existing "verbal gradients," a genuine extension of the AHD paradigm.

- **Resource efficiency with practical significance.** The system runs locally on a single 24GB GPU with an INT4-quantized 7B model, fine-tuning only 1.15% of weights. This lean setup matches or beats API-dependent baselines (GPT-4o-mini) that use much more powerful language models, lowering the barrier to entry for AHD research.

- **Relatively thorough ablation study.** Table 4 tests removing each operator individually, disabling the collapse mechanism under multiple hyperparameter configurations, and two alternative reward designs, allowing the reader to attribute contributions to specific components.

- **Multiple problem domains with out-of-distribution scaling tests.** Evaluation spans OBP, TSP, CVRP, and OP, with tests at larger scales than training (e.g., TSP N=100 and 200 trained on N=50; OBP 10k items trained on up to 5k items), going beyond i.i.d. testing.

## Weaknesses

### Fatal
None.

### Major

- **The number of sampled responses per prompt (G) is not stated for the main GRPO experiments, making the budget comparison uninterpretable.** The methodology (line 68) introduces G but never assigns a value for the GRPO variant. The API variant explicitly sets G=1 (line 221), but the local GRPO experiments that produce headline results in Tables 1-3 do not disclose G. Since GRPO requires a group of responses per prompt to compute normalized advantages, G must be > 1. The paper frames the comparison as "1,000 heuristic evaluations for baselines and a fixed budget of 2,000 LLM queries for CALM" (line 140), but the total heuristic evaluations for CALM is T × G, not just T. Without G, the claimed cost advantage cannot be assessed. This is the single most important missing piece of information for evaluating the paper's central efficiency claim.

- **Factually incorrect claim about CVRP results in Section 5.2.** Lines 221-222 state the API-based variant "matches MCTS-AHD and outperforms all other baselines on **every CVRP test set**." Table 3 shows CALM API (5.81%, 7.46%, 5.72%) is strictly worse than MCTS-AHD (5.44%, 6.98%, 4.70%) at all three CVRP scales. This is not a minor overstatement but a factual error in the paper's own central discussion section. It must be corrected regardless of any other revisions.

### Minor

- **TSP results do not support unqualified SOTA claims.** The abstract and introduction claim CALM "outperforms SOTA baselines" without caveat, but on TSP N=50 (in-domain), CALM GRPO (10.04%) is worse than MCTS-AHD (9.69%). The body partially qualifies (line 165: "second-best LLM-based result on the in-domain set"), but the headline framing overstates the TSP evidence. The TSP results are competitive but not dominant, and the framing should be adjusted accordingly.

- **The two HSEvo rows in Table 3** (lines 206-207) show different CVRP and OP values under the same method label with no explanation. This creates ambiguity about which HSEvo configuration is being compared and whether the comparison is consistent.

### Trivial
None.

## Nice-to-Haves

- Add standard deviations to the main result tables (Tables 1-3), not just in the appendix, since some comparisons hinge on very small margins.
- Consider elevating the cleanest comparison (same operators and collapse mechanism, with vs. without GRPO) to isolate the contribution of RL more directly.
- Address the "no breakthrough" failure mode for the collapse mechanism (line 260) more thoroughly — if collapse can kill exploration prematurely, this is an important practical limitation.

## Removed Points

The following points from the input review were removed after verification:
1. **"GRPO's 'most significant impact' claim is overstated"** — Verified against Table 4: w/o GRPO gives the worst performance among structure ablations on both OBP (1.78% vs full 0.71%) and OP (19.89% vs full 17.41%). The paper says "near all" which is accurate. Removed as factually incorrect criticism.
2. **"Statistical significance and variance not reported in main text"** — The paper mentions p-values in appendix (line 264) and Figure 2 includes std. dev. shading. Not a required standard for this paper type.
3. **"Collapse mechanism hyperparameter sensitivity is a limitation"** — The paper explicitly acknowledges this (lines 260-261). Already addressed.
4. **"Missing related works"** — Removed per instructions (cannot verify external sources).
5. **"Reproducibility concerns about undisclosed hyperparameters"** — Removed per instructions (nitpick about implementation details).
6. **"Missing appendix content"** — Removed per instructions (parser strips appendices).
7. **"Reward function division by zero edge case"** — The min denominator in Eq. 3 is a plausible concern but extremely unlikely in practice (both parent and child would need exactly 0 performance). Trivial.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **State the value of G for the GRPO experiments** and report total heuristic evaluations (T × G) alongside LLM query counts to enable fair budget comparison. This is the highest-leverage fix.
2. **Correct the factual error about CVRP in Section 5.2** — CALM API does NOT match MCTS-AHD on CVRP by the paper's own data.
3. **Calibrate SOTA claims**: replace unqualified "outperforms SOTA baselines" in abstract/introduction with a nuanced summary that acknowledges the weaker TSP (in-domain) results.
4. **Clarify the two HSEvo rows** in Table 3.

## Score and Decision

**Calibration summary** (all anchors retrieved, ordered by score):

| Anchor | Avg Score | Round | Itemized? | Comparison |
|--------|-----------|-------|-----------|------------|
| 8QTpYC4smR (systematic review) | 1.00 | R1 | No | Unrelated topic, much weaker |
| 5kMwiMnUip (jailbreaking) | 1.40 | R1 | No | Unrelated topic, much weaker |
| Uj0h13lVrR (GFlowNets) | 1.00 | R1 | No | Unrelated topic, much weaker |
| gwZ90hFSL2 (robot cross-lingual) | 1.00 | R1 | No | Completely unrelated |
| sUywd7UhFT (MHRE multi-objective) | 2.50 | R1 | No | Similar topic, weaker methodology and results |
| XTxdDEFR6D (LLM4Solver) | 3.40 | R1 | Yes | Similar topic; CALM has stronger novelty and much milder negatives (−3.47 vs −12.59, −2.69 vs −9.24) |
| xxSK3ZNAhh (HeurAgenix) | 3.80 | R1 | Yes | Similar topic; CALM has better ablation, clearer method; CALM is strictly stronger |
| iTrd5xyHLP (LLMatic NAS) | 3.40 | R1 | No | Different domain (NAS), similar framework |
| t9U3LW7JVX (ADAS) | 3.00* | R1 | No | Misclassified (avg 6.00), broader scope |
| rh54qNvxKO (critical nodes) | 4.17 | R1 | No | Similar LLM+EA approach, less rigorous |
| 0fwJMANq9P (Efficient Heuristics) | 5.25 | R1 | Yes | **Closest anchor.** Same domain and task type. CALM has comparable positive weights (+5.38 vs +5.57 peak) but far milder negatives (−3.47 vs −10.44). CALM is stronger. |
| Usk4KzBxLW (LLM-LNS) | 5.25 | R1 | No | Different task (MILP LNS), similar methodology level |
| cJPUpL8mOw (REvolve) | 6.00 | R1 | No | Related (reward evolution via LLMs), similar quality tier |
| 7mlvOHL6qJ (LASeR robot design) | 6.25 | R1 | No | Different domain (robot design), similar methodology level |
| ZG3RaNIsO8 (EvoPrompt) | 6.50 | R1 | Yes | **Upper anchor.** Cleaner writing, no factual errors. CALM's peak positive (+5.38) is lower than EvoPrompt's (+8.65), but CALM's negatives are milder (−3.47 vs −10.89). CALM is slightly weaker overall. |
| awWiNvQwf3 (Chem space search) | 7.00 | R1 | No | Different domain (molecular discovery), stronger execution |
| OOxotBmGol (LLAMBO) | 8.00 | R1 | No | Different domain (BO), higher impact |
| m2nmp8P5in (LLM-SR) | 8.00 | R1 | No | Different domain (equation discovery), exceptional execution |
| mMPMHWOdOy (WizardMath) | 8.00 | R1 | No | Different domain (math reasoning), higher impact |
| OI3RoHoWAN (GenSim robotics) | 8.00 | R1 | No | Different domain, higher impact |

**Score rationale:** The paper's core contribution — fine-tuning the LLM via RL during evolutionary heuristic search — is a genuine extension of the AHD paradigm that no prior frozen-LLM method achieves. The weighted-item comparison shows CALM's positives (+4.40 novelty, +5.38 ablation, +3.84 efficiency, +3.19 multi-domain) clearly outpace its negatives (−3.47 undisclosed G, −2.69 factual error, −2.24 HSEvo ambiguity, −1.35 TSP claim). The negative weights are far milder than the closest-scoring anchor Efficient Heuristics (5.25), whose review contained −10.44 and −9.24 weight criticisms about incremental contribution. CALM's issues (undisclosed hyperparameter, corrigible factual error) are less fundamental. However, the paper falls short of EvoPrompt (6.50) because EvoPrompt has no comparable clarity issues and its strongest positive weight (+8.65) substantially exceeds CALM's (+5.38). CALM sits between these anchors, with the undisclosed G and factual error preventing a higher score while the genuine methodological novelty and thorough evaluation prevent a lower one.

**Final score: 6.0 — borderline accept.** The contribution is sound and the issues are fixable with straightforward corrections (stating G, correcting the CVRP claim, calibrating claims). If the authors resolve these in the rebuttal, the paper represents a meaningful advance to the LLM-based AHD literature.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>