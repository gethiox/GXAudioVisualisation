# GXAudioVisualisation (GxAV)
Generate Audio Visualization in Blender!  
Check user guide on the [wiki page](https://github.com/gethiox/GXAudioVisualisation/wiki).

Also you can see promotion video:
[![GxAV youtube video](https://img.youtube.com/vi/cXTEqtcLDKU/0.jpg)](https://youtu.be/cXTEqtcLDKU)

## TODO:
- [x] Prepare GitWiki
- [x] Make script as addon
- [x] More dynamic, adjusting options manipulate visiblo objects in
      realtime
- [ ] Integrated one-click-visualizer option for Blender internal
      and Cycles renderer
- [ ] Predefined visualizer scenes (normal, cicrle, particle effects,
      camera movements)
- [ ] Some more features
- [ ] Independed (and better) bake algorithm of internal bake function
- [ ] [Peak feature](http://youtu.be/ZOYp0FfVE4Q)

## How to build:
Just zip `GxAV` folder and your addon is ready to instal inside Blender.  
You can also run `./tools/build.sh` under Linux.

### Changelog
#### 21.08.2014 - 1.0 STABLE \o/ ####
- 'Tercja bake engine' has been fully implemented, many thanks to
  [Xevaquor](https://github.com/Xevaquor) for tercja.py module
- Interface improvements
- That's all folks, patches are welcome

#### 09.08.2014 - 0.99v RC4 ####
- Interface improvements

#### 30.07.2014 - 0.99v RC3 ####
- In-terminal bake progress information for debugging purpose
- Added 'slash' visualizer shape feature

#### 26.07.2014 - 0.99v RC2 ####
- All known bugs fixed \o/
- Added separated box for 'Bake sound to F-Curves' method variables

#### 25.07.2014 - 0.99v RC1 ####
- Fix a few bugs
- Added two visualisation modes - object and center object
- Optimisations
- Improved panel usability

#### 25.07.2014 - 0.93v beta ####
- Panel interface adjustments - now you don't need to press "init
  variables" anymore, yay \o/

#### 24.07.2014 - 0.92v beta ####
- Added dynamically changed driver-power control slider
- initial implementation of sound-accurate bake algorithm, temporarily
  named "tercja"
  ([wikipedia](https://pl.wikipedia.org/wiki/Tercja_(akustyka)) \[POL\])

#### 22.07.2014 - 0.91v beta ####
- Reorganized panel interface
- Added Logarithm bake mode
- min/max freq works well
- Still a little bit buggy, chaos in the code
- Added usage guide in the Wiki

#### 21.07.2014 - 0.9v beta ####
- Initial version of a new, re-writed script (very basic features)
- Now script can be loaded as addon (accessed by properties_window>scene)
- Dynamic interface that changes visible objects in realtime
- Script still needed more features and many optimizations

#### 11.02.2014 - 0.5v ####
- Added two visualisation modes - cube_scale and center_cube_scale
- Added "debug mode" - generate additional empty objects with
  frequency in name
- Added PANEL INTERFACE!!!! sadfsjfhasfgdsagfagsfjhsfjas

#### Unknown Date ####
- Script still needed to be run in text editor, no addon-mode yet
- Agrh (api change, bpy.context restrictions)
- Who knows if I ever bring it to life