require('dotenv').config()
const GistClient = require('gist-client')

const { GIST_TOKEN } = process.env;

const gistClient = new GistClient()
gistClient.setToken(GIST_TOKEN)

module.exports = gistClient
