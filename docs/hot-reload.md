# Hot Reload with Subinterpreters

Storyville provides true hot reload using Python 3.14+ subinterpreters. When you save a `stories.py` file, your changes appear instantly in the browser—no server restart needed.

## Why Subinterpreters?

Python's import system caches modules. Simply re-importing doesn't reload changes. Traditional solutions (importlib.reload, sys.modules manipulation) are fragile and error-prone.

**Subinterpreters solve this:**
- Each build runs in a fresh, isolated interpreter
- Modules are imported cleanly every time
- No cache pollution or stale imports
- True module isolation

## Architecture

### Interpreter Pool

Storyville maintains a pool of 2 subinterpreters:
- **Active interpreter**: Running the current build
- **Standby interpreter**: Pre-warmed and ready

When a file changes:
1. Pull standby interpreter from pool
2. Execute build in that interpreter
3. Discard used interpreter
4. Warm up a replacement

This approach:
- Minimizes latency (standby is pre-warmed)
- Ensures clean state (interpreters are single-use)
- Maintains pool size automatically

### Pre-warming Strategy

New interpreters pre-import common modules:
- `storyville` - Core framework
- `tdom` - Templating library

This reduces first-build latency in each interpreter.

## Usage

### Enable Subinterpreters (Default)

```bash
# Subinterpreters enabled by default
storyville serve my_project
```

### Disable Subinterpreters

```bash
# Use direct builds (faster but no module reload)
storyville serve my_project --no-use-subinterpreters
```

**When to disable:**
- Quick testing without needing hot reload
- Debugging import issues
- Profiling build performance

## File Watching

Storyville watches for changes in:
- `stories.py` files
- Python source files in your package
- Template files (if using custom templates)

When a change is detected:
1. Debounce (wait for rapid changes to settle)
2. Pull interpreter from pool
3. Run build in subinterpreter
4. Write output to disk
5. Broadcast WebSocket reload signal
6. Browser refreshes automatically

### Watched Paths

By default, watches:
- Package directory (where your stories are)
- All Python files recursively

### Debouncing

Changes are debounced with a small delay to avoid rebuilding on rapid successive saves (e.g., editor auto-save).

## WebSocket Live Reload

The browser connects via WebSocket to receive reload signals.

**Flow:**
1. File changes detected
2. Build succeeds
3. Server broadcasts `{"type": "reload"}` 
4. Browser receives message
5. Page reloads automatically

**No reload on build failure:**
- Errors are logged to console
- Browser stays on current (working) version
- Watch continues for next change

## Performance

### Benchmarks

From performance testing with `examples.huge` (300 stories):
- **Cold start**: ~450-500ms (first build in interpreter)
- **Warm start**: Similar (pre-warming helps)
- **Overhead**: Minimal (~5-10ms interpreter management)

### Pool Size

Fixed at 2 interpreters:
- 1 active + 1 standby
- Balance between memory and latency
- Tested to be optimal for development workflow

## Compatibility

### Requirements

- **Python 3.14+** - Subinterpreters require PEP 684
- **Modern OS** - Linux, macOS, Windows (all support subinterpreters)

### Limitations

**Cannot use with:**
- C extensions with global state (rare in practice)
- Modules that don't support multiple interpreters

**Storyville's dependencies are compatible:**
- tdom ✅
- Starlette ✅  
- PicoCSS (CSS, no Python) ✅

## Development Workflow

### Typical Session

```bash
# 1. Start server (subinterpreters enabled by default)
storyville serve my_project

# 2. Edit stories.py in your editor
# 3. Save file
# 4. Browser auto-refreshes with changes!
```

### Hot Reload in Action

```python
# Before (in stories.py)
Story(props=dict(text="Old Text"))

# Save and edit
Story(props=dict(text="New Text"))

# Browser shows "New Text" immediately after save!
```

### Debugging

```bash
# Watch console for build events
storyville serve my_project

# Output shows:
INFO:     storyville.watchers - File change detected: stories.py
INFO:     storyville.build - Building catalog...
INFO:     storyville.build - Build complete
```

## CLI vs Web Server

### Web Server (Default)

```bash
storyville serve my_project
# Uses subinterpreters + hot reload + WebSocket
```

### One-time Build

```bash
storyville build my_project ./output
# Direct build (no subinterpreters, no watching)
```

**Build command:**
- Runs once and exits
- No file watching
- No server
- No subinterpreter overhead
- Fastest for CI/CD

## Error Handling

### Build Failures

When a build fails:
1. Error is logged to console
2. Browser keeps current version
3. Watcher continues running
4. Next save triggers new build attempt

```python
# Syntax error in stories.py
Story(props=dict(text="Oops" # Missing closing paren

# Console shows:
ERROR: Build failed: SyntaxError...
# Browser unchanged, watcher still active
```

### Import Errors

```python
# Missing import
from nonexistent import Something

# Console shows clear error:
ERROR: Could not import module: nonexistent
# Fix the import, save, auto-rebuilds!
```

### Recovery

Just fix the error and save—watcher automatically tries again.

## Advanced: Custom Warm-up

While not configurable, understanding the warm-up can help debug issues:

```python
# What gets pre-imported (internal)
def _warmup_interpreter():
    import storyville
    import tdom
```

These are the core modules needed for every build. Pre-importing them reduces latency.

## Comparison to Alternatives

### importlib.reload()

**Problems:**
- Doesn't reload transitive dependencies
- Leaves stale references
- Module state persists
- Fragile and error-prone

**Subinterpreters:**
- ✅ Clean slate every time
- ✅ All dependencies reloaded
- ✅ No stale state
- ✅ Reliable and predictable

### Process Restart

**Problems:**
- Slow (seconds to restart)
- Loses server state
- Poor development experience

**Subinterpreters:**
- ✅ Fast (<100ms overhead)
- ✅ Server keeps running
- ✅ Instant feedback

## Best Practices

1. **Keep subinterpreters enabled** - Default is best for development
2. **Watch the console** - Build errors appear there
3. **Save frequently** - Changes appear instantly
4. **Test in browser** - Visual feedback is immediate
5. **Use direct build for CI** - `build` command is faster for one-offs

## Troubleshooting

### Slow Rebuilds

**Check:**
- Number of stories (more = slower)
- Assertion complexity
- Component rendering logic

**Optimize:**
- Use `--no-with-assertions` for faster dev builds
- Profile component rendering
- Consider splitting large sites into sections

### Changes Not Appearing

**Verify:**
1. Is file in watched path?
2. Did save actually write to disk?
3. Check console for build errors
4. Is WebSocket connected? (check browser console)

**Debug:**
```bash
# See watcher events
storyville serve my_project
# Watch console for "File change detected" messages
```

### Import Issues

**Common causes:**
- Circular imports
- Module not installed
- Wrong package path

**Fix:**
- Check imports in changed files
- Ensure package is importable
- Use absolute imports

## Next Steps

- [Getting Started](getting-started.md) - Set up your first project
- [Writing Stories](writing-stories.md) - Create components and stories
- [pytest Plugin](pytest-plugin.md) - Automatic testing
