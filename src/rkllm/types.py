import ctypes
import os


PROMPT_TOKENS = {
    "deepseek": {
        "unk": None,
        "eos": "<|end_of_sentence|>",
        "pad": "<|pad|>",
        "bos": "<|begin_of_sentence|>",
        "bot": "<|begin_of_thinking|>",
        "eot": "<|end_of_thinking|>",
    },
    "deepseek_v2": {
        "unk": None,
        "eos": "<|end_of_sentence_v2|>",
        "pad": "<|pad_v2|>",
        "bos": "<|begin_of_sentence_v2|>",
        "bot": "<|begin_of_thinking_v2|>",
        "eot": "<|end_of_thinking_v2|>",
    },
    "deepseek_v3": {
        "unk": None,
        "eos": "<|end_of_sentence_v3|>",
        "pad": "<|pad_v3|>",
        "bos": "<|begin_of_sentence_v3|>",
        "bot": "<|begin_of_thinking_v3|>",
        "eot": "<|end_of_thinking_v3|>",
    },
    "llama": {
        "unk": "<unk>",
        "bos": "<s>",
        "eos": "</s>",
        "pad": None,
        "eot": None,
        "bot": None,
    },
    "llama2": {
        "unk": "<unk>",
        "bos": "<s>",
        "eos": "</s>",
        "pad": None,
        "eot": None,
        "bot": None,
    },
    "qwen": {
        "unk": "<unk>",
        "bos": "<s>",
        "eos": "</s>",
        "pad": None,
        "eot": None,
        "bot": None,
    },
    "bloom": {
        "unk": "<unk>",
        "bos": "<s>",
        "eos": "</s>",
        "pad": "<pad>",
        "eot": None,
        "bot": None,
    },
    "gpt2": {"unk": "", "bos": "", "eos": "", "pad": None, "eot": None, "bot": None},
    "opt": {
        "unk": "",
        "bos": "<s>",
        "eos": "</s>",
        "pad": "<pad>",
        "eot": None,
        "bot": None,
    },
    "t5": {
        "unk": "<unk>",
        "bos": "<s>",
        "eos": "</s>",
        "pad": "<pad>",
        "eot": None,
        "bot": None,
    },
    "bert": {
        "unk": "[UNK]",
        "bos": "[CLS]",
        "eos": "[SEP]",
        "pad": "[PAD]",
        "eot": None,
        "bot": None,
    },
    "tinyllama": {
        "unk": None,
        "bos": None,
        "eos": None,
        "pad": None,
        "eot": None,
        "bot": None,
    },
    "qwen_1.8b": {
        "unk": None,
        "bos": None,
        "eos": None,
        "pad": None,
        "eot": None,
        "bot": None,
    },
    "qwen2": {
        "unk": "<unk>",
        "bos": "<|im_start|>",
        "eos": "<|im_end|>",
        "pad": "<pad>",
        "eot": "<|endoftext|>",
        "bot": "<|im_think|>",
        "system": "<|im_system|>",
        "user": "<|im_user|>",
        "assistant": "<|im_assistant|>",
    },
    "phi2_2.7b": {
        "unk": None,
        "bos": None,
        "eos": None,
        "pad": None,
        "eot": None,
        "bot": None,
    },
}

PROMPT_TEXT_PREFIX = "{bos}system You are a helpful assistant. {eos} {bos}user"
PROMPT_TEXT_POSTFIX = "{eos}{bos}assistant"


# Set the dynamic library path
rkllm_lib = ctypes.CDLL(os.environ.get("LIBRKLLMRT_PATH") or "/lib/librkllmrt.so")

# Define the structures from the library
RKLLM_Handle_t = ctypes.c_void_p
userdata = ctypes.c_void_p(None)


class LLMCallState(ctypes.c_int):
    RKLLM_RUN_NORMAL = 0
    RKLLM_RUN_WAITING = 1
    RKLLM_RUN_FINISH = 2
    RKLLM_RUN_ERROR = 3
    RKLLM_RUN_GET_LAST_HIDDEN_LAYER = 4


