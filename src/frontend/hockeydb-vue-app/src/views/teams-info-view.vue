<template>

    <div>
        <select v-model="filters.team" class="filter-select">
          <option value="">All Teams</option>
          <option v-for="team in teams" :key="team" :value="team">
            {{ team }}
          </option>
        </select>
    </div>
      <input
          type="text"
          v-model="filters.team"
          placeholder="Search by Team"
          class="filter-select"
        />
    <div>

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
          <p>Grad: {{ player.grad }}</p>
        </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TeamView',
    data() {
      return {
        players: [
          { name: 'Player 1', team: 'Team A', position: 'Forward', grad: 2025 },
          { name: 'Player 2', team: 'Team A', position: 'Defense', grad: 2026 },
          { name: 'Player 3', team: 'Team A', position: 'Goalie', grad: 2026 },
          { name: 'Player 2', team: 'Team B', position: 'Defense', grad: 2025 },
          { name: 'Player 1', team: 'Team B', position: 'Forward', grad: 2027 },
          { name: 'Player 3', team: 'Team B', position: 'Goalie', grad: 2026 },
          { name: 'Player 4', team: 'Team C', position: 'Forward', grad: 2026 },
          { name: 'Player 1', team: 'Team C', position: 'Goalie', grad: 2025 },
          { name: 'Player 1', team: 'Team C', position: 'Defense', grad: 2027 },
        ],
        teams: ['Team A', 'Team B', 'Team C'],
        positions: ['Forward', 'Defense', 'Goalie'],
        filters: {
          name: '',
          team: '',
          position: '',
          grad: '',
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
          const matchesGrad =
            !this.filters.grad || player.grad === Number(this.filters.grad);

          return matchesName && matchesTeam && matchesPosition && matchesGrad;
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