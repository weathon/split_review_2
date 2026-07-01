## Summary

This paper identifies a novel and practically important problem: test-time adaptation (TTA) of vision-language models (VLMs) under long-tailed test distributions. The authors propose L-TTA, comprising three co-designed components—Synergistic Prototypes (SyPs) with Deterministic and Exclusionary Prototypes to enrich tail class representations, Rebalancing Shortcuts (RSs) with a class-reallocation loss to dynamically balance prototypes, and Balanced Entropy Minimization (BEM) to counteract head-class bias in standard entropy minimization. Extensive experiments on 15 datasets across three benchmarks with varying imbalance ratios show consistent improvements over 12 recent baselines in both accuracy and macro-F1, along with competitive computational efficiency.

## Strengths

- **Novel and well-motivated problem formulation.** This is the first work to systematically study long-tailed TTA for VLMs, a realistic scenario where existing TTA methods break down. The paper identifies and clearly illustrates two VLM-specific failure modes (text-induced tail erosion and modality-bias amplification) that justify the need for new designs beyond simply porting unimodal long-tailed or non-i.i.d. TTA methods.

- **Three complementary components with solid ablation support.** SyPs (DPs + EPs), RSs with class re-allocation, and BEM are each well-motivated by specific weaknesses of prior approaches. The ablations in Table 6 confirm that all three components contribute positively and synergistically, and the sensitivity analyses on λ₁, λ₂, η, K, and β show the method is reasonably robust to reasonable hyperparameter choices.

- **Extensive and rigorous experimental evaluation.** The authors evaluate on 15 datasets across three distinct benchmarks (OOD, cross-domain, corruption), three imbalance ratios (10, 20, 50), and 12 strong baselines. Results are reported with both accuracy and macro-F1, and the gains are consistent and often substantial (e.g., +1–3% accuracy, +2–3% macro-F1 on averaged metrics). The efficiency study (Table 4) and backbone scaling experiments (Table 5) further demonstrate practical viability.

- **Theoretical propositions for BEM.** Propositions 1 and 2 provide formal reasoning about why standard EM biases head classes and how the proposed BEM reduces the gradient gap between head and tail classes. This theoretical grounding strengthens the objective contribution.

## Weaknesses

### Fatal
None.

### Major

- **Artificially constructed long-tailed test sets.** The long-tailed distributions are created by randomly subsampling from originally balanced datasets. While this is a standard practice in long-tailed learning research, it may not fully capture characteristics of naturally long-tailed test distributions (e.g., correlations between frequency and visual difficulty, domain structure). This limits ecological validity and leaves open whether the gains would transfer to truly long-tailed test scenarios like those encountered in wild deployment.

- **Missing comparison with simpler baselines combining TTA + post-hoc logit adjustment.** The paper argues that simply adding logit adjustment to EM would exacerbate bias (and Proposition 1 supports this), but it does not empirically evaluate even a straightforward baseline: running a competitive TTA method (e.g., TDA or DPE) and then applying standard logit adjustment (Menon et al., 2020; Ren et al., 2020) based on running class frequency estimates from the test stream. Such a baseline would help isolate the benefit of the specifically proposed components (SyPs, RSs, BEM's confidence-weighted penalty) over this simple alternative, and would strengthen the claim that BEM's design is necessary.

- **The method has many moving parts and hyperparameters.** L-TTA requires setting: two EMA thresholds (θ and its decaying rule), an affinity function with two hyperparameters (λ₁, λ₂), the number of hyper-class vectors K, and a penalty factor β, plus the balance factor η. While the ablation studies explore each individually, the overall configuration space is large. In practice, this could make adoption difficult without clear guidelines for tuning on new datasets.

### Minor

- **Proposition 2's practical significance is not empirically verified.** The proposition claims BEM shortens the gradient gap between head and tail classes, but no experiment measures actual gradient magnitudes during adaptation to confirm this mechanism is responsible for the observed improvements. A simple gradient norm comparison during TTA would strengthen the theoretical claim.

- **Limited discussion of why non-i.i.d. TTA methods (LAME, DA-TTA, SAR, DELTA) are insufficient for this setting.** The paper briefly mentions that applying unimodal methods like SAR to VLMs causes modality-bias amplification (Figure 1b.2), but these methods are not included as baselines in the main tables. Including one or two representative non-i.i.d. TTA baselines adapted to the VLM setting would concretely demonstrate the need for the proposed bi-modal approach.

- **Notation density in Section 3.1.** The formal definition of layer-wise features (Equation 1) is heavy for a TTA paper and could be simplified to focus on the key inputs (visual/text embeddings, logits) without loss of clarity.

### Trivial
None.

## Nice-to-Haves

- Add a baseline that applies a leading TTA method (e.g., TDA) followed by post-hoc logit adjustment using running class frequency estimates from the test stream.
- Evaluate on naturally long-tailed datasets (e.g., iNaturalist subsets) where the class distribution is inherent, to strengthen ecological validity.
- Provide gradient norm measurements during adaptation to empirically validate the claim of Proposition 2.
- Discuss practical guidelines for hyperparameter selection (e.g., η around 1, β around 1, K around 0.2–0.4 fraction of classes) based on the sensitivity results.

## Novel Insights

Beyond the paper's own contributions, the most insightful analysis is the identification of two failure modes unique to VLM-based long-tailed TTA: (1) text-induced tail erosion, where the textual modality carries inherent biases that compound the long-tailed problem when "rich classes" coincide with head classes, and (2) modality-bias amplification, where unimodal long-tailed methods destabilize the visual-textual alignment in VLMs. These observations suggest that future TTA methods for VLMs must explicitly manage cross-modal balance, not just per-class frequency, which differs from traditional long-tailed learning wisdom.

## Suggestions

- Add a baseline that applies a strong TTA method (e.g., TDA) and then performs logit adjustment using test-time class frequency estimates. This would clarify whether the main benefit comes from the specific components or simply from re-calibrating with estimated priors during TTA.
- Consider evaluating on at least one naturally long-tailed test set (e.g., derived from iNaturalist or Places-LT) to demonstrate the method works beyond artificially constructed distributions.
- Include a brief experiment measuring the gradient norms of head vs. tail logits under standard EM vs. BEM to confirm the mechanism stated in Proposition 2.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>