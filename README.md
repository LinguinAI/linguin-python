# Linguin AI Python wrapper

This is a Python wrapper for the [Linguin AI](https://linguin.ai) API (see [API docs](https://linguin.ai/api-docs/v1)) providing Language Detection as a Service.

Linguin AI is free for up to 100 detections per day. You can get your API key [here](https://linguin.ai).

## Installation

Coming soon!

## Usage

Get started with just a few lines of code:

```
from linguin import Linguin

# go to https://linguin.ai to get your key
linguin = Linguin("YOUR_API_TOKEN")

response = linguin.detect("test")

response.is_success
# >> True

response.result
# >> {'results': [{ 'lang': 'en', confidence: 1.0 }, ...]}
```

If anything goes wrong for example: empty query string:

```
response = linguin.detect(" ")
    
response.is_success
# >> False
   
print(response.error)
# >> Error code: 400. The language of an empty text is more of a philosophical question.

response.error.status
# >> 400

response.error.message
# >> The language of an empty text is more of a philosophical question.
```

If you prefer to handle exceptions instead:

```
response = linguin.detect(" ", raise_on_error=True)
# >> raises LinguinInputError
```

See the list of all exceptions here.

### Bulk detection

To detect the language of multiple texts with one API call, you can pass them as an array to the `bulk` method.
The results will be returned in the same order as the texts. All texts have to not be empty.

```
response = linguin.bulk(["test", "Bahnhof", "고마워요"])

response.is_success
# >> True

response.result
# >> [{'results': [{'lang': 'en', 'confidence': 1.0}, ...]}, {...}, ...]
```

### Account status

You can fetch the status of your account:

```
response = linguin.status()

response.result
# >> {'daily_limit': 50000, 'detections_today': 4500, 'remaining_today': 45500}
# for unlimited usage we return -1
```
