export default {
  methods: {
    playtime: function(min, max) {
      let msg
      if (min === max) {
        msg = max
      } else {
        msg = min + ' - ' + max
      }
      return msg + ' min'
    },
    num_players: function(min, max) {
      if (min === max) {
        return min
      } else {
        return min + ' - ' + max
      }
    },
  },
}
