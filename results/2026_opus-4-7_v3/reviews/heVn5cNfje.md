Now let me read the remaining sections of the paper for completeness:Now I have a comprehensive view of the paper. Let me draft the review before calibration.Now let me run Round 1 calibration — bracketing across score bands:Let me read some of the most relevant anchor papers for calibration:Now let me read one more very relevant anchor - the paper about data selection that was rejected with 4.40:Now I have sufficient calibration data. Let me form my bracket and finalize the review.

**Round 1 Bracket Analysis:**
- The HES paper is clearly above the 3.5-5.5 rejected papers (e.g., "Random Selection is Almost All You Need" at 4.40 and "Pre-Memorization Train Accuracy" at 4.25) — it has more thorough experiments, a novel metric, and broader validation.
- It is comparable to the 5.5-6.5 borderline papers (e.g., "3DS" at 5.75/Reject, "Rule-Based Rating" at 5.75/Reject, "DELIFT" at 6.00/Accept).
- It is clearly below the 7.5-8.5 accepted papers (e.g., "DiSF" at 8.00 — stronger theoretical grounding and more novel insight).

**Initial bracket: 5.0–6.5**

Now let me finalize the review:

---

## Summary
This paper proposes High-Entropy Sum (HES), a training-free metric for data selection in LLM reasoning training. HES sums the entropy of the top 0.5% highest-entropy tokens in each reasoning sample, motivated by the idea that these correspond to critical "forking" tokens in reasoning paths. The authors validate HES across three training paradigms (SFT, RFT, RL), three domains (math, code, STEM), and two base models, showing that data selected by HES can match or exceed full-dataset training with substantially less data.

## Strengths
- **Breadth of experimental validation is genuinely impressive.** Tables 1–6 validate HES across SFT (two model-dataset pairs), RFT (per-query and global-pool, k∈{2,4,8}), and RL, covering math, code, and STEM domains. This scope is rare for a data selection paper and strengthens the practical value of the contribution.

- **Strong negative controls provide compelling evidence of a real signal.** Lowest-HES experiments show dramatic degradation: Table 1 Lowest-HES-20% averages 14.90% versus Highest-HES-20% at 31.14% (a ~16-point gap). Table 2 shows 20.78% vs 34.61%. These large, consistent gaps across benchmarks convincingly demonstrate HES captures meaningful quality differentiation, not noise.

- **The small-to-large model transfer result (Table 1) is practically valuable.** Using a 0.6B proxy model for data curation of an 8B model achieves 32.12% versus self-selection at 31.14%, reducing compute by over an order of magnitude. This validates that HES captures intrinsic data properties rather than model-specific artifacts.

- **The 80% pruning result is well-demonstrated.** Table 1: Highest-HES-80% achieves 35.36% versus Full-Dataset 32.61%, a consistent ~3-point gain from simply removing the bottom 20% of data. This is replicated across domains (Tables 3, 4), providing strong practical guidance.

## Weaknesses

### Fatal
None

### Major
1. **HES is confounded with sequence length, and the paper does not adequately disentangle this.** Since |T_high| = ⌈0.005 × N⌉ (Equation 1), HES mechanically scales with sequence length. In Table 1, HES-20% (31.14%) outperforms Length-20% (30.67%) by only 0.47 points; Entropy Sum (30.92%) is only 0.22 below HES. Critically, AvgHE (Equation 3), which normalizes HES by |T_high| and thus removes the length dependency, performs substantially worse (27.97%). The paper interprets this as showing "cumulative sum is better than average intensity" (Section 3.1), but the simpler explanation — that AvgHE removes the length signal that partly drives HES's advantage — is not considered. No length-controlled experiment (e.g., length-matched strata comparison, residualized HES) is provided. This is an evidential gap because the paper's claimed intellectual contribution centers on the "forking token" mechanism rather than length-based selection, but the current evidence cannot distinguish between these explanations.

2. **RL improvements are modest and inconsistent, undermining the "significantly surpassing" claim.** Table 6: Pos-High, Neg-Rand averages 21.30% versus Full-Batch at 20.63% (+0.67 points). However, on HMMT25 it scores 11.88% versus 15.21% (−3.33 points), and on GPQA 35.54% versus 36.71% (−1.17 points). No confidence intervals or significance tests are reported anywhere in the paper. Given that AIME contains only 30 problems and evaluations use 16 sampling paths, variance could account for differences of this magnitude. The abstract's claim of "significantly surpassing existing training-free selection methods" in RL is not established by the evidence presented.

