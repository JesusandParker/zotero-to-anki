# The Editor Stage

This is the piece the old ChatGPT system never had, and the single biggest reason the new cards will beat the old ones. After a card is drafted, run it through this checklist **as an adversary** — your job is to *break* the card, not to approve it. Default to "rewrite" when unsure.

Run every drafted card through all 11 checks. Output one of: **PASS**, **REWRITE** (with the fix applied), or **DROP** (with a one-line reason).

| # | Check | How to test it | If it fails |
|---|-------|----------------|-------------|
| 1 | **One answer** | Hide the cloze. Read the stem. Could a knowledgeable EMT write a *different* correct answer? | Rewrite the stem to constrain to one answer, or DROP. |
| 2 | **No tautology / leak** | Is the answer stated or strongly implied by the visible words? | Rewrite so the stem cues without revealing. |
| 3 | **Grounded** | Is every claim supported by the highlight's `context` paragraph? Any invented detail? | Remove/fix the unsupported part. If the fact needs info that isn't there, DROP and flag. |
| 4 | **Fully clozed** | Are there other distinct testable facts in this passage left untested? | Add sibling card(s) for the missed facts. |
| 5 | **List handled** | Is this a list where only some items are clozed and the rest revealed? | Restructure into sibling cards or one grouped-reveal card (card-rules Layer B #4). |
| 6 | **Crisp cloze** | Is the hidden span a tight keyword/number, or a long fuzzy phrase you couldn't recall verbatim? | Tighten the deletion to the key term. |
| 7 | **Right size** | Does one card hide more than ~3–4 items, or exceed 60 words? | Split. |
| 8 | **Worth it** | Is the card built around genuinely testable knowledge, or around soft connective filler? | Re-anchor the card to the real fact. Do NOT drop a highlighted item — if it's truly uncardable even after checking card-rules Rule 0, flag `needs_human_check`. |
| 9 | **Hint clean** | Could the hint replace the answer and mean the same thing? | Make it a slot-label, or remove it. |
| 10 | **Standalone** | Any deixis, source-artifact word, or sentence-initial pronoun? Does it read cold, right after an unrelated card? | Rewrite to be self-contained. |
| 11 | **Back Extra earns its place** | Does it add a real edge (Distinguish/Pitfall/Why…), or just restate the Text? | Rewrite it, don't pad. |

**Safety overlay:** if the card states a number, dose, threshold, or time window, or the extractor marked its grounding `PARTIAL`/`NOT_FOUND`, set `needs_human_check: true` regardless of the verdict above. These go to Parker for a human glance before he moves them out of `EMT::_Review`.

**Tone:** be strict. A smaller deck of cards that are all genuinely good beats a big deck where one in five is vague. When you genuinely can't decide between two phrasings, keep the one that reads most like a human tutor quizzing him.
