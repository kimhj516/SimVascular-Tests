import vtk
import Repository
import vis
# -----------
# vis_imgInit
# -----------
def vis_imgInit(ren):
    rdr = [None]*2
    txt = [None]*2
    plane = [None]*2
    tmap = [None]*2
    cast = [None]*2
    vmap = [None]*2
    actor = [None]*2
    lookupGrayscale = [None]*2
    lookupColor = [None]*2
    
    rdr[0] = 'vis_img_reader_' + ren[0]
    txt[0] = 'vis_img_texture_' + ren[0]
    plane[0] = 'vis_img_plane_' + ren[0]
    tmap[0] = 'vis_img_tmap_' + ren[0]
    vmap[0] = 'vis_img_map_' + ren[0]
    actor[0] = 'vis_img_actor_' + ren[0]
    lookupGrayscale[0] = 'vis_img_g8bitGrayscaleLUT_' + ren[0]
    lookupColor[0] = 'vis_img_gBlueToRedLUT_'+ ren[0]
    
    rdr[1] = vtk.vtkImageReader()
    rdr[1].SetDataScalarTypeToShort()
    rdr[1].SetFileDimensionality(2)
    rdr[1].SetDataByteOrderToBigEndian()
    
    txt[1] = vtk.vtkTexture()
    plane[1] = vtk.vtkPlaneSource()
    plane[1].SetResolution(1,1)
    plane[1].SetOrigin(0.,0.,0.)
    
    tmap[1] = vtk.vtkTextureMapToPlane()
    tmap[1].SetInputConnection(plane[1].GetOutputPort())
    
    cast[1] = vtk.vtkCastToConcrete()
    cast[1].SetInputConnection(tmap[1].GetOutputPort())
    
    vmap[1] = vtk.vtkPolyDataMapper()
    vmap[1].SetInputConnection(cast[1].GetOutputPort())
    
    actor[1] = vtk.vtkActor()
    actor[1].SetMapper(vmap[1])
    actor[1].SetTexture(txt[1])
    
    lookupGrayscale[1] = vtk.vtkLookupTable()
    lookupGrayscale[1].SetHueRange(0.,0.)
    lookupGrayscale[1].SetSaturationRange(0.,0.)
    lookupGrayscale[1].SetValueRange(0.,1.)
    lookupGrayscale[1].SetNumberOfColors(16384)
    lookupGrayscale[1].Build()
    
    lookupColor[1] = vtk.vtkLookupTable()
    lookupColor[1].SetHueRange(0.6667,0.)
    lookupColor[1].SetSaturationRange(1.,1.)
    lookupColor[1].SetValueRange(1.,1.)
    lookupColor[1].SetAlphaRange(1.,1.)
    lookupColor[1].SetNumberOfColors(16384)
    lookupColor[1].Build()
    
    setattr(vis,rdr[0], rdr)
    setattr(vis,txt[0], txt)
    setattr(vis,plane[0], plane)
    setattr(vis,tmap[0], tmap)
    setattr(vis,vmap[0], vmap)
    setattr(vis,actor[0], actor)
    setattr(vis,lookupGrayscale[0], lookupGrayscale)
    setattr(vis,lookupColor[0], lookupColor)
    return
    
# ----------------
# vis_imgSetOrigin
# ----------------
def vis_imgSetOrigin(ren, x, y, z):
    try:
        plane = getattr(vis,'vis_img_plane_'+ren[0])
    except:
        return
    plane[1].SetOrigin(x,y,x)
    setattr(vis, plane[0], plane)
    vis.renfun.render(ren)
    return
    

# --------------
# vis_imgSetFile
# --------------
def vis_imgSetFile(ren, name, dims, spacing):
    try:
        rdr = getattr(vis, 'vis_img_reader_'+ren[0])
        txt = getattr(vis, 'vis_img_texture_'+ren[0])
        plane = getattr(vis, 'vis_img_plane_'+ren[0])
        actor = getattr(vis, 'vis_img_actor_'+ren[0])
        lookupGrayscale = getattr(vis, 'vis_img_g8bitGrayscaleLUT_'+ren[0])
    except:
        vis_imgInit(ren)

    rdr = getattr(vis, 'vis_img_reader_'+ren[0])
    txt = getattr(vis, 'vis_img_texture_'+ren[0])
    plane = getattr(vis, 'vis_img_plane_'+ren[0])
    actor = getattr(vis, 'vis_img_actor_'+ren[0])
    lookupGrayscale = getattr(vis, 'vis_img_g8bitGrayscaleLUT_'+ren[0])
    xsize = dims[0]*spacing[0]
    ysize = dims[1]*spacing[1]
    
    rdr[1].Modified()
    rdr[1].SetFileName(name)
    rdr[1].SetDataExtent(0, dims[0]-1,0, dims[1]-1, 1,1)
    rdr[1].SetDataSpacing(spacing[0], spacing[1], 1.0)
    rdr[1].Update()
    
    txt[1].SetInputConnection(rdr[1].GetOutputPort())
    txt[1].Render(ren[1])
    txt[1].SetLookupTable(lookupGrayscale[1])
    txt[1].RepeatOff()
    
    plane[1].SetPoint1(xsize, 0.,0.)
    plane[1].SetPoint2(0.,ysize, 0.)
    
    ren[1].AddActor(actor[1])
    vis.renfun.render(ren)
    
    return
    
