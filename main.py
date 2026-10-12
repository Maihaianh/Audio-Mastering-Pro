import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
import numpy as np
import soundfile as sf

class AMMHAApp(App):
    def build(self):
        self.title = "AM-MHA Pro - Audio Mastering"
        self.selected_file = None

        root = BoxLayout(orientation='vertical', padding=15, spacing=10)

        root.add_widget(Label(text="[b]AM-MHA AUDIO MASTERING PRO[/b]", markup=True, font_size=20, size_hint_y=None, height=40))

        self.file_label = Label(text="Chưa chọn file âm thanh", color=(0.6, 0.6, 0.6, 1), size_hint_y=None, height=30)
        root.add_widget(self.file_label)
        
        btn_select = Button(text="01 / CHỌN FILE ÂM THANH (WAV/FLAC)", background_color=(0.5, 0.3, 0.9, 1), size_hint_y=None, height=50)
        btn_select.bind(on_press=self.open_file_chooser)
        root.add_widget(btn_select)

        root.add_widget(Label(text="02 / TONE & DYNAMICS (DSP)", bold=True, size_hint_y=None, height=30))
        
        root.add_widget(Label(text="Low Gain (dB): 0.0", size_hint_y=None, height=25))
        self.sld_low = Slider(min=-12, max=12, value=0, step=0.5)
        root.add_widget(self.sld_low)

        root.add_widget(Label(text="Compression (%): 35", size_hint_y=None, height=25))
        self.sld_comp = Slider(min=0, max=100, value=35)
        root.add_widget(self.sld_comp)

        root.add_widget(Label(text="Output Gain (dB): 0.0", size_hint_y=None, height=25))
        self.sld_gain = Slider(min=-6, max=6, value=0, step=0.1)
        root.add_widget(self.sld_gain)

        btn_export = Button(text="↓ XUẤT FILE MASTER WAV 24-BIT", background_color=(0.1, 0.7, 0.4, 1), size_hint_y=None, height=60)
        btn_export.bind(on_press=self.process_and_export)
        root.add_widget(btn_export)

        self.status_label = Label(text="Engine Ready - Offline Processing", color=(0.2, 0.9, 0.5, 1), size_hint_y=None, height=30)
        root.add_widget(self.status_label)

        return root

    def open_file_chooser(self, instance):
        content = FileChooserIconView(filters=['*.wav', '*.flac', '*.mp3'])
        content.bind(on_submit=self.file_selected)
        self.popup = Popup(title="Chọn file âm thanh", content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def file_selected(self, instance, selection, touch):
        if selection:
            self.selected_file = selection[0]
            self.file_label.text = f"Đã chọn: {os.path.basename(self.selected_file)}"
            self.popup.dismiss()

    def process_and_export(self, instance):
        if not self.selected_file:
            self.status_label.text = "Lỗi: Chưa chọn file đầu vào!"
            return

        self.status_label.text = "Đang xử lý Offline Mastering DSP..."
        
        try:
            data, samplerate = sf.read(self.selected_file)
            if len(data.shape) == 1:
                data = np.stack((data, data), axis=-1)

            low_gain = self.sld_low.value
            comp_ratio = 1.0 + (self.sld_comp.value / 20.0)
            output_gain_db = self.sld_gain.value

            if low_gain != 0:
                data[:, 0] *= (1.0 + (low_gain / 10.0))
                data[:, 1] *= (1.0 + (low_gain / 10.0))

            threshold = 0.7
            compressed_data = np.where(np.abs(data) > threshold, 
                                       threshold + (np.abs(data) - threshold) / comp_ratio * np.sign(data), 
                                       data)

            gain_linear = 10 ** (output_gain_db / 20.0)
            final_data = compressed_data * gain_linear
            final_data = np.clip(final_data, -1.0, 1.0)

            output_filename = os.path.splitext(self.selected_file)[0] + "_AM_MHA_Mastered.wav"
            sf.write(output_filename, final_data, samplerate, subtype='PCM_24')

            self.status_label.text = f"Thành công! Đã lưu: {os.path.basename(output_filename)}"
        except Exception as e:
            self.status_label.text = f"Lỗi xử lý: {str(e)}"

if __name__ == '__main__':
    AMMHAApp().run()