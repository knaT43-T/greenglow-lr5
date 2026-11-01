# Лог выполнения лабораторной работы №5

**Проект:** GreenGlow — магазин натуральной косметики  
**Дисциплина:** Информатика  
**Студент:** Кислов К. Е., группа 4616  
**Логин GitHub:** knaT43-T  
**Дата выполнения:** 31.10.2026 — 01.11.2026  
**Рабочая папка:** `C:\Users\Kira\Downloads\project`

---

## Шаг 0. Проверка окружения

| Инструмент | Результат |
|---|---|
| `git --version` | `git version 2.55.0.windows.5` |
| `gh --version` | `gh version 2.102.0 (2026-09-30)` |
| `curl.exe --version` | `curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.2.13 WinIDN WinLDAP` |
| `python --version` | `Python 3.10.6` |
| `node --version` | `v20.18.1` |
| GitHub CLI авторизация | `gh auth status` — вход выполнен под `knaT43-T`, протокол HTTPS, scopes: `gist`, `read:org`, `repo`, `workflow` |
| Git user.name | `knaT43-T` |
| Git user.email | `146657699+knaT43-T@users.noreply.github.com` |
| Браузер для скриншотов | Microsoft Edge `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` |
| Python-библиотеки | Pillow 12.1.1, python-docx, PyMuPDF — доступны |

**Исходная структура рабочей папки:** только два PDF-файла:
- `LR5Informatika_итог.pdf` — методические указания к ЛР №5 (42 страницы);
- `ЛР4КисловКЕ4616.pdf` — отчёт по ЛР №4 (21 страница).

Сайт из ЛР №4 в рабочей папке отсутствовал, поэтому лендинг GreenGlow восстановлен по контексту отчёта ЛР №4 и методических указаний. Исходные PDF и извлечённый текст перемещены в служебную папку `source_materials/`, которая исключена из Git через `.gitignore`.

**Прочитанные материалы:**
- методические указания ЛР №5: цель, задачи, критерии оценивания (15 баллов), требования к отчёту, раздел 5 «Выполнение индивидуального задания»;
- отчёт ЛР №4: описание проекта GreenGlow, структура из 8 блоков, палитра, промт, ограничения (один `index.html`, без JavaScript, без внешних шрифтов и изображений).

---

## Шаг 1. Восстановление сайта и первый коммит

1. Создан `index.html` в корне рабочей папки — одностраничный лендинг GreenGlow.
2. Реализованы 8 блоков: шапка с навигацией и CSS-бургер-меню, hero, «О бренде», преимущества, каталог из 6 товаров, отзывы, контакты и доставка, footer.
3. Использована палитра ЛР №4: `#F9F6F0`, `#8A9A86`, `#2C3E2D`, `#FFFFFF`.
4. Сайт адаптивен (3 → 2 → 1 колонка), без JavaScript, без внешних шрифтов и библиотек.
5. В логотипе и блоке преимуществ оставлены эмодзи `🌿`, `♻️`, `🐇` — они понадобятся для отдельной ветки `fix/remove-emoji`.
6. В первых трёх карточках каталога используются текстовые заглушки изображений — состояние «до» добавления фотографий.
7. Созданы `README.md` и `.gitignore`.
8. Создана служебная папка `docs/`.

**Проверка:** локальный скриншот `report_screens/local_before_full.png` (Edge headless, 1440×3000) — сайт корректно отображается, сетка каталога не сломана.

---

## Шаг 2. Инициализация Git и публикация на GitHub

1. В корне рабочей папки выполнена инициализация репозитория:
   ```bash
   git init
   git branch -M main
   ```
2. В первый коммит включены сайт, README, `.gitignore`, служебная папка `docs/` и скриншоты состояния «до». Изображения `assets/img/photo*.jpg` намеренно оставлены вне первого коммита — они добавляются в ветке `feature/add-images`, чтобы изменение было видно в истории.
3. Первый коммит:
   ```bash
   git commit -m "Initial commit: restore GreenGlow landing from LR4"
   ```
   Хеш: `c16204f` (после очистки дубликатов скриншотов).
