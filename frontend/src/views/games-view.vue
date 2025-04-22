<template>
  <div>
    <div class="dropdown-row">
      <select id="team1" v-model="selectedTeam1">
        <option value="" disabled>Select team</option>
        <option v-for="team in teams" :key="team.id" :value="team.name">
          {{ team.name }}
        </option>
      </select>

      <div class="vs-text">vs.</div>

      <select id="team2" v-model="selectedTeam2">
        <option value="" disabled>Select team</option>
        <option v-for="team in teams" :key="team.id" :value="team.name">
          {{ team.name }}
        </option>
      </select>
    </div>

    <div class="teams-container" v-if="selectedTeam1 && selectedTeam2">
      <div class="team">
        <h3 style="margin-bottom: 30px">{{ selectedTeam1 }}</h3>
        <ul>
          <li v-for="player in getPlayers(selectedTeam1)" :key="player.id">
            <div>
              <strong><span style="color: #ffcd00">#{{ player.number_on_team }}</span>&nbsp; {{ player.first_name }} {{ player.last_name }}</strong>
              <br>Position: {{ player.position }} <br> Graduation Year: {{ player.grad }}
            </div>
          </li>
        </ul>
      </div>

      <div class="team">
        <h3 style="margin-bottom: 30px">{{ selectedTeam2 }}</h3>
        <ul>
          <li v-for="player in getPlayers(selectedTeam2)" :key="player.id">
            <div>
              <strong><span style="color: #ffcd00">#{{ player.number_on_team }}</span>&nbsp; {{ player.first_name }} {{ player.last_name }}</strong>
              <br>Position: {{ player.position }} <br> Graduation Year: {{ player.grad }}
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
      teams: [], // Teams will be dynamically populated
      selectedTeam1: '',
      selectedTeam2: '',
    };
  },
  methods: {
    fetchTeams() {
      // Simulate fetching data from an API
      const response = {
        status: "success",
        data: [
          {
            id: 1,
            name: "The Puckaneers",
            coach_first_name: "Jamie",
            coach_last_name: "Bennet",
            coach_email: "jamie.bennet@example.com",
            players: [
              { id: 5, first_name: "Jona", last_name: "Baldwin", date_of_birth: "2003-02-20", position: "Defense", number_on_team: 27 },
              { id: 6, first_name: "Lily", last_name: "Schultz", date_of_birth: "2005-09-20", position: "Defense", number_on_team: 13 },
              { id: 7, first_name: "Gianna", last_name: "Bartells", date_of_birth: "2000-08-21", position: "Forward", number_on_team: 4 },
            ],
          },
          {
            id: 2,
            name: "Tigers",
            coach_first_name: "Lola",
            coach_last_name: "Caines",
            coach_email: "lola.caines@example.com",
            players: [
              { id: 1, first_name: "Janette", last_name: "Lane", date_of_birth: "2001-06-18", position: "Defense", number_on_team: 2 },
              { id: 2, first_name: "Jay", last_name: "Stacy", date_of_birth: "2003-06-18", position: "Goalie", number_on_team: 87 },
              { id: 3, first_name: "Gigi", last_name: "Bartells", date_of_birth: "2002-04-21", position: "Goalie", number_on_team: 11 },
              { id: 4, first_name: "Maria", last_name: "Rory-Smith", date_of_birth: "2003-03-20", position: "Forward", number_on_team: 25 },
            ],
          },
        ],
      };

      // Process the data into teams
      const teams = response.data;

      // Add graduation year to each player
      teams.forEach((team) => {
        team.players.forEach((player) => {
          const birthYear = new Date(player.date_of_birth).getFullYear();
          player.grad = birthYear + 18; // Assuming graduation year is birth year + 18
        });
      });

      this.teams = teams;
    },
    getPlayers(teamName) {
      const team = this.teams.find((team) => team.name === teamName);
      return team ? team.players : [];
    },
  },
  mounted() {
    this.fetchTeams(); // Fetch teams when the component is mounted
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