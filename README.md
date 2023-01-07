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

---

# Plan

1. - [ ] build the blackjack session

> ~~make that the bot can create session and player can join and also i guess... make it that when there are no player, close down the session~~ to join a blackjack session, do /bet \[amount\], but still working on it!

2.  - [ ] make player can place bet

    give player time to place bet... dont start dealing the card for a certain time?
    
    maybe start a timer on the first bet placed by a player
    
    betting is over when all player place their bet

2. - [ ]make bot able to deal card to player

3.  - [ ] make player able to do their options

    - hit
    - stand
    - split if they has same value card

4. - [ ] dealer check card and if under 17, draw until win or bust

5. - [ ] hand out win or take losses from player `balance`