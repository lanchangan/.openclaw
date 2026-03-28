#!/usr/bin/env python3
"""
生成Word文档 - Bilibili视频逐字稿
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import json
import os

def set_ch