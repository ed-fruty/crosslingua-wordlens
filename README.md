# CrossLingua Word Lens packs

Данные и инструменты для **Word Lens** — режима прошивки
[CrossLingua](https://github.com/ed-fruty/crosslingua-reader) (Xteink X4 и другие ESP32-читалки),
который подписывает над трудными словами книги их краткий перевод. Здесь лежат готовые пакеты
глосс, скрипты, которые их собирают и обновляют, и workflow, публикующие их как GitHub-релизы.
Устройство скачивает пакеты отсюда:

```
https://github.com/ed-fruty/crosslingua-wordlens/releases/latest/download/word-lens-manifest.json
https://github.com/ed-fruty/crosslingua-wordlens/releases/latest/download/word-lens-<source>-<target>.lens
```

Если GitHub недоступен, прошивка берёт исходный JSON-пакет Readest с `cdn.readest.com/wordlens/`
и конвертирует его сама (кроме en-uk — его на CDN Readest нет).

## Что такое пакет

Один пакет — одна пара языков `<source>-<target>`: леммы исходного языка с рангом частотности
(уровень сложности) и короткой глоссой, плюс словоформы, которые сворачиваются к своей лемме.
Данные — из Word Lens пакетов [Readest](https://github.com/readest/readest)
(WikDict / Wiktionary, FrequencyWords, ECDICT, WordNet). Глоссы чистятся: первые смыслы,
без разметки, помет частей речи, ударений и огласовок.

Список пакетов ниже генерируется из манифеста архива (`python3 scripts/readme_table.py`;
`ci.yml` проверяет, что он не устарел). Происхождение: `readest` — сконвертирован из пакета Readest,
`derived` — выведен нами (en-uk, см. ниже), `ua-dict` — импортирован из ua-dict.

<!-- packs-table:begin -->
Пакетов: 19, всего 21.9 MB.

| Пара | Исходный | Перевод | Происхождение | Размер | Леммы | Записи (с формами) |
|---|---|---|---|---:|---:|---:|
| `de-en` | de | en | readest | 1.32 MB | 13806 | 63088 |
| `en-ar` | en | ar | readest | 0.69 MB | 12870 | 26331 |
| `en-de` | en | de | readest | 0.80 MB | 14926 | 31789 |
| `en-en` | en | en | readest (определения на английском) | 1.41 MB | 24246 | 56686 |
| `en-es` | en | es | readest | 0.79 MB | 14769 | 31798 |
| `en-fr` | en | fr | readest | 0.77 MB | 15070 | 31688 |
| `en-hu` | en | hu | readest | 0.74 MB | 13639 | 29391 |
| `en-pt` | en | pt | readest | 0.77 MB | 14656 | 31715 |
| `en-ru` | en | ru | readest | 0.99 MB | 14914 | 31691 |
| `en-uk` | en | uk | derived из en-ru (машинный перевод) | 0.80 MB | 14914 | 31691 |
| `en-vi` | en | vi | readest | 0.53 MB | 9759 | 20572 |
| `en-zh` | en | zh | readest | 1.42 MB | 24446 | 56714 |
| `es-en` | es | en | readest | 1.26 MB | 10949 | 68297 |
| `fr-en` | fr | en | readest | 1.33 MB | 12361 | 68151 |
| `it-en` | it | en | readest | 1.37 MB | 11657 | 72058 |
| `pt-en` | pt | en | readest | 1.72 MB | 11808 | 95878 |
| `ro-ru` | ro | ru | ua-dict (профиль personal) | 1.83 MB | 13450 | 89021 |
| `ro-uk` | ro | uk | ua-dict (профиль personal) | 1.89 MB | 13540 | 89753 |
| `ru-en` | ru | en | readest | 1.48 MB | 8780 | 56172 |
<!-- packs-table:end -->

Это все пакеты, которые есть у Readest (на CDN и в `apps/readest-app/data/wordlens` его
репозитория — 17 пар на 2026-10-18), кроме `zh-en`. Исходный язык ограничен токенайзером прошивки:
он делит текст по пробелам, поэтому подходит любой язык, кроме тех, которым нужен сегментатор слов —
zh, ja, ko, th (`NEEDS_SEGMENTER` в `scripts/update_packs.py`; в прошивке — `supportedSource()` в
`src/modules/lingua/activities/WordLensPacksActivity.cpp`). Язык перевода не ограничен (`en-zh`
есть). Новые пары Readest с подходящим исходным языком подхватываются синхронизацией автоматически.

## Форматы

* **`.lens`** — бинарный формат, который прошивка читает прямо с SD-карты
  (`/.crosspoint/wordlens/word-lens-<source>-<target>.lens`): 64-байтный заголовок, хеш-таблица
  записей `ключ → ранг + смещение глоссы`, пул глосс, строка атрибуции. Спецификация — в прошивке,
  [`docs/file-formats.md`, «Word Lens pack (.lens)»](https://github.com/ed-fruty/crosslingua-reader/blob/main/docs/file-formats.md#word-lens-pack-lens),
  эталонный писатель и читатель — `scripts/lens_format.py`. Конвертер прошивки (`LensBuilder`)
  обязан давать байт-в-байт тот же файл из того же JSON; это проверяют фикстуры (ниже).
* **`word-lens-manifest.json`** — список пакетов релиза: `pair`, `source`, `target`, `file`,
  `bytes`, `sha256` (по нему устройство проверяет скачанный файл), `entries`, `headwords`,
  `version`, `contentHash`, а также происхождение: `readest` (sha256 исходного JSON),
  `derivedFrom` + `translationCacheSha256` для en-uk, `origin` для импортированных пакетов.
* **`data/word-lens-packs.tar.xz`** — все пакеты, манифест и `ATTRIBUTION.md` одним архивом в
  git. Архив воспроизводимый (`scripts/pack_archive.py`: отсортированные члены, нулевые
  mtime/uid, xz preset 9e), поэтому без изменений в данных байты архива не меняются и git не
  раздувается. Посмотреть: `tar -tJf data/word-lens-packs.tar.xz`.
* **`ATTRIBUTION.md`** — копия атрибуции из архива (она же публикуется как
  `word-lens-ATTRIBUTION.md`).

## Структура

```
data/word-lens-packs.tar.xz     пакеты + манифест + ATTRIBUTION.md
data/en-uk.translations.tsv     кэш переводов ru → uk для en-uk
ATTRIBUTION.md                  источники и лицензии
LICENSES/                       тексты лицензий (добавляет мейнтейнер)
scripts/update_packs.py         синхронизация с CDN Readest
scripts/make_en_uk.py           вывод en-uk из en-ru
scripts/import_packs.py         импорт пакетов, собранных вне Readest (ua-dict)
scripts/lens_format.py          эталонный формат .lens
scripts/pack_archive.py         воспроизводимый архив
scripts/stage_release_assets.py проверка и распаковка архива в ассеты релиза
scripts/readme_table.py         таблица пакетов в README из манифеста
scripts/make_fixtures.py        фикстуры для тестов (здесь и в прошивке)
tests/                          офлайн-тесты и фикстуры
.github/workflows/              ci.yml, sync.yml, release.yml
```

Нужен только Python ≥ 3.10, сторонних зависимостей нет.

## Обновление из CDN Readest

```bash
python3 scripts/update_packs.py --dry-run          # что изменилось у Readest (ничего не пишет и не переводит)
python3 scripts/update_packs.py                    # пересобрать изменившиеся пакеты
python3 scripts/update_packs.py --pairs en-ru,en-uk
python3 scripts/update_packs.py --exclude en-uk    # всё, кроме en-uk
python3 scripts/update_packs.py --readest-dir ~/readest/apps/readest-app/data/wordlens   # из локального checkout
python3 scripts/readme_table.py                    # обновить таблицу пакетов в README
```

Скрипт качает `manifest.json` и пакеты с `https://cdn.readest.com/wordlens/`, сверяет их sha256 и
размер, конвертирует **только** изменившиеся пакеты (или все при смене `FORMAT_VERSION` /
`DATA_VERSION`, или с `--force`), проверяет, что каждый ключ находится и указывает на свою лемму,
переписывает архив, манифест и `ATTRIBUTION.md` и печатает, что `git add`. Повторный запуск без
изменений у Readest ничего не меняет. Коммит — за вами. Остальные флаги: `--offline` (никогда не
обращаться к переводчику), `--retry-failed`, `--samples N` (показать N глосс каждого пересобранного
пакета).

Автоматически это делает **`sync.yml`**: по понедельникам и вручную (Actions → Sync from Readest →
Run workflow; можно указать пары и `retry_failed`). Он запускает синхронизацию и тесты и
открывает (или обновляет) PR из ветки `sync/readest`. Если переводчик недоступен с раннера,
остальные пакеты всё равно обновляются, en-uk остаётся прежним, и это написано в PR — тогда
en-uk можно пересобрать локально и запушить в ту же ветку. Ветка `sync/readest` перезаписывается
каждым запуском.

## Как собирается en-uk

У Readest нет ни en-uk, ни других пар с украинским (проверено 2026-10-18: CDN-манифест и `main`
репозитория Readest — 17 пар, `uk` нет ни как исходного, ни как целевого языка). Если Readest
добавит нативный en-uk, `update_packs.py` его пропустит и сообщит об этом (`DERIVED` побеждает) —
тогда его нужно сравнить с нашим и решить осознанно. Поэтому он выводится из en-ru (`scripts/make_en_uk.py`, его вызывает
`update_packs.py`): первый смысл каждой русской глоссы переводится на украинский через бесплатный
endpoint Google `translateHtml` (тот же, что у движка «Google (Free) — HTML» в прошивке), пачками
до 100 строк с паузами. Ранги и словоформы — от en-ru.

Результаты хранятся в закоммиченном кэше `data/en-uk.translations.tsv`
(`русский<TAB>украинский`, отсортирован, одна строка на уникальную глоссу; пустая правая часть —
неудачный перевод). Поэтому пересборка en-uk детерминированна и почти офлайн: в сеть уходят
только русские глоссы, которых ещё нет в кэше (и с `--retry-failed` — прежде неудачные).
Записи без перевода выпадают из пакета. en-uk пересобирается, когда меняется sha256 исходного
en-ru или содержимое кэша. `python3 scripts/make_en_uk.py --probe` проверяет, отвечает ли переводчик.

## Пакеты из ua-dict

Соседний проект `ua-dict` (отдельный репозиторий, рядом с этим: `../ua-dict`) собирает пакеты вида
`ro-uk`, `ro-ru` из Викисловаря и других словарей и кладёт их в `dist/wordlens/` вместе с
`word-lens-manifest.fragment.json` и `ATTRIBUTION.fragment.md`. Импорт сюда:

```bash
cd ../ua-dict && ./build.sh --pairs ro-uk,ro-ru       # собрать там
cd ../crosslingua-wordlens
python3 scripts/import_packs.py --packs ../ua-dict/dist/wordlens            # план (dry run)
python3 scripts/import_packs.py --packs ../ua-dict/dist/wordlens --apply    # записать
python3 scripts/import_packs.py --remove ro-ru --name ua-dict --apply       # убрать пакет
python3 scripts/readme_table.py                                             # обновить таблицу
```

Импорт проверяет `formatVersion`, sha256/размер и разбор каждого `.lens`, добавляет или заменяет
пакеты той же пары (пакеты Readest заменять отказывается; а `update_packs.py` не заменяет
импортированный пакет, даже если у Readest появится та же пара), обновляет манифест и вставляет в
`ATTRIBUTION.md` раздел между `<!-- ua-dict:begin -->` и `<!-- ua-dict:end -->`. `update_packs.py`
оставляет импортированные пакеты и такие разделы как есть, так что синхронизация с Readest их не
стирает. Затем — обычный коммит и релиз. (Скрипт `scripts/import_into_crosslingua.py` в ua-dict
писал в старый путь внутри репозитория прошивки; теперь используйте `import_packs.py` отсюда.)

## Релиз

Релизы — датированные теги **`packs-YYYY.MM.DD`** (второй релиз в тот же день —
`packs-YYYY.MM.DD.2`):

```bash
git pull
git tag packs-2026.10.18
git push origin packs-2026.10.18
```

`release.yml` по тегу прогоняет тесты, распаковывает архив, сверяет каждый пакет с sha256 и
размером из манифеста и разбирает его (`scripts/stage_release_assets.py`), затем публикует
**не-pre-release** релиз, отмеченный latest, с ассетами `word-lens-<pair>.lens`,
`word-lens-manifest.json` и `word-lens-ATTRIBUTION.md` и таблицей пакетов в описании. Устройства
ходят на `releases/latest/download/`, поэтому новый релиз сразу становится источником для всех;
pre-release устройства не увидят. Повторный запуск workflow для того же тега перезаливает ассеты.

## Тесты

```bash
python3 -m unittest discover -s tests -v
```

Офлайн, без сети: детерминированность конвертации, воспроизведение фикстур, правила кэша en-uk,
идемпотентность `update_packs.py`, `--pairs`/`--exclude`, импорт и сохранение разделов
атрибуции, staging релиза. `ci.yml` запускает их на каждый push и PR и проверяет закоммиченный архив.

Фикстуры (`tests/fixtures/mini-*.json` и их `.lens.hex`, `gloss_cases.txt`) — общие с прошивкой:
её C++-тест `test/word_lens_format` проверяет, что `LensBuilder` даёт те же байты. При изменении
формата или правил очистки глосс обновите обе копии:

```bash
python3 scripts/make_fixtures.py [readest-data-wordlens-dir]
python3 scripts/make_fixtures.py --out ../crosslingua-reader/test/word_lens_format/fixtures [readest-data-wordlens-dir]
```

и поднимите `FORMAT_VERSION` в `scripts/lens_format.py` и в прошивке, если меняются байты.

## Лицензии

Данные пакетов — под лицензиями их источников: WikDict и Wiktionary — CC-BY-SA (3.0 / 4.0),
FrequencyWords — CC-BY-SA 4.0, ECDICT — MIT, WordNet — WordNet 3.0; CC-BY-SA данные остаются
CC-BY-SA и в сконвертированных пакетах. en-uk — машинный перевод глосс en-ru и наследует его
CC-BY-SA. Подробности по каждому пакету — в [`ATTRIBUTION.md`](ATTRIBUTION.md), тексты лицензий —
в [`LICENSES/`](LICENSES/).
