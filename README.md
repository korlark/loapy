# loapy

An unofficial asynchronous SDK for Lostark Open API written in Python.

## Installation

**loapy requires Python 3.7 or higher**

```sh
python -m pip install --upgrade loapy
```

## Usage

```python
from asyncio import run
from loapy import LostArkRest

lostark = LostArkRest("your_api_key_here")

async def main() -> None:
    print(
        await lostark.fetch_events()
    )

run(main())
```