import serial
import time
import numpy as np
from config import DSPConfig

def send_with_handshake(port: str, baudrate: int = 115200):
    cfg = DSPConfig()
    
    # Generowanie identycznej fali testowej
    t = np.arange(cfg.fft_size) / cfg.audio_sample_rate
    signal_float = 0.5 * np.sin(2 * np.pi * 500 * t) + 0.5 * np.sin(2 * np.pi * 2000 * t)
    golden_frame_int16 = np.int16(signal_float * 15000)
    raw_bytes = golden_frame_int16.tobytes()
    
    print(f"🔌 Otwieranie portu {port}...")
    try:
        # Zostawiamy timeout=1, aby readline nie blokowało skryptu na zawsze
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print("👀 Port otwarty. Nasłuchuję sygnału startowego z ESP32...")
            
            # KROK 1: Pętla nasłuchująca przed wysłaniem danych
            esp_is_ready = False
            while not esp_is_ready:
                if ser.in_waiting > 0:
                    try:
                        line = ser.readline().decode('utf-8', errors='replace').strip()
                        if line:
                            print(f"[BOOT-LOG] {line}")
                        
                        # Sprawdzamy czy to nasze słowo kluczowe
                        if "ESP32_READY_FOR_DATA" in line:
                            print("\n🎯 Wykryto sygnał gotowości od ESP32!")
                            esp_is_ready = True
                    except Exception:
                        pass
                time.sleep(0.01)
            
            # Dodatkowe 50ms na upewnienie się, że bufor UART po stronie ESP32 jest czysty
            time.sleep(0.05)
            ser.reset_input_buffer()
            
            # KROK 2: Wysyłanie fali dokładnie wtedy, kiedy ESP32 na nią czeka
            print(f"📤 Wysyłanie {len(raw_bytes)} bajtów fali do ESP32...")
            ser.write(raw_bytes)
            ser.flush()
            print("✅ Dane wysłane pomyślnie. Zbieram wyniki końcowe:\n")
            print("-" * 50)
            
            # KROK 3: Ciągły nasłuch na wyniki przetwarzania DSP
            start_time = time.time()
            while time.time() - start_time < 4000: # Słuchaj przez 4 sekundy na wyniki
                if ser.in_waiting > 0:
                    try:
                        line = ser.readline().decode('utf-8', errors='replace').strip()
                        if line:
                            print(f"[ESP32-DSP] {line}")
                    except Exception:
                        pass
                time.sleep(0.01)
                
            print("-" * 50)
            print("Koniec testu synchronizacji.")

    except serial.SerialException as e:
        print(f"❌ Błąd: {e}")
        print("💡 Pamiętaj, aby zamknąć monitor szeregowy w PlatformIO!")

if __name__ == "__main__":
    # Ustaw swój zweryfikowany port
    send_with_handshake("/dev/ttyUSB1", 115200)