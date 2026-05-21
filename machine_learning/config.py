from dataclasses import dataclass

@dataclass
class DSPConfig:
    audio_sample_rate: int = 16000
    audio_channels: int = 1

    ml_window_size_ms: int = 40
    ml_stride_size_ms: int = 20

    fft_size: int = 1024
    fft_hop_size: int = 512  # 50% overlap
    mel_bins: int = 40

    @property
    def ml_window_samples(self) -> int:
        return int((self.audio_sample_rate * self.ml_window_size_ms) / 1000)

    @property
    def ml_stride_samples(self) -> int:
        return int((self.audio_sample_rate * self.ml_stride_size_ms) / 1000)

    @property
    def spectrum_cols(self) -> int:
        return int(self.fft_size / 2)

    @property
    def spectrum_rows(self) -> int:
        return int((self.ml_window_samples - self.fft_size) / self.fft_hop_size) + 1

    @property
    def spectrum_total_size(self) -> int:
        return self.spectrum_rows * self.spectrum_cols
