Now I have enough calibration data. Let me finalize my analysis.

**Anchor analysis summary:**
- **"Mimetic Initialization" (iVy7aRMb0K)** — avg 4.5, Rejected. Very similar topic but narrower, less thorough, incremental. Our paper is clearly better.
- **"Understanding Bottlenecks of SSMs" (pymXpl4qvi)** — avg 6.0, Accepted. SSM limitations study with uniform 6s. Our paper is more thorough with more actionable insights.
- **"Zoology" (LY3ukUANko)** — avg 6.33, Accepted. The paper our work directly extends and corrects. Our analysis is more careful.
- **"RNNs are not Transformers (Yet)" (h3wbI8Uk1Z)** — avg 5.5, Accepted. Theoretical RNN vs Transformer expressivity gap.
- **"SSMs are Provably Comparable" (QFgbJOYJSE)** — avg 5.75, Accepted. Theoretical SSM capabilities.
- **"Never Train from Scratch" (PdaPky8MUn)** — avg 8.0, Accepted. Very similar thesis (prior comparisons confounded by methodology), but broader scope and proposes a concrete solution.
- **"Small-scale proxies" (d8w0pmvXbZ)** — avg 8.0, Accepted. Training instability analysis with mitigations.

**Initial bracket: 6.0–7.0.** Our paper is clearly above the 5.5–6.0 anchors (more thorough, more impactful, corrects prior published work) but below the 7.5–8.0 anchors (which propose solutions or have broader scope). The narrow LR window persists even after tuning (framing issue) and synthetic-only benchmarks keep it below 7.5.

**Narrowed bracket after Round 2: 6.0–7.0.** The Round 2 anchors confirm this range. "Understanding Bottlenecks of SSMs" (6.0, accepted with uniform 6s) is a weaker paper than ours but in the same space. Our paper provides more extensive experiments (3000+ runs), more actionable findings (conv1d ablation, DeltaNet result), and directly corrects prior published results. This puts us above 6.0. "Never Train from Scratch" (8.0) shares our thesis about confounding factors but has broader scope (LRA benchmarks) and proposes a concrete solution, putting it above us.

**Final score: 6.5.** The paper is a solid empirical contribution that corrects an important finding in the literature, with impressive experimental scale and clean architectural ablations. It falls slightly short of the 7.5+ tier due to: (1) overclaimed framing ("mainly" optimization), (2) synthetic-only benchmarks limiting practical impact, and (3) no proposed solution beyond diagnosis. But these are not fatal — the core contribution is valuable.

---

## Summary
This paper provides an extensive empirical study (3,000+ runs, 5 seeds each) demonstrating that prior evaluations concluding SSMs cannot solve associative recall and copying tasks were confounded by suboptimal learning rate tuning. With careful LR grid search, Mamba solves MQAR at sequence lengths where it previously failed, and the conv1d component emerges as the key architectural driver for 1-layer recall in both SSMs and Transformers. The paper also reveals contrasting width vs. depth scaling preferences and shows DeltaNet achieves Transformer-level optimization stability.

## Strengths
- **Critical confounder revealed via massive LR grid search (Figures 1, 2):** Over 3,000 runs demonstrate that the learning rates used by Arora et al. (2023) fall outside the optimal range for Mamba and Hyena. With finer grids, Mamba solves MQAR at long sequence lengths where it previously scored near-zero. This is a concrete, important correction to the published literature.
- **Clean conv1d ablation (Table 2):** Adding conv1d to a 1-layer Transformer brings accuracy from 2% to 99%; removing it from Mamba drops it to 2%. This establishes a precise mechanistic link between the architectures and provides actionable architectural insight.
- **Contrasting scaling behavior documented with clear evidence (Figures 3, 4, Table 1):** The copy task result — 12-layer, 1408-width Mamba (150M params, 100%) vs. 24-layer, 1024-width Mamba (150M params, 16%) — cleanly shows that fair parameter-matching requires scaling SSMs along their preferred axis (width).
- **DeltaNet achieves Transformer-level LR robustness (Figure 7):** DeltaNet maintains high accuracy across a wide LR range while Mamba/Mamba2 show sharp peaks, with a plausible mechanistic explanation tied to Householder matrices avoiding vanishing gradients in the off-diagonal terms.
- **Findings validated on two benchmarks (MQAR + copying):** The narrow LR window and width-over-depth scaling replicate across both tasks, suggesting these are general properties rather than artifacts of one synthetic setup.

