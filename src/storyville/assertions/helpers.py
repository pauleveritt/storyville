"""Frozen dataclass-based assertion helpers for Story.assertions.

This module provides immutable assertion helper classes that wrap aria-testing
queries for use in Story.assertions fields. Each helper is a frozen dataclass
that stores query parameters and implements a __call__ method for execution.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Self

from aria_testing import (
    ElementNotFoundError,
    MultipleElementsError,
    get_all_by_class,
    get_all_by_label_text,
    get_all_by_role,
    get_all_by_tag_name,
    get_all_by_test_id,
    get_all_by_text,
    get_by_class,
    get_by_id,
    get_by_label_text,
    get_by_role,
    get_by_tag_name,
    get_by_test_id,
    get_by_text,
    get_text_content,
)
from tdom import Element, Fragment, Node


def _format_error_message(
    error: ElementNotFoundError | MultipleElementsError,
    container: Element | Fragment | Node,
    query_description: str,
) -> str:
    """Format a detailed error message for assertion failures.

    Args:
        error: The original error from aria-testing
        container: The container that was searched
        query_description: Human-readable description of what was searched for

    Returns:
        Formatted error message with context
    """
    container_html = str(container)
    # Truncate long HTML for readability
    if len(container_html) > 300:
        container_html = container_html[:300] + "..."

    return f"""{str(error)}

Query: {query_description}

Searched in:
{container_html}
"""


@dataclass(frozen=True)
class GetByRole:
    """Assert element with specific ARIA role exists in container.

    Example:
        GetByRole(role="button")
        GetByRole(role="heading", level=1)
        GetByRole(role="button", name="Submit")
        GetByRole(role="button").not_()
        GetByRole(role="button").text_content("Submit")
    """

    role: str
    level: int | None = None
    name: str | None = None
    negate: bool = False
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment | Node) -> None:
        """Execute assertion, raising AssertionError on failure.

        Args:
            container: The Element or Fragment to search within

        Raises:
            AssertionError: If element not found or assertion conditions fail
        """
        query_desc = f"role={self.role!r}"
        if self.level is not None:
            query_desc += f", level={self.level}"
        if self.name is not None:
            query_desc += f", name={self.name!r}"

        try:
            element = get_by_role(
                container, self.role, level=self.level, name=self.name
            )

            # If .not_() was used, element should NOT exist
            if self.negate:
                raise AssertionError(
                    f"Expected element NOT to exist but found: {element}\n\nQuery: {query_desc}"
                )

            # Check text content if specified
            if self.expected_text is not None:
                actual_text = get_text_content(element)
                if actual_text != self.expected_text:
                    raise AssertionError(
                        f"Expected text: {self.expected_text!r} but got: {actual_text!r}\n\nQuery: {query_desc}"
                    )

            # Check attribute if specified
            if self.attribute_name is not None:
                actual_value = element.attrs.get(self.attribute_name)
                if actual_value is None:
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r} not found\n\nQuery: {query_desc}"
                    )
                if (
                    self.attribute_value is not None
                    and actual_value != self.attribute_value
                ):
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r}={self.attribute_value!r} but got {actual_value!r}\n\nQuery: {query_desc}"
                    )

        except (ElementNotFoundError, MultipleElementsError) as e:
            # If .not_() was used, element not found is success
            if self.negate:
                return

            error_msg = _format_error_message(e, container, query_desc)
            raise AssertionError(error_msg) from e

    def not_(self) -> Self:
        """Return instance for negative assertion (element should not exist).

        Returns:
            New instance with negate=True
        """
        return replace(self, negate=True)

    def text_content(self, expected: str) -> Self:
        """Return instance that verifies element's text content.

        Args:
            expected: The expected text content

        Returns:
            New instance with expected_text set
        """
        return replace(self, expected_text=expected)

    def with_attribute(self, name: str, value: str | None = None) -> Self:
        """Return instance that verifies element has specified attribute.

        Args:
            name: Attribute name to check
            value: Expected attribute value (None means just check existence)

        Returns:
            New instance with attribute check configured
        """
        return replace(self, attribute_name=name, attribute_value=value)


@dataclass(frozen=True)
class GetByText:
    """Assert element with specific text content exists in container.

    Example:
        GetByText(text="Submit")
        GetByText(text="Button").not_()
    """

    text: str
    negate: bool = False
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment | Node) -> None:
        """Execute assertion, raising AssertionError on failure."""
        query_desc = f"text={self.text!r}"

        try:
            element = get_by_text(container, self.text)

            if self.negate:
                raise AssertionError(
                    f"Expected element NOT to exist but found: {element}\n\nQuery: {query_desc}"
                )

            if self.expected_text is not None:
                actual_text = get_text_content(element)
                if actual_text != self.expected_text:
                    raise AssertionError(
                        f"Expected text: {self.expected_text!r} but got: {actual_text!r}\n\nQuery: {query_desc}"
                    )

            if self.attribute_name is not None:
                actual_value = element.attrs.get(self.attribute_name)
                if actual_value is None:
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r} not found\n\nQuery: {query_desc}"
                    )
                if (
                    self.attribute_value is not None
                    and actual_value != self.attribute_value
                ):
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r}={self.attribute_value!r} but got {actual_value!r}\n\nQuery: {query_desc}"
                    )

        except (ElementNotFoundError, MultipleElementsError) as e:
            if self.negate:
                return

            error_msg = _format_error_message(e, container, query_desc)
            raise AssertionError(error_msg) from e

    def not_(self) -> Self:
        """Return instance for negative assertion."""
        return replace(self, negate=True)

    def text_content(self, expected: str) -> Self:
        """Return instance that verifies element's text content."""
        return replace(self, expected_text=expected)

    def with_attribute(self, name: str, value: str | None = None) -> Self:
        """Return instance that verifies element has specified attribute."""
        return replace(self, attribute_name=name, attribute_value=value)