class RKLLMInputMode(ctypes.c_int):
    RKLLM_INPUT_PROMPT = 0
    RKLLM_INPUT_TOKEN = 1
    RKLLM_INPUT_EMBED = 2
    RKLLM_INPUT_MULTIMODAL = 3


class RKLLMInferMode(ctypes.c_int):
    RKLLM_INFER_GENERATE = 0
    RKLLM_INFER_GET_LAST_HIDDEN_LAYER = 1


class RKLLMExtendParam(ctypes.Structure):
    _fields_ = [("base_domain_id", ctypes.c_int32), ("reserved", ctypes.c_uint8 * 112)]


class RKLLMParam(ctypes.Structure):
    _fields_ = [
        ("model_path", ctypes.c_char_p),
        ("max_context_len", ctypes.c_int32),
        ("max_new_tokens", ctypes.c_int32),
        ("top_k", ctypes.c_int32),
        ("top_p", ctypes.c_float),
        ("temperature", ctypes.c_float),
        ("repeat_penalty", ctypes.c_float),
        ("frequency_penalty", ctypes.c_float),
        ("presence_penalty", ctypes.c_float),
        ("mirostat", ctypes.c_int32),
        ("mirostat_tau", ctypes.c_float),
        ("mirostat_eta", ctypes.c_float),
        ("skip_special_token", ctypes.c_bool),
        ("is_async", ctypes.c_bool),
        ("img_start", ctypes.c_char_p),
        ("img_end", ctypes.c_char_p),
        ("img_content", ctypes.c_char_p),
        ("extend_param", RKLLMExtendParam),
    ]


class RKLLMLoraAdapter(ctypes.Structure):
    _fields_ = [
        ("lora_adapter_path", ctypes.c_char_p),
        ("lora_adapter_name", ctypes.c_char_p),
        ("scale", ctypes.c_float),
    ]


class RKLLMEmbedInput(ctypes.Structure):
    _fields_ = [
        ("embed", ctypes.POINTER(ctypes.c_float)),
        ("n_tokens", ctypes.c_size_t),
    ]


class RKLLMTokenInput(ctypes.Structure):
    _fields_ = [
        ("input_ids", ctypes.POINTER(ctypes.c_int32)),
        ("n_tokens", ctypes.c_size_t),
    ]


class RKLLMMultiModelInput(ctypes.Structure):
    _fields_ = [
        ("prompt", ctypes.c_char_p),
        ("image_embed", ctypes.POINTER(ctypes.c_float)),
        ("n_image_tokens", ctypes.c_size_t),
    ]


class RKLLMInputUnion(ctypes.Union):
    _fields_ = [
        ("prompt_input", ctypes.c_char_p),
        ("embed_input", RKLLMEmbedInput),
        ("token_input", RKLLMTokenInput),
        ("multimodal_input", RKLLMMultiModelInput),
    ]


class RKLLMInput(ctypes.Structure):
    _fields_ = [("input_mode", ctypes.c_int), ("input_data", RKLLMInputUnion)]


class RKLLMLoraParam(ctypes.Structure):
    _fields_ = [("lora_adapter_name", ctypes.c_char_p)]


class RKLLMPromptCacheParam(ctypes.Structure):
    _fields_ = [
        ("save_prompt_cache", ctypes.c_int),
        ("prompt_cache_path", ctypes.c_char_p),
    ]


class RKLLMInferParam(ctypes.Structure):
    _fields_ = [
        ("mode", RKLLMInferMode),
        ("lora_params", ctypes.POINTER(RKLLMLoraParam)),
        ("prompt_cache_params", ctypes.POINTER(RKLLMPromptCacheParam)),
    ]


class RKLLMResultLastHiddenLayer(ctypes.Structure):
    _fields_ = [
        ("hidden_states", ctypes.POINTER(ctypes.c_float)),
        ("embd_size", ctypes.c_int),
        ("num_tokens", ctypes.c_int),
    ]


class RKLLMResult(ctypes.Structure):
    _fields_ = [
        ("text", ctypes.c_char_p),
        ("size", ctypes.c_int),
        ("last_hidden_layer", RKLLMResultLastHiddenLayer),
    ]
