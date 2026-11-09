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
 ("mt-hood-pink", C, "Mt Hood Pink (pick snow/cloud/concrete)", "neutral",
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
  # dark by the tone curve and grading, not Exposure (which stays the photographer's): about what -1.8 EV gave
  {"channel_mixer": SWAP, "light": {"contrast": 20}, "color": {"saturation": -40},
   "curve": {"highlights": -100, "lights": -100, "darks": -80, "shadows": -60},
   "grading": {"global": {"hue": 220, "sat": 35, "lum": -60}}}),
 ("mars", S, "Mars Holiday (pick foliage)", "foliage",
  {"channel_mixer": mix([120, 0, -20], [40, 60, 0], [0, 30, 70]), "grading": {"global": {"hue": 22, "sat": 40}},
   "color": {"vibrance": 20}}),
]

def slug(s):
    out = "".join(c.lower() if c.isascii() and c.isalnum() else "-" for c in s)
    return "-".join(w for w in out.split("-") if w)


def leaves(d, path=()):
    for k, v in d.items():
        if isinstance(v, dict):
            yield from leaves(v, path + (k,))
        else:
            yield path + (k,)


def put(d, path, v):
    for k in path[:-1]:
        d = d.setdefault(k, {})
    d[path[-1]] = v


def with_neutrals(settings, shared):
    """`settings` plus every setting in `shared` it doesn't name, at its neutral value (0 for all of them: what a
    freshly imported photo has). So switching from one preset to another never leaves the first one's extras behind
    (Day for Night's grading, Night Vision's vignette and grain...). Exposure is in no preset, so it stays yours."""
    out = json.loads(json.dumps(settings))
    named = set(leaves(settings))
    for path in shared:
        if path not in named:
            put(out, path, 0)
    return out


def write(path, presets):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"format": "lightcraft.preset", "version": 1, "presets": presets}, f, indent=2)


if __name__ == "__main__":
    # A fixed low white balance under every picked recipe: the pick cancels white balance (it is diagonal), so this
    # doesn't change the result, but the raw is so red that without it some mixers black the spot out and the picker
    # refuses it ("pick a brighter, less saturated area"). Measured on DSC03220: as-shot fails two recipes, 2000 K / 0 none.
    WB = {"mode": "custom", "temp": 2000, "tint": 0}
    # The no-pick recipes set the camera's white balance back, so one applied after a picked recipe doesn't keep 2000 K.
    AS_SHOT = {"mode": "asShot"}
    # Every setting any recipe names, besides the mixer and white balance (which every recipe sets): each recipe names
    # them all, its own value or neutral. Settings no recipe touches (sharpening, noise, lens, crop...) are left alone.
    shared = sorted({path for *_, s in R for path in leaves(s) if path[0] != "channel_mixer"})
    assert ("light", "exposure") not in shared, "Exposure is the photographer's: no recipe may set it"
    presets = [{"id": f"ir-recipe-{i}", "name": n, "group": g, "settings": {"wb": WB if p else AS_SHOT} | with_neutrals(s, shared)}
               for i, g, n, p, s in R]
    # Writes, under the folder given (default: here), all fifteen in one file to install everything, and each on its
    # own under presets/<group>/. A preset keeps its group either way, and importing one that is already installed
    # (same name, group and settings) is skipped, so the two can be mixed.
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    write(os.path.join(root, "IR Recipes.lcpreset"), presets)
    groups = {g: f"{k}-{slug(g.split('·')[-1])}" for k, g in enumerate([C, W, S], 1)}
    for (i, g, *_), p in zip(R, presets):
        write(os.path.join(root, "presets", groups[g], f"{i}.lcpreset"), [p])
    json.dump([[i, n, p] for i, _, n, p, _ in R], sys.stdout)
