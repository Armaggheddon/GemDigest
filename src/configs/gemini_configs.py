
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

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