const dotenv = require('dotenv')
const _ = require('lodash')
const Discord = require('discord.js')
const GistClient = require('gist-client')

// env
dotenv.config()
const {
  BOT_TOKEN,
  GIST_FILENAME,
  GIST_TOKEN,
  GIST_ID,
} = process.env

// init clients
const bot = new Discord.Client()
const gistClient = new GistClient()

// login clients
bot.login(BOT_TOKEN)
gistClient.setToken(GIST_TOKEN)

// msg handler
bot.on('messageUpdate', async (old, current) => {
  const path = 'embeds[0].url'
  const oldUrl = _.get(old, path)
  const currentUrl = _.get(current, path)

  if (!oldUrl && currentUrl && currentUrl.includes('themoviedb.org/movie')) {
    const title = _.get(current, 'embeds[0].title')
    current.reply(`I'm Leo Getz, and whatever you want, Leo gets. Leo will be getting ${title}, you stupid fuck.`)

    const gist = await gistClient.getOneById(GIST_ID)

    const datum = {
      title: title,
      url: currentUrl,
    }

    const oldContent = gist.files[GIST_FILENAME].content

    const movieList = JSON.parse(oldContent)

    const updatedMovieList = movieList.concat([datum])

    const request = {
      files: {
        [GIST_FILENAME]: {
          content: JSON.stringify(updatedMovieList),
        },
      },
    }

    const newGist = await gistClient.update(GIST_ID, request)
  }
})
