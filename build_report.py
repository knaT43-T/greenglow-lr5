# -*- coding: utf-8 -*-
"""Сборка отчёта по лабораторной работе №5 (GreenGlow).

Единственный источник правды для .docx. Правки текста — здесь, затем:
    python build_report.py "Отчет_ЛР5_Кислов.docx"
"""
import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.opc.constants import RELATIONSHIP_TYPE as RT

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "Отчет_ЛР5_Кислов.docx"
IMG = ROOT / "report_screens"

FNT = "Times New Roman"
BASE = 12
INDENT = Cm(1.25)

ALIGN = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
}

doc = Document()
doc.core_properties.title = "Отчет по лабораторной работе №5"
doc.core_properties.author = "Кислов К. Е."
doc.core_properties.subject = "Организация репозитория в системе управления версиями Git"

# ------------------------------------------------------------------ страница
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.left_margin, sec.right_margin = Cm(3.0), Cm(1.5)
sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)
sec.footer_distance = Cm(1.25)

# ------------------------------------------------------------- стиль Normal
normal = doc.styles["Normal"]
normal.font.name = FNT
normal.font.size = Pt(BASE)
normal.font.color.rgb = RGBColor(0, 0, 0)
rpr = normal.element.get_or_add_rPr()
rfonts = rpr.find(qn("w:rFonts"))
if rfonts is None:
    rfonts = OxmlElement("w:rFonts")
    rpr.insert(0, rfonts)
for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
    rfonts.set(qn(attr), FNT)
npf = normal.paragraph_format
npf.line_spacing = 1.5
npf.space_before = Pt(0)
npf.space_after = Pt(0)
npf.first_line_indent = INDENT
npf.alignment = ALIGN["justify"]
npf.widow_control = True

# ------------------------------------------------------- колонтитул с номером
sec.different_first_page_header_footer = False
footer_p = sec.footer.paragraphs[0]
footer_p.alignment = ALIGN["center"]
footer_p.paragraph_format.first_line_indent = Cm(0)
footer_p.paragraph_format.line_spacing = 1.0
for r in list(footer_p.runs):
    r._r.getparent().remove(r._r)
run = footer_p.add_run()
run.font.name = FNT
run.font.size = Pt(BASE)
fld1 = OxmlElement("w:fldChar")
fld1.set(qn("w:fldCharType"), "begin")
instr = OxmlElement("w:instrText")
instr.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
instr.text = " PAGE "
fld2 = OxmlElement("w:fldChar")
fld2.set(qn("w:fldCharType"), "separate")
txt = OxmlElement("w:t")
txt.text = "1"
fld3 = OxmlElement("w:fldChar")
fld3.set(qn("w:fldCharType"), "end")
for el in (fld1, instr, fld2, txt, fld3):
    run._r.append(el)

# Разрешить Word обновить поле PAGE при открытии.
settings = doc.settings.element
upd = OxmlElement("w:updateFields")
upd.set(qn("w:val"), "true")
settings.append(upd)


# ------------------------------------------------------------------- хелперы
def _set_run(run, size=BASE, bold=False, italic=False):
    run.font.name = FNT
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(attr), FNT)
    return run


def P(runs, align="justify", indent=True, space_before=0, space_after=0,
      keep_with_next=False, line_spacing=1.5):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.first_line_indent = INDENT if indent else Cm(0)
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line_spacing
    pf.keep_with_next = keep_with_next
    p.alignment = ALIGN[align]
    if isinstance(runs, str):
        runs = [(runs, False)]
    for item in runs:
        text = item[0]
        bold = item[1] if len(item) > 1 else False
        italic = item[2] if len(item) > 2 else False
        _set_run(p.add_run(text), bold=bold, italic=italic)
    return p


def H(text, size=BASE, align="center", upper=False, space_before=12, space_after=6):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.keep_with_next = True
    pf.line_spacing = 1.5
    p.alignment = ALIGN[align]
    _set_run(p.add_run(text.upper() if upper else text), size=size, bold=True)
    return p


def page_break():
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.add_run().add_break(WD_BREAK.PAGE)


