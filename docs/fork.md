# Форк внешнего репозитория

## Основные сведения

| Параметр | Значение |
|---|---|
| Исходный репозиторий | [pytorch/pytorch](https://github.com/pytorch/pytorch) |
| Форк | [knaT43-T/pytorch](https://github.com/knaT43-T/pytorch) |
| Платформа | GitHub |
| Дата форка | 01.11.2026 |
| Способ | GitHub CLI (`gh repo fork`) |
| Клонирование | Не выполнялось (`--clone=false`), форк создан на стороне GitHub |
| Статус | Форк создан, является копией исходного репозитория в аккаунте `knaT43-T` |

## Команда

```bash
gh repo fork pytorch/pytorch --clone=false
```

Результат команды:

```text
https://github.com/knaT43-T/pytorch
```

## Проверка

```bash
gh repo view knaT43-T/pytorch --json name,url,isFork
```

Результат:

```json
{"isFork":true,"name":"pytorch","url":"https://github.com/knaT43-T/pytorch"}
```

Дополнительная проверка через GitHub API:

```bash
gh api repos/knaT43-T/pytorch --jq '{fork: .fork, parent: .parent.full_name, source: .source.full_name}'
```

Результат:

```json
{"fork":true,"parent":"pytorch/pytorch","source":"pytorch/pytorch"}
```

## Назначение форка в работе

Форк показывает умение работать с чужими открытыми репозиториями: находить проект на GitHub, создавать собственную копию в своём аккаунте, сохранять связь с исходным репозиторием и использовать форк как основу для изучения или доработки внешнего кода. В отличие от клонирования, форк создаёт полноценный удалённый репозиторий в аккаунте пользователя и позволяет предлагать изменения через Pull Request.

## Скриншот

Для отчёта используется скриншот страницы форка:

- `report_screens/06_fork_pytorch.png` — страница `https://github.com/knaT43-T/pytorch` с пометкой «forked from pytorch/pytorch».

## Примечание

Форк создан без локального клонирования, так как в рамках лабораторной работы требуется продемонстрировать сам факт форка внешнего проекта, а не его локальную доработку. Репозиторий форка публичный.
