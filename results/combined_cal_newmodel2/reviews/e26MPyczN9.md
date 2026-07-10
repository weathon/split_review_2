## Summary

This paper re-evaluates claims from prior work that programmatic policies generalize better than neural policies in RL. Through experiments on TORCS, KAREL, and PARKING, the authors show that neural policies can match programmatic ones when training conditions are adjusted (e.g., cautious reward functions, partial observability with last-action augmentation). The paper introduces an expressivity/discoverability framework for analyzing OOD generalization and identifies instance-scaling memory requirements as a class of problems where programmatic representations have a genuine advantage over fixed-capacity neural networks. A proof-of-concept using FUNSEARCH demonstrates that a program synthesizer can produce BFS for a modified KAREL maze.

## Strengths

- The paper tackles a genuinely important and under-examined question: whether the reported OOD generalization advantage of programmatic policies over neural ones is due to representational differences or experimental confounds. Testing this is a valuable scientific contribution regardless of outcome. **[favorability=10.07]**

- The expressivity/discoverability framework (Section 5, Definitions 2 and 3) provides a clean conceptual separation between a representation *containing* a generalizing solution and the search process *finding* it. The insight that prior work inadvertently controlled discoverability for programmatic spaces but not neural spaces is a genuine insight that explains the pattern of results. **[favorability=12.39]**

- The KAREL re-evaluation (Table 2) is informative and clean: showing that a simple feedforward network augmented with the last action (PPO with a_{t-1}) achieves 1.00 return on 4 out of 5 tasks at 100×100 scale, matching or exceeding LEAPS on tasks where LEAPS performs well, is a useful counterexample to claims of inherent programmatic superiority. **[favorability=9.86]**

- The identification of instance-scaling memory as the genuine differentiator (Section 5) is well-motivated. The reasoning that fixed-capacity networks cannot represent algorithms whose working memory grows with input size (BFS frontier, nested subproblem stacks) is sound and points future work in a productive direction. **[favorability=13.42]**

- The PARKING experiment (Section 4.3, Table 3) is honestly reported — the authors acknowledge that results are ambiguous (PSM shows a smaller train-test gap but lower absolute test performance than DQN) rather than forcing a narrative to fit the paper's thesis. **[favorability=9.89]**

## Weaknesses

### Fatal

None.

### Major

- **Asymmetric TORCS comparison undermines the central re-evaluation claim (Section 4.1, Table 1).** The headline comparison pits NDPS trained with the original reward (β=1.0, results from Verma et al. 2018) against DRL trained with a modified reward (β=0.5). The paper argues (line 209) that changing β "is not changing the problem, but only how the agent learns to complete a given track," but this conflates the task definition with the training objective. The training objective is the primary determinant of what the optimizer finds; changing it changes the optimization landscape. The paper's own reasoning supports this — NDPS generalizes because it is "less effective at optimizing speed" (line 15), and DRL with β=0.5 is explicitly steered toward the same cautious behavior. The experiment therefore shows that *both can produce cautious policies when steered that way*, not that neural and programmatic representations are comparable under the same conditions. A cleaner test would train NDPS with β=0.5 as well. **[favorability=0.08]**

### Minor

- **The FUNSEARCH proof-of-concept (Section 5, lines 304–308) is not an RL experiment.** It shows that program synthesis (LLM + FUNSEARCH) can produce a BFS implementation for a KAREL maze, but does not demonstrate that RL-based *programmatic policy learning* can discover such solutions where neural RL policies fail. There is no RL training signal, no neural baseline comparison on the same task, and no connection to the policy learning setting that the rest of the paper studies. The paper is careful to call this a "proof-of-concept," but the evidential gap between this demonstration and the claim about programmatic representations solving problems neural ones cannot is significant. **[favorability=-1.29]**

- **Asymmetric evaluation protocols across comparisons hinder interpretation.** TORCS (Table 1): NDPS results are 3 seeds from the original paper vs. 30/15 seeds for DRL. KAREL (Table 2): LEAPS results are 5 seeds vs. 30 seeds for PPO with a_{t-1}. PARKING (Table 3): 30 seeds for PSM vs. 15 for DQN. LEAPS was also not retrained under the partial-observability / last-action conditions used for the neural policy. While these asymmetries do not invalidate the results, they make it harder to assess whether observed differences stem from the methods or from evaluation protocol variation. **[favorability=4.61]**

- **Selection bias in TORCS results.** Only 13/30 models on G-TRACK-1 and 4/15 on AALBORG successfully learned to complete laps; OOD generalization fractions are reported only over these successful models. The paper does not discuss whether failed models would have generalized had they learned to complete laps, or whether conditioning on successful completion inflates the apparent generalization rate. **[favorability=5.26]**

### Trivial

- **Inconsistency in PARKING seed counts.** Line 260 states "For each policy type, we trained 30 independently seeded models," but line 264 and Table 3 report 30 seeds for PSM and 15 for DQN. This should be clarified. **[favorability=5.81]**

## Nice-to-Haves

- Retrain NDPS with β=0.5 and compare against DRL with β=0.5 to make the TORCS comparison symmetric. This would directly test whether the two representations are comparable under the same training objective.
- Strengthen the FUNSEARCH proof-of-concept: implement BFS as a programmatic policy in the KAREL DSL and learn it through an existing programmatic RL method (e.g., LEAPS), then compare against neural policies on the wall-sparse maze.
- Standardize seed counts and evaluation protocols across all comparisons.
- Report confidence intervals or bootstrap estimates for the TORCS generalization fractions to address the selection-bias concern.

