# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed - BREAKING

- **Project renamed from Storytime to Storyville**: The entire project has been renamed to "Storyville". This includes the package name, import statements, and all documentation. The PyPI package name is now `storyville` and all imports should use `from storyville` or `import storyville`.

#### Migration Guide for Project Rename

To update your code for this breaking change:

1. **Installation**: Install the new package name:
   ```bash
   # Uninstall old package
   pip uninstall storytime

   # Install new package
   pip install storyville
   ```

2. **Import statements**: Change all imports from `storytime` to `storyville`:
   ```python
   # Before
   from storytime import Catalog, Story, Subject, Section
   from storytime.catalog import make_catalog

   # After
   from storyville import Catalog, Story, Subject, Section
   from storyville.catalog import make_catalog
   ```

3. **CLI commands**: Use the new `storyville` command:
   ```bash
   # Before
   storytime serve my_package
   storytime build my_package dist/

   # After
   storyville serve my_package
   storyville build my_package dist/
   ```

- **Site renamed to Catalog throughout the codebase**: The main organizational concept has been renamed from "Site" to "Catalog" to better reflect its purpose as a browseable collection of components. This is a breaking change that affects all projects using Storyville.

#### Migration Guide

To update your code for this breaking change:

1. **Import statements**: Change all imports from `storyville.site` to `storyville.catalog`:
   ```python
   # Before
   from storyville.site import Site, make_site
   from storyville import Site

   # After
   from storyville.catalog import Catalog, make_catalog
   from storyville import Catalog
   ```

2. **Class names**: Rename `Site` to `Catalog` in your code:
   ```python
   # Before
   site = Site(title="My Component Library")

   # After
   catalog = Catalog(title="My Component Library")
   ```

3. **Function names**: Update function calls:
   ```python
   # Before
   def this_site() -> Site:
       return make_site(...)

   # After
   def this_catalog() -> Catalog:
       return make_catalog(...)
   ```

4. **View classes**: Rename `SiteView` to `CatalogView`:
   ```python
   # Before
   from storyville.site import SiteView

   # After
   from storyville.catalog import CatalogView
   ```

5. **Type hints**: Update all type hints from `Site` to `Catalog`:
   ```python
   # Before
   def my_function(site: Site) -> None:
       pass

   # After
   def my_function(catalog: Catalog) -> None:
       pass
   ```

6. **Variable names**: Update variable names from `site` to `catalog` throughout your codebase

The hierarchy terminology is now: **Catalog → Section → Subject → Story**

## [0.1.0] - Previous Release

Initial alpha release of Storyville.
