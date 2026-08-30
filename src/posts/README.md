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
  "body": [
    "<p>First paragraph.</p>",
    "<h2>A section heading</h2>",
    "<p>Second paragraph, with <em>emphasis</em> or <strong>bold</strong> inline.</p>",
    "<ul><li>A bullet point</li><li>Another bullet point</li></ul>",
    "<p class=\"article-pull\">A short pull-quote or epigraph, rendered large and gold.</p>"
  ]
}
```

- `slug` — lowercase, hyphenated, must be unique and must not collide with an existing page filename (`about`, `services`, `faq`, `coaching`, `blog`, `index`, etc.).
- `date` — ISO `YYYY-MM-DD`. Posts are sorted newest-first on the index by this field.
- `tag` — short category label shown next to the date (e.g. `Psychology`, `Performance`, `Leadership`, `Relationships`).
- `body` — **each array entry is a raw HTML block, inserted as-is** (not auto-wrapped in `<p>`). Use `<p>`, `<h2>` (major section break), `<h3>` (numbered/minor sub-section), `<ul><li>...</li></ul>`, and `<p class="article-pull">...</p>` for a standout quote — plus inline `<em>`/`<strong>` as needed. For a References section, wrap it as:
  ```html
  "<div class=\"prose-refs\"><p class=\"eyebrow\">References</p><p>Citation one.</p><p>Citation two.</p></div>"
  ```
- **Use Alina's own wording verbatim — never paraphrase or invent clinical content** (per `HANDOFF.md` §6/§9). Only the semantic HTML wrapping (which words become a heading vs. a paragraph vs. a list) is something Claude adds — the words themselves must be unchanged from what she provided.

Required fields: `slug`, `title`, `date`, `tag`, `excerpt`, `body`. `subtitle` is optional.
