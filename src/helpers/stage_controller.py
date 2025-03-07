



class StageController ():
    def __init__ (self):
        self.isStage1Activated()

    def stage1Activator(self):
        self.stage1isActivated = True
        self.stage2isActivated = False
        self.stage3isActivated = False
    
    def stage2Activator(self):
        self.stage1isActivated = False
        self.stage2isActivated = True

    def stage3Activator(self):
        self.stage2isActivated = False
        self.stage3isActivated = True   
