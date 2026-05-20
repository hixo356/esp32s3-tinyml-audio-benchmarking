import numpy as np
import librosa
import re
import os

CONFIG_PATH = "include/app_config.h"
OUTPUT_PATH = "include/mel_data.h"

# GET A PARAMETER FROM APP_CONFIG
def get_config_value(key):
    with open(CONFIG_PATH, "r") as f:
        content = f.read()
        match = re.search(fr'#define\s+{key}\s+(\d+)', content)
        if match:
            return int(match.group(1))
    raise ValueError(f"Could not find {key} in {CONFIG_PATH}")

# GENERATE HEADER WITH MEL VALUES
def generate_header():
    try:
        fs = get_config_value("AUDIO_SAMPLE_RATE")
        n_fft = get_config_value("FFT_SIZE")
        n_mels = get_config_value("MEL_BINS")
        
        print(f"Reading config: SR={fs}, FFT={n_fft}, Mels={n_mels}")

        mel_basis = librosa.filters.mel(sr=fs, n_fft=n_fft, n_mels=n_mels)

        with open(OUTPUT_PATH, "w") as f:
            f.write("// AUTOMATICALLY GENERATED FROM APP_CONFIG.H - DO NOT EDIT\n")
            f.write("#pragma once\n\n")
            f.write(f"#define GENERATED_MEL_FFT_SIZE {n_fft}\n")
            f.write(f"#define GENERATED_MEL_BINS {n_mels}\n")
            f.write(f"#define GENERATED_MEL_SAMPLE_RATE {fs}\n\n")
            
            f.write(f"const float mel_filterbank[{n_mels}][{n_fft // 2 + 1}] = {{\n")
            for i, row in enumerate(mel_basis):
                f.write("    {")
                f.write(", ".join([f"{x:.6f}f" for x in row]))
                f.write("}" + ("," if i < n_mels - 1 else "") + "\n")
            f.write("};\n")
            
        print(f"Successfully synced and generated: {OUTPUT_PATH}")

    except Exception as e:
        print(f"Error during generation: {e}")
        exit(1)

if __name__ == "__main__":
    generate_header()