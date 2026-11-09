"""Builds IR Recipes.lcpreset (all fifteen) and presets/<group>/<id>.lcpreset (one each): channel-mixer looks for a 590 nm infrared camera.
Every recipe that wants a neutral pick has mixer rows summing to 100 %, so the picker can always solve it."""
import json, os, sys

def mix(r, g, b):
    row = lambda v: {"red": v[0], "green": v[1], "blue": v[2]}
    return {"red": row(r), "green": row(g), "blue": row(b)}

SWAP = mix([0, 0, 100], [0, 100, 0], [100, 0, 0])
C, W, S = "IR Recipes 1 · Classic", "IR Recipes 2 · Wild", "IR Recipes 3 · Silly"
# (id, group, name, pick, settings)  pick: "foliage" | "neutral" | None (mixers solved from DSC03220's measured snow/foliage/sky) — what the Channel Mixer picker should be clicked on
R = [
 ("classic-swap", C, "Classic Swap: pink foliage, teal sky (pick snow/cloud/concrete)", "neutral",
  {"channel_mixer": SWAP, "color": {"vibrance": 15}}),
 ("hood-river-pink", C, "Hood River Pink (pick snow/cloud/concrete)", "neutral",
  {"channel_mixer": SWAP, "color": {"vibrance": 35, "saturation": 7},
   "mixer": {"magenta": {"hue": 100}, "purple": {"hue": 100}}, "curve": {"darks": 19, "highlights": -36}}),
 ("white-foliage", C, "White Foliage, Blue Sky (pick foliage)", "foliage",
  {"channel_mixer": mix([-40, 0, 140], [50, -20, 70], [0, 30, 70]), "color": {"vibrance": 10}}),
 ("gold-foliage", C, "Gold Foliage, Blue Sky (pick snow/cloud/concrete)", "neutral",
  {"channel_mixer": mix([-20, 0, 120], [60, 0, 40], [140, 90, -130]), "color": {"vibrance": 10}}),
 ("pastel", C, "Soft Pastel, half swap (pick snow/cloud/concrete)", "neutral",
  {"channel_mixer": mix([40, 0, 60], [0, 100, 0], [60, 0, 40]), "color": {"vibrance": 20},
   "light": {"contrast": -15}, "grading": {"highlights": {"hue": 330, "sat": 8}, "shadows": {"hue": 200, "sat": 10}}}),
 ("mono-wood", C, "IR Mono, Wood Effect (no pick)", None,
  {"channel_mixer": mix([100, 0, 0], [100, 0, 0], [100, 0, 0]), "light": {"contrast": 35}, "effects": {"clarity": 15}}),
 ("mono-glow", C, "IR Mono, Soft Glow (no pick)", None,
  {"channel_mixer": mix([100, 0, 0], [100, 0, 0], [100, 0, 0]), "light": {"contrast": 10}, "effects": {"clarity": -30}}),
 ("aerochrome", W, "Faux Aerochrome: red foliage, blue sky (pick snow/cloud/concrete)", "neutral",
  {"channel_mixer": mix([-10, -30, 140], [10, 150, -60], [140, 90, -130]), "color": {"vibrance": 10}}),
 ("fake-summer", W, "Fake Summer: green foliage (pick snow/cloud/concrete)", "neutral",
  {"channel_mixer": mix([-170, 140, 130], [-30, 20, 110], [20, 110, -30])}),
 ("teal-forest", W, "Teal Forest, Orange Sky (pick snow/cloud/concrete)", "neutral",
  {"channel_mixer": mix([80, 90, -70], [10, -10, 100], [-150, 50, 200])}),
 ("lava", W, "Lava Fields: orange-red foliage, violet sky (pick snow/cloud/concrete)", "neutral",
  {"channel_mixer": mix([80, -30, 50], [-70, 100, 70], [130, 50, -80]), "color": {"vibrance": 15}}),
 ("alien", W, "Alien Planet: purple trees, green sky (pick snow/cloud/concrete)", "neutral",
  {"channel_mixer": mix([0, 20, 80], [130, 110, -140], [30, -10, 80])}),
 ("night-vision", S, "Night Vision Goggles (no pick)", None,
  {"channel_mixer": mix([20, 0, 0], [100, 0, 0], [20, 0, 0]), "light": {"contrast": 35},
   "vignette": {"amount": -60}, "grain": {"amount": 45}}),
 ("day-for-night", S, "Day for Night (pick snow/cloud/concrete)", "neutral",
  {"channel_mixer": SWAP, "light": {"exposure": -1.8, "contrast": 20}, "color": {"saturation": -40},
   "grading": {"global": {"hue": 220, "sat": 35}}}),
 ("mars", S, "Mars Holiday (pick foliage)", "foliage",
  {"channel_mixer": mix([120, 0, -20], [40, 60, 0], [0, 30, 70]), "grading": {"global": {"hue": 22, "sat": 40}},
   "color": {"vibrance": 20}}),
]

def slug(s):
    out = "".join(c.lower() if c.isascii() and c.isalnum() else "-" for c in s)
    return "-".join(w for w in out.split("-") if w)


def write(path, presets):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"format": "lightcraft.preset", "version": 1, "presets": presets}, f, indent=2)


if __name__ == "__main__":
    # A fixed low white balance under every picked recipe: the pick cancels white balance (it is diagonal), so this
    # doesn't change the result, but the raw is so red that without it some mixers black the spot out and the picker
    # refuses it ("pick a brighter, less saturated area"). Measured on DSC03220: as-shot fails two recipes, 2000 K / 0 none.
    WB = {"mode": "custom", "temp": 2000, "tint": 0}
    presets = [{"id": f"ir-recipe-{i}", "name": n, "group": g, "settings": ({"wb": WB} if p else {}) | s} for i, g, n, p, s in R]
    # Writes, under the folder given (default: here), all fifteen in one file to install everything, and each on its
    # own under presets/<group>/. A preset keeps its group either way, and importing one that is already installed
    # (same name, group and settings) is skipped, so the two can be mixed.
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    write(os.path.join(root, "IR Recipes.lcpreset"), presets)
    groups = {g: f"{k}-{slug(g.split('·')[-1])}" for k, g in enumerate([C, W, S], 1)}
    for (i, g, *_), p in zip(R, presets):
        write(os.path.join(root, "presets", groups[g], f"{i}.lcpreset"), [p])
    json.dump([[i, n, p] for i, _, n, p, _ in R], sys.stdout)