@dataclass(frozen=True)
class GetByLabelText:
    """Assert element with specific label text exists in container.

    Example:
        GetByLabelText(label="Username")
        GetByLabelText(label="Email")
    """

    label: str
    negate: bool = False
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment | Node) -> None:
        """Execute assertion, raising AssertionError on failure."""
        query_desc = f"label={self.label!r}"

        try:
            element = get_by_label_text(container, self.label)

            if self.negate:
                raise AssertionError(
                    f"Expected element NOT to exist but found: {element}\n\nQuery: {query_desc}"
                )

            if self.expected_text is not None:
                actual_text = get_text_content(element)
                if actual_text != self.expected_text:
                    raise AssertionError(
                        f"Expected text: {self.expected_text!r} but got: {actual_text!r}\n\nQuery: {query_desc}"
                    )

            if self.attribute_name is not None:
                actual_value = element.attrs.get(self.attribute_name)
                if actual_value is None:
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r} not found\n\nQuery: {query_desc}"
                    )
                if (
                    self.attribute_value is not None
                    and actual_value != self.attribute_value
                ):
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r}={self.attribute_value!r} but got {actual_value!r}\n\nQuery: {query_desc}"
                    )

        except (ElementNotFoundError, MultipleElementsError) as e:
            if self.negate:
                return

            error_msg = _format_error_message(e, container, query_desc)
            raise AssertionError(error_msg) from e

    def not_(self) -> Self:
        """Return instance for negative assertion."""
        return replace(self, negate=True)

    def text_content(self, expected: str) -> Self:
        """Return instance that verifies element's text content."""
        return replace(self, expected_text=expected)

    def with_attribute(self, name: str, value: str | None = None) -> Self:
        """Return instance that verifies element has specified attribute."""
        return replace(self, attribute_name=name, attribute_value=value)


