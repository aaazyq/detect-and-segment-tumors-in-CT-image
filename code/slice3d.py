# -*-coding:utf-8-*-
import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np
import vtk

def slice_3d(path, S_low=0, S_up=0, A_low=0, A_up=0, C_low=0, C_up=0, color=[1, 1, 0, 0.6]):
    # 读脑子的数据
    img = sitk.ReadImage(path)
    dims = img.GetSize()
    spacing = img.GetSpacing()
    brain_data = sitk.GetArrayFromImage(img)

    # 规避错误
    if (int(float(S_low)) >= int(float(S_up))) or (int(float(S_low)) < 0) or (int(float(S_up)) > dims[0]):
        S_low = 0
        S_up = dims[0]
    else:
        S_low = int(float(S_low))
        S_up = int(float(S_up))

    # 如果S动过，则A不动
    if S_low != 0 or S_up != dims[0]:
        A_low = 0
        A_up = dims[1]
    elif (int(float(A_low)) >= int(float(A_up))) or (int(float(A_low)) < 0) or (int(float(A_up)) > dims[0]):
        A_low = 0
        A_up = dims[1]
    else:
        A_low = int(float(A_low))
        A_up = int(float(A_up))

    # 如果S和A任一被动过，则C不能再动
    if  (S_low != 0 or S_up != dims[0]) or (A_low != 0 or A_up != dims[1]):
        C_low = 0
        C_up = dims[2]
    elif (int(float(C_low)) >= int(float(C_up))) or (int(float(C_low)) < 0) or (int(float(C_up)) > dims[0]):
        C_low = 0
        C_up = dims[2]
    else:
        C_low = int(float(C_low))
        C_up = int(float(C_up))
    # print(S_low,S_up,A_low,A_up,C_low,C_up)

    # 找到脑子的点的分布
    n1, bins1, patches1 = plt.hist(brain_data[S_low:S_up][A_low:A_up][C_low:C_up].flatten())
    # print (brain_data[S_low:S_up][A_low:A_up][C_low:C_up].flatten())
    plt.clf()
    n1 = list(n1)
    bins1 = list(bins1)
    max_index = n1.index(max(n1))
    # 找到要画的等值线
    brain_isopleth = int((bins1[max_index] + bins1[max_index + 1]) / 2)
    # print (brain_isopleth)

    # 开始VTK设置
    image = vtk.vtkImageData()
    image.SetDimensions(dims[2], dims[1], dims[0])  # 设置维度
    image.SetSpacing(spacing[0], spacing[1], spacing[2])  # 设置X、Y、Z三个方向上的采样间距（每两个点在真实世界中的间距
    image.SetOrigin(0, 0, 0)  # 设置原点

    if vtk.VTK_MAJOR_VERSION <= 5:
        image.SetNumberOfScalarComponets(1)
        image.SetScalarTypeToDouble()
    else:
        image.AllocateScalars(vtk.VTK_DOUBLE, 1)

    # 录入数据
    for z in range(S_low, S_up):  # dims[0]
        for y in range(A_low, A_up):  # dims[1]
            for x in range(C_low, C_up):  # dims[2]
                scalardata = brain_data[x][y][z]
                image.SetScalarComponentFromDouble(x, y, z, 0, scalardata)

    Extractor = vtk.vtkMarchingCubes()
    Extractor.SetInputData(image)
    Extractor.SetValue(0, brain_isopleth)

    stripper = vtk.vtkStripper()
    stripper.SetInputConnection(Extractor.GetOutputPort())
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(stripper.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    actor.GetProperty().SetColor(color[0], color[1], color[2])
    actor.GetProperty().SetOpacity(color[3])
    actor.GetProperty().SetAmbient(0.25)
    actor.GetProperty().SetDiffuse(0.6)
    actor.GetProperty().SetSpecular(1.0)

    ren = vtk.vtkRenderer()
    ren.SetBackground(0, 0, 0)
    ren.AddActor(actor)
    return ren
    # renWin = vtk.vtkRenderWindow()
    #
    # renWin.AddRenderer(ren)
    # renWin.SetSize(250, 250)
    # iren = vtk.vtkRenderWindowInteractor()
    #
    # iren.SetRenderWindow(renWin)
    # iren.Initialize()
    # renWin.Render()
    # iren.Start()