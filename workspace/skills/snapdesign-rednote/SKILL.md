---
name: rednote-card-generator
description: Use when you need to generate Xiaohongshu (小红书 / RedNote) carousel card HTML layouts. Given a piece of text content, this skill produces a complete, self-contained HTML document containing multiple vertical 450×600px cards styled for the RedNote / Xiaohongshu platform.
---

# RedNote Card Generator

## Overview

Use `rednote-card-generator` to turn any text content into a beautifully styled Xiaohongshu (小红书) carousel post. The output is a single, self-contained HTML string that renders multiple vertical cards (each 450×600 px) stacked vertically with a 20 px gap.

The skill calls the OpenRouter API (model: `google/gemini-2.5-flash` with fallback to `google/gemini-2.5-flash-lite`) and streams the HTML response back.

## Inputs to collect

| Field | Required | Description |
|---|---|---|
| `content` | Yes | The text content to turn into RedNote cards. Can be plain text or light HTML. |
| `colorScheme` | No | One of: `auto` (default), `warm-brown`, `sunset`, `ocean`, `forest`, `lavender`, `monochrome`. Controls the dominant palette. |
| `openrouterApiKey` | Yes | A valid OpenRouter API key (Bearer token). |

## Output

Returns a JSON object:

```json
{
  "html": "<!DOCTYPE html>...",
  "cardCount": 5
}
```

- `html`: Complete self-contained HTML document. Render this inside an iframe or a sandboxed div.
- `cardCount`: Estimated number of cards generated.

## Actions

### Generate cards

```json
{
  "action": "generate",
  "content": "今天分享三个提升专注力的方法...",
  "colorScheme": "warm-brown",
  "openrouterApiKey": "sk-or-..."
}
```

### Color scheme options

| id | Description |
|---|---|
| `auto` | AI picks colors based on content mood |
| `warm-brown` | Primary `#3E2723`, background `#FFFCF8` — cozy editorial |
| `sunset` | Primary `#FF6B6B`, secondary `#FFD93D` — vibrant warm |
| `ocean` | Primary `#4A90E2`, secondary `#50C9CE` — fresh cool |
| `forest` | Primary `#2D6A4F`, secondary `#52B788` — natural green |
| `lavender` | Primary `#9D84B7`, secondary `#C8B6E2` — soft purple |
| `monochrome` | Primary `#2C3E50`, accent `#E74C3C` — clean minimal |

## Card layout specification

The generated HTML follows these rules so downstream renderers can reliably parse it:

- **Outer container**: `div` with `display:flex; flex-direction:column; gap:20px`
- **Each card**: `div` with `width:450px; height:600px; position:relative; overflow:hidden`
- **Card backgrounds**: warm paper tones — `#FDF8F3`, `#F5EFE6`, `#FFFBF5`, `#F0EBE3` — varied per card
- **Top accent strip**: `div` with `height:8px; width:100%` in a warm accent color
- **Typography**:
  - Card title / section number: 30–38 px, `font-weight:700`, Playfair Display or Space Grotesk
  - Body text: 15–17 px, `line-height:1.75`, Noto Sans SC or Inter
  - Labels / captions: 12–13 px, muted color
- **Text colors**: coffee-brown tones `#3E2723`, `#664A42`, `#5D4037`
- **Accent shapes**: left-border bars (6 px wide), bullet circles (10×10 px), number badges (32×32 px, border-radius 16 px)
- **NO emojis** in generated content
- Fonts imported via `@import` inside `<style>` — never via `<link>` tags

## Card types

The AI selects the best card type for each section of the content:

| Card type | When to use |
|---|---|
| **Title card** (first) | Large decorative title + subtitle + author/tag label |
| **Section header** | Bold large number (01, 02…) + section heading + 1-sentence teaser |
| **Text block** | Body paragraphs with colored left-accent bar |
| **Bullet list** | Key points as rows with filled-circle bullet shapes |
| **Numbered steps** | Step-by-step instructions with rounded number badges |
| **Quote / highlight** | One key sentence enlarged (28–34 px), centered, with decorative quote marks |
| **Summary** (last) | Recap of core message + thin decorative bottom strip |

## System prompt used

When calling the LLM, the following system instruction is used:

> You are an expert graphic designer who generates production-ready HTML layouts with embedded CSS. Your output is a complete, self-contained HTML document that can be rendered directly in a browser. Output ONLY valid HTML. No markdown, no code fences, no explanation. Include a `<style>` tag with all CSS. Do NOT use Noto Sans SC. Do NOT set margin or padding on html or body tags. Do NOT use global CSS resets.

## User prompt template

The user message sent to the LLM is constructed as follows:

```
This is a Xiaohongshu (小红书) carousel post. Generate MULTIPLE vertical cards (each 450×600px) stacked vertically with 20px gap between them.

CONTENT FIDELITY — INCLUDE EVERYTHING:
- Cover ALL of the user's text. Do NOT omit, summarize, or skip any sentence.
- Distribute content logically across cards: one topic or section per card.
- Generate as many cards as needed to fit all content (typically 3–10 cards).

Content to include:
"<USER_CONTENT>"

<COLOR_INSTRUCTION>

Return ONLY valid HTML with embedded CSS. No markdown, no code fences, no explanation.
```

Where `<COLOR_INSTRUCTION>` is:
- If `colorScheme` is `auto`: `Analyze the content and choose bold, contextually appropriate colors and modern typography.`
- Otherwise: `Color Palette — foundation colors are: "<primary>" (primary) and "<secondary>" (secondary). Use them as the dominant palette with tints and shades for depth. Do NOT apply them flatly.`

## API call details

```
POST https://openrouter.ai/api/v1/chat/completions
Authorization: Bearer <openrouterApiKey>
Content-Type: application/json

{
  "model": "google/gemini-2.5-flash",
  "messages": [
    { "role": "system", "content": "<SYSTEM_PROMPT>" },
    { "role": "user",   "content": "<USER_PROMPT>" }
  ],
  "stream": true,
  "temperature": 0.4
}
```

Fallback model order: `google/gemini-2.5-flash` → `google/gemini-2.5-flash-lite`

## Post-processing steps

After receiving the full streamed HTML, apply these cleanup steps in order:

1. Strip leading/trailing markdown fences (` ```html ` … ` ``` `) if present.
2. Fix broken `<img>` tags — collapse internal whitespace/newlines to a single space.
3. If the output does not contain `<html` or `<!DOCTYPE`, wrap it:
   ```html
   <!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>RedNote</title></head><body>…</body></html>
   ```
4. Count the number of card `div` elements to populate `cardCount` in the response.

## Ideas to try

- Paste a WeChat article and get a ready-to-publish 小红书 carousel.
- Summarize a product review into a 5-card visual post.
- Turn meeting notes into a step-by-step visual guide.
- Convert a recipe into numbered-step cards with a title cover.

