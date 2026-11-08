---
name: "remotion"
description: "Use when building, editing or rendering videos in code with Remotion (React): compositions, animations, voiceover sync, captions, Arabic RTL text, and rendering to MP4."
---

# Remotion video skill

Remotion turns React components into video. Every frame is a pure render of `useCurrentFrame()`; never animate with CSS transitions, `setTimeout`, or `requestAnimationFrame` — they break rendering.

## 1. Project setup
- New project: `npx create-video@latest` (template: blank or hello-world), then `npm i`.
- Preview: `npx remotion studio`. Render: `npx remotion render <CompositionId> out/video.mp4`.
- Extra packages as needed (keep versions identical to `remotion`): `@remotion/transitions`, `@remotion/google-fonts`, `@remotion/media-utils`, `@remotion/captions`, `@remotion/lottie`, `@remotion/three`.
- Put assets (audio, images, fonts, video) in `public/` and load with `staticFile('name.ext')`.
- If the sandbox has no network, say so: npm install will fail; write the project files and give the user the install/render commands to run locally.

## 2. Register compositions (src/Root.tsx)
```tsx
import { Composition } from 'remotion';
import { Main } from './Main';
export const RemotionRoot = () => (
  <Composition id="Main" component={Main}
    durationInFrames={30 * 30} fps={30} width={1080} height={1920}
    defaultProps={{}} />
);
```
Common sizes: vertical 1080x1920 (Reels/TikTok/Stories), square 1080x1080, landscape 1920x1080. Default 30 fps.
For duration driven by audio length, use `calculateMetadata` with `getAudioDurationInSeconds` from `@remotion/media-utils`.

## 3. Animation primitives
```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring, Easing } from 'remotion';
const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
const scale = spring({ frame, fps, config: { damping: 200 } });
const y = interpolate(frame, [0, 20], [80, 0], { easing: Easing.out(Easing.cubic), extrapolateRight: 'clamp' });
```
- Always clamp `interpolate` unless overshoot is wanted.
- Delay a spring: `spring({ frame: frame - 10, fps })`.
- Stagger lists: offset each item's frame by `i * 4`.

## 4. Timing & scenes
- `<Sequence from={60} durationInFrames={90}>` — children see frame reset to 0 at `from`.
- `<Series>` with `<Series.Sequence durationInFrames={n}>` for back-to-back scenes.
- Transitions: `@remotion/transitions` → `<TransitionSeries>` with `fade()`, `slide()`, `wipe()`, `linearTiming({durationInFrames: 15})` or `springTiming()`.
- Keep scene durations in one config object (seconds × fps) so timing can be re-synced to a voiceover quickly.

## 5. Media
- Audio: `<Audio src={staticFile('voiceover.mp3')} volume={1} />`; background music with lower volume or a volume callback `volume={(f) => interpolate(f,[0,30],[0,0.3],{extrapolateRight:'clamp'})}`.
- Images: `<Img src={staticFile('logo.png')} />` (not `<img>`), so rendering waits for load.
- Video: `<OffthreadVideo src={...} />` for rendering performance.
- Trim: `startFrom` / `endAt` (in frames).

## 6. Fonts & Arabic RTL
```tsx
import { loadFont } from '@remotion/google-fonts/Cairo'; // or Tajawal, Almarai, IBMPlexSansArabic
const { fontFamily } = loadFont();
<div style={{ fontFamily, direction: 'rtl', textAlign: 'right', unicodeBidi: 'plaintext' }}>نص عربي</div>
```
- Arabic letters connect: never split an Arabic word into per-letter spans (breaks shaping). Animate per word or per line instead.
- Mixed Arabic + numbers/Latin: wrap the Latin run in `<bdi>` or set `unicodeBidi: 'isolate'`.
- Slide-ins for RTL should usually enter from the right.
- Give line-height ≥ 1.4 for Arabic diacritics and descenders.

## 7. Voiceover-driven videos
1. Get the voiceover file and its duration; set `durationInFrames = ceil(seconds * fps)` (+ ~1s tail).
2. Split script into beats with start/end seconds (from a transcript with timestamps if available).
3. Map each beat to a `<Sequence from={s*fps} durationInFrames={(e-s)*fps}>` scene.
4. Key words appear on the frame the word is spoken.

## 8. Captions
- Use `@remotion/captions` (`createTikTokStyleCaptions`) from a `Caption[]` array ({text, startMs, endMs}); show the active page by comparing `frame / fps * 1000`.
- For Arabic captions, keep whole words and RTL direction.

## 9. Rendering
- MP4 H.264: `npx remotion render Main out/video.mp4 --codec=h264 --crf=18`.
- Still/thumbnail: `npx remotion still Main out/thumb.png --frame=45`.
- Props from CLI: `--props='{"title":"..."}'`.
- Faster: `--concurrency=50%`. Transparent: `--codec=prores --prores-profile=4444` with no background.

## 10. Quality checklist
- No `Math.random()` without `random('seed')` from remotion (must be deterministic).
- No CSS animations/transitions; everything from `frame`.
- Every asset through `staticFile` + `<Img>/<Audio>/<OffthreadVideo>`.
- Check safe areas on vertical video (keep text out of top ~250px and bottom ~350px for platform UI).
- Render a few stills at key frames and look at them before the full render.

## Docs
When unsure of an API, check https://www.remotion.dev/docs (official Agent Skills: https://www.remotion.dev/docs/ai/skills).