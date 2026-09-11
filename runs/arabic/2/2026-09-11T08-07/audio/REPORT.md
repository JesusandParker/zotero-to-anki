# Unit 2 audio pass — 2026-09-11 (follow-on to run 2026-09-11T08-07)

Parker: *"add all of the audio that you can as much audio as you can into all of the
flashcards that you just created, and you also should go through my lecture transcripts
… and add in my actual professor, saying the words."*

## What landed

26 notes gained audio. Nothing was overwritten — every write went through
`authorship.guard(..., fill_empty=True)` and was read back before being recorded.

| Where | Notes | Clip |
|---|---|---|
| baa / taa / thaa / yaa positional forms (12) | Audio field | `arabic_pron_0{2,3,4}_*.mp4`, `arabic_pron_28_yaa.mp4` |
| waaw positional form (1) | Audio field | `arabic_pron_27_waaw.mp4` |
| waaw, yaa, thaa sound cards (3) | Audio field | the same publisher letter clips |
| fatHa cards (3) | Audio field | `arabic_ab3e_fatha.mp3` **new** |
| Damma card (1) | Audio field | `arabic_ab3e_damma.mp3` **new** |
| kasra cards (2) | Audio field | `arabic_ab3e_kasra.mp3` **new** |
| long/short correspondence card (1) | Back Extra | all three vowel clips, labelled |
| yaa + waaw cards (6) | Back Extra | `arabic_khouri_u2_{yaa,waaw}.mp3` **new, her voice** |
| Unit 1 fatHa / Damma / kasra symbol notes (3) | Audio field | the three new vowel clips |

Unit 2 Book Highlights: 37 notes / 55 cards, **22 now carry an Audio clip (was 0)**.
Whole Arabic tree: 165 notes, 105 with audio. `media_audit`: 159 refs / 159 files, all clear.

## The five new clips, and how each was verified

Every clip was cut with the playbook's 95 ms of real room lead-in and then **re-gated
after encoding, in both languages** (R66) — the transcription below is of the final mp3,
not the source:

| file | source | cut | expect | AR readback |
|---|---|---|---|---|
| `arabic_khouri_u2_waaw.mp3` | Dr. Khouri, 9/1 lecture 31:24 | 1884.25–1884.64 | واو | **واو** ✓ |
| `arabic_khouri_u2_yaa.mp3` | Dr. Khouri, 9/3 lecture 06:41 | 401.36–401.78 | يا | **يا** ✓ |
| `arabic_ab3e_fatha.mp3` | Alif Baa 3e "Writing ـَـ" | 4.69–5.28 | الفتحة | **الفتحة** ✓ |
| `arabic_ab3e_damma.mp3` | Alif Baa 3e "Writing ـُـ" | 1.63–2.39 | الضمة | **والضمّة** ✓ (keeps the leading *wa-*) |
| `arabic_ab3e_kasra.mp3` | Alif Baa 3e "Writing ـِـ" | 1.60–2.40 | الكسرة | **والكسرة** ✓ (keeps the leading *wa-*) |

## What did NOT get audio, and why

11 of the 34 cards, deliberately — reasons in `u2_audio_plan.json`. The ones worth
stating out loud:

- **برافو / braafoo has no clip anywhere.** The full Lingco harvest (10 units,
  263 items, 1616 assets) does not contain the word, and Dr. Khouri never says
  "bravo" in any of the six captured lectures. Shipped silent, per the standing rule
  that a card with neither a clean own-voice cut nor a verified publisher clip ships
  with no audio and is reported.
- The culture cards, the three English definitions, and the four abstract
  orthography/length rules have no sound that is their answer.

## Dr. Khouri: two clips, not more — and why

Her lectures were searched end to end for every Unit 2 target (six letter names, three
vowel names, braafoo) across four mlx-whisper full passes and 157 silence-bounded
islands in eighteen hand-picked windows. **Only two cuts survived the post-encode
dual-language gate.** The rest transcribe to noise at sub-second length: her isolated
"fatHa" comes back as *Fatal*, "kasra" as *guess it up*, "ba-ta-tha" as *Ciao*. Islands
long enough to transcribe reliably are English sentences with the Arabic word buried
mid-phrase, which is not a pronunciation model.

This is the R63 discipline holding: a clip is verified by transcribing it, never by the
fact that the transcript says she said the word somewhere in that second.

## Guard change

`authorship.py` gained a fourth VERIFIED predicate, `is_fill_of_empty` / `fill_empty=`.
The 34 Unit 2 notes had never had an `Audio` value written, so the field was `unknown`
and the guard refused — correctly, since an unknown field may hold Parker's own HyperTTS
clip. The predicate states the precondition instead of bypassing it: the live value must
reduce to nothing once whitespace, `<br>`, `&nbsp;` and `&#160;` are stripped, and the
new value must be non-empty. Five self-test cases were added, including the two that
matter — it must NOT license overwriting his audio, and it must NOT leak to another
field written in the same call. 19/19 pass.

The Unit 1 vowel notes proved the point: their `Audio` was empty (filled), their
`Back Extra` came back **`edited`** — Parker's own work — and was left untouched.

## Gates

`check_cards` 0 hard errors / 3 warnings (the same three already cleared on this run) ·
`check_block_spec` 21/21 · `test_regressions` 110/110 · `test_block_spec` green ·
`authorship self-test` 19/19 · `media_audit` all clear · render review done on a
contact sheet: one play button per clip, no direction flips, correct cards silent.
