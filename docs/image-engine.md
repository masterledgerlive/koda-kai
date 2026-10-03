# Koda Kai Image Engine 🎨

*How pictures get made: free iteration on our own GPU, tokens only for finals.*
*Companion to the story→video pipeline in `vision-multi-station.md`.*

## The economics (David's question, answered)

- **ComfyUI on Shadow = free.** The box is already paid for; every local render costs
  zero tokens. Iterate 50 times, pay nothing.
- **Kodakai's built-in generation = tokens per image/video.** Great for finals,
  expensive for exploring.
- **The rule:** explore free on ComfyUI → lock the winner → spend tokens only on
  finals (or fal.ai for final video).

## Status (2026-10-03)

- ComfyUI deployed on Shadow D:, models 100% downloaded. **Not running right now** —
  the GPU belongs to the caption batch (37/383) until it finishes.
- Kodakai drives ComfyUI over SSH whenever we're ready. First test render happens
  after captions clear the GPU.

## The style lock (where creativity kicks in)

One-shot generation is why some outputs feel elementary: no iteration, no memory of
what "right" looks like. The fix isn't a bigger model — it's a **locked style**:

1. Generate dozens of free variations on ComfyUI (characters, palettes, line styles).
2. David picks the winners → that becomes the **Koda Kai house style**.
3. Save it as a reusable ComfyUI workflow preset: same base prompt, same sampler,
   same style tags, every time.
4. Every future image starts from the locked base — consistent world, on purpose.
5. Later, optional: LoRA trained on the kids' own drawings for a true house model.

## The kid-drawing pipeline (the heart of it)

This is where Kai gives Koda Kai its shape:

1. **Kid draws** in the book (Draw lives in Story Studio).
2. **Photo/scan of the drawing + the kid's spoken explanation** ("it's a dragon with
   flappy wings!") go in together.
3. **ComfyUI img2img** re-renders it: keeps the kid's composition, finishes it in
   the locked house style. A poorly drawn dragon becomes a *cool* dragon — still
   *their* dragon.
4. The finished character **joins the transform library** as a living character.
5. **Animate it** — tail wags, wings flap — and drop it into stories, the word-dance,
   the puppet stage.
6. Every drawing the kids ever make becomes a citizen of the world. Lifelong.

### Essence preservation (David's rule)

The upgrade is an *extension of the kid's mind*, never a replacement. The re-render
keeps their lines, their colors, their scribbles outside the lines — it adds light,
texture, and background *around* what they made. The kid must always point at the
finished piece and say "that's MY dragon." If the upgrade ever "fixes" the drawing
into something unrecognizable, it failed.

## Placeholders → finals

- Today's placeholders (SVG/CSS art in the app) get replaced **per-section** as
  ComfyUI finals land — no big-bang redesign.
- Each final is generated from the locked style preset, so the app converges on one
  coherent look instead of drifting.
- Video: iterate stills free on ComfyUI → final motion via Kodakai's video or fal.ai
  (paid — David's key + spend approval).

## What David decides

- The house style winners (the fun part — picking).
- When a placeholder is "final enough" to ship.
- Any paid final renders (fal.ai) — exact spend approved first, as always.
