const _ = require('lodash')
const getData = require('./database/getData')
const gistClient = require('./providers/gistClient')
const writeData = require('./database/writeData')

const URL_PATH = 'embeds[0].url'
const TITLE_PATH = 'embeds[0].title'
const YEAR_PATH = 'embeds[0].year'

const wasUpdatedWithInfo = (old, current) => {
  const oldUrl = _.get(old, URL_PATH)
  const url = _.get(current, URL_PATH)
  return !oldUrl && url && url.includes('themoviedb.org/movie')
}

const isExistingRequest = (requests, url) => _.find(
  requests,
  (movie) => movie.url === url,
)

const isDeniedRequest = (denyList, url) => _.find(
  denyList,
  (movie) => movie.url === url,
)

/**
 * Updates secret gist with movie information
 */
module.exports =  async (old, current) => {
  if (!wasUpdatedWithInfo(old, current)) {
    return
  }

  const url = _.get(current, URL_PATH)
  const title = _.get(current, TITLE_PATH)
  const year = _.get(current, YEAR_PATH)

  const data = await getData(gistClient)
  const { requests, denyList } =  data;

  if (isExistingRequest(requests, url)) {
    return current.reply(`${title} has already been requested. Sorry.`)
  }

  if (isDeniedRequest(denyList, url)) {
    return current.reply(`
      Big Rick says NO THANKS. BIG RICK DENIES ${title}.
      Maybe ask Big Rick to stop denying your freedoms.
    `)
  }

  const request = {
    title,
    url,
    year,
  }
  const updatedRequests = requests.concat([request])
  const updatedData = { ...data, requests: updatedRequests }
  const newGist = await writeData(gistClient, updatedData)

  return current.reply(`
    I'm Leo Getz, and whatever you want, Leo gets, ayyyyye.
    Leo will be getting ${title} for you today, all right?!
  `)
}
