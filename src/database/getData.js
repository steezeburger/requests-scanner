require('dotenv').config()
const {
  GIST_ID,
  GIST_FILENAME,
} = process.env;

module.exports = async (client) => {
  const gist = await client.getOneById(GIST_ID)
  const content = gist.files[GIST_FILENAME].content
  const data = JSON.parse(content)
  return data
}
