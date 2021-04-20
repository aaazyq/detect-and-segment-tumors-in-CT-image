#-*-coding:utf-8-*-
import SimpleITK as sitk
import vtk
import matplotlib.pyplot as plt
import numpy as np

def draw_tumour(brain_path, tumour_points, brain_color, tumour_color):

    # get array of brain
    img = sitk.ReadImage(brain_path)
    dims = img.GetSize()
    spacing = img.GetSpacing()
    brain_data = sitk.GetArrayFromImage(img)

    # collect original values of tumour points
    values = []
    for i in tumour_points:
        values.append(brain_data[int(float(i[0]))][int(float(i[1]))][int(float(i[2]))])

    # get the distribution of brain point's values
    n1, bins1, patches1 = plt.hist(brain_data.flatten())
    plt.clf()
    n1 = list(n1)
    bins1 = list(bins1)
    max_index1 = n1.index(max(n1))
    # find out the right value of outline
    brain_isopleth = int((bins1[max_index1] + bins1[max_index1 + 1]) / 2)

    # get the distribution of tumour point's values
    n2, bins2, patches2 = plt.hist(values)
    plt.clf()
    n2 = list(n2)
    bins2 = list(bins2)
    max_index2 = n2.index(max(n2))
    # find out the right value of outline
    tumour_isopleth = int((bins2[max_index2] + bins2[max_index2 + 1]) / 2)

    # start VTK setting
    # set brain's actor
    brain_image = vtk.vtkImageData()
    brain_image.SetDimensions(dims[2], dims[1], dims[0])
    brain_image.SetSpacing(spacing[0], spacing[1], spacing[2])  # sampling distance
    brain_image.SetOrigin(0, 0, 0)  # origin

    if vtk.VTK_MAJOR_VERSION <= 5:
        brain_image.SetNumberOfScalarComponets(1)
        brain_image.SetScalarTypeToDouble()
    else:
        brain_image.AllocateScalars(vtk.VTK_DOUBLE, 1)

    for z in range(dims[0]):
        for y in range(dims[1]):
            for x in range(dims[2]):
                scalardata = brain_data[x][y][z]
                brain_image.SetScalarComponentFromDouble(x, y, z, 0, scalardata)

    # isosurface rendering (by marching cubes)
    Extractor = vtk.vtkMarchingCubes()
    Extractor.SetInputData(brain_image)
    Extractor.SetValue(0, brain_isopleth)

    # connect triangles
    stripper = vtk.vtkStripper()
    stripper.SetInputConnection(Extractor.GetOutputPort())

    # mapping geometric data into image data
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(stripper.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # set properties
    actor.GetProperty().SetColor(brain_color[0], brain_color[1], brain_color[2])
    actor.GetProperty().SetOpacity(brain_color[3])
    actor.GetProperty().SetAmbient(0.25)
    actor.GetProperty().SetDiffuse(0.6)
    actor.GetProperty().SetSpecular(1.0)

    # set tumour's actor
    Extractor2 = vtk.vtkMarchingCubes()
    Extractor2.SetInputData(brain_image)
    Extractor2.SetValue(0, tumour_isopleth)
    # Extractor.GenerateValues(1, 250, 300)

    # connect triangles
    stripper2 = vtk.vtkStripper()
    stripper2.SetInputConnection(Extractor2.GetOutputPort())

    # mapping geometric data into image data
    mapper2 = vtk.vtkPolyDataMapper()
    mapper2.SetInputConnection(stripper2.GetOutputPort())
    actor2 = vtk.vtkActor()
    actor2.SetMapper(mapper2)

    # set properties
    actor2.GetProperty().SetColor(tumour_color[0], tumour_color[1], tumour_color[2])
    actor2.GetProperty().SetOpacity(tumour_color[3])
    actor2.GetProperty().SetAmbient(0.25)
    actor2.GetProperty().SetDiffuse(0.6)
    actor2.GetProperty().SetSpecular(1.0)

    # add a camera
    # camera = vtk.vtkCamera()
    # camera.SetViewUp(0,0,-1)  # postion of view point
    # camera.SetPosition(0, 1, 0) # postion of camera
    # camera.SetFocalPoint(0, 0, 0)   # postion of focal point
    # camera.ComputeViewPlaneNormal() # auto
    # camera.Azimuth(30)
    # camera.Elevation(30)

    # scene setting
    ren = vtk.vtkRenderer()
    ren.SetBackground(0, 0, 0)  # background color
    ren.AddActor(actor)
    ren.AddActor(actor2)
    return ren
    # # ren.SetActiveCamera(camera)
    # renWin = vtk.vtkRenderWindow()
    # renWin.AddRenderer(ren)
    # renWin.SetSize(250, 250)
    # iren = vtk.vtkRenderWindowInteractor()  # connect with mouse
    #
    # iren.SetRenderWindow(renWin)
    # iren.Initialize()
    # renWin.Render()
    # iren.Start()