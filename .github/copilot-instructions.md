# Project Guidelines

## Architecture
- This repository is a small Jekyll site. Root pages such as `index.html` and `news.html` use YAML front matter and render through `_layouts/default.html` plus shared partials in `_includes/`.
- Put shared markup changes in `_includes/` or `_layouts/`. Keep page-specific content in the page file or `_posts/`.
- Treat `assets/vendor/` as third-party code. Prefer changes in `assets/css/main.css`, `assets/js/main.js`, or the templates instead of editing vendored libraries.
- The `junk/` directory contains duplicate or archival copies of site files. Unless the task explicitly targets it, make changes in the root site files instead.

## Build And Test
- Install Ruby dependencies with `bundle install`.
- Run the site locally with `bundle exec jekyll serve`.
- A Docker workflow is also available via `docker-compose up`, which serves the site on port `4001`.
- There is no automated test suite in this repo. Validate changes by building or serving the site and checking the affected pages manually.

## Conventions
- Use `{{ site.baseurl }}` for internal asset and page URLs in templates.
- Keep Jekyll front matter valid on every page and post. Broken YAML will break rendering.
- Contact details are populated at runtime from `data.json` by the script in `_includes/head.html`, using CSS classes such as `mu-email`, `mu-phone`, and `mu-address`. When changing contact content, keep the JSON data and the expected class names in sync.
- Preserve the existing BootstrapMade Day template structure and Bootstrap-based class patterns unless the task calls for a broader redesign.