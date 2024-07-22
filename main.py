import hashlib
import os
import subprocess
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.utils import platform

# Import plyer for Android permissions
if platform == 'android':
    from plyer import storagepath


class FileCheckerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10)
        
        self.label = Label(text='+++ BOS DEVICE CHECKER +++', size_hint=(1, 0.2))
        layout.add_widget(self.label)

        self.menu_label = Label(text='Menu:', size_hint=(1, 0.1))
        layout.add_widget(self.menu_label)

        self.menu_button1 = Button(text='1. FF ORI', size_hint=(1, 0.1))
        self.menu_button1.bind(on_press=self.menu_ff_ori)
        layout.add_widget(self.menu_button1)

        self.menu_button2 = Button(text='2. FF MAX', size_hint=(1, 0.1))
        self.menu_button2.bind(on_press=self.menu_ff_max)
        layout.add_widget(self.menu_button2)

        self.result_label = Label(text='', size_hint=(1, 0.2))
        layout.add_widget(self.result_label)

        return layout

    def request_storage_permission(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    def install_module(self, module):
        try:
            import importlib
            importlib.import_module(module)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

    def calculate_md5(self, filename):
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def verify_file_authenticity(self, filename, expected_md5sum, folder_path):
        full_path = os.path.join(folder_path, filename)

        actual_md5sum = self.calculate_md5(full_path)

        if actual_md5sum == expected_md5sum:
            result_text = "BERSIH, file asli."
        else:
            result_text = "CHEAT / RECODED DETECT, file palsu."
            try:
                os.remove(full_path)
                result_text += "\nFile Modifikasi berhasil dihapus."
            except OSError as e:
                result_text += "\nError!"

        # Create and display a popup with the result
        popup = Popup(title='Hasil Verifikasi', content=Label(text=result_text), size_hint=(None, None), size=(400, 400))
        popup.open()

    def menu_ff_ori(self, instance):
        self.request_storage_permission()  # Request storage permission on button press

        if platform == 'android':
            folder_path = storagepath.get_external_storage_path() + "/Android/obb/com.dts.freefireth"
        else:
            folder_path = "/storage/emulated/0/Android/obb/com.dts.freefireth"

        file_to_check = "main.2019117513.com.dts.freefireth.obb"
        expected_md5sum = 'b6d4e94323219665b848aaff1700a718'
        self.verify_file_authenticity(file_to_check, expected_md5sum, folder_path)

    def menu_ff_max(self, instance):
        self.request_storage_permission()  # Request storage permission on button press

        if platform == 'android':
            folder_path = storagepath.get_external_storage_path() + "/Android/obb/com.dts.freefiremax"
        else:
            folder_path = "/storage/emulated/0/Android/obb/com.dts.freefiremax"

        file_to_check = "main.2019114504.com.dts.freefiremax.obb"
        expected_md5sum = 'd37fef40978cd5f6fa564c090f7879bc'
        self.verify_file_authenticity(file_to_check, expected_md5sum, folder_path)


if __name__ == "__main__":
    FileCheckerApp().run()
