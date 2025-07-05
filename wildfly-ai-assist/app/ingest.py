"""Download every page of a Confluence space and save as Markdown.

Run once, then rebuild whenever pages change:
    poetry run python -m app.ingest
"""

from pathlib import Path

from atlassian import Confluence
from slugify import slugify

from .config import get_settings

settings = get_settings()
OUT_DIR = Path("data/pages")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def export_space_to_markdown() -> None:
    """Iterate through the entire space and dump each page to `OUT_DIR`."""
    confluence = Confluence(
        url=settings.confluence_base_url,
        token=settings.confluence_token,
        cloud=True,
    )

    pages = confluence.get_all_pages_from_space(
        space=settings.confluence_space, limit=5_000
    )
    for page in pages:
        title = page["title"]
        # Fetch the raw storage format (XHTML); Confluence will convert later.
        raw = confluence.get_page_by_id(page["id"], expand="body.storage")["body"]["storage"]["value"]
        slug = slugify(title)
        (OUT_DIR / f"{slug}.md").write_text(raw)
        print(f"✓ exported '{title}'")


if __name__ == "__main__":  # pragma: no cover
    export_space_to_markdown()
    print("Done.")
