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
              <strong><span style="color: #ffcd00">#{{ player.number }}</span>&nbsp; {{ player.name }}</strong>
              <br>Position: {{ player.position }} <br> Graduation Year: {{ player.grad }}
            </div>
            <div>
              <label for="notes">Notes:</label>
              <textarea
                v-model="player.notes"
                class="notes-textarea"
                placeholder="Add notes here..."
              ></textarea>
            </div>
          </li>
        </ul>
      </div>

      <div class="team">
        <h3 style="margin-bottom: 30px">{{ selectedTeam2 }}</h3>
        <ul>
          <li v-for="player in getPlayers(selectedTeam2)" :key="player.name">
            <div>
              <strong><span style="color: #ffcd00">#{{ player.number }}</span>&nbsp; {{ player.name }}</strong>
              <br>Position: {{ player.position }} <br> Graduation Year: {{ player.grad }}
            </div>
            <div>
              <label for="notes">Notes:</label>
              <textarea
                v-model="player.notes"
                class="notes-textarea"
                placeholder="Add notes here..."
              ></textarea>
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
            { name: 'Player 1', number: 5, position: 'Forward', grad: 2025, notes: 'Top scorer' },
            { name: 'Player 2', number: 28, position: 'Defense', grad: 2026, notes: 'Strong defense' },
          ],
        },
        {
          name: 'Team B',
          players: [
            { name: 'Player 3', number: 82, position: 'Goalie', grad: 2027, notes: 'Strong player'},
            { name: 'Player 4', number: 99, position: 'Forward', grad: 2025, notes: 'Fast'},
          ],
        },
        {
          name: 'Team C',
          players: [
            { name: 'Player 5', number: 13, position: 'Defense', grad: 2027, notes: 'Good passes' },
            { name: 'Player 6', number: 15, position: 'Forward', grad: 2026, notes: 'Good shots' },
          ],
        },
        {
          name: 'Team D',
          players: [
            { name: 'Player 7', number: 11, position: 'Forward', grad: 2025, notes: 'Good shots' },
            { name: 'Player 8', number: 6, position: 'Goalie', grad: 2028, notes: 'Strong player'},
          ],
        },
      ],
      selectedTeam1: '',
      selectedTeam2: '',
    };
  },
  methods: {
    getPlayers(teamName) {
      const team = this.teams.find((team) => team.name === teamName);
      return team ? team.players : [];
    },
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