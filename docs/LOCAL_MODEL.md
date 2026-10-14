# An actual model run, including the failures

The project now contains three exploratory local model attempts on one synthetic CSM task. Unlike the scripted MCP smoke test, a language model selected the tool names and arguments. The host executed accepted calls through the real MCP stdio transport and returned their full results to the model.

**The most complete attempt executed all four requested tool actions, then produced an explanation that needs revision.** That distinction is the point of this experiment: tool completion does not establish answer fidelity.

[Inspect the browser replay](https://yuchi-wang02.github.io/csm-copilot/#model-runs) · [Read the reviewed results](../evidence/MODEL_RUNS.md) · [Review annotations](../evidence/model-runs/review.json)

## Task and observed attempts

The task names Lantern Games' Android and iOS integration IDs, asks for readiness checks and English follow-up drafts for both, then requests a short evidence-citing explanation of why the follow-ups differ. It also requires the assistant to avoid launch approval claims and state that nothing was sent.

| Attempt | Host contract | Observed result |
|---|---|---|
| Qwen3-0.6B smoke | One plain JSON action per turn; two-turn cap | Markdown-fenced output with an invented date; rejected before any call |
| Qwen3-4B initial | Same single-action prompt; eight-turn cap | Four relevant but concatenated JSON objects; rejected before any call |
| Qwen3-4B revised host | One action or an explicit array of up to four; eight-turn cap | Four requested calls executed, followed by an explanation with unsupported or omitted claims |

The first two raw outputs were not repaired or replayed as successful calls. The third is a fresh generation under a changed system prompt. All three attempts are retained. The different turn caps did not affect the first two outcomes because both stopped on their first response. This is iterative host development, not a controlled comparison of model sizes or a benchmark score.

## The final explanation still needs review

The batch attempt correctly called `check_readiness` and `draft_followup` for both platforms. Its final response described iOS as having “full compliance,” although the tool only established a scoped checklist. It claimed no evidence IDs were missing for Android, despite three unknown checks with empty evidence lists. It also failed to cite source IDs or distinguish the failed Android device check from missing evidence.

The statement that nothing was sent is supported by the tool outputs. The complete unedited response and an AI-assisted source comparison are published in the [results](../evidence/MODEL_RUNS.md). No independent human review or customer-use approval is claimed.

The existing promise-pattern lint returned **zero flags** for this response. This is a concrete example of why a narrow regex check cannot verify whether model-written claims match source evidence.

## Runtime and provenance

- Local NVIDIA GeForce RTX 5070 Ti; BF16 inference, no paid API calls or remote inference.
- Existing cached model snapshots; no model weights included in the repository.
- Worker: Python 3.10.18, PyTorch 2.8.0+cu128, Transformers 4.55.4. The MCP host uses the separate project environment (Python 3.11+).
- Non-thinking mode; sampling enabled, seed 42, temperature 0.7, top-p 0.8, top-k 20; 768 generated-token cap per turn and 12,000 input-token cap.
- Model revisions, timestamps, initial messages, prompt hash, raw responses, token counts, generation durations, tool calls and tool results are stored in each trace. Durations are generation observations, not an end-to-end customer productivity measure.
- Sampling and GPU kernels may vary across environments. Regeneration is not guaranteed to reproduce byte-identical model text.

Model references: [Qwen3-0.6B model card](https://huggingface.co/Qwen/Qwen3-0.6B) and [Qwen3-4B model card](https://huggingface.co/Qwen/Qwen3-4B). The implementation uses their documented Transformers loading and `enable_thinking=False` chat-template option. The recorded revisions, rather than a moving `main`, identify these attempts.

## Reproduce a local attempt

Install the CSM project in its usual environment. Separately prepare a CUDA-capable Python environment with the recorded PyTorch and Transformers versions and a complete local model snapshot. The model worker can use a different Python executable from the MCP host; it does not import the project package.

```sh
python scripts/run_local_host.py \
  --model-python /path/to/gpu-environment/python \
  --model-path /path/to/Qwen3-4B/snapshot \
  --model-id Qwen/Qwen3-4B \
  --revision 1cfa9a7208912126459214e8b04321603b3df60c \
  --protocol batch \
  --output work/my-local-run.json
```

PowerShell users can put the command on one line and use their Windows executable paths. Use `--protocol single` for the original host contract; add `--max-steps 2` for the small-model smoke configuration. Qwen3-0.6B used revision `c1899de289a04d12100db370d81485cdf75e47ca`.

The worker loads local files only, disables Hugging Face network access, and does not execute custom model code. It cannot download a missing snapshot. The host refuses to overwrite an existing trace. Each accepted batch is validated before any of its calls execute; unknown tool names, duplicate JSON keys, non-JSON constants and mixed final/action batches are rejected. Model-provided arguments still pass through the MCP tool schemas and engine checks. The host is scoped to this project's read-only server; it is not a general sandbox for arbitrary servers.

## Review and publishing

`python scripts/build_model_replay.py` packages the checked-in traces and review annotations into the website. It does not perform inference. CI checks structural coverage consistency, regenerates the replay and compares the artifact with Git; it does not certify the review annotations as independent truth or rerun a GPU model.

The automated coverage check only asks whether the four requested successful tool actions occurred. The separate source review examines the final prose. Do not combine these into one unqualified accuracy number.

For an interview exercise, hide the review panel, annotate every claim in the unedited response, then compare your findings. Explain why the model can choose the correct tools yet still overstate their results, and why a zero-flag lint result should not approve the answer.
