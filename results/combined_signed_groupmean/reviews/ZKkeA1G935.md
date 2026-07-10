Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper investigates whether LLMs can alleviate catastrophic forgetting in Graph Continual Learning (GCL). It makes three main contributions: (1) identifying a critical evaluation flaw in prior GCL work where "local testing" allows task ID leakage, inflating reported performance; (2) introducing LLM4GCL, a benchmark evaluating 9 methods across 7 textual-attributed graph datasets under corrected global testing; and (3) proposing SimGCL, a method combining first-session instruction tuning with frozen prototype classifiers.

## Strengths

- **Clear identification of a genuine evaluation flaw (Section 3.1, Table 1).** The paper convincingly demonstrates that the "local testing" setup in prior GCL work allows task ID to be predicted with 100% accuracy via simple mean pooling (Table 1, GNN+MP row), causing class-incremental learning to degrade into task-incremental learning and inflating reported performance. The evidence is clean, well-supported, and constitutes the paper's strongest contribution.

- **Comprehensive benchmarking.** The paper evaluates 9 methods across 7 TAG datasets under two settings (NCIL and FSNCIL) using standardized global testing, providing a practically useful benchmark for the community. The open-source LLM4GCL platform is a concrete infrastructure contribution.

- **SimGCL achieves strong results on several datasets.** On Cora, Citeseer, Photo, and Products, SimGCL dominates all baselines by large margins (e.g., +21.7% over SimpleCIL on Photo average accuracy, +15.1% on Products), demonstrating that instruction-tuned LLM backbones with frozen prototypes can be effective in dense-graph regimes.

## Weaknesses

### Major

- **SimGCL's backbone is not specified for the main results (Tables 2 and 3).** The paper never states which LLM backbone (e.g., RoBERTa-large, BERT-large) produces the central experimental claims labeled "SimGCL (Ours)." Figure 3 tests SimGCL across multiple backbones (B-small, B-medium, B-large, Ro-large) but Tables 2/3 do not identify which one was used. This makes the main results difficult to interpret (e.g., is SimGCL's advantage from method design or from using a larger backbone than the baselines?) and impossible to reproduce from the main paper alone.

- **SimGCL underperforms SimpleCIL substantially on Arxiv-23 (avg accuracy 38.7 vs 52.4, Table 2), and the paper's explanation is logically incomplete.** The paper attributes this to Arxiv-23's "sparse graph structure providing limited topological information." However, SimpleCIL does not use graph structure at all — it is a pure text-based method. If sparse structure were the problem, SimGCL should merely be no better than SimpleCIL, not substantially *worse*. This gap suggests the instruction tuning or graph prompts actively hurt performance on this dataset, but the paper does not investigate why. This weakens the claim that graph prompts uniformly improve LLM-based GCL.

### Minor

- **The headline "20% improvement over SOTA GNN-based baselines" conflates the advantage of LLM pretraining with continual learning method design.** The comparison pits a pretrained LLM (trained on massive text corpora) against GNNs trained from scratch. The more meaningful comparisons are against other pretrained models (SimpleCIL, BERT, RoBERTa, LLaMA), where SimGCL's margins are smaller and less uniform (e.g., it loses to SimpleCIL on Arxiv-23). This claim should be qualified.

- **No ablation isolating the contribution of graph prompts from first-session instruction tuning.** The comparison against SimpleCIL partially addresses this, but SimpleCIL uses a different protocol. An ablation of SimGCL without graph prompts (text-only instruction tuning + prototypes) would directly test whether graph-structural information or just first-session tuning drives improvements.

- **No variance or uncertainty reported.** None of the tables report standard deviations or confidence intervals. Given that several methods cluster within small margins on some datasets (e.g., Arxiv results), single runs do not support reliable fine-grained comparisons. At minimum, 3–5 seeds should be reported.

- **The scaling parameter τ in Eq. 2 is never given a value or ablated in the main paper.** This controls the sharpness of the prototype-matching distribution and could significantly impact results. Additionally, the LLM backbone for SimGCL in Tables 2/3 should be explicitly stated.

### Trivial

- **Inconsistent notation for the GCN+LLM-embedding baseline.** The same method is labeled "GCN<sub>Enh</sub>" (line 78), "GCN <sub>LLMEmb</sub>" (Table 2), "GCN <sub>LLM<sup>Emb</sup></sub>" (Table 3), and "GCN <sub>LLMemb</sub>" (Table 4) — four different notations for what appears to be the same method.
- **Observation numbering inconsistency.** The observations jump from ④→⑥→⑧ (missing 5 and 7 in the first pass), with 7 and 8 then appearing after ⑧. Minor editing artifact.

