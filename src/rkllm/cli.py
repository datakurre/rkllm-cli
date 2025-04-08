from huggingface_hub import hf_hub_download
from huggingface_hub import list_repo_files
from rkllm.RKLLM import RKLLM
from rkllm.types import LLMCallState
from rkllm.types import RKLLMResult
from transformers import AutoTokenizer
import ctypes
import os
import sys
import time
import typer


global_state = -1
split_byte_data = bytes(b"")


# Currently heavily based on
# https://github.com/airockchip/rknn-llm/blob/main/examples/rkllm_server_demo/rkllm_server/flask_server.py


def callback_impl(result, userdata, state):
    global global_text, global_state, split_byte_data
    if state == LLMCallState.RKLLM_RUN_FINISH:
        global_state = state
        print("\n")
        sys.stdout.flush()
    elif state == LLMCallState.RKLLM_RUN_ERROR:
        global_state = state
        print("run error")
        sys.stdout.flush()
    elif state == LLMCallState.RKLLM_RUN_NORMAL:
        global_state = state
        print(result.contents.text.decode("utf-8"), end="")
        sys.stdout.flush()


# Connect the callback function between the Python side and the C++ side
callback_type = ctypes.CFUNCTYPE(
    None, ctypes.POINTER(RKLLMResult), ctypes.c_void_p, ctypes.c_int
)
callback = callback_type(callback_impl)


cli = typer.Typer()


@cli.command(name="repl", no_args_is_help=True)
def repl(model_id: str):
    model_file = None
    for file in list_repo_files(model_id):
        if file.endswith(".rkllm"):
            model_file = file
            if "opt-1" in file:
                break
    assert model_file, "No .rkllm model found."
    model = hf_hub_download(model_id, model_file)
    rkllm_model = RKLLM(
        model,
        None,
        None,
        callback=callback,
        callback_type=callback_type,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    messages = [
        {"role": "assistant", "content": "You are a helpful assistant."},
    ]
    while True:
        try:
            messages = messages[:1]
            user_input = input(">>> ")
            if user_input.lower() in ["exit", "quit"]:
                break
            messages.append(
                {"role": "user", "content": user_input},
            )
            tokens = tokenizer.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True
            )
            rkllm_model.run(tokens)
        except (EOFError, KeyboardInterrupt):
            break
    sys.stdout.flush()
    print("Done.")
    rkllm_model.release()


def main():
    cli()
