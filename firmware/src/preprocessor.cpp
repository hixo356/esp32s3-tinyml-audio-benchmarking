#include "preprocessor.hpp"
#include <cmath>
#include "esp_log.h"
#include "esp_heap_caps.h"
#include "esp_dsp.h"
#include "esp_check.h"
#include "mel_data.h"

static const char* TAG = "PREPROCESSOR";

Preprocessor::Preprocessor(size_t fft_size) : m_fft_size(fft_size) {
    m_window_coeffs = (float*)heap_caps_aligned_alloc(16, m_fft_size * sizeof(float), MALLOC_CAP_INTERNAL | MALLOC_CAP_8BIT);
    m_fft_buffer = (float*)heap_caps_aligned_alloc(16, m_fft_size * 2 * sizeof(float), MALLOC_CAP_INTERNAL | MALLOC_CAP_8BIT);

    if (m_window_coeffs == nullptr || m_fft_buffer == nullptr) {
        ESP_LOGE(TAG, "Failed to allocate memory for the Preprocessor.");
    }
}

Preprocessor::~Preprocessor() {
    if (m_window_coeffs) free(m_window_coeffs);
    if (m_fft_buffer) free(m_fft_buffer);
}

esp_err_t Preprocessor::init(){
    ESP_RETURN_ON_ERROR(dsps_fft2r_init_fc32(NULL, CONFIG_DSP_MAX_FFT_SIZE), TAG, "FFT init fail");

    dsps_wind_hann_f32(m_window_coeffs, m_fft_size);

    return ESP_OK;
}

/*
    returns ONE log-mel spectrogram COLUMN into output_mel
*/
void Preprocessor::process_frame(int16_t* new_stride_data, float* output_mel){
    // size_t overlap_samples = ML_WINDOW_SAMPLES - ML_STRIDE_SAMPLES;

    // moving old data to the left (maintaining overlap)
    // memmove(m_internal_audio_buffer, m_internal_audio_buffer + ML_STRIDE_SAMPLES, overlap_samples * sizeof(int16_t));

    // adding new data at the end of the buffer 
    // memcpy(m_internal_audio_buffer + overlap_samples, new_stride_data, ML_STRIDE_SAMPLES * sizeof(int16_t));

    memcpy(m_internal_audio_buffer, new_stride_data, m_fft_size * sizeof(int16_t));

    for (int i = 0; i < m_fft_size; i++){
        float val = ((float)m_internal_audio_buffer[i] / 32768.0f) * m_window_coeffs[i];

        m_fft_buffer[i * 2 + 0] = val;
        m_fft_buffer[i * 2 + 1] = 0.0f;
    }

    dsps_fft2r_fc32(m_fft_buffer, m_fft_size);
    dsps_bit_rev_fc32(m_fft_buffer, m_fft_size);

    float power_spectrum[FFT_SIZE / 2 + 1];
    for (int i = 0; i < m_fft_size / 2; i++){
        float re = m_fft_buffer[i * 2 + 0];
        float im = m_fft_buffer[i * 2 + 1];

        power_spectrum[i] = (re * re) + (im * im);
    }

    for (int m = 0; m < MEL_BINS; m++) {
        float mel_energy = 0.0f;
        
        for (int f = 0; f <= m_fft_size / 2; f++) {
            mel_energy += power_spectrum[f] * MEL_FILTERBANK[m][f];
        }
        
        // Zapis do bufora wyjściowego (rozmiar: MEL_BINS)
        output_mel[m] = 10.0f * log10f(mel_energy + 1e-10f);
    }
}