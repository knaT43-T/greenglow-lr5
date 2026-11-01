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

**Проверка:** локальные скриншоты `report_screens/before_hero.png`, `before_full.png` (Edge headless, 1440×5640), `before_mobile.png` (390×844) — сайт корректно отображается, сетка каталога не сломана, горизонтальной прокрутки нет.

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

1. Ветка `feature/add-images` отправлена на GitHub:
   ```bash
   git push -u origin feature/add-images
   ```
2. Создан Pull Request №1:
   - URL: https://github.com/knaT43-T/greenglow-lr5/pull/1
   - Заголовок: «Add three images to GreenGlow catalog»
   - База: `main`, источник: `feature/add-images`
   - Текст описания сохранён в `docs/pr_body.md`
3. Выполнено слияние через GitHub CLI:
   ```bash
   gh pr merge 1 --merge
   ```
4. Результат: PR №1 в состоянии `MERGED`, дата слияния `2026-11-01T11:57:47Z`, merge commit `9c7655f`. Ветка `feature/add-images` **не удалена** после слияния.
5. Локальная `main` обновлена:
   ```bash
   git checkout main
   git pull origin main
   ```
   Обновление прошло fast-forward до `9c7655f`; в `main` появились изображения, документация и скриншоты.

---

## Шаг 6. Ветка `fix/remove-emoji`

1. От актуальной `main` создана ветка:
   ```bash
   git checkout -b fix/remove-emoji
   ```
2. Выполнены изменения дизайна:
   - эмодзи `🌿` в логотипе заменён на CSS-знак листа `.leaf-mark` (в шапке и подвале);
   - эмодзи `🌿`, `♻️`, `🐇` в блоке преимуществ заменены на строгие текстовые маркеры `100%`, `ЭКО`, `CF`;
   - декоративный символ `✿` в строке ценностей заменён на нейтральную точку;
   - добавлены `docs/branch_notes.txt` и `docs/branch_description.md`.
3. Сняты скриншоты варианта без эмодзи:
   - `report_screens/fix_remove_emoji_hero.png`;
   - `report_screens/fix_remove_emoji_full.png`;
   - `report_screens/fix_remove_emoji_benefits.png`.
4. Коммит и отправка:
   ```bash
   git add index.html docs/branch_notes.txt docs/branch_description.md report_screens/fix_remove_emoji_*.png
   git commit -m "Remove emoji noise and improve minimal visual style"
   git push -u origin fix/remove-emoji
   ```
   Хеш коммита: `d196168`.
5. Ветка **не слита** с `main`: она остаётся отдельной альтернативной линией разработки для демонстрации трёх ветвей. Файл `docs/branch_description.md` скопирован в `main` отдельным коммитом, чтобы описание ветвей было доступно в основной ветке.

---

## Шаг 7. GitHub Pages

1. Проверено, что GitHub Pages ещё не включён:
   ```bash
   gh api repos/knaT43-T/greenglow-lr5/pages
   ```
   Ответ: `HTTP 404 Not Found`.
2. Публикация включена через GitHub API:
   ```powershell
   '{"source":{"branch":"main","path":"/"}}' | Out-File -Encoding ascii source_materials\pages.json
   gh api -X POST repos/knaT43-T/greenglow-lr5/pages --input source_materials/pages.json
   ```
   Ответ API: `html_url = https://knat43-t.github.io/greenglow-lr5/`, `build_type = legacy`, `source.branch = main`, `source.path = /`, `https_enforced = true`, `public = true`.
3. Первый запрос к сайту вернул HTTP 404: сборка ещё шла. Через несколько минут сборка завершилась.
4. Проверка сборки:
   ```bash
   gh api repos/knaT43-T/greenglow-lr5/pages/builds/latest `
     --jq '{status,created_at,updated_at,commit,url}'
   ```
   Результат: `status = built`, сборка создана `2026-11-01T12:00:39Z`, завершена `2026-11-01T12:01:27Z`, коммит `8753b68`.
5. Проверка сайта:
   ```powershell
   curl.exe -L --max-time 30 -A "Mozilla/5.0" `
     -o NUL -w "HTTP %{http_code} size %{size_download}`n" `
     "https://knat43-t.github.io/greenglow-lr5/"
   ```
   Результат: `HTTP 200 size 51896`.
6. Сайт открыт в headless-браузере Edge. Заголовок — «GreenGlow — красота, созданная природой», все три изображения загружены (`naturalWidth = 1200`), на мобильном `scrollWidth = clientWidth = 390`.
7. Сборка прошла в workflow `pages-build-deployment` (run #1, 56 секунд): jobs `build` (23 с), `report-build-status` (3 с), `deploy` (21 с). Адрес деплоя: `https://knat43-t.github.io/greenglow-lr5/`.
8. Сняты скриншоты:
   - `report_screens/11_github_actions.png` — успешный workflow;
   - `report_screens/12_pages_build_run.png` — детали run и адрес сайта;
   - `report_screens/09_pages_site.png` — опубликованный сайт, десктоп;
   - `report_screens/09_pages_site_full.png` — опубликованный сайт целиком;
   - `report_screens/10_pages_site_mobile.png` — мобильная версия.
