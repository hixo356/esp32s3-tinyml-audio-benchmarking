import numpy as np
import os
from config import DSPConfig
from preprocessor import DSPPreprocessor

def generate_golden_frame():
    cfg = DSPConfig()
    
    t = np.arange(cfg.fft_size) / cfg.audio_sample_rate
    
    signal_float = 0.5 * np.sin(2 * np.pi * 500 * t) + 0.5 * np.sin(2 * np.pi * 2000 * t)
    
    golden_frame_int16 = np.int16(signal_float * 15000)
    
    cpp_array_str = ", ".join(map(str, golden_frame_int16))
    
    cpp_code = f"""#pragma once
#include <cstdint>
// Single frame to perform Bit-Exactness test between two DSPs
// 500 Hz + 2000 Hz
// {cfg.fft_size} samples

const int16_t GOLDEN_FRAME[{cfg.fft_size}] = {{
    {cpp_array_str}
}};
"""
    firmware_dir = "../firmware/include"
    os.makedirs(firmware_dir, exist_ok=True)
    out_path = os.path.join(firmware_dir, "test_frame.h")
    
    with open(out_path, "w") as f:
        f.write(cpp_code)
        
    print(f"Saved frame for cpp: {out_path}\n")
    

    dsp = DSPPreprocessor(cfg)
    expected_mel = dsp.process_single_frame(golden_frame_int16)
    
    print("--- Expected mel spectrogram results (PYTHON) ---")
    
    for i, val in enumerate(expected_mel):
        print(f"Bin [{i:2d}]: {val:10.6f}")

if __name__ == "__main__":
    generate_golden_frame()