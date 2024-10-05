import io
from typing import Mapping, Any, List
from .types import GeminiOutputFormat


def parse_gemini_json(
    response_text: str, 
    format: Mapping[str, Any]
) -> GeminiOutputFormat:

    expected_keys = list(format.__annotations__.keys())

    # start from the first quote
    start = response_text.find("\"")
    curr_pos = start
    delimiter_count = 0
    tokens: List[str] = []

    # split based on the quotes while keeping the quotes
    while curr_pos < len(response_text):
        if response_text[curr_pos] == "\"":
            delimiter_count += 1

        if delimiter_count == 2:
            tokens.append(response_text[start:curr_pos + 1])
            start = curr_pos + 1
            delimiter_count = 0

        curr_pos += 1

    # remove the quotes from the tokens only if are not escaped
    for i, token in enumerate(tokens):
        s_quote = token.find("\"")
        e_quote = token.rfind("\"")

        if s_quote == e_quote: # considers also the case where both are -1
            # no quotes, or is only one quote (the same)
            continue

        s_quote_escaped = s_quote > 0 and token[s_quote - 1] == "\\"
        e_quote_escaped = e_quote > 0 and token[e_quote - 1] == "\\"

        if s_quote_escaped or e_quote_escaped:
            # at least one quote is escaped
            if token[s_quote - 1] == "\\":
                # s_quote is escaped, so we remove the escape
                s_quote = 0
            else:
                # s_quote is not escaped, so we add 1 to it
                # to remove the first quote
                s_quote = s_quote + 1
            
            if token[e_quote - 1] == "\\":
                # e_quote is escaped, so we remove the escape
                e_quote = len(token)
            
            tokens[i] = token[s_quote:e_quote].strip()
        else:
            # no escaped quotes
            # add 1 to s_quote to remove the first quote
            tokens[i] = token[s_quote+1: e_quote].strip()
    
    tmp_buff = io.StringIO()
    values = []
    
    # accumulate the values for each of the keys
    # the first token is the key, skip it so we can start
    # accumulating from the first key value, to avoid
    # haky code to remove the first item from values
    for token in tokens[1:]:
        if token in expected_keys:
            # everything that has been found
            # until now is the value of the previous key
            values.append(tmp_buff.getvalue())
            tmp_buff = io.StringIO()
        else:
            # we are still in the value of the current key
            tmp_buff.write(token)
    
    # add the last value
    values.append(tmp_buff.getvalue())

    # TODO: return the values as a GeminiOutputFormat
    return GeminiOutputFormat(*values)