### Minor
1. **The paper's narrative around "reasoning quality" is inconsistent with Figure 1.** Figure 1 shows that *incorrect* responses have substantially higher HES (normalized mean 0.68) than *correct* ones (0.29) — i.e., higher HES marks failure at the response level. Yet for SFT/RFT data selection among correct responses, higher HES is used to select "higher quality" data. The paper claims "a higher HES score signifies a greater diversity and complexity of reasoning patterns, indicating a higher learning value" (Section 3.1), but this is true only within the subset of correct responses. The paper never explicitly reconciles these two different phenomena. This suggests HES may operate primarily as a difficulty/complexity proxy (harder problems induce more uncertainty in correct solutions) rather than a quality metric capturing "critical forking points," but this alternative interpretation is never discussed.

2. **Sensitivity analysis reveals the top-0.5% mechanism adds little value in non-math domains.** Figure 4 data shows MMLU STEM scores are identical across all four token ratios (0.005, 0.05, 0.5, 1.0), all at 0.855. LiveCodeBench is similarly flat at 0.544. When ratio=1.0, HES reduces to total entropy sum (ES). This undermines the paper's claim that focusing specifically on high-entropy "forking tokens" is the key insight — in non-math domains, simply summing all token entropies works equally well.

3. **Table 2 omits key baselines.** Table 2 (DeepSeek-R1-Distilled-7B on OpenR1-Math-220k) excludes Length, ES, Difficulty, and AvgHE baselines that were included in Table 1. This prevents assessing whether HES's advantage over simpler heuristics holds consistently across model-dataset configurations.

4. **No statistical significance testing across any experiment.** While the paper's results are directionally consistent, many critical margins are under 1 point (SFT: HES vs ES/Length; RL: HES vs alternatives). On small benchmarks (AIME: 30 problems), this is a meaningful gap in evidential rigor.

### Trivial
None

## Nice-to-Haves
- A **qualitative analysis of what high-entropy tokens actually correspond to** — reasoning forks vs. formatting tokens, stylistic uncertainty, or repetition — would ground the "forking token" narrative the paper borrows from Wang et al. (2025).
- **Length-controlled ablation** (HES residualized against length, or HES vs. random within length-matched bins) — this is the single highest-leverage experiment to either substantiate or honestly reframe the contribution.
- **Bootstrap confidence intervals** on benchmark averages, especially for RL results.
- Inclusion of Length/ES/Difficulty baselines in Table 2 for completeness.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Repeated paragraph in Section 4.2.2**: The paragraph "HES shows robust performance in both Per-Query and Global Pool settings" appears twice with near-identical text. Removed as a production/formatting artifact per rules — the original submission likely does not have this issue.
- **Missing comparison with established data selection methods (IFD, LESS, DQ)**: Removed per rules against criticizing absence of specific related methods/baselines that may not exist or be applicable.
- **Forking-Only baseline matching HES**: Table 1 shows Forking-Only (32.51%) outperforms HES-20% (31.14%), but Forking-Only uses 100% of the data (applying gradient updates only to high-entropy tokens). This is a fundamentally different approach (gradient masking vs. data selection) and not a fair comparison. Removed as misleading.
- **Sensitivity analysis strength about 0.5% "consistently optimal across domains"**: This strength claim is contradicted by verified weakness that in STEM and Code domains, all token ratios perform identically. The weakness wins per rules.

## Novel Insights
The observation that HES-based positive selection combined with *random* negative selection outperforms curated negative selection in RL (Table 6: Pos-High, Neg-Rand at 21.30% vs. Pos-High, Neg-Low at 19.50%) is a genuinely useful finding about the asymmetry of quality curation for positive vs. negative trajectories. The insight that diversity in failure modes matters more than curating "easy" failures is practically actionable for RL practitioners. Additionally, the small-to-large model transfer for entropy-based data scoring is a practical contribution with real cost implications.

## Suggestions
- **Disentangle HES from length**: Regress HES on sequence length and use the residual for selection, or compare HES vs. random within length-matched strata. If HES still wins after controlling for length, the forking-token contribution becomes convincing. If not, honestly reframing HES as a length-weighted entropy signal would itself be valuable.
- **Add significance testing**: Bootstrap confidence intervals on benchmark averages would resolve whether the ~0.5–1.5 point margins over baselines are reliable.
- **Explicitly reconcile the Figure 1 narrative**: Discuss that HES correlates with incorrectness across all responses but with higher quality/difficulty among correct responses. Clarify that HES likely acts as a difficulty proxy, which is still useful but is a different story than the "forking token quality" framing.
- **Include full baseline suite in Table 2** to enable cross-setup comparison.
- **Test whether domain-specific token ratios improve non-math results**: The flat sensitivity curves for STEM/Code suggest the 0.5% ratio is math-specific. Exploring whether different ratios or simply using total entropy sum is better for other domains would strengthen the "unified" claim.

## Calibration Anchors

