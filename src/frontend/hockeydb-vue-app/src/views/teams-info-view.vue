<template>

    <div>
        <select v-model="filters.team" class="filter-select">
          <option value="">All Teams</option>
          <option v-for="team in teams" :key="team" :value="team">
            {{ team }}
          </option>
        </select>
    </div>

    <div class="team-list">
      <div
        v-for="player in filteredPlayers"
          :key="player.name"
          class="player-box"
        >
          <h3>{{ player.name }}</h3>
          <p>Team: {{ player.team }}</p>
          <p>Position: {{ player.position }}</p>
          <p>Age: {{ player.age }}</p>
        </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TeamView',
    data() {
      return {
        players: [
          { name: 'Player 1', team: 'Team A', position: 'Forward', age: 18 },
          { name: 'Player 2', team: 'Team A', position: 'Defense', age: 19 },
          { name: 'Player 3', team: 'Team A', position: 'Goalie', age: 21 },
          { name: 'Player 2', team: 'Team B', position: 'Defense', age: 19 },
          { name: 'Player 1', team: 'Team B', position: 'Forward', age: 18 },
          { name: 'Player 3', team: 'Team B', position: 'Goalie', age: 20 },
          { name: 'Player 4', team: 'Team C', position: 'Forward', age: 21 },
          { name: 'Player 1', team: 'Team C', position: 'Goalie', age: 20 },
          { name: 'Player 1', team: 'Team C', position: 'Defense', age: 23 },
        ],
        teams: ['Team A', 'Team B', 'Team C'],
        positions: ['Forward', 'Defense', 'Goalie'],
        filters: {
          name: '',
          team: '',
          position: '',
          age: '',
        },
      };
    },
    computed: {
      filteredPlayers() {
        return this.players.filter((player) => {
          const matchesName =
            !this.filters.name ||
            player.name.toLowerCase().includes(this.filters.name.toLowerCase());
          const matchesTeam =
            !this.filters.team || player.team === this.filters.team;
          const matchesPosition =
            !this.filters.position || player.position === this.filters.position;
          const matchesAge =
            !this.filters.age || player.age === Number(this.filters.age);

          return matchesName && matchesTeam && matchesPosition && matchesAge;
        });
      },
    },
  };
  </script>
  
  <style>
  .filters {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
  }

  .filter-input,
  .filter-select {
    padding: 5px;
    font-size: 1rem;
    border: 1px solid #ddd;
    border-radius: 5px;
  }

  .player-box {
    margin: 0 100px;
    margin-top: 20px;
    padding: 0 20px;
    border: 1px solid #01463c;
    border-radius: 5px;
    background-color: #004e42;
    text-align: left;
    color: #fff;
    font-family: "Montserrat", sans-serif;
  }
</style>