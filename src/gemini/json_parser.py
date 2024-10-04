from .types import GeminiOutputFormat

output = """{"title": "LeafSense: AI-Powered Disease Detection for Vineyards", "summary": "🍇 LeafSense is a revolutionary app that uses AI to help vineyard owners identify diseases early on. Simply take a picture of a leaf with your smartphone, and LeafSense's algorithms will analyze it for signs of disease. The app provides a 'probability index' to let you know how likely a problem is. 💪 If you need more information, you can access a built-in encyclopedia of vineyard diseases or even export the image to your technician for further analysis. 🔍 The app also allows you to save results and locations to keep track of potential issues in your vineyard. 🗺️ LeafSense empowers farmers by offering real-time disease monitoring and helping them make informed decisions to protect their crops. 🌱", "image_url": "\\\"images/iphone-app-470.png\\\""}"""

def parse_gemini_json(output: str) -> GeminiOutputFormat:
    after_title = output.split("title", 1)[-1]
    
    tmp_vlue_list = []
    tmp_vlue = ""
    value_delimiter_count = 0
    curr_pos = 0
    for ch in after_title:
        if value_delimiter_count == 2 or value_delimiter_count == 3:
            if ch == "\"":
                value_delimiter_count = 0
                tmp_vlue_list.append(tmp_vlue)
                if len(tmp_vlue_list) == 4:
                    break
                tmp_vlue = ""
            tmp_vlue += ch 
        if ch == "\"":
            value_delimiter_count += 1
        curr_pos += 1
    
    missing = output[curr_pos:]
    after_missing = missing.split("\"", 1)[-1]
    after_missing = after_missing.rsplit("\"", 1)[0]
    tmp_vlue_list.append(after_missing)

    tmp_vlue_list.pop(1)
    tmp_vlue_list.pop(2)

    if len(tmp_vlue_list) != 3:
        raise ValueError(f"Missing json Key: got {tmp_vlue_list}")
    return GeminiOutputFormat(*tmp_vlue_list)
