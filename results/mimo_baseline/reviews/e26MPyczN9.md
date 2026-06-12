## Summary

This paper re-evaluates prior claims that programmatic policies generalize better than neural policies in RL across three benchmarks (TORCS, Karel, Parking). The authors show that much of the reported OOD generalization gap arises from experimental confounds—such as reward function design and observation space choices—rather than inherent representational advantages. They propose a conceptual framework distinguishing *expressivity* (whether the policy space contains a generalizing solution) from *discoverability* (whether the search algorithm can find it), and identify tasks requiring instance-scaling working memory as the class where programmatic representations have a genuine structural advantage over fixed-capacity neural architectures.

## Strengths

- **Convincing confound identification across multiple benchmarks.** The TORCS re-evaluation (Table 1) clearly demonstrates that de-emphasizing speed via a cautious reward (β=0.5) enables neural policies to generalize to OOD tracks (76% and 69% success from G-TRACK-1; 100% from AALBORG), matching programmatic policies. The Karel re-evaluation (Table 2) shows that augmenting observations with the last action and using a simpler fully connected network achieves perfect generalization on 4/5 tasks at 100×100 scale, outperforming both LSTM and ConvNet baselines.

- **Clear and useful conceptual framework.** The expressivity/discoverability distinction (Definitions 2 and 3) provides a principled vocabulary for analyzing representation comparisons in RL. The paper correctly observes that the DSLs used in prior work induce policy spaces similar to neural networks, so both are expressive—differences in observed generalization stem from discoverability (search effectiveness), which is domain-specific and confounded by training details.

- **Identifies a genuine structural limitation of fixed-capacity neural architectures.** The argument that pathfinding and nested subproblems require working memory growing with input size—and that feedforward/recurrent models with fixed hidden dimensions cannot represent such solutions—is well-grounded in computational complexity theory. The FUNSEARCH proof-of-concept successfully synthesizing BFS for a wall-sparse maze variant provides concrete evidence.

- **Honest and careful positioning.** The paper appropriately calls the FUNSEARCH experiment a "proof-of-concept," acknowledges the difficulty of controlling for discoverability, and notes where its results are mixed (PARKING). It does not overclaim.

## Weaknesses

### Fatal
None.

### Major

- **TORCS generalization success rates are inflated by survivorship bias.** Of 30 seeds trained with β=0.5 on G-TRACK-1, only 13 learned to complete the training track at all. The reported generalization rates (76%, 69%) are computed over only these 13 successful models, not over all 30. The 17 models that failed to learn at all represent a substantial failure rate that undermines the claim that neural policies "match" programmatic ones. A fair comparison should report generalization rates over all seeds (roughly 33% and 30%), which would paint a less favorable picture.

- **The instance-scaling memory argument lacks empirical support beyond a single synthetic proof-of-concept.** The paper's most important forward-looking claim—that tasks requiring growing memory represent the genuine differentiator—is supported only by FUNSEARCH generating BFS on a hand-designed wall-sparse maze. No experiments show neural policies actually failing on such tasks due to memory limitations, nor is there evaluation on real-world benchmarks like NetHack that the paper invokes. The argument would be substantially stronger with even one experiment demonstrating neural failure on a memory-scaling task.

### Minor

- **The expressivity/discoverability framework, while useful, is not deeply novel.** The distinction between "the solution exists in the hypothesis space" and "the search can find it" is essentially a restatement of well-known ideas about search bias and optimization landscape properties. The paper would benefit from more explicitly connecting to this prior work rather than presenting it as a new contribution.

- **PARKING results are inconclusive.** The paper acknowledges that neither PSM nor DQN reliably generalizes (Table 3), and the test success rates are comparable (0.16 vs 0.18). This benchmark doesn't clearly support either side, making it hard to draw conclusions from this re-evaluation.

### Trivial
None.

## Nice-to-Haves

- An ablation in Karel comparing "PPO with last action" vs "PPO with last action + sparse observations" would help isolate how much of the generalization gain comes from the observation augmentation versus the architectural simplification.
- A table showing per-seed success/failure for TORCS models would make the survivorship analysis transparent.

## Novel Insights

The paper's most novel contribution is the identification of instance-scaling working memory as the key structural property that differentiates programmatic from neural representations for OOD generalization. While the notion that fixed-capacity models have inherent limitations is not new, the paper's specific application of this idea to explain *why* programmatic policies succeed in RL generalization—and the corresponding experimental re-evaluation showing that prior benchmark differences were confounds rather than genuine structural advantages—is a valuable contribution that reframes how the community should approach representation design for generalization.

## Suggestions

- Report TORCS generalization rates over all seeds (not just successful training completions) to provide a more honest assessment. Include a column showing what fraction of models learned to complete the training track for all conditions.
- Add a concrete experiment on the memory-scaling claim: e.g., train neural policies on pathfinding graphs of increasing size and demonstrate the failure mode, or evaluate on an existing benchmark with known nested subproblem structure. Even one such experiment would substantially strengthen the paper's most important claim.
- Clarify the distinction between the paper's two main theses (confounds in prior work vs. genuine structural advantages of programs) early in the introduction, as the paper sometimes conflates "neural policies can match programmatic ones when confounds are removed" with "programmatic policies have an inherent advantage in certain task classes." These are complementary but distinct messages.

## Score and Decision

The paper provides a solid re-evaluation that corrects important misconceptions in the literature, offers a clean conceptual framework, and points toward a meaningful research direction. However, the survivorship bias in TORCS analysis and the limited empirical support for the instance-scaling memory claim weaken the contribution. The forward-looking theoretical argument is sound but under-supported experimentally.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>