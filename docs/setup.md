# Setup details

Create an atlantis target in ScummVM using the original German data directory; a .scummvm hook containing atlantis launches it directly. The registered target's path must point to the actual USB directory. Set savepath to a writable internal directory.

This recipe builds the library, not scummvm.zip. Install matching system assets from the pinned source dists/engine-data and gui/themes: scummmodern.zip, translations.dat and gui-icons.dat in the theme directory, fonts.dat in the extra directory. Match the configured themepath/extrapath in scummvm.ini. German menus need these fonts/resources. The config examples use a dedicated Atlantis system directory.
