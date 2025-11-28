# Raw Idea

Full static paths. I would like any layout/component/view to define its own `static` folder which gets copied into the output_dir. To prevent filename collisions, and to make it clear where each asset came from, I would like to preserve the path to the static directory. Meaning, the output_dir should have `static/components/layout/static/` as a directory. The rendered paths should then point to the correct static asset.
