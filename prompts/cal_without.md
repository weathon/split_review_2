After filtering the Harsh Critic and Strength Finder inputs into a draft review, call `draft_review` exactly once, passing each kept strength as one entry of `strengths`, each kept weakness (with its severity tier in the text) as one entry of `weaknesses`, and the rest (removed points, novel insights, suggestions) as `other`.

The tool returns each of your draft's items tagged with a favorability in [0,1] from a trained scoring model:
- 0 means the item drags the paper's score down (a serious weakness),
- 1 means the item strongly pushes the score up (a strong strength),
- 0.5 is roughly neutral.

There is NO retrieval or human-anchor comparison. Use these per-item favorabilities to judge which strengths and weaknesses matter most — heavy negatives (near 0) and heavy positives (near 1) should dominate your final score, minor points (near 0.5) should barely move it. Then assign the final score based on your own assessment weighted by these signals.
