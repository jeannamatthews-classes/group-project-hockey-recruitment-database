<template>

  <div class="filters">
      <select v-model="selectedTeamId" class="filter-select" @change="selectTeam()">
        <option value="">Add Team</option>
        <option v-for="t in teams" :key="t.id" :value="t.id">
          {{ t.name }}
        </option>
      </select>
  </div>
  <div>

  </div>

  <div class="details-grid">
    <div class="detail-item">
      <span class="detail-label">Team Name:</span>
      <span class="detail-value"><input type="text" v-model="team.name"/></span>
    </div>
    <div class="detail-item">
      <span class="detail-label">Coach Name:</span>
      <span class="detail-value"><input type="text" v-model="team.coach_first_name" placeholder="First"/><input type="text" v-model="team.coach_last_name" placeholder="Last"/></span>
    </div>
  </div>
  <button class="btn" :disabled="!team.name || !team.name.trim().length" @click="saveTeam(team)">Save</button>     

  <h3 v-if="team.players">Players</h3>
  <div class="details-grid" v-for="player in team.players" :key="player.name">
    <div class="detail-item">
      <span class="detail-label">Name:</span>
      <span class="detail-value">{{ player.first_name }} {{ player.last_name }}</span>
    </div>
    <div class="detail-item">
      <span class="detail-label">Number:</span>
      <span class="detail-value"><input type="text" v-model="player.number_on_team" placeholder=""/></span>
      <button class="btn-outline" @click="saveTeamPlayer(team.id, player)">Save</button>  
      <button class="btn-outline" @click="removeTeamPlayer(team.id, player)">Remove</button>  
    </div>
  </div>

</template>

<script>
export default {
  name: 'TeamView',
  data() {
    return {
      teams: [
        {id:1, name:"Team A", coach_first_name:"Coach", coach_last_name:"1", players:[
        { id: 1, first_name: 'Player 1', last_name: '', number_on_team: 5, position: 'Forward', grad_year: 2025},
        { id: 2, first_name: 'Player 2', last_name: '', number_on_team: 28, position: 'Defense', grad_year: 2026},
      ]},
        {id:2, name:"Team B", coach_first_name:"Coach", coach_last_name:"2", players:[
        { id: 1, first_name: 'Player 3', last_name: '', number_on_team: 5, position: 'Forward', grad_year: 2025},
        { id: 2, first_name: 'Player 4', last_name: '', number_on_team: 28, position: 'Defense', grad_year: 2026},
      ]},
        {id:3, name:"Team C", coach_first_name:"Coach", coach_last_name:"3", players:[
        { id: 1, first_name: 'Player 5', last_name: '', number_on_team: 5, position: 'Forward', grad_year: 2025},
        { id: 2, first_name: 'Player 6', last_name: '', number_on_team: 28, position: 'Defense', grad_year: 2026},
      ]},
      ],
      team: {id:0, name:"", coach_first_name:"", coach_last_name:""},
      selectedTeamId: '',
      players: [
        { id: 1, first_name: 'Player 1', last_name: '', number_on_team: 5, position: 'Forward', grad_year: 2025},
        { id: 2, first_name: 'Player 2', last_name: '', number_on_team: 28, position: 'Defense', grad_year: 2026},
      ],
    }
  },

  created() {
    // fetch on init
    this.fetchTeams();
  },

  methods:{
    selectTeam(){
      if (this.selectedTeamId > 0) this.team = this.teams[this.selectedTeamId-1];
      else this.team = {id:0, name:"", coach_first_name:"", coach_last_name:""};
    },

    async fetchTeams() {
      const url = 'http://localhost/api/search/team?all';
      const response = await (await fetch(url)).json();
      console.log('Teams response', response);
      this.teams = response.data;
    },
    async saveTeam(team) {
      const body = JSON.stringify(team);
      console.log(body);
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body
      };
      var mode = "create";
      if (team.id) mode = "update"; 
      const response = await fetch("http://localhost/api/"+mode+"/team", requestOptions);
      const data = await response.json();      
      if (data.data.id) {
        console.log("Team saved id", data.data.id);   
        this.fetchTeams(); //refresh listbox
        this.selectedTeamId = data.data.id;
      } else {
        alert("Error saving team");
      }
    },
    async saveTeamPlayer(team_id, player){
      if (!player.id || !player.number_on_team) return;
      const body = JSON.stringify({team_id: team_id, player_id: player.id, number_on_team: player.number_on_team});
      console.log(body);
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body
      };
      const response = await fetch("http://localhost/api/update/team_membership", requestOptions);
      const data = await response.json();      
      if (data.data.id) {
        console.log("Team Membership saved id", data.data.id);   
      } else {
        alert("Error saving team membership");
      }
    },

    async removeTeamPlayer(team_id, player){
      const body = JSON.stringify({team_id: team_id, player_id: player.id});
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body
      };
      const response = await fetch("http://localhost/api/delete/team_membership", requestOptions);
      const data = await response.json();      
      if (data.success) {
        console.log("Team Membership deleted");  
        this.fetchTeams(); //refresh list
      } else {
        alert("Error deleting team membership");
      }
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
.filter-select,
input[type="number"] {
 padding: 0.5rem;
  background: #006d5b;
  border: 1px solid #ffcd00;
  border-radius: 6px;
  color: #fff;
  font-size: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  background: #ffcd00;
  color: #004e42;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  margin: 15px 0;
  border: none;
}
.btn-outline {
  padding: 0.5rem 1rem;
  background: none;
  border: 2px solid #ffcd00;
  border-radius: 6px;
  color: #ffcd00;
  font-weight: 600;
  cursor: pointer;
  margin-left: 8px;
}

.details-grid {
display: grid;
grid-template-columns: 1fr 1fr;
gap: 15px;
margin-bottom: 30px;
padding: 20px;
background: #01463c;
border-radius: 8px;
}

.detail-item {
display: flex;
justify-content: space-between;
align-items: center;
padding: 12px;
background: #006d5b;
border-radius: 6px;
color: white;
}  

.detail-item:nth-child(odd) {
background: #005c4d;
}

.detail-label {
font-weight: 600;
color: #ffcd00;
}

.detail-value {
text-align: right;
}

</style>