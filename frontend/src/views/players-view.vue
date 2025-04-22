<template>
  <div>

    <div class="search-container">
      <input v-model="search.first_name" placeholder="Search by First Name" class="filter-input" />
      <input v-model="search.last_name" placeholder="Search by Last Name" class="filter-input" />
      <input v-model="search.team" placeholder="Search by Team" class="filter-input" />
      <input v-model="search.position" placeholder="Search by Position" class="filter-input" />

      <div style="text-align: center; margin-bottom: 20px;">
        <button @click="showNewPlayerForm = !showNewPlayerForm" class="styled-button">
          {{ showNewPlayerForm ? 'Cancel' : 'Add New Player' }}
        </button>
      </div>
    </div>

    <div v-if="showNewPlayerForm" class="modal-overlay">
      <div class="modal-content">
        <h2>Add New Player</h2>
        <input v-model="newPlayer.first_name" placeholder="First Name" />
        <input v-model="newPlayer.last_name" placeholder="Last Name" />
        <input v-model="newPlayer.position" placeholder="Position" />
        <input v-model="newPlayer.date_of_birth" placeholder="YYYY-MM-DD" />
        <select v-model="newPlayer.team">
          <option disabled value="">Select a Team</option>
          <option v-for="team in teams" :key="team.id" :value="team.id">{{ team.name }}</option>
        </select>
        <div class="modal-buttons">
          <button @click="createPlayer" class="styled-button">Create Player</button>
          <button @click="showNewPlayerForm = false" class="styled-button cancel-button">Cancel</button>
        </div>
      </div>
    </div>

    <div class="player-list">
      <div v-for="player in filteredPlayers" :key="player.id" class="player-card">
        <h3>
          <span style="color: #ffcd00">#{{ player.number }}</span> &nbsp;
          <a href="#" @click.prevent="showPlayerDetails(player)">{{ player.first_name }} {{ player.last_name }}</a>
        </h3>
        <div class="player-divider"></div>
        <p>Team: {{ player.team }}</p>
        <p>Position: {{ player.position }}</p>
        <p>Birth Date: {{ formatDate(player.date_of_birth) }}</p>
        <!-- Notes Section -->
        <div class="player-notes">
          <label for="notes-{{ player.id }}"><strong>Notes:</strong></label>
          <textarea
            id="notes-{{ player.id }}"
            class="notes-textarea"
            placeholder="Add notes here..."
          ></textarea>
        </div>
      </div>

      <div
        v-for="popup in playerPopups"
        :key="popup.id"
        class="player-popup"
        :style="{ top: popup.top + 'px', left: popup.left + 'px', width: popup.width + 'px', height: popup.height + 'px' }"
        @mousedown="bringToFront(popup.id)"
      >
        <div class="popup-header" @mousedown="startDrag($event, popup.id)">
          <span>{{ popup.player.first_name }} {{ popup.player.last_name }}</span>
          <button class="close-button" @click="closePopup(popup.id)">X</button>
        </div>
        <div class="popup-content">
          <p><strong>Team:</strong> {{ popup.player.team }}</p>
          <p><strong>Position:</strong> {{ popup.player.position }}</p>
          <p><strong>Birth Date:</strong> {{ formatDate(popup.player.date_of_birth) }}</p>
          <p><strong>Notes:</strong></p>
          <textarea class="notes-textarea" placeholder="Add notes here..."></textarea>
        </div>
        <div class="popup-resizer" @mousedown="startResize($event, popup.id)"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      players: [],
      teams: [],
      search: {
        first_name: '',
        last_name: '',
        team: '',
        position: ''
      },
      showNewPlayerForm: false,
      newPlayer: {
        first_name: '',
        last_name: '',
        position: '',
        date_of_birth: '',
        team: ''
      },
      playerPopups: [], // Array to track open popups
      draggingPopup: null,
      resizingPopup: null,
      dragOffset: { x: 0, y: 0 },
      resizeStart: { x: 0, y: 0, width: 0, height: 0 },
    }
  },
  computed: {
    filteredPlayers() {
      return this.players.filter(player => {
        const matchesFirstName = this.search.first_name === '' || player.first_name.toLowerCase().includes(this.search.first_name.toLowerCase())
        const matchesLastName = this.search.last_name === '' || player.last_name.toLowerCase().includes(this.search.last_name.toLowerCase())
        const matchesPosition = this.search.position === '' || (player.position && player.position.toLowerCase().includes(this.search.position.toLowerCase()))
        const matchesTeam = this.search.team === '' || (player.team && player.team.toLowerCase().includes(this.search.team.toLowerCase()))
        return matchesFirstName && matchesLastName && matchesPosition && matchesTeam
      })
    }
  },

  methods: {
    formatDate(dateStr) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' }
      return new Date(dateStr).toLocaleDateString(undefined, options)
    },
    showPlayerDetails(player) {
      const popupId = Date.now(); // Unique ID for the popup
      this.playerPopups.push({
        id: popupId,
        player,
        top: 100,
        left: 100,
        width: 300,
        height: 200,
        zIndex: this.playerPopups.length + 1,
      });
    },
    closePopup(popupId) {
      this.playerPopups = this.playerPopups.filter((popup) => popup.id !== popupId);
    },
    bringToFront(popupId) {
      const popup = this.playerPopups.find((popup) => popup.id === popupId);
      if (popup) {
        popup.zIndex = Math.max(...this.playerPopups.map((p) => p.zIndex)) + 1;
      }
    },
    startDrag(event, popupId) {
      const popup = this.playerPopups.find((popup) => popup.id === popupId);
      if (popup) {
        this.draggingPopup = popup;
        this.dragOffset.x = event.clientX - popup.left;
        this.dragOffset.y = event.clientY - popup.top;
        document.addEventListener('mousemove', this.drag);
        document.addEventListener('mouseup', this.stopDrag);
      }
    },
    drag(event) {
      if (this.draggingPopup) {
        this.draggingPopup.top = event.clientY - this.dragOffset.y;
        this.draggingPopup.left = event.clientX - this.dragOffset.x;
      }
    },
    stopDrag() {
      this.draggingPopup = null;
      document.removeEventListener('mousemove', this.drag);
      document.removeEventListener('mouseup', this.stopDrag);
    },
    startResize(event, popupId) {
      const popup = this.playerPopups.find((popup) => popup.id === popupId);
      if (popup) {
        this.resizingPopup = popup;
        this.resizeStart.x = event.clientX;
        this.resizeStart.y = event.clientY;
        this.resizeStart.width = popup.width;
        this.resizeStart.height = popup.height;
        document.addEventListener('mousemove', this.resize);
        document.addEventListener('mouseup', this.stopResize);
      }
    },
    resize(event) {
      if (this.resizingPopup) {
        this.resizingPopup.width = this.resizeStart.width + (event.clientX - this.resizeStart.x);
        this.resizingPopup.height = this.resizeStart.height + (event.clientY - this.resizeStart.y);
      }
    },
    stopResize() {
      this.resizingPopup = null;
      document.removeEventListener('mousemove', this.resize);
      document.removeEventListener('mouseup', this.stopResize);
    },

    async createPlayer() {
      try {
        // Create the player
        const res = await axios.post('/api/create/player', {
          first_name: this.newPlayer.first_name,
          last_name: this.newPlayer.last_name,
          position: this.newPlayer.position,
          date_of_birth: this.newPlayer.date_of_birth
        })
        const newPlayerId = res.data.data.id

        // Add to team
        await axios.post('/api/create/team_membership', {
            team_id: this.newPlayer.team,
            player_id: newPlayerId,
            number_on_team: 0  // or let them input a number if needed
        })

        // Re-fetch or locally add
        this.players.push({
          id: newPlayerId,
          ...this.newPlayer,
          team: this.teams.find(t => t.id === this.newPlayer.team).name,
          number: 0,
          note: { content: '', id: null }
        })

        // Reset form
        this.newPlayer = {
          first_name: '',
          last_name: '',
          position: '',
          date_of_birth: '',
          team: ''
        }
        this.showNewPlayerForm = false
      } catch (error) {
        console.error("Failed to create player:", error)
      }
    }
  },

  async mounted() {
    const playersRes = await axios.get('/api/search/player', { params: { all: true } })
    const allPlayers = playersRes.data.data

    const teamSearchRes = await axios.get('/api/search/team', { params: { name: '' } })
    const allTeams = teamSearchRes.data.data
    this.teams = allTeams

    const enrichedPlayers = []

    for (const team of allTeams) {
      const teamDetailRes = await axios.get('/api/get/team', { params: { id: team.id } })
      const teamDetail = teamDetailRes.data.data

      for (const player of teamDetail.players) {
        
        const fullPlayer = allPlayers.find(p => p.id === player.id)
        if (fullPlayer) {
         
          fullPlayer.team = team.name
          fullPlayer.number = player.number_on_team
          enrichedPlayers.push(fullPlayer)
        }
      }
    }

    this.players = enrichedPlayers
  }
}
</script>

