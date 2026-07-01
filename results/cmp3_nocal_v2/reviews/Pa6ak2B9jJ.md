## Summary

This paper proposes AUTO-RT, a reinforcement learning framework for automated red-teaming of LLMs that formulates jailbreak prompt generation as a sequential decision process. The key innovations are: (1) a hierarchical decomposition of attack generation into strategy generation (AM^g) and strategy rephrasing (AM^r), enabling strategy-level exploration beyond fixed templates; (2) Dynamic Strategy Pruning (DSP) to eliminate redundant exploration branches; and (3) Progressive Reward Tracking (PRT) with a First Inverse Rate (FIR) metric to select downgrade models for reward shaping. Experiments are conducted across 16 white-box and 2 black-box LLMs.

## Strengths

1. **Hierarchical decomposition of attack generation (AM^g + AM^r) is a well-motivated architectural choice.** Section 2.2 (Equation 2) cleanly separates the problem into learning reusable high-level attack strategies and instantiating them for specific toxic intents. This is a genuine structural departure from the fixed-template paradigm and enables generalization across toxicity intents that per-intent optimization does not.

2. **FIR-based downgrade model selection (Section 2.3.3) is a novel contribution to reward shaping for adversarial prompt generation.** The insight that the "first inverse" in a sequence of progressively weakened models marks the point where the downgrade model becomes informative without being misleading is a non-obvious heuristic. Figure 4 — where attack performance peaks just before the FIR spike — provides reasonable supporting evidence for this specific claim.

## Weaknesses

### Major

1. **The main comparison (Table 1) is against baselines too weak to support the central claim of state-of-the-art effectiveness.** Table 1 compares AUTO-RT only against DA (direct attack), Few-Shot (FS), Imitation Learning (IL), and a basic PPO-based RL baseline. The paper's own Related Work (Section 4) catalogs substantially stronger automated methods — PAIR, TAP, AutoDAN, GCG, Rainbow-Teaming, Cold-Attack, CRT, Diver-CT — none of which appear in the main comparison. CRT and Diver-CT are the closest relatives (they also use RL for red-teaming, Section 4, lines 261–275) yet are not compared even though the paper cites them. The one place where a stronger baseline *is* compared (Table 3, against AutoDAN) tells a different story: **AutoDAN achieves ASR_rst of 55.23%, while AUTO-RT achieves 38.38%.** The paper frames this as "near-human-level sustained attack capabilities" (line 251) by pivoting to DeD (defense generalization), but the abstract and introduction emphasize *effectiveness* — discovering jailbreaks — not specifically sustained attacks against defenses. The 16.63% improvement claimed in the abstract is computed against the weak Table-1 baselines only. The central claim of superior attack effectiveness is not supported by comparisons against the strongest relevant prior work.

2. **The evaluation metric ASR_st is ambiguous and potentially inflated.** Equation 6 defines ASR_st as "the average ASR of the top 100 strategies with the highest ASR on $\mathcal{T}_{\text{st}}$." The paper defines $\mathcal{T}_{\text{tm}}$ (training split) and $\mathcal{T}_{\text{ts}}$ (test split) in Section 3.1 (line 127), but $\mathcal{T}_{\text{st}}$ is not defined — it appears to be a formatting artifact for $\mathcal{T}_{\text{ts}}$ (test set). If the top 100 strategies are selected based on their ASR *on the test set* and then re-evaluated on that same test set, this is circular and overestimates performance. Even if selection is on the training set and the subscript is a formatting error, reporting only the top-100 average inflates results relative to the mean across all generated strategies. The paper does not report what fraction of total generated strategies $S_{100}$ represents, nor the mean ASR across *all* strategies. Without this, it is impossible to assess how much selection bias contributes to the reported numbers.

3. **Severity is invoked as a core motivation but never measured.** The introduction (lines 15–28 and 58–64) repeatedly frames the problem as a failure of prior work to jointly optimize for exploitability *and* severity, arguing that the most important vulnerabilities combine both. However, the evaluation contains no metric that measures severity. The safety classifier (Llama-Guard2-8B) produces a binary safe/harmful judgment, not a severity score. The three evaluation dimensions (effectiveness, efficiency, diversity) all measure exploitability or coverage, not harm severity. No differential measurement of high-severity vs. low-severity outputs is presented, and no analysis shows that AUTO-RT discovers higher-severity flaws than baselines. This is a structural gap between the paper's motivational framing and its experimental evaluation.

### Minor

