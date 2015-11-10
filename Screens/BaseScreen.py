class BaseScreen:
    def __init__(self):
        self.ActionWidgets = []
        self.PassiveWidgets = []
        self.CurrentWidget = 0
        self.Init()
    
    # Initializes the screen on construction (virtual)
    def Init(self):
        pass

    # Calls UpdateDisplay() on all widgets
    def Update(self):
        for w in self.PassiveWidgets:
            w.UpdateDisplay()
        for w in self.ActiveWidgets:
            w.UpdateDisplay()
    
    # Hides the screen by hiding all widgets
    def Hide(self):
        for w in self.PassiveWidgets:
            w.Hide()
        for w in self.ActionWidgets:
            w.Hide()
    
    # Shows the screen by displaying all widgets
    def Show(self):
        for w in self.PassiveWidgets:
            w.Show()
        for w in self.ActionWidgets:
            w.Show()        
        if self.ActionWidgets:
            self.ActionWidgets[self.CurrentWidget].Active()
    
    # Moves all of the screen's widgets to the top
    def ToTop(self):
        for w in self.PassiveWidgets:
            w.ToTop()
        for w in self.ActionWidgets:
            w.ToTop()
    
    # Moves all of the screen's widgets to the bottom
    def ToBottom(self):
        for w in self.PassiveWidgets:
            w.ToBottom()
        for w in self.ActionWidgets:
            w.ToBottom()
    
    # Advance to the next active widget
    def NextWidget(self):
        self.CurrentWidget += 1
        if self.CurrentWidget >= len(self.ActionWidgets):
            self.CurrentWidget = 0
        if self.ActionWidgets:
            self.ActionWidgets[self.CurrentWidget].Active()
    
    # Virtual method to be overloaded
    # Must return the next screen to be visited
    def Next(self):
        return None
