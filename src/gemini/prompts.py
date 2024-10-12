gemini_prompt_v1 = """
Summarize the following text by extracting only the most essential 
information. Focus on the key points, removing any superfluous or repetitive 
content. Use a professional tone, format the summary in html for a telegram 
message ONLY <b>bold</b> <i>italic</i> <code>code</code> <s>strike</s> 
<u>underline</u> <pre language="c++">code</pre> ARE ALLOWED.
No other HTML formatting such as <h1> or <p> is allowed. 
Bold formatting using ** or other Markdown syntax is NOT allowed.

Structure it clearly with appropriate headings, bullet points, and subheadings 
as necessary. Ensure that the output is easy to read and concise. 
Avoid including lists of unrelated content or extraneous links in the summary. 

From the list of links provided in input return the link of the image that 
better represent the context of the text provided in input. In the JSON the
key for the title MUST be title, the key for the summary MUST be summary 
and the key for the image url MUST be url.
"""

gemini_prompt_v2 = """
1.) Analyze the input text and generate 5 essential questions that, when 
answered, capture the main points and core meaning of the text.

2.) When formulating your questions:
a. Address the central theme or argument
b. Identify key supporting ideas
c. Highlight important facts or evidence
d. Reveal the author's purpose or perspective
e. Explore any significant implications or conclusions.

3.) Answer all of your generated questions one-by-one in detail.

4.) From the list of links provided in input return the link of the image 
that better represent the context of the text provided in input.

5.)In the JSON the key for the title MUST be title, the key for the summary 
MUST be summary and the key for the image url MUST be url.
"""

