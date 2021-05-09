# Vaccine Availability on Telegram Channel
Get vaccine availability in any district in India

Steps
- Fork the code
- Install all the dependencies mentioned in requirements.txt
- Change the district details [here]()
- Change age group [here]()  
- Create a new [Telegram Bot](https://core.telegram.org/bots) and Channel
- Add the bot to the channel, as a member and give admin rights
- Update bot token [here](). This is given by botfather at the time of bot creation
- Find channel id by hitting this API - https://api.telegram.org/bot<bot_token>/getUpdates. 
  Find your channel name in the response and get the value of id in chat array (typically -ve value for channel)
- Update scheduling frequency [here](). Refer schedule man page [here](https://pypi.org/project/schedule/)
- Run availability.py