# ------------
# vis_imgRepos
# ------------
def vis_imgRepos(ren , imgObj):
    try:
        vis_imgRm(ren)
    except:
        pass
    vis_imgInit(ren)
    if Repository.Type(imgObj) != "StructuredPts":
        raise ValueError("Object is not an imgae")
    vimg = Repository.ExportToVtk(imgObj)
    vorig = vimg.GetOrigin()
    vspc = vimg.GetSpacing()
    vdims = vimg.GetExtent()
    irng = vimg.GetScalarRange()
    
    if (vdims[4]!=vdims[5]+vdims[0]!=vdims[1]+vdims[2]!=vdims[3]):
        raise ValueError("image is not planar")
        return
        
    #logical image dims:
    ldims = []    
    ldims.append(vdims[1]-vdims[0]+1)
    ldims.append(vdims[3]-vdims[2]+1)
    ldims.append(vdims[5]-vdims[4]+1)
    
    #Physical image dimensions (spatial extent covered by pixels):
    pdims = []
    pdims.append(ldims[0]*vspc[0])
    pdims.append(ldims[1]*vspc[1])
    pdims.append(ldims[2]*vspc[2])
    
    # Physical origin of the physical extent:
    porig = []
    porig.append(vorig[0]-0.5*vspc[0])
    porig.append(vorig[1]-0.5*vspc[1])
    porig.append(vorig[2]-0.5*vspc[2])
    
    txt = getattr(vis, 'vis_img_texture_'+ren[0])
    plane = getattr(vis, 'vis_img_plane_' + ren[0])
    vmap = getattr(vis, 'vis_img_map_' + ren[0])
    actor = getattr(vis, 'vis_img_actor_'+ren[0])
    lookupGrayscale = getattr(vis, 'vis_img_g8bitGrayscaleLUT_'+ren[0])
    lookupColor = getattr(vis, 'vis_img_gBlueToRedLUT_'+ren[0])
    
    txt[1].SetInputDataObject(vimg)
    txt[1].Render(ren[1])
    txt[1].SetLookupTable(lookupGrayscale[1])
    txt[1].RepeatOff()
    
    plane[1].SetOrigin(porig[0],porig[1],0.)
    plane[1].SetPoint1(porig[0]+pdims[0],porig[1],0.)       
    plane[1].SetPoint2(porig[0], pdims[1]+porig[1],0.)
    
    plane[1].SetNormal(0.,0.,1.)
    plane[1].Push(-0.01)
    
    vmap[1].SetScalarRange(irng[0], irng[1])
    lookupGrayscale[1].SetTableRange(irng[0], irng[1])
    lookupColor[1].SetTableRange(irng[0], irng[1])
    
    ren[1].AddActor(actor[1])
    vis.renfun.render(ren)
    
    return
 
# -----------
# vis_imgShow
# -----------
def vis_imgShow(ren):
    try:
        actor = getattr(vis, 'vis_img_actor_'+ren[0])
    except:
        return
        
    ren[1].AddActor(actor[1])
    ren[1].ResetCamera()
    vis.renfun.render(ren)
    
    return
    

# -------------
# vis_imgUnshow
# -------------
def vis_imgUnshow(ren):
    try:
        actor = getattr(vis, "vis_img_actor_"+ren[0])
    except:
        return
        
    if (ren[1].GetActors().IsItemPresent(actor[1])>0):
        ren[1].RemoveActor(actor[1])
    vis.renfun.render(ren)
    return
    
        
    
# ---------
# vis_imgRm
# ---------
def vis_imgRm(ren):

    vis.img.vis_imgUnshow(ren)        
    delList = ["vis_img_texture_" +ren[0],"vis_img_plane_" + ren[0],"vis_img_tmap_" + 
    ren[0],"vis_img_cast_" + ren[0],"vis_img_map_" +ren[0],"vis_img_actor_" + ren[0],
    "vis_img_g8bitGrayscaleLUT_" + ren[0],"vis_img_gBlueToRedLUT_" + ren[0]]
    for i in delList:
        try:
            delattr(vis,i)
        except:
            pass
    return

    
    