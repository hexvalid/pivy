/**************************************************************************\
 *
 *  This file is part of the Coin 3D visualization library.
 *  Copyright (C) 1998-2002 by Systems in Motion. All rights reserved.
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public License
 *  version 2.1 as published by the Free Software Foundation. See the
 *  file LICENSE.LGPL at the root directory of the distribution for
 *  more details.
 *
 *  If you want to use Coin for applications not compatible with the
 *  LGPL, please contact SIM to acquire a Professional Edition license.
 *
 *  Systems in Motion, Prof Brochs gate 6, 7030 Trondheim, NORWAY
 *  http://www.sim.no support@sim.no Voice: +47 22114160 Fax: +47 22207097
 *
\**************************************************************************/

#ifndef COIN_SOMFVEC4F_H
#define COIN_SOMFVEC4F_H

#include <Inventor/fields/SoMField.h>
#include <Inventor/fields/SoSubField.h>
#include <Inventor/SbVec4f.h>

#ifdef __PIVY__
%{
static void
convert_SoMFVec4f_array(PyObject *input, int len, float temp[][4])
{
  int i,j;

  for (i=0; i<len; i++) {
	PyObject *oi = PySequence_GetItem(input,i);

	for (j=0; j<4; j++) {
	  PyObject *oj = PySequence_GetItem(oi,j);

	  if (PyNumber_Check(oj)) {
		temp[i][j] = (float) PyFloat_AsDouble(oj);
	  } else {
		PyErr_SetString(PyExc_ValueError,"Sequence elements must be numbers");
		free(temp);       
		return;
	  }
	}
  }
  return;
}
%}

%typemap(in) float xyzw[][4] (float (*temp)[4]) {
  int len;

  if (PySequence_Check($input)) {
	len  = PySequence_Length($input);

	temp = (float (*)[4]) malloc(len*4*sizeof(float));
	convert_SoMFVec4f_array($input, len, temp);
  
	$1 = temp;
  } else {
	PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}

%typemap(in) float xyzw[4] (float temp[4]) {
  convert_SbVec4f_array($input, temp);
  $1 = temp;
}

%rename(setValue_vec) SoMFVec4f::setValue(SbVec4f const &);
%rename(setValue_ffff) SoMFVec4f::setValue(const float x, const float y, const float z, const float w);

%feature("shadow") SoMFVec4f::setValue(const float xyzw[4]) %{
def setValue(*args):
   if isinstance(args[1], SbVec4f):
      return apply(pivyc.SoMFVec4f_setValue_vec,args)
   elif len(args) == 5:
      return apply(pivyc.SoMFVec4f_setValue_ffff,args)
   return apply(pivyc.SoMFVec4f_setValue,args)
%}

%rename(set1Value_i_vec) SoMFVec4f::set1Value(int const ,SbVec4f const &);
%rename(set1Value_i_ffff) SoMFVec4f::set1Value(const int idx, const float x, const float y, const float z, const float w);

%feature("shadow") SoMFVec4f::set1Value(const int idx, const float xyzw[4]) %{
def set1Value(*args):
   if isinstance(args[2], SbVec4f):
      return apply(pivyc.SoMFVec4f_set1Value_i_vec,args)
   elif len(args) == 6:
      return apply(pivyc.SoMFVec4f_set1Value_i_fff,args)
   return apply(pivyc.SoMFVec4f_set1Value,args)
%}

%rename(setValues_i_i_vec) SoMFVec4f::setValues(int const ,int const ,SbVec4f const *);

%feature("shadow") SoMFVec4f::setValues(const int start, const int num, const float xyzw[][4]) %{
def setValues(*args):
   if isinstance(args[3], SbVec4f):
      return apply(pivyc.SoMFVec4f_setValues_i_i_vec,args)
   return apply(pivyc.SoMFVec4f_setValues,args)
%}
#endif

class COIN_DLL_API SoMFVec4f : public SoMField {
  typedef SoMField inherited;

  SO_MFIELD_HEADER(SoMFVec4f, SbVec4f, const SbVec4f &);

public:
  static void initClass(void);

  void setValues(const int start, const int num, const float xyzw[][4]);
  void set1Value(const int idx,
                 const float x, const float y, const float z, const float w);
  void set1Value(const int idx, const float xyzw[4]);
  void setValue(const float x, const float y, const float z, const float w);

#ifdef __PIVY__
  %addmethods {
        void __call__(float xyzw[4]) {
          self->setValue(xyzw);
        }
  }
#endif

  void setValue(const float xyzw[4]);
};

#endif // !COIN_SOMFVEC4F_H