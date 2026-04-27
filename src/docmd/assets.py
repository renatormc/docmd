from pathlib import Path


def collect_assets(assets_path: Path) -> dict[str, dict]:
    assets: dict[str, dict] = {}
    if not assets_path.is_dir():
        return assets
    for f in sorted(assets_path.iterdir()):
        if f.is_file():
            assets[f.stem] = {"path": f, "caption": ""}
    return assets
