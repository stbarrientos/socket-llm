# Import necessary modules
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig, TextStreamer
from llm_response_streamer import LLMResponseStreamer

def init_local_llm():
    global tokenizer, model
    # Load the pre-trained tokenizer and model
    print("Loading tokenizer and model")
    config = GenerationConfig.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
    print("Done")

# This will need to be rethought in the future, the socket_client doesn't belong here.
# However, because it is used by the streamer, it is necessary for now.
def respond_to_prompt(prompt, socket_client):
    # Encode the input text
    input_ids = tokenizer([prompt], return_tensors='pt').input_ids

    kwargs = {
      "streamer": LLMResponseStreamer(tokenizer, socket_client),
      "max_length": 1000,
      "pad_token_id": tokenizer.eos_token_id,
      "eos_token_id": tokenizer.eos_token_id
    }

    # Generate text
    model.generate(input_ids, **kwargs)
