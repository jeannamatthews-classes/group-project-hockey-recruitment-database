<template>
  <div class="player-info-view">
    <router-link class="btn" v-if="player.id > 0" :to="{ name: 'player-info', params: { id: player.id } }">Player Info</router-link>

    <!-- Photo Section -->
    <div class="photo-section">
      <img 
        src="@/assets/placeholder.jpg"
        alt="Player Photo"
        class="player-photo"
      >
    </div>

    <!-- Details Grid -->
    <div class="details-grid">
      <div class="detail-item">
        <span class="detail-label">Name:</span>
        <span class="detail-value"><input type="text" v-model="player.first_name" placeholder="First"/><input type="text" v-model="player.last_name" placeholder="Last"/></span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Rank:</span>
        <span class="detail-value"><input type="text" v-model="player.rank"/></span>
      </div>

      <div class="detail-item">
        <span class="detail-label">Number:</span>
        <span class="detail-value">#<input type="text" v-model="player.number"/></span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Phone:</span>
        <span class="detail-value"><input type="text" v-model="player.phone"/></span>
      </div>

      <div class="detail-item">
        <span class="detail-label">Position:</span>
        <span class="detail-value"><input type="text" v-model="player.position"/></span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Email:</span>
        <span class="detail-value"><input type="text" v-model="player.email"/></span>
      </div>

      <div class="detail-item">
        <span class="detail-label">Year:</span>
        <span class="detail-value"><input type="text" v-model="player.year"/></span>
      </div>

      <div class="detail-item">
        <span class="detail-label">DOB:</span>
        <span class="detail-value"><input type="text" v-model="player.date_of_birth"/></span>
      </div>
    </div>
    <button class="btn" v-if="player.first_name && player.last_name" @click="savePlayer(player)">Save</button>
  </div>

    <!-- Current Teams Section -->
    <h3 v-if="memberships.length">Current Teams</h3>
    <div class="details-grid" v-for="m in memberships" :key="m.team_id">
      <div class="detail-item">
        <span class="detail-label">Team:</span>
        <span class="detail-value">{{ m.team.name }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Number:</span>
        <span class="detail-value">
          <input
            type="number"
            v-model.number="m.number_on_team"
            min="1"
            max="99"
          />
        </span>
        <button class="btn-outline" @click="saveTeamPlayer(m.team_id, { id: player.id, number_on_team: m.number_on_team })">Save</button>
        <button class="btn-outline" @click="removeTeamPlayer(m.team_id, { id: player.id })">Remove</button>
      </div>
    </div>

    <!-- Add to Team Section -->
    <div>
      <h3>Add to Team</h3>
      <div class="details-grid">
        <div class="detail-item">
          <span class="detail-label">Team:</span>
          <span class="detail-value">
            <select v-model="newMembership.team_id">
              <option :value="0">Select Team</option>
              <option v-for="t in teams" :key="t.id" :value="t.id">{{ t.name }}</option>
            </select>
          </span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Number:</span>
          <span class="detail-value">
            <input
              type="number"
              v-model.number="newMembership.number_on_team"
              placeholder="1-99"
              min="1"
              max="99"
            />
          </span>
          <button class="btn" :disabled="!addFormValid" @click="addTeamPlayer(newMembership.team_id, { id: player.id, number_on_team: newMembership.number_on_team })">
            Add
          </button>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  name: 'PlayerInfoView',
  data() {
    return {
      player: {
        id: this.$route.params.id,        
        first_name: "Player",
        last_name: this.$route.params.id,
        rank: 99,
        number:  this.$route.params.id,
        phone: "(555) 555-5555",
        position: "Forward",
        email: "player@clarkson.edu",
        year: 2026,
        date_of_birth: "2004-06-07"
      },
      teams: [],
      memberships: [],
      newMembership: {
        team_id: 0,
        number_on_team: null
      }
    };
  },
  computed: {
    addFormValid() {
      const num = this.newMembership.number_on_team;
      return this.newMembership.team_id > 0 && Number.isInteger(num) && num >= 1 && num <= 99;
    }
  },
  created() {
    // fetch on init
    if (this.player.id > 0) {
      this.fetchPlayer(this.player.id);
      this.fetchMemberships(this.player.id);
      this.fetchTeams();
    } else {
      this.fetchTeams();
      this.player = {
        id: 0,
        first_name: "",
        last_name: "",
        rank: undefined,
        number: undefined,
        phone: undefined,
        position: undefined,
        email: undefined,
        year: undefined,
        date_of_birth: undefined
      };
    }
  },
  methods: {
    async fetchPlayer(id) {
      const url = 'http://localhost/api/get/player?id='+id;
      const response = await (await fetch(url)).json();
      console.log('Request succeeded with JSON response', response);
      this.player = response.data;
    },
    async fetchTeams() {
      const resp = await (await fetch('http://localhost/api/search/team?all')).json();
      this.teams = resp.data;
    },
    async fetchMemberships(playerId) {
      const resp = await (await fetch(`http://localhost/api/search/team_membership?player_id=${playerId}`)).json();
      this.memberships = resp.data;
    },
    async saveTeamPlayer(team_id, player) {
      if (!player.id || !player.number_on_team) return;
      const body = JSON.stringify({ team_id, player_id: player.id, number_on_team: player.number_on_team });
      const opts = { method: 'POST', headers: { 'Content-Type': 'application/json' }, body };
      const resp = await (await fetch('http://localhost/api/update/team_membership', opts)).json();
      if (resp.data && resp.data.id) this.fetchMemberships(this.player.id);
      else alert('Error saving membership');
    },
    async removeTeamPlayer(team_id, player) {
      const body = JSON.stringify({ team_id, player_id: player.id });
      const opts = { method: 'POST', headers: { 'Content-Type': 'application/json' }, body };
      const resp = await (await fetch('http://localhost/api/delete/team_membership', opts)).json();
      if (resp.success) this.fetchMemberships(this.player.id);
      else alert('Error removing membership');
    },
    async addTeamPlayer(team_id, player) {
      if (!player.id || !player.number_on_team) return;
      const body = JSON.stringify({ team_id, player_id: player.id, number_on_team: player.number_on_team });
      const opts = { method: 'POST', headers: { 'Content-Type': 'application/json' }, body };
      const resp = await (await fetch('http://localhost/api/create/team_membership', opts)).json();
      if (resp.data && resp.data.id) {
        this.newMembership.team_id = 0;
        this.newMembership.number_on_team = null;
        this.fetchMemberships(this.player.id);
      } else alert('Error adding membership');
    },
    async savePlayer(player){
      this.player.rank = Number(this.player.rank) 
      const body = JSON.stringify(player);
      console.log(body);
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body
      };
      var mode = "create";
      if (player.id) mode = "update"; 
      const response = await fetch("http://localhost/api/"+mode+"/player", requestOptions);
      const data = await response.json();
      if (data.data.id) {
        console.log("Player saved id", data.data.id);   
      } else {
        alert("Error saving player");
      }
    }

  }

};
</script>

