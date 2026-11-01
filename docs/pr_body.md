## Лабораторная работа №5 — добавление изображений

Ветка создана для выполнения требования ЛР №5: показать отдельную линию разработки и объединить её с `main`.

### Что сделано

- Агент добавил три локальных изображения из рабочей папки в первые три карточки каталога:
  - `assets/img/photo1.jpg` — увлажняющий крем с алоэ;
  - `assets/img/photo2.jpg` — сыворотка с витамином C;
  - `assets/img/photo3.jpg` — гидрофильное масло.
- В `index.html` добавлены `<img>` с `alt`, `width`, `height`, `loading="lazy"`, `decoding="async"`.
- Добавлен CSS `.product-img img` с `object-fit: cover`.
- Убраны два декоративных блока в hero, перекрывавших подпись товара.
- Обновлены `docs/agent_changes.md`, `docs/images.md`, `docs/before_after.md`, `docs/execution_log.md`.
- Diff сохранён в `docs/diff_add_images.diff`.

### Изменённые файлы

`index.html`, `assets/img/photo1.jpg`, `assets/img/photo2.jpg`, `assets/img/photo3.jpg`, документация в `docs/`, скриншоты в `report_screens/`.

### Проверка

- Три изображения загружаются локально, внешних ссылок нет.
- Сетка каталога 3×2 не сломана, мобильная версия корректна.
- Скриншоты «до» и «после» приложены в `report_screens/`.