9. Подробное описание публикации — в `docs/github_pages.md`. Страница `Settings → Pages` требует авторизации, поэтому её скриншот не снимался; настройка подтверждена API и успешным run. Инструкция для ручного скриншота — в `SCREENSHOT_CHECKLIST.md`.

---

## Шаг 8. Отчётные материалы и скриншоты

1. Сняты скриншоты публичных страниц GitHub через Playwright и Microsoft Edge (viewport 1440×900):
   - `01_github_profile.png` — профиль `knaT43-T`;
   - `02_repo_main.png` — главная страница репозитория;
   - `03_repo_branches.png` — список из трёх ветвей;
   - `04_branch_feature_add_images.png` — ветвь `feature/add-images`;
   - `05_branch_fix_remove_emoji.png` — ветвь `fix/remove-emoji`;
   - `06_fork_pytorch.png` — форк `pytorch`;
   - `07_pull_request_1.png` — PR #1 со статусом `Merged`;
   - `08_commits_main.png` — история коммитов `main`.
2. Сняты скриншоты сайта «до» и «после»:
   - `before_hero.png`, `before_full.png`, `before_mobile.png`, `before_mobile_full.png`;
   - `after_hero.png`, `after_full.png`, `after_catalog.png`, `after_catalog_grid.png`, `after_mobile.png`, `after_mobile_full.png`.
3. Сняты скриншоты альтернативной ветви:
   - `fix_remove_emoji_hero.png`;
   - `fix_remove_emoji_full.png`;
   - `fix_remove_emoji_benefits.png`.
4. Созданы документы:
   - `docs/github_pages.md` — публикация, настройки, сборка, проверки;
   - `docs/report_materials.md` — карта скриншотов и подписей;
   - `REPORT_CONTENT.md` — готовый текст отчёта;
   - `SCREENSHOT_CHECKLIST.md` — чек-лист скриншотов;
   - `VERIFICATION.md` — итоговая проверка требований.
5. Обновлены `README.md` (ссылка на сайт и материалы отчёта), `docs/execution_log.md`, `docs/agent_changes.md`, `docs/branch_description.md`.
6. Проверено соответствие подписей рисунков и файлов: рисунки 1–20 в `REPORT_CONTENT.md` совпадают с таблицей в `docs/report_materials.md` и `SCREENSHOT_CHECKLIST.md`.

---

## Шаг 9. Итоговая проверка

1. Проверено состояние Git:
   ```bash
   git status --short
   git branch -a
   git remote -v
   git log --oneline --graph --all --decorate
   ```
   Рабочая папка чистая, три локальные ветви и три ветви на `origin`, `origin` указывает на `https://github.com/knaT43-T/greenglow-lr5.git`.
2. Проверено слияние:
   ```bash
   git merge-base --is-ancestor feature/add-images main
   ```
   Код возврата `0` — ветвь слита.
   ```bash
   git merge-base --is-ancestor fix/remove-emoji main
   ```
   Код возврата `1` — ветвь не слита, оставлена как альтернативная.
3. Проверены GitHub API:
   - репозиторий публичный (`isPrivate: false`), ветка по умолчанию `main`;
   - `/branches` возвращает `feature/add-images`, `fix/remove-emoji`, `main`;
   - PR #1 в состоянии `MERGED`, merge commit `9c7655f`;
   - форк `knaT43-T/pytorch` имеет `fork: true`, parent `pytorch/pytorch`;
   - GitHub Pages: `status: built`, `source: main /`, `https_enforced: true`.
4. Проверены изображения: три файла JPEG 1200×900 в `assets/img`, все используются в HTML через относительные пути, внешних ссылок нет.
5. Проверен HTML: 6 секций + шапка + подвал (8 блоков), 3 `<img>`, 0 `<script>`, 0 внешних ссылок, 5 медиазапросов, UTF-8, `lang="ru"`, viewport.
6. Проверен опубликованный сайт: HTTP 200, заголовок корректный, изображения загружаются, мобильная версия без горизонтальной прокрутки.
7. Проверена кодировка текстовых файлов: UTF-8, ошибок декодирования нет.
8. Блокеров нет, `BLOCKERS.md` не создавался. Единственное ограничение — скриншот `Settings → Pages` требует ручной авторизации; он не обязателен, факт публикации подтверждён API, run и сайтом.
9. Итоговая проверка зафиксирована в `VERIFICATION.md`. После финального коммита рабочая папка чистая, `main` синхронизирована с `origin/main`.
