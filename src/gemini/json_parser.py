"""
#
"""
# from .types import GeminiOutputFormat

TEST = """{"title": "LeafSense: AI-Powered Disease Detection for Vineyards", "summary": "🍇 LeafSense is a revolutionary app that uses AI to help vineyard owners identify diseases early on. Simply take a picture of a leaf with your smartphone, and LeafSense's algorithms will analyze it for signs of disease. The app provides a 'probability index' to let you know how likely a problem is. 💪 If you need more information, you can access a built-in encyclopedia of vineyard diseases or even export the image to your technician for further analysis. 🔍 The app also allows you to save results and locations to keep track of potential issues in your vineyard. 🗺️ LeafSense empowers farmers by offering real-time disease monitoring and helping them make informed decisions to protect their crops. 🌱", "image_url": "\\\"images/iphone-app-470.png\\\""}"""

def parse_gemini_json(response_text: str) -> str: #GeminiOutputFormat:
    """
    #
    """
    if response_text is None:
        raise ValueError("The input string is missing."
                         "Can't convert it into GeminiOutputFormat")

    output = response_text.split("\": \"")
    for token in output:
        print(token)



#     output = [token
#               for token in output
#               if token not in ["",": ",", ", "", ":", "{", "}"]
#     ]

#     try:
#         title_index = output.index("title")
#         summary_index = output.index("summary")
#         image_url_index = output.index("image_url")
#     except ValueError as exc:
#         raise ValueError(f"One of the keys is missing. "
#                         f"Can't convert it into GeminiOutputFormat: {exc}"
#         ) from exc

#     title_to_summary = output[title_index + 1:summary_index]
#     summary_to_image_url = output[summary_index + 1:image_url_index]
#     image_url = output[image_url_index + 1:]

#     output = [
#         ' '.join(title_to_summary),
#         ' '.join(summary_to_image_url),
#         ' '.join(image_url)
#     ]

#     output = [token.strip() for token in output]

#     #return GeminiOutputFormat(*output)
#     return output

# parse_gemini_json(TEST)