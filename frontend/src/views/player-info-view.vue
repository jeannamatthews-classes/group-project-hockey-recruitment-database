<template>
  <div class="player-info-view">
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
        <span class="detail-value">{{ player.name }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Rank:</span>
        <span class="detail-value">{{ player.rank }}</span>
      </div>

      <div class="detail-item">
        <span class="detail-label">Number:</span>
        <span class="detail-value">#{{ player.number }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Phone:</span>
        <span class="detail-value">{{ player.phone }}</span>
      </div>

      <div class="detail-item">
        <span class="detail-label">Position:</span>
        <span class="detail-value">{{ player.position }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Email:</span>
        <span class="detail-value">{{ player.email }}</span>
      </div>

      <div class="detail-item">
        <span class="detail-label">Year:</span>
        <span class="detail-value">{{ player.year }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Team Website:</span>
        <a :href="player.teamWebsite" class="detail-link">{{ player.teamWebsite }}</a>
      </div>

      <div class="detail-item">
        <span class="detail-label">School:</span>
        <span class="detail-value">{{ player.school }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Coach Email:</span>
        <span class="detail-value">{{ player.coachEmail }}</span>
      </div>
    </div>

    <!-- Tabs Section -->
    <div class="tabs-section">
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab" 
          @click="activeTab = tab"
          :class="{ 'active': activeTab === tab }"
        >
          {{ tab }}
        </button>
      </div>

      <div class="tab-content">
      <!-- Notes Tab -->
      <div v-if="activeTab === 'Notes'" class="notes-tab">
    <table class="notes-table">
      <thead>
        <tr>
          <th class="date-col">Date</th>
          <th class="coach-col">Coach</th>
          <th class="note-col">Note</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="note in notes">
          <td>{{note.date}}</td>
          <td>{{note.coach}}</td>
          <td>{{note.content}}</td>
        </tr>
      </tbody>
    </table>
  </div>

        <!-- Videos Tab -->
        <div v-if="activeTab === 'Videos'" class="videos-tab">
          <div class="video-placeholder">
            <p>🎥 Player videos will be displayed here</p>
          </div>
        </div>

        <!-- Stats Tab -->
        <div v-if="activeTab === 'Stats'" class="stats-tab">
          <div class="stats-placeholder">
            <p>📈 Season statistics will be displayed here</p>
          </div>
        </div>
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
        name: "",
        rank: "",
        number: 0,
        phone: "",
        position: "",
        email: "",
        year: "",
        teamWebsite: "",
        school: "",
        coachEmail: "",
        notes: ""
      },
      notes: [
        {
          date: '2025-01-01',
          coach: 'Coach',
          content: 'Content'
        },
      ],
      tabs: ['Notes', 'Videos', 'Stats'],
      activeTab: 'Notes'
    };
  },
  created() {
    // fetch on init
    this.fetchPlayer(4);
  },
  
  methods: {
    async fetchPlayer(id) {
      const url = 'http://localhost/api/get/player?id='+id;
      const response = await (await fetch(url)).json();
      console.log('Request succeeded with JSON response', response);
      const p = response.data;
      this.player = { name: p.first_name+' '+p.last_name, rank:p.rank, position: p.position, year: p.grad_year, phone: p.phone };
    },
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