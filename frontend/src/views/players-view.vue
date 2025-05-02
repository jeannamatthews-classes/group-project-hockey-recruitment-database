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
          v-model="filters.grad"
          placeholder="Search by Grad. Year"
          class="filter-input"
        />
    </div>

    <div class="player-list">
      <div
        v-for="player in filteredPlayers"
        :key="player.name"
        class="player-card"
      >
        <h3><span style="color: #ffcd00">#{{ player.number }} </span> &nbsp {{ player.name }}</h3>
        <div class="player-divider"></div>
        <p>Team: {{ player.team }}</p>
        <p>Position: {{ player.position }}</p>
        <p>Graduation Year: {{ player.grad }}</p>
        <div class="player-notes">
          <label for="notes"><strong>Notes:</strong></label>
          <textarea
              v-model="player.notes"
              class="notes-textarea"
              placeholder="Add notes here..."
          ></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlayerView',
  data() {
    return {
      players: [],
      teams: [],
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

  created() {
    // fetch on init
    this.fetchTeams()
    //this.fetchPlayers()
  },

  methods: {
    async fetchPlayers() {
      const url = 'http://localhost/api/search/player?all';
      const response = await (await fetch(url)).json();
      console.log('Request succeeded with JSON response', response);
      var players = [];
      response.data.forEach((d)=>{
        players.push({ name: d.first_name+' '+d.last_name, team: 'Team A', number:'' , position: d.position, grad: d.grad_year, notes:''  });
      });

      console.log(players);
      this.players = players;
    },
    async fetchTeams() {
      const url = 'http://localhost/api/search/team?all';
      const response = await (await fetch(url)).json();
      console.log('Request succeeded with JSON response', response);
      var teams = [];
      var players = [];
      response.data.forEach((t)=>{
        teams.push(t.name);
        t.players.forEach((p)=>{
          players.push({ name: p.first_name+' '+p.last_name, team: t.name, number: p.number_on_team, position: p.position, grad: p.grad_year, notes:''  });
        });
      });
      this.teams = teams;
      this.players = players;
    },
  }
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
  margin: 20px;
  color: #fff;
}

.player-card {
  text-align: left;
  background-color: #004e42;
  padding: 30px;
  border: 1px solid #01463c;
  border-radius: 5px;
  box-sizing: border-box;
}

.players-search {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.player-divider {
  width: 100%;
  height: 1px; /* Thin horizontal line */
  background-color: #ffcd00; /* Yellow color */
  margin: 10px 0; /* Add spacing above and below the line */
}

</style>