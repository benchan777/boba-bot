# Boba Bot
A discord bot that displays information about boba stores near the user input location. Also provides the ability for multiple users to specify food/drinks they want from specific stores to make group orders easier.

## Invite Bot
[Click here to invite bot to your server](https://discord.com/api/oauth2/authorize?client_id=821142110072864789&permissions=2148001856&scope=bot)


## Running the bot locally
1. Go to the Developer portal [here](https://discord.com/developers/applications) to create a new bot and retrieve its token.

2. Clone the repo:
`git clone https://github.com/benchan777/boba-bot.git`

3. Place the token in your .env file with the format `discord_bot_token=<bot token here>`

4. `pip3 install -r requirements.txt`

5. `python3 app.py`

## Commands
| Command 	| Description 	| Example 	|
|-	|-	|-	|
| `$boba <location>` 	| Displays boba stores near the specified location 	| $boba San Francisco 	|
| `$location <location>` 	| Saves the specified location so it doesn't have to be entered again 	| $location San Francisco 	|
| `$order <store #> <order info>` 	| Saves order information to specified store # 	| $order 4 Jasmine Milk Tea 	|
| `$store <store name>` 	| Displays order information of all users who saved information to specified store 	| $store Boba Guys 	|

## Screenshots
| $boba | $location | $order | $store |
|- |- |- |- |
| ![](https://i.imgur.com/vzD8N36.png) | ![](https://i.imgur.com/85eTdge.png) | ![](https://i.imgur.com/Zcf4TbA.png) | ![](https://i.imgur.com/6rjYQCY.png) |