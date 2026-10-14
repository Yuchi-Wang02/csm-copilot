"""Optional offline Transformers worker. Can run in a separate GPU Python environment."""

import argparse
import json
import sys
import time


def emit(value):
    sys.stdout.write(json.dumps(value, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--max-new-tokens", type=int, default=768)
    args = parser.parse_args()
    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed

    if not torch.cuda.is_available():
        raise RuntimeError("This recorded workflow requires a local CUDA GPU")
    set_seed(42)
    tokenizer = AutoTokenizer.from_pretrained(
        args.model_path, local_files_only=True, trust_remote_code=False
    )
    model = (
        AutoModelForCausalLM.from_pretrained(
            args.model_path,
            local_files_only=True,
            trust_remote_code=False,
            torch_dtype=torch.bfloat16,
        )
        .to("cuda")
        .eval()
    )
    emit(
        {
            "ready": True,
            "torch": torch.__version__,
            "transformers": transformers.__version__,
            "python": sys.version.split()[0],
            "device": torch.cuda.get_device_name(0),
            "dtype": "bfloat16",
            "enable_thinking": False,
            "seed": 42,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 20,
            "max_new_tokens": args.max_new_tokens,
            "max_input_tokens": 12000,
        }
    )
    for line in sys.stdin:
        request = json.loads(line)
        rendered = tokenizer.apply_chat_template(
            request["messages"], tokenize=False, add_generation_prompt=True, enable_thinking=False
        )
        inputs = tokenizer(rendered, return_tensors="pt").to("cuda")
        input_tokens = inputs.input_ids.shape[1]
        if input_tokens > 12000:
            emit({"error": "context_limit", "input_tokens": input_tokens})
            continue
        started = time.perf_counter()
        with torch.inference_mode():
            output = model.generate(
                **inputs,
                max_new_tokens=args.max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.8,
                top_k=20,
                pad_token_id=tokenizer.eos_token_id,
            )
        generated = output[0, input_tokens:]
        emit(
            {
                "text": tokenizer.decode(generated, skip_special_tokens=True).strip(),
                "input_tokens": input_tokens,
                "output_tokens": len(generated),
                "seconds": round(time.perf_counter() - started, 3),
                "token_limit_reached": len(generated) >= args.max_new_tokens,
            }
        )


if __name__ == "__main__":
    main()
