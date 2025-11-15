# Views

- A "View" accepts the resource that is being rendered
- It should return a `tdom.Element`
- It will have an HTML template, meaning `html(t'''<div>Some html</div>''')`
- That returns a `tdom.Node` butuse a type guard or some type narrowing, and have the view return a `tdom.Element`
  