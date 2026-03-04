#!/usr/bin/env python3
"""
Создание русских PDF-документов с использованием ReportLab.
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

# Регистрируем шрифт с поддержкой кириллицы
# Используем системные шрифты macOS
FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Courier New.ttf",
]

font_registered = False
for font_path in FONT_PATHS:
    if os.path.exists(font_path):
        try:
            if font_path.endswith('.ttc'):
                # TrueType Collection - пропускаем
                continue
            pdfmetrics.registerFont(TTFont('RussianFont', font_path))
            font_registered = True
            print(f"Зарегистрирован шрифт: {font_path}")
            break
        except Exception as e:
            print(f"Не удалось загрузить шрифт {font_path}: {e}")

if not font_registered:
    # Используем DejaVu если есть
    dejavu_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/DejaVuSans.ttf",
    ]
    for path in dejavu_paths:
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont('RussianFont', path))
            font_registered = True
            break

FONT_NAME = 'RussianFont' if font_registered else 'Helvetica'


def create_styles():
    """Создаёт стили для документа"""
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='RussianTitle',
        fontName=FONT_NAME,
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=20
    ))
    
    styles.add(ParagraphStyle(
        name='RussianHeading1',
        fontName=FONT_NAME,
        fontSize=14,
        leading=18,
        spaceBefore=15,
        spaceAfter=10,
        textColor=colors.darkblue
    ))
    
    styles.add(ParagraphStyle(
        name='RussianHeading2',
        fontName=FONT_NAME,
        fontSize=12,
        leading=15,
        spaceBefore=12,
        spaceAfter=8,
        textColor=colors.darkblue
    ))
    
    styles.add(ParagraphStyle(
        name='RussianBody',
        fontName=FONT_NAME,
        fontSize=10,
        leading=13,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    ))
    
    styles.add(ParagraphStyle(
        name='RussianBullet',
        fontName=FONT_NAME,
        fontSize=10,
        leading=13,
        leftIndent=20,
        spaceAfter=4
    ))
    
    styles.add(ParagraphStyle(
        name='RussianWarning',
        fontName=FONT_NAME,
        fontSize=10,
        leading=13,
        backColor=colors.lightyellow,
        borderColor=colors.orange,
        borderWidth=1,
        borderPadding=5,
        spaceAfter=10
    ))
    
    return styles


def create_main_manual(output_path):
    """Создаёт основное руководство на русском"""
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    styles = create_styles()
    story = []
    
    # Титульная страница
    story.append(Spacer(1, 5*cm))
    story.append(Paragraph("РОБОТ", styles['RussianTitle']))
    story.append(Paragraph("Руководство по продукту", styles['RussianTitle']))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Версия 1.0", styles['RussianBody']))
    story.append(Paragraph("Февраль 2026", styles['RussianBody']))
    story.append(PageBreak())
    
    # Меры предосторожности
    story.append(Paragraph("МЕРЫ ПРЕДОСТОРОЖНОСТИ", styles['RussianHeading1']))
    
    precautions = [
        "1. Перед использованием внимательно изучите этот документ, чтобы понять свои права, обязанности и меры безопасности.",
        "2. Данное устройство не является игрушкой, не рекомендуется для лиц младше 18 лет.",
        "3. Не используйте продукт в местах скопления людей. Обеспечьте дистанцию не менее 1 метра между людьми и машиной.",
        "4. Продукт предназначен для использования на земле. Не поднимайте устройство во время движения.",
        "5. Не используйте продукт в экстремальных условиях (высокая/низкая температура, агрессивные химикаты).",
        "6. При нормальной эксплуатации износ деталей и старение батареи не считаются дефектами качества.",
        "7. Запрещено использовать продукт для деятельности, угрожающей национальной безопасности.",
    ]
    
    for p in precautions:
        story.append(Paragraph(p, styles['RussianBody']))
    
    story.append(PageBreak())
    
    # Безопасность при сборке
    story.append(Paragraph("МЕРЫ ПРЕДОСТОРОЖНОСТИ ПРИ СБОРКЕ", styles['RussianHeading1']))
    
    story.append(Paragraph("1. Организация рабочего места", styles['RussianHeading2']))
    story.append(Paragraph("Зонирование:", styles['RussianBody']))
    story.append(Paragraph("• Слева: зона материалов (только для текущей операции)", styles['RussianBullet']))
    story.append(Paragraph("• Центр: рабочая зона (антистатическое покрытие, чистота)", styles['RussianBullet']))
    story.append(Paragraph("• Справа: зона готовой/полуготовой продукции", styles['RussianBullet']))
    
    story.append(Paragraph("2. Средства индивидуальной защиты", styles['RussianHeading2']))
    story.append(Paragraph("• Антистатические перчатки: при работе с электронными компонентами", styles['RussianBullet']))
    story.append(Paragraph("• Нитриловые перчатки: при работе со смазками, термопастой", styles['RussianBullet']))
    story.append(Paragraph("• Рабочая шапка: длинные волосы убрать под шапку", styles['RussianBullet']))
    
    story.append(Paragraph("3. Безопасность литиевых батарей", styles['RussianHeading2']))
    story.append(Paragraph("ВНИМАНИЕ: Продукт использует литиевые батареи высокой плотности — неправильная эксплуатация может вызвать пожар!", styles['RussianWarning']))
    
    story.append(Paragraph("При падении батареи (>30 см) или сильном ударе:", styles['RussianBody']))
    story.append(Paragraph("• Запрещено повторное использование", styles['RussianBullet']))
    story.append(Paragraph("• Наклейте красную метку «На утилизацию/наблюдение»", styles['RussianBullet']))
    story.append(Paragraph("• Поместите в противовзрывной шкаф на 24 часа", styles['RussianBullet']))
    
    story.append(Paragraph("4. Порядок действий в аварийной ситуации", styles['RussianHeading2']))
    story.append(Paragraph("При аварии (дым, огонь, посторонние звуки, травма):", styles['RussianBody']))
    story.append(Paragraph("СТОП → ИЗОЛЯЦИЯ → ДОКЛАД", styles['RussianWarning']))
    story.append(Paragraph("Шаг 1: Немедленно нажмите кнопку аварийного отключения", styles['RussianBullet']))
    story.append(Paragraph("Шаг 2: Эвакуируйтесь на безопасное расстояние (>3 м)", styles['RussianBullet']))
    story.append(Paragraph("Шаг 3: При небольшом возгорании — порошковый огнетушитель (НЕ ВОДА!)", styles['RussianBullet']))
    
    story.append(PageBreak())
    
    # Обзор продукта
    story.append(Paragraph("1. ОБЗОР ПРОДУКТА", styles['RussianHeading1']))
    
    story.append(Paragraph("1.1 Описание продукта", styles['RussianHeading2']))
    story.append(Paragraph(
        "РОБОТ — это платформа человекоподобного робота для научных исследований, образования и демонстраций. "
        "Главные особенности: полностью открытый исходный код и модульная конструкция.",
        styles['RussianBody']
    ))
    
    story.append(Paragraph("1.2 Основные параметры", styles['RussianHeading2']))
    
    params_data = [
        ["Параметр", "Значение"],
        ["Высота", "1.25 м"],
        ["Вес", "34 кг"],
        ["Длина бедра", "400 мм"],
        ["Длина голени", "400 мм"],
        ["Общая длина руки", "685 мм"],
        ["Ёмкость батареи", "48V, 15Ah"],
        ["Датчик глубины", "Intel D435i (опционально)"],
        ["3D LiDAR", "RoboSense E1R (опционально)"],
        ["Пиковый момент ног", "120 Нм"],
        ["Пиковый момент рук", "27 Нм"],
        ["Энкодер", "14-битный"],
        ["Разводка кабелей", "Полностью внутренняя"],
        ["Скорость передвижения", "2 м/с (до 4 м/с)"],
        ["Моторы суставов", "Damiao (10010L, 4340P)"],
    ]
    
    params_table = Table(params_data, colWidths=[7*cm, 8*cm])
    params_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(params_table)
    
    story.append(PageBreak())
    
    # Список компонентов
    story.append(Paragraph("2. ИНСТРУКЦИЯ ПО УСТАНОВКЕ", styles['RussianHeading1']))
    story.append(Paragraph("2.2 Список компонентов", styles['RussianHeading2']))
    
    story.append(Paragraph("Упаковка A: Механические детали", styles['RussianBody']))
    
    parts_a = [
        ["№", "Артикул", "Наименование", "Кол-во"],
        ["1", "ATOM-01-001", "Рука Atom — деталь (1)", "4 шт."],
        ["2", "ATOM-01-002", "Рука Atom — деталь (2)", "4 шт."],
        ["3", "ATOM-01-003", "Рука Atom — деталь (3)", "4 шт."],
        ["4", "ATOM-01-004", "Рука Atom — деталь (4)", "4 шт."],
        ["5", "ATOM-01-005", "Плата IMU", "1 шт."],
        ["6", "ATOM-01-006", "Боковая пластина", "2 шт."],
        ["7", "ATOM-01-007", "Внутренняя часть бедра", "2 шт."],
        ["8", "ATOM-01-008", "Крышка аккумулятора", "1 шт."],
        ["9", "ATOM-01-009", "Плечо", "2 шт."],
        ["10", "ATOM-01-010", "Подошва стопы", "2 шт."],
        ["11", "ATOM-01-011", "Тяга подошвы", "2 шт."],
        ["12", "ATOM-01-012", "Соединитель голеностопа", "4 шт."],
        ["13", "ATOM-01-013", "Крепление таза", "1 шт."],
        ["14", "ATOM-01-014", "Тазобедренная шина", "2 шт."],
        ["15-26", "...", "Прочие детали", "~40 шт."],
    ]
    
    parts_table = Table(parts_a, colWidths=[1*cm, 2.5*cm, 8*cm, 2*cm])
    parts_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(parts_table)
    
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Упаковка B: Моторы + подшипники + крепёж", styles['RussianBody']))
    
    parts_b = [
        ["№", "Артикул", "Наименование", "Кол-во"],
        ["27", "ATOM-01-033", "DM 4340P (48V)", "14 шт."],
        ["28", "ATOM-01-034", "DM J10010L", "9 шт."],
        ["29", "GB/T 276", "Радиальный подшипник 130×165×18", "1 шт."],
        ["30", "GB/T 9161", "Шарнирный подшипник G8", "8 шт."],
        ["31", "GB/T 4605", "Упорный игольчатый AXK6085", "9 шт."],
        ["32", "JB/T 8925", "Крестовина кардана 16×40", "2 шт."],
    ]
    
    parts_b_table = Table(parts_b, colWidths=[1*cm, 2.5*cm, 8*cm, 2*cm])
    parts_b_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(parts_b_table)
    
    story.append(PageBreak())
    
    # Этапы установки
    story.append(Paragraph("2.3 ЭТАПЫ УСТАНОВКИ", styles['RussianHeading1']))
    
    story.append(Paragraph("Инструкция по установке ног", styles['RussianHeading2']))
    
    steps_legs = [
        ("ШАГ 1", "Расположите детали и мотор в соответствии с положением стоя робота. Убедитесь, что разъём мотора направлен вертикально. Сторона с надписью DM-J10010L-2EC направлена вниз."),
        ("ШАГ 2", "Установите DM4340p в отверстие голени. Два последовательных порта расположите сверху и снизу."),
        ("ШАГ 3-4", "Переверните и вкрутите винты M3×8, используя метод позиционирования и диагональной затяжки."),
        ("ШАГ 5", "Используйте ручной пресс для запрессовки подшипника в тягу. При использовании пресса подкладывайте пластину."),
        ("ШАГ 6-10", "Установите крестовой подшипник, замок подшипника, подошву и крестовину голеностопа."),
        ("ШАГ 11-14", "Установите упорный игольчатый подшипник."),
        ("ШАГ 15", "Установите вторую ногу аналогичным способом. Левая и правая ноги должны быть зеркально симметричны."),
    ]
    
    for step, desc in steps_legs:
        story.append(Paragraph(f"<b>{step}</b>", styles['RussianBody']))
        story.append(Paragraph(desc, styles['RussianBody']))
        story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph("Инструкция по установке таза", styles['RussianHeading2']))
    
    steps_hip = [
        ("ШАГ 16", "Разместите DM-J10010L и тазовую пластину, совместив отверстия. Убедитесь, что разъёмы мотора направлены одинаково."),
        ("ШАГ 17", "После затяжки винтов по диагонали установите шуруповёрт на максимальную скорость и затяните винты по часовой стрелке (минимум 2 цикла)."),
        ("ШАГ 18-19", "Установите вторую тазовую пластину. Постучите молотком по обратной стороне, пока звук не станет глухим."),
        ("ШАГ 20-28", "Установите упорный подшипник, универсальный фланец и мотор."),
        ("ШАГ 29-30", "Таз после установки готов. Тазобедренный сустав ожидает соединения с ногами."),
    ]
    
    for step, desc in steps_hip:
        story.append(Paragraph(f"<b>{step}</b>", styles['RussianBody']))
        story.append(Paragraph(desc, styles['RussianBody']))
        story.append(Spacer(1, 0.2*cm))
    
    story.append(PageBreak())
    
    story.append(Paragraph("Инструкция по установке поясницы", styles['RussianHeading2']))
    
    steps_waist = [
        ("ШАГ 31-33", "Установите упорный игольчатый подшипник и соедините ноги с тазом винтами M5×10."),
        ("ШАГ 34-38", "Установите мотор DM-J10010L, крепление тазобедренного сустава. Глубокие винты затягивайте ручным ключом."),
        ("ШАГ 39-44", "Установите основание батареи, пластину и плечи. Одну боковую пластину пока не устанавливайте — для удобства установки батареи."),
    ]
    
    for step, desc in steps_waist:
        story.append(Paragraph(f"<b>{step}</b>", styles['RussianBody']))
        story.append(Paragraph(desc, styles['RussianBody']))
        story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph("Инструкция по установке рук", styles['RussianHeading2']))
    
    steps_arms = [
        ("ШАГ 45-48", "Установите мотор DM4340p, закрепите винтами M3×6. Установите Руку Atom — деталь (1) винтами M4×10 и M3×16."),
        ("ШАГ 49-52", "Установите детали руки (3) и (4) с моторами DM4340p. При сборке следите за направлением деталей."),
        ("ШАГ 53-54", "Закрепите Руку Atom — деталь (4) и кисть винтами M3×8. Закрепите плечо и предплечье винтами M3×16."),
        ("ШАГ 56-57", "Установите батарею и боковую пластину из шага 44."),
    ]
    
    for step, desc in steps_arms:
        story.append(Paragraph(f"<b>{step}</b>", styles['RussianBody']))
        story.append(Paragraph(desc, styles['RussianBody']))
        story.append(Spacer(1, 0.2*cm))
    
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("СБОРКА РОБОТА ЗАВЕРШЕНА!", styles['RussianTitle']))
    
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Документ создан: Февраль 2026", styles['RussianBody']))
    story.append(Paragraph("Проект РОБОТ — открытый российский проект робототехники", styles['RussianBody']))
    
    # Собираем документ
    doc.build(story)
    print(f"Создан PDF: {output_path}")


def create_sop_manual(output_path):
    """Создаёт Стандартную операционную процедуру на русском"""
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    styles = create_styles()
    story = []
    
    # Титульная страница
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("СТАНДАРТНАЯ ОПЕРАЦИОННАЯ ПРОЦЕДУРА", styles['RussianTitle']))
    story.append(Paragraph("Сборка робота", styles['RussianTitle']))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Номер документа: RP-SOP-ASM-001", styles['RussianBody']))
    story.append(Paragraph("Версия: 1.0", styles['RussianBody']))
    story.append(Paragraph("Применимо к: подготовка к полной сборке", styles['RussianBody']))
    story.append(PageBreak())
    
    # Раздел 1
    story.append(Paragraph("1. ТРЕБОВАНИЯ К РАБОЧЕЙ СРЕДЕ И БЕЗОПАСНОСТИ", styles['RussianHeading1']))
    
    story.append(Paragraph("1.1 Организация рабочего места", styles['RussianHeading2']))
    story.append(Paragraph("Зонирование:", styles['RussianBody']))
    story.append(Paragraph("• Слева: зона материалов (только для текущей операции)", styles['RussianBullet']))
    story.append(Paragraph("• Центр: рабочая зона (антистатическое покрытие, чистота)", styles['RussianBullet']))
    story.append(Paragraph("• Справа: зона готовой/полуготовой продукции", styles['RussianBullet']))
    
    story.append(Paragraph("Предотвращение посторонних предметов (FOD):", styles['RussianBody']))
    story.append(Paragraph("Запрещено класть посторонние предметы (телефон, чашки, ключи) во избежание попадания металлических предметов внутрь продукта и короткого замыкания.", styles['RussianBody']))
    
    story.append(Paragraph("1.2 Средства индивидуальной защиты", styles['RussianHeading2']))
    
    ppe_data = [
        ["СИЗ", "Когда использовать"],
        ["Антистатические перчатки", "При работе с электронными компонентами, платами, камерами"],
        ["Нитриловые перчатки", "При работе со смазками, термопастой, фиксатором резьбы"],
        ["Рабочая шапка", "Длинные волосы убрать под шапку"],
    ]
    
    ppe_table = Table(ppe_data, colWidths=[5*cm, 10*cm])
    ppe_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(ppe_table)
    
    story.append(Paragraph("Запрещено: подвесные украшения (цепочки, браслеты), свободные рукава.", styles['RussianBody']))
    
    story.append(Paragraph("1.3 Основные правила безопасной работы", styles['RussianHeading2']))
    
    story.append(Paragraph("1.3.1 Безопасность литиевых батарей", styles['RussianBody']))
    story.append(Paragraph("При падении батареи (высота >30 см) или сильном ударе:", styles['RussianBody']))
    story.append(Paragraph("• Запрещено повторное использование", styles['RussianBullet']))
    story.append(Paragraph("• Наклейте красную метку «На утилизацию/наблюдение»", styles['RussianBullet']))
    story.append(Paragraph("• Поместите в противовзрывной шкаф или песочницу на 24 часа", styles['RussianBullet']))
    
    story.append(Paragraph("Предотвращение короткого замыкания:", styles['RussianBody']))
    story.append(Paragraph("• Разъём батареи до подключения должен быть защищён заводской крышкой или изолентой", styles['RussianBullet']))
    story.append(Paragraph("• Запрещено касаться разъёма металлическими инструментами при включённом питании", styles['RussianBullet']))
    
    story.append(Paragraph("1.3.2 Механическая безопасность", styles['RussianBody']))
    story.append(Paragraph("• Работа при отключённом питании: установка, отладка и замена суставов только при нажатой аварийной кнопке", styles['RussianBullet']))
    story.append(Paragraph("• Ручное вращение: запрещено вставлять пальцы в зазоры суставов", styles['RussianBullet']))
    
    story.append(Paragraph("1.3.3 Безопасность при работе с химикатами", styles['RussianBody']))
    story.append(Paragraph("• Фиксатор резьбы: наносить только на 3-4 витка в конце резьбы", styles['RussianBullet']))
    story.append(Paragraph("• Не допускать попадания на пластиковые детали (могут стать хрупкими)", styles['RussianBullet']))
    story.append(Paragraph("• Ветошь с химикатами — опасные отходы, утилизировать в жёлтые контейнеры", styles['RussianBullet']))
    
    story.append(PageBreak())
    
    # Раздел 2
    story.append(Paragraph("2. ИНСТРУМЕНТЫ И МАТЕРИАЛЫ", styles['RussianHeading1']))
    
    tools_data = [
        ["Категория", "Инструменты"],
        ["Сборочные", "Электрический шуруповёрт, набор шестигранных бит, резиновый молоток"],
        ["Приспособления", "Ручной пресс"],
        ["Электрические", "Цифровой мультиметр, стриппер, паяльник/паяльная станция, источник питания"],
        ["Программные", "Компьютер для отладки, Damiao Serial Assistant"],
        ["Расходные", "Кабельные стяжки, термоусадочные трубки, фиксатор резьбы, ленты"],
    ]
    
    tools_table = Table(tools_data, colWidths=[4*cm, 11*cm])
    tools_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(tools_table)
    
    # Раздел 3
    story.append(Paragraph("3. ПРЕДВАРИТЕЛЬНАЯ СБОРКА И ПРОШИВКА", styles['RussianHeading1']))
    
    story.append(Paragraph("3.1 Тестирование основных компонентов", styles['RussianHeading2']))
    story.append(Paragraph("Функциональный тест PCBA (FCT):", styles['RussianBody']))
    story.append(Paragraph("• Подайте питание на голую плату", styles['RussianBullet']))
    story.append(Paragraph("• Проверьте напряжения: 3.3V, 5V, 12V, 24V/48V", styles['RussianBullet']))
    story.append(Paragraph("• Убедитесь в соответствии норме", styles['RussianBullet']))
    
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Документ создан: Февраль 2026", styles['RussianBody']))
    story.append(Paragraph("Проект РОБОТ — открытый российский проект робототехники", styles['RussianBody']))
    
    doc.build(story)
    print(f"Создан PDF: {output_path}")


if __name__ == "__main__":
    docs_dir = "/Users/amentes/Desktop/РОБОТЫ/robot/modules/Atom01_hardware/atom01_mechnaic/00_Docs"
    
    # Основное руководство
    create_main_manual(os.path.join(docs_dir, "руководство_робот_RU.pdf"))
    
    # Стандартная операционная процедура
    create_sop_manual(os.path.join(docs_dir, "стандартная_операционная_процедура_RU.pdf"))
    
    print("\nВсе PDF-файлы созданы!")
