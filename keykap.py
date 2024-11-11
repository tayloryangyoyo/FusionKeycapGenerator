#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

# 取得 Fusion 360 的根應用程式物件
app = adsk.core.Application.get()
# 取得 Fusion 360 的使用者介面物件
if app:
    ui = app.userInterface

newComp = None

# 定義一個函數來建立新的元件
def createNewComponent() -> adsk.fusion.Component:
    # 取得目前的設計
    product = app.activeProduct
    # 取得設計的根元件
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent
    # 建立新的元件.事件.增加新的元件
    newOcc = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    # 回傳新的元件
    return newOcc.component

# 建立草圖的函數
def createSketch(comp: adsk.fusion.Component, plane: adsk.fusion.ConstructionPlane) -> adsk.fusion.Sketch:
    # 取得元件的所有草圖
    sketches = comp.sketches
    # 在指定的平面建立草圖
    sketch = sketches.add(plane)
    # 回傳建立的草圖
    return sketch

# 傳入草圖然後繪製矩形草圖的函數
def drawRectangleSketch(sketch: adsk.fusion.Sketch, width: float, height: float):
    '''在被傳入的草圖上繪製一個矩形'''
    # 取得草圖的線
    lines = sketch.sketchCurves.sketchLines
    # 繪製一個中心點矩形
    lines.addCenterPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(width / 2, height / 2, 0))
    return 

# 傳入草圖然後繪製圓形草圖的函數
def drawCircleSketch(sketch: adsk.fusion.Sketch, radius: float):
    '''在被傳入的草圖上繪製一個圓形'''
    circles = sketch.sketchCurves.sketchCircles
    circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius)
    return

# # 傳入圓形草圖並在圓形草圖上繪製一個小圓形的函數
# def drawCircleOnCircleSketch(sketch: adsk.fusion.Sketch, radius: float):
#     '''在圓形草圖上繪製一個小圓形'''
#     circles = sketch.sketchCurves.sketchCircles
#     circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, -3), radius)
#     circles.addByCenterRadius(circle1.centerSketchPoint, radius / 2)
#     return

# 製作立方體的函數
# def createBox(design: adsk.fusion.Design, sizeX: float, sizeY: float, sizeZ: float) -> adsk.fusion.BRepBody:
#     '''建立一個立方體'''
#     component = design.rootComponent
#     # 建立一個新的草圖
#     sketches = component.sketches
#     # 在 XY 平面建立草圖
#     sketch: adsk.fusion.Sketch = sketches.add(component.xYConstructionPlane)
#     # 取得草圖的線
#     lines = sketch.sketchCurves.sketchLines
#     # 繪製一個中心點矩形
#     recLines = lines.addCenterPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(sizeX / 2, sizeY / 2, 0))
#     # 取得矩形的外圍
#     prof = sketch.profiles.item(0)
#     # 取得拉伸特徵
#     extrudes = component.features.extrudeFeatures
#     # 拉伸的距離
#     distance = adsk.core.ValueInput.createByReal(sizeZ)
    
#     ext = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
#     return ext.bodies.item(0)

