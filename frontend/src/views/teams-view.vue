<template>

    <div>
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
    <button v-if="team.name.length > 3" @click="saveTeam(team)">Save</button>    
  </template>
  
  <script>
  export default {
    name: 'TeamView',
    data() {
      return {
        teams: [
          {id:1, name:"Team A", coach_first_name:"Coach", coach_last_name:"1"},
          {id:2, name:"Team B", coach_first_name:"Coach", coach_last_name:"2"},
          {id:3, name:"Team C", coach_first_name:"Coach", coach_last_name:"3"},
        ],
        team: {id:0, name:"", coach_first_name:"", coach_last_name:""},
        selectedTeamId: ''
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
      async saveTeam(team){
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