## Nice-to-Haves

- The paper scopes to rehearsal-free settings (Section 5), but including a single replay-based GNN baseline (e.g., GCN with episodic memory) would help calibrate how far SimGCL is from the upper bound of methods with data access.
- A discussion of SimGCL's inherent limitation — its frozen-backbone design cannot adapt to distribution shifts in later tasks — would improve the paper's intellectual honesty and help readers understand when the method is appropriate.

## Removed Points

- The critic claimed Obs numbering skips ❸ — this is factually incorrect; Obs ❸ exists at line 141. The numbering has minor inconsistencies (4→6→8 with 7 and 8 repeated) but these are trivial editing artifacts.
- The critic claimed SimGCL "does not perform continual learning in the adaptive sense" — this characterization applies equally to SimpleCIL and all rehearsal-free prototype-based methods in the benchmark. The paper is transparent about its design choice. Removed as a strawman criticism not specific to this method.
- The critic requested a replay-based baseline — the paper explicitly scopes to rehearsal-free settings (Section 5). Moved to Nice-to-Haves.
- Grammar/typo nitpicks ("overperform") — parser/formatting artifacts, removed.
- "The appendix (stripped) may contain this information" — kept only the main-paper self-containment concern; the appendix-origin part is removed per policy.
- Criticisms about missing related works, missing appendix proofs — removed per policy.

## Novel Insights

None beyond the paper's own contributions. The reviews surface granular concerns about reproducibility and logical completeness but do not add structural observations about the paper's approach that the paper itself does not already articulate.

## Suggestions

1. In the main paper, explicitly state which LLM backbone SimGCL uses for the results in Tables 2 and 3, and report the value of τ.
2. Add an ablation of SimGCL without graph prompts (text-only instruction tuning + prototypes) to isolate the contribution of graph-structural information.
3. Investigate why SimGCL underperforms SimpleCIL on Arxiv-23 — is the instruction tuning overfitting, or are the graph prompts introducing noise?
4. Report results over multiple seeds with standard deviations for key comparisons.
5. Qualify the headline "20% improvement" to clarify it compares against scratch-trained GNNs, not against other pretrained methods.

## Score and Decision

**Round 1 bracket (from calibration):** The paper's strongest contribution (evaluation flaw analysis + benchmark) places it above papers like "Online Continual Graph Learning" (5.0, rejected) which was penalized for lacking a novel method. It is comparable to "CLDyB" (5.67, accepted) and below "UB-GOLD" (6.5, accepted), having a stronger analytical finding but a less comprehensive benchmark.

**Anchors consulted:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/4sJJixGIZX.md` (avg 5.0, Round 1, itemized) — Online Continual Graph Learning. Lacks a novel method; penalized for limited contribution. Our paper has stronger contributions (evaluation flaw + method).
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/RnxwxGXxex.md` (avg 5.67, Rounds 1–2, itemized) — CLDyB benchmark for CL with PTMs. Similar hybrid paper (benchmark + analysis), accepted. Our paper has an additional evaluation-flaw finding that CLDyB lacks, but our method component is weaker.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/8QfK9Dq4q0.md` (avg 6.0, Round 2, itemized) — CIL via likelihood-ratio task prediction. Strong method paper on a related topic (task ID in CIL). Our paper has a different focus (graph CL) and a stronger evaluation analysis but a weaker method.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/g90RNzs8wX.md` (avg 6.5, Round 2, itemized) — UB-GOLD graph-level anomaly/OOD detection benchmark. More comprehensive (35 datasets) but mainly a unification benchmark without a flaw-discovery contribution.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gNoqEdT2wO.md` (avg 2.33, Round 1, not itemized) — Multimodal CIL benchmark. Rejected for limited contribution; our paper is substantially stronger.

**Final score placement:** The paper's strongest items (evaluation flaw: impact +10.00, benchmark: +9.98) are decisive strengths that put it above reject-range papers. Its two major weaknesses (missing backbone: -8.87, Arxiv-23 explanation: -10.00) are real but addressable. Compared to CLDyB (5.67, accepted), our paper has a sharper analytical finding but similar-scale method issues. The missing backbone raises the entry cost for reproducibility but does not invalidate the core flaw analysis, which is the paper's primary contribution. Calibrated against these anchors, a score of 6.0 reflects a paper with a genuine and well-supported contribution that is undermined by addressable but nontrivial presentation gaps.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>