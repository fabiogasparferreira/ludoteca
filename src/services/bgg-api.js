import axios from 'axios'

export { bggApi }

const parser = require('xml2json-light')

const API_URL = 'https://www.boardgamegeek.com/xmlapi2'

const TIMEOUT = 7000

const bggApi = axios.create({
  baseURL: API_URL,
  timeout: TIMEOUT,
})

bggApi.interceptors.response.use(response => {
  return parser.xml2json(response.data)
})