| Anchor Paper | Path | Avg Score | Round | Comparison to HES Paper |
|---|---|---|---|---|
| NEMESIS: Jailbreaking LLMs | 5kMwiMnUip | 1.40 | R1 | Far weaker — no rigorous methodology |
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Survey paper, no contribution. HES far above |
| KL Divergence for GFlowNets | Uj0h13lVrR | 1.00 | R1 | Deeply flawed. HES far above |
| Financial Markets Neural Network | nSDOkm0SKo | 1.00 | R1 | Not a real contribution. HES far above |
| Language Models for Textual Data Valuation | OdoS6cH8MP | 2.00 | R1 | Weak contribution; HES clearly above |
| Disentangling Representation & Selection | EOPLy80bBm | 3.00 | R1 | Limited novelty; HES has more positive results |
| Self-Consuming Training Loop | SaOxhcDCM3 | 3.20 | R1 | Different topic; HES more thorough |
| Task Calibration for LLMs | 8LZ1D1yqeg | 3.00 | R1 | Different focus; HES has broader validation |
| Pre-Memorization Train Accuracy | OegBJMucyM | 4.25 | R1 | Interesting idea but poorly executed; HES more thorough (scores: 8,3,3,3 — split) |
| Rethinking Data Selection at Scale | qUJsX3XMBH | 4.40 | R1 | **Most directly comparable.** Found simple methods sufficient; HES shows its metric adds value above length/random. HES paper is clearly above |
| 100 Instances is All You Need | UoWslU6hsX | 4.33 | R1 | Prediction task, different scope. HES more practical |
| LLMs are Demonstration Pre-Selectors | diKRhKs5yl | 5.25 | R1 | ICL demonstration selection. HES has stronger experimental program |
| Rule-Based Rating of LLM Data | SpTzsQjgxF | 5.75 | R1 | **Comparable.** Both propose data selection frameworks with limited novelty concerns. HES has broader paradigm coverage; Rule-Based has more novel framework. Both rejected |
| DELIFT | Fty0wTcemV | 6.00 | R1 | **Key accept anchor.** Both propose data selection metrics across multiple stages. DELIFT has clearer submodular optimization theory; HES has broader paradigm coverage but weaker mechanistic grounding. Comparable quality, slight edge to DELIFT for clearer theory |
| Putnam-AXIOM | WrBqgoseGL | 5.80 | R1 | Benchmark paper, different type. Not directly comparable |
| 3DS Medical Domain Adaptation | I5p1Gm8GFS | 5.75 | R1 | **Comparable.** Domain-specific SFT selection, limited scope (one domain). HES has broader coverage. Both borderline |
| DiSF: Submodular File Selection | f4gF6AIHRy | 8.00 | R1 | **Accept anchor.** Much stronger theoretical grounding, novel dimensional collapse insight, rigorous greedy algorithm analysis. HES clearly below |
| MMQA | GGlpykXDCa | 8.00 | R1 | Benchmark paper, different domain. Not comparable |
| Magnushammer | oYjPk8mqAV | 8.00 | R1 | Theorem proving, different domain. Clear accept quality — HES below |
| Trustworthiness in RAG | Iyrtb9EJBp | 8.00 | R1 | Different focus. Clear accept quality — HES below |

**Round 1 bracket: 5.0–6.5**

**Narrowing assessment:** The HES paper is comparable in quality to the rejected papers at 5.75 (3DS, Rule-Based Rating) and the accepted DELIFT at 6.00. The key differentiators: (1) HES has impressive experimental breadth (3 paradigms, 3 domains) which the 5.75 papers lack; (2) but HES has a significant unresolved confound (length) and overclaimed mechanism, while DELIFT (6.00) has clearer theoretical backing. The RL section, which the paper emphasizes, is its weakest contribution. The SFT and RFT contributions are solid.

**Final score determination:** The paper's practical contributions (strong negative controls, 80% pruning, small-to-large transfer) place it above the 5.0 range. However, the major weaknesses (length confound, RL inconsistency, overclaimed mechanism) prevent it from reaching a confident accept. It sits right at the borderline, comparable to the 5.75 rejected papers and slightly below the DELIFT accept at 6.0. I place it at **5.5**, reflecting a paper with real but modest contribution whose central mechanistic claim outpaces its evidence.

## Score and Decision

The paper proposes a simple, practical metric (HES) and validates it with impressive breadth. The negative controls are strong, and the SFT/RFT results demonstrate clear utility. However, two major issues — the unresolved length confound that challenges the paper's claimed mechanism, and the modest/inconsistent RL results — prevent the paper from fully supporting its intellectual contribution. The paper presents itself as uncovering the importance of "forking tokens" for data quality, but the evidence is more consistent with HES being an effective length-weighted entropy heuristic. This is still useful but is a less distinctive contribution than claimed. Compared to accepted data selection papers (DELIFT at 6.0), the HES paper has broader scope but weaker theoretical grounding. Compared to rejected borderline papers (3DS at 5.75, Rule-Based Rating at 5.75), it is comparable or slightly above due to its paradigm breadth.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>