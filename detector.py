from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.config import Config

Config.set('input', 'mouse', 'mouse,disable_multitouch')

import os
import label_image


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ImgDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Detector(BoxLayout):
    chosenFolder = ObjectProperty(None)
    image = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_img_load(self):
        content = ImgDialog(load=self.loadImg, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load image", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, pathName):
        print('Debug:: Selected directory: ' + pathName[0])
        self.dismiss_popup()

    def loadImg(self, fileName):
        print('Debug:: Selected picture: ' + fileName[0])
        self.image.source = fileName[0]
        self.chosenFolder.text = fileName[0] + '\n'
        results = label_image.main(fileName[0])

        top_k = results.argsort()[-5:][::-1]
        labels = label_image.load_labels("tf_files/labels.txt")

        for i in top_k:
            self.chosenFolder.text += str(labels[i])+': '+str(round(results[i]*100, 2))+'%\n'

        self.dismiss_popup()


class DetectorApp(App):
    def build(self):
        return Detector()


app = DetectorApp()
app.run()
