"""
## `NotGiven`

- **Purpose**: Indicates that a parameter was not provided at all. It's used to
  distinguish between a parameter being explicitly set to `None` and not being
  provided.
- **Use Case**: Common in APIs where default behavior is triggered when a
  parameter is not given, but `None` might be a valid, meaningful input. For
  example, `None` might mean "disable timeout", while `NotGiven` means "use a
  default timeout".
- Other example usage is if you want to assign a default empty list or dict but
  it is mutable, so you assign this type but not None since None don't make
  sense.
- **Behavior**: Functions can check for `NotGiven` to apply default behavior.

## `Omit`

- **Purpose**: Used to explicitly remove or omit a default value that would
  otherwise be applied. It's not just about a value being absent, but rather
  about actively removing a pre-existing default.
- **Use Case**: Useful in situations where the default behavior or value needs
  to be explicitly overridden or disabled, and where `None` is not a suitable
  option. For example, removing a default HTTP header.
- **Behavior**: Functions can check for `Omit` to actively remove or ignore a
  default setting or value.

### Comparison

- **Similarity**: Both are used to signal special cases in the absence of normal
  parameter values.
- **Difference**: `NotGiven` is about the absence of a value where a default may
  apply, while `Omit` is about actively overriding a default.
"""

from __future__ import annotations

from typing import Any, Literal, Type

from typing_extensions import override


class _NotGiven:
    """
    A sentinel singleton class used to distinguish omitted keyword arguments
    from those passed in with the value None (which may have different behavior).

    Quite similar with dataclass's MISSING.

    This is used to differentiate between cases where a parameter is not
    provided and where a parameter is provided with the value None. The class
    provides a more descriptive representation than None or other placeholders.

    NOTE: example usage is if you want to assign a default empty list or dict
    but it is mutable, so you assign this type but not None since None don't make
    sense.

    It is a singleton because `None` is also a singleton so we mimic this
    behaviour. No matter how many times you call `None` in any function or
    methods, it will reference the same unique singleton `None` class.

    More importantly, because `None` is a singleton, we can use the `is`
    operator to check for object identity. This is why the idiomatic way
    to check if a variable is `None` is to do `if var is None`.

    So that is why we make `_NotGiven` a singleton, because referencing this
    class across scripts will maintain its unique identity across imports.

    We further make this class immutable to behave a bit like `None`.

    Example
    -------
    ```python
    def get(timeout: Union[int, _NotGiven, None] = _NotGiven()) -> Response:
        if timeout is _NotGiven:
            # Default timeout behavior
        elif timeout is None:
            # No timeout
        else:
            # Specific timeout given

    get(timeout=1) # 1s timeout
    get(timeout=None) # No timeout
    get() # Default timeout behavior, which may not be statically known at
          # the method definition.
    ```
    """

    _instance: _NotGiven | None = None

    def __new__(cls: Type[_NotGiven]) -> _NotGiven:  # noqa: PYI034
        if cls._instance is None:
            cls._instance = super(_NotGiven, cls).__new__(cls)  # noqa: UP008
        return cls._instance

    def __bool__(self) -> Literal[False]:
        """
        This method is used to define the boolean value of an instance of `_NotGiven`.
        By returning `False`, it allows `_NotGiven` to be used in boolean contexts (like
        `if` statements) to signify the absence of a value. This is especially useful
        for checking if an argument was provided or not in a function.
        """
        return False

    @override
    def __repr__(self) -> Literal["_NOT_GIVEN"]:
        return "_NOT_GIVEN"

    def __setattr__(self, key: str, value: Any) -> None:
        raise AttributeError("_NotGiven instances are immutable")

    def __delattr__(self, key: str) -> None:
        raise AttributeError("_NotGiven instances are immutable")


NOT_GIVEN = _NotGiven()


class _Omit:
    """
    In certain situations you need to be able to represent a case where a default
    value has to be explicitly removed and `None` is not an appropriate substitute,
    for example:

    ```python
    # as the default `Content-Type` header is `application/json` that will be sent
    client.post('/upload/files', files={'file': b'my raw file content'})

    # you can't explicitly override the header as it has to be dynamically generated
    # to look something like:
    # 'multipart/form-data; boundary=0d8382fcf5f8c3be01ca2e11002d2983'
    client.post(..., headers={'Content-Type': 'multipart/form-data'})

    # instead you can remove the default `application/json` header by passing Omit
    client.post(..., headers={'Content-Type': Omit()})
    ```
    """

    def __bool__(self) -> Literal[False]:
        return False
