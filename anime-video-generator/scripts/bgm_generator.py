#!/usr/bin/env python3
"""
专业古风BGM生成器 — 模拟剪映热门仙侠古风音乐
特点：
- 古筝拨弦 + 竹笛旋律 + 空灵pad + 鼓点节拍
- 中国五声音阶（宫商角徵羽）
- 明确的节拍点，供转场卡点使用
- 44100Hz 立体声输出
"""

import numpy as np
import math
import random
import struct
import wave
import os


def midi_to_freq(note):
    """MIDI音符号转频率"""
    return 440.0 * (2.0 ** ((note - 69) / 12.0))


# 中国五声音阶 (C D E G A) 的MIDI音符
# C4=60, D4=62, E4=64, G4=67, A4=69
PENTATONIC_BASE = [60, 62, 64, 67, 69]  # 宫商角徵羽

def get_pentatonic_scale(octave_offset=0):
    """获取指定八度的五声音阶"""
    return [n + octave_offset * 12 for n in PENTATONIC_BASE]


class AncientBGMGenerator:
    def __init__(self, duration=35, sr=44100, bpm=72):
        self.duration = duration
        self.sr = sr
        self.bpm = bpm
        self.beat_duration = 60.0 / bpm  # 每拍时长（秒）
        self.total_samples = int(duration * sr)
        self.t = np.linspace(0, duration, self.total_samples, endpoint=False)
        self.rng = random.Random(42)
        
        # 节拍时间点（用于转场卡点）
        self.beat_times = []
        t = 0
        while t < duration:
            self.beat_times.append(t)
            t += self.beat_duration
        
        # 强拍时间点（每4拍一个强拍，更适合转场）
        self.strong_beat_times = [self.beat_times[i] for i in range(0, len(self.beat_times), 4)]
    
    def _envelope_adsr(self, start, dur, attack=0.02, decay=0.1, sustain_level=0.7, release=0.3):
        """ADSR包络"""
        env = np.zeros(self.total_samples)
        s_start = int(start * self.sr)
        s_end = min(int((start + dur) * self.sr), self.total_samples)
        
        for i in range(s_start, s_end):
            local_t = (i - s_start) / self.sr
            if local_t < attack:
                env[i] = local_t / attack
            elif local_t < attack + decay:
                env[i] = 1.0 - (1.0 - sustain_level) * (local_t - attack) / decay
            elif local_t < dur - release:
                env[i] = sustain_level
            else:
                remaining = dur - local_t
                env[i] = sustain_level * max(0, remaining / release)
        
        return env
    
    def guzheng_pluck(self, freq, start, dur, amp=0.12):
        """
        古筝拨弦音色 — 模拟真实古筝的泛音结构
        特点：快速起音、指数衰减、丰富泛音、轻微滑音
        """
        signal = np.zeros(self.total_samples)
        s_start = int(start * self.sr)
        s_end = min(int((start + dur) * self.sr), self.total_samples)
        
        if s_start >= self.total_samples:
            return signal
        
        length = s_end - s_start
        local_t = np.arange(length) / self.sr
        
        # 快速起音 + 指数衰减（模拟拨弦）
        attack = np.minimum(local_t / 0.005, 1.0)  # 5ms超快起音
        decay = np.exp(-local_t * 3.5 / dur)
        envelope = attack * decay
        
        # 泛音结构（古筝特征：基频强，二次泛音适中，高次泛音快速衰减）
        tone = np.sin(2 * np.pi * freq * local_t) * 1.0
        tone += np.sin(2 * np.pi * freq * 2 * local_t) * 0.45 * np.exp(-local_t * 1.5)
        tone += np.sin(2 * np.pi * freq * 3 * local_t) * 0.20 * np.exp(-local_t * 2.5)
        tone += np.sin(2 * np.pi * freq * 4 * local_t) * 0.08 * np.exp(-local_t * 4.0)
        tone += np.sin(2 * np.pi * freq * 5 * local_t) * 0.03 * np.exp(-local_t * 6.0)
        
        # 轻微滑音效果（古筝揉弦）
        vibrato_depth = 0.003 * np.exp(-local_t * 2.0)  # 衰减的揉弦
        vibrato = 1 + vibrato_depth * np.sin(2 * np.pi * 5.5 * local_t)
        tone *= vibrato
        
        # 拨弦噪声（增加真实感）
        noise = np.random.RandomState(int(freq * 100)).randn(length) * 0.02
        noise *= np.exp(-local_t * 30)  # 噪声快速衰减
        
        signal[s_start:s_end] = amp * (tone * envelope + noise * decay)
        return signal
    
    def bamboo_flute(self, freq, start, dur, amp=0.08):
        """
        竹笛音色 — 空灵悠扬
        特点：柔和起音、气息感、颤音
        """
        signal = np.zeros(self.total_samples)
        s_start = int(start * self.sr)
        s_end = min(int((start + dur) * self.sr), self.total_samples)
        
        if s_start >= self.total_samples:
            return signal
        
        length = s_end - s_start
        local_t = np.arange(length) / self.sr
        
        # 柔和ADSR
        attack_t = min(0.25, dur * 0.15)
        release_t = min(0.4, dur * 0.2)
        attack = np.minimum(local_t / attack_t, 1.0)
        release = np.minimum((dur - local_t) / release_t, 1.0)
        envelope = attack * release * np.clip(release, 0, 1)
        
        # 颤音（竹笛特征）
        vibrato_rate = 5.2 + 0.8 * np.sin(2 * np.pi * 0.3 * local_t)  # 变化的颤音速率
        vibrato = 1 + 0.006 * np.sin(2 * np.pi * vibrato_rate * local_t)
        
        # 音色：基频为主 + 少量偶次泛音（竹笛特征）
        tone = np.sin(2 * np.pi * freq * vibrato * local_t) * 1.0
        tone += np.sin(2 * np.pi * freq * 2 * vibrato * local_t) * 0.30
        tone += np.sin(2 * np.pi * freq * 3 * vibrato * local_t) * 0.10
        
        # 气息噪声（增加竹笛真实感）
        breath = np.random.RandomState(int(freq * 50)).randn(length) * 0.015
        breath_env = envelope * 0.5
        
        signal[s_start:s_end] = amp * (tone * envelope + breath * breath_env)
        return signal
    
    def taiko_drum(self, start, amp=0.15, pitch=60):
        """
        太鼓/大鼓 — 低沉有力的节拍
        """
        signal = np.zeros(self.total_samples)
        dur = 0.4
        s_start = int(start * self.sr)
        s_end = min(int((start + dur) * self.sr), self.total_samples)
        
        if s_start >= self.total_samples:
            return signal
        
        length = s_end - s_start
        local_t = np.arange(length) / self.sr
        
        # 快速起音 + 指数衰减
        envelope = np.exp(-local_t * 8) * np.minimum(local_t / 0.003, 1.0)
        
        # 低频基音 + 频率下滑（鼓皮振动特征）
        freq = pitch * np.exp(-local_t * 3)  # 频率下滑
        phase = 2 * np.pi * np.cumsum(freq) / self.sr
        tone = np.sin(phase)
        
        # 冲击噪声
        noise = np.random.RandomState(int(start * 1000)).randn(length)
        noise_env = np.exp(-local_t * 25)
        
        signal[s_start:s_end] = amp * (tone * envelope * 0.7 + noise * noise_env * 0.3)
        return signal
    
    def wood_block(self, start, amp=0.06):
        """木鱼/木块 — 清脆的节拍标记"""
        signal = np.zeros(self.total_samples)
        dur = 0.08
        s_start = int(start * self.sr)
        s_end = min(int((start + dur) * self.sr), self.total_samples)
        
        if s_start >= self.total_samples:
            return signal
        
        length = s_end - s_start
        local_t = np.arange(length) / self.sr
        
        envelope = np.exp(-local_t * 50)
        tone = np.sin(2 * np.pi * 800 * local_t) + 0.5 * np.sin(2 * np.pi * 1200 * local_t)
        
        signal[s_start:s_end] = amp * tone * envelope
        return signal
    
    def ambient_pad(self):
        """
        空灵背景pad — 营造仙侠氛围
        使用多层正弦波叠加，模拟空灵的和声垫
        """
        pad = np.zeros(self.total_samples)
        
        # 低频底层（温暖的基底）
        pad += 0.020 * np.sin(2 * np.pi * 110 * self.t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.15 * self.t))
        pad += 0.015 * np.sin(2 * np.pi * 165 * self.t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.12 * self.t))
        
        # 中频和声层
        pad += 0.012 * np.sin(2 * np.pi * 220 * self.t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.08 * self.t))
        pad += 0.008 * np.sin(2 * np.pi * 330 * self.t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.10 * self.t))
        pad += 0.006 * np.sin(2 * np.pi * 440 * self.t) * (0.4 + 0.6 * np.sin(2 * np.pi * 0.07 * self.t))
        
        # 高频泛音（空灵感）
        pad += 0.004 * np.sin(2 * np.pi * 660 * self.t) * (0.3 + 0.7 * np.sin(2 * np.pi * 0.05 * self.t))
        pad += 0.003 * np.sin(2 * np.pi * 880 * self.t) * (0.2 + 0.8 * np.sin(2 * np.pi * 0.04 * self.t))
        
        # 缓慢的滤波效果（模拟呼吸感）
        breath = 0.5 + 0.5 * np.sin(2 * np.pi * 0.18 * self.t)
        pad *= breath
        
        return pad
    
    def generate_guzheng_melody(self):
        """古筝主旋律 — 模拟剪映热门古风曲风"""
        melody = np.zeros(self.total_samples)
        
        # 经典古风旋律走向（模拟《权御天下》《千秋此意》风格）
        # 使用五声音阶，每个乐句4-8拍
        scale_low = get_pentatonic_scale(-1)   # C3-A3
        scale_mid = get_pentatonic_scale(0)    # C4-A4
        scale_high = get_pentatonic_scale(1)   # C5-A5
        
        # 预设的旋律片段（音符索引 in scale_mid, 持续拍数）
        phrases = [
            # 乐句1：起（悠扬开场）
            [(2, 2), (4, 1), (3, 1), (2, 2), (1, 2)],
            # 乐句2：承（上行发展）
            [(0, 1), (1, 1), (2, 2), (4, 1), (3, 1), (2, 2)],
            # 乐句3：转（高潮）
            [(4, 2), (3, 1), (4, 1), (2, 2), (0, 1), (1, 1)],
            # 乐句4：合（回落收束）
            [(3, 1.5), (2, 1.5), (1, 1), (0, 2), (2, 2)],
        ]
        
        time_pos = self.beat_duration * 4  # 从第4拍开始（前面是引子）
        phrase_idx = 0
        
        while time_pos < self.duration - 4:
            phrase = phrases[phrase_idx % len(phrases)]
            
            for note_idx, beats in phrase:
                if time_pos >= self.duration - 2:
                    break
                
                # 选择音域（随乐句发展变化）
                if phrase_idx % 4 == 2:  # 高潮段用高音域
                    scale = scale_high
                    amp = 0.10
                elif phrase_idx % 4 == 0:  # 开头用中音域
                    scale = scale_mid
                    amp = 0.08
                else:
                    scale = scale_mid
                    amp = 0.09
                
                freq = midi_to_freq(scale[note_idx % len(scale)])
                dur = beats * self.beat_duration
                
                melody += self.guzheng_pluck(freq, time_pos, dur * 1.2, amp=amp)
                time_pos += dur
            
            # 乐句间短暂停顿
            time_pos += self.beat_duration * self.rng.choice([1, 2])
            phrase_idx += 1
        
        return melody
    
    def generate_guzheng_arpeggio(self):
        """古筝琶音伴奏 — 如流水般的分解和弦"""
        arp = np.zeros(self.total_samples)
        
        # 和弦进行（五声音阶和弦）
        chord_progressions = [
            [60, 64, 67],    # C E G (宫和弦)
            [62, 67, 69],    # D G A (商和弦)
            [64, 67, 72],    # E G C' (角和弦)
            [60, 64, 69],    # C E A (宫-羽)
        ]
        
        time_pos = 2.0  # 2秒后开始
        chord_idx = 0
        
        while time_pos < self.duration - 3:
            chord = chord_progressions[chord_idx % len(chord_progressions)]
            
            # 每个和弦持续4拍，琶音分解
            for beat in range(4):
                if time_pos >= self.duration - 2:
                    break
                
                for i, note in enumerate(chord):
                    t = time_pos + i * 0.08  # 每个音间隔80ms（琶音效果）
                    freq = midi_to_freq(note - 12)  # 低一个八度
                    arp += self.guzheng_pluck(freq, t, self.beat_duration * 0.8, amp=0.04)
                
                time_pos += self.beat_duration
            
            time_pos += self.beat_duration  # 和弦间停顿
            chord_idx += 1
        
        return arp
    
    def generate_flute_melody(self):
        """竹笛副旋律 — 在古筝旋律间隙穿插"""
        flute = np.zeros(self.total_samples)
        
        scale = get_pentatonic_scale(1)  # 高八度，更空灵
        
        # 笛子在第8秒后才进入
        time_pos = 8.0
        note_idx = 3  # 从徵音开始
        
        while time_pos < self.duration - 4:
            freq = midi_to_freq(scale[note_idx % len(scale)])
            dur = self.beat_duration * self.rng.choice([2, 3, 4])
            
            flute += self.bamboo_flute(freq, time_pos, dur, amp=0.06)
            
            time_pos += dur + self.beat_duration * self.rng.choice([1, 2, 3])
            note_idx += self.rng.choice([1, 2, -1, -2])
            note_idx = max(0, min(len(scale) - 1, note_idx))
        
        return flute
    
    def generate_drum_pattern(self):
        """鼓点节拍 — 提供明确的节拍感"""
        drums = np.zeros(self.total_samples)
        
        beat_idx = 0
        for bt in self.beat_times:
            if bt < 3.0 or bt > self.duration - 3:
                beat_idx += 1
                continue  # 前3秒和后3秒不加鼓
            
            pos_in_bar = beat_idx % 4
            
            if pos_in_bar == 0:
                # 强拍：大鼓
                drums += self.taiko_drum(bt, amp=0.12, pitch=55)
                drums += self.wood_block(bt, amp=0.04)
            elif pos_in_bar == 2:
                # 次强拍：轻鼓
                drums += self.taiko_drum(bt, amp=0.06, pitch=65)
            
            if pos_in_bar in [1, 3]:
                # 弱拍：木鱼
                drums += self.wood_block(bt, amp=0.025)
            
            beat_idx += 1
        
        return drums
    
    def generate(self):
        """生成完整BGM"""
        print("🎵 生成古风BGM...")
        print(f"   BPM: {self.bpm}, 时长: {self.duration}s")
        print(f"   节拍间隔: {self.beat_duration:.3f}s")
        print(f"   总节拍数: {len(self.beat_times)}")
        print(f"   强拍数: {len(self.strong_beat_times)}")
        
        # 各层音轨
        print("   🎸 生成空灵pad...")
        pad = self.ambient_pad()
        
        print("   🎸 生成古筝主旋律...")
        guzheng = self.generate_guzheng_melody()
        
        print("   🎸 生成古筝琶音...")
        arpeggio = self.generate_guzheng_arpeggio()
        
        print("   🎸 生成竹笛旋律...")
        flute = self.generate_flute_melody()
        
        print("   🥁 生成鼓点节拍...")
        drums = self.generate_drum_pattern()
        
        # 混音
        print("   🎛️ 混音...")
        mix = pad + guzheng + arpeggio + flute + drums
        
        # 淡入淡出
        fade_in = np.minimum(self.t / 2.5, 1.0)
        fade_out = np.minimum((self.duration - self.t) / 3.0, 1.0)
        mix *= fade_in * fade_out
        
        # 轻微压缩（防止削波）
        peak = np.max(np.abs(mix))
        if peak > 0:
            mix = mix / peak * 0.75
        
        # 软限幅
        mix = np.tanh(mix * 1.2) * 0.8
        
        print("   ✅ BGM生成完成")
        return mix
    
    def save_wav(self, audio, path):
        """保存为WAV文件"""
        audio_16bit = np.clip(audio * 32767, -32768, 32767).astype(np.int16)
        
        with wave.open(path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sr)
            wf.writeframes(audio_16bit.tobytes())
        
        size_kb = os.path.getsize(path) / 1024
        print(f"   💾 保存: {path} ({size_kb:.0f}KB)")
    
    def get_beat_times_for_video(self, video_duration):
        """
        返回适合视频转场的节拍时间点
        选择强拍（每4拍），且在视频时长范围内
        """
        # 过滤：跳过前2秒和后3秒
        valid_beats = [
            bt for bt in self.strong_beat_times 
            if 2.0 < bt < video_duration - 3.0
        ]
        return valid_beats


def generate_bgm_and_beats(duration=35, bpm=72, output_wav=None):
    """
    生成BGM音频和节拍时间点
    返回: (audio_array, beat_times, sr)
    """
    gen = AncientBGMGenerator(duration=duration, sr=44100, bpm=bpm)
    audio = gen.generate()
    beats = gen.get_beat_times_for_video(duration)
    
    if output_wav:
        gen.save_wav(audio, output_wav)
    
    return audio, beats, gen.sr, gen.beat_duration


if __name__ == "__main__":
    audio, beats, sr, beat_dur = generate_bgm_and_beats(
        duration=35, bpm=72, 
        output_wav="/data/workspace/anime_videos/bgm_ancient.wav"
    )
    print(f"\n节拍时间点 (用于转场):")
    for i, bt in enumerate(beats):
        print(f"  [{i}] {bt:.2f}s")
    print(f"\n每拍时长: {beat_dur:.3f}s")
