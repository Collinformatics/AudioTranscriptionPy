print('The Python interpreter was successfully configured\n\n'
      'Loading GPU Configuration\n')

from faster_whisper import WhisperModel
import torch

# Display device usage
model = WhisperModel("base", device="cuda")
print("Model Device:", model.model.device)
print("CUDA Available:", torch.cuda.is_available())
print("CUDA Device Count:", torch.cuda.device_count())
print("CUDA Device Name:",
      torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU detected")
print("PyTorch Version:", torch.__version__)

