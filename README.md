# LightCraft IR Presets

Fifteen infrared presets for [LightCraft](https://github.com/storytold/lightcraft), built on its RGB **Channel
Mixer**: classic red/blue swaps, a few wild false-colour looks, and some silly ones on purpose.

**Not official, not part of LightCraft.** The Channel Mixer these presets use is proposed in
[storytold/lightcraft#3579](https://github.com/storytold/lightcraft/pull/3579) and isn't in a LightCraft release yet.
Until it is, the presets need a build of that pull request (see [below](#which-lightcraft)). In a LightCraft
without the Channel Mixer they import, but only the white balance and tone settings apply, which gives a strong blue
cast.

![The fifteen presets on one 590 nm photo of Mt. Hood](images/contact-sheet.jpg)

## Install

1. Download from the [latest release](../../releases/latest):
   - **`IR Recipes.lcpreset`** for all fifteen presets in one file, or
   - just the ones you want: each preset is also its own file, named after it (`classic-swap.lcpreset`,
     `aerochrome.lcpreset`…). They're also in the [`presets`](presets) folder here.
2. In LightCraft, either drag the file(s) onto the window, or click **Import Presets…** at the top of the Presets
   panel (also under **File ▸ Import Presets…**).

They appear in three groups: **IR Recipes 1 · Classic**, **2 · Wild** and **3 · Silly**. A single preset goes into
its usual group too, and mixing is fine: a preset you already have is skipped, so importing everything after a few
single ones doesn't add duplicates.

### Updating to a new version

Importing doesn't replace presets you already have. A preset whose settings changed is added next to the old one
with the same name. So before importing a new version, **delete the three IR Recipes groups** (right-click a group in
the Presets panel), then import the new file.

## Using them

1. **Click a preset.** It sets the Channel Mixer and white balance, plus a few touches like Vibrance or Contrast.
2. **If the name says "(pick …)", pick.** In the **Channel Mixer** section, click the picker (the eyedropper):

   ![The Channel Mixer's picker](images/3-picker-button.jpg)

   Then click what the name says:
   - **snow/cloud/concrete:** anything that should come out white or grey;
   - **foliage:** bright leafy trees or grass.

   ![Before and after picking the snow](images/4-pick-before-after.jpg)

   Names ending in **(no pick)** need no step 2.
3. **Adjust Exposure to taste.** The picker keeps the spot's own brightness and never changes Exposure. If a strong
   mix has to be scaled down to fit the sliders, it says so ("Darker by 0.4…"): raise Exposure by about that much.
4. **Switching presets:** click the new preset, then pick again. A preset sets the mixer and white balance, which
   replaces your last pick.

**Presets replace each other cleanly.** Every preset sets the same settings: the mixer, white balance, and every
tone and colour setting any of the presets uses (Vibrance, Saturation, Contrast, Clarity, the tone curve, colour
grading, the HSL mixer, vignette and grain), at zero when it doesn't use one. So going from Day for Night or Night
Vision back to Classic Swap leaves no grading, vignette or grain behind, and clicking back and forth always gives the
same result. Settings no preset uses (sharpening, noise reduction, lens corrections, crop, masks) are left alone,
and so is **Exposure**: no preset ever changes it. The flip side: a preset replaces your own changes to those tone and
colour settings, so apply the preset first, then fine-tune.

Then open **Channel Mixer** to see how the look is made, and change it from there.

**Which filter?** The presets were fitted on a 590 nm camera. They're a reasonable start for 590–720 nm and
full-spectrum cameras with an IR filter. At **850 nm** and beyond there's almost no colour to mix, so use the two
**IR Mono** presets.

## The presets

| Preset | Pick | Look |
| --- | --- | --- |
| Classic Swap | neutral | The textbook red/blue swap. On a 590 nm filter that gives pink foliage and a teal sky |
| Hood River Pink | neutral | The colour settings of the Mt. Hood edit in the pull request |
| White Foliage, Blue Sky | foliage | White trees under a blue sky |
| Gold Foliage, Blue Sky | neutral | Gold trees, the look many 590 nm tutorials show |
| Soft Pastel | neutral | Half swap, low contrast, a faint pink/teal split tone |
| IR Mono, Wood Effect | none | Black and white from the red channel, punchy |
| IR Mono, Soft Glow | none | Same source, negative Clarity for a dreamy glow |
| Faux Aerochrome | neutral | Red foliage in the style of Kodak Aerochrome film |
| Fake Summer | neutral | Green trees again, though not quite the right green |
| Teal Forest, Orange Sky | neutral | Complementary teal and orange |
| Lava Fields | neutral | Brick-red land under a violet sky |
| Alien Planet | neutral | Magenta trees, a green-tinted sky |
| Night Vision Goggles | none | Green phosphor, vignette and grain; lower Exposure if it's too bright |
| Day for Night | neutral | Old-Hollywood fake moonlight: dark, blue, desaturated (darkened by the tone curve, not Exposure) |
| Mars Holiday | foliage | Everything rust and dust |

("neutral" means pick snow, cloud or concrete.)

**White balance jumps to 2000 K:** the picked presets set it on purpose. A 590 nm raw is so red that some mixers black
out the spot before the picker can measure it, and it refuses. The pick cancels white balance anyway, so this doesn't
change the colours.

## Which LightCraft?

The presets need the Channel Mixer from
[storytold/lightcraft#3579](https://github.com/storytold/lightcraft/pull/3579). Until it's merged:

- **In your browser:** the [IR playground](https://darthnut.github.io/lightcraft-ir-recipes/) is a test build with the
  mixer and these presets already built in. Nothing to install.
- **On the desktop:** build the pull request's branch (you need [Rust](https://rustup.rs)):

  ```bash
  git clone --branch feat/channel-mixer https://github.com/darthnut/lightcraft.git lightcraft-mixer
  ```

  ```bash
  cd lightcraft-mixer
  ```

  ```bash
  cargo run --release -p lightcraft -- --library ~/lightcraft-mixer-test
  ```

  The `--library` folder keeps this test build away from your real LightCraft library.

## How they were made

- **Fitted to one photo.** The colours of snow, foliage and sky were measured in one raw from a Sony A6000 with a
  590 nm filter, each "wild" mixer was solved to send those colours to a target hue, and the result was checked by
  rendering it. Other filters, sensors and subjects will land differently.
- **Always pickable.** In every picked preset, each mixer row adds up to 100 %, which guarantees the picker can solve
  it, whatever the camera.

`make_recipes.py` generates `IR Recipes.lcpreset` and every file in `presets`: edit the numbers there, never a
`.lcpreset` by hand, then run

```bash
python make_recipes.py
```

A check on every push makes sure the committed files match what the script generates.

## Share yours

Got IR numbers from Photoshop, GIMP, Affinity, Capture One or another editor's channel mixer?
[Share them with this form](../../issues/new?template=share-recipe.yml). Good ones may become presets here, credited.

Made by darthnut with Claude (Anthropic). Licensed MIT or Apache-2.0, like LightCraft. The sample photos are by
darthnut, shared under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/): free to use and adapt with
credit, not for commercial use.
