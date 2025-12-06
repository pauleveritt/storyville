# Raw Idea: Subinterpreters for Hot Reloading

**Feature: Subinterpreters for Hot Reloading**

Problem: Our server process detects changes and rebuilds, but changes to stories.py don't have an effect, since the module is already imported.

Solution: Run the build process in a subinterpreter using InterpreterPoolExecutor. The subinterpreter can do the imports and then be thrown away. The next build can start with a new subinterpreter.

Key requirements:
- Use InterpreterPoolExecutor to run builds in isolated subinterpreters
- Consider having a pool so the next interpreter is ready to go
- Warm up the pending interpreter by having it do some common imports such as `import storyville`
- When it is time to build, it can import everything in the input_dir package
- Have good integration in Starlette
- Reference: https://blog.changs.co.uk/subinterpreters-and-asyncio.html
