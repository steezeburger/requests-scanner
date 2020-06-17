require('dotenv').config()
const Discord = require('discord.js')
const _ = require('lodash')

const TOKEN = process.env.BOT_TOKEN
const bot = new Discord.Client()

bot.login(TOKEN)

bot.on('messageUpdate', (old, current) => {
  const path = 'embeds[0].url'
  const oldUrl = _.get(old, path)
  const currentUrl = _.get(current, path)

  if (!oldUrl && currentUrl && currentUrl.includes('themoviedb.org/movie')) {
    console.log(currentUrl);
    // TODO - post to github
    const title = _.get(current, 'embeds[0].title')
    current.reply(`say, you wanted to download ${title}. is that correct?`)
  }
})
