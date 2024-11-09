#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

# 存放所有的命令處理程序
handlers = []
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
    # 建立新的元件
    allOccs = rootComp.occurrences
    newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
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

# # 建立XY草圖的函數
# def createXYSketch(comp: adsk.fusion.Component) -> adsk.fusion.Sketch:
#     # 取得元件的所有草圖
#     sketches = comp.sketches
#     # 建立XY平面
#     xyPlane = comp.xYConstructionPlane
#     # 在指定的平面建立草圖
#     sketch = sketches.add(xyPlane)
#     # 回傳建立的草圖
#     return sketch

# # 建立線的函數
# def createSketchLines(sketch: adsk.fusion.Sketch):
#     lines = sketch.sketchCurves.sketchLines;
#     line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(3, 1, 0))
#     line2 = lines.addByTwoPoints(adsk.core.Point3D.create(4, 3, 0), adsk.core.Point3D.create(2, 4, 0))
#     line3 = lines.addByTwoPoints(adsk.core.Point3D.create(-1, 0, 0), adsk.core.Point3D.create(0, 4, 0))
#     return

# 傳入草圖然後繪製矩形草圖的函數
def drawRectangleSketch(sketch: adsk.fusion.Sketch, width: float, height: float):
    '''繪製一個矩形草圖'''
    # 取得草圖的線
    lines = sketch.sketchCurves.sketchLines
    # 繪製一個中心點矩形
    lines.addCenterPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(width / 2, height / 2, 0))
    return 

# 傳入草圖然後繪製圓形草圖的函數
def drawCircleSketch(sketch: adsk.fusion.Sketch, radius: float):
    '''繪製一個圓形草圖'''
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

# # 傳入草圖然後增加文字的函數
# def addTextToSketch(sketch: adsk.fusion.Sketch, text: str):
#     '''在草圖上增加文字'''
#     # 取得草圖的文字
#     texts = sketch.sketchTexts
#     # 增加文字
#     text = texts.add(text, adsk.core.Point3D.create(0, 0, 0), sketch.sketchCurves.sketchLines.item(0))
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

# 製作圓形的函數
def createCircle(design: adsk.fusion.Design, radius: float) -> adsk.fusion.BRepBody:
    '''建立一個圓形'''
    component = design.rootComponent
    # 建立一個新的草圖
    sketches = component.sketches
    # 在 XY 平面建立草圖
    sketch: adsk.fusion.Sketch = sketches.add(component.xYConstructionPlane)
    # 取得草圖的線
    lines = sketch.sketchCurves.sketchLines
    # 繪製一個圓形
    circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius)
    # 取得圓形的外圍
    prof = sketch.profiles.item(0)
    # 取得拉伸特徵
    extrudes = component.features.extrudeFeatures
    # 拉伸的距離
    distance = adsk.core.ValueInput.createByReal(1)
    
    ext = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    return ext.bodies.item(0)

def run(context):
    try:
        # 建立新的元件
        squareComp = createNewComponent()
        
        # 建立一個新的草圖
        sketch = createSketch(squareComp, squareComp.xYConstructionPlane)
        drawRectangleSketch(sketch, 17, 17)

        # 繪製一個圓形草圖
        sketch2 = createSketch(squareComp, squareComp.xYConstructionPlane)
        drawCircleSketch(sketch2, 5.5/2)
        drawRectangleSketch(sketch2, 4.05, 1.25)
        drawRectangleSketch(sketch2, 1.25, 4.05)

        # 取得拉伸功能
        extrudes = squareComp.features.extrudeFeatures
        
        # 拉伸矩形2mm
        recProfiles = sketch.profiles
        extInput = extrudes.createInput(recProfiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        recHeight = adsk.core.ValueInput.createByReal(2)
        extInput.setDistanceExtent(False, recHeight)
        ext = extrudes.add(extInput)

        # 拉伸圓形3mm
        circle_profiles= sketch2.profiles
        extInput2 = extrudes.createInput(circle_profiles.item(0), adsk.fusion.FeatureOperations.JoinFeatureOperation)
        circleHeight = adsk.core.ValueInput.createByReal(-3)
        extInput2.setDistanceExtent(False, circleHeight)
        ext = extrudes.add(extInput2)
        
        # 顯示參數的表達式
        ui.messageBox("DONE")

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
