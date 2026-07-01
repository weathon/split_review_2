## Summary

MoRE (Mixture of Remapping Experts) proposes a training-free feature-level unlearning framework with three components: (i) prototype-orthogonal (PO) projection that decorrelates forget/remain prototypes before editing, (ii) a remapping mechanism that redirects forget features toward remain prototypes to impede recovery, and (iii) efficient activation-mean prototypes achieving O(Nd) time and O(dk) memory. The PO projection is mathematically clean and demonstrably effective (ablation in Table 3 shows HM rising from ≈88.6 to ≈99.7 on CIFAR-10 after adding PO to erasure). The remapping idea — making forget features indistinguishable from remain features rather than merely absent — is a genuine conceptual advance over prior subspace-erasure approaches.

## Strengths

1. **Well-motivated and clean mathematical formulation of PO projection.** The observation that forget/remain prototypes are highly correlated (cosine similarities ~0.5 in Fig. 3) and that naively erasing correlated prototypes degrades utility is empirically grounded. The pseudoinverse construction (Eq. 2) and the complement-space skip connection (Eq. 4) are technically sound. The ablation in Table 3 provides unambiguous evidence: adding PO raises Erase HM from 88.62 to 99.68 on CIFAR-10. This is the paper's strongest technical contribution.

2. **Remapping as a conceptual advance over erasure.** Extending erasure to active remapping (Eq. 6) — detecting forget-prototype presence and redirecting toward remain prototypes — addresses the residual-cluster problem that ESC leaves behind (visible in Fig. 1's t-SNE). The paper correctly identifies that erasure alone leaves forget features separable, and that remapping them into the remain distribution is a principled solution. This is a genuine insight that goes beyond prior subspace-based methods.

3. **Impressive efficiency and scalability.** Reducing unlearning to a single forward pass with O(Nd) time and O(dk) memory is a significant practical advantage. Fig. 5 reports under 10 seconds and <200 MB for CIFAR-10/100, which is credible and important. Training-based methods require orders of magnitude more compute, making MoRE attractive for deployment even if its absolute performance were merely competitive.

## Weaknesses

### Fatal

None. The core technical contributions (PO projection, remapping framework) are valid and demonstrated. The overclaiming and missing evaluations are serious but addressable.

### Major

1. **The "irreversible" and "exact" claims are not supported by the evidence provided.** The paper uses "irreversible" in the title, abstract, introduction, method sections, and conclusion (lines 9, 43, 58, 65, 83, 88, 106, 180, 253, 364). "Exact" appears once in the abstract (line 9). The sole evidence for irreversibility is the KR evaluation with a single fine-tuning setting (lr=0.1, shown in Table 1 and Table 3). This tests one mild adversary. The paper does not report:
   - Recovery accuracy under varying attack strengths (higher learning rates, more epochs, different optimizers).
   - Linear probing experiments, despite claiming (lines 82, 120, 180, 364) that MoRE "significantly impedes recovery through fine-tuning or linear probing."
   - Any formal bound on residual information.
   - Feature-space attacks beyond fine-tuning (e.g., k-NN, clustering-based recovery).

   The paper mentions "additional learning rate configurations" are in the appendix, but the main paper's claim of irreversibility rests on a single point of evidence. Claiming "irreversible" unlearning from a single mild recovery attempt is not justified. The method may well provide stronger resistance than ESC, which is a genuine contribution — but the evidence as presented does not support the headline claim.

2. **No linear probing experiments, despite repeatedly invoking linear probing as a threat model.** Lines 82, 120, and 180 each state that remapping makes recovery via linear probing significantly harder, yet no linear probing results appear anywhere in the main paper. This is a directly testable prediction of the method's claimed mechanism and should have been evaluated. The KR metric (fine-tuning) is related but not identical to linear probing.

3. **Overclaimed diffusion model results.** The paper states (line 326) that MoRE "outperforms SOTA diffusion model unlearning methods both quantitatively and qualitatively." Table 2 shows Ours achieves the best LPIPS_d tradeoff metric (0.25 for Van Gogh, 0.26 for Kelly McKernan), but **does not** achieve the best individual LPIPS_f or LPIPS_r. For Van Gogh removal: SAFEE achieves LPIPS_f=0.42 vs Ours 0.33 (where higher LPIPS_f is better per line 276). The claim should be that MoRE achieves the best tradeoff — "outperforms" is too strong and not supported by the data.

4. **No limitations or broader impact section.** The paper makes strong claims ("irreversible," "exact," "outperforms SOTA") but includes no discussion of the method's own limitations. The only "limitations" discussed are those of the ESC baseline (line 106). Given the centrality of the irreversibility claim and the clear trade-offs evident in the ablation results, the absence of a limitations section is a notable omission.

### Minor

1. **The utility-irreversibility trade-off is under-acknowledged in the ablation narrative.** Table 3 shows that with PO, simple Erase achieves HM=99.68 while Remap achieves HM=95.38 and MoRE achieves HM=95.23 — a ~4.3 point utility drop for the remapping variants. The ablation section (lines 330-332) correctly states that PO "yields the strongest results" (comparing PO vs no-PO), but does not explicitly state the trade-off that if a practitioner cares only about standard unlearning metrics (not recovery resistance), Erase+PO is superior. Remapping trades standard utility for irreversibility. Making this transparent would strengthen the paper.

2. **MoRE's advantage over single-expert Remap is narrowly concentrated.** In the standard (non-KR) setting (Table 1), Remap and MoRE achieve nearly identical HM (95.38 vs 95.30 on CIFAR-10). The benefit of multiple experts is visible primarily in the HM_f KR metric (33.20 vs 10.79). The paper should more clearly characterize where the MoE component matters and where it does not.

3. **The full-orthogonality simplification (footnote, line 168) could affect utility.** The footnote acknowledges that full mutual orthogonality (rather than only forget-remain orthogonality) is adopted "for mathematical brevity." This means the PO projection may introduce unnecessary distortions among remain prototypes, potentially explaining the HM degradation observed in remapping variants. This design choice and its implications deserve main-text discussion, not a footnote.

4. **Sensitivity to layer choice.** Table 7 shows that applying the method at the third-last layer substantially degrades performance (e.g., CIFAR-10 Erase D_f jumps from 0.95 to 46.30). This is mentioned briefly (line 358) but warrants more analysis and discussion, given that practical deployment requires knowing which layers to target.

### Trivial

None.

## Nice-to-Haves

- Test recovery resistance under multiple attack strengths (learning rates from 0.01–1.0, varying epochs, different optimizers, linear probing with varied regularization). If MoRE degrades recovery across all these, that would be a strong and honest result.
- Report direct measurements of feature-space cohesion (e.g., average pairwise distances within the forget feature set before/after unlearning) to verify the claimed mechanism.
- Ablate the cost of full- vs. selective-orthogonality to quantify the distortion introduced by the current simplification.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Zero-variance entries in tables (0.00 ± 0.00).** The extracted text has parser-induced formatting artifacts that make it impossible to verify whether standard deviations were reported or suppressed. Per policy, formatting/parser issues are not author errors.
- **Baseline comparisons are unfair because Finetune/NG/RL show near-zero D_r.** This is a known characteristic of these baselines in the unlearning literature (fine-tuning on forget data with random labels typically collapses the model). The paper includes them for completeness following established practice. This is not a sign of unfair tuning, though the paper could add a note explaining this behavior.
- **ImageNet results omitted from main text.** The paper states (line 243) that full results including ImageNet are in Appendix §C.1. The appendix is stripped by the parser; per policy, missing appendix content is not a valid criticism.
- **Contradiction between Fig. 7 and Table 1 regarding single-expert performance.** The figure is evaluated under the KR setting while the standard-setting comparison is non-KR. The paper's statement about single-expert "dip in performance" refers to the KR setting, where the data supports it (HM_f 33.20 vs 10.79). There is no direct contradiction.

## Novel Insights

The key novel observation from consolidating these reviews is that the paper's strongest technical contribution (PO projection) is decoupled from its most ambitious claim (irreversibility). The PO projection demonstrably solves a real problem — correlated prototypes causing utility degradation during subspace erasure — and this alone is a publishable contribution independent of the irreversibility framing. The remapping mechanism is a natural extension that is conceptually appealing, but its value depends on whether practitioners actually face the recovery threat it addresses. The review process has not surfaced any challenge to the correctness of the math or the validity of the core empirical results; the issues are uniformly about over-interpretation and insufficient boundary testing.

## Suggestions

1. **Replace "irreversible" with "recovery-resistant" or "strongly irreversible" throughout**, and remove "exact" from the abstract unless formal guarantees are provided. Characterize what recovery attacks the method resists and where it starts to fail.
2. **Report linear probing results** — this is a directly testable, low-cost experiment that would either confirm or refute the paper's stated mechanism.
3. **Add a limitations section** discussing: (a) the single-attack evaluation of irreversibility, (b) the utility cost of remapping vs. erasure, (c) sensitivity to layer choice, (d) the full-orthogonality simplification, and (e) the narrow benefit of the MoE component.
4. **Tone down the diffusion model claim** to "achieves the best overall tradeoff (LPIPS_d) and competitive individual metrics."

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>