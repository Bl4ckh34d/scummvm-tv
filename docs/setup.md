# Setup details

Create an atlantis target in ScummVM using the original German data directory; a .scummvm hook containing atlantis launches it directly. The registered target's path must point to the actual USB directory. Set savepath to a writable internal directory.

The TV build exposes native quicksave/quickload mapper actions. The example maps L3/R3 to SCUMM slot 1 and leaves L2 for frontend fast-forward. Start opens the ScummVM menu; View opens the virtual keyboard. Native quick actions are permitted only when the engine allows them. Generic RetroArch save states are unsupported. Reset restarts the game, after which R3 can load the native slot. Synchronous audio is selected for the tested Android RetroArch build to avoid its threaded-audio shutdown crash.

This recipe builds the library, not scummvm.zip. Install matching system assets from the pinned source dists/engine-data and gui/themes: scummmodern.zip, translations.dat and gui-icons.dat in the theme directory, fonts.dat in the extra directory. Match the configured themepath/extrapath in scummvm.ini. German menus need these fonts/resources. The config examples use a dedicated Atlantis system directory.

`config/Monkey1`, `config/Monkey2` and `config/Monkey3` contain content overrides, core options and target INI examples from the tested installation. Adjust every path for your device and place files in the locations named by the overrides. The optional `monkey_scummvm_libretro_android.so` filename is a copy of the same build, not a separate engine or repository. MI3 requires the included GL/GLES2 settings for the tested performance; all three examples disable the frontend's threaded audio pipeline to avoid the observed shutdown crash. Assets and game data are not included.
