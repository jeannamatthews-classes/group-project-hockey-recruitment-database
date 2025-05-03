import { createRouter, createWebHistory } from 'vue-router'
import GamesView from '../views/games-view.vue'
import PlayersView from '../views/players-view.vue'
import TeamsView from '../views/teams-view.vue'
import TeamsInfoView from '../views/teams-info-view.vue'
import PlayerInfoView from '../views/player-info-view.vue'
import PlayerEditView from '../views/player-edit-view.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'default',
      component: PlayersView, // Set PlayerView as the default route
    },
    {
      path: '/games',
      name: 'games',
      component: GamesView,
    },
    {
      path: '/players',
      name: 'players',
      component: PlayersView,
    },
    {
      path: '/player-info/:id',
      name: 'player-info',
      component: PlayerInfoView,
    },
    {
      path: '/player-edit/:id',
      name: 'player-edit',
      component: PlayerEditView,
    },  
    {
      path: '/teams',
      name: 'teams',
      component: TeamsView,
    },
    {
      path: '/team-info/:id',
      name: 'team-info',
      component: TeamsInfoView,
    },
  ],
})

export default router
