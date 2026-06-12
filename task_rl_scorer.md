Understand the current repo and set it up if needed by looking at code/ and prompts/ and do this task. 
Put all files in network storage in ~/abc besides venv, that should be in ~/, but a quick setup for the venv should be in ~/abc

Problem:
Currently the LLM cannot rank the current paper in the retrival list well and usually over rank them.

Goal:
Develop a offline RL dataset to improve it. 

Make a copy of code/main.py such 

For each paper, Do
    1. (Using Openrouter API for deepseek v4 flash) that now after the merger generated the review and retrival anchors, it does NOT do cal or scoring. The currently reviewed paper's review itself might be included in the anchor, we should exclude it. 
    2. Collect the generated review, and N anchors, save it as a prompt to let another LLM call give a calibrated score. 
    For j in range(K):
        Rollout k samples using the prompt using vllm (NOT cloud) Qwen 3.6 27B, collecting reasoning process and final answer
    End for

    For the k generated calibration scores, save them in a json with their reward (10 - |pred - gt|)
End for

Make a bash to start the dataset collection, the dataset collection should run on datasets/deepreview_13k_train. Do it for 1000 samples with k = 5. 