import { createRouter, createWebHistory } from 'vue-router'
import GamesView from '../views/games-view.vue'
import PlayersView from '../views/players-view.vue'
import TeamsView from '../views/teams-info-view.vue'
import PlayerInfoView from '../views/player-info-view.vue'

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
      path: '/team-info',
      name: 'team-info',
      component: TeamsView,
    },
    {
      path: '/player-info',
      name: 'player-info',
      component: PlayerInfoView,
    },
  ],
})

export default router
