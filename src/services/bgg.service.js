import { bggApi } from '@/services/bgg-api'

export default {
  search,
  fetch,
}

function search(search) {
  return bggApi
    .get('/search/', {
      params: {
        type: 'boardgame',
        query: search,
      },
    })
    .then(response => {
      if (!response.items || !response.items.item) {
        return []
      }
      let items = response.items.item

      items = items.map(item => {
        item.name = getGameName(item)
        item.rank = calculateRank(item.name, search)
        return item
      })

      items.sort((a, b) => b.rank - a.rank)

      items = items.slice(0, 30)

      return items.map(item => mapGame(item))
    })
}

function fetch(id) {
  return bggApi
    .get('/thing/', {
      params: {
        // type: 'boardgame',
        id: id,
      },
    })
    .then(response => {
      if (!response.items || !response.items.item) {
        return {}
      }

      let game = response.items.item

      game.name = getGameName(game)

      return mapGame(response.items.item)
    })
}

function mapGame(game) {
  return {
    id: game.id,
    name: game.name,
    year: game.yearpublished ? game.yearpublished.value : '',
    thumbnail: game.thumbnail ? game.thumbnail : '',
    min_players: game.minplayers ? game.minplayers.value : '',
    max_players: game.maxplayers ? game.maxplayers.value : '',
    min_playtime: game.minplaytime ? game.minplaytime.value : '',
    max_playtime: game.maxplaytime ? game.maxplaytime.value : '',
    rank: game.rank,
  }
}

function calculateRank(name, search) {
  if (name) {
    search = search.trim().toUpperCase()
    name = name.trim().toUpperCase()

    if (name === search) {
      return 4
    } else if (name.startsWith(search)) {
      return 3
    } else if (name.includes(search)) {
      return 2
    } else {
      return 1
    }
  } else {
    return 0
  }
}

function getGameName(game) {
  return decodeHTML(
    Array.isArray(game.name) ? game.name[0].value : game.name.value,
  )
}

function decodeHTML(value) {
  return new DOMParser()
    .parseFromString(value, 'text/html')
    .querySelector('html').textContent
}
