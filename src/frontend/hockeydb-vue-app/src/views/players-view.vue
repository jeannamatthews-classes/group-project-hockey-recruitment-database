<template>
  <div>
    <div>
        <input
          type="text"
          v-model="filters.name"
          placeholder="Search by name"
          class="filter-input"
        />


        <select v-model="filters.team" class="filter-select">
          <option value="">All Teams</option>
          <option v-for="team in teams" :key="team" :value="team">
            {{ team }}
          </option>
        </select>


        <select v-model="filters.position" class="filter-select">
          <option value="">All Positions</option>
          <option v-for="position in positions" :key="position" :value="position">
            {{ position }}
          </option>
        </select>


        <input
          type="number"
          v-model="filters.age"
          placeholder="Search by age"
          class="filter-input"
        />
    </div>

    <div class="player-list">
      <div
        v-for="player in filteredPlayers"
        :key="player.name"
        class="player-card"
      >
        <h3>{{ player.name }}</h3>
        <p>Team: {{ player.team }}</p>
        <p>Position: {{ player.position }}</p>
        <p>Age: {{ player.age }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlayerView',
  data() {
    return {
      players: [
        { name: 'Player 1', team: 'Team A', position: 'Forward', age: 18 },
        { name: 'Player 2', team: 'Team B', position: 'Defense', age: 19 },
        { name: 'Player 3', team: 'Team A', position: 'Goalie', age: 20 },
        { name: 'Player 4', team: 'Team C', position: 'Forward', age: 21 },
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

.player-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.player-card {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
  text-align: left;
}

.players-search {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

</style>