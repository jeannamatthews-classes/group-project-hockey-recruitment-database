<template>
  <div>
    <div class="dropdown-row">

      <select id="team1" v-model="selectedTeam1">
        <option value="" disabled>Select team</option>
        <option v-for="team in teams" :key="team.name" :value="team.name">
          {{ team.name }}
        </option>
      </select>

      <div class="vs-text">vs.</div>

      <select id="team2" v-model="selectedTeam2">
        <option value="" disabled>Select team</option>
        <option v-for="team in teams" :key="team.name" :value="team.name">
          {{ team.name }}
        </option>
      </select>
    </div>

    <div class="teams-container" v-if="selectedTeam1 && selectedTeam2">
      <div class="team">
        <h3 style="margin-bottom: 30px">{{ selectedTeam1 }}</h3>
        <ul>
          <li v-for="player in getPlayers(selectedTeam1)" :key="player.name">
            <div>
              <strong><span style="color: #ffcd00">#{{ player.number_on_team }}</span>&nbsp; {{ player.first_name + ' ' + player.last_name }}</strong>
              <br>Position: {{ player.position }} <br> Graduation Year: {{ player.grad_year }}
            </div>
            <div>
              <label for="notes">Notes:</label>
              <textarea
                v-model="player.notes"
                class="notes-textarea"
                placeholder="Add notes here..."
              ></textarea>
              <button @click="saveNote(player)">Save</button>
            </div>
          </li>
        </ul>
      </div>

      <div class="team">
        <h3 style="margin-bottom: 30px">{{ selectedTeam2 }}</h3>
        <ul>
          <li v-for="player in getPlayers(selectedTeam2)" :key="player.id">
            <div>
              <strong><span style="color: #ffcd00">#{{ player.number_on_team }}</span>&nbsp; {{ player.first_name + ' ' + player.last_name  }}</strong>
              <br>Position: {{ player.position }} <br> Graduation Year: {{ player.grad_year }}
            </div>
            <div>
              <label for="notes">Notes:</label>
              <textarea
                v-model="player.notes"
                class="notes-textarea"
                placeholder="Add notes here..."
              ></textarea>
              <button @click="saveNote(player)">Save</button>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GameView',
  data() {
    return {
      teams: [ // example team info
        {
          name: 'Team A',
          players: [
            { id: 1, first_name: 'Player 1', last_name: '', number_on_team: 5, position: 'Forward', grad_year: 2025},
            { id: 2, first_name: 'Player 2', last_name: '', number_on_team: 28, position: 'Defense', grad_year: 2026},
          ],
        },
        {
          name: 'Team B',
          players: [
            { id: 3, first_name: 'Player 3', last_name: '', number_on_team: 82, position: 'Goalie', grad_year: 2027},
            { id: 4, first_name: 'Player 4', last_name: '', number_on_team: 99, position: 'Forward', grad_year: 2025},
          ],
        },
        {
          name: 'Team C',
          players: [
            { id: 5, first_name: 'Player 5', last_name: '', number_on_team: 13, position: 'Defense', grad_year: 2027},
            { id: 6, first_name: 'Player 6', last_name: '', number_on_team: 15, position: 'Forward', grad_year: 2026},
          ],
        },
        {
          name: 'Team D',
          players: [
            { id: 7, first_name: 'Player 7', last_name: '', number_on_team: 11, position: 'Forward', grad_year: 2025},
            { id: 8, first_name: 'Player 8', last_name: '', number_on_team: 6, position: 'Goalie', grad_year: 2028},
          ],
        },
      ],
      selectedTeam1: '',
      selectedTeam2: '',
    };
  },

  created() {
    // fetch on init
    this.fetchTeams()
  },

  methods: {
    getPlayers(teamName) {
      const team = this.teams.find((team) => team.name === teamName);
      var players = [];
      //Add notes field
      if (team.players){
        team.players.forEach((p)=>{
          players.push({id: p.id, first_name: p.first_name, last_name: p.last_name, number_on_team: p.number_on_team, position: p.position, grad_year: p.grad_year, notes: '' });
        });
        console.log(players);
        return players;
      } 
      return [];
    },

    async fetchTeams() {
      const url = 'http://localhost/api/search/team?all';
      const response = await (await fetch(url)).json();
      console.log('Request succeeded with JSON response', response);
      this.teams = response.data;
    },

    async saveNote(player){
      if (!player.notes) return;
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
  },
};
</script>

<style>
label {
  margin-right: 10px;
}

select {
  margin: 10px 20px;
  padding: 5px;
  font-size: 1rem;
}

p {
  margin-top: 20px;
  font-weight: bold;
}

.dropdown-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px; 
  /* color-scheme: #D3D3D3; */
}

.vs-text {
  margin: 0 20px;
  font-size: 1.2rem;
  font-weight: bold;
  color: rgb(55, 55, 55);
}

.teams-container {
  display: flex;
  justify-content: space-between; 
  margin-top: 20px;
  padding: 0 20px;
  flex-wrap: nowrap;
  color: #fff;
  font-family: "Montserrat", sans-serif;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.team {
  width: 48%; 
  background-color: #004e42;
  padding: 30px;
  border: 1px solid #01463c;
  border-radius: 5px;
  box-sizing: border-box;
}

.team h3 {
  text-align: center;
  margin-bottom: 10px;
}

.team ul {
  list-style-type: none;
  padding: 0;
}

.team li {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  border-bottom: 1px solid #ffcd00;
  margin-top: 5px;
  margin-bottom: 5px;
  text-align: left;
}

.team li:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.notes {
  font-size: 1rem;
  margin-left: 10px;
  text-transform: none;
}

.notes-textarea {
  width: 100%;
  margin-top: 5px;
  padding: 5px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  resize: vertical; /* Allow vertical resizing */
  box-sizing: border-box;
  min-height: 30px;
  margin-bottom: 10px;
}

.notes-textarea:focus {
  outline: none;
  border-color: #ffcd00;
  box-shadow: 0 0 5px rgba(255, 205, 0, 0.5);
}

</style>