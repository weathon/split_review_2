Now let me read the Discussion section and Stage II more carefully to verify the key claims:Now I have a thorough understanding of the paper. Let me draft the review.Now let me run Round 1 calibration — bracketing across score bands:Let me read the most relevant anchor papers to calibrate:Now let me read one more highly relevant anchor — the "Benchmark Inflation" paper (4.25):Now I have enough context to form my bracket and write the final review. Let me synthesize.

**Round 1 Bracket:** Based on the anchors, the paper under review is:
- Clearly above the 3.5–5.5 range (much stronger methodology than "Evading Data Contamination Detection" at 4.25)
- Comparable to the 5.5–7.5 range papers ("Detecting Pretraining Data" at 6.25, "How much can we Forget about Data Contamination?" at 6.75)
- Below the 7.5–8.5 range ("Training on the Test Task" at 8.0 has cleaner, more universally praised contributions)

**Initial bracket: 6.0–7.0**

Now let me produce the final review.

---

## Summary
This paper presents the first systematic study of benchmark contamination detection in Large Reasoning Models (LRMs), organized around two realistic attack vectors: Stage I (contamination during base-to-LRM transition via SFT followed by RL) and Stage II (contamination applied to already-capable LRMs via final SFT with CoT). The core finding is that PPO-style importance sampling and clipping in RL training actively conceals prior SFT contamination signals, and that SFT contamination with CoT on advanced LRMs leaves near-undetectable traces because LRMs generalize to distributionally similar non-member questions.

## Strengths

- **Stage I mechanistic ablation is genuinely novel and well-executed (Table 3, Figure 2).** The comparison between RAFT (no clipping), RAFT++ (with clipping), and GRPO (with/without clipping) isolates PPO-style clipping as the specific driver of contamination concealment. Table 3 shows that removing clipping from RAFT++ restores AUROC from 57.58% to 74.39% (a Δ of only −1.09 vs. −17.91 with clipping), and removing clipping from GRPO restores it from 61.26% to 73.28%. This moves beyond simply observing "RL makes detection harder" to identifying *which component* is responsible — a concrete, actionable finding.

- **The further-SFT control experiment rules out a key alternative hypothesis (Section 3.1, Figure 2).** The paper demonstrates that continuing SFT on the contaminated model with clean data does *not* reduce detection AUROC, while GRPO does. This is a necessary control that the paper includes and executes well: "further SFT is unable to conceal the benchmark contamination, while the pass@1 would continue to rise" (line 136).

- **Comprehensive evaluation breadth.** Ten detection methods spanning five categories (generation-based, perturbation-based, reference-based, embedding-based, reference-free), six benchmarks, two base models for Stage I, and four LRMs for Stage II. The finding is robust across methods and benchmarks, not cherry-picked.

- **Theory (Theorem 3.1) provides a useful supporting framework.** The decomposition of NLL drift into a mean-push term μ(x) and a covariance-reweighting term β(x), with the argument that clipping makes β more negative for non-members, offers a concrete mechanistic story that aligns qualitatively with the empirical ablation. While simplified, it plays its supporting role well.

## Weaknesses

### Fatal
None

### Major
- **Stage II interpretation confound: detection "failure" vs. correct reporting of genuine generalization.** In Stage II, members and non-members are random halves of the same benchmark (Section 3, line 52). The paper's key observation is that after SFT contamination with CoT, both members' and non-members' log-probabilities increase by a similar margin (Figure 4). The paper frames this as detection "fragility," but there is a critical ambiguity: when an already-capable LRM is fine-tuned on half of an in-distribution benchmark with full chain-of-thought supervision, generalization to the other half is expected behavior. The paper's Discussion (line 330) acknowledges this: "This confounding factor (i.e. generalization) is not accounted for by existing detection approaches." However, the paper does not adequately separate two distinct conclusions: (a) detection methods are fundamentally broken for LRMs, or (b) detection methods are correctly reporting no differential treatment because the model genuinely learned rather than memorized. This matters because the practical threat of contamination depends on whether performance gains are specific to seen items (cheating) or general capability improvement (legitimate learning). The performance inflation in Table 4 (e.g., +11.76% for DS-Llama-8B) could partly reflect genuine learning. Without testing non-members from a truly different distribution, the Stage II claim remains interpretively ambiguous.

