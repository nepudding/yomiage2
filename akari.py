import pyvcroid2

class akari:
    def __init__(self):
        self.default = defaultParam()
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

    def getVoiceList(self):
        return self.voice_list
    
    def textToWav(self, text, filename):
        speech, tts_events = self.vc.textToSpeech(text)
        with open(filename, mode="wb") as f:
            f.write(speech)
        return filename

class defaultParam:
    def __init__(self):
        self.volume = 2.00
        self.speed = 1.25
        self.pitch = 1.10
        self.emphasis = 1.70
        self.pauseMiddle = 150
        self.pauseLong = 370
        self.pauseSentence = 800
        self.masterVolume = 1.20
        