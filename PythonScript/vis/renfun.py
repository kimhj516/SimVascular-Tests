import vis
import vtk
# -------------
# ::vis::renNew
# -------------
def renNew(renWin):

    #@c Create a new vtkRenderer in the given vtkRenderWindow.  If the named
    #@c vtkRenderWindow does not exist, then create it.  Multiple renderers
    #@c can be contained in a particular render window.  These renderers are
    #@c named with a sequentially assigned identifier.
    #@a renWin: Existing render window, or name of render window to
    #@a renWin: to be created.
    try:
        getattr(vis,renWin[0])
        numRens = renWin[1].GetRenderers().GetNumberOfItems()
        renId = numRens+1
    except:
        renId = 1
        renWin[1] = vtk.vtkRenderWindow()
        iren = [None]*2
        iren[0] = "iren_%s" % (renWin[0])
        iren[1] = vtk.vtkRenderWindowInteractor()
        iren[1].SetRenderWindow(renWin[1])
        #$iren SetUserMethod { wm deiconify .vtkInteract }
        iren[1].Initialize()
        setattr(vis,iren[0], iren)
        
    ren = [None]*2
    ren[1] = vtk.vtkRenderer()
    ren[1].SetBackground(0,0,0)

    renWin[1].AddRenderer(ren[1])
    renWin[1].SetSize(320,320)
    
    ren[0] = "%s_ren%d" % (renWin[0], renId)
    setattr(vis,ren[0], ren)
    
    return ren



# -----------------------
# ::vis::renSetBackground
# -----------------------
def renSetBackground(ren, r,g,b):
    #@c Set the background color of the given
    #@c renderer.
    #@a ren: renderer
    #@a r: red (value between 0 and 1)
    #@a g: green (value between 0 and 1)
    #@a b: blue (value between 0 and 1)
    ren[1].SetBackground(r,g,b)
    vis.renfun.render(ren)
    return


# ---------------
# ::vis::renReset
# ---------------
def renReset(ren):
    #@c Reset the viewpoint of the renderer.
   #@a ren: renderer

    ren[1].ResetCamera()
    vis.renfun.render(ren)
    return

# --------------------
# ::vis::renSetFlatAll
# --------------------
def renSetFlatAll(ren):
    
    #@c Set the interpolation mode of all actors
    #@c displayed by given renderer to flat
    #@a ren: renderer
    actors = ren[1].GetActors()
    actors.InitTraversal()
    
    for i in range(0,actors.GetNumberOfItems()):
        a = actors.GetNextItem()
        a.GetProperty().SetInterpolationToFlat()
        vis.renfun.render(ren)
    return 

# -----------------------
# ::vis::renSetGouraudAll
# -----------------------
def renSetGouraudAll(ren):

    #@c Set interpolation to Gouraud shading
    #@c for all actors displayed in given renderer.
    #@a ren: renderer
    actors = ren[1].GetActors()
    actors.InitTraversal()
    
    for i in range(0,actors.GetNumberOfItems()):
        a = actors.GetNextItem()
        a.GetProperty().SetInterpolationToGouraud()
        vis.renfun.render(ren)
    return 

# ---------------------
# ::vis::renSetPhongAll
# ---------------------
def renSetPhongAll(ren):

    #@c Set interpolation to Phong shading for all
    #@c for all actors in given renderer.
    #@a ren: renderer
    actors = ren[1].GetActors()
    actors.InitTraversal()
    
    for i in range(0,actors.GetNumberOfItems()):
        a = actors.GetNextItem()
        a.GetProperty().SetInterpolationToPhong()
        vis.renfun.render(ren)
    return 
    
# ----------------------------
# ::vis::renParallelProjection
# ----------------------------
def renParallelProjection(ren):

  #@c Turn on parallel projection for given
  #@c renderer.
  #@a ren: renderer
    ren[1].GetActiveCamera().ParallelProjectionOn()
    vis.renfun.render(ren)
    return



# -------------------------------
# ::vis::renPerspectiveProjection
# -------------------------------
def renPerspectiveProjection(ren):

  #@c Turn on perspective projection for
  #@c given renderer
  #@a ren: renderer
    ren[1].GetActiveCamera().ParallelProjectionOff()
    vis.renfun.render(ren)
    return


# -------------------
# ::vis::renWriteJPEG
# -------------------
def renWriteJPEG(ren,args):
  #@c Save the current window image to a file
  #@c in jpeg format.  If no filename is specified,
  #@c then an interactive window is popped up asking
  #@c for a name to be given.
  #@a ren: renderer
  #@a args: filename
    if (args ==""):
        filename = raw_input("Please enter image name to save")
    else:
        filename = args
        
    if (filename ==""):
        return
        
    jwriter = vtk.vtkJPEGWriter()
    jwriter.ProgressiveOff()
    jwriter.SetQuality(95)
    ren.GetRenderWindow().Render()
    
    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(ren.GetRenderWindow())
    w2i.Update()
    
    jwriter.SetInput(w2i.GetOutput())
    jwriter.SetFileName(filename)
    jwriter.Write()
    
    del w2i
    del jwriter
    return 


# ------------------
# ::vis::renAddActor
# ------------------
def renAddActor(ren, actor):
  #@c Add the specified actor to the given
  #@c renderer.
  #@a ren: renderer
  #@a actor: vtkActor object
  #@warning should check here to see if
  #@warning actor has already been added
  ren[1].AddActor(actor[1])
  return


# -----------------
# ::vis::renRmActor
# -----------------
def renRmActor(ren, actor):
  #@c Remove given actor from renderer.
  #@a ren: renderer
  #@a actor: vtkActor object.
  ren[1].RemoveActor(actor[1])
  return

# -----------------
# ::vis::renAddProp
# -----------------
def renAddProp(ren,prop):
  #@c Add given prop to renderer
  #@a ren: renderer
  #@a prop: vtkProp object
    ren[1].AddProp(prop[1])
    return

# ----------------
# ::vis::renRmProp
# ----------------
def renRmProp(ren,prop):
  #@c Remove given prop from renderer
  #@a ren: renderer
  #@a prop:  vtkProp object  
  ren[1].RemoveProp(prop[1])
  return


# -------------
# ::vis::render
# -------------
def render(ren):
  #@c Render the current window.
  #@a ren: renderer
  vis.renfun.renderWindow(ren[1].GetRenderWindow())
  
 
  return 
  
def interact(ren):
  #@c interaction mode for the current window
  #@a ren: renderer  
  iren = getattr(vis, 'iren_'+ren[0])  
  iren[1].Start()

# ----------------
# ::vis::renFreeze
# ----------------
#def renFreeze(ren):
#
#  #@c Freeze the current window.
#  #@a ren: renderer
#  vis.frozen(ren) = 1
#  return 



# ------------------
# ::vis::renUnfreeze
# ------------------
#def renThaw(ren):
#
#  #@c unfreeze current window
#  #@a ren: renderer
#  if (vis.frozen(ren)):
#      vis.frozen(ren)==0
#      vis.renfun.renderWindow(ren.GetRenderWindow())
#  return

# -------------------
# ::vis::renderWindow
# -------------------
def renderWindow(win):

  #@c Render the current window.
  #@a win:  window name

  win.Render()
  return