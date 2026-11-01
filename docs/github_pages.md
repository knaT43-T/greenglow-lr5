# Публикация сайта через GitHub Pages

## Итоговая ссылка

**https://knat43-t.github.io/greenglow-lr5/**

Ссылка в верхнем регистре также открывается:

**https://knaT43-T.github.io/greenglow-lr5/**

Обе ссылки ведут на один и тот же сайт; GitHub Pages использует имя пользователя в нижнем регистре.

## Параметры публикации

| Параметр | Значение |
|---|---|
| Репозиторий | [knaT43-T/greenglow-lr5](https://github.com/knaT43-T/greenglow-lr5) |
| Ветка источника | `main` |
| Папка | `/` (корень репозитория) |
| Тип сборки | `legacy` (GitHub Pages build) |
| Публичность | публичный сайт |
| HTTPS | включён принудительно (`https_enforced: true`) |
| Статус | `built` |
| Коммит сборки, опубликовавшей сайт | `8753b68e86c035348ebabcaba35651bfc380e25f` |
| Сборка создана | `2026-11-01T12:00:39Z` |
| Сборка завершена | `2026-11-01T12:01:27Z` |
| Время сборки | 56 секунд |
| Actions run | [pages build and deployment #1](https://github.com/knaT43-T/greenglow-lr5/actions/runs/41304416467) |

После добавления отчётных материалов в `main` GitHub Pages выполняет повторные сборки из последующих коммитов. Они не меняют содержимое сайта: страница по-прежнему отдаёт HTTP 200 и тот же HTML. В таблице указан коммит, который впервые опубликовал сайт.

## Как включена публикация

Публикация включена через GitHub API, без ручного входа в Settings → Pages. Это позволило агенту выполнить настройку автономно.

Команда:

```powershell
'{"source":{"branch":"main","path":"/"}}' | Out-File -Encoding ascii source_materials\pages.json
gh api -X POST repos/knaT43-T/greenglow-lr5/pages --input source_materials/pages.json
```

Ответ API:

```json
{
  "url": "https://api.github.com/repos/knaT43-T/greenglow-lr5/pages",
  "status": null,
  "cname": null,
  "custom_404": false,
  "html_url": "https://knat43-t.github.io/greenglow-lr5/",
  "build_type": "legacy",
  "source": {
    "branch": "main",
    "path": "/"
  },
  "public": true,
  "protected_domain_state": null,
  "pending_domain_unverified_at": null,
  "https_enforced": true
}
```

Сразу после включения сайт ещё не был доступен: первый запрос вернул HTTP 404, потому что сборка только началась. Через несколько минут сборка завершилась, и сайт стал отдавать HTTP 200.

## Проверка публикации

### Через API

```powershell
gh api repos/knaT43-T/greenglow-lr5/pages `
  --jq '{html_url,status,build_type,source,public,https_enforced}'
```

Результат:

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

Результат:

```json
{
  "commit": "8753b68e86c035348ebabcaba35651bfc380e25f",
  "created_at": "2026-11-01T12:00:39Z",
  "status": "built",
  "updated_at": "2026-11-01T12:01:27Z",
  "url": "https://api.github.com/repos/knaT43-T/greenglow-lr5/pages/builds/1332167131"
}
```

### Через HTTP

```powershell
curl.exe -L --max-time 30 -A "Mozilla/5.0" `
  -o NUL -w "HTTP %{http_code} size %{size_download}`n" `
  "https://knat43-t.github.io/greenglow-lr5/"
```

Результат:

```text
HTTP 200 size 51896
```

### Проверка содержимого страницы

Страница открыта в headless-браузере Microsoft Edge через Playwright. Проверено:

- HTTP-статус: `200`;
- заголовок страницы: `GreenGlow — красота, созданная природой`;
- все три изображения загружены: `assets/img/photo1.jpg`, `photo2.jpg`, `photo3.jpg`, `naturalWidth = 1200`;
- ширина документа на десктопе: `1440 px`, высота: `5625 px`;
- мобильная версия при ширине `390 px` отображается без горизонтальной прокрутки.

## Сборка GitHub Actions

Сборка прошла в workflow `pages-build-deployment`:

| Job | Статус | Время |
|---|---|---|
| `build` | успешно | 23 с |
| `report-build-status` | успешно | 3 с |
| `deploy` | успешно | 21 с |

Итоговый адрес деплоя, указанный в run: `https://knat43-t.github.io/greenglow-lr5/`.

## Скриншоты

| Файл | Что показано |
|---|---|
| `report_screens/11_github_actions.png` | список Actions, workflow `pages build and deployment` завершён успешно |
| `report_screens/12_pages_build_run.png` | детали run: jobs `build`, `report-build-status`, `deploy`, адрес опубликованного сайта |
| `report_screens/09_pages_site.png` | опубликованный сайт, десктоп, первый экран |
| `report_screens/09_pages_site_full.png` | опубликованный сайт целиком, десктоп |
| `report_screens/10_pages_site_mobile.png` | опубликованный сайт, мобильная версия 390 px |

## Про скриншот страницы Settings → Pages

Страница `https://github.com/knaT43-T/greenglow-lr5/settings/pages` требует авторизации в GitHub. Автоматический headless-браузер не имеет сессии пользователя, поэтому снять её без ручного входа нельзя. Настройка выполнена через API, а факт успешной публикации подтверждён:

1. ответом API `status: built`, `source: main /`;
2. успешным run `pages build and deployment #1`;
3. HTTP 200 по публичному адресу;
4. скриншотами опубликованного сайта.

Если преподаватель требует именно скриншот страницы настроек, его можно сделать вручную:

1. войти в GitHub под `knaT43-T`;
2. открыть `https://github.com/knaT43-T/greenglow-lr5/settings/pages`;
3. убедиться, что указаны `Source: Deploy from a branch`, `Branch: main`, `Folder: / (root)`;
4. сделать скриншот страницы и сохранить как `report_screens/13_pages_settings_manual.png`.

## Примечание о 404

Первый запрос к `https://knat43-t.github.io/greenglow-lr5/` вернул HTTP 404 и страницу GitHub с кодом 404. Это ожидаемое поведение для только что включённого GitHub Pages: сборка ещё не завершилась. После завершения сборки (`status: built`) сайт начал отдавать HTTP 200. В отчёте зафиксирован итоговый рабочий адрес, а не промежуточное состояние.
