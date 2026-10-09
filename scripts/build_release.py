"""Build a verified, reproducible ZIP containing only manifest-listed public resources."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile
from check_package import check


def build(output):
    root = Path(__file__).resolve().parent.parent
    output = Path(output).expanduser().resolve()
    if output == root or output.is_relative_to(root) or output.suffix.lower() != '.zip':
        raise ValueError('Choose a .zip output outside the Skill directory')
    check(root)
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    output.parent.mkdir(parents=True, exist_ok=True)
    created = False
    try:
        with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
            created = True
            for rel in sorted([*manifest['files'], 'manifest.json']):
                info = zipfile.ZipInfo('xuxiaoyu-skill/' + rel, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, (root / rel).read_bytes(), compress_type=zipfile.ZIP_DEFLATED)
        with tempfile.TemporaryDirectory(prefix='xuxiaoyu-zip-check-') as td:
            with zipfile.ZipFile(output) as archive:
                if archive.testzip() is not None:
                    raise ValueError('ZIP CRC check failed')
                archive.extractall(td)
            check(Path(td) / 'xuxiaoyu-skill')
    except Exception:
        if created:
            output.unlink(missing_ok=True)
        raise
    return {'zip': str(output), 'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
            'bytes': output.stat().st_size, 'version': manifest['version'],
            'files': len(manifest['files']) + 1, 'extracted_package': 'verified'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.output), ensure_ascii=False, indent=2))
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        parser.exit(1, 'Build failed: ' + str(exc) + '\n')
