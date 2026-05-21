#include "config_ml.h"
#include "esp_err.h"
#include "preprocessor.hpp"
#include <esp_log.h>

#ifdef MODE_UART
    #include "uart_audio_provider.hpp"
#elif defined(MODE_LIVE)
    #include "i2s_audio_provider.hpp"
#endif

// #ifdef MODE_UART
    UARTAudioProvider* audio_provider = nullptr;
// #elif defined(MODE_LIVE)

// #endif

SemaphoreHandle_t data_ready_sem = nullptr;
Preprocessor* dsp_pipeline = nullptr;


void dsp_task(void *pvParameters){

    printf("halo task\n");
    size_t retrieved_size = 0;
    float output_mel[MEL_BINS] = {0};

    while(1){
        if (xSemaphoreTake(data_ready_sem, portMAX_DELAY) == pdTRUE){
            int16_t* new_samples = (int16_t*)audio_provider->getLatestWindow(&retrieved_size);

            if(new_samples != nullptr){
                vTaskDelay(pdMS_TO_TICKS(500));
                dsp_pipeline->process_frame(new_samples, output_mel);

                audio_provider->releaseWindow(new_samples);
            }

            printf("\n--- ESP32 DSP (SANITY CHECK) ---\n");
            for(int i = 0; i < MEL_BINS; i++) {
                printf("Bin [%2d]: %10.6f\n", i, output_mel[i]);
            }
            printf("----------------------------------\n");
        }
    }
}


extern "C" {
    void app_main() {

// #ifdef MODE_UART
        audio_provider = new UARTAudioProvider();
// #elif defined(MODE_LIVE)
// #endif
        
        ESP_ERROR_CHECK(audio_provider->init());

        vTaskDelay(pdMS_TO_TICKS(500));

        dsp_pipeline = new Preprocessor();

        ESP_ERROR_CHECK(dsp_pipeline->init());

        data_ready_sem = xSemaphoreCreateBinary();

        xTaskCreatePinnedToCore(dsp_task, "DSP_Task", 8192, NULL, 5, NULL, 1);

        while(1){
            audio_provider->readDataStream(data_ready_sem);
        }

    }
}