@dataclass(frozen=True)
class GetByTestId:
    """Assert element with specific test ID exists in container.

    Example:
        GetByTestId(test_id="submit-button")
        GetByTestId(test_id="user-profile").with_attribute("aria-expanded", "true")
    """

    test_id: str
    negate: bool = False
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment | Node) -> None:
        """Execute assertion, raising AssertionError on failure."""
        query_desc = f"test_id={self.test_id!r}"

        try:
            element = get_by_test_id(container, self.test_id)

            if self.negate:
                raise AssertionError(
                    f"Expected element NOT to exist but found: {element}\n\nQuery: {query_desc}"
                )

            if self.expected_text is not None:
                actual_text = get_text_content(element)
                if actual_text != self.expected_text:
                    raise AssertionError(
                        f"Expected text: {self.expected_text!r} but got: {actual_text!r}\n\nQuery: {query_desc}"
                    )

            if self.attribute_name is not None:
                actual_value = element.attrs.get(self.attribute_name)
                if actual_value is None:
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r} not found\n\nQuery: {query_desc}"
                    )
                if (
                    self.attribute_value is not None
                    and actual_value != self.attribute_value
                ):
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r}={self.attribute_value!r} but got {actual_value!r}\n\nQuery: {query_desc}"
                    )

        except (ElementNotFoundError, MultipleElementsError) as e:
            if self.negate:
                return

            error_msg = _format_error_message(e, container, query_desc)
            raise AssertionError(error_msg) from e

    def not_(self) -> Self:
        """Return instance for negative assertion."""
        return replace(self, negate=True)

    def text_content(self, expected: str) -> Self:
        """Return instance that verifies element's text content."""
        return replace(self, expected_text=expected)

    def with_attribute(self, name: str, value: str | None = None) -> Self:
        """Return instance that verifies element has specified attribute."""
        return replace(self, attribute_name=name, attribute_value=value)


@dataclass(frozen=True)
class GetByClass:
    """Assert element with specific CSS class exists in container.

    Example:
        GetByClass(class_name="btn-primary")
        GetByClass(class_name="active").text_content("Selected")
    """

    class_name: str
    negate: bool = False
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment | Node) -> None:
        """Execute assertion, raising AssertionError on failure."""
        query_desc = f"class_name={self.class_name!r}"

        try:
            element = get_by_class(container, self.class_name)

            if self.negate:
                raise AssertionError(
                    f"Expected element NOT to exist but found: {element}\n\nQuery: {query_desc}"
                )

            if self.expected_text is not None:
                actual_text = get_text_content(element)
                if actual_text != self.expected_text:
                    raise AssertionError(
                        f"Expected text: {self.expected_text!r} but got: {actual_text!r}\n\nQuery: {query_desc}"
                    )

            if self.attribute_name is not None:
                actual_value = element.attrs.get(self.attribute_name)
                if actual_value is None:
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r} not found\n\nQuery: {query_desc}"
                    )
                if (
                    self.attribute_value is not None
                    and actual_value != self.attribute_value
                ):
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r}={self.attribute_value!r} but got {actual_value!r}\n\nQuery: {query_desc}"
                    )

        except (ElementNotFoundError, MultipleElementsError) as e:
            if self.negate:
                return

            error_msg = _format_error_message(e, container, query_desc)
            raise AssertionError(error_msg) from e

    def not_(self) -> Self:
        """Return instance for negative assertion."""
        return replace(self, negate=True)

    def text_content(self, expected: str) -> Self:
        """Return instance that verifies element's text content."""
        return replace(self, expected_text=expected)

    def with_attribute(self, name: str, value: str | None = None) -> Self:
        """Return instance that verifies element has specified attribute."""
        return replace(self, attribute_name=name, attribute_value=value)


