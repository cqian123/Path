"""
控制厚度变化的函数
"""
import numpy
def thick (thickest,thick_d_value,num_translation,i):
    thickness = (thickest - thick_d_value * i) / num_translation
    return thickness