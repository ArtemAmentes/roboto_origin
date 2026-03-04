#!/usr/bin/env python3
"""
Создание PDF руководства по сборке робота ATOM 01 на русском.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Регистрация шрифта
font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont('RussianFont', font_path))
    FONT_NAME = 'RussianFont'
else:
    FONT_NAME = 'Helvetica'


def create_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='RuTitle', fontName=FONT_NAME, fontSize=18, leading=22,
        alignment=TA_CENTER, spaceAfter=20
    ))
    styles.add(ParagraphStyle(
        name='RuH1', fontName=FONT_NAME, fontSize=14, leading=18,
        spaceBefore=15, spaceAfter=10, textColor=colors.darkblue
    ))
    styles.add(ParagraphStyle(
        name='RuH2', fontName=FONT_NAME, fontSize=12, leading=15,
        spaceBefore=12, spaceAfter=8, textColor=colors.darkblue
    ))
    styles.add(ParagraphStyle(
        name='RuBody', fontName=FONT_NAME, fontSize=10, leading=13,
        alignment=TA_JUSTIFY, spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='RuBullet', fontName=FONT_NAME, fontSize=10, leading=13,
        leftIndent=20, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name='RuNote', fontName=FONT_NAME, fontSize=9, leading=12,
        backColor=colors.lightyellow, borderPadding=5, spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name='RuStep', fontName=FONT_NAME, fontSize=11, leading=14,
        spaceBefore=8, spaceAfter=4, textColor=colors.darkgreen
    ))
    
    return styles


def create_assembly_guide_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    
    styles = create_styles()
    story = []
    
    # Титульная страница
    story.append(Spacer(1, 5*cm))
    story.append(Paragraph("РУКОВОДСТВО ПО СБОРКЕ", styles['RuTitle']))
    story.append(Paragraph("Робот АТОМ 01", styles['RuTitle']))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Версия 1.14", styles['RuBody']))
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("Февраль 2026", styles['RuBody']))
    story.append(PageBreak())
    
    # Общие примечания
    story.append(Paragraph("ОБЩИЕ ПРИМЕЧАНИЯ", styles['RuH1']))
    story.append(Paragraph(
        "1. При затяжке всех винтов соблюдайте метод диагональной затяжки: затянув один винт, "
        "затяните диагонально противоположный, затем остальные.",
        styles['RuBody']
    ))
    story.append(Paragraph(
        "2. Перед затяжкой всех винтов нанесите на резьбу небольшое количество фиксатора резьбы.",
        styles['RuBody']
    ))
    story.append(PageBreak())
    
    # Часть 1: Сборка руки
    story.append(Paragraph("ЧАСТЬ 1: СБОРКА РУКИ РОБОТА (ОДНА РУКА)", styles['RuH1']))
    
    story.append(Paragraph("Необходимые детали (без винтов)", styles['RuH2']))
    
    parts_arm = [
        ["Наименование детали", "Количество"],
        ["Двигатель DM340p", "3 шт."],
        ["Рука atom - копия (1)", "1 шт."],
        ["Рука atom - копия (2)", "2 шт."],
        ["Рука atom - копия (3)", "2 шт."],
        ["Рука atom - копия (4)", "1 шт."],
        ["Винт M3×8 с внутр. шестигранником", "12 шт."],
        ["Винт M3×10 с плоской головкой", "12 шт."],
        ["Винт M3×10 с внутр. шестигранником", "12 шт."],
        ["Винт M3×16 с внутр. шестигранником", "24 шт."],
    ]
    
    t = Table(parts_arm, colWidths=[10*cm, 5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    
    arm_steps = [
        ("Шаг 1", "Соберите деталь «Рука atom - копия (3)» с двигателем DM340p. Поместите двигатель в деталь, выровняйте и закрепите 6 винтами M3×8. Обратите внимание на положение разъёма двигателя."),
        ("Шаг 2", "Соберите сборку из шага 1 с деталью «Рука atom - копия (4)». Соедините на стороне, противоположной двигателю, закрепите 12 винтами M3×10 с плоской головкой."),
        ("Шаг 3", "Аналогично шагу 1: поместите DM340p в «Рука atom - копия (3)», закрепите 6 винтами M3×8."),
        ("Шаг 4", "Соберите сборку из шага 1 с «Рука atom - копия (1)». Выровняйте конец с пазом на внешней окружности, закрепите 6 винтами M3×16."),
        ("Шаг 5", "Установите DM340p в «Рука atom - копия (1)». Выровняйте с вогнутой стороной двигателя, закрепите 6 винтами M3×10."),
        ("Шаг 6", "Соберите «Рука atom - копия (2)» со сборкой из шага 2. Сначала закрепите M3×16, затем замените на M3×10 для фиксации с DM340p."),
        ("Шаг 7", "Соедините сборку из шага 6 со сборкой из шага 5. Закрепите 6 винтами M3×16."),
        ("Шаг 8", "Соберите сборку из шага 7 с «Рука atom - копия (2)». Закрепите 6 винтами M3×16."),
    ]
    
    for step, desc in arm_steps:
        story.append(Paragraph(f"<b>{step}</b>", styles['RuStep']))
        story.append(Paragraph(desc, styles['RuBody']))
    
    story.append(Paragraph("Сборка руки завершена. Соберите вторую руку аналогично.", styles['RuNote']))
    story.append(PageBreak())
    
    # Часть 2: Сборка ноги
    story.append(Paragraph("ЧАСТЬ 2: СБОРКА НОГИ РОБОТА (ОДНА НОГА)", styles['RuH1']))
    
    story.append(Paragraph("Необходимые детали (без винтов)", styles['RuH2']))
    
    parts_leg = [
        ["Наименование детали", "Количество"],
        ["Двигатель DM-J10010L", "1 шт."],
        ["Двигатель DM4340p", "2 шт."],
        ["Радиальный шарнирный подшипник", "4 шт."],
        ["Карданный крестовой подшипник", "1 шт."],
        ["Соединитель голеностопа боковой", "1 шт."],
        ["Замок подшипника голени", "2 шт."],
        ["Рычаг подошвы", "1 шт."],
        ["Подошва", "1 шт."],
        ["Выходной фланцевый рычаг", "2 шт."],
        ["Упорный игольчатый подшипник", "1 шт."],
        ["Ограничительный штифт", "2 шт."],
    ]
    
    t = Table(parts_leg, colWidths=[10*cm, 5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    
    leg_steps = [
        ("Шаг 1", "Соберите внутреннюю часть бедра с DM-J10010L. Расположите в положении стоящего робота. Разъём мотора вертикально, «DM-J10010L-2EC» вниз. Сначала M4×12 для позиционирования, затем M4×8 диагонально. Всего: 8 винтов M4×8."),
        ("Шаг 2", "Соберите голень с 2 двигателями DM4340p. Два порта сверху и снизу. Переверните, затяните M3×8. Всего: 12 винтов M3×8."),
        ("Шаг 3", "Соберите длинный и короткий рычаги с 4 радиальными шарнирными подшипниками. Нанесите клей на внутренние стенки. Запрессуйте ручным прессом по 2 подшипника на рычаг."),
        ("Шаг 4", "Соберите карданный крестовой подшипник с соединителем голеностопа. Снимите крышки с диагональных концов, запрессуйте в соединитель."),
        ("Шаг 5", "Соберите сборку шага 4 со сборкой шага 2. Используйте замки подшипника. Всего: 4 винта M5×10, 4 винта M4×8."),
        ("Шаг 6", "Соберите подошву и рычаг подошвы. Всего: 10 винтов M5×12."),
        ("Шаг 7", "Соберите выходные фланцевые рычаги и рычаги из шага 3. Всего: 10 винтов M3×12, 4 винта M5×16."),
        ("Шаг 8", "Соберите бедро с голенью. Поместите упорный игольчатый подшипник между ними. Всего: 9 винтов M5×10. Ограничительные штифты — после калибровки: 2 винта M4×14."),
    ]
    
    for step, desc in leg_steps:
        story.append(Paragraph(f"<b>{step}</b>", styles['RuStep']))
        story.append(Paragraph(desc, styles['RuBody']))
    
    story.append(Paragraph("Сборка ноги завершена. Соберите вторую ногу аналогично.", styles['RuNote']))
    story.append(PageBreak())
    
    # Часть 3: Сборка таза
    story.append(Paragraph("ЧАСТЬ 3: СБОРКА ТАЗОБЕДРЕННОЙ ЧАСТИ", styles['RuH1']))
    
    story.append(Paragraph("Необходимые детали (без винтов)", styles['RuH2']))
    
    parts_hip = [
        ["Наименование детали", "Количество"],
        ["Двигатель DM-J10010L", "6 шт."],
        ["Пластина тазобедренная", "2 шт."],
        ["Упорный игольчатый подшипник", "4 шт."],
        ["Универсальный соединитель", "4 шт."],
        ["Универсальный соединитель с расш. фланцем", "2 шт."],
        ["Универсальный расширенный фланец", "2 шт."],
    ]
    
    t = Table(parts_hip, colWidths=[10*cm, 5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    
    hip_steps = [
        ("Шаг 1", "Соберите 2 DM-J10010L с 2 тазобедренными пластинами. «DM-J10010L-2EC» в одну сторону. Затяните диагонально, шуруповёрт на максимум, минимум 2 цикла. Вторую пластину постучите молотком до глухого звука. Всего: 32 винта M4×8."),
        ("Шаг 2", "Установите 2 упорных игольчатых подшипника в вогнутые части пластин. Установите 2 универсальных соединителя. Всего: 14 винтов M5×16."),
        ("Шаг 3", "Установите 2 DM-J10010L на стороны соединителей. «DM-J10010L» перевёрнуто вверх. Всего: 12 винтов M4×10, 8 винтов M4×10 плоских, 4 винта M3×10."),
        ("Шаг 4", "Установите 2 соединителя с расширенным фланцем. Всего: 20 винтов M4×8."),
        ("Шаг 5", "Установите 2 упорных подшипника, 2 универсальных соединителя, 2 DM-J10010L. Всего: 14 винтов M5×16, 20 винтов M4×8, 8 винтов M4×12."),
        ("Шаг 6", "Установите 2 универсальных расширенных фланца. Всего: 20 винтов M4×8, 8 винтов M4×12."),
    ]
    
    for step, desc in hip_steps:
        story.append(Paragraph(f"<b>{step}</b>", styles['RuStep']))
        story.append(Paragraph(desc, styles['RuBody']))
    
    story.append(Paragraph("Сборка тазобедренной части завершена.", styles['RuNote']))
    story.append(PageBreak())
    
    # Часть 4: Грудная клетка и поясница
    story.append(Paragraph("ЧАСТЬ 4: СБОРКА ГРУДНОЙ КЛЕТКИ И ПОЯСНИЦЫ", styles['RuH1']))
    
    torso_steps = [
        ("Шаг 1", "Соберите 2 пластины, 2 плеча и 2 боковые панели в замкнутый прямоугольник. Одну боковую панель оставьте для установки батареи. Всего: 40 винтов M4×10."),
        ("Шаг 2", "Забейте радиальный шарикоподшипник в крепление подшипника резиновым молотком."),
        ("Шаг 3", "Установите крепление подшипника на DM-J10010L. Всего: 10 винтов M4×8."),
        ("Шаг 4", "Установите основание аккумулятора на подшипник. Всего: 9 винтов M5×10."),
        ("Шаг 5", "Установите фиксатор тазобедренного сустава. У выхода проводов — плоские винты. Всего: 4 винта M4×12 плоских, 6 винтов M4×12."),
        ("Шаг 6", "Соедините поясницу с грудной клеткой. Всего: 14 винтов M4×10."),
        ("Шаг 7", "Установите плату IMU на фиксатор. Всего: 6 винтов M3×8."),
    ]
    
    for step, desc in torso_steps:
        story.append(Paragraph(f"<b>{step}</b>", styles['RuStep']))
        story.append(Paragraph(desc, styles['RuBody']))
    
    story.append(Paragraph("Сборка грудной клетки и поясницы завершена.", styles['RuNote']))
    story.append(PageBreak())
    
    # Часть 5: Финальная сборка
    story.append(Paragraph("ЧАСТЬ 5: ФИНАЛЬНАЯ СБОРКА", styles['RuH1']))
    
    final_steps = [
        ("Шаг 1", "Соедините фиксатор таза с тазобедренной частью. «DM-J10010L-2EC» к длинной стороне фиксатора. Сначала 4 винта M4×12 по краям, затем остальные. Всего: 64 винта M4×12."),
        ("Шаг 2", "Вкрутите рым-болты в плечевую часть. Отрегулируйте углы суставов."),
        ("Шаг 3", "Установите 2 DM340p в плечевые отверстия, корпус внутри грудной клетки. Всего: 12 винтов M3×6."),
        ("Шаг 4", "Установите 2 «Рука atom - копия (1)» на DM340p. Сторона с пазом к резьбовым отверстиям. Всего: 12 винтов M3×16."),
        ("Шаг 5", "Установите 2 DM340p на окружность деталей руки. Сначала M3×16, затем M3×10. Всего: 12 винтов M3×10."),
        ("Шаг 6", "Установите 2 руки робота. Выровняйте «копия (2)» с «копия (1)». Всего: 12 винтов M3×16."),
        ("Шаг 7", "Подвесьте робота на приспособлении для установки ног."),
        ("Шаг 8", "Установите ноги. Поверните передние DM-J10010L выпуклыми сторонами внутрь. Установите упорные подшипники. Всего: 18 винтов M5×10."),
    ]
    
    for step, desc in final_steps:
        story.append(Paragraph(f"<b>{step}</b>", styles['RuStep']))
        story.append(Paragraph(desc, styles['RuBody']))
    
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("СБОРКА РОБОТА ПОЛНОСТЬЮ ЗАВЕРШЕНА!", styles['RuTitle']))
    
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Документ создан: Февраль 2026", styles['RuBody']))
    story.append(Paragraph("Проект РОБОТ — открытый российский проект робототехники", styles['RuBody']))
    
    doc.build(story)
    print(f"Создан PDF: {output_path}")


if __name__ == "__main__":
    output = "/Users/amentes/Desktop/РОБОТЫ/robot/modules/Atom01_hardware/atom01_mechnaic/00_Docs/руководство_по_сборке_v1.14_RU.pdf"
    create_assembly_guide_pdf(output)
