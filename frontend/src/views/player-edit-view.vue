<template>
  <div class="player-info-view">
    <router-link v-if="player.id > 0" :to="{ name: 'player-info', params: { id: player.id } }">Player Info</router-link>

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
    <button v-if="player.first_name && player.last_name" @click="savePlayer(player)">Save</button>
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
        rank: "99",
        number:  this.$route.params.id,
        phone: "(555) 555-5555",
        position: "Forward",
        email: "player@clarkson.edu",
        year: "2026",
        date_of_birth: "06/07/2004"
      },
    };
  },
  created() {
    // fetch on init
    if (this.$route.params.id > 0) this.fetchPlayer(this.$route.params.id);
    else this.player = {
        id: 0,        
        first_name: "",
        last_name: "",
        rank: "",
        number:  "",
        phone: "",
        position: "",
        email: "",
        year: "",
        date_of_birth: ""
      }
  },
  
  methods: {
    async fetchPlayer(id) {
      const url = 'http://localhost/api/get/player?id='+id;
      const response = await (await fetch(url)).json();
      console.log('Request succeeded with JSON response', response);
      this.player = response.data;
    },
    async savePlayer(player){
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