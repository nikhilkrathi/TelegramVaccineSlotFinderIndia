# Vaccine Availability on Telegram Channel
Get vaccine availability in any district in India

Steps
- Fork the code
- Install all the dependencies mentioned in requirements.txt
- Change the district details [here](https://github.com/nikhilkrathi/TelegramVaccineSlotFinderIndia/blob/6d78a39d04390d0316e3e53a39f2dada7f7dd960/availability.py#L91)
- Change age group [here](https://github.com/nikhilkrathi/TelegramVaccineSlotFinderIndia/blob/6d78a39d04390d0316e3e53a39f2dada7f7dd960/availability.py#L95)  
- Create a new [Telegram Bot](https://core.telegram.org/bots) and Channel
- Add the bot to the channel, as a member and give admin rights
- Update bot token [here](https://github.com/nikhilkrathi/TelegramVaccineSlotFinderIndia/blob/6d78a39d04390d0316e3e53a39f2dada7f7dd960/availability.py#L73). This is given by botfather at the time of bot creation
- Find channel id by hitting this API - https://api.telegram.org/bot<bot_token>/getUpdates. 
  Find your channel name in the response and get the value of id in chat array (typically -ve value for channel)
- Update channel id [here](https://github.com/nikhilkrathi/TelegramVaccineSlotFinderIndia/blob/6d78a39d04390d0316e3e53a39f2dada7f7dd960/availability.py#L74)  
- Update scheduling frequency [here](https://github.com/nikhilkrathi/TelegramVaccineSlotFinderIndia/blob/6d78a39d04390d0316e3e53a39f2dada7f7dd960/availability.py#L102). Refer schedule man page [here](https://pypi.org/project/schedule/)
- Run availability.py