## Removed Points

These points were raised in the original review but are removed as per filtering rules:

- "Expressivity/discoverability framework is circular" — REMOVED. The framework is intentionally conceptual, not a formal theorem. The paper acknowledges the challenge of discoverability (line 290). Criticizing the unquantified "bounded time limit" misreads the framework's purpose.
- "Transformers/memory-augmented architectures not discussed" — REMOVED. The paper explicitly discusses this at lines 312–313: "Large language models, and memory-augmented models, such as stack-RNNs and neural Turing machines, can in principle approximate the structures needed…"
- "Wall-sparse maze (Figure 7) not described in main text" — REMOVED per policy: Figure 7 is in the appendix, which is stripped from all papers by the parser.
- "HARVESTER failure not analyzed" — REMOVED. This is an observation, not a substantive weakness; the paper's main results stand on 4 of 5 tasks.
- "Missing hyperparameters/compute details" — REMOVED per policy: trivial reproducibility nitpicks.
- "Missing related works" — REMOVED per policy: cannot verify.

## Novel Insights

None beyond the paper's own contributions. The review surfaces the β-asymmetry issue in the TORCS comparison and evaluation protocol inconsistencies but does not add fundamentally new conceptual insights beyond what the paper already provides.

## Suggestions

1. Retrain NDPS with β=0.5 and compare against DRL with β=0.5 to make the TORCS comparison fully symmetric. This is the single most impactful fix.
2. Replace or substantially strengthen the FUNSEARCH proof-of-concept with an RL-relevant experiment (e.g., learn BFS as a programmatic policy through LEAPS and compare against neural policies).
3. Standardize seed counts and retrain all baselines under the same evaluation protocol.
4. Report confidence intervals or bootstrap estimates for the TORCS generalization fractions.

## Score and Decision

**Calibration anchors consulted (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Uj0h13lVrR.md | 1.00 | R1 | No | Unrelated topic, strong reject |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gwZ90hFSL2.md | 1.00 | R1 | No | Unrelated topic, strong reject |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8QTpYC4smR.md | 1.00 | R1 | No | Unrelated topic, strong reject |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/It4KL6XnPq.md | 3.00 | R1 | No | Foundation policies with memory; less topical overlap |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/fvTaoyH96Z.md | 2.33 | R1 | No | Environmental generalization in DRL; less rigorous |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/q1Cv7Hp52y.md | 3.00 | R1 | No | Skills-to-plans; different approach |
| **/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NGVljI6HkR.md** | **3.67** | R1/R2 | **Yes** | Directly topical: questions programmatic vs latent space. Weaker conceptual contribution, many detail-oriented weaknesses. Our paper has stronger conceptual framework but similar empirical concerns. |
| **/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lUWf41nR4v.md** | **4.50** | R1/R2 | **Yes** | Program synthesis + state machines for RL; accepted borderline. Our paper has broader scope. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/k6OQ9VTZBZ.md | 4.00 | R1 | No | Spatial concept learning; less topical |
| **/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ehSQZa4vuk.md** | **5.25** | R2 | **Yes** | **Most topically similar**: re-evaluation of RL generalization confounds. Rejected despite strong strengths because empirical scope was limited to toy domains. Our paper has broader empirical scope (3 domains) but similar structural weakness in its central comparison. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/PH7ja3T0vN.md | 4.50 | R2 | No | State combinatorial generalization; different framing |
| **/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/3w6xuXDOdY.md** | **6.50** | R2 | **Yes** | Generalization gap in offline RL; accepted. Cleaner experiments, no asymmetric comparison issues. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/iMI4HRpZFc.md | 5.25 | R2 | No | Delusions in decision making; different topic |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/X1p0eNzTGH.md | 5.67 | R1/R2 | No | Level sampling for ZSG; different methodology |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/eY5JNJE56i.md | 6.75 | R2 | No | Offline RL with OOD generalization; different subfield |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/CJWMXqAnAy.md | 7.00 | R1/R2 | Yes | Hypernetworks for policy generation; much cleaner empirical work. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OI3RoHoWAN.md | 8.00 | R1 | No | LLM-based simulation generation; different topic, higher quality |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/DzGe40glxs.md | 8.00 | R1 | No | Interpreting emergent planning; different topic, higher quality |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9pW2J49flQ.md | 8.00 | R1 | No | LTL task satisfaction; different topic, higher quality |

**Round-1 bracket:** 4–6, based on the gap between the most topical anchor (3.67) and clearly stronger papers (7.00+).

**Narrowing (Round 2):** The most comparable anchor is "Bad Habits: Policy Confounding" (avg 5.25). Both are re-evaluation studies about RL generalization confounds. That paper was rejected. My paper has higher-favorability strengths (9.86–13.42 vs. 8.02–13.06) and weaker most-negative items (my worst at -1.29 vs. their worst at -2.91), but my paper's central empirical comparison (TORCS β asymmetry) has near-neutral favorability (0.08), indicating a genuine structural concern. The "Generalization Gap in Offline RL" anchor (6.50, accepted) has uniformly positive-favorability weaknesses and no asymmetric comparison issue — a higher bar my paper does not reach.

**Final score:** 5.0. The paper's conceptual contributions (expressivity/discoverability, instance-scaling memory) are genuinely valuable, but the central re-evaluation claim is weakened by the asymmetric TORCS comparison, and the main claim about programmatic advantages for instance-scaling memory rests on a proof-of-concept that does not connect to RL policy learning. These are fixable issues, and the paper makes useful contributions even in its current form, but the empirical evidence does not fully support the strength of the claims made.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>