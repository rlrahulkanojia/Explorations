import numpy as np
import time
import torch
import subprocess as sp
from transformers import AutoModelForCausalLM, AutoTokenizer

# Uncomment if using a gated model
# from huggingface_hub import login
# login(token = 'token')
# model = "meta-llama/Meta-Llama-3-8B" # Gated Model

def get_gpu_memory():
    """
    Python equivalent of nvidia-smi, copied from https://stackoverflow.com/a/67722676
    and verified as being equivalent ✅
    """
    output_to_list = lambda x: x.decode('ascii').split('\n')[:-1]
    COMMAND = "nvidia-smi --query-gpu=memory.used --format=csv"
    
    try:
        memory_use_info = output_to_list(sp.check_output(COMMAND.split(),stderr=sp.STDOUT))[1:]
    except sp.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    
    memory_use_values = [int(x.split()[0]) for i, x in enumerate(memory_use_info)]
    return memory_use_values

def load_model_and_tokenizer(model_name, device):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    return model, tokenizer

def measure_generation_time(model, tokenizer, device, use_cache, num_loops):
    times = []
    for _ in range(num_loops):  # measuring num_loops generations
        start = time.time()
        model.generate(**tokenizer("What is KV caching?", return_tensors="pt").to(device), use_cache=use_cache, max_new_tokens=1000)
        times.append(time.time() - start)
    return np.mean(times), np.std(times)

def main():
    model_name = "gpt2"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    num_loops = 2
    
    for use_cache in (True, False):
        model, tokenizer = load_model_and_tokenizer(model_name, device)
        mean_time, std_time = measure_generation_time(model, tokenizer, device, use_cache, num_loops)
        print(f"{'with' if use_cache else 'without'} KV caching: {round(mean_time, 3)} +- {round(std_time, 3)} seconds")
         
        if device == "cuda":
            print("VRAM with: ", get_gpu_memory()[0])
            torch.cuda.empty_cache()
        
        del model

if __name__ == "__main__":
    main()
  
    