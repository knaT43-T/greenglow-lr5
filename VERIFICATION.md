# Итоговая проверка выполнения лабораторной работы №5

**Проект:** GreenGlow  
**Студент:** Кислов К. Е., группа 4616  
**Логин GitHub:** knaT43-T  
**Дата проверки:** 01.11.2026  
**Основная ветвь:** `main`  
**Рабочая папка:** `C:\Users\Kira\Downloads\project`

## Краткий итог

**Все обязательные требования выполнены.** Публичный репозиторий создан, три ветви опубликованы, ветвь с изображениями слита с `main`, форк внешнего проекта создан, три локальных изображения добавлены агентом, сайт опубликован через GitHub Pages и доступен по HTTP 200. Блокеров нет, `BLOCKERS.md` не требуется.

## Таблица требований

| № | Требование | Результат | Доказательство |
|---|---|---|---|
| 1 | Публичный репозиторий на GitHub | выполнено | `https://github.com/knaT43-T/greenglow-lr5`, API `isPrivate: false` |
| 2 | Не менее трёх ветвей | выполнено | `main`, `feature/add-images`, `fix/remove-emoji`; API `/branches` возвращает 3 ветви |
| 3 | Слияние ветви с `main` | выполнено | PR #1 `MERGED`, merge commit `9c7655f`, `git merge-base --is-ancestor` = 0 |
| 4 | Ветвь после слияния не удалена | выполнено | `feature/add-images` есть локально и на `origin` |
| 5 | Форк внешнего репозитория | выполнено | `knaT43-T/pytorch`, API `fork: true`, parent `pytorch/pytorch` |
| 6 | Не менее трёх локальных изображений | выполнено | `assets/img/photo1.jpg`, `photo2.jpg`, `photo3.jpg`, 1200 × 900, JPEG |
| 7 | Изображения добавлены агентом | выполнено | `docs/agent_changes.md`, `docs/agent_prompt.md`, `docs/diff_add_images.diff` |
| 8 | Изображения используются на сайте | выполнено | 3 тега `<img>` с относительными путями `assets/img/...` |
| 9 | GitHub Pages | выполнено | `https://knat43-t.github.io/greenglow-lr5/`, HTTP 200, build `built` |
| 10 | Сайт из ветви `main`, корень репозитория | выполнено | API Pages: `source.branch = main`, `source.path = /` |
| 11 | Текст отчёта | выполнено | `REPORT_CONTENT.md` |
| 12 | Чек-лист скриншотов | выполнено | `SCREENSHOT_CHECKLIST.md` |
| 13 | Материалы скриншотов | выполнено | 26 PNG в `report_screens/` |
| 14 | Документация выполнения | выполнено | `docs/execution_log.md` и тематические файлы в `docs/` |
| 15 | Кодировка текстовых файлов UTF-8 | выполнено | проверка Python: все `.md`, `.txt`, `.html`, `.css`, `.py` читаются как UTF-8 |
| 16 | Отсутствие разрушительных операций | выполнено | ветви не удалялись, история не переписывалась, `source_materials/` исключена через `.gitignore` |

## Проверка Git

### Состояние рабочей папки

```powershell
git status --short
```

Ожидаемый результат после финального коммита: пустой вывод (рабочая папка чистая).

### Ветви

```powershell
git branch -a
```

```text
  feature/add-images
  fix/remove-emoji
* main
  remotes/origin/feature/add-images
  remotes/origin/fix/remove-emoji
  remotes/origin/main
```

### Удалённый репозиторий

```powershell
git remote -v
```

```text
origin  https://github.com/knaT43-T/greenglow-lr5.git (fetch)
origin  https://github.com/knaT43-T/greenglow-lr5.git (push)
```

### История коммитов

```powershell
git log --oneline --graph --all --decorate -12
```

```text
* 8753b68 (HEAD -> main, origin/main) Add branch description and document PR merge
| * d196168 (origin/fix/remove-emoji, fix/remove-emoji) Remove emoji noise and improve minimal visual style
|/
*   9c7655f Merge pull request #1 from knaT43-T/feature/add-images
|\
| * 1301295 (origin/feature/add-images, feature/add-images) Add image diff and update agent change notes
| * a5a936e Add three local images to GreenGlow catalog via AI agent
|/
* b876b97 Document GitHub repository setup and external fork
* c16204f Initial commit: restore GreenGlow landing from LR4
```

После добавления отчётных материалов появится ещё один коммит в `main`; хеш можно получить командой:

```powershell
git log -1 --oneline
```

### Проверка слияния

```powershell
git merge-base --is-ancestor feature/add-images main
$LASTEXITCODE
```

```text
0
```

`0` означает, что ветвь `feature/add-images` является предком `main`, то есть её изменения вошли в основную ветвь.

```powershell
git merge-base --is-ancestor fix/remove-emoji main
$LASTEXITCODE
```

```text
1
```

`1` означает, что ветвь `fix/remove-emoji` **не** является предком `main`, то есть она не слита. Это ожидаемо: ветвь оставлена как альтернативный вариант.

## Проверка GitHub API

### Репозиторий

```powershell
gh repo view knaT43-T/greenglow-lr5 `
  --json name,url,isPrivate,defaultBranchRef `
  --jq '{name,url,isPrivate,default:.defaultBranchRef.name}'
```

```json
{"default":"main","isPrivate":false,"name":"greenglow-lr5","url":"https://github.com/knaT43-T/greenglow-lr5"}
```

### Ветви

```powershell
gh api repos/knaT43-T/greenglow-lr5/branches --jq '.[].name'
```

```text
feature/add-images
fix/remove-emoji
main
```

### Pull Request

