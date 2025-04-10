# https://github.com/airockchip/rknn-llm/blob/main/examples/rkllm_server_demo/rkllm_server/flask_server.py
from rkllm.types import RKLLM_Handle_t
from rkllm.types import rkllm_lib
from rkllm.types import RKLLMInferMode
from rkllm.types import RKLLMInferParam
from rkllm.types import RKLLMInput
from rkllm.types import RKLLMInputMode
from rkllm.types import RKLLMLoraAdapter
from rkllm.types import RKLLMLoraParam
from rkllm.types import RKLLMParam
import ctypes


class RKLLM:
    def __init__(
        self,
        model_path,
        lora_model_path=None,
        prompt_cache_path=None,
        callback=None,
        callback_type=None,
    ):
        assert callback is not None
        assert callback_type is not None

        rkllm_param = RKLLMParam()
        rkllm_param.model_path = bytes(model_path, "utf-8")

        rkllm_param.max_context_len = 4096
        rkllm_param.max_new_tokens = -1
        rkllm_param.skip_special_token = True

        rkllm_param.n_keep = -1
        rkllm_param.top_k = 1
        rkllm_param.top_p = 0.9
        rkllm_param.temperature = 0.8
        rkllm_param.repeat_penalty = 1.1
        rkllm_param.frequency_penalty = 0.0
        rkllm_param.presence_penalty = 0.0

        rkllm_param.mirostat = 0
        rkllm_param.mirostat_tau = 5.0
        rkllm_param.mirostat_eta = 0.1

        rkllm_param.is_async = False

        rkllm_param.img_start = "".encode("utf-8")
        rkllm_param.img_end = "".encode("utf-8")
        rkllm_param.img_content = "".encode("utf-8")

        rkllm_param.extend_param.base_domain_id = 0
        rkllm_param.extend_param.enabled_cpus_num = 4
        rkllm_param.extend_param.enabled_cpus_mask = (
            (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7)
        )

        self.handle = RKLLM_Handle_t()

        self.rkllm_init = rkllm_lib.rkllm_init
        self.rkllm_init.argtypes = [
            ctypes.POINTER(RKLLM_Handle_t),
            ctypes.POINTER(RKLLMParam),
            callback_type,
        ]
        self.rkllm_init.restype = ctypes.c_int
        self.rkllm_init(ctypes.byref(self.handle), ctypes.byref(rkllm_param), callback)

        self.rkllm_run = rkllm_lib.rkllm_run
        self.rkllm_run.argtypes = [
            RKLLM_Handle_t,
            ctypes.POINTER(RKLLMInput),
            ctypes.POINTER(RKLLMInferParam),
            ctypes.c_void_p,
        ]
        self.rkllm_run.restype = ctypes.c_int

        self.rkllm_destroy = rkllm_lib.rkllm_destroy
        self.rkllm_destroy.argtypes = [RKLLM_Handle_t]
        self.rkllm_destroy.restype = ctypes.c_int

        rkllm_lora_params = None
        if lora_model_path:
            lora_adapter_name = "test"

            lora_adapter = RKLLMLoraAdapter()
            ctypes.memset(
                ctypes.byref(lora_adapter), 0, ctypes.sizeof(RKLLMLoraAdapter)
            )

            lora_adapter.lora_adapter_path = ctypes.c_char_p(
                (lora_model_path).encode("utf-8")
            )
            lora_adapter.lora_adapter_name = ctypes.c_char_p(
                (lora_adapter_name).encode("utf-8")
            )
            lora_adapter.scale = 1.0

            rkllm_load_lora = rkllm_lib.rkllm_load_lora
            rkllm_load_lora.argtypes = [
                RKLLM_Handle_t,
                ctypes.POINTER(RKLLMLoraAdapter),
            ]
            rkllm_load_lora.restype = ctypes.c_int
            rkllm_load_lora(self.handle, ctypes.byref(lora_adapter))
            rkllm_lora_params = RKLLMLoraParam()
            rkllm_lora_params.lora_adapter_name = ctypes.c_char_p(
                (lora_adapter_name).encode("utf-8")
            )

        self.rkllm_infer_params = RKLLMInferParam()
        ctypes.memset(
            ctypes.byref(self.rkllm_infer_params), 0, ctypes.sizeof(RKLLMInferParam)
        )
        self.rkllm_infer_params.mode = RKLLMInferMode.RKLLM_INFER_GENERATE
        self.rkllm_infer_params.lora_params = (
            ctypes.pointer(rkllm_lora_params) if rkllm_lora_params else None
        )
        self.rkllm_infer_params.keep_history = 0

        self.prompt_cache_path = None
        if prompt_cache_path:
            self.prompt_cache_path = prompt_cache_path

            rkllm_load_prompt_cache = rkllm_lib.rkllm_load_prompt_cache
            rkllm_load_prompt_cache.argtypes = [RKLLM_Handle_t, ctypes.c_char_p]
            rkllm_load_prompt_cache.restype = ctypes.c_int
            rkllm_load_prompt_cache(
                self.handle, ctypes.c_char_p((prompt_cache_path).encode("utf-8"))
            )

    def run(self, prompt_tokens):
        rkllm_input = RKLLMInput()
        rkllm_input.input_mode = RKLLMInputMode.RKLLM_INPUT_TOKEN

        if prompt_tokens[-1] != 2:
            prompt_tokens.append(2)

        token_array = (ctypes.c_int * len(prompt_tokens))(*prompt_tokens)
        rkllm_input.input_data.token_input.input_ids = token_array
        rkllm_input.input_data.token_input.n_tokens = ctypes.c_ulong(len(prompt_tokens))

        self.rkllm_run(
            self.handle,
            ctypes.byref(rkllm_input),
            ctypes.byref(self.rkllm_infer_params),
            None,
        )
        return

    def release(self):
        self.rkllm_destroy(self.handle)