def add_hyperlink(paragraph, url, text):
    part = paragraph.part
    r_id = part.relate_to(url, RT.HYPERLINK, is_external=True)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    rf = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(attr), FNT)
    rpr.append(rf)
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0000FF")
    rpr.append(color)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rpr.append(u)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(BASE * 2))
    rpr.append(sz)
    new_run.append(rpr)
    t = OxmlElement("w:t")
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def figure(path, caption, width_cm=15.5):
    figure.n += 1
    p = doc.add_paragraph()
    p.alignment = ALIGN["center"]
    pf = p.paragraph_format
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(6)
    pf.space_after = Pt(2)
    pf.line_spacing = 1.0
    pf.keep_with_next = True
    img = Path(path)
    if not img.exists():
        raise FileNotFoundError(img)
    p.add_run().add_picture(str(img), width=Cm(width_cm))

    c = doc.add_paragraph()
    c.alignment = ALIGN["center"]
    cf = c.paragraph_format
    cf.first_line_indent = Cm(0)
    cf.space_before = Pt(0)
    cf.space_after = Pt(6)
    cf.line_spacing = 1.0
    cf.keep_together = True
    _set_run(c.add_run("Рисунок %d – %s" % (figure.n, caption)), size=BASE)
    return c


figure.n = 0


def title_center(text, bold=False, size=BASE, space_before=0, space_after=0):
    p = doc.add_paragraph()
    p.alignment = ALIGN["center"]
    pf = p.paragraph_format
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.0
    _set_run(p.add_run(text), size=size, bold=bold)
    return p


def title_left(text, bold=False, size=BASE, space_before=0, space_after=0):
    p = doc.add_paragraph()
    p.alignment = ALIGN["left"]
    pf = p.paragraph_format
    pf.first_line_indent = Cm(0)
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.0
    _set_run(p.add_run(text), size=size, bold=bold)
    return p