<style>

.player-popup {
  position: absolute;
  background-color: #004e42;
  color: white;
  border: 1px solid #01463c;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  z-index: 1000;
}

.popup-header {
  background-color: #006b5a;
  color: white;
  padding: 10px;
  cursor: move;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.popup-header .close-button {
  background-color: #b30000;
  color: white;
  border: none;
  border-radius: 3px;
  padding: 5px 10px;
  cursor: pointer;
}

.popup-header .close-button:hover {
  background-color: #d11a2a;
}

.popup-content {
  padding: 10px;
}

.popup-resizer {
  width: 10px;
  height: 10px;
  background-color: #ffcd00;
  position: absolute;
  bottom: 0;
  right: 0;
  cursor: se-resize;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Ensure it appears above other content */
}

/* Modal Content */
.modal-content {
  background-color: #004e42;
  padding: 20px;
  border-radius: 10px;
  width: 90%;
  max-width: 400px;
  color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.modal-content h2 {
  margin-bottom: 20px;
}

.modal-content input,
.modal-content select {
  width: 90%;
  max-width: 500px;
  padding: 10px;
  margin-bottom: 15px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

  .search-container {
    display: flex;
    flex-wrap: wrap; 
    gap: 20px; 
    margin-bottom: 20px; 
    align-items: center;
    justify-content: center;
    flex-direction: row;
  }

  .filter-input,
  .filter-select {
    padding: 5px;
    font-size: 1rem;
    border: 1px solid #ddd;
    border-radius: 5px;
  }

  .styled-button {
    padding: 10px 20px;
    font-size: 1rem;
    color: black;
    /* background-color: #fff; Match the theme */
    border: 1px solid #01463c;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
  }

  .styled-button:hover {
    background-color: #006b5a; /* Slightly lighter green on hover */
    transform: scale(1.05); /* Slight zoom effect */
  }

  .styled-button:active {
    background-color: #003d2f; /* Darker green when clicked */
    transform: scale(0.95); /* Slight shrink effect */
  }

  .player-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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
    min-width: 250px;
  }

  
  .player-divider {
    width: 100%;
    height: 1px; /* Thin horizontal line */
    background-color: #ffcd00; /* Yellow color */
    margin: 10px 0; /* Add spacing above and below the line */
  }

  .new-player-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 20px auto;
    max-width: 400px;
    background-color: #004e42;
    padding: 20px;
    border-radius: 5px;
    color: white;
  }
  .new-player-form input,
  .new-player-form select {
    padding: 5px;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
  }

  

</style>