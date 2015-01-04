#!/usr/bin/env python
# coding: iso-8859-1
"""The wxPython classes to help loading GUI from XRC file easily.

   Original version from Gary Lee,
   http://markmail.org/message/wqc2qp5vmafsgoeo#query:+page:1+mid:wqc2qp5vmafsgoeo+state:results

   modified by Tobias Eberle, 2010

"""

import wx
import wx.xrc as xrc

def MethodNameToEvent(name, prefix='on'):
    """Convert method name to event and event sources. The method name should 
    be one of following formats.
    
    <prefix>_<control name>_<event name>
    <prefix>_<id1>_<event name>
    <prefix>_<id1>_<id2>_<event name>
    
    For example, on_Button1_button method will be bound to EVT_BUTTON event 
    and Button1 control. on_1001_1010_button will be bound to EVT_BUTTON event
    and all control which id is between 1001 and 1010.
 
    @param name: Method name to be converted.
    @param prefix: The prefix of event. 
    
    @return: The return value contain four items. They are event object, event
        source, id1 and id2 which will be used in Bind method.
    """
    
    parts = name.split('_')
    if (len(parts) < 3):
        # error
        raise Exception('Invalid method name: ' + name)

    if (parts[0] != prefix):
        # ignore invalid prefixes
        return

    id1 = -1
    id2 = -1
    src = None
    if (parts[1].isdigit()):
        id1 = int(parts[1])
    else:
        src = parts[1]
    if (parts[2].isdigit()):
        id2 = int(parts[2])
        N = 3
    else:
        N = 2
    
    evtName = 'EVT_' + "_".join(parts[N:]).upper()

    try:
      evt = getattr(wx, evtName)
    except:
      raise Exception('Invalid event name "' + evtName + '" in ' + name)
    
    return evt, src, id1, id2

def AutoBindEvent(win, prefix='on', excludes=[]):
    """Bind methods of a given window object to corresponding events. The method
    name must following the rules which used by MethodNameToEvent function.
    
    @param win: The window object to be bound.
    @param prefix: The prefix of method name of event handler to be bound.
    @param excludes: All method names listed in the list will not be bound.
    """
    for attr in dir(win):
        if ((attr not in excludes) and (attr.startswith(prefix))):
            value = getattr(win, attr)
            if (callable(value)):
                event, src, id1, id2 = MethodNameToEvent(attr, prefix)
                if (src):
                    src_object = getattr(win, src)
                    if (src_object is None):
                        raise Exception('Cannot find widget "' + src + '" in ' + win.__class__.__name__)
                    else:
                        src = src_object
                if ((src is not None) or (id1 >= 0) or (id2 >= 0)):
                    win.Bind(event, value, src, id1, id2)

class XrcFrame(wx.Frame):
    """XrcFrame is a helper class derived from wx.Frame. It can help to load 
    frame from XRC resource automatically and bind the corresponding event 
    handlers easily."""
    
    def __init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, 
        pos=wx.DefaultPosition, size=wx.DefaultSize, 
        style=wx.DEFAULT_FRAME_STYLE, name=wx.FrameNameStr, 
        resName=None, res=None, autoBindEvt=True):
        """The constructor of XrcFrame. 
        
        @param self: self
        @param parent: The parent window.
        @param id: The id.
        @param title: The title.
        @param pos: The position of window.
        @param size: The size of window in pixel.
        @param name: The frame name.
        @param resName: The resource name of this window in XRC resource file.
        @param res: The XRC resource. If it's None, the global XRC resource will
            be used.
        @param autoBindEvt: If it's True, the method names of this window which
            matched the rules of MethodNameToEvent method will be bound to 
            corresponding event automatically.
        """
        
        pre = wx.PreFrame()
        
        if not res:
            self.res = xrc.XmlResource.Get()
        else:
            self.res = res
            
        if not resName:
            self.resName = self.__class__.__name__
        else:
            self.resName = resName
        
        self.res.LoadOnFrame(pre, parent, self.resName)
        self.PostCreate(pre)
        
        self.SetId(id)    
        self.SetTitle(title)
        self.SetPosition(pos)
        self.SetSize(size)
        self.SetWindowStyle(style)
        self.SetName(name)
        
        if autoBindEvt:
            AutoBindEvent(self)
            
    def __getattr__(self, name):
        ctrl = xrc.XRCCTRL(self, name)
        if (ctrl is None):
            raise AttributeError(self.__class__.__name__ + " instance has no attribute '" + name + "'")
        else:
            self.__dict__[name] = xrc.XRCCTRL(self, name)
            return self.__dict__[name]
        
    