def _no_borders(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:%s" % edge)
        el.set(qn("w:val"), "none")
        el.set(qn("w:sz"), "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        borders.append(el)
    tblPr.append(borders)


def _bottom_border(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "0")
    bottom.set(qn("w:color"), "000000")
    tcBorders.append(bottom)
    tcPr.append(tcBorders)


def signature_block(role, role_label, name, name_label, middle=""):
    t = doc.add_table(rows=2, cols=3)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    _no_borders(t)
    spacing = OxmlElement("w:tblCellSpacing")
    spacing.set(qn("w:w"), "68")
    spacing.set(qn("w:type"), "dxa")
    t._tbl.tblPr.append(spacing)
    widths = [Cm(6.3), Cm(4.7), Cm(4.9)]
    for i, w in enumerate(widths):
        t.columns[i].width = w
        for row in t.rows:
            row.cells[i].width = w

    row1, row2 = t.rows[0], t.rows[1]
    row1.height = Cm(0.8)
    row2.height = Cm(0.45)
    for cell in row1.cells:
        cell.vertical_alignment = WD_ALIGN_VERTICAL.BOTTOM
        _bottom_border(cell)
    for cell in row2.cells:
        cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP

    def cell_par(cell, text, align, size=BASE, bold=False):
        p = cell.paragraphs[0]
        p.alignment = ALIGN[align]
        pf = p.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = 1.0
        _set_run(p.add_run(text), size=size, bold=bold)

    cell_par(row1.cells[0], role, "left")
    cell_par(row1.cells[1], middle, "center")
    cell_par(row1.cells[2], name, "right")
    cell_par(row2.cells[0], role_label, "center", size=9)
    cell_par(row2.cells[1], "подпись, дата", "center", size=9)
    cell_par(row2.cells[2], name_label, "center", size=9)


# =====================================================================
# ТИТУЛЬНЫЙ ЛИСТ
# =====================================================================
title_center("ГУАП", space_after=6)
title_center("КАФЕДРА № 4Ц", space_after=60)

title_left("ОТЧЕТ")
title_left("ЗАЩИЩЕН С ОЦЕНКОЙ")
title_left("ПРЕПОДАВАТЕЛЬ", space_after=4)
signature_block("ассистент", "должность, уч. степень, звание", "И. А. Маханов", "инициалы, фамилия")

title_center("", space_after=45)
title_center("ОТЧЕТ О ЛАБОРАТОРНОЙ РАБОТЕ №5", size=14, space_after=12)
title_center("ОРГАНИЗАЦИЯ РЕПОЗИТОРИЯ В СИСТЕМЕ УПРАВЛЕНИЯ", bold=True, size=14)
title_center("ВЕРСИЯМИ GIT", bold=True, size=14, space_after=18)
title_center("по курсу: Информатика", space_after=80)

title_left("РАБОТУ ВЫПОЛНИЛ")
title_left("СТУДЕНТ гр. №", space_after=4)
signature_block("", "", "Кислов К. Е.", "инициалы, фамилия", middle="4616")

title_center("", space_before=150)
title_center("Санкт-Петербург 2026")
page_break()

# =====================================================================
# ОСНОВНАЯ ЧАСТЬ
# =====================================================================
H("ЛАБОРАТОРНАЯ РАБОТА № 5.", space_before=0, space_after=6)
P([("Цель работы: ", True),
   ("получение практических навыков работы с распределённой системой управления версиями Git и сервисом для хранения, совместной работы и управления кодом GitHub.", False)])

P([("Постановка задачи", True)], space_before=6)
P("Для достижения цели были решены следующие задачи: создание публичного репозитория проекта на GitHub; разработка трёх ветвей проекта и объединение одной из них с основной ветвью; выполнение форка внешнего репозитория; выполнение индивидуального проекта — доработка сайта GreenGlow, созданного в лабораторной работе №4, с помощью AI-агента и публикация сайта через GitHub Pages.")

P([("Выполнение общих упражнений", True)], space_before=6)
P("На аккаунте GitHub (knaT43-T) создан публичный репозиторий greenglow-lr5. В основную ветвь main загружены файлы сайта, изображения, документация и файл README.md с описанием проекта. Репозиторий доступен по адресу https://github.com/knaT43-T/greenglow-lr5. Профиль GitHub показан на рисунке 1.")
figure(IMG / "01_github_profile.png", "Профиль GitHub с репозиторием greenglow-lr5 и форком pytorch")

P("Главная страница репозитория показана на рисунке 2. В ней видны ветка main, количество ветвей, список файлов и README с описанием проекта.")
figure(IMG / "02_repo_main.png", "Главная страница публичного репозитория greenglow-lr5")

P("В проекте созданы три ветви: main, feature/add-images и fix/remove-emoji. Ветвь feature/add-images предназначена для добавления изображений, ветвь fix/remove-emoji — для альтернативного оформления без эмодзи. Каждое изменение фиксировалось отдельным коммитом с комментарием. Список ветвей показан на рисунке 3.")
figure(IMG / "03_repo_branches.png", "Три ветви проекта GreenGlow на GitHub")

P("Ветвь feature/add-images создана от main. В ней агент добавил три локальных изображения товаров и обновил разметку каталога. Коммиты ветви показаны на рисунке 4.")
figure(IMG / "04_branch_feature_add_images.png", "Ветвь feature/add-images с коммитами добавления изображений")

P("После проверки ветвь объединена с main через Pull Request №1 (Рисунок 5). Ветвь после слияния не удалена: это позволяет показать её в отчёте и при необходимости вернуться к изменениям.")
figure(IMG / "07_pull_request_1.png", "Pull Request №1: объединение ветви feature/add-images с main")

P("Также выполнено копирование (форк) внешнего репозитория с полезными библиотеками — pytorch/pytorch (Рисунок 6). Ссылка на репозиторий упражнений: https://github.com/knaT43-T/greenglow-lr5.")
figure(IMG / "06_fork_pytorch.png", "Форк внешнего репозитория pytorch/pytorch")

P("История коммитов основной ветви показана на рисунке 7. В ней видны начальный коммит, коммиты с изображениями и merge commit 9c7655f.")
figure(IMG / "08_commits_main.png", "История коммитов основной ветви main")

page_break()

P([("Выполнение индивидуального проекта", True)], space_before=0)
P("Индивидуальный проект выполнен на основе сайта-лендинга магазина натуральной косметики GreenGlow, созданного в лабораторной работе №4. Проект опубликован в публичном репозитории: https://github.com/knaT43-T/greenglow-lr5.")
P("В ходе лабораторной работы сайт восстановлен в рабочей папке проекта, после чего опубликован в репозитории на GitHub. Исходное состояние сайта содержало текстовые заглушки вместо изображений товаров (Рисунок 8).")
figure(IMG / "before_hero.png", "Сайт GreenGlow до добавления изображений")

P("Доработка сайта выполнялась с помощью AI-агента (OpenCode). Агенту ставились задачи, после выполнения которых изменения фиксировались в отдельных ветвях проекта. Промт и описание изменений сохранены в docs/agent_prompt.md и docs/agent_changes.md.")

P([("Задача 1 для агента: ", True),
   ("добавить в первые три карточки каталога локальные изображения из рабочей папки — photo1.jpg, photo2.jpg и photo3.jpg. Агент заменил текстовые заглушки на теги img, добавил alt, width, height, loading=\"lazy\", decoding=\"async\" и CSS object-fit: cover. Изменения выполнены в ветви feature/add-images. После слияния каталог выглядит так, как показано на рисунке 9.", False)])
figure(IMG / "after_catalog.png", "Каталог товаров после добавления трёх локальных изображений", width_cm=14.5)

P("Изображения созданы агентом в рабочей папке программно с помощью Python и Pillow: встроенный генератор изображений вернул ошибку Access denied by security policy. Скрипт сохранён в docs/tools/make_product_images.py. Главный экран сайта после добавления изображений показан на рисунке 10. Изображения не нарушили адаптивную сетку: на десктопе сохраняются три колонки, на планшете — две, на мобильном — одна.")
figure(IMG / "after_hero.png", "Главный экран сайта после доработки")

P([("Задача 2 для агента: ", True),
   ("подготовить альтернативный вариант оформления без эмодзи. В ветви fix/remove-emoji эмодзи в логотипе заменены на CSS-знак листа, а в блоке преимуществ — на текстовые маркеры «100%», «ЭКО», «CF». Ветвь не слита с main и оставлена для сравнения (Рисунок 11).", False)])
figure(IMG / "fix_remove_emoji_benefits.png", "Блок преимуществ в ветви fix/remove-emoji")

P([("Задача 3: ", True),
   ("опубликовать готовый сайт через GitHub Pages. Публикация включена из ветви main, папка — корень репозитория. Сборка прошла в workflow pages-build-deployment (Рисунок 12); в журнале сборки указан адрес сайта (Рисунок 13).", False)])
figure(IMG / "11_github_actions_crop.png", "Успешная сборка GitHub Pages в Actions")
figure(IMG / "12_pages_build_run.png", "Детали сборки и адрес опубликованного сайта")

P("Готовый сайт доступен по адресу https://knat43-t.github.io/greenglow-lr5/ (Рисунок 14). Мобильная версия опубликованного сайта показана на рисунке 15.")
P("Публикация настроена для ветви main и корневой папки репозитория: при каждом коммите workflow pages-build-deployment автоматически пересобирает сайт. Сборка завершилась успешно: статус запуска — Success, длительность — 56 с. Доступность сайта проверена запросом к опубликованному адресу: сервер вернул код 200, а сборка GitHub Pages имеет статус built.")

page_break()
figure(IMG / "09_pages_site.png", "Опубликованный сайт GreenGlow на GitHub Pages", width_cm=14.5)
figure(IMG / "10_pages_site_mobile.png", "Мобильная версия опубликованного сайта", width_cm=6.4)

page_break()

H("ВЫВОД", space_before=0, space_after=6)
P("Целью лабораторной работы было получение практических навыков работы с распределённой системой управления версиями Git и сервисом GitHub. Система управления версиями предназначена для хранения истории изменений проекта: она позволяет фиксировать каждое изменение, возвращаться к предыдущим версиям, вести параллельную разработку в отдельных ветвях и объединять результаты работы. Эти возможности составляют основу командной разработки программных проектов.")
P("В ходе работы решены все поставленные задачи: создан публичный репозиторий greenglow-lr5; разработаны три ветви main, feature/add-images и fix/remove-emoji; выполнено объединение ветви feature/add-images с основной ветвью через Pull Request №1; создан форк внешнего репозитория pytorch/pytorch.")
P("Индивидуальный проект — доработка сайта GreenGlow из лабораторной работы №4 — выполнен с применением AI-агента: агент добавил три локальных изображения товаров, изменил HTML и CSS, подготовил документацию и diff. Все изменения выполнялись в отдельной ветви и были объединены с основной ветвью через Pull Request, что позволило сохранить историю разработки. Итоговый сайт опубликован через GitHub Pages и доступен по публичной ссылке.")
P("В результате освоены практические навыки: создание репозиториев и работа с ветвями, фиксация изменений, объединение ветвей, форк внешних проектов, публикация сайтов через GitHub Pages и совместная работа с AI-агентом под контролем разработчика.")

page_break()

H("ЗАКЛЮЧЕНИЕ", space_before=0, space_after=6)
P("Подводя итог выполненной работе, необходимо зафиксировать ключевой вывод, который был практически подтверждён на каждом этапе лабораторной. Инструменты генеративного искусственного интеллекта не подменяют разработчика, а берут на себя ту часть работы, которая раньше отнимала непропорционально много времени: подготовку однотипных фрагментов разметки, добавление изображений, оформление документации и служебных файлов.")
P("Агент OpenCode восстановил каркас лендинга и внёс изменения в каталог изображений, однако ни на одном из этапов модель не принимала решений о том, каким должен быть сайт с точки зрения бизнеса, какой эмоциональный отклик он должен вызывать у посетителя и какие элементы заслуживают приоритетного внимания. Контроль качества, принятие проектных решений и определение дальнейшего направления развития сайта остаются за разработчиком.")
P("Взаимодействие с ИИ в данной работе свелось к чёткому распределению ролей: генерация и рутинные модификации выполняются моделью или агентом, а контроль качества, принятие проектных решений и определение дальнейшего направления развития сайта остаются за разработчиком.")

page_break()

H("СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ", space_before=0, space_after=6)
sources = [
    "Методические указания к лабораторной работе №5 по дисциплине «Информатика». — 42 с.",
    "Отчёт по лабораторной работе №4 «Разработка одностраничного сайта GreenGlow». — 21 с.",
    "ГОСТ 7.32-2017. СИБИД. Отчёт о научно-исследовательской работе. Структура и правила оформления. — URL: https://docs.cntd.ru/document/1200162161 (дата обращения: 01.11.2026).",
    "ГОСТ 2.105-2019. ЕСКД. Общие требования к текстовым документам. — URL: https://docs.cntd.ru/document/1200162162 (дата обращения: 01.11.2026).",
    "Git Documentation. — URL: https://git-scm.com/doc (дата обращения: 01.11.2026).",
    "GitHub Docs. About forks. — URL: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks (дата обращения: 01.11.2026).",
    "GitHub Docs. GitHub Pages. — URL: https://docs.github.com/en/pages (дата обращения: 01.11.2026).",
    "GitHub CLI Manual. — URL: https://cli.github.com/manual/ (дата обращения: 01.11.2026).",
    "OpenCode documentation. — URL: https://opencode.ai/docs/ (дата обращения: 01.11.2026).",
    "Python 3.10 documentation. — URL: https://docs.python.org/3.10/ (дата обращения: 01.11.2026).",
]
for i, src in enumerate(sources, 1):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.first_line_indent = Cm(-0.7)
    pf.left_indent = Cm(1.3)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.5
    pf.tab_stops.add_tab_stop(Cm(1.3))
    p.alignment = ALIGN["justify"]
    _set_run(p.add_run("%d.\t" % i))
    # Разделяем текст и URL, чтобы ссылка была кликабельной.
    if "URL: " in src:
        before, after = src.split("URL: ", 1)
        _set_run(p.add_run(before))
        url, tail = after.split(" ", 1) if " " in after else (after, "")
        add_hyperlink(p, url, url)
        if tail:
            _set_run(p.add_run(" " + tail))
    else:
        _set_run(p.add_run(src))

# ------------------------------------------------------------------- сохранение
OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUT)
print("SAVED:", OUT)
print("FIGURES:", figure.n)
