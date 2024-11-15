import sys
import os

sys.path.append(os.path.dirname(__file__))

import adsk.core, adsk.fusion, adsk.cam, traceback
from keyArray import keyArrayList

# 取得 Fusion 360 的根應用程式物件
app = adsk.core.Application.get()
# 取得 Fusion 360 的使用者介面物件
if app:
    ui = app.userInterface

newComp = None

# 全域變數
TEXT_ONE_SIZE = 0.4
TEXT_TWO_SIZE = 0.3
TEXT_THREE_SIZE = 0.2
TEXT_FOUR_SIZE = 0.2

TEXT_DEEP = -0.02
KEY_CAP_TOP_HEIGHT = 0.2
KEY_CAP_TOP_WIDTH = 1.7
KEY_CAP_TOP_DEPTH = 1.7
KEY_CAP_BUTTOM_HEIGHT = -0.3

R_TEXT_DEEP = adsk.core.ValueInput.createByReal(TEXT_DEEP)
R_KEY_CAP_TOP_HEIGHT = adsk.core.ValueInput.createByReal(KEY_CAP_TOP_HEIGHT)
R_KEY_CAP_TOP_WIDTH = adsk.core.ValueInput.createByReal(KEY_CAP_TOP_WIDTH)
R_KEY_CAP_TOP_DEPTH = adsk.core.ValueInput.createByReal(KEY_CAP_TOP_DEPTH)
R_KEY_CAP_BUTTOM_HEIGHT = adsk.core.ValueInput.createByReal(KEY_CAP_BUTTOM_HEIGHT)


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
def createSketch(
    comp: adsk.fusion.Component, plane: adsk.fusion.ConstructionPlane
) -> adsk.fusion.Sketch:
    # 取得元件的所有草圖
    sketches = comp.sketches
    # 在指定的平面建立草圖
    sketch = sketches.add(plane)
    # 回傳建立的草圖
    return sketch


# 傳入草圖然後繪製矩形草圖的函數
def drawRectangleSketch(sketch: adsk.fusion.Sketch, width: float, height: float):
    """在被傳入的草圖上繪製一個矩形"""
    # 取得草圖的線
    lines = sketch.sketchCurves.sketchLines
    # 繪製一個中心點矩形
    lines.addCenterPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(width / 2, height / 2, 0),
    )
    return


# 傳入草圖然後繪製圓形草圖的函數
def drawCircleSketch(sketch: adsk.fusion.Sketch, radius: float):
    """在被傳入的草圖上繪製一個圓形"""
    circles = sketch.sketchCurves.sketchCircles
    circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius)
    return


# 傳入草圖然後繪製文字草圖的函數
def drawTextSketch(
    sketch: adsk.fusion.Sketch,
    text: str,
    corner1: adsk.core.Base,
    corner2: adsk.core.Base,
):
    """在被傳入的草圖上繪製文字"""
    # 在指定的平面建立草圖
    texts = sketch.sketchTexts
    # 左上角的文字
    input = texts.createInput2(text, 0.4)
    input.setAsMultiLine(
        corner1,
        corner2,
        adsk.core.HorizontalAlignments.LeftHorizontalAlignment,
        adsk.core.VerticalAlignments.TopVerticalAlignment,
        0,
    )

    return texts.add(input)


