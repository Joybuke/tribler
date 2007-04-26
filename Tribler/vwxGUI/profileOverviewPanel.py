import wx
import wx.xrc as xrc
import random
from Tribler.vwxGUI.GuiUtility import GUIUtility

class ProfileOverviewPanel(wx.Panel):
    def __init__(self, *args, **kw):
#        print "<mluc> tribler_topButton in init"
        self.initDone = False
        self.elementsName = [ 'perf_Overall', 'text_Overall', 'icon_Overall', 'bgPanel_Quality', 'perf_Quality',
                          'text_Quality', 'bgPanel_Files', 'perf_Files', 'text_Files', 'bgPanel_Persons',
                          'perf_Persons', 'text_Persons', 'bgPanel_Download', 'perf_Download', 'text_Download', 
                          'bgPanel_Presence', 'perf_Presence', 'text_Presence']
        self.elements = {}
        if len(args) == 0: 
            pre = wx.PrePanel() 
            # the Create step is done by XRC. 
            self.PostCreate(pre) 
            self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate) 
        else:
            wx.Panel.__init__(self, *args, **kw) 
            self._PostInit()     
        
    def OnCreate(self, event):
#        print "<mluc> tribler_topButton in OnCreate"
        self.Unbind(wx.EVT_WINDOW_CREATE)
        wx.CallAfter(self._PostInit)
        event.Skip()
        return True
    
    def _PostInit(self):
#        print "<mluc> tribler_topButton in _PostInit"
        # Do all init here
        self.guiUtility = GUIUtility.getInstance()
#        self.Bind(wx.EVT_MOUSE_EVENTS, self.mouseAction)
        self.Bind(wx.EVT_LEFT_UP, self.guiUtility.buttonClicked)
        
        for element in self.elementsName:
            xrcElement = xrc.XRCCTRL(self, element)
            if not xrcElement:
                print 'profileOverviewPanel: Error: Could not identify xrc element:',element
            self.elements[element] = xrcElement

        #add mouse over text and progress icon
        for elem_name in self.elementsName:
            if elem_name.startswith("bgPanel_") and self.getGuiElement(elem_name).__class__.__name__.endswith("tribler_topButton") :
                suffix = elem_name[8:]
                self.getGuiElement('text_%s' % suffix).Bind(wx.EVT_MOUSE_EVENTS, self.getGuiElement(elem_name).mouseAction)
                self.getGuiElement('perf_%s' % suffix).Bind(wx.EVT_MOUSE_EVENTS, self.getGuiElement(elem_name).mouseAction)
        #add click event for panels in this panel:
        
#        self.getGuiElement('bgPanel_Quality').Bind(wx.EVT_LEFT_UP, self.guiUtility.buttonClicked)
        self.getGuiElement('bgPanel_Files').Bind(wx.EVT_LEFT_UP, self.guiUtility.buttonClicked)
        self.getGuiElement('bgPanel_Persons').Bind(wx.EVT_LEFT_UP, self.guiUtility.buttonClicked)
        self.getGuiElement('bgPanel_Download').Bind(wx.EVT_LEFT_UP, self.guiUtility.buttonClicked)
        self.getGuiElement('bgPanel_Presence').Bind(wx.EVT_LEFT_UP, self.guiUtility.buttonClicked)

        #also set alternative background color:
#===============================================================================
#        bgpanels = ['bgPanel_Quality', 'bgPanel_Files', 'bgPanel_Persons', 'bgPanel_Download', 'bgPanel_Presence']
#        light_color = 'LIGHT_GREY'
#        darker_color = 'GREY'
#        color = light_color
#        for panel_name in bgpanels:
#            self.getGuiElement(panel_name).SetBackgroundColour(color)
#            if color == light_color:
#                color = darker_color
#            else:
#                color = light_color
#===============================================================================
        print "<mluc> full name for a panel is",self.getGuiElement('bgPanel_Quality').GetName(),"[",self.getGuiElement('bgPanel_Quality').GetParent().GetName(),"]"
        self.initDone = True
        self.Refresh(True)
#        self.Update()
        self.timer = None
        wx.CallAfter(self.reloadData)

    def getGuiElement(self, name):
        if not self.elements[name]:
            print "[profileOverviewPanel] gui element %s not available" % name
        return self.elements[name]
    
    def reloadData(self, event=None):
        """updates the fields in the panel with new data if it has changed"""
        if not self.IsShown(): #should not update data if not shown
            return
        bShouldRefresh = False

        #set the overall performance to a random number
        new_index = random.randint(0,5) #used only for testing
        elem = self.getGuiElement("perf_Overall")
        if elem and new_index != elem.getIndex():
            elem.setIndex(new_index)
            bShouldRefresh = True
        #set the overall ranking to a random number
        new_index = random.randint(0,3) #used only for testing
        elem = self.getGuiElement("icon_Overall")
        if elem and new_index != elem.getIndex():
            elem.setIndex(new_index)
            bShouldRefresh = True
        
        #get the number of downloads for this user
        count = self.guiUtility.data_manager.getDownloadHistCount()
        if count > 100:
            count = 100
        if count < 0:
            count = 0
        new_index = int((count-1)/20)+1
        qualityElem = self.getGuiElement("perf_Quality")
        if qualityElem and new_index != qualityElem.getIndex():
            qualityElem.setIndex(new_index)
            bShouldRefresh = True
        
        #get the number of similar peers
        count = self.guiUtility.peer_manager.getCountOfSimilarPeers()
        if count > 500:
            count = 500
        if count < 0:
            count = 0
        new_index = int((count-1)/100)+1
        elem = self.getGuiElement("perf_Persons")
        if elem and new_index != elem.getIndex():
            elem.setIndex(new_index)
            bShouldRefresh = True
        
        if bShouldRefresh:
            self.Refresh()
        #wx.CallAfter(self.reloadData) #should be called from time to time
        if not self.timer:
            self.timer = wx.Timer(self, -1)
            self.Bind(wx.EVT_TIMER, self.reloadData, self.timer)
            self.timer.Start(2000)
        
    def mouseAction(self, event):
        pass
#        print "mouse event in panel"
        