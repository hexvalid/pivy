#!/usr/bin/env python

###
# Copyright (c) 2002, Tamer Fahmy <tamer@tammura.at>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#   * Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

###
# This is an example from the Inventor Mentor Programming Guide,
# chapter 8, example 4.
#
# This example creates and displays a Bezier Surface
# with trim curves.  The surface is identical to the
# surface in example 08.3.BezSurf.  The SoNurbsProfile
# class is used to define the trims.
# 
# One trim curve makes a counter-clockwise square around
# the whole surface.  Two other trim curves are combined
# end to end to cut a hole from the surface.  The outside
# trim curve and the first inside trim curve are both
# order 2 curves and are therefore sets of straight lines
# in parameter space.  The second inside curve is a
# Bezier curve.
#

from sogui import *
from pivy import *
import sys

floorData = """#Inventor V2.0 ascii\n
Separator {\n
   SpotLight {\n
      cutOffAngle 0.9\n
      dropOffRate 0.2\n 
      location 6 12 2\n 
      direction 0 -1 0\n
   }\n
   ShapeHints {\n
      faceType UNKNOWN_FACE_TYPE\n
   }\n
   Texture2Transform {\n
      #rotation 1.57\n
      scaleFactor 8 8\n
   }\n
   Texture2 {\n
      filename oak.rgb\n
   }\n
   NormalBinding {\n
        value  PER_PART\n
   }\n
   Material { diffuseColor 1 1 1 specularColor 1 1 1 shininess 0.4 }\n
   DEF FloorPanel Separator {\n
      DEF FloorStrip Separator {\n
         DEF FloorBoard Separator {\n
            Normal { vector 0 1 0 }\n
            TextureCoordinate2 {\n
               point [ 0 0, 0.5 0, 0.5 2, 0.5 4, 0.5 6,\n
                       0.5 8, 0 8, 0 6, 0 4, 0 2 ] }\n
            Coordinate3 {\n
               point [ 0 0 0, .5 0 0, .5 0 -2, .5 0 -4, .5 0 -6,\n
                       .5 0 -8, 0 0 -8, 0 0 -6, 0 0 -4, 0 0 -2, ]\n
            }\n
            FaceSet { numVertices 10 }\n
            BaseColor { rgb 0.3 0.1 0.0 }\n
            Translation { translation 0.125 0 -0.333 }\n
            Cylinder { parts TOP radius 0.04167 height 0.002 }\n
            Translation { translation 0.25 0 0 }\n
            Cylinder { parts TOP radius 0.04167 height 0.002 }\n
            Translation { translation 0 0 -7.333 }\n
            Cylinder { parts TOP radius 0.04167 height 0.002 }\n
            Translation { translation -0.25 0 0 }\n
            Cylinder { parts TOP radius 0.04167 height 0.002 }\n
         }\n
         Translation { translation 0 0 8.03 }\n
         USE FloorBoard\n
         Translation { translation 0 0 8.04 }\n
         USE FloorBoard\n
      }\n
      Translation { translation 0.53 0 -0.87 }\n
      USE FloorStrip\n
      Translation { translation 0.53 0 -2.3 }\n
      USE FloorStrip\n
      Translation { translation 0.53 0 1.3 }\n
      USE FloorStrip\n
      Translation { translation 0.53 0 1.1 }\n
      USE FloorStrip\n
      Translation { translation 0.53 0 -0.87 }\n
      USE FloorStrip\n
      Translation { translation 0.53 0 1.7 }\n
      USE FloorStrip\n
      Translation { translation 0.53 0 -0.5 }\n
      USE FloorStrip\n
   }\n
   Translation { translation 4.24 0 0 }\n
   USE FloorPanel\n
   Translation { translation 4.24 0 0 }\n
   USE FloorPanel\n
}"""

############################################################
# CODE FOR The Inventor Mentor STARTS HERE

# The array of trim coordinates
tpts = (
   (0.0, 0.0),
   (1.0, 0.0),
   (1.0, 1.0),
   (0.0, 1.0),
   (0.2, 0.2),
   (0.2, 0.7),
   (0.9, 0.7),
   (0.9, 0.2),
   (0.7, 0.0),
   (0.4, 0.8))

# The 16 coordinates defining the Bezier surface. 
pts = (
   (-4.5, -2.0,  8.0),
   (-2.0,  1.0,  8.0),
   ( 2.0, -3.0,  6.0),
   ( 5.0, -1.0,  8.0),
   (-3.0,  3.0,  4.0),
   ( 0.0, -1.0,  4.0),
   ( 1.0, -1.0,  4.0),
   ( 3.0,  2.0,  4.0),
   (-5.0, -2.0, -2.0),
   (-2.0, -4.0, -2.0),
   ( 2.0, -1.0, -2.0),
   ( 5.0,  0.0, -2.0),
   (-4.5,  2.0, -6.0),
   (-2.0, -4.0, -5.0),
   ( 2.0,  3.0, -5.0),
   ( 4.5, -2.0, -6.0))

