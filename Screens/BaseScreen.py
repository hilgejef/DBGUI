
class BaseScreen:
    def __init__(self):
        self.ActionWidgets = []
        self.PassiveWidgets = []
        self.CurrentWidget = 0
        self.Init()
    
    # Initializes the screen on construction (virtual)
    def Init(self):
        pass
    
    # Hides the screen by hiding all widgets
    def Hide(self):
        for w in self.PassiveWidgets:
            w.Pnl.hide()
        for w in self.ActionWidgets:
            w.Pnl.hide()
    
    # Shows the screen by displaying all widgets
    def Show(self):
        for w in self.PassiveWidgets:
            w.Pnl.show()
        for w in self.ActionWidgets:
            w.Pnl.show()        
        self.ActionWidgets[self.CurrentWidget].Active()
    
    # Moves all of the screen's widgets to the bottom
    def ToTop(self):
        for w in self.PassiveWidgets:
            w.Pnl.bottom()
        for w in self.ActionWidgets:
            w.Pnl.bottom()
    
    # Moves all of the screen's widgets to the bottom
    def ToBottom(self):
        for w in self.PassiveWidgets:
            w.Pnl.bottom()
        for w in self.ActionWidgets:
            w.Pnl.bottom()
    
    # Advance to the next active widget
    def NextWidget(self):
        self.CurrentWidget += 1
        if self.CurrentWidget >= len(self.ActionWidgets):
            self.CurrentWidget = 0
        self.ActionWidgets[self.CurrentWidget].Active()
    
    # Virtual method to be overloaded
    # Must return the next screen to be visited
    def Next(self):
        return None