4. **PRT reward scheme has an undefined case.** Equation 4 defines $R_s$ for three cases ($R_{\text{TM}'}=0 \Rightarrow 0$; $R_{\text{TM}'}=1, R_{\text{TM}}=0 \Rightarrow 1$; $R_{\text{TM}'}=1, R_{\text{TM}}=1 \Rightarrow 2$) but does not define the fourth — $R_{\text{TM}'}=0, R_{\text{TM}}=1$ (downgrade model says safe while target model is actually jailbroken). The paper states (line 93) that "most cases with $R_{\text{TM}'}=0$ also yield $R_{\text{TM}}=0$," but this is an empirical claim; when the case occurs, the reward would be 0 (by the first rule), which gives no credit for an actual jailbreak. This is a methodological gap in the reward design.

5. **AutoDAN comparison table (Table 3) has a blank SeD value for AUTO-RT** (line 248). The semantic diversity score for the proposed method is conspicuously omitted with no explanation.

6. **DSP penalty values are not specified.** The paper claims (line 85) that when the penalty $C(f_i, c_i)$ is "sufficiently small" (a condition it says "is easy to satisfy in practice"), the optimal policy of the modified CMDP coincides with the original. However, the paper does not state what penalty values are used or whether this condition is verified, making the theoretical guarantee hollow.

7. **DeD (defense generalization) construction is underspecified.** The metric is described (line 152) as "constructing defenses based on the successful attacks" without describing the defense mechanism. This makes the metric difficult to interpret or reproduce.

8. **No variance or statistical significance reported for key tables.** Tables 1, 2, 3, and 4 report point estimates only. The violin plots (Figure 3) show variance for a subset (four models, vs. RL only), but the primary comparison tables lack any confidence intervals or significance tests. Given that RL training typically has high variance, readers cannot assess which differences are meaningful.

### Trivial

None.

## Nice-to-Haves

- **Compare against CRT and Diver-CT in the main table.** These are the closest RL-based competitors cited in the Related Work, and including them would directly test whether the strategy-level decomposition (versus prompt-level RL) provides the claimed benefit.
- **Add a severity measure or reframe the motivation.** Since severity is invoked as a key motivation, either (a) add a graded harm classifier or human annotation to measure severity of successful jailbreaks, or (b) remove severity from the motivational framing and focus the paper on exploitability and diversity, which is what the evaluation actually measures.
- **Clarify the ASR_st metric** by reporting what fraction of total strategies the top-100 represents, the mean ASR across all generated strategies, and whether the top-100 selection is based on training or test performance.
- **Address the missing case in Equation 4** either by providing evidence it never occurs or by defining the reward for that case.
- **Test against proprietary black-box models** (e.g., GPT-4, Claude) to strengthen the claim of black-box applicability, since the current black-box evaluation uses open-weight models (Llama3-70B, Qwen2.5-72B) with ICL.

## Removed Points

These points were flagged in the input but are removed with brief justification:

- *Allspaw & Cook citation mismatch* — The citation is used to support a general claim about complex systems leaving vulnerabilities undiscovered; this is a reasonable use of a general systems safety reference. Removed as a minor citation nitpick.
- *FIR metric is a heuristic with underdeveloped theory* — The paper provides empirical evidence (Figure 4) and does not claim a rigorous theoretical derivation; the heuristic nature is transparently stated. Removed as demanding a level of theoretical depth not promised by the paper.
- *Black-box evaluation uses open-weight models, not proprietary ones* — The paper explicitly states it is simulating black-box settings via ICL. This is a scope-boundary issue, not a flaw. Removed per scope-creep rule.
- *Weakness about missing appendix content* — The parser strips appendices from all papers; criticisms about absent details that may be in the appendix are removed per hard rules.
- *Strength about "addressing an important problem"* — Generic; not grounded in specific content. Removed.
- *Section-by-section notes that are purely descriptive* — Removed per filtering rules.

## Novel Insights

The harsh critic's main novel insight beyond the paper's own contributions is the observation that the severity-extrinsic motivation is empirically unoperationalized — the paper argues for joint optimization of exploitability and severity but evaluates only exploitability and diversity. This gap between framing and evidence is a non-obvious structural critique that the paper itself does not surface. Additionally, the critic correctly identifies that the one strong-baseline comparison (AutoDAN) reverses the paper's headline claim on the primary metric, which is a tension the paper's narrative glosses over.

## Suggestions

1. Add at least one strong RL-based baseline (CRT or Diver-CT) and one strong attack method (AutoDAN) to Table 1, or substantially weaken the "state-of-the-art effectiveness" claim to reflect the actual comparison scope.
2. Either add a severity measure (graded harm classifier, human rating on a subset) or remove severity from the paper's motivational framing.
3. Clarify the ASR_st metric: specify whether top-100 selection is on training or test data, report the mean ASR across all generated strategies, and state what fraction of total strategies the top-100 represents.
4. Fill the blank SeD cell for AUTO-RT in Table 3 and explain the omission.
5. Specify the penalty values used in DSP and verify the "sufficiently small" condition empirically.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>