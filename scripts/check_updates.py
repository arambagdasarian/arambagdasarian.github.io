"""Build synthetic posts in a temporary source outside the public repository."""
from pathlib import Path
from tempfile import TemporaryDirectory
import os
import shutil
import subprocess
from check_site import check

repo = Path(__file__).resolve().parents[1]
with TemporaryDirectory(prefix="aram-site-check-") as tmp:
    source, output = Path(tmp) / "source", Path(tmp) / "output"
    shutil.copytree(repo, source, ignore=shutil.ignore_patterns(
        ".git", ".bundle", "vendor", "_site", ".jekyll-cache", "__pycache__", "node_modules"
    ))
    # Isolate the synthetic archive from any real posts.
    shutil.rmtree(source / "_posts")
    (source / "_posts").mkdir()
    for day in range(1, 7):
        (source / "_posts" / f"2000-01-{day:02d}-fixture-{day}.md").write_text(
            f'---\ntitle: "Fixture {day}"\ndate: 2000-01-{day:02d} 12:00:00 -0500\n'
            'summary: "Local verification only."\nupdated: 2000-02-01\n---\n'
            'A paragraph with **Markdown**.\n\n## A section\n\n'
            '[CV]({{ site.cv_path | relative_url }})\n'
        )
    (source / "_posts" / "2999-01-01-future-fixture.md").write_text(
        '---\ntitle: Future fixture\ndate: 2999-01-01\n---\nFuture content.\n'
    )
    (source / "_posts" / "2000-01-07-unpublished-fixture.md").write_text(
        '---\ntitle: Unpublished fixture\npublished: false\n---\nUnpublished content.\n'
    )
    (source / "_drafts").mkdir(exist_ok=True)
    (source / "_drafts" / "draft-fixture.md").write_text(
        '---\ntitle: Draft fixture\n---\nDraft content.\n'
    )
    subprocess.run([
        "bundle", "exec", "jekyll", "build", "--source", str(source),
        "--destination", str(output), "--baseurl", "/path-test", "--strict_front_matter"
    ], cwd=repo, env={**os.environ, "JEKYLL_ENV": "production"}, check=True)
    home = (output / "index.html").read_text()
    archive = (output / "updates/index.html").read_text()
    assert home.count('class="update-title"') == 4
    assert archive.count('class="update-title"') == 6
    assert home.index("Fixture 6") < home.index("Fixture 5") < home.index("Fixture 4") < home.index("Fixture 3")
    assert "Fixture 2" not in home and "Fixture 1" not in home
    for path in output.rglob("*"):
        if path.is_file() and path.suffix in (".html", ".xml"):
            text = path.read_text()
            for title in ("Future fixture", "Unpublished fixture", "Draft fixture"):
                assert title not in text, f'{title} appeared in {path}'
    post = (output / "updates/2000-01-06-fixture-6/index.html").read_text()
    assert "<strong>Markdown</strong>" in post
    assert "January 6, 2000" in post and "February 1, 2000" in post
    assert "/path-test/updates/" in post
    check(output, "https://arambagdasarian.github.io", "/path-test")
print("Verified automatic recent posts and archive, stable post URLs, Markdown, dates, base paths, and draft/future exclusion.")
