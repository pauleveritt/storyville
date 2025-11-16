# Inheritance Example

## Overview

Demonstrates field inheritance patterns across the hierarchy. Shows how Stories inherit target from Subject and how titles are auto-generated when not specified.

## Structure

- Site: Inheritance Example
- Section: Card Components
- Subject: Card component (target defined, no explicit title)
- Stories: Four stories demonstrating different inheritance patterns

## Key Features

- **Target inheritance**: Stories inherit the target (Card) from their Subject when story.target is None
- **Title generation**: Stories without explicit titles get auto-generated titles from Subject
- **Target override**: One Story overrides the Subject's target with Badge component
- **Inheritance rules**: Explicit Story title or target values override inheritance
