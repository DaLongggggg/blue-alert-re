import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import GameBadge from './components/GameBadge.vue'
import GameBadges from './components/GameBadges.vue'
import MediaImage from './components/MediaImage.vue'
import MediaVideo from './components/MediaVideo.vue'
import MissionCard from './components/MissionCard.vue'
import UnitCard from './components/UnitCard.vue'
import MuseumExplorer from './components/MuseumExplorer.vue'
import UnitExplorer from './components/UnitExplorer.vue'
import MissionMeta from './components/MissionMeta.vue'
import MediaZoom from './components/MediaZoom.vue'
import CreditsList from './components/CreditsList.vue'
import NetworkMapGrid from './components/NetworkMapGrid.vue'
import UnitGallery from './components/UnitGallery.vue'
import HotkeysTable from './components/HotkeysTable.vue'
import WeaponTable from './components/WeaponTable.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('GameBadge', GameBadge)
    app.component('GameBadges', GameBadges)
    app.component('MediaImage', MediaImage)
    app.component('MediaVideo', MediaVideo)
    app.component('MissionCard', MissionCard)
    app.component('UnitCard', UnitCard)
    app.component('MuseumExplorer', MuseumExplorer)
    app.component('UnitExplorer', UnitExplorer)
    app.component('MissionMeta', MissionMeta)
    app.component('MediaZoom', MediaZoom)
    app.component('CreditsList', CreditsList)
    app.component('NetworkMapGrid', NetworkMapGrid)
    app.component('UnitGallery', UnitGallery)
    app.component('HotkeysTable', HotkeysTable)
    app.component('WeaponTable', WeaponTable)
  }
} satisfies Theme
