#include "app_config.h"
#include "esp_err.h"

#ifdef MODE_UART
    #include "uart_audio_provider.hpp"
#elif defined(MODE_LIVE)
    #include "i2s_audio_provider.hpp"
#endif

#ifdef MODE_UART
    UARTAudioProvider audio_provider;
#elif defined(MODE_LIVE)

#endif

extern "C" {
    void app_main() {

        esp_err_t err = audio_provider.init();
        

    }
}