@dataclass(frozen=True)
class GetById:
    """Assert element with specific ID exists in container.

    Example:
        GetById(id="main-content")
        GetById(id="user-menu").with_attribute("aria-expanded", "false")
    """

    id: str
    negate: bool = False
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment | Node) -> None:
        """Execute assertion, raising AssertionError on failure."""
        query_desc = f"id={self.id!r}"

        try:
            element = get_by_id(container, self.id)

            if self.negate:
                raise AssertionError(
                    f"Expected element NOT to exist but found: {element}\n\nQuery: {query_desc}"
                )

            if self.expected_text is not None:
                actual_text = get_text_content(element)
                if actual_text != self.expected_text:
                    raise AssertionError(
                        f"Expected text: {self.expected_text!r} but got: {actual_text!r}\n\nQuery: {query_desc}"
                    )

            if self.attribute_name is not None:
                actual_value = element.attrs.get(self.attribute_name)
                if actual_value is None:
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r} not found\n\nQuery: {query_desc}"
                    )
                if (
                    self.attribute_value is not None
                    and actual_value != self.attribute_value
                ):
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r}={self.attribute_value!r} but got {actual_value!r}\n\nQuery: {query_desc}"
                    )

        except (ElementNotFoundError, MultipleElementsError) as e:
            if self.negate:
                return

            error_msg = _format_error_message(e, container, query_desc)
            raise AssertionError(error_msg) from e

    def not_(self) -> Self:
        """Return instance for negative assertion."""
        return replace(self, negate=True)

    def text_content(self, expected: str) -> Self:
        """Return instance that verifies element's text content."""
        return replace(self, expected_text=expected)

    def with_attribute(self, name: str, value: str | None = None) -> Self:
        """Return instance that verifies element has specified attribute."""
        return replace(self, attribute_name=name, attribute_value=value)


@dataclass(frozen=True)
class GetByTagName:
    """Assert element with specific HTML tag exists in container.

    Example:
        GetByTagName(tag_name="button")
        GetByTagName(tag_name="input").with_attribute("type", "text")
    """

    tag_name: str
    negate: bool = False
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment | Node) -> None:
        """Execute assertion, raising AssertionError on failure."""
        query_desc = f"tag_name={self.tag_name!r}"

        try:
            element = get_by_tag_name(container, self.tag_name)

            if self.negate:
                raise AssertionError(
                    f"Expected element NOT to exist but found: {element}\n\nQuery: {query_desc}"
                )

            if self.expected_text is not None:
                actual_text = get_text_content(element)
                if actual_text != self.expected_text:
                    raise AssertionError(
                        f"Expected text: {self.expected_text!r} but got: {actual_text!r}\n\nQuery: {query_desc}"
                    )

            if self.attribute_name is not None:
                actual_value = element.attrs.get(self.attribute_name)
                if actual_value is None:
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r} not found\n\nQuery: {query_desc}"
                    )
                if (
                    self.attribute_value is not None
                    and actual_value != self.attribute_value
                ):
                    raise AssertionError(
                        f"Expected attribute {self.attribute_name!r}={self.attribute_value!r} but got {actual_value!r}\n\nQuery: {query_desc}"
                    )

        except (ElementNotFoundError, MultipleElementsError) as e:
            if self.negate:
                return

            error_msg = _format_error_message(e, container, query_desc)
            raise AssertionError(error_msg) from e

    def not_(self) -> Self:
        """Return instance for negative assertion."""
        return replace(self, negate=True)

    def text_content(self, expected: str) -> Self:
        """Return instance that verifies element's text content."""
        return replace(self, expected_text=expected)

    def with_attribute(self, name: str, value: str | None = None) -> Self:
        """Return instance that verifies element has specified attribute."""
        return replace(self, attribute_name=name, attribute_value=value)


# List-Oriented Query Helpers (GetAllBy*)