class XrcDialog(wx.Dialog):
    """XrcDialog will load dialog from XRC resource automatically."""
    
    def __init__(self, parent, id=-1, title=wx.EmptyString, 
        pos=wx.DefaultPosition, size=wx.DefaultSize, 
        style=wx.DEFAULT_DIALOG_STYLE, name=wx.DialogNameStr,
        resName=None, res=None, autoBindEvt=True):
        """The constructor of XrcFrame. 
        
        @param self: self
        @param parent: The parent window.
        @param id: The id.
        @param title: The title.
        @param pos: The position of window.
        @param size: The size of window in pixel.
        @param name: The dialog name.
        @param resName: The resource name of this window in XRC resource file.
        @param res: The XRC resource. If it's None, the global XRC resource will
            be used.
        @param autoBindEvt: If it's True, the method names of this window which
            matched the rules of MethodNameToEvent method will be bound to 
            corresponding event automatically.
        """
        pre = wx.PreDialog()
        
        if not res:
            self.res = xrc.XmlResource.Get()
        else:
            self.res = res
            
        if not resName:
            self.resName = self.__class__.__name__
        else:
            self.resName = resName
            
        self.res.LoadOnDialog(pre, parent, self.resName)
        self.PostCreate(pre)
        
        self.SetId(id)
        self.SetTitle(title)
        self.SetPosition(pos)
        self.SetSize(size)
        self.SetWindowStyle(style)
        self.SetName(name)
        
        if autoBindEvt:
            AutoBindEvent(self)
            
    def __getattr__(self, name):
        ctrl = xrc.XRCCTRL(self, name)
        if (ctrl is None):
            raise AttributeError(self.__class__.__name__ + " instance has no attribute '" + name + "'")
        else:
            self.__dict__[name] = xrc.XRCCTRL(self, name)
            return self.__dict__[name]

class XrcPanel(wx.Panel):
    """XrcPanel will load panel from XRC resource automatically."""
    
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, 
        size=wx.DefaultSize, style=wx.TAB_TRAVERSAL|wx.NO_BORDER, 
        name=wx.EmptyString, resName=None, res=None, autoBindEvt=True):
        """The constructor of XrcFrame. 
        
        @param self: self
        @param parent: The parent window.
        @param id: The id.
        @param pos: The position of window.
        @param size: The size of window in pixel.
        @param name: The panel name.
        @param resName: The resource name of this window in XRC resource file.
        @param res: The XRC resource. If it's None, the global XRC resource will
            be used.
        @param autoBindEvt: If it's True, the method names of this window which
            matched the rules of MethodNameToEvent method will be bound to 
            corresponding event automatically.
        """
        pre = wx.PrePanel()
        
        if not res:
            self.res = xrc.XmlResource.Get()
        else:
            self.res = res
            
        if not resName:
            self.resName = self.__class__.__name__
        else:
            self.resName = resName
            
        self.res.LoadOnPanel(pre, parent, self.resName)
        self.PostCreate(pre)
        
        self.SetId(id)
        self.SetPosition(pos)
        self.SetSize(size)
        self.SetWindowStyle(style)
        self.SetName(name)
        
        if autoBindEvt:
            AutoBindEvent(self)
            
    def __getattr__(self, name):
        ctrl = xrc.XRCCTRL(self, name)
        if (ctrl is None):
            raise AttributeError(self.__class__.__name__ + " instance has no attribute '" + name + "'")
        else:
            self.__dict__[name] = xrc.XRCCTRL(self, name)
            return self.__dict__[name]
        

# EOF.