```powershell
gh pr view 1 --repo knaT43-T/greenglow-lr5 `
  --json number,title,state,mergedAt,mergeCommit,headRefName,baseRefName
```

```json
{
  "base": "main",
  "head": "feature/add-images",
  "mergeCommit": "9c7655f15bff6e93904247135b76621c93807387",
  "mergedAt": "2026-11-01T11:57:47Z",
  "number": 1,
  "state": "MERGED",
  "title": "Add three images to GreenGlow catalog"
}
```

### Форк

```powershell
gh api repos/knaT43-T/pytorch `
  --jq '{fork,parent:.parent.full_name,source:.source.full_name}'
```

```json
{"fork":true,"parent":"pytorch/pytorch","source":"pytorch/pytorch"}
```

### GitHub Pages

```powershell
gh api repos/knaT43-T/greenglow-lr5/pages `
  --jq '{html_url,status,build_type,source,public,https_enforced}'
```

```json
{
  "build_type": "legacy",
  "html_url": "https://knat43-t.github.io/greenglow-lr5/",
  "https_enforced": true,
  "public": true,
  "source": {"branch": "main", "path": "/"},
  "status": "built"
}
```

```powershell
gh api repos/knaT43-T/greenglow-lr5/pages/builds/latest `
  --jq '{status,created_at,updated_at,commit,url}'
```

```json
{
  "commit": "8753b68e86c035348ebabcaba35651bfc380e25f",
  "created_at": "2026-11-01T12:00:39Z",
  "status": "built",
  "updated_at": "2026-11-01T12:01:27Z",
  "url": "https://api.github.com/repos/knaT43-T/greenglow-lr5/pages/builds/1332167131"
}
```

Это сборка, которая впервые опубликовала сайт. После добавления отчётных материалов GitHub Pages выполняет повторные сборки из последующих коммитов; содержимое страницы при этом не меняется, HTTP 200 сохраняется.

## Проверка сайта

### HTTP

```powershell
curl.exe -L --max-time 30 -A "Mozilla/5.0" `
  -o NUL -w "HTTP %{http_code} size %{size_download}`n" `
  "https://knat43-t.github.io/greenglow-lr5/"
```

```text
HTTP 200 size 51896
```

### Содержимое страницы

Проверка в headless-браузере Edge:

| Параметр | Значение |
|---|---|
| HTTP-статус | 200 |
| Заголовок | `GreenGlow — красота, созданная природой` |
| Язык | `ru` |
| Viewport | `width=device-width, initial-scale=1.0` |
| Секций `<section>` | 6 |
| Шапка и подвал | есть (итого 8 смысловых блоков) |
| Тегов `<script>` | 0 |
| Внешних таблиц стилей | 0 |
| Локальных изображений | 3 |
| Изображения загружаются | да, `naturalWidth = 1200` у всех трёх |
| Ширина документа на мобильном | 390 px |
| `scrollWidth` на мобильном | 390 px (горизонтальной прокрутки нет) |

### Изображения

```powershell
python -c "from PIL import Image; from pathlib import Path; [print(p.name, Image.open(p).format, Image.open(p).size, p.stat().st_size) for p in sorted(Path('assets/img').glob('*.jpg'))]"
```

```text
photo1.jpg JPEG (1200, 900) 62193
photo2.jpg JPEG (1200, 900) 73385
photo3.jpg JPEG (1200, 900) 61170
```

### HTML

```text
bytes 51896
sections 6
img_tags 3
scripts 0
external_refs 0
media_queries 5
has_viewport True
lang_ru True
charset_utf8 True
local_img_refs 3
```

## Проверка файлов отчёта

| Файл | Назначение | Статус |
|---|---|---|
| `REPORT_CONTENT.md` | готовый текст отчёта | есть |
| `SCREENSHOT_CHECKLIST.md` | чек-лист скриншотов | есть |
| `VERIFICATION.md` | итоговая проверка | есть |
| `docs/execution_log.md` | лог выполнения | есть |
| `docs/agent_prompt.md` | промт агента | есть |
| `docs/agent_changes.md` | изменения агента | есть |
| `docs/branch_description.md` | описание ветвей | есть |
| `docs/fork.md` | описание форка | есть |
| `docs/github_pages.md` | описание публикации | есть |
| `docs/images.md` | описание изображений | есть |
| `docs/report_materials.md` | материалы для отчёта | есть |
| `docs/pr_body.md` | текст описания Pull Request | есть |
| `docs/before_after.md` | состояние до/после | есть |
| `docs/diff_add_images.diff` | diff изменений | есть |
| `docs/tools/make_product_images.py` | скрипт генерации изображений | есть |

## Проверка кодировки

Все текстовые файлы проекта сохранены в UTF-8. Проверка выполняется чтением с `encoding='utf-8'`; ошибок декодирования нет. HTML содержит `<meta charset="UTF-8">`.

## Ограничения

1. Страница `Settings → Pages` требует авторизации. Автоматический headless-браузер не имеет сессии GitHub, поэтому её скриншот не снят. Настройка подтверждена API, успешным run и публичным сайтом. При необходимости скриншот можно сделать вручную по инструкции в `SCREENSHOT_CHECKLIST.md`.
2. Встроенный генератор изображений вернул `Access denied by security policy`, поэтому изображения созданы программно Python/Pillow. Это не блокирует требование: файлы физически находятся в рабочей папке, добавлены агентом и используются на сайте.
3. Первый запрос к GitHub Pages вернул 404, пока шла сборка. После завершения сборки сайт отдаёт 200; в отчёте зафиксирован рабочий адрес.

## Итоговый вердикт

Лабораторная работа №5 выполнена в полном объёме. Все обязательные критерии подтверждены командами Git, ответами GitHub API, скриншотами и проверкой опубликованного сайта. Работа готова к сдаче.