### Minor
- **Theory-experiment data setting mismatch.** The theoretical analysis (Section 3.2, line 188) assumes "RL training is performed on the benchmark data (i.e., training data is the combination of members M and non-members N)," but the primary Stage I experimental finding uses *clean* RL data from DeepMath-103K (line 91). The theory thus analyzes a different data regime than the most interesting experimental result (GRPO with clean data concealing contamination). The paper does not discuss whether the theoretical predictions would differ when RL data is entirely non-benchmark.

- **"Broad class of RL methods" slightly overclaimed.** The abstract states "a broad class of RL methods may inherently exhibit similar concealment capability," but only GRPO, RAFT, and RAFT++ are tested (Table 3). The theoretical argument that any method using importance sampling and clipping should exhibit concealment is plausible, but DPO-family methods do not use clipping, and PPO with a learned value function has different variance properties. The claim should be explicitly scoped to methods with PPO-style clipped objectives.

- **"Near random guesses" framing slightly overstated for Stage II.** While the overall average AUROC across all methods/models in Table 5 is close to 50%, specific method-model pairs achieve mid-60s (e.g., LiRA on DS-Qwen-14B: 65.55%, Min-K% on DS-Llama-8B: 62.42%). The blanket "near random guesses" framing in the abstract and Section title obscures this variation.

### Trivial
None

## Nice-to-Haves
- Test Stage II detection with out-of-distribution non-members (from a different domain or difficulty level) to cleanly separate detection failure from generalization — this would be the single most impactful addition.
- Directly measure the intermediate covariance terms (β) from Theorem 3.1 for members vs. non-members to bridge the gap between theoretical prediction and empirical validation.
- Test partial/selective contamination (e.g., 5–10% of hardest questions) to assess whether findings hold under more strategic and realistic attack patterns.
- Quantify the contamination-strength vs. RL-steps tradeoff: how many GRPO steps are needed to reach chance-level detection as a function of initial contamination intensity?
- Discuss expected scaling behavior beyond 7B–14B models, given that larger LRMs may generalize even more readily from contamination data.

## Removed Points
*These points are flagged to be removed, treat them with caution:*

- **"Releasing intermediate checkpoints is naive as a defense"** — This is a critique of a future-directions suggestion in the conclusion (line 334), not of the paper's core contribution. The paper is an empirical vulnerability study, not a defense proposal. Removed as out-of-scope critique.
- **"Missing watermarking/fingerprinting-based detection approaches"** — The paper explicitly focuses on memorization-based detection methods (the dominant paradigm). Requesting fundamentally different detection families is scope creep.
- **"Missing analysis of why RL contamination is less effective than SFT contamination"** — The paper's scope is detection evasion, not contamination effectiveness. This is a suggestion for future work, not a weakness of the current contribution.
- **"The paper evaluates only 7B-14B models"** — This is standard for empirical LRM studies at this scale. Demanding larger models is a generic scope-expansion request that doesn't threaten the core claims.

## Novel Insights
The paper's most genuinely novel insight is the mechanistic identification of PPO-style clipping as the specific RL component responsible for concealing contamination signals. The key empirical finding — that plain rejection sampling (RAFT) preserves detection performance while its clipping-augmented variant (RAFT++) degrades it — combined with the theoretical decomposition showing how clipping makes the covariance term β more negative for non-members, provides an actionable understanding of *why* RL training makes contamination harder to detect. This goes beyond prior work that either observed detection failures or proposed evasion attacks, by pinpointing the algorithmic mechanism.

