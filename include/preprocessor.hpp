#pragma once

#include "app_config.h"
#include "esp_err.h"

class Preprocessor{
    private:
        size_t m_fft_size;
        float* m_window_coeffs;
        float* m_fft_buffer;
    public:
        Preprocessor(size_t fft_size = 512);
        ~Preprocessor();    
        
        esp_err_t init();
        void process_frame(int16_t* input_raw, float* output_mel);

        
};