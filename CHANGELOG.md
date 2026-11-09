# Changelog

## 1.1.1

- **Hood River Pink is now Mt Hood Pink** (file `mt-hood-pink.lcpreset`). Same settings.

## 1.1.0

- **Presets replace each other cleanly.** Every preset now sets the same settings: the mixer, white balance and every
  tone and colour setting any preset uses, at zero when it doesn't use one. Before, a preset left behind whatever an
  earlier one set that it didn't: Day for Night's grading and darkening, Night Vision's vignette and grain, a picked
  preset's 2000 K under IR Mono. The no-pick presets now set the camera's own white balance.
- **No preset changes Exposure.** Day for Night got its darkness from Exposure −1.8, which stayed behind after
  switching and overwrote the Exposure you'd set after a pick. It's now dark through the tone curve and colour
  grading instead, at about the same brightness.

## 1.0.0

The first release: fifteen presets in three groups (Classic, Wild, Silly), as one file to install everything and
one file each, moved here from
[darthnut/lightcraft-ir-recipes](https://github.com/darthnut/lightcraft-ir-recipes), which keeps the browser
playground.

- Made for the Channel Mixer in [storytold/lightcraft#3579](https://github.com/storytold/lightcraft/pull/3579) as of
  its "Neutral picker keeps the spot's own brightness" change: the picker never changes Exposure, so after a pick
  you set Exposure yourself.
