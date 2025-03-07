print('The Python interpreter was successfully configured\n\n'
      'Evaluating GPU Configuration\n')

from faster_whisper import WhisperModel
import torch

# Display device usage
device = "cuda" if torch.cuda.is_available() else "CPU"
model = WhisperModel("base", device=device)
print("Model Device:", model.model.device)
print("CUDA Available:", torch.cuda.is_available())
print("CUDA Device Count:", torch.cuda.device_count())
print("CUDA Device Name:",
      torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU detected")
print("PyTorch Version:", torch.__version__)