## Weaknesses

### Fatal
None.

### Major
- **Central thesis is overstated relative to evidence.** Line 39 states: "Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics." However, Figure 1 shows that even after careful tuning, Mamba's good LR window remains extremely narrow (~one order of magnitude) versus Transformers (~four orders of magnitude). A model that only works within a single-order-of-magnitude LR window has a structural loss-landscape property that is functionally indistinguishable from an expressivity limitation for practitioners without massive grid search. The evidence supports the weaker claim that "expressivity assessments have been confounded by optimization instabilities," but the stronger "mainly optimization" framing goes beyond what the data shows.

- **Conv1d ablation partially undermines the SSM-vs-Transformer narrative.** Table 2 shows that the key component enabling 1-layer Mamba recall is the conv1d — since adding conv1d to a plain Transformer achieves identical performance. The paper acknowledges this in Section 7 but the broader narrative about "SSMs vs Transformers" does not fully integrate the finding that a trivial architectural modification makes the two architectures perform identically. The cleaner story is "convolutions provide a useful inductive bias for recall," which is a narrower but better-supported conclusion.

### Minor
- **No direct gradient analysis.** The paper claims optimization instability (vanishing/exploding gradients) but does not directly measure gradient norms or gradient variance during training. The paper cites Trockman et al. (2024) for the vanishing gradient claim in Mamba's A_k matrices but does not reproduce or verify this empirically. Direct gradient evidence would substantially strengthen the optimization instability story.
- **LR window width not quantified systematically.** The paper shows LR sensitivity curves qualitatively but does not report a metric like "range of LRs achieving >90% accuracy" across architectures, sequence lengths, and dimensions. Computing this would make the instability argument more rigorous and less dependent on visual inspection.
- **Scaling claim demonstrated only on MQAR.** Line 151 ("rather than the number of parameters, it is the way these models is scaled that has most impact on their performance") is presented as a general insight but demonstrated only on one synthetic task.
- **Loss bump interpretation is speculative.** Line 188 states "we hypothesize that during this phase transition, the Attention mechanism attempts to form induction heads." The paper appropriately frames this as a hypothesis, but no mechanistic evidence (e.g., attention pattern analysis) is provided.

### Trivial
None.

## Nice-to-Haves
- Study whether gradient clipping or learning rate warmup widens SSMs' effective LR window — this would directly strengthen the practical contribution.
- Investigate whether scaling width also widens the LR window, unifying the width/depth scaling and LR sensitivity findings.
- Connection to downstream language modeling tasks (acknowledged in the Discussion as a critical next step).
- Quantitative metric for LR window width (e.g., log-range of LRs achieving >90% accuracy).

## Removed Points
These points are flagged to be removed, treat them with caution:
- Harsh critic's concern about missing specific LR grid values in main text — the paper states all experimental details are in Appendix A.2 (parser strips appendices; they exist in the original submission).
- Harsh critic's note about speculative induction head interpretation — the paper already frames this as a hypothesis (line 188: "we hypothesize"), which is appropriate academic language.
- Harsh critic's note about optimizer sensitivity beyond LR — this is a nice-to-have, not a weakness of the current paper's scope.
- Harsh critic's note about missing gradient analysis — this is valid but would require the paper to fundamentally change its methodology; it's more of a nice-to-have extension than a flaw.

## Novel Insights
The paper's most novel empirical finding is that prior SSM failure on MQAR was largely an artifact of suboptimal learning rate tuning rather than fundamental expressivity limits — a direct correction to published results (Arora et al., 2023). The conv1d ablation (Table 2) provides a particularly clean mechanistic insight: conv1d is the single architectural component that makes 1-layer recall work for both SSMs and Transformers, suggesting the real story is about locality rather than recurrence vs. attention. The DeltaNet stability result (Figure 7) offers a concrete architectural direction for improving SSM optimization, with a plausible explanation tied to Householder matrices.

## Suggestions
- Reframe the central thesis from "mainly optimization dynamics" to "expressivity assessments have been confounded by optimization instabilities." This is better supported by the evidence.
- Give the conv1d finding (Table 2) more prominence in the narrative — it is arguably the paper's cleanest mechanistic result and should be presented as a strength rather than an inconvenient complication.
- Add a quantitative metric for LR window width (e.g., log-range of LRs achieving >90% accuracy) to make the instability claim more rigorous.
- Add direct gradient norm measurements during training to substantiate the optimization instability claim.

