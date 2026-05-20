import numpy as np
import scipy.io.wavfile as wav
import librosa
from config import DSPConfig

class DSPPreprocessor:
    def __init__(self, config: DSPConfig):
        self.config = config
        
        self.window_coeffs = np.hanning(self.config.fft_size)
        
        self.mel_filterbank = librosa.filters.mel(
            sr=self.config.audio_sample_rate, 
            n_fft=self.config.fft_size, 
            n_mels=self.config.mel_bins,
            fmin=0.0,
            fmax=self.config.audio_sample_rate / 2.0
        )

    def process_single_frame(self, frame_16bit):
        val = (frame_16bit / 32768.0) * self.window_coeffs
        
        fft_result = np.fft.rfft(val, n=self.config.fft_size)
        
        power_spectrum = np.real(fft_result)**2 + np.imag(fft_result)**2
        
        mel_energy = np.dot(self.mel_filterbank, power_spectrum)
        
        output_mel = 10.0 * np.log10(mel_energy + 1e-10)
        
        return output_mel

    def generate_spectrogram(self, wav_path):
        sample_rate, audio_data = wav.read(wav_path)
        
        if sample_rate != self.config.audio_sample_rate:
            raise ValueError(f"Sample rate mismatch, file has {sample_rate}Hz, config needs {self.config.audio_sample_rate}Hz.")
        
        spectrogram = []
        
        for start_idx in range(0, len(audio_data) - self.config.fft_size + 1, self.config.stride_samples):
            frame = audio_data[start_idx : start_idx + self.config.fft_size]
            mel_vector = self.process_single_frame(frame)
            spectrogram.append(mel_vector)
            
        spectrogram_matrix = np.array(spectrogram)
        
        if len(spectrogram_matrix) >= self.config.frames_required:
            return spectrogram_matrix[:self.config.frames_required, :]
        else:
            raise ValueError("Audio file is too short")