4. Публичный репозиторий создан через GitHub CLI и связан с рабочей папкой:
   ```bash
   gh repo create greenglow-lr5 --public --source=. --remote=origin --push
   ```
5. **URL репозитория:** https://github.com/knaT43-T/greenglow-lr5
6. Проверка: `git remote -v` — `origin` указывает на `https://github.com/knaT43-T/greenglow-lr5.git`; ветка `main` отслеживает `origin/main`.

---

## Шаг 3. Форк внешнего репозитория

1. Проверена авторизация GitHub CLI: `gh auth status` — активный аккаунт `knaT43-T`, scopes включают `repo`.
2. Проверено, что форка `knaT43-T/pytorch` ещё нет.
3. Выполнен форк внешнего проекта:
   ```bash
   gh repo fork pytorch/pytorch --clone=false
   ```
4. **URL форка:** https://github.com/knaT43-T/pytorch
5. Проверка через API: `isFork = true`, исходный репозиторий — `pytorch/pytorch`.
6. Подробное описание — в `docs/fork.md`.

---

## Шаг 4. Ветка `feature/add-images` и добавление изображений

1. От актуальной ветки `main` создана ветка:
   ```bash
   git checkout -b feature/add-images
   ```
2. Подготовлена папка `assets/img` с тремя локальными изображениями:
   - `photo1.jpg` — увлажняющий крем с алоэ, 1200×900, JPEG;
   - `photo2.jpg` — сыворотка с витамином C, 1200×900, JPEG;
   - `photo3.jpg` — гидрофильное масло, 1200×900, JPEG.
3. Встроенный сервис генерации изображений вернул ошибку `Access denied by security policy` для всех запросов. В качестве резервного варианта агент создал изображения программно с помощью Python/Pillow. Скрипт сохранён в `docs/tools/make_product_images.py`; изображения имеют единый стиль и палитру сайта.
4. В `index.html` в первых трёх карточках каталога заменены текстовые заглушки на `<img>` с относительными путями:
   - `assets/img/photo1.jpg`, alt «Увлажняющий крем с алоэ»;
   - `assets/img/photo2.jpg`, alt «Сыворотка с витамином С»;
   - `assets/img/photo3.jpg`, alt «Гидрофильное масло».
5. Добавлен CSS:
   ```css
   .product-img img {
     position: absolute;
     inset: 0;
     width: 100%;
     height: 100%;
     object-fit: cover;
     display: block;
   }
   ```
6. Убраны два декоративных «плавающих» блока в hero-визуале, которые перекрывали подпись товара на карточке; это улучшило читаемость первого экрана.
7. Сняты скриншоты «после»: `after_hero.png`, `after_full.png`, `after_catalog.png`, `after_catalog_grid.png`, `after_mobile.png`, `after_mobile_full.png`.
8. Подготовлены `docs/agent_changes.md`, `docs/images.md`, `docs/before_after.md`.
9. Изменения закоммичены и ветка отправлена на GitHub:
   ```bash
   git add .
   git commit -m "Add three local images to GreenGlow catalog via AI agent"
   git push -u origin feature/add-images
   ```
   Хеш коммита: `a5a936e`.

---

## Шаг 5. Pull Request и слияние с `main`

*(раздел заполняется по мере выполнения)*

---

## Шаг 6. Ветка `fix/remove-emoji`

*(раздел заполняется по мере выполнения)*

---

## Шаг 7. GitHub Pages

*(раздел заполняется по мере выполнения)*

---

## Шаг 8. Отчётные материалы и скриншоты

*(раздел заполняется по мере выполнения)*

---

## Шаг 9. Итоговая проверка

*(раздел заполняется по мере выполнения)*
