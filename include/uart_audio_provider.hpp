#pragma once

#include "driver/uart.h"
#include "freertos/ringbuf.h"
#include "app_config.h"

#define TAG "uart_audio_provider"

class UARTAudioProvider{
    private:
        RingbufHandle_t rb_handle;
        size_t samples_counter = 0;

    public:
        esp_err_t init();
        void readDataStream(SemaphoreHandle_t data_ready_sem);
        void* getLatestWindow(size_t* retrievedSize);
        void releaseWindow(void* data_ptr);

        UARTAudioProvider();
};