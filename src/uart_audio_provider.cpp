#include "uart_audio_provider.hpp"
#include <esp_check.h>

esp_err_t UARTAudioProvider::init(){
    size_t rb_size = ML_WINDOW_SAMPLES * 2 *sizeof(int16_t);
    rb_handle = xRingbufferCreate(rb_size, RINGBUF_TYPE_NOSPLIT);
    if(rb_handle == nullptr){
        return ESP_ERR_NO_MEM;
    }

    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_DEFAULT,
    };

    ESP_RETURN_ON_ERROR(uart_param_config(UART_PORT_NUM, &uart_config), TAG, "UART Param Fail");

    ESP_RETURN_ON_ERROR(uart_set_pin(UART_PORT_NUM, UART_TX_PIN, UART_RX_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE), TAG, "UART Pin Fail");

    ESP_RETURN_ON_ERROR(uart_driver_install(UART_PORT_NUM, 1024, 0, 0, NULL, 0), TAG, "UART Driver Fail");

    return ESP_OK;
}

void UARTAudioProvider::readDataStream(SemaphoreHandle_t data_ready_sem){
    uint8_t tmp_buf[256];

    int length = uart_read_bytes(UART_NUM_1, tmp_buf, sizeof(tmp_buf), 10/portTICK_PERIOD_MS);

    if(length > 0){
        xRingbufferSend(this->rb_handle, tmp_buf, length, 0);

        samples_counter += (length/2);

        if(samples_counter >= ML_STRIDE_SAMPLES){
            xSemaphoreGive(data_ready_sem);
            samples_counter = 0;
        }
    }
}

void* UARTAudioProvider::getLatestWindow(size_t* retrieved_size) {
    return xRingbufferReceiveUpTo(
        rb_handle, 
        retrieved_size, 
        pdMS_TO_TICKS(10), 
        ML_WINDOW_SAMPLES * sizeof(int16_t)
    );
}

void UARTAudioProvider::releaseWindow(void* data_ptr) {
    if (data_ptr != nullptr) {
        vRingbufferReturnItem(rb_handle, data_ptr);
    }
}