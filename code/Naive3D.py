#-*-coding:utf-8-*-
import SimpleITK as sitk
import random
import vtk
import matplotlib.pyplot as plt

def show_brain_tumour_rough(path,colorlist1 = [round(random.random(),3),round(random.random(),3),round(random.random(),3),0.2],colorlist2 = [round(random.random(),3),round(random.random(),3),round(random.random(),3),0.2],colorlist3 = [round(random.random(),3),round(random.random(),3),round(random.random(),3),0.5]):
    img = sitk.ReadImage(path)
    dims = img.GetSize()
    spacing = img.GetSpacing()
    brain_data = sitk.GetArrayFromImage(img)

    image = vtk.vtkImageData()
    image.SetDimensions(dims[2],dims[1],dims[0]) # 设置维度
    image.SetSpacing(spacing[0],spacing[1],spacing[2]) # 设置X、Y、Z三个方向上的采样间距（每两个点在真实世界中的间距
    image.SetOrigin(0,0,0) # 设置原点

    if vtk.VTK_MAJOR_VERSION <= 5:
        image.SetNumberOfScalarComponets(1)
        image.SetScalarTypeToDouble()
    else:
        image.AllocateScalars(vtk.VTK_DOUBLE,1)

    # 找到脑子的点的分布
    n1, bins1, patches1 = plt.hist(brain_data.flatten())
    plt.clf()
    n1 = list(n1)
    n1_sort = sorted(n1,reverse = True)
    bins1 = list(bins1)
    max_index1 = n1.index(n1_sort[0])
    max_index2 = n1.index(n1_sort[1])
    max_index3 = n1.index(n1_sort[2])
    # 找到要画的等值线
    brain_isopleth1 = int((bins1[max_index1] + bins1[max_index1 + 1]) / 2)
    brain_isopleth2 = int((bins1[max_index2] + bins1[max_index2 + 1]) / 2)
    brain_isopleth3 = int((bins1[max_index3] + bins1[max_index3 + 1]) / 2)
    print (brain_isopleth3,brain_isopleth2,brain_isopleth1)

    for z in range(dims[0]):
        for y in range(dims[1]):
            for x in range(dims[2]):
                scalardata = brain_data[x][y][z]
                image.SetScalarComponentFromDouble(x,y,z,0,scalardata)

    # 用marching cubes算法 进行面绘制
    Extractor = vtk.vtkMarchingCubes()
    Extractor.SetInputData(image)
    Extractor.SetValue(0,brain_isopleth1)

    # 链接三角形
    stripper = vtk.vtkStripper()
    stripper.SetInputConnection(Extractor.GetOutputPort())

    # 建立mapper，将几何数据映射成图像数据
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(stripper.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # property设置（材质、颜色、光线）
    actor.GetProperty().SetColor(colorlist1[0],colorlist1[1],colorlist1[2])
    actor.GetProperty().SetOpacity(colorlist1[3])
    actor.GetProperty().SetAmbient(0.25)
    actor.GetProperty().SetDiffuse(0.6)
    actor.GetProperty().SetSpecular(1.0)

    # 添加一个相机
    # camera = vtk.vtkCamera()
    # camera.SetViewUp(0,0,-1)  # 视角位置
    # camera.SetPosition(0, 1, 0) # 相机位置
    # camera.SetFocalPoint(0, 0, 0)   # 焦点
    # camera.ComputeViewPlaneNormal() # 自动
    # camera.Azimuth(30)
    # camera.Elevation(30)
    # 用marching cubes算法 进行面绘制
    Extractor2 = vtk.vtkMarchingCubes()
    Extractor2.SetInputData(image)
    Extractor2.SetValue(0, brain_isopleth2)

    # 链接三角形
    stripper2 = vtk.vtkStripper()
    stripper2.SetInputConnection(Extractor2.GetOutputPort())

    # 建立mapper，将几何数据映射成图像数据
    mapper2 = vtk.vtkPolyDataMapper()
    mapper2.SetInputConnection(stripper2.GetOutputPort())
    actor2 = vtk.vtkActor()
    actor2.SetMapper(mapper2)

    # property设置（材质、颜色、光线）
    actor2.GetProperty().SetColor(colorlist2[0],colorlist2[1],colorlist2[2])
    actor2.GetProperty().SetOpacity(colorlist2[3])
    actor2.GetProperty().SetAmbient(0.25)
    actor2.GetProperty().SetDiffuse(0.6)
    actor2.GetProperty().SetSpecular(1.0)

    # 用marching cubes算法 进行面绘制
    Extractor3 = vtk.vtkMarchingCubes()
    Extractor3.SetInputData(image)
    Extractor3.SetValue(0, brain_isopleth3)

    # 链接三角形
    stripper3 = vtk.vtkStripper()
    stripper3.SetInputConnection(Extractor3.GetOutputPort())

    # 建立mapper，将几何数据映射成图像数据
    mapper3 = vtk.vtkPolyDataMapper()
    mapper3.SetInputConnection(stripper3.GetOutputPort())
    actor3 = vtk.vtkActor()
    actor3.SetMapper(mapper3)

    # property设置（材质、颜色、光线）
    actor3.GetProperty().SetColor(colorlist3[0],colorlist3[1],colorlist3[2])
    actor3.GetProperty().SetOpacity(colorlist3[3])
    actor3.GetProperty().SetAmbient(0.25)
    actor3.GetProperty().SetDiffuse(0.6)
    actor3.GetProperty().SetSpecular(1.0)



    # 场景设置
    ren = vtk.vtkRenderer()
    ren.SetBackground(0,0,0)    # 设置背景颜色
    ren.AddActor(actor) # 增加actor
    ren.AddActor(actor2)
    ren.AddActor(actor3)
    return ren
    # ren.AddActor(cubeActor)
    # ren.SetActiveCamera(camera)
    # renWin = vtk.vtkRenderWindow()
    #
    # # 窗口设置
    # renWin.AddRenderer(ren)
    # renWin.SetSize(250,250)
    # iren = vtk.vtkRenderWindowInteractor() # 关联事件（鼠标）
    #
    # iren.SetRenderWindow(renWin)
    # iren.Initialize()
    # renWin.Render()
    # iren.Start()

def show_3D_brain(path,colorlist = [round(random.random(),3),round(random.random(),3),round(random.random(),3),0.2]):
    img = sitk.ReadImage(path)
    dims = img.GetSize()
    spacing = img.GetSpacing()
    brain_data = sitk.GetArrayFromImage(img)

    image = vtk.vtkImageData()
    image.SetDimensions(dims[2],dims[1],dims[0]) # 设置维度
    image.SetSpacing(spacing[0],spacing[1],spacing[2]) # 设置X、Y、Z三个方向上的采样间距（每两个点在真实世界中的间距
    image.SetOrigin(0,0,0) # 设置原点

    if vtk.VTK_MAJOR_VERSION <= 5:
        image.SetNumberOfScalarComponets(1)
        image.SetScalarTypeToDouble()
    else:
        image.AllocateScalars(vtk.VTK_DOUBLE,1)

    # 找到脑子的点的分布
    n1, bins1, patches1 = plt.hist(brain_data.flatten())
    plt.clf()
    n1 = list(n1)
    bins1 = list(bins1)
    max_index1 = n1.index(max(n1))
    # 找到要画的等值线
    brain_isopleth = int((bins1[max_index1] + bins1[max_index1 + 1]) / 2)

    for z in range(dims[0]):
        for y in range(dims[1]):
            for x in range(dims[2]):
                scalardata = brain_data[x][y][z]
                image.SetScalarComponentFromDouble(x,y,z,0,scalardata)

    # 用marching cubes算法 进行面绘制
    Extractor = vtk.vtkMarchingCubes()
    Extractor.SetInputData(image)
    Extractor.SetValue(0,brain_isopleth)

    # 链接三角形
    stripper = vtk.vtkStripper()
    stripper.SetInputConnection(Extractor.GetOutputPort())

    # 建立mapper，将几何数据映射成图像数据
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(stripper.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # property设置（材质、颜色、光线）
    actor.GetProperty().SetColor(colorlist[0],colorlist[1],colorlist[2])
    actor.GetProperty().SetOpacity(colorlist[3])
    actor.GetProperty().SetAmbient(0.25)
    actor.GetProperty().SetDiffuse(0.6)
    actor.GetProperty().SetSpecular(1.0)

    # 场景设置
    ren = vtk.vtkRenderer()
    ren.SetBackground(0,0,0)    # 设置背景颜色
    ren.AddActor(actor) # 增加actor
    return ren
    # ren.AddActor(cubeActor)
    # ren.SetActiveCamera(camera)
    # renWin = vtk.vtkRenderWindow()
    #
    # # 窗口设置
    # renWin.AddRenderer(ren)
    # renWin.SetSize(250,250)
    # iren = vtk.vtkRenderWindowInteractor() # 关联事件（鼠标）
    #
    # iren.SetRenderWindow(renWin)
    # iren.Initialize()
    # renWin.Render()
    # iren.Start()

print(show_3D_brain('BRATS_HG0015_FLAIR.mha'))
#show_brain_tumour_rough('BRATS_HG0015_FLAIR.mha')