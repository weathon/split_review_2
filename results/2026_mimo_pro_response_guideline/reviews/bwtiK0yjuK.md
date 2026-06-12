Based on my calibration analysis, I have a clear picture of where this paper falls. Let me finalize my assessment.

**Calibration anchors summary:**
- I5MquO1g7R (4.75, Reject): Change point detection via TV-HMM — weaker theory, no clear advantage over competitors. Our paper is clearly stronger.
- vjHCyOWc7h (4.40, Reject): Mixture SBM for multiplex graphs — limited experiments, incremental. Our paper is clearly stronger.
- ILqA09Oeq2 (6.20, Accept): Performance gaps in tensor model for multi-view clustering — similar theoretical depth, less practical evaluation. Comparable.
- p1TBYyqy8v (6.60, Accept): Spreading OOD detection — novel problem, good experiments. Slightly above our paper due to cleaner empirical validation.
- zhFyKgqxlz (5.75, Accept): Exact community recovery — strong theory but felt to belong in a journal. Comparable theoretical depth.
- Frok9AItud (5.80, Accept): Random projections on graphs — solid theory, less applied.

**Bracket**: 5.5–6.5. The paper is clearly stronger than the 4.40–4.75 rejects (which have weaker theory and less convincing experiments) and comparable to the 6.20 tensor model paper. The CI issues prevent a higher score. My final score is **6.0**.

The paper has genuine theoretical novelty (Theorem 2 is the first limiting distribution result for change point estimators in network data) and strong localization performance (Table 1), but the CI procedure — presented as a major contribution — has significant empirical anomalies (Table 4 CIs exclude detected change points for 2 of 4 cases; Scenario 3 coverage at 76.67%). These issues affect the inference contribution but not the localization contribution. The score reflects a paper with a real and valuable core contribution (localization theory and algorithm) partially undermined by an underdeveloped inference component.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>