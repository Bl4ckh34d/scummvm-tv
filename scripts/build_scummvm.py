"""Build the pinned SCUMM-only checkout with the Windows Android NDK."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCES = Path(os.environ.get("PORT_SOURCES_DIR", str(ROOT / "sources"))).resolve()
NDK_HOME = Path(os.environ.get("ANDROID_NDK_HOME", "C:/tools/android/android-ndk-r27d"))
SOURCE = SOURCES / 'scummvm'
REVISION = 'f11533e680532eb61e9123d00602f8cff9bb91db'
NDK = Path(os.environ.get('ANDROID_NDK_HOME', 'C:/tools/android/android-ndk-r27d'))

def main():
    revision = subprocess.check_output(['git', '-C', str(SOURCE), 'rev-parse', 'HEAD'], text=True).strip()
    if revision != REVISION:
        raise SystemExit(f'Expected {REVISION}, found {revision}')
    # Upstream's dependency configurator can delete/reset a mismatched checkout.
    # Refuse that situation before invoking make; preserve existing user work.
    for dependency in json.loads((ROOT / 'dependencies.json').read_text())[1:]:
        path = SOURCES / dependency['path']
        if not (path / '.git').exists():
            raise SystemExit('Missing dependency; run scripts/fetch_sources.py first')
        for arguments, expected in [(['rev-parse', 'HEAD'], dependency['revision']),
                                    (['remote', 'get-url', 'origin'], dependency['url'])]:
            actual = subprocess.check_output(['git', '-C', str(path), *arguments], text=True).strip()
            if actual != expected:
                raise SystemExit(f'Unexpected dependency checkout: {path}')
        if subprocess.check_output(['git', '-C', str(path), 'status', '--porcelain'], text=True).strip():
            raise SystemExit(f'Dirty dependency; preserve changes before building: {path}')
    engines = [p.parent.name for p in (SOURCE / 'engines').glob('*/configure.engine')]
    if sorted(engines) != ['scumm']:
        raise SystemExit('This recipe requires the SCUMM-only sparse checkout in dependencies.json')
    env = os.environ.copy()
    env['PATH'] = 'C:/Program Files/Git/usr/bin;C:/Program Files/Git/bin;' + env['PATH']
    args = [str(NDK / 'prebuilt/windows-x86_64/bin/make.exe'), '-O',
            '-f', str(NDK / 'build/core/build-local.mk'),
            'SHELL=C:/Progra~1/Git/bin/sh.exe', 'HOST_OS=cygwin', 'HOST_OS_BASE=windows', 'NDK_PROJECT_PATH=.',
            'APP_BUILD_SCRIPT=Android.mk', 'NDK_APPLICATION_MK=Application.mk',
            'NDK_OUT=' + Path(os.path.relpath(ROOT / 'build/scummvm-armv7/obj', SOURCE / 'backends/platform/libretro/jni')).as_posix(),
            'NDK_LIBS_OUT=' + Path(os.path.relpath(ROOT / 'build/scummvm-armv7/libs', SOURCE / 'backends/platform/libretro/jni')).as_posix(),
            'APP_ABI=armeabi-v7a', 'APP_PLATFORM=android-21',

            'USE_MAD=0', 'USE_FLUIDSYNTH=0', 'USE_MT32EMU=0',
            'APP_CPPFLAGS=-DUSE_SJIS', 'APP_SHORT_COMMANDS=true', '-j4', 'installed_modules']
    if '--verbose' in sys.argv:
        args.append('V=1')
    log = ROOT / 'evidence/scummvm-build.log'
    log.parent.mkdir(exist_ok=True)
    log.parent.mkdir(exist_ok=True)
    (ROOT / 'release').mkdir(exist_ok=True)
    with log.open('w', encoding='utf-8') as output:
        process = subprocess.Popen(args, cwd=SOURCE / 'backends/platform/libretro/jni', env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                   encoding='utf-8', errors='replace')
        for line in process.stdout:
            output.write(line)
            output.flush()
            if any(word in line for word in ('error:', 'Error ', 'failed', 'Install ', 'SharedLibrary')):
                print(line[:500], end='', flush=True)
        code = process.wait()
    if code:
        print(f'Build failed ({code}); see {log}')
        return code
    built = ROOT / 'build/scummvm-armv7/libs/armeabi-v7a/libretro.so'
    target = ROOT / 'release/atlantis_libretro_android.so'
    target.parent.mkdir(exist_ok=True)
    shutil.copyfile(built, target)
    subprocess.run([str(NDK / 'toolchains/llvm/prebuilt/windows-x86_64/bin/llvm-strip.exe'),
                    '--strip-unneeded', str(target)], check=True)
    print(f'Built {target} ({target.stat().st_size} bytes)')
    return 0

if __name__ == '__main__':
    sys.exit(main())
