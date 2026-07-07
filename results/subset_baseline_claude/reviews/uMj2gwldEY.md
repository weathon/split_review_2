## Summary
The paper proposes FL-DDPG, a federated deep reinforcement learning framework for multi-UAV wildfire front tracking. Each UAV independently runs a DDPG-based planning/control policy; a virtual central server periodically aggregates only the velocity-related neural network parameters using an exponential performance-weighted scheme that gives more influence to UAVs maintaining tighter formation spacing. The method is evaluated in 3-UAV and 5-UAV simulation scenarios based on the Kilmore East wildfire data.

## Strengths
- **Practically motivated problem**: Wildfire monitoring with multi-UAV fleets is an important real-world application, and the use of actual fire spread parameters (FARSITE calibrated with Kilmore East data) adds credibility to the simulation setup.
- **Selective federation is a sensible design choice**: Federating only velocity-related parameters rather than the full model is a principled and computationally efficient decision that reflects domain understanding—inter-UAV spacing is most sensitive to velocity control.
- **Clear improvement over independent DDPG baseline**: FLDDPG achieves a standard deviation of inter-UAV distances of ~2.5 m versus ~14 m for standard DDPG, and improves average episode reward from −355.45 to −122.21, demonstrating that naive independent learning fails at the formation coordination task.

## Weaknesses

### Fatal
None.

### Major
1. **Critically weak baselines**: The only comparison is against *independent* DDPG, which is the weakest possible multi-agent baseline. Established MARL methods designed for cooperative tasks—MADDPG, QMIX, MAPPO, VDN (mentioned but not compared against)—are entirely absent. The claimed improvements are therefore uninterpretable as evidence of method quality; almost any cooperative information-sharing mechanism would beat independent DDPG.

2. **No statistical evaluation**: All reported numbers come from a single simulation run with no error bars, confidence intervals, or repeated trials. The core quantitative claims (2.5 m vs 14 m, −122.21 vs −355.45) could simply be results of a favorable random seed. This is a fundamental scientific rigor issue, not a minor concern.

3. **Minimal ML novelty**: The technical contribution—exponential weighting of federated averaging by a domain-specific performance metric—is a straightforward extension of FedAvg. Performance-weighted aggregation is well-established in the FL literature. Applying it to DDPG with formation-error weighting is an application contribution, not a learning contribution. The planning and control architecture is entirely borrowed from Raoufi et al. (2025).

4. **Simulation scope is insufficient to support scalability claims**: "Scalability" is claimed but tested only at N=3 and N=5 UAVs—both very small fleets. No trajectory-length analysis, no test of degradation with growing N, and only ~10–20 second episodes.

### Minor
1. **No ablation study**: Key hyperparameters (σ controlling sensitivity in Equation 12, τ_g, federated update frequency, choice of which parameters to federate) are not ablated. It is unclear whether the gains come from the weighting scheme itself or simply from any form of parameter sharing.

2. **Circularity in the reward-weighting design**: The formation spacing term appears in both the reward function (Equation 10) and the federated weight computation (Equation 12), which are drawn from the same inter-UAV distances. This design is logical but also somewhat tautological—it specifically boosts UAVs that are doing well on exactly the metric being optimized.

3. **Evaluation duration is very short**: 10 s and 20 s simulation horizons are too brief to assess steady-state behavior, long-term stability, or policy robustness to changing wind conditions.

### Trivial
None worth raising.

## Nice-to-Haves
- Comparison against MADDPG or MAPPO to understand where FL-DDPG sits relative to standard cooperative MARL.
- Ablation over σ and τ_g to quantify sensitivity.
- Multiple random seeds with confidence intervals.
- Longer simulation runs to demonstrate sustained formation under a full fire evolution cycle.

## Novel Insights
The idea of selectively federating only the subset of neural network parameters most responsible for inter-agent coordination (velocity and its control gain) rather than the full model is a useful inductive bias. If validated rigorously, this "selective federation" principle could generalize to other multi-agent physical systems where one control channel dominates the coordination objective. However, the paper does not isolate or formally study this property, so it remains an engineering choice rather than an insight.

## Suggestions
- Add MADDPG and at least one other cooperative MARL baseline (MAPPO or QMIX) to contextualize the contribution.
- Run at least 10 independent seeds per method and report mean ± std for all metrics.
- Include an ablation comparing full-model federation vs. selective federation vs. uniform-weight federation to validate each design choice independently.
- Test with N ∈ {3, 5, 10, 20} UAVs and report formation variance as a function of N to substantiate scalability claims.

## Score and Decision
The paper addresses a real problem and the FL-DDPG idea is sensible, but the evaluation is insufficient for ICLR: a single random seed, a single trivial baseline (independent DDPG), very short simulation horizons, and no ablations. The core ML contribution—performance-weighted FedAvg—is incremental. The combined weight of these major issues makes the paper unsuitable for acceptance without substantial additional experimental work.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>