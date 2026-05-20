#pragma once
// AUTOMATICALLY GENERATED - DO NOT EDIT
// SSOT - Python script (DSPConfig)

#define AUDIO_SAMPLE_RATE    16000
#define AUDIO_CHANNELS       1

#define ML_WINDOW_SIZE_MS    1000
#define ML_STRIDE_SIZE_MS    200

#define ML_WINDOW_SAMPLES    16000
#define ML_STRIDE_SAMPLES    3200

#define FFT_SIZE             512
#define FFT_HOP_SIZE         256

// --- tensor input dimensions ---
#define SPECTRUM_COLS        256
#define SPECTRUM_ROWS        61
#define MEL_BINS             40
#define SPECTRUM_TOTAL_SIZE  15616