## Score and Decision

### All retrieved anchors across rounds:

| Round | Path | Avg Score | Topic | Comparison |
|-------|------|-----------|-------|------------|
| R1 | Uj0h13lVrR | 1.00 | GFlowNets | Irrelevant, much weaker |
| R1 | 8QTpYC4smR | 1.00 | LLM survey | Irrelevant, much weaker |
| R1 | gwZ90hFSL2 | 1.00 | Cross-lingual robotics | Irrelevant, much weaker |
| R1 | BUpdp5gETF | 2.50 | Learning rate schedules | Different focus, weaker contribution |
| R1 | qPwQj4Mf3u | 3.00 | Hopfield networks | Related topic, weaker empirical contribution |
| R1 | vnp2LtLlQg | 3.00 | Optimizing attention | Different focus, weaker |
| R1 | iVy7aRMb0K | 4.50 | Mimetic init for SSM recall | Most similar topic; narrower, less thorough than ours |
| R1 | YuFUUcSUgx | 4.00 | LRA fair comparison | Related but less thorough |
| R1 | sBSC0OXEQG | 4.50 | Correlated associative memories | Related topic, different focus |
| R1 | hwSmPOAmhk | 7.33 | Factual recall in Transformers | Theoretical, broader scope |
| R1 | IiagjrJNwF | 6.25 | Memory Mosaics | Different architecture focus |
| R1 | LY3ukUANko | 6.33 | Zoology | Paper we directly extend and correct |
| R1 | Tzh6xAJSll | 7.60 | Scaling laws for associative memories | Broader theoretical scope |
| R1 | d8w0pmvXbZ | 8.00 | Small-scale proxies for training instabilities | Similar thesis, proposes solutions |
| R1 | PdaPky8MUn | 8.00 | Never Train from Scratch | Most similar thesis, broader scope + proposed solution |
| R2 | pymXpl4qvi | 6.00 | Understanding Bottlenecks of SSMs | Similar topic, less thorough, accepted at 6.0 |
| R2 | b5lXUwZiD3 | 5.25 | Transformer for HMMs | Related (RNN vs Transformer), weaker |
| R2 | QFgbJOYJSE | 5.75 | SSMs provably comparable | Theoretical, less empirical depth |
| R2 | EGjvMcKrrl | 6.00 | Generalization analysis for SSMs | More theoretical, rejected at 6.0 |
| R2 | zDze7VtB5C | 5.50 | Log-depth transformer expressivity | Different focus |
| R2 | h3wbI8Uk1Z | 5.50 | RNNs not Transformers (Yet) | Theoretical expressivity, accepted |
| R2 | aWLQTbfFgV | 6.25 | Formal language recognizers | Different methodology |
| R2 | Hxm0hOxph2 | 5.25 | Length/compositional generalization | Different focus |
| R2 | YlleMywQzX | 5.75 | NAS for tabular | Irrelevant |
| R2 | E1ML0nEReb | 6.20 | Point cloud segmentation | Different domain |
| R2 | HZndRcfyNI | 6.50 | Architecture-aware scaling | Related (hyperparameter sensitivity) |

**Round 1 bracket: 6.0–7.0.** Paper is clearly above the 5.5–6.0 range (more thorough, more impactful, directly corrects published work) but below 7.5+ (which either propose solutions or have broader scope on downstream tasks).

**Round 2 confirmation: 6.0–7.0.** "Understanding Bottlenecks of SSMs" (6.0, accepted with uniform 6s) is a weaker paper in the same space — our paper has 3000+ runs vs. their moderate experiments, more actionable insights, and corrects prior published results. The "Architecture-aware scaling" paper (6.5, accepted) is comparable in experimental rigor but in a different domain.

**Final score: 6.5.** The paper provides a valuable empirical correction to the literature with impressive experimental scale (3000+ runs, 20K GPU hours). It is above the 6.0 anchors in thoroughness and impact, but below the 7.5+ anchors due to overclaimed framing ("mainly" optimization when the narrow LR window persists), synthetic-only benchmarks limiting practical scope, and lack of a proposed solution beyond diagnosis.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>