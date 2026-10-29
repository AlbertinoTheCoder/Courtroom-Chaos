"""Bundle the existing Windows package without saves, logs, or debug symbols."""
import hashlib
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[1]
runtime = root / 'Builds' / 'Windows'
output = root / 'Releases'
output.mkdir(exist_ok=True)
archive = output / 'CourtroomChaos-Windows-x64.zip'
assert (runtime / 'CourtSimulator.exe').is_file(), 'Package the game first.'
assert (root / 'CourtroomChaos.exe').is_file(), 'Build the root launcher first.'

with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
    bundle.write(root / 'CourtroomChaos.exe', 'CourtroomChaos.exe')
    bundle.writestr('READ ME.txt',
        'COURTROOM CHAOS\nJustice. With extra mustard.\n\n'
        'Extract the entire ZIP, then double-click CourtroomChaos.exe.\n'
        'Keep the Game folder beside the EXE. No Unreal Editor is needed.\n\n'
        'Three authored cases, offline synthetic voices, adaptive music, and three lives per attempt.\n'
        'Space: advance. Q: press. E: evidence. H: transcript. Escape: back/save.\n'
        'Skip Voice explicitly interrupts speech; Continue waits for it to finish.\n\n'
        'If prerequisites are requested, run Game/Engine/Extras/Redist/en-us/UEPrereqSetup_x64.exe.\n'
        'Windows x64 development build. Broader hardware testing remains future work.\n\n'
        'Source and bug reports: https://github.com/AlbertinoTheCoder/Courtroom-Chaos\n'
        'Audio credits: CREDITS.md\n')
    bundle.write(root / 'Documentation' / 'AudioCredits.md', 'CREDITS.md')
    for file in sorted(runtime.rglob('*')):
        if not file.is_file():
            continue
        relative = file.relative_to(runtime)
        if any(part.lower() == 'saved' for part in relative.parts):
            continue
        if file.suffix.lower() in {'.pdb', '.log', '.csv'} or file.name.startswith('Manifest_'):
            continue
        compression = zipfile.ZIP_STORED if file.suffix.lower() in {'.ucas', '.pak'} else zipfile.ZIP_DEFLATED
        bundle.write(file, 'Game/' + relative.as_posix(), compress_type=compression)
with zipfile.ZipFile(archive) as bundle:
    names = bundle.namelist()
    assert 'CourtroomChaos.exe' in names and 'Game/CourtSimulator.exe' in names
    assert 'Game/CourtSimulator/Binaries/Win64/CourtSimulator.exe' in names
    assert not any('/saved/' in name.lower() or name.lower().endswith('.pdb') for name in names)
    assert bundle.testzip() is None, 'Archive CRC verification failed.'
digest = hashlib.file_digest(archive.open('rb'), 'sha256').hexdigest()
(output / 'SHA256SUMS.txt').write_text(digest + '  ' + archive.name + '\n', encoding='ascii')
print(f'RELEASE_OK: {archive} ({archive.stat().st_size:,} bytes)', flush=True)
