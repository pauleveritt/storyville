# Raw Idea: Starlette App

Create a Starlette-based web app to serve Storyville portfolios from a built site. The app should:

1. Serve a built site from a `var` directory
2. Comment out/remove everything related to reloading functionality (focus on static serving first)
3. Tests should use tempdir fixture instead of the project root `var` directory
4. Properly serve the layout's static directory using `StaticFiles`
5. Handle potentially unusual static directory paths like `static/components/layout/static`
6. Determine whether the entire site should be a StaticFiles path or just the static assets

Starting point: `app.py` and `test_app.py` have broken beginnings that need to be fixed.