# The 3 knot vectors for the 3 trim curves.
tknots1 = (0, 0, 1, 2, 3, 4, 4)
tknots2 = (0, 0, 1, 2, 3, 3)
tknots3 = (0, 0, 0, 0, 1, 1, 1, 1)

# The Bezier knot vector for the surface.
# This knot vector is used in both the U and
# V directions.
knots = (0, 0, 0, 0, 1, 1, 1, 1)

# Create the nodes needed for the Bezier patch
# and its trim curves.
def makeSurface():
    surfSep = SoSeparator()
    surfSep.ref()

    # Define the Bezier surface including the control
    # points, trim curve, and a complexity.
    complexity = SoComplexity()
    controlPts = SoCoordinate3()
    surface    = SoNurbsSurface()
    complexity.value(0.7)
    controlPts.point.setValues(0, 16, pts)
    surface.numUControlPoints.setValue(4)
    surface.numVControlPoints.setValue(4)
    surface.uKnotVector.setValues(0, 8, knots)
    surface.vKnotVector.setValues(0, 8, knots)
    surfSep.addChild(complexity)
    surfSep.addChild(controlPts)
    
    trimPts = SoProfileCoordinate2()
    nTrim1 = SoNurbsProfile()
    nTrim2 = SoNurbsProfile()
    nTrim3 = SoNurbsProfile()

    trimPts.point.setValues(0, 12, tpts)
    trimInds = (0, 1, 2, 3, 0)
    nTrim1.index.setValues(0, 5, trimInds)
    nTrim1.knotVector.setValues(0, 7, tknots1)
    trimInds = (4, 5, 6, 7)
    nTrim2.linkage.setValue(SoProfile.START_NEW)
    nTrim2.index.setValues(0, 4, trimInds)
    nTrim2.knotVector.setValues(0, 6, tknots2)
    trimInds = (7, 8, 9, 4)
    nTrim3.linkage.setValue(SoProfile.ADD_TO_CURRENT)
    nTrim3.index.setValues(0, 4, trimInds)
    nTrim3.knotVector.setValues(0, 8, tknots3)

    surfSep.addChild(trimPts)
    surfSep.addChild(nTrim1)
    surfSep.addChild(nTrim2)
    surfSep.addChild(nTrim3)
    surfSep.addChild(surface)

    surfSep.unrefNoDelete()
    return surfSep

# CODE FOR The Inventor Mentor ENDS HERE
############################################################


def main():
    # Initialize Inventor and Qt
    appWindow = SoGui.init(sys.argv[0])
    if appWindow == None:
        sys.exit(1)

    root = SoSeparator()
    root.ref()

    rot = SoRotation()
    rot.rotation.setValue(SbRotation(SbVec3f(0.0, 1.0, 0.0), M_PI/2.0))
    root.addChild(rot)

    # Create the scene graph for the carpet
    carpet = SoSeparator()
    surf   = makeSurface()
    tex    = SoTexture2()

    tex.ref()
    tex.filename.setValue("diamondRug.rgb")
    carpet.addChild(tex)
    carpet.addChild(surf)
    root.addChild(carpet)

    # Create the scene graph for the floor
    floor = SoSeparator()
    xlate = SoTranslation()
    scale = SoScale()
    input = SoInput()

    input.setBuffer(floorData)
    result = SoDB.readAll(input)
    xlate.translation.setValue(SbVec3f(-12.0, -5.0, -5.0))
    scale.scaleFactor.setValue(SbVec3f(2.0, 1.0, 2.0))
    floor.addChild(xlate)
    floor.addChild(scale)
    floor.addChild(result)
    root.addChild(floor)

    # Create the scene graph for the carpet's shadow
    shadow = SoSeparator()
    shmdl  = SoLightModel()
    shmtl  = SoMaterial()
    shclr  = SoBaseColor()
    shxl   = SoTranslation()
    shscl  = SoScale()

    shmdl.model(SoLightModel.BASE_COLOR)
    shclr.rgb.setValue(SbColor(0.21, 0.15, 0.09))
    shmtl.transparency(0.3)
    shxl.translation.setValue(SbVec3f(0.0, -4.9, 0.0))
    shscl.scaleFactor.setValue(SbVec3f(1.0, 0.0, 1.0))
    shadow.addChild(shmtl)
    shadow.addChild(shmdl)
    shadow.addChild(shclr)
    shadow.addChild(shxl)
    shadow.addChild(shscl)
    shadow.addChild(surf)
    root.addChild(shadow)

    # Initialize an Examiner Viewer
    viewer = SoGuiExaminerViewer(appWindow)
    viewer.setSceneGraph(root)
    viewer.setTitle("Trimmed Nurbs Surface")
    cam = viewer.getCamera()
    cam.position.setValue(SbVec3f(-8.5, 13.0, 23.0))
    cam.pointAt(SbVec3f(-2.0, -2.0, -4.0))
    viewer.show()

    SoGui.show(appWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
