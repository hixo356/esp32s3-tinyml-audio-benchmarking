import os
import librosa
from config import DSPConfig

def generate_config_ml_h(config: DSPConfig, output_dir: str):
    filepath = os.path.join(output_dir, "config_ml.h")
    
    content = f"""#pragma once
// AUTOMATICALLY GENERATED - DO NOT EDIT
// SSOT - Python script (DSPConfig)

#define AUDIO_SAMPLE_RATE    {config.audio_sample_rate}
#define AUDIO_CHANNELS       {config.audio_channels}

#define ML_WINDOW_SIZE_MS    {config.ml_window_size_ms}
#define ML_STRIDE_SIZE_MS    {config.ml_stride_size_ms}

#define ML_WINDOW_SAMPLES    {config.ml_window_samples}
#define ML_STRIDE_SAMPLES    {config.ml_stride_samples}

#define FFT_SIZE             {config.fft_size}
#define FFT_HOP_SIZE         {config.fft_hop_size}

// --- tensor input dimensions ---
#define SPECTRUM_COLS        {config.spectrum_cols}
#define SPECTRUM_ROWS        {config.spectrum_rows}
#define MEL_BINS             {config.mel_bins}
#define SPECTRUM_TOTAL_SIZE  {config.spectrum_total_size}
"""
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Generated {filepath}")


def generate_mel_data_h(config: DSPConfig, output_dir: str):
    filepath = os.path.join(output_dir, "mel_data.h")
    
    mel_weights = librosa.filters.mel(
        sr=config.audio_sample_rate, 
        n_fft=config.fft_size, 
        n_mels=config.mel_bins,
        fmin=0,
        fmax=config.audio_sample_rate / 2.0
    )
    
    content = f"""#pragma once
// AUTOMATICALLY GENERATED - DO NOT EDIT

#include "config_ml.h"

const float MEL_FILTERBANK[{config.mel_bins}][SPECTRUM_COLS + 1] = {{
"""
    for row in mel_weights:
        row_str = ", ".join([f"{val:.6f}f" for val in row])
        content += f"    {{{row_str}}},\n"
        
    content += "};\n"
    
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Generated {filepath}")


if __name__ == "__main__":
    config = DSPConfig()
    
    firmware_include_dir = "../firmware/include"
    
    generate_config_ml_h(config, firmware_include_dir)
    generate_mel_data_h(config, firmware_include_dir)