# Feature: Pico Layout

Using the page at https://picocss.com/docs/group as a guide, implement a layout in Layout that matches this look:
- Navigation at the top in <header>
- Left aside that shows the tree of sections, subjects, and stories
    - All menus are collapsed
    - Except the current node
    - Do this without JavaScript
    - See the `<aside>` below for a PicoCSS example that doesn't need JS for collapse/expand
- In the middle a breadcrumbs area with the path to the current view
- The <main> area that shows the current view
- A footer with a copyright
- Put custom styling in storytime.css
- We already have the CSS from that site in pico-docs.css
- Use pytest-playwright for tests that require DOM interaction such as clicking
- But mark these tests as slow

Example aside:
```html
<aside>
  <nav>
    <details>
      <summary>Section 1</summary>
      <ul>
        <li><a href="#link1">Link 1</a></li>
        <li><a href="#link2">Link 2</a></li>
        <li><a href="#link3">Link 3</a></li>
      </ul>
    </details>
    <details>
      <summary>Section 2</summary>
      <ul>
        <li><a href="#link4">Link 4</a></li>
        <li><a href="#link5">Link 5</a></li>
      </ul>
    </details>
    <details open>
      <summary>Section 3 (Open by default)</summary>
      <ul>
        <li><a href="#link6">Link 6</a></li>
        <li><a href="#link7">Link 7</a></li>
      </ul>
    </details>
  </nav>
</aside>
```
