#!/usr/bin/env python3
"""
Скрипт для перевода CNC-чертежей с использованием redaction.
Полностью удаляет китайский текст и заменяет на русский.
"""

import fitz
import os
import re

# Словарь перевода
TRANSLATIONS = {
    # Названия деталей
    "侧板横板": "Боков.панель",
    "大腿内侧": "Вн.ч.бедра",
    "小腿": "Голень",
    "小腿轴承锁": "Замок подш.",
    "手臂": "Рука",
    "电池底盖": "Крышка АКБ",
    "短连杆": "Кор.рычаг",
    "肩膀": "Плечо",
    "胸腔前后夹板": "Пласт.груди",
    "胸腔夹板后": "Задн.пласт.",
    "脚底板": "Подошва",
    "脚底连杆": "Рычаг подош.",
    "脚踝横滚连接件": "Соед.голеност.",
    "腰部支撑": "Пояс.опора",
    "载板": "Плата",
    "输出法兰连杆": "Вых.фланец",
    "通用连接件": "Унив.соед.",
    "通用连接件扩孔法兰": "Фланец соед.",
    "长连杆": "Дл.рычаг",
    "限位销": "Огр.штифт",
    "髋关节固定": "Крепл.таза",
    "髋夹板": "Таз.пластина",
    "脚": "Стопа",
    
    # Штамп
    "审核": "Пров.",
    "校核": "Контр.",
    "设计": "Разраб.",
    "标记": "Марк.",
    "处数": "Кол.",
    "签名": "Подп.",
    "签字": "Подп.",
    "签": "",
    "日期": "Дата",
    "比例": "М-б",
    "重量": "Масса",
    "质量": "Масса",
    "图样代号": "Обозн.",
    "零件代号": "Код",
    "版本": "Верс.",
    "底图总号": "№черт.",
    "旧底图总号": "Ст.№",
    "更改文件号": "№изм.",
    "用件登记": "Рег.",
    "标准化": "Станд.",
    "工艺": "Техн.",
    "批准": "Утв.",
    "描图": "Копир.",
    "描校": "Пров.к.",
    "主管设计": "Гл.констр.",
    
    # Технические пометки
    "完全贯穿": "Сквозн.",
    "对侧同理": "Аналог.др.ст.",
    "大径": "Б.диам.",
    "螺丝孔中心对称": "Симм.отв.",
    "六组": "6гр.",
    
    # Материалы
    "铝合金": "Ал.спл.",
    "合金": "Сплав",
    "钢": "Сталь",
    
    # Прочее (одиночные символы - удаляем или сокращаем)
    "年": "г",
    "月": "м",
    "日": "",
    "期": "",
    "图": "",
    "零": "",
    "件": "",
    "代": "",
    "号": "",
    "字": "",
    "记": "",
    "标": "",
    "视图": "Вид",
    "通": "",
    "底": "",
    "总": "",
    "张": "л",
    "第": "№",
    "阶": "",
    "段": "",
    "分区": "",
    "共": "",
    "替代": "Зам.",
    "借": "",
}


def translate_text(text: str) -> str:
    """Переводит текст, заменяя китайские фразы на русские"""
    result = text
    for cn, ru in sorted(TRANSLATIONS.items(), key=lambda x: -len(x[0])):
        result = result.replace(cn, ru)
    return result


def process_pdf(input_path: str, output_path: str) -> int:
    """Обрабатывает один PDF-файл"""
    
    doc = fitz.open(input_path)
    replacements = 0
    
    for page in doc:
        # Собираем все текстовые области с китайским текстом
        chinese_areas = []
        
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"]
                    if re.search(r'[\u4e00-\u9fff]', text):
                        translated = translate_text(text)
                        chinese_areas.append({
                            "rect": fitz.Rect(span["bbox"]),
                            "original": text,
                            "translated": translated,
                            "size": span["size"]
                        })
        
        # Применяем redaction для удаления китайского текста
        for area in chinese_areas:
            # Добавляем redaction с новым текстом
            page.add_redact_annot(
                area["rect"],
                text=area["translated"],
                fontname="helv",
                fontsize=area["size"] * 0.7,
                fill=(1, 1, 1),
                text_color=(0, 0, 0)
            )
            replacements += 1
        
        # Применяем все redactions
        page.apply_redactions()
    
    doc.save(output_path)
    doc.close()
    
    return replacements


def main():
    cnc_dir = "/Users/amentes/Desktop/РОБОТЫ/robot/modules/Atom01_hardware/atom01_mechnaic/02_Manufacturing/CNC_Machining"
    output_dir = os.path.join(cnc_dir, "RU")
    
    # Удаляем старые файлы
    if os.path.exists(output_dir):
        for f in os.listdir(output_dir):
            if f.endswith('.pdf'):
                os.remove(os.path.join(output_dir, f))
    else:
        os.makedirs(output_dir)
    
    pdfs = sorted([f for f in os.listdir(cnc_dir) if f.endswith('.pdf')])
    print(f"Обработка {len(pdfs)} CNC-чертежей (метод redaction)...\n")
    
    total = 0
    for pdf_name in pdfs:
        input_path = os.path.join(cnc_dir, pdf_name)
        output_path = os.path.join(output_dir, pdf_name.replace('.pdf', '_RU.pdf'))
        
        try:
            count = process_pdf(input_path, output_path)
            total += count
            print(f"✓ {pdf_name}: {count} замен")
        except Exception as e:
            print(f"✗ {pdf_name}: {e}")
    
    print(f"\nГотово! Всего: {total} замен")
    print(f"Файлы в: {output_dir}")


if __name__ == "__main__":
    main()
