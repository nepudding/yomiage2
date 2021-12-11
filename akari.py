import pyvcroid2

class akari:
    def __init__(self):
        self.vc = pyvcroid2.VcRoid2()
        if "standard" in self.vc.listLanguages():
            self.vc.loadLanguage("standard")
        else:
            raise Exception("No language library")
        self.voice_list = self.vc.listVoices()
        if 0 < len(self.voice_list):
            self.vc.loadVoice(self.voice_list[0])
        else:
            raise Exception("No voice library")
        self.vc.reloadWordDictionary(r"dict\user.wdic")
        self.vc.reloadPhraseDictionary(r"dict\user.pdic")

        # 腹から声出す
        self.vc.param.volume = self.vc.param.maxVolume

    def getVoiceList(self):
        return self.voice_list
    
    def textToWav(self, text, filename):
        speech, tts_events = self.vc.textToSpeech(text)
        with open(filename, mode="wb") as f:
            f.write(speech)
        return filename

        