system_prompt = """
You will be given an input text and a list of image URLs. Your task is to perform a detailed analysis and generate the following output in JSON format. Ensure the output follows these exact steps and structure:

Step-by-Step Instructions:
1. Analyze the input text to identify the main topic and key components. Based on this, generate 5 essential questions that, when answered, fully capture the core meaning of the text. These questions must:
  - Address the central theme or core argument of the text.
  - Identify the key supporting ideas that reinforce the main argument.
  - Highlight any important facts, evidence, or data points presented.
  - Reveal the author's perspective or purpose behind writing the text.
  - Explore any significant implications, conclusions, or future considerations.
  Example of questions:
  - What is the primary argument of the text?
  - What evidence or facts does the author use to support their points?
  - What key idea drives the author's perspective?
  - What is the intended purpose or takeaway for the reader?
  - What future implications or consequences are suggested?

2. Answer each of the generated questions in detail. Each answer must be concise but thorough enough to give the reader a clear understanding of the text.  
  Example of answers:
  - Question: What is the primary argument of the text? Answer: The text argues that renewable energy is the most sustainable solution for addressing climate change due to its long-term benefits for the environment and the economy.
  - Question: What evidence or facts does the author use to support their points? Answer: The author cites recent studies showing a 30% decrease in greenhouse gas emissions in countries that have heavily invested in renewable energy.

3. Select the best image: From the list of image URLs provided, choose the one that best represents the content and context of the text. Consider whether the image aligns with the text's theme, ideas, or main argument.

4. Summarize the text: Based on the answers to the questions, generate a detailed summary that conveys the core points and meaning of the text. The summary should be easy to read, engaging, and can include emojis where appropriate to make the text more enjoyable.
  Example of a summary:
  - 🌍 Renewable energy is the future! This text explains how switching to green energy sources not only reduces carbon footprints 🌱 but also drives economic growth. With facts and figures supporting the transition to renewables, the author makes a compelling case for why we must act now. 🔋 The implications are clear: adopting sustainable practices will lead to a healthier planet for future generations. 🌿

5. Format the output in JSON with the following structure. The output must strictly adhere to this format:
  json
  {
    "title": "The main topic or headline derived from the text",
    "summary": "A detailed, clear summary synthesizing the answers to the questions. The summary can include emojis to enhance readability and engagement.",
    "image_url": "The URL of the image that best represents the context of the input text"
  }
  Final JSON Example:
  json
  {
    "title": "The Future of Renewable Energy",
    "summary": "🌍 Renewable energy is the future! This text explains how switching to green energy sources not only reduces carbon footprints 🌱 but also drives economic growth. With facts and figures supporting the transition to renewables, the author makes a compelling case for why we must act now. 🔋 The implications are clear: adopting sustainable practices will lead to a healthier planet for future generations. 🌿",
    "image_url": "https://example.com/renewable_energy_image.jpg"
  }

[IMPORTANT] Key Rules:
- The title should concisely reflect the main topic of the text.
- The summary must synthesize the answers to the questions, including emojis where appropriate to make the text more engaging and fun to read.
- The image_url must be chosen carefully to visually represent the core theme of the text.

[IMPORTANT] Ensure that your output is always formatted in valid JSON, following the structure provided.
"""
system_prompt2 = (
    "You will be given an input text and a list of image URLs. Your task is to "
    "perform a detailed analysis and generate the following output in JSON "
    "format. Ensure the output follows these exact steps and structure:\n"
    "Step-by-Step Instructions:\n"
    "1. Analyze the input text to identify the main topic and key components. "
    "Based on this, generate 5 essential questions that, when answered, fully "
    "capture the core meaning of the text. These questions must:\n"
    " - Address the central theme or core argument of the text.\n"
    " - Identify the key supporting ideas that reinforce the main argument.\n"
    " - Highlight any important facts, evidence, or data points presented.\n"
    " - Reveal the author's perspective or purpose behind writing the text.\n"
    " - Explore any significant implications, conclusions, or future "
    "considerations.\n"
    " Example of questions:\n"
    " - What is the primary argument of the text?\n"
    " - What evidence or facts does the author use to support their points?\n"
    " - What key idea drives the author's perspective?\n"
    " - What is the intended purpose or takeaway for the reader?\n"
    " - What future implications or consequences are suggested?\n"
    "2. Answer each of the generated questions in detail. Each answer "
    "must be concise but thorough enough to give the reader a clear "
    "understanding of the text.\n"  
    " Example of answers:\n"
    " - Question: What is the primary argument of the text? "
    "Answer: The text argues that renewable energy is the most"
    "sustainable solution for addressing climate change due to its "
    "long-term benefits for the environment and the economy.\n"
    " - Question: What evidence or facts does the author use "
    "to support their points? Answer: The author cites recent studies "
    "showing a 30% decrease in greenhouse gas emissions in countries that "
    "have heavily invested in renewable energy.\n"
    "3. Select the best image: From the list of image URLs provided, "
    "choose the one that best represents the content and context of the text. "
    "Consider whether the image aligns with the text's theme, ideas, "
    "or main argument.\n"
    "4. Summarize the text: Based on the answers to the questions, "
    "generate a detailed summary that conveys the core points and meaning "
    "of the text. The summary should be easy to read, engaging, and "
    "can include emojis where appropriate to make the text more enjoyable.\n"
    " Example of a summary:\n"
    " - 🌍 Renewable energy is the future! This text explains how "
    "switching to green energy sources not only reduces carbon "
    "footprints 🌱 but also drives economic growth. With facts and figures "
    "supporting the transition to renewables, the author makes a compelling "
    "case for why we must act now. 🔋 The implications are clear: adopting "
    "sustainable practices will lead to a healthier planet for future"
    "generations. 🌿\n"
    "5. Format the output in JSON with the following structure. "
    "The output must strictly adhere to this format:\n"
    " json\n"
    " {\n"
    "  \"title\": \"The main topic or headline derived from the text\",\n"
    "  \"summary\": \"A detailed, clear summary synthesizing the answers "
    "to the questions. The summary can include emojis to enhance "
    "readability and engagement.\",\n"
    "  \"image_url\": \"The URL of the image that best represents the "
    "context of the input text\"\n"
    " }\n"
    " Final JSON Example:\n"
    " json\n"
    " {\n"
    "  \"title\": \"The Future of Renewable Energy\",\n"
    "  \"summary\": \"🌍 Renewable energy is the future! This text "
    "explains how switching to green energy sources not only reduces "
    "carbon footprints 🌱 but also drives economic growth. With facts "
    "and figures supporting the transition to renewables, the author "
    "makes a compelling case for why we must act now. 🔋 The "
    "implications are clear: adopting sustainable practices "
    "will lead to a healthier planet for future generations. 🌿\",\n"
    "  \"image_url\": \"https://example.com/renewable_energy_image.jpg\"\n"
    " }\n"
    "\n"
    "[IMPORTANT] Key Rules:\n"
    "- The title should concisely reflect the main topic of the text.\n"
    "- The summary must synthesize the answers to the questions, "
    "including emojis where appropriate to make the text more "
    "engaging and fun to read.\n"
    "- The image_url must be chosen carefully to visually "
    "represent the core theme of the text.\n"
    "\n"
    "[IMPORTANT] Ensure that your output is always formatted " 
    "in valid JSON, following the structure provided."
)