def run(context):
    try:
        # 迴圈
        for keyIndex in range(len(keyArrayList)):
            # 建立新的元件
            component = createNewComponent()
            component.name = "Key" + str(keyIndex)
            # 取得拉伸功能
            extrudes: adsk.fusion.ExtrudeFeatures = component.features.extrudeFeatures
            # 取得圓角功能
            filletFeats = component.features.filletFeatures
            # ----------建立矩形並且拉伸----------
            keyText = keyArrayList[keyIndex]
            # 建立一個新的草圖
            rectSketch = createSketch(component, component.xYConstructionPlane)
            # 繪製一個矩形
            drawRectangleSketch(rectSketch, 1.7, 1.7)
            # 拉伸矩形2mm
            recProfiles = rectSketch.profiles
            extInput = extrudes.createInput(
                recProfiles.item(0),
                adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
            )
            extInput.setDistanceExtent(False, R_KEY_CAP_TOP_HEIGHT)
            extInput.isSolid = True
            ext = extrudes.add(extInput)

            # 為四方形的頂部邊緣添加圓角
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

            # ----------建立圓形和十字凹槽並且拉伸----------
            # 繪製圓形以及中間十字的草圖
            circleSketch = createSketch(component, component.xYConstructionPlane)
            drawCircleSketch(circleSketch, 0.55 / 2)
            drawRectangleSketch(circleSketch, 0.405, 0.125)
            drawRectangleSketch(circleSketch, 0.125, 0.405)

            # 拉伸圓形外圍3mm
            circle_profiles = circleSketch.profiles
            extInput2 = extrudes.createInput(
                circle_profiles.item(0),
                adsk.fusion.FeatureOperations.JoinFeatureOperation,
            )

            extInput2.setDistanceExtent(False, R_KEY_CAP_BUTTOM_HEIGHT)
            extInput2.isSolid = True
            ext = extrudes.add(extInput2)

            # ----------建立文字並且切割----------
            # CenterHorizontalAlignment	1	Aligned along the center.
            # LeftHorizontalAlignment	0	Aligned to the left.
            # RightHorizontalAlignment	2	Aligned to the right.

            # BottomVerticalAlignment	2	Aligned to the bottom.
            # MiddleVerticalAlignment	1	Aligned along the middle.
            # TopVerticalAlignment		0	Aligned to the top.
            # --左上角--
            textSketch = createSketch(component, component.xYConstructionPlane)
            sketchText = drawTextSketch(
                textSketch,
                keyText[0],
                adsk.core.Point3D.create(0, 0, 0),
                adsk.core.Point3D.create(-0.7, 0.7, 0),
            )

            # 拉伸文字
            extTextInput = extrudes.createInput(
                sketchText, adsk.fusion.FeatureOperations.CutFeatureOperation
            )
            # 設置從 3mm 的 Z 軸偏移開始向下拉伸
            extTextInput.startExtent = adsk.fusion.OffsetStartDefinition.create(
                R_KEY_CAP_TOP_HEIGHT
            )
            # 設置拉伸距離 -0.2mm（向下）
            extTextInput.setDistanceExtent(False, R_TEXT_DEEP)
            extTextInput.isSolid = True
            ext = extrudes.add(extTextInput)

            # --右上角--
            if keyText[1] != "":
                textSketch2 = createSketch(component, component.xYConstructionPlane)
                # 在指定的平面建立草圖
                sketchText2 = textSketch2.sketchTexts
                # 左上角的文字
                textInput2 = sketchText2.createInput2(keyText[1], 0.3)
                textInput2.setAsMultiLine(
                    adsk.core.Point3D.create(0, 0, 0),
                    adsk.core.Point3D.create(0.7, 0.7, 0),
                    adsk.core.HorizontalAlignments.RightHorizontalAlignment,
                    adsk.core.VerticalAlignments.TopVerticalAlignment,
                    0,
                )
                extText2 = sketchText2.add(textInput2)
                # 拉伸文字
                extTextInput2 = extrudes.createInput(
                    extText2, adsk.fusion.FeatureOperations.CutFeatureOperation
                )
                # 設置從 3mm 的 Z 軸偏移開始向下拉伸
                extTextInput2.startExtent = adsk.fusion.OffsetStartDefinition.create(
                    R_KEY_CAP_TOP_HEIGHT
                )
                # 設置拉伸距離 -0.2mm（向下）
                extTextInput2.setDistanceExtent(False, R_TEXT_DEEP)
                extTextInput2.isSolid = True
                ext = extrudes.add(extTextInput2)

            # --左下角--
            if keyText[2] != "":
                textSketch3 = createSketch(component, component.xYConstructionPlane)
                # 在指定的平面建立草圖
                sketchText3 = textSketch3.sketchTexts
                # 左上角的文字
                textInput3 = sketchText3.createInput2(keyText[2], 0.2)
                textInput3.setAsMultiLine(
                    adsk.core.Point3D.create(0, 0, 0),
                    adsk.core.Point3D.create(-0.7, -0.7, 0),
                    adsk.core.HorizontalAlignments.LeftHorizontalAlignment,
                    adsk.core.VerticalAlignments.BottomVerticalAlignment,
                    0,
                )
                extText3 = sketchText3.add(textInput3)
                # 拉伸文字
                extTextInput3 = extrudes.createInput(
                    extText3, adsk.fusion.FeatureOperations.CutFeatureOperation
                )
                # 設置從 3mm 的 Z 軸偏移開始向下拉伸
                extTextInput3.startExtent = adsk.fusion.OffsetStartDefinition.create(
                    R_KEY_CAP_TOP_HEIGHT
                )
                # 設置拉伸距離 -0.2mm（向下）
                extTextInput3.setDistanceExtent(False, R_TEXT_DEEP)
                extTextInput3.isSolid = True
                ext = extrudes.add(extTextInput3)

            # --右下角--
            if keyText[3] != "":
                textSketch4 = createSketch(component, component.xYConstructionPlane)
                # 在指定的平面建立草圖
                sketchText4 = textSketch4.sketchTexts
                # 左上角的文字
                textInput4 = sketchText4.createInput2(keyText[3], 0.2)
                textInput4.setAsMultiLine(
                    adsk.core.Point3D.create(0, 0, 0),
                    adsk.core.Point3D.create(0.7, -0.7, 0),
                    adsk.core.HorizontalAlignments.RightHorizontalAlignment,
                    adsk.core.VerticalAlignments.BottomVerticalAlignment,
                    0,
                )
                extText4 = sketchText4.add(textInput4)
                # 拉伸文字
                extTextInput4 = extrudes.createInput(
                    extText4, adsk.fusion.FeatureOperations.CutFeatureOperation
                )
                # 設置從 3mm 的 Z 軸偏移開始向下拉伸
                extTextInput4.startExtent = adsk.fusion.OffsetStartDefinition.create(
                    R_KEY_CAP_TOP_HEIGHT
                )
                # 設置拉伸距離 -0.2mm（向下）
                extTextInput4.setDistanceExtent(False, R_TEXT_DEEP)
                extTextInput4.isSolid = True
                ext = extrudes.add(extTextInput4)

            # 將所有物件向右移動
            moveFeats = component.features.moveFeatures
            allBodies = adsk.core.ObjectCollection.create()
            for body in component.bRepBodies:
                allBodies.add(body)

            # 創建移動矩陣，沿 X 軸移動
            transform = adsk.core.Matrix3D.create()
            transform.translation = adsk.core.Vector3D.create(
                (keyIndex + 1) * 1.9, 0, 0
            )

            # 使用 Matrix3D 移動物件
            moveInput = moveFeats.createInput(allBodies, transform)
            moveFeats.add(moveInput)

        # 顯示參數的表達式
        ui.messageBox("DONE Git")

    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
