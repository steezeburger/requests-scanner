require('dotenv').config()
const {
  GIST_ID,
  GIST_FILENAME,
} = process.env;

module.exports =  async (client, data) => {
  const requestData = {
    files: {
      [GIST_FILENAME]: {
        content: JSON.stringify(data),
      },
    },
  }
  const gist = await client.update(GIST_ID, requestData)
  return gist
}
