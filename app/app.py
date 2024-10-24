# Import necessary modules
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the pre-trained tokenizer and model
print("Loading tokenizer and model")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
print("Done")


def respond_to_prompt(prompt):
  # Encode the input text
  input_ids = tokenizer(prompt, return_tensors='pt').input_ids

  # Generate text
  generated_ids = model.generate(input_ids, max_length=30)

  # Decode the generated text
  generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
  print(generated_text)

while True:
  prompt = input('>')
  if prompt == 'quit':
    break
  respond_to_prompt(prompt)