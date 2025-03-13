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


global_text = []
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
    elif state == LLMCallState.RKLLM_RUN_GET_LAST_HIDDEN_LAYER:
        """
        If using the GET_LAST_HIDDEN_LAYER function, the callback interface will return the memory pointer: last_hidden_layer, the number of tokens: num_tokens, and the size of the hidden layer: embd_size.
        With these three parameters, you can retrieve the data from last_hidden_layer.
        Note: The data needs to be retrieved during the current callback; if not obtained in time, the pointer will be released by the next callback.
        """
        if (
            result.last_hidden_layer.embd_size != 0
            and result.last_hidden_layer.num_tokens != 0
        ):
            data_size = (
                result.last_hidden_layer.embd_size
                * result.last_hidden_layer.num_tokens
                * ctypes.sizeof(ctypes.c_float)
            )
            print(f"data_size: {data_size}")
            global_text.append(f"data_size: {data_size}\n")
            output_path = os.getcwd() + "/last_hidden_layer.bin"
            with open(output_path, "wb") as outFile:
                data = ctypes.cast(
                    result.last_hidden_layer.hidden_states,
                    ctypes.POINTER(ctypes.c_float),
                )
                float_array_type = ctypes.c_float * (
                    data_size // ctypes.sizeof(ctypes.c_float)
                )
                float_array = float_array_type.from_address(
                    ctypes.addressof(data.contents)
                )
                outFile.write(bytearray(float_array))
                print(f"Data saved to {output_path} successfully!")
                global_text.append(f"Data saved to {output_path} successfully!")
        else:
            print("Invalid hidden layer data.")
            global_text.append("Invalid hidden layer data.")
        global_state = state
        time.sleep(0.05)  # Delay for 0.05 seconds to wait for the output result
        sys.stdout.flush()
    else:
        # Save the output token text and the RKLLM running state
        global_state = state
        # Monitor if the current byte data is complete; if incomplete, record it for later parsing
        try:
            global_text.append((split_byte_data + result.contents.text).decode("utf-8"))
            print((split_byte_data + result.contents.text).decode("utf-8"), end="")
            split_byte_data = bytes(b"")
        except Exception:
            split_byte_data += result.contents.text or b""
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
