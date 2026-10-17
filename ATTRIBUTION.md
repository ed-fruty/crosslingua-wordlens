# Word Lens data attributions

The Readest-derived `.lens` packs are converted from Readest's Word Lens JSON packs
(https://github.com/readest/readest, `apps/readest-app/data/wordlens`, served from
https://cdn.readest.com/wordlens) by `scripts/update_packs.py` of
https://github.com/ed-fruty/crosslingua-wordlens. Glosses are cleaned (first
senses only, markup, part-of-speech tags, stress marks and Arabic vowel signs removed).

Sources and licences (CC-BY-SA data stays CC-BY-SA in the converted packs):

- WikDict (bilingual glosses) - CC-BY-SA 3.0, derived from DBnary / Wiktionary. https://www.wikdict.com/
- kaikki.org wiktextract dump of the English Wiktionary (en-vi, en-hu, en-ar glosses) - CC-BY-SA 4.0.
  https://kaikki.org/dictionary/rawdata.html
- FrequencyWords (difficulty ranks, OpenSubtitles/OPUS) - CC-BY-SA 4.0. https://github.com/hermitdave/FrequencyWords
- ECDICT (en-zh and en-en glosses, ranks, English inflections) - MIT. https://github.com/skywind3000/ECDICT
- WordNet (en-en synonyms and hypernyms) - WordNet 3.0 licence. https://wordnet.princeton.edu/
- lemmatization-lists (source-language inflections) - https://github.com/michmech/lemmatization-lists

`word-lens-en-uk.lens` is derived by CrossLingua: its glosses are the en-ru pack's Russian
glosses machine-translated into Ukrainian (Google Translate), with en-ru's ranks and
inflections. It inherits en-ru's CC-BY-SA licence.

Each pack also carries its own attribution string (shown on the device):

- `word-lens-de-en.lens`: Glosses: WikDict (CC-BY-SA-3.0), derived from DBnary/Wiktionary. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-3.0.
- `word-lens-en-ar.lens`: Glosses: Wiktionary (CC-BY-SA-4.0) via kaikki.org. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-4.0.
- `word-lens-en-de.lens`: Glosses: WikDict (CC-BY-SA-3.0), derived from DBnary/Wiktionary. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-3.0.
- `word-lens-en-en.lens`: Word Lens data derived from Readest's Word Lens packs (https://github.com/readest/readest). See ATTRIBUTION.md for sources and licences.
- `word-lens-en-es.lens`: Glosses: WikDict (CC-BY-SA-3.0), derived from DBnary/Wiktionary. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-3.0.
- `word-lens-en-fr.lens`: Glosses: WikDict (CC-BY-SA-3.0), derived from DBnary/Wiktionary. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-3.0.
- `word-lens-en-hu.lens`: Glosses: Wiktionary (CC-BY-SA-4.0) via kaikki.org. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-4.0.
- `word-lens-en-pt.lens`: Glosses: WikDict (CC-BY-SA-3.0), derived from DBnary/Wiktionary. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-3.0.
- `word-lens-en-ru.lens`: Glosses: WikDict (CC-BY-SA-3.0), derived from DBnary/Wiktionary. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-3.0.
- `word-lens-en-uk.lens`: Glosses: machine-translated (Google Translate) from the Readest en-ru Word Lens pack, whose glosses come from WikDict (CC-BY-SA-3.0), derived from DBnary/Wiktionary. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-3.0.
- `word-lens-en-vi.lens`: Glosses: Wiktionary (CC-BY-SA-4.0) via kaikki.org. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-4.0.
- `word-lens-en-zh.lens`: Word Lens data derived from Readest's Word Lens packs (https://github.com/readest/readest). See ATTRIBUTION.md for sources and licences.
- `word-lens-es-en.lens`: Glosses: WikDict (CC-BY-SA-3.0), derived from DBnary/Wiktionary. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-3.0.
- `word-lens-fr-en.lens`: Glosses: WikDict (CC-BY-SA-3.0), derived from DBnary/Wiktionary. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-3.0.
- `word-lens-it-en.lens`: Glosses: WikDict (CC-BY-SA-3.0), derived from DBnary/Wiktionary. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-3.0.
- `word-lens-pt-en.lens`: Glosses: WikDict (CC-BY-SA-3.0), derived from DBnary/Wiktionary. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-3.0.
- `word-lens-ru-en.lens`: Glosses: WikDict (CC-BY-SA-3.0), derived from DBnary/Wiktionary. Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). License: CC-BY-SA-3.0.

<!-- ua-dict:begin -->
## Word Lens packs built by ua-dict

- `word-lens-ro-uk.lens` (personal profile; sources: kaikki-en-translations, kaikki-ru-entries, kaikki-ru-translations, kaikki-uk-entries, mueller7, slovnyk-en-uk, slovnyk-ru-uk, slovnyk-uk-en, slovnyk-uk-ru, wikdict-en-ru, wikt-ro-en)
- `word-lens-ro-ru.lens` (personal profile; sources: kaikki-en-translations, kaikki-ru-entries, kaikki-ru-translations, mueller7, wikdict-en-ru, wikt-ro-en)

Per-pack attribution strings (shown on the device):

- `word-lens-ro-uk.lens`: Glosses: English Wiktionary translation tables (kaikki.org / wiktextract) (CC-BY-SA-4.0); English Wiktionary entries (kaikki.org / wiktextract) (CC-BY-SA-4.0); Russian Wiktionary translation tables (kaikki.org / wiktextract) (CC-BY-SA-4.0); English Wiktionary entries (kaikki.org / wiktextract) (CC-BY-SA-4.0); V.K. Mueller, English-Russian Dictionary, 7th ed. (Mueller 7 GPL) (GPL (Mueller 7 GPL)); slovnyk.org.ua English-Ukrainian (mova.org dictd conversion) (GPL (slovnyk.org.ua)); slovnyk.org.ua Russian-Ukrainian (mova.org dictd conversion) (GPL (slovnyk.org.ua)); slovnyk.org.ua Ukrainian-English (mova.org dictd conversion) (GPL (slovnyk.org.ua)); slovnyk.org.ua Ukrainian-Russian (mova.org dictd conversion) (GPL (slovnyk.org.ua)); WikDict / FreeDict (Wiktionary via DBnary) (CC-BY-SA-4.0); Wiktionary (English edition) via xxyzz/wiktionary_stardict (CC-BY-SA-4.0). Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). Used with permission of the authors; see LICENSES/ (licence files to be added by the maintainer).
- `word-lens-ro-ru.lens`: Glosses: English Wiktionary translation tables (kaikki.org / wiktextract) (CC-BY-SA-4.0); English Wiktionary entries (kaikki.org / wiktextract) (CC-BY-SA-4.0); Russian Wiktionary translation tables (kaikki.org / wiktextract) (CC-BY-SA-4.0); V.K. Mueller, English-Russian Dictionary, 7th ed. (Mueller 7 GPL) (GPL (Mueller 7 GPL)); WikDict / FreeDict (Wiktionary via DBnary) (CC-BY-SA-4.0); Wiktionary (English edition) via xxyzz/wiktionary_stardict (CC-BY-SA-4.0). Frequency: hermitdave/FrequencyWords from OpenSubtitles/OPUS (CC-BY-SA-4.0). Used with permission of the authors; see LICENSES/ (licence files to be added by the maintainer).
<!-- ua-dict:end -->