@dataclass(frozen=True)
class GetAllByRole:
    """Assert multiple elements with specific ARIA role exist in container.

    Example:
        GetAllByRole(role="button")
        GetAllByRole(role="button").count(3)
        GetAllByRole(role="button").nth(0).text_content("Submit")
    """

    role: str
    level: int | None = None
    name: str | None = None
    expected_count: int | None = None
    nth_index: int | None = None
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment | Node) -> None:
        """Execute assertion, raising AssertionError on failure.

        Args:
            container: The Element or Fragment to search within

        Raises:
            AssertionError: If elements not found or assertion conditions fail
        """
        query_desc = f"role={self.role!r}"
        if self.level is not None:
            query_desc += f", level={self.level}"
        if self.name is not None:
            query_desc += f", name={self.name!r}"

        try:
            elements = get_all_by_role(
                container, self.role, level=self.level, name=self.name
            )

            # Check count if specified
            if self.expected_count is not None:
                actual_count = len(elements)
                if actual_count != self.expected_count:
                    raise AssertionError(
                        f"Expected count: {self.expected_count} but found: {actual_count} elements\n\nQuery: {query_desc}"
                    )

            # Select nth element if specified
            if self.nth_index is not None:
                if self.nth_index >= len(elements) or self.nth_index < 0:
                    raise AssertionError(
                        f"Index {self.nth_index} out of bounds, found {len(elements)} elements\n\nQuery: {query_desc}"
                    )
                element = elements[self.nth_index]

                # Check text content if specified
                if self.expected_text is not None:
                    actual_text = get_text_content(element)
                    if actual_text != self.expected_text:
                        raise AssertionError(
                            f"Expected text: {self.expected_text!r} but got: {actual_text!r}\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )

                # Check attribute if specified
                if self.attribute_name is not None:
                    actual_value = element.attrs.get(self.attribute_name)
                    if actual_value is None:
                        raise AssertionError(
                            f"Expected attribute {self.attribute_name!r} not found\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )
                    if (
                        self.attribute_value is not None
                        and actual_value != self.attribute_value
                    ):
                        raise AssertionError(
                            f"Expected attribute {self.attribute_name!r}={self.attribute_value!r} but got {actual_value!r}\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )

        except (ElementNotFoundError, MultipleElementsError) as e:
            error_msg = _format_error_message(e, container, query_desc)
            raise AssertionError(error_msg) from e

    def count(self, expected: int) -> Self:
        """Return instance that verifies element count.

        Args:
            expected: Expected number of elements

        Returns:
            New instance with expected_count set
        """
        return replace(self, expected_count=expected)

    def nth(self, index: int) -> Self:
        """Return instance that selects nth element for further checks.

        Args:
            index: Zero-based index of element to select

        Returns:
            New instance with nth_index set
        """
        return replace(self, nth_index=index)

    def text_content(self, expected: str) -> Self:
        """Return instance that verifies element's text content.

        Args:
            expected: The expected text content

        Returns:
            New instance with expected_text set
        """
        return replace(self, expected_text=expected)

    def with_attribute(self, name: str, value: str | None = None) -> Self:
        """Return instance that verifies element has specified attribute.

        Args:
            name: Attribute name to check
            value: Expected attribute value (None means just check existence)

        Returns:
            New instance with attribute check configured
        """
        return replace(self, attribute_name=name, attribute_value=value)


@dataclass(frozen=True)
class GetAllByText:
    """Assert multiple elements with specific text content exist in container.

    Example:
        GetAllByText(text="Item")
        GetAllByText(text="Item").count(3)
        GetAllByText(text="Item").nth(0).with_attribute("class", "active")
    """

    text: str
    expected_count: int | None = None
    nth_index: int | None = None
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment | Node) -> None:
        """Execute assertion, raising AssertionError on failure."""
        query_desc = f"text={self.text!r}"

        try:
            elements = get_all_by_text(container, self.text)

            if self.expected_count is not None:
                actual_count = len(elements)
                if actual_count != self.expected_count:
                    raise AssertionError(
                        f"Expected count: {self.expected_count} but found: {actual_count} elements\n\nQuery: {query_desc}"
                    )

            if self.nth_index is not None:
                if self.nth_index >= len(elements) or self.nth_index < 0:
                    raise AssertionError(
                        f"Index {self.nth_index} out of bounds, found {len(elements)} elements\n\nQuery: {query_desc}"
                    )
                element = elements[self.nth_index]

                if self.expected_text is not None:
                    actual_text = get_text_content(element)
                    if actual_text != self.expected_text:
                        raise AssertionError(
                            f"Expected text: {self.expected_text!r} but got: {actual_text!r}\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )

                if self.attribute_name is not None:
                    actual_value = element.attrs.get(self.attribute_name)
                    if actual_value is None:
                        raise AssertionError(
                            f"Expected attribute {self.attribute_name!r} not found\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )
                    if (
                        self.attribute_value is not None
                        and actual_value != self.attribute_value
                    ):
                        raise AssertionError(
                            f"Expected attribute {self.attribute_name!r}={self.attribute_value!r} but got {actual_value!r}\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )

        except (ElementNotFoundError, MultipleElementsError) as e:
            error_msg = _format_error_message(e, container, query_desc)
            raise AssertionError(error_msg) from e

    def count(self, expected: int) -> Self:
        """Return instance that verifies element count."""
        return replace(self, expected_count=expected)

    def nth(self, index: int) -> Self:
        """Return instance that selects nth element for further checks."""
        return replace(self, nth_index=index)

    def text_content(self, expected: str) -> Self:
        """Return instance that verifies element's text content."""
        return replace(self, expected_text=expected)

    def with_attribute(self, name: str, value: str | None = None) -> Self:
        """Return instance that verifies element has specified attribute."""
        return replace(self, attribute_name=name, attribute_value=value)


@dataclass(frozen=True)
class GetAllByLabelText:
    """Assert multiple elements with specific label text exist in container.

    Example:
        GetAllByLabelText(label="Option")
        GetAllByLabelText(label="Option").count(2)
        GetAllByLabelText(label="Option").nth(1).with_attribute("checked", "true")
    """

    label: str
    expected_count: int | None = None
    nth_index: int | None = None
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment | Node) -> None:
        """Execute assertion, raising AssertionError on failure."""
        query_desc = f"label={self.label!r}"

        try:
            elements = get_all_by_label_text(container, self.label)

            if self.expected_count is not None:
                actual_count = len(elements)
                if actual_count != self.expected_count:
                    raise AssertionError(
                        f"Expected count: {self.expected_count} but found: {actual_count} elements\n\nQuery: {query_desc}"
                    )

            if self.nth_index is not None:
                if self.nth_index >= len(elements) or self.nth_index < 0:
                    raise AssertionError(
                        f"Index {self.nth_index} out of bounds, found {len(elements)} elements\n\nQuery: {query_desc}"
                    )
                element = elements[self.nth_index]

                if self.expected_text is not None:
                    actual_text = get_text_content(element)
                    if actual_text != self.expected_text:
                        raise AssertionError(
                            f"Expected text: {self.expected_text!r} but got: {actual_text!r}\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )

                if self.attribute_name is not None:
                    actual_value = element.attrs.get(self.attribute_name)
                    if actual_value is None:
                        raise AssertionError(
                            f"Expected attribute {self.attribute_name!r} not found\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )
                    if (
                        self.attribute_value is not None
                        and actual_value != self.attribute_value
                    ):
                        raise AssertionError(
                            f"Expected attribute {self.attribute_name!r}={self.attribute_value!r} but got {actual_value!r}\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )

        except (ElementNotFoundError, MultipleElementsError) as e:
            error_msg = _format_error_message(e, container, query_desc)
            raise AssertionError(error_msg) from e

    def count(self, expected: int) -> Self:
        """Return instance that verifies element count."""
        return replace(self, expected_count=expected)

    def nth(self, index: int) -> Self:
        """Return instance that selects nth element for further checks."""
        return replace(self, nth_index=index)

    def text_content(self, expected: str) -> Self:
        """Return instance that verifies element's text content."""
        return replace(self, expected_text=expected)

    def with_attribute(self, name: str, value: str | None = None) -> Self:
        """Return instance that verifies element has specified attribute."""
        return replace(self, attribute_name=name, attribute_value=value)


@dataclass(frozen=True)
class GetAllByTestId:
    """Assert multiple elements with specific test ID exist in container.

    Example:
        GetAllByTestId(test_id="card")
        GetAllByTestId(test_id="card").count(3)
        GetAllByTestId(test_id="card").nth(0).text_content("First Card")
    """

    test_id: str
    expected_count: int | None = None
    nth_index: int | None = None
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment | Node) -> None:
        """Execute assertion, raising AssertionError on failure."""
        query_desc = f"test_id={self.test_id!r}"

        try:
            elements = get_all_by_test_id(container, self.test_id)

            if self.expected_count is not None:
                actual_count = len(elements)
                if actual_count != self.expected_count:
                    raise AssertionError(
                        f"Expected count: {self.expected_count} but found: {actual_count} elements\n\nQuery: {query_desc}"
                    )

            if self.nth_index is not None:
                if self.nth_index >= len(elements) or self.nth_index < 0:
                    raise AssertionError(
                        f"Index {self.nth_index} out of bounds, found {len(elements)} elements\n\nQuery: {query_desc}"
                    )
                element = elements[self.nth_index]

                if self.expected_text is not None:
                    actual_text = get_text_content(element)
                    if actual_text != self.expected_text:
                        raise AssertionError(
                            f"Expected text: {self.expected_text!r} but got: {actual_text!r}\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )

                if self.attribute_name is not None:
                    actual_value = element.attrs.get(self.attribute_name)
                    if actual_value is None:
                        raise AssertionError(
                            f"Expected attribute {self.attribute_name!r} not found\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )
                    if (
                        self.attribute_value is not None
                        and actual_value != self.attribute_value
                    ):
                        raise AssertionError(
                            f"Expected attribute {self.attribute_name!r}={self.attribute_value!r} but got {actual_value!r}\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )

        except (ElementNotFoundError, MultipleElementsError) as e:
            error_msg = _format_error_message(e, container, query_desc)
            raise AssertionError(error_msg) from e

    def count(self, expected: int) -> Self:
        """Return instance that verifies element count."""
        return replace(self, expected_count=expected)

    def nth(self, index: int) -> Self:
        """Return instance that selects nth element for further checks."""
        return replace(self, nth_index=index)

    def text_content(self, expected: str) -> Self:
        """Return instance that verifies element's text content."""
        return replace(self, expected_text=expected)

    def with_attribute(self, name: str, value: str | None = None) -> Self:
        """Return instance that verifies element has specified attribute."""
        return replace(self, attribute_name=name, attribute_value=value)


@dataclass(frozen=True)
class GetAllByClass:
    """Assert multiple elements with specific CSS class exist in container.

    Example:
        GetAllByClass(class_name="item")
        GetAllByClass(class_name="item").count(5)
        GetAllByClass(class_name="item").nth(2).text_content("Third Item")
    """

    class_name: str
    expected_count: int | None = None
    nth_index: int | None = None
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment | Node) -> None:
        """Execute assertion, raising AssertionError on failure."""
        query_desc = f"class_name={self.class_name!r}"

        try:
            elements = get_all_by_class(container, self.class_name)

            if self.expected_count is not None:
                actual_count = len(elements)
                if actual_count != self.expected_count:
                    raise AssertionError(
                        f"Expected count: {self.expected_count} but found: {actual_count} elements\n\nQuery: {query_desc}"
                    )

            if self.nth_index is not None:
                if self.nth_index >= len(elements) or self.nth_index < 0:
                    raise AssertionError(
                        f"Index {self.nth_index} out of bounds, found {len(elements)} elements\n\nQuery: {query_desc}"
                    )
                element = elements[self.nth_index]

                if self.expected_text is not None:
                    actual_text = get_text_content(element)
                    if actual_text != self.expected_text:
                        raise AssertionError(
                            f"Expected text: {self.expected_text!r} but got: {actual_text!r}\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )

                if self.attribute_name is not None:
                    actual_value = element.attrs.get(self.attribute_name)
                    if actual_value is None:
                        raise AssertionError(
                            f"Expected attribute {self.attribute_name!r} not found\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )
                    if (
                        self.attribute_value is not None
                        and actual_value != self.attribute_value
                    ):
                        raise AssertionError(
                            f"Expected attribute {self.attribute_name!r}={self.attribute_value!r} but got {actual_value!r}\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )

        except (ElementNotFoundError, MultipleElementsError) as e:
            error_msg = _format_error_message(e, container, query_desc)
            raise AssertionError(error_msg) from e

    def count(self, expected: int) -> Self:
        """Return instance that verifies element count."""
        return replace(self, expected_count=expected)

    def nth(self, index: int) -> Self:
        """Return instance that selects nth element for further checks."""
        return replace(self, nth_index=index)

    def text_content(self, expected: str) -> Self:
        """Return instance that verifies element's text content."""
        return replace(self, expected_text=expected)

    def with_attribute(self, name: str, value: str | None = None) -> Self:
        """Return instance that verifies element has specified attribute."""
        return replace(self, attribute_name=name, attribute_value=value)


@dataclass(frozen=True)
class GetAllByTagName:
    """Assert multiple elements with specific HTML tag exist in container.

    Example:
        GetAllByTagName(tag_name="li")
        GetAllByTagName(tag_name="li").count(4)
        GetAllByTagName(tag_name="button").nth(0).with_attribute("type", "submit")
    """

    tag_name: str
    expected_count: int | None = None
    nth_index: int | None = None
    expected_text: str | None = None
    attribute_name: str | None = None
    attribute_value: str | None = None

    def __call__(self, container: Element | Fragment | Node) -> None:
        """Execute assertion, raising AssertionError on failure."""
        query_desc = f"tag_name={self.tag_name!r}"

        try:
            elements = get_all_by_tag_name(container, self.tag_name)

            if self.expected_count is not None:
                actual_count = len(elements)
                if actual_count != self.expected_count:
                    raise AssertionError(
                        f"Expected count: {self.expected_count} but found: {actual_count} elements\n\nQuery: {query_desc}"
                    )

            if self.nth_index is not None:
                if self.nth_index >= len(elements) or self.nth_index < 0:
                    raise AssertionError(
                        f"Index {self.nth_index} out of bounds, found {len(elements)} elements\n\nQuery: {query_desc}"
                    )
                element = elements[self.nth_index]

                if self.expected_text is not None:
                    actual_text = get_text_content(element)
                    if actual_text != self.expected_text:
                        raise AssertionError(
                            f"Expected text: {self.expected_text!r} but got: {actual_text!r}\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )

                if self.attribute_name is not None:
                    actual_value = element.attrs.get(self.attribute_name)
                    if actual_value is None:
                        raise AssertionError(
                            f"Expected attribute {self.attribute_name!r} not found\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )
                    if (
                        self.attribute_value is not None
                        and actual_value != self.attribute_value
                    ):
                        raise AssertionError(
                            f"Expected attribute {self.attribute_name!r}={self.attribute_value!r} but got {actual_value!r}\n\nQuery: {query_desc}, nth={self.nth_index}"
                        )

        except (ElementNotFoundError, MultipleElementsError) as e:
            error_msg = _format_error_message(e, container, query_desc)
            raise AssertionError(error_msg) from e

    def count(self, expected: int) -> Self:
        """Return instance that verifies element count."""
        return replace(self, expected_count=expected)

    def nth(self, index: int) -> Self:
        """Return instance that selects nth element for further checks."""
        return replace(self, nth_index=index)

    def text_content(self, expected: str) -> Self:
        """Return instance that verifies element's text content."""
        return replace(self, expected_text=expected)

    def with_attribute(self, name: str, value: str | None = None) -> Self:
        """Return instance that verifies element has specified attribute."""
        return replace(self, attribute_name=name, attribute_value=value)
