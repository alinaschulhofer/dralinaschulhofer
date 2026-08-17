# Blog posts

Each post is one JSON file in this folder. To publish a post:

1. Add a file here, e.g. `src/posts/my-post-slug.json` (filename doesn't matter — `slug` inside the file controls the URL).
2. Run `python3 src/build_blog.py` from the repo root.
3. Commit the new JSON file *and* the regenerated `blog.html` + `<slug>.html` at the repo root together.

## Schema

```json
{
  "slug": "my-post-slug",
  "title": "Post Title",
  "date": "2026-08-17",
  "tag": "Psychology",
  "excerpt": "One or two sentences used on the blog index card and as the meta description.",
  "subtitle": "Optional italic sub-line shown under the title on the post page.",
  "pull_quote": "Optional short pull-quote rendered in large gold italic mid-article.",
  "body": [
    "First paragraph. Plain text or simple inline HTML like <em>this</em> or <a href=\"...\">a link</a> is fine — each array entry becomes one <p>.",
    "Second paragraph.",
    "..."
  ]
}
```

- `slug` — lowercase, hyphenated, must be unique and must not collide with an existing page filename (`about`, `services`, `faq`, `coaching`, `blog`, `index`, etc.).
- `date` — ISO `YYYY-MM-DD`. Posts are sorted newest-first on the index by this field.
- `tag` — short category label shown next to the date (e.g. `Psychology`, `Performance`, `Leadership`, `Relationships`).
- `body` — one array entry per paragraph. **Use Alina's own wording verbatim — never paraphrase or invent clinical content** (per `HANDOFF.md` §6/§9).

Required fields: `slug`, `title`, `date`, `tag`, `excerpt`, `body`. `subtitle` and `pull_quote` are optional.
