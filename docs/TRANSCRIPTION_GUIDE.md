# Transcription guide (IRCAM Latin)

Transcripts are written in the **IRCAM Latin alphabet**. Tifinagh is generated automatically
(`tachelhit_asr.tifinagh.latin_to_tifinagh`), so annotators only need to learn one script.

## Alphabet

| Latin | Tifinagh | Sound | | Latin | Tifinagh | Sound |
|---|---|---|---|---|---|---|
| a | ⴰ | a | | m | ⵎ | m |
| b | ⴱ | b | | n | ⵏ | n |
| c | ⵛ | ch (ش) | | q | ⵇ | q (ق) |
| d | ⴷ | d | | r | ⵔ | r |
| ḍ | ⴹ | emphatic d (ض) | | ṛ | ⵕ | emphatic r |
| e | ⴻ | schwa (rare) | | s | ⵙ | s |
| ɛ | ⵄ | ʿayn (ع) | | ṣ | ⵚ | emphatic s (ص) |
| f | ⴼ | f | | t | ⵜ | t |
| g | ⴳ | g | | ṭ | ⵟ | emphatic t (ط) |
| ɣ | ⵖ | gh (غ) | | u | ⵓ | u / w |
| h | ⵀ | h (ه) | | w | ⵡ | w |
| ḥ | ⵃ | ḥ (ح) | | x | ⵅ | kh (خ) |
| i | ⵉ | i | | y | ⵢ | y |
| j | ⵊ | j (ج) | | z | ⵣ | z |
| k | ⴽ | k | | ẓ | ⵥ | emphatic z |
| l | ⵍ | l | | ʷ | ⵯ | labialisation (gʷ, kʷ) |

Typing tip: `gh`, `ch`, `3` are accepted and converted to `ɣ`, `c`, `ɛ`.

## Rules

1. Write what is **said**, not a corrected or translated version.
2. Lowercase, no punctuation except `?` (removed before scoring anyway).
3. Geminated (doubled) consonants are written twice: `tamttut`, `iggan`.
4. Separate words with spaces; attach clitics with `-` (e.g. `inna-yas`), the hyphen is normalised away for scoring.
5. Arabic / French code-switching: write the word as pronounced in Latin letters and wrap it: `[fr:telefon]`.
6. Unintelligible parts: `[?]`. Noise / music: `[noise]`. Skip clips that are mostly noise.

## Workflow

1. Listen to the clip fully once, then transcribe.
2. Mark uncertain words with `*` (e.g. `*tagant`) so a reviewer checks them.
3. A second speaker reviews ~10% of clips; we report their agreement (CER between the two versions).
