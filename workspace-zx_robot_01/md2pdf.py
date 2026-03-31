# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register Chinese font (use system font)
pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))

# Create PDF
c = canvas.Canvas(r"C:\Users\LWS\.openclaw\workspace-zx_robot_01\一年级下册语文一二单元考点清单.pdf", pagesize=A4)
width, height = A4

# Title
c.setFont("SimHei", 18)
c.drawCentredString(width/2, height - 50, "部编版一年级下册语文一二单元 考点清单")

# Content
c.setFont("SimHei", 10)
y = height - 90

lines = [
    "",
    "📌 通用必考（课本必抓）",
    "",
    "考点              怎么考                怎么练",
    "────────────────────────────────────────────────────────────",
    "会认字            读音、连线组词        每天读蓝色条生字，口头组2词",
    "会写字            看拼音写词、笔顺      田字格字书空写笔顺，组词",
    "拼音              平翘舌、前后鼻音      拼读课文音节，重点练 zh/ch/sh vs z/c/s",
    "词语              ABB/AABB式、搭配     记课本原词，如\"红红的\"\"开开心心\"",
    "背诵              按课文填空            合书背诵，易错句反复巩固",
    "仿写              课本句式仿写          仿说生活中句子，如\"弯弯的___像___\"",
    "",
    "⚠️ 第一单元难点",
    "",
    "• 发音：平翘舌、前后鼻音分不清",
    "• 字形：\"青清晴情请\"同音字家族",
    "• 笔顺：火、水、心、方易错",
    "",
    "家庭辅导：",
    "- 每天10分钟指读蓝色条生字，田字格书空写笔顺",
    "- 口诀记字：\"日出天晴，河水清清，心情真好，请你过来\"",
    "",
    "⚠️ 第二单元难点",
    "",
    "• 课文朗读不添字漏字",
    "• 说完整句子、仿写无从下手",
    "• 词语搭配不规范",
    "",
    "家庭辅导：",
    "- 朗读：家长范读→跟读→独立读，不指读、不拖音",
    "- 句子练习：结合课本例句仿说，如\"弯弯的眉毛像月牙\"",
    "",
    "💡 辅导温馨提示",
    "",
    "1. 时长：每天15-20分钟足够",
    "2. 重点：紧抓课本，吃透生字+课文+课后题，无需刷题",
    "3. 态度：多表扬、少批评，培养兴趣",
    "4. 检查：每天3件事 ✓ 田字格会写会组词 ✓ 必背会背 ✓ 课后题会答",
]

for line in lines:
    c.drawString(50, y, line)
    y -= 15
    if y < 50:
        c.showPage()
        c.setFont("SimHei", 10)
        y = height - 50

c.save()
print("PDF created successfully!")