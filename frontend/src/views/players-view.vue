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
        &nbsp;
        <button><router-link to="/player-edit/0">Add Player</router-link></button>

    </div>

    <div class="player-list" v-if="players.length">
      <div
        v-for="player in filteredPlayers"
        :key="player.name"
        class="player-card"
      >
        <router-link :to="{ name: 'player-info', params: { id: player.id } }">Player Info</router-link>
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
          <button v-if="player.notes.length > 3" @click="saveNote(player)">Save</button>
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
      players: [
        { id: 1, name: 'Player 1', team: 'Team A', number: 5, position: 'Forward', grad: 2025, notes: ''  },
        { id: 2,  name: 'Player 2', team: 'Team A', number: 28, position: 'Defense', grad: 2026, notes: '' },
        { id: 3,  name: 'Player 3', team: 'Team B', number: 82, position: 'Goalie', grad: 2027, notes: '' },
        { id: 4,  name: 'Player 4', team: 'Team B', number: 99, position: 'Forward', grad: 2025, notes: '' },
        { id: 5,  name: 'Player 5', team: 'Team C', number: 13, position: 'Defense', grad: 2027, notes: '' },
        { id: 6,  name: 'Player 6', team: 'Team C', number: 15, position: 'Forward', grad: 2026, notes: '' },
        { id: 7,  name: 'Player 7', team: 'Team D', number: 11, position: 'Forward', grad: 2025, notes: '' },
        { id: 8,  name: 'Player 8', team: 'Team D', number: 6, position: 'Goalie', grad: 2028, notes: '' },
      ],
      teams: ['Team A', 'Team B', 'Team C', 'Team D'],
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
          !this.filters.position || player.position.toUpperCase().indexOf(this.filters.position.toUpperCase()) !== -1;
        const matchesGrad =
          !this.filters.grad || player.grad === Number(this.filters.grad);

        return matchesName && matchesTeam && matchesPosition && matchesGrad;
      });
    },
  },

  created() {
    // fetch on init
    this.fetchTeams()
  },

  methods: {
    async fetchTeams() {
      const url = 'http://localhost/api/search/team?all';
      const response = await (await fetch(url)).json();
      console.log('Request succeeded with JSON response', response);
      var teams = [];
      var players = [];
      response.data.forEach((t)=>{
        teams.push(t.name);
        t.players.forEach((p)=>{
          players.push({ id: p.id, name: p.first_name+' '+p.last_name, team: t.name, number: p.number_on_team, position: p.position, grad: p.grad_year, notes:''  });
        });
      });
      this.teams = teams;
      this.players = players;
    },

    async saveNote(player){
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ player: player.id, content: player.notes })
      };
      const response = await fetch("http://localhost/api/create/note", requestOptions);
      const data = await response.json();
      if (data.data.id) {
        console.log("Note saved id", data.data.id);   
        //clear form
        player.notes = '';
      } else {
        alert("Error saving note");
      }
    }
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