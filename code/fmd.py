import SimpleITK as sitk
from skimage import io,transform
import vtk

def show_3D_simpleITK(path):
    img1 = sitk.ReadImage(path)
    dims = img1.GetSize()
    spacing = img1.GetSpacing()
    img1_data = sitk.GetArrayFromImage(img1)

    image = vtk.vtkImageData()
    image.SetDimensions(dims[2],dims[1],dims[0])
    image.SetSpacing(spacing[0],spacing[1],spacing[2])
    image.SetOrigin(0,0,0)

    if vtk.VTK_MAJOR_VERSION <= 5:
        image.SetNumberOfScalarComponets(1)
        image.SetScalarTypeToDouble()
    else:
        image.AllocateScalars(vtk.VTK_DOUBLE,1)

    for z in range(dims[0]):
        for y in range(dims[1]):
            for x in range(dims[2]):
                scalardata = img1_data[x][y][z]
                image.SetScalarComponentFromDouble(x,y,z,0,scalardata)

    Extractor = vtk.vtkMarchingCubes()
    Extractor.SetInputData(image)
    Extractor.SetValue(0,150)
    stripper = vtk.vtkStripper()
    stripper.SetInputConnection(Extractor.GetOutputPort())
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(stripper.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    actor.GetProperty().SetColor(1,1,0)
    actor.GetProperty().SetOpacity(0.9)
    actor.GetProperty().SetAmbient(0.25)
    actor.GetProperty().SetDiffuse(0.6)
    actor.GetProperty().SetSpecular(1.0)

    ren = vtk.vtkRenderer()
    ren.SetBackground(0,0,0)
    ren.AddActor(actor)
    return ren
    # renWin = vtk.vtkRenderWindow()
    #
    # renWin.AddRenderer(ren)
    # renWin.SetSize(250,250)
    # iren = vtk.vtkRenderWindowInteractor()
    #
    # iren.SetRenderWindow(renWin)
    # iren.Initialize()
    # renWin.Render()
    # iren.Start()
