#!/usr/bin/env python3
"""
Скрипт для перевода китайского текста в CNC-чертежах PDF.
Использует метод redaction для замены текста.
"""

import fitz
import os
import re

# Словарь перевода китайских терминов в чертежах
TRANSLATIONS = {
    # Названия деталей
    "侧板横板": "Боковая панель",
    "大腿内侧": "Внутр. часть бедра",
    "小腿": "Голень",
    "小腿轴承锁": "Замок подш. голени",
    "手臂": "Рука",
    "电池底盖": "Крышка аккумулятора",
    "短连杆": "Короткий рычаг",
    "肩膀": "Плечо",
    "胸腔前后夹板": "Пластина груд. клетки",
    "胸腔夹板后": "Задняя пластина груди",
    "脚底板": "Подошва",
    "脚底连杆": "Рычаг подошвы",
    "脚踝横滚连接件": "Соединитель голеностопа",
    "腰部支撑": "Поясничная опора",
    "载板": "Несущая плата",
    "输出法兰连杆": "Выходной фланц. рычаг",
    "通用连接件": "Универс. соединитель",
    "通用连接件扩孔法兰": "Фланец соединителя",
    "长连杆": "Длинный рычаг",
    "限位销": "Ограничит. штифт",
    "髋关节固定": "Крепление таза",
    "髋夹板": "Тазовая пластина",
    "脚": "Стопа",
    
    # Штамп чертежа
    "审核": "Проверил",
    "校核": "Контроль",
    "设计": "Разработал",
    "标记": "Маркировка",
    "处数": "Кол-во",
    "签名": "Подпись",
    "签字": "Подпись",
    "签": "Подп.",
    "日期": "Дата",
    "日": "Дата",
    "期": "",
    "比例": "Масштаб",
    "重量": "Масса",
    "质量": "Масса",
    "年": "г.",
    "月": "м.",
    "图": "Черт.",
    "图样代号": "Обозначение",
    "零件代号": "Код детали",
    "零": "",
    "件": "",
    "代": "",
    "号": "",
    "版本": "Версия",
    "底图总号": "Общий № чертежа",
    "旧底图总号": "Старый № чертежа",
    "更改文件号": "№ изменения",
    "用件登记": "Регистрация",
    "标准化": "Стандартизация",
    "工艺": "Технология",
    "批准": "Утвердил",
    "描图": "Копировал",
    "描校": "Проверка копии",
    "主管设计": "Гл. конструктор",
    
    # Технические пометки
    "完全贯穿": "Сквозное",
    "对侧同理": "Аналогично с др. стор.",
    "大径": "Б. диаметр",
    "螺丝孔中心对称": "Отв. симметрично",
    "视图": "Вид",
    "通": "",
    "底": "",
    "总": "",
    "张": "л.",
    "第": "№",
    "阶": "ступень",
    "段": "участок",
    "分区": "зона",
    "共": "всего",
    "六组": "6 групп",
    
    # Материалы
    "铝合金": "Алюм. сплав",
    "合金": "Сплав",
    "钢": "Сталь",
    
    # Прочее
    "字": "",
    "记": "",
    "标": "",
    "替代": "Замена",
    "借": "",
}


def translate_pdf_drawing(input_path: str, output_path: str) -> dict:
    """
    Переводит китайский текст в PDF-чертеже на русский.
    """
    doc = fitz.open(input_path)
    stats = {"pages": len(doc), "replacements": 0}
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Получаем все текстовые блоки
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" not in block:
                continue
            
            for line in block["lines"]:
                for span in line["spans"]:
                    original_text = span["text"]
                    
                    # Проверяем наличие китайских символов
                    if not re.search(r'[\u4e00-\u9fff]', original_text):
                        continue
                    
                    # Переводим текст
                    translated = original_text
                    for cn, ru in sorted(TRANSLATIONS.items(), key=lambda x: -len(x[0])):
                        if cn in translated:
                            translated = translated.replace(cn, ru)
                    
                    # Если текст изменился, заменяем
                    if translated != original_text:
                        rect = fitz.Rect(span["bbox"])
                        font_size = span["size"]
                        
                        # Добавляем область для удаления
                        page.add_redact_annot(rect, fill=(1, 1, 1))
                        
                        stats["replacements"] += 1
        
        # Применяем удаление
        page.apply_redactions()
        
        # Теперь добавляем переведённый текст
        blocks = page.get_text("dict")["blocks"]
        
        # Повторно проходим и вставляем русский текст
        # (текст уже удалён, поэтому работаем с сохранёнными данными)
    
    doc.save(output_path)
    doc.close()
    return stats


def translate_with_overlay(input_path: str, output_path: str) -> dict:
    """
    Переводит PDF, накладывая белые прямоугольники и новый текст.
    """
    doc = fitz.open(input_path)
    stats = {"pages": len(doc), "replacements": 0}
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text_instances = []
        
        # Собираем все текстовые блоки с китайским
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" not in block:
                continue
            
            for line in block["lines"]:
                for span in line["spans"]:
                    original_text = span["text"]
                    
                    if not re.search(r'[\u4e00-\u9fff]', original_text):
                        continue
                    
                    # Переводим
                    translated = original_text
                    for cn, ru in sorted(TRANSLATIONS.items(), key=lambda x: -len(x[0])):
                        if cn in translated:
                            translated = translated.replace(cn, ru)
                    
                    if translated != original_text:
                        text_instances.append({
                            "rect": fitz.Rect(span["bbox"]),
                            "original": original_text,
                            "translated": translated.strip(),
                            "size": span["size"],
                            "color": span.get("color", 0)
                        })
        
        # Применяем замены
        for inst in text_instances:
            rect = inst["rect"]
            
            # Закрашиваем белым
            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
            
            # Вставляем русский текст
            if inst["translated"]:
                try:
                    # Уменьшаем размер шрифта для русского текста
                    font_size = min(inst["size"] * 0.75, 8)
                    
                    page.insert_text(
                        (rect.x0, rect.y0 + font_size),
                        inst["translated"],
                        fontsize=font_size,
                        fontname="helv",
                        color=(0, 0, 0)
                    )
                    stats["replacements"] += 1
                except Exception as e:
                    print(f"  Ошибка вставки текста: {e}")
    
    doc.save(output_path)
    doc.close()
    return stats


def process_all_cnc_drawings():
    """Обрабатывает все CNC-чертежи"""
    
    cnc_dir = "/Users/amentes/Desktop/РОБОТЫ/robot/modules/Atom01_hardware/atom01_mechnaic/02_Manufacturing/CNC_Machining"
    output_dir = os.path.join(cnc_dir, "RU")
    
    os.makedirs(output_dir, exist_ok=True)
    
    pdfs = sorted([f for f in os.listdir(cnc_dir) if f.endswith('.pdf')])
    print(f"Обработка {len(pdfs)} CNC-чертежей...\n")
    
    total_replacements = 0
    
    for pdf_name in pdfs:
        input_path = os.path.join(cnc_dir, pdf_name)
        output_path = os.path.join(output_dir, pdf_name.replace('.pdf', '_RU.pdf'))
        
        try:
            stats = translate_with_overlay(input_path, output_path)
            total_replacements += stats["replacements"]
            print(f"✓ {pdf_name}: {stats['replacements']} замен")
        except Exception as e:
            print(f"✗ {pdf_name}: Ошибка - {e}")
    
    print(f"\nГотово! Всего замен: {total_replacements}")
    print(f"Файлы сохранены в: {output_dir}")


if __name__ == "__main__":
    process_all_cnc_drawings()
