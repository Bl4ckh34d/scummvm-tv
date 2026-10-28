# Follow-up verification — 2026-10-29

The repository's build script completed on Windows with NDK r27d using the pinned shared sources. Python scripts parse, and source patches pass both a forward check against a temporary pristine upstream index and a reverse check against the working source. Original game data, saves, screenshots and binaries are excluded from publication.

Build: `atlantis_libretro_android.so`, 8,661,436 bytes, SHA-256 `b1c769695b63cb00cfe1271322dd39910084bab175e29f13fa6e2e8fecd90e8b`.

The checked-in patch reproduces the byte-identical installed SCUMM build. Atlantis and Monkey Island I–III passed actual gameplay native save/load, Reset with subsequent loading, fast-forward and Close Content. MI3 uses GLES2; synchronous frontend audio avoids the observed Android shutdown crash. Skip restricted intro scenes before quickloading. This publication adds all required SCUMM source modifications and Monkey profile examples.

These are bounded checks on Android 11 ARMv7. They do not establish whole-campaign performance or subjective physical-controller feel. Earlier records below describe their own historical builds.

`tests/native_probe.cpp` is the real-core input driver used for isolated checks. Compile with the NDK ARMv7 C++ compiler, C++17, `-static-libstdc++`, the pinned libretro-common include directory and `-ldl`. Arguments are core path, system directory, content path, isolated save directory, core-options file and `--interactive`. Commands include `run N`, `pad ID`, `axis STICK AXIS VALUE FRAMES`, `reset N`, `ff 0|1` and `quit`; each produces a bounded PPM capture in the supplied save directory. Copy matching ScummVM assets and an INI pointing to the isolated saves. Use software rendering for this standalone driver; actual MI3 GLES2 acceptance was performed in RetroArch.

---

# Publication verification � 2026-10-28

The checked-in build recipe passed on Windows with Python/Git and NDK r27d, targeting ARMv7 API 21. Python scripts parse successfully. All patches pass forward checks against the pinned upstream index and reverse checks against the patched working tree.

Build: `atlantis_libretro_android.so`, 8659780 bytes, SHA256 `93bd5d6d08e7f8d5eac70f4374fc26e8bfbe1d34d02d922a24dace840149d804`. This identifies this verification build; paths and timestamps can affect rebuild hashes. Original game files, player saves and generated output are not included in Git.

Rebuilt hash is identical to the previously installed, gameplay-tested binary recorded in project evidence. Production core unchanged.
