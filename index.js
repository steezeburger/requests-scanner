const Discord = require('discord.js')
const handleMovieRequest = require('./src/handleMovieRequest')

// env
require('dotenv').config()
const { BOT_TOKEN } = process.env

const bot = new Discord.Client()
bot.login(BOT_TOKEN)

bot.on('messageUpdate', async (old, current) => {
  await handleMovieRequest(old, current)
})