<style scoped>
.player-info-view {
  padding: 30px;
  max-width: 1000px;
  margin: 20px auto;
  background: #004e42;
  border-radius: 12px;
  color: #fff;
  font-family: "Montserrat", sans-serif;
}

.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #ffcd00;
  color: #004e42;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  margin-bottom: 15px;
}
.btn:hover {
  background-color: #ffd633;
  transform: translateY(-1px);
}

.btn-outline {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: none;
  border: 2px solid #ffcd00;
  border-radius: 6px;
  color: #ffcd00;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
  margin-right: 8px;
}
.btn-outline:hover {
  background-color: #ffcd00;
  color: #004e42;
}

input[type="text"],
input[type="number"],
input[type="date"],
select {
  width: 70%;                
  height: 2rem;               
  padding: 0 0.5rem;          
  margin-top: 0;             
  background: #006d5b;
  border: 1px solid rgba(255, 205, 0, 0.7);
  border-radius: 6px;
  color: #fff;
  font-family: inherit;
  font-size: 1rem;
  box-sizing: border-box;
}

.photo-section {
  text-align: center;
  margin-bottom: 25px;
}

.player-photo {
  width: 220px;
  height: 220px;
  border-radius: 8px;
  border: 3px solid #ffcd00;
  object-fit: cover;
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

.detail-link {
  color: #ffcd00;
  text-decoration: none;
}

.detail-link:hover {
  text-decoration: underline;
}

.tabs-section {
  margin-top: 25px;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  background: #01463c;
  color: #fff;
  cursor: pointer;
  font-weight: 600;
  transition: 0.2s;
}

.tabs button.active {
  background: #ffcd00;
  color: #000;
}

.notes-textarea {
  width: 100%;
  min-height: 150px;
  padding: 15px;
  border: 2px solid #ffcd00;
  border-radius: 8px;
  background: #01463c;
  color: #fff;
  font-family: inherit;
  font-size: 1rem;
  resize: vertical;
}

.video-placeholder,
.stats-placeholder {
  text-align: center;
  padding: 40px;
  background: #01463c;
  border-radius: 8px;
  font-size: 1.1rem;
  color: #ffcd00;
}

.notes-table {
  width: 100%;
  border-collapse: collapse;
  background: #01463c;
  border-radius: 8px;
  overflow: hidden;
}

.notes-table th,
.notes-table td {
  padding: 12px 15px;
  text-align: left;
}

.notes-table th {
  background: #01352e;
  color: #ffcd00;
  font-weight: 600;
}

.notes-table tr:nth-child(even) {
  background: #005c4d;
}

.date-col {
  width: 15%;
  min-width: 120px;
}

.coach-col {
  width: 15%;
  min-width: 150px;
}

.note-col {
  width: 70%;
}

.note-content {
  white-space: pre-wrap;
  line-height: 1.5;
}
</style>