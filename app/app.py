# Import necessary modules
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig, TextStreamer

# Load the pre-trained tokenizer and model
print("Loading tokenizer and model")
config = GenerationConfig.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
print("Done")


def respond_to_prompt(prompt):
  # Encode the input text
  input_ids = tokenizer([prompt], return_tensors='pt').input_ids

  # Generate text
  model.generate(input_ids, streamer=TextStreamer(tokenizer, True), max_length=1000, pad_token_id=tokenizer.eos_token_id, eos_token_id=tokenizer.eos_token_id)

while True:
  prompt = input('> ')
  if prompt == 'quit':
    break
  respond_to_prompt(prompt)