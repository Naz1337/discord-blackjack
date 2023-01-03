# Blackjack on Discord
**PROGRESS**: *WIP*

---

dependencies:
1. discord.py
2. python-dotenv
3. aiosqlite

# Run Instruction
To run this bot, you'll need to grab your bot token and store it in an environment variable called `dsc_key`. To do this, create a file named `.env` and add the following line to it:

```bash
dsc_key=YOUR_BOT_TOKEN_HERE
```

Then, the script will be able to access the bot token by looking for the `dsc_key` key in the `os.environ` object.