def run(context):
    try:
        # 建立新的元件
        component = createNewComponent()
        
        # 建立一個新的草圖
        sketch = createSketch(component, component.xYConstructionPlane)
        drawRectangleSketch(sketch, 1.7, 1.7)

        # 繪製圓形以及中間十字的草圖
        sketch2 = createSketch(component, component.xYConstructionPlane)
        drawCircleSketch(sketch2, 0.55/2)
        drawRectangleSketch(sketch2, 0.405, 0.125)
        drawRectangleSketch(sketch2, 0.125, 0.405)
        
        sketches = component.sketches
        
        # offset_plane_input = component.constructionPlanes.createInput()
        # offset_plane_input.setByOffset(component.xYConstructionPlane, adsk.core.ValueInput.createByReal(0.3))  # 偏移 0.3 cm
        # offset_plane = component.constructionPlanes.add(offset_plane_input)
        textSketch = sketches.add(component.xYConstructionPlane)
        
        # 在指定的平面建立草圖
        texts = textSketch.sketchTexts
        
        
        # 左上角的文字
        input = texts.createInput2('Q', 0.3)
        input.setAsMultiLine(adsk.core.Point3D.create(0, 0, 0),
                            adsk.core.Point3D.create(-0.7, 0.7, 0),
                            adsk.core.HorizontalAlignments.LeftHorizontalAlignment,
                            adsk.core.VerticalAlignments.TopVerticalAlignment, 0)
        # 右上角的文字
        input2 = texts.createInput2('Esc', 0.3)
        input2.setAsMultiLine(adsk.core.Point3D.create(0, 0, 0),
                            adsk.core.Point3D.create(0.7, 0.7, 0),
                            adsk.core.HorizontalAlignments.RightHorizontalAlignment,
                            adsk.core.VerticalAlignments.TopVerticalAlignment, 0)
        # 左下角的文字
        input3 = texts.createInput2('BT_01', 0.3)
        input3.setAsMultiLine(adsk.core.Point3D.create(0, 0, 0),
                            adsk.core.Point3D.create(-0.7, -0.7, 0),
                            adsk.core.HorizontalAlignments.LeftHorizontalAlignment,
                            adsk.core.VerticalAlignments.BottomVerticalAlignment, 0)
        # 右下角的文字
        input4 = texts.createInput2('', 0.3)
        input4.setAsMultiLine(adsk.core.Point3D.create(0, 0, 0),
                            adsk.core.Point3D.create(0.7, -0.7, 0),
                            adsk.core.HorizontalAlignments.RightHorizontalAlignment,
                            adsk.core.VerticalAlignments.BottomVerticalAlignment, 0)
        
        texts.add(input)
        texts.add(input2)
        texts.add(input3)
        texts.add(input4)


        # 取得拉伸功能
        extrudes: adsk.fusion.ExtrudeFeatures = component.features.extrudeFeatures
        
        # ----------矩形的拉伸----------
        # 拉伸矩形2mm
        recProfiles = sketch.profiles
        extInput = extrudes.createInput(recProfiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        recHeight = adsk.core.ValueInput.createByReal(0.2)
        extInput.setDistanceExtent(False, recHeight)
        ext = extrudes.add(extInput)

        # 為四方形的頂部邊緣添加圓角
        filletFeats = component.features.filletFeatures
        edges = adsk.core.ObjectCollection.create()

        # 獲取頂部的面
        topFace = ext.endFaces.item(0)

        # 將頂部面的四條邊加入圓角集合
        for edge in topFace.edges:
            edges.add(edge)
        
        # 遍歷立方體的所有邊，篩選出垂直邊
        for edge in ext.bodies.item(0).edges:
            # 垂直邊的方向與Z軸平行
            edgeDir = edge.startVertex.geometry.vectorTo(edge.endVertex.geometry)
            if abs(edgeDir.x) < 1e-5 and abs(edgeDir.y) < 1e-5:  # 垂直於Z軸
                edges.add(edge)

        # 設定圓角半徑
        filletRadius = adsk.core.ValueInput.createByReal(0.1)
        # 創建垂直邊的圓角特徵
        if edges.count > 0:
            filletInput = filletFeats.createInput()
            filletInput.addConstantRadiusEdgeSet(edges, filletRadius, True)
            filletFeats.add(filletInput)
            
        # ----------文字的拉伸----------
        # text_profiles = adsk.core.ObjectCollection.create()
        # for prof in textSketch.profiles:
        #     text_profiles.add(prof)
        # textInput = extrudes.createInput(text_profiles.item(0), adsk.fusion.FeatureOperations.JoinFeatureOperation)
        # textDeepHeight = adsk.core.ValueInput.createByReal(-0.3)
        # textInput.setDistanceExtent(False, textDeepHeight)
        # textInput.setByOffset(component.xYConstructionPlane, adsk.core.ValueInput.createByReal(0.3))
        
        # ext = extrudes.add(textInput)

        # ----------圓形的拉伸----------
        # 拉伸圓形外圍3mm
        circle_profiles= sketch2.profiles
        extInput2 = extrudes.createInput(circle_profiles.item(0), adsk.fusion.FeatureOperations.JoinFeatureOperation)
        circleHeight = adsk.core.ValueInput.createByReal(-0.3)
        extInput2.setDistanceExtent(False, circleHeight)
        ext = extrudes.add(extInput2)
        
        # 顯示參數的表達式
        ui.messageBox("DONE Git")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
