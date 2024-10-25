<h1 id="documentation"><br/><br/>📚  Documentation</h1>
<h3 id="gemini"><br/><img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/google-gemini-icon.png" width="20">  GEMINI</h3>
<p>
    The bot is highly customizable 🤖, allowing you to adjust the prompt according to your needs, resulting in more personalized responses ✍️. You can also configure various settings ⚙️, such as the model and the temperature, depending on the context or the type of output you want to generate <a href="../src/gemini/api_client.py#83">here</a>.
</p>
<p>
    By default, the following parameters are set:
</p>
<ul>
    <li><strong>Model:</strong> gemini-1.5-flash-001 🧠</li>
    <li><strong>Temperature:</strong> 1 🌡️</li>
    <li><strong>Top P:</strong> 0.95 🎯</li>
    <li><strong>Top K:</strong> 40 📊</li>
    <li><strong>Max Output Tokens:</strong> 8192 📄</li>
    <li><strong>Response Mime Type:</strong> application/json 📙</li>
</ul>
<p>
    You can modify these parameters to suit your specific needs, such as increasing the temperature for more creative responses 🎨 or lowering it for more deterministic outputs ✅. Similarly, Top P, Top K, and Top N can be adjusted to control how broad or narrow the selection of possible next tokens should be during generation.
</p>

> [!WARNING]
> Changing the response mime type might change the way gemini formats its response and its response parser. 

<h3 id="crawler"><br/>🕷️🤖  CRAWLER</h3>

> [!NOTE]  
> Currently, it is not possible to set custom parameters for the crawler 🚧.

<p>
    The crawler operates with a fixed configuration designed to efficiently retrieve and process data 📂, but future updates may include options for more granular control ⚙️, such as setting intervals ⏲️ or data extraction rules 📋.
</p>

<h3 id="usergroups"><br/>🧑‍🧑‍🧒‍🧒  USERS & GROUPS</h3>
<p>
    In terms of user interaction, the bot can be set up to interact either with individual users 👤 or with users within groups 👥. This allows for flexible engagement depending on your needs.
</p>
<p>
    For example, if you set <code>ADMIN_USER_ID=123</code> where <code>123</code> is the user's ID, the bot will be able to interact with this specific user through a private chat 💬. If you wish to allow multiple users to interact with the bot in separate private chats, you can simply add their IDs, like so: <code>ADMIN_USER_ID=123;456</code>. This way, each user will have the ability to privately communicate with the bot 👥💬.
</p>
<p>
    Only admin users can add the GemDigest bot to group chats. Once added, GemDigest will interact with everyone in the group—no admin status needed for standard interactions! However, only admins can issue direct commands to control the bot's features.
    If a non-admin attempts to:
    <ul>
    <li><b>Create a private chat with the bot</b> – GemDigest will simply ignore the message 🤷</li>
    <li><b>Add the bot to another group</b> – it will politely leave the chat 👋</li>
    </ul>
    This setup ensures GemDigest runs smoothly in groups and maintains control with admin users!
</p>

> [!NOTE]  
> To get a user’s ID, follow this guide 📝: [whoami_bot](https://github.com/Armaggheddon/whoami_bot)

<p>
    With this flexible setup, you can fine-tune how the bot communicates 📞, whether for one-on-one interactions or group-wide discussions 🗨️💡.
</p>

<h3 id="defaultcommands"><br/>📋 DEFAULT COMMANDS</h3>
<p>
    You can use the following predefined commands to get information about the bot's functionalities:
</p>
<ul>
    <li><strong>/help:</strong> Returns a list of available commands 📜</li>
    <li><strong>/tokens:</strong> Returns the number of tokens used 🔢</li>
    <li><strong>/info:</strong> Returns information such as the current temperature and the model being used 📊</li>
    <li><strong>/blacklist:</strong> Returns the list of website for which the summary is not needed (e.g. youtube) ⛔</li>
</ul>
<p>
    Examples of the following commands are provided in the table below:
</p>
<table>
<tr>
    <th>Command</th>
    <th>Description</th>
    <th>Image</th>
</tr>
<tr>
    <td><code>/help</code></td>
    <td>Displays a list of all available commands, helping you explore the bot's features more easily 🛠️</td>
    <td><img src="images/help.png"></td>
</tr>
<tr>
    <td><code>/tokens</code></td>
    <td>Shows the number of tokens used so far, helping to keep track of the token consumption efficiently 🔍</td>
    <td><img src="images/info.png"></td>
</tr>
<tr>
    <td><code>/info</code></td>
    <td>Provides details about the current bot configuration, including temperature, model, and other settings ⚙️</td>
    <td><img src="images/tokens.png"></td>
</tr>
<tr>
    <td><code>/blacklist</code></td>
    <td>Provides the list of websites that will be ignored, such as YouTube ⛔</td>
    <td><img src="images/blacklist.jpg"></td>
</tr>
</table>


<h3 id="blacklist"><br/>⛔  BLACKLIST</h3>
<p>
    To add a website to the blacklist you can edit <a href="../extra_configs/website_blacklist.txt"><code>website_blacklist.txt</code></a> and add the website you want to blacklist (For example www.youtube.com or www.x.com) are already in! Then close the file and restart the bot or the container.
</p>