## Suggestions
- **Most impactful:** Test Stage II with out-of-distribution non-members. If detection recovers, the finding clarifies that Stage II is about in-distribution generalization; if it still fails, the contribution becomes much stronger.
- Explicitly scope the "broad class of RL methods" claim to "methods with PPO-style clipped objectives" throughout the paper.
- Compute empirical β terms from Theorem 3.1 to bridge the theory-experiment gap.
- Soften the "near random guesses" framing for Stage II to "near or at random guessing on average, with modest but weak detection for specific method-model pairs."
- Discuss the theory-experiment data mismatch (clean RL vs. benchmark RL) and whether predictions change.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| "NEMESIS: Jailbreaking LLMs" | 5kMwiMnUip | 1.40 | R1 | Fundamentally weak; far below paper under review |
| "Systematic Review of LLMs" | 8QTpYC4smR | 1.00 | R1 | Survey with no contribution; not comparable |
| "Instruction Following is not all you need" | RuY1r1PDdQ | 3.00 | R1 | Lacks technical depth; paper under review is much stronger |
| "Sparse Watermarking in LLMs" | jbfDg4DgAk | 3.00 | R1 | Different topic but similar reject-level quality; paper under review is superior |
| "Evading Data Contamination Detection" | Nk1MegaPuG | 4.25 | R1 | Most directly related predecessor — same topic (evasion of contamination detection). Paper under review is substantially deeper with mechanistic ablations and theory |
| "Benchmark Inflation: Retro-Holdouts" | rAylWUIKtu | 4.25 | R1 | Narrow scope (single benchmark), methodology concerns. Paper under review is broader and more rigorous |
| "Detecting Training Data via EM" | asA7vvsgcI | 3.75 | R1 | MIA method paper with missing experiments. Different contribution type |
| "Leveraging Set Assumption for MI" | HozsY9Gdcl | 5.00 | R1 | Solid but limited method paper; paper under review has broader scope and clearer contribution |
| "Detecting Pretraining Data (Min-K%)" | zWqr3MQuNs | 6.25 | R1 | Accepted; proposes novel method with clear utility. Paper under review is comparable in rigor but different in type (vulnerability study vs. method proposal) |
| "Infilling Score" | 9QPH1YQCMn | 6.25 | R1 | Accepted; novel detection method. Paper under review contributes at similar quality level |
| "To the Cutoff... and Beyond?" | m2NVG4Htxs | 6.75 | R1 | Accepted; thorough longitudinal analysis. Comparable rigor to paper under review |
| "How much can we Forget about Data Contamination?" | Nsms7NeU2x | 6.75 | R1 | Rejected despite high scores; similar profile (empirical study + theory with gap). Paper under review has stronger mechanistic contribution but weaker Stage II |
| "RM-Bench" | QEHrmQPBdd | 8.00 | R1 | Accepted with strong scores; more polished contribution. Paper under review's Stage II weakness prevents reaching this level |
| "How much of my dataset" | EUSkm2sVJ6 | 7.60 | R1 | Accepted; novel quantitative framework. More technically complete than paper under review |
| "LOKI" | z8sxoCYgmd | 8.00 | R1 | Accepted; comprehensive benchmark. Paper under review doesn't reach this polish |
| "Training on the Test Task" | jOmk0uS1hl | 8.00 | R1 | Accepted with unanimous 8s; cleaner and broader contribution. Paper under review is below this level |

**Round 1 bracket: 6.0–7.0**

**Narrowing rationale:** The paper's Stage I contribution (mechanistic identification of PPO-style clipping as the contamination concealment driver) is genuinely novel, well-supported by ablations and theory, and practically important. This places it above the borderline-reject contamination papers (4.25 range). However, the Stage II interpretation confound — where the paper cannot disentangle detection failure from genuine generalization — weakens approximately half the paper's narrative. The "broad class of RL methods" overclaiming and "near random guesses" overstatement are minor but compound. Compared to accepted papers in the 6.25–6.75 range (Min-K%, "To the Cutoff"), the paper under review has a comparably strong core contribution but a weaker second half. I place it at 6.5 — borderline accept with a clear path to strengthening through the suggested out-of-distribution non-member experiment.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>