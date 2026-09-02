/* Hand-drawn SVG sigil icons for every race and class.
   Each icon is the inner content of an <svg viewBox="0 0 64 64">
   with fill="none" stroke="currentColor" - one cohesive line-icon set.
   Placeholder sigils are auto-generated; replace under each key. */

const ICONS = {

  /* ------------------------------- RACES ------------------------------ */
  dragonkin:
    `<path d="M20 46 C14 44 12 38 14 32 C16 26 22 24 30 24 C38 24 42 26 46 30 C50 34 50 40 44 44 C40 48 32 50 26 50 C22 50 19 48 20 46 Z"/>
          <path d="M30 24 C28 16 22 12 16 12"/>
          <path d="M20 46 L14 56 L24 50"/>
          <circle cx="30" cy="31" r="2"/>
          <path d="M46 30 L52 27 M46 33 L52 31"/>`,

  kitsune:
    `<path d="M20 26 L16 10 L30 16 M44 26 L48 10 L34 16"/>
          <path d="M16 26 C16 40 22 46 32 46 C42 46 48 40 48 26 C44 32 40 30 32 30 C24 30 20 32 16 26 Z"/>
          <path d="M36 16 C44 6 56 8 58 18"/>
          <path d="M42 24 C50 16 58 20 56 30"/>
          <path d="M30 12 C40 2 54 4 56 16"/>
          <circle cx="26" cy="33" r="2"/><circle cx="38" cy="33" r="2"/>`,

  titanborn:
    `<path d="M10 46 L28 14 L38 30 L46 20 L56 46 Z"/>
          <path d="M28 14 L24 22 L32 24 Z" opacity=".55"/>
          <path d="M46 20 L42 28 L50 30 Z" opacity=".55"/>
          <path d="M8 52 L58 52"/>
          <path d="M14 52 L12 46 M52 52 L54 44"/>`,

  drow:
    `<circle cx="32" cy="38" rx="9" ry="12"/>
          <circle cx="32" cy="22" r="4"/>
          <path d="M26 30 L16 14 M38 30 L48 14"/>
          <path d="M23 36 L10 26 M41 36 L54 26"/>
          <path d="M25 46 L16 56 M39 46 L48 56"/>
          <path d="M27 49 L20 58 M37 49 L44 58"/>`,

  celestial:
    `<circle cx="32" cy="18" r="6"/>
          <path d="M16 30 C6 24 6 12 16 10 C22 10 26 15 26 20 C26 26 22 28 16 30 Z"/>
          <path d="M48 30 C58 24 58 12 48 10 C42 10 38 15 38 20 C38 26 42 28 48 30 Z"/>
          <path d="M32 26 L22 50 L42 50 Z"/>
          <path d="M14 10 L18 6 M50 10 L46 6"/>`,

  abyssal:
    `<path d="M20 26 C16 12 24 2 30 10"/>
          <path d="M44 26 C48 12 40 2 34 10"/>
          <path d="M20 26 C20 42 25 48 32 48 C39 48 44 42 44 26 C40 31 36 33 32 32 C28 31 24 31 20 26 Z"/>
          <path d="M24 36 L28 33 M40 36 L36 33"/>`,

  naga:
    `<path d="M14 16 C14 40 20 54 32 54 C44 54 50 42 50 34 C50 26 44 22 38 24 C34 26 32 30 34 34 C36 38 42 38 43 34"/>
          <path d="M43 34 L54 26 M54 26 L58 22 M54 26 L60 30"/>
          <path d="M14 16 C10 16 8 20 10 24"/>`,

  djinn:
    `<path d="M20 40 C20 28 24 24 32 22 C40 20 44 26 42 32 C40 38 33 40 32 48 C31 54 40 54 44 54 Q24 56 20 40 Z"/>
          <path d="M44 54 L54 50 L50 45"/>
          <path d="M22 22 Q16 16 22 16"/>
          <path d="M44 22 C48 12 56 18 54 26"/>
          <path d="M54 18 C58 12 62 18 60 22"/>`,

  satyr:
    `<path d="M18 22 C14 12 22 6 28 12 M46 22 C50 12 42 6 36 12"/>
          <path d="M20 26 C20 40 26 46 32 46 C38 46 44 40 44 26 C38 30 34 30 32 30 C28 30 24 30 20 26 Z"/>
          <path d="M28 46 L26 53 M32 46 L32 54 M36 46 L38 53"/>
          <path d="M24 46 L18 52 M40 46 L46 52"/>`,

  treant:
    `<circle cx="24" cy="18" r="8"/><circle cx="40" cy="18" r="8"/><circle cx="32" cy="12" r="8"/>
          <path d="M30 24 L28 54 M34 24 L36 54"/>
          <path d="M20 32 L13 38 M44 32 L51 38"/>
          <circle cx="28" cy="34" r="2"/><circle cx="36" cy="34" r="2"/>
          <path d="M29 41 Q32 44 35 41"/>`,

  orc:
    `<path d="M24 16 C20 16 15 22 17 31 C19 40 26 45 32 45 C38 45 45 40 47 31 C49 22 44 16 40 16 Z"/>
          <path d="M25 36 L20 46 M39 36 L44 46"/>
          <circle cx="27" cy="27" r="2.4"/><circle cx="37" cy="27" r="2.4"/>
          <path d="M27 27 L24 25 M37 27 L40 25 M24 21 L28 16 M44 21 L40 16"/>`,

  dwarf:
    `<path d="M22 26 L42 26 C43 34 39 40 32 40 C25 40 21 34 22 26 Z"/>
          <circle cx="32" cy="32" r="3"/>
          <path d="M24 40 L20 52 L28 47 L32 53 L36 47 L44 52 L40 40 Z"/>`,

  undead:
    `<path d="M23 16 C17 16 15 22 16 29 L16 34 C20 38 24 40 32 40 C40 40 44 38 48 34 L48 29 C49 22 47 16 41 16 Z"/>
          <circle cx="26" cy="28" r="3"/><circle cx="38" cy="28" r="3"/>
          <path d="M29 32 L35 32"/>
          <path d="M30 36 L32 34 L34 36"/>
          <path d="M20 42 L22 46 M44 42 L42 46"/>`,

  human:
    `<circle cx="32" cy="17" r="5"/>
          <path d="M32 24 L32 40"/>
          <path d="M32 30 L20 40 M32 30 L44 40"/>
          <path d="M32 40 L24 54 M32 40 L40 54"/>`,

  vampire:
    `<path d="M32 24 C24 12 10 10 7 16 C13 20 16 27 14 33 C20 27 25 28 32 28 C39 28 44 27 50 33 C48 27 51 20 57 16 C54 10 40 12 32 24 Z"/>
          <path d="M27 28 L30 36 L27 31 Z M37 28 L34 36 L37 31 Z"/>
          <path d="M32 36 L32 42"/>`,

  elf:
    `<path d="M16 20 Q6 32 16 44"/>
          <path d="M16 20 L16 44"/>
          <path d="M16 32 L52 32"/>
          <path d="M44 28 L52 32 L44 36 L44 32 Z"/>
          <path d="M54 30 L58 28 M54 34 L58 36"/>`,

  werewolf:
    `<path d="M14 16 Q6 12 6 22 C12 18 14 20 14 26 Z"/>
          <path d="M22 12 Q16 8 17 18 C22 14 24 15 24 21 Z" opacity=".6"/>
          <path d="M48 16 C56 10 58 18 54 24 C50 20 48 24 48 28 Z" opacity=".6"/>
          <path d="M40 12 C48 6 50 16 46 22 C42 18 40 22 40 28 Z"/>`,

  dryad:
    `<circle cx="32" cy="16" r="4"/>
          <path d="M32 20 L32 38"/>
          <path d="M18 26 C10 22 10 14 18 12 C22 20 22 24 18 26 Z"/>
          <path d="M46 26 C54 22 54 14 46 12 C42 20 42 24 46 26 Z"/>
          <path d="M32 38 C24 46 40 46 32 38 Z"/>
          <path d="M32 10 L32 4 M29 7 L35 7"/>`,

  beastkin:
    `<path d="M24 22 L20 6 L32 14 M40 22 L44 6 L32 14"/>
          <path d="M15 25 C15 39 22 47 32 47 C42 47 49 39 49 25 C44 31 40 30 32 30 C24 30 20 31 15 25 Z"/>
          <path d="M15 33 L5 31 M15 37 L6 39 M49 33 L59 31 M49 37 L58 39"/>`,

  avian:
    `<path d="M21 22 C14 28 16 37 25 39 C33 41 41 37 44 31 C48 25 44 19 38 19 C36 13 25 13 21 22 Z"/>
          <path d="M26 24 C31 30 38 30 38 30"/>
          <path d="M44 27 L52 27 L44 31 Z"/>
          <path d="M21 36 L14 44 M21 36 L18 46"/>
          <circle cx="29" cy="26" r="1.4"/>`,

  fairy:
    `<path d="M18 30 C9 21 11 12 19 12 C25 12 26 20 22 27 M46 30 C55 21 53 12 45 12 C39 12 38 20 42 27"/>
          <circle cx="32" cy="40" r="3"/>
          <path d="M32 14 L32 18 M30 16 L34 16 M26 22 L30 20 M38 22 L34 20"/>`,

  brethren:
    `<path d="M32 48 C21 41 20 27 28 22 C31 36 37 37 39 25 C45 30 45 41 32 48 Z"/>
          <path d="M17 50 L47 50 M21 54 L43 54"/>`,

  tortle:
    `<path d="M16 34 C16 50 48 50 48 34 Z"/>
          <path d="M20 34 L20 40 M28 34 L27 42 M36 34 L37 42 M44 34 L44 40 M32 34 L32 42 M32 24 L32 30"/>
          <path d="M16 34 L9 32 L10 38 Z M48 34 L55 32 L54 38 Z"/>
          <path d="M22 44 L18 52 M42 44 L46 52"/>`,

  hafis:
    `<path d="M16 18 L16 36 C16 45 24 50 32 54 C40 50 48 45 48 36 L48 18 Z"/>
          <path d="M28 28 L32 35 L38 26 M30 34 L25 40 M34 40 L40 44"/>`,

  golemkin:
    `<rect x="20" y="14" width="24" height="26" rx="4"/>
          <path d="M20 24 H44 M26 14 V40 M38 14 V40"/>
          <circle cx="28" cy="30" r="2"/><circle cx="36" cy="30" r="2"/>
          <path d="M24 40 L22 52 M40 40 L42 52 M32 40 V48"/>`,

  frostborne:
    `<path d="M32 6 L42 22 L50 52 L32 40 L14 52 L22 22 Z"/>
          <path d="M32 14 L32 40 M22 34 L42 34 M26 45 L38 45"/>
          <path d="M32 40 L36 30 M32 40 L28 30"/>`,

  wraith:
    `<path d="M24 14 C14 14 12 24 12 32 L12 48 L18 42 L24 48 L30 42 L36 48 L42 42 L48 48 L52 32 C52 24 50 14 40 14 C36 19 28 19 24 14 Z"/>
          <circle cx="27" cy="28" r="2.2"/><circle cx="37" cy="28" r="2.2"/>
          <path d="M29 35 Q32 38 35 35"/>`,

  fire_elemental:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  water_elemental:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  earth_elemental:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  air_elemental:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  lightning_elemental:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  magma_lord:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  stormborn:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  tidal_dancer:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  glacial:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  volcanic:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  dust_wraith:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  mistwalker:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  ashborn:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  cinder_spark:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  tempest_lord:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  sky_sovereign:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  inferno_touched:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  void_essence:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  ember_knight:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  frost_kin:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  ember_soul:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  wolf_blooded:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  bear_folk:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  hawk_kin:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  serpent_blooded:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  spider_kin:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  raven_folk:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  fox_blooded:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  stag_folk:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  shark_kin:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  lion_folk:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  owlkin:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  raptor_kin:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  boar_folk:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  bat_folk:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  lupine_hunter:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  serpent_sages:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  lich:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  banshee:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  revenant:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  spectral: /* placeholder - replace with race sigil */
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
     <circle cx="32" cy="32" r="10"/>
     <circle cx="32" cy="32" r="3"/>`,

  shade:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  specter:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  poltergeist:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  ghost_kin:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  zombie_forged:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  seraph:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  archon:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  demigod:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  solar_angel:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  lunar_kin:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  starborn:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  cherub:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  aasimar:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  imp:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  cambion:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  pit_fiend:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  balor:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  tiefling:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  shadow_demon:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  nightmare:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  void_fiend:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  sprite:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  pixie:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  centaur:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  sylph:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  gnome:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  leshy:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  mushroom_folk:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  treant_sprout:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  faun:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  merfolk:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  sea_elf:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  kelpie:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  sahuagin:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  triton:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  deep_one:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  abyssal_serpent:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  pearl_mermaid:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  automaton:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  warforged:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  clockwork:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  crystal_golem:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  construct:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  soulforged:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  ogre:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  troll:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  jotun:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  cyclops:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  firbolg:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  goliath:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  half_giant:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  verdant_giant:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  monolith: /* placeholder - replace with race sigil */
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
     <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
     <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  astral:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  void_touched:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  ethereal:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  planar:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  chrono:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  rune_carved:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  soul_echo:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  dream_walker:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  aether_born:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  null_kin:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  sand_wraith:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  iron_bound:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  bloodkin: /* placeholder - replace with race sigil */
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
     <circle cx="32" cy="32" r="6"/>
     <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  storm_herald: /* placeholder - replace with race sigil */
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
     <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  crystal_shard:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  twilight_elf:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  dust_djinn:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  ironheart:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  rune_sorcerer:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  storm_spirit:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  thornweaver:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  ember_drake:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  storm_dragon:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  void_serpent:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  iron_drake:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  frost_dragon:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  sandstorm_beast:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  wild_kin:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  abyssal_kraken:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  crystal_nymph:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  mossling:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  shadow_drake:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  bone_colossus:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  ash_knight:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  lava_walker:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  ice_witch:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  plague_bearer:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  flamecaller:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  glacierborn:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  stonecaller:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  windrider:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  thunderlord:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  ashwalker:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  tidecaller:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  dustfiend:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  ember_sprite:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  frost_spirit:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  storm_wraith:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  earth_shaper:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  sky_dancer:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  shadowcaster:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  plague_doctor:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  void_weaver:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  crystal_mage:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  moon_weaver:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  sunCaller:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  starCaller:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  abyss_walker:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  soul_reaper:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  bone_weaver:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  sand_serpent:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  tundra_wolf:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  swamp_hag:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  sky_dragon:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  iron_golem:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  dark_elf:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  high_elf:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  wood_elf:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  sea_dwarf:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  mountain_giant:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  hill_giant:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  fog_phantom:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  dust_devil:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  magma_sprite:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  frost_fairy:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  shadow_fairy:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  star_fairy:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  plague_witch:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  warlock_v2:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  demon_hunter:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  vampire_hunter:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  dragon_slayer:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  undead_hunter:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  giant_slayer:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  troll_kin:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  orc_raider:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  elven_ranger:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  dwarven_smith:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  human_mage:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  undead_mage:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  celestial_warrior:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  abyssal_warrior:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  magma_golem:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  frost_golem:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  storm_golem:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  void_golem:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  shadow_elf:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  flame_elf:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  ice_elf:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  mountain_dwarf:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  hill_dwarf:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  deep_dwarf:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  necro_undead:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  war_undead:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  spirit_undead:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  wight:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  /* ------------------------------- CLASSES ----------------------------- */
  berserker:
    `<path d="M20 12 L40 52 M44 12 L24 52" opacity=".45"/>
          <path d="M24 14 C14 11 9 19 15 25 C20 22 24 18 24 14 Z"/>
          <path d="M40 50 C50 47 55 39 49 33 C44 36 40 42 40 50 Z"/>`,

  warrior:
    `<path d="M22 12 L42 12 L42 34 C42 44 37 51 32 55 C27 51 22 44 22 34 Z"/>
          <path d="M32 20 L32 40 M24 30 L40 30"/>
          <path d="M32 41 L32 49 M29 47 L32 53 L35 47"/>`,

  paladin:
    `<path d="M32 12 L32 52 M20 26 L44 26"/>
          <path d="M36 14 L40 10 M40 18 L44 14 M28 50 L24 54 M24 46 L20 50"/>`,

  death_knight:
    `<path d="M36 52 L52 14 M36 52 L46 20"/>
          <path d="M48 18 L52 14 M44 22 L48 26"/>
          <path d="M40 26 L42 22 M36 32 L38 28 Z"/>
          <circle cx="21" cy="32" r="6"/>
          <circle cx="18.6" cy="31" r="1.4"/><circle cx="23.4" cy="31" r="1.4"/>`,

  spellbreaker:
    `<path d="M18 34 C18 22 26 16 34 19 C42 22 46 31 42 39"/>
          <path d="M34 19 L30 22 M38 32 L42 28 L37 24"/>
          <path d="M42 39 L47 44 M42 39 L47 36 M44 33 L48 31"/>`,

  assassin:
    `<path d="M32 8 L40 32 L34 40 L26 30 Z"/>
          <path d="M24 34 L38 40"/>
          <path d="M30 44 L34 43 M31 48 L35 47"/>
          <path d="M36 34 L44 36 L38 32 Z"/>
          <path d="M46 44 L46 48"/><circle cx="46" cy="51" r="1.4"/>`,

  monk:
    `<circle cx="32" cy="30" r="7"/>
          <path d="M28 34 L34 34 M30 37 L34 37 M29 40 L33 40"/>
          <path d="M22 26 L14 24 M42 24 L50 22"/>
          <path d="M24 22 C18 12 10 14 10 22 C14 24 20 24 24 22 Z" opacity=".5"/>
          <path d="M40 22 C46 12 54 14 54 22 C50 24 44 24 40 22 Z" opacity=".5"/>`,

  barbarian:
    `<path d="M32 10 L32 54"/>
          <path d="M32 18 C21 13 13 17 13 25 C13 31 19 33 29 30 L32 18 Z"/>
          <path d="M32 14 L28 6 M32 14 L36 6"/>
          <path d="M29 44 L35 44 L32 50 Z"/>`,

  ranger:
    `<path d="M16 18 Q5 32 16 46"/>
          <path d="M17.5 19.5 L14.5 44.5"/>
          <path d="M16 32 L52 32"/>
          <path d="M44 28 L52 32 L44 36 Z"/>`,

  champion:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  duelist:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  marauder:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  gladiator:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  lancer:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  warmonger:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  reaper:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  juggernaut:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  blade_dancer:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  pit_fighter:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  sky_knight:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  alchemist:
    `<path d="M28 12 L36 12 M30 12 L32 20 M34 12 L32 20"/>
          <path d="M20 34 C18 46 22 54 32 54 C42 54 46 46 44 34 Z"/>
          <path d="M24 40 Q28 44 32 40 Q36 36 40 40"/>
          <circle cx="27" cy="47" r="1.3"/><circle cx="37" cy="47" r="1.3"/>`,

  mage:
    `<path d="M32 54 L32 18"/>
          <circle cx="32" cy="12" r="5"/>
          <path d="M30 12 L34 12 M32 10 L32 14"/>
          <path d="M22 32 A14 14 0 0 0 42 32" opacity=".6"/>
          <path d="M46 48 L44 45 M14 18 L16 22"/>`,

  warlock:
    `<path d="M14 32 Q32 16 50 32 Q32 48 14 32 Z"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 25 L32 39"/>
          <path d="M12 22 Q4 20 8 12 M52 22 Q60 20 56 12"/>`,

  cleric:
    `<path d="M20 22 L20 31 C20 37 44 37 44 31 L44 22 Z"/>
          <path d="M32 31 L32 40 M26 40 L38 40 M26 48 L38 48 M32 40 L32 48"/>
          <path d="M26 22 L18 16 M38 22 L46 16 M38 22 L30 16 M26 22 L34 16"/>`,

  enchanter:
    `<path d="M12 22 C20 18 27 19 32 25 C37 19 44 18 52 22 L52 44 C44 40 37 41 32 47 C27 41 20 40 12 44 Z"/>
          <path d="M32 25 L32 47"/>
          <path d="M40 14 L42 18 M38 16 L44 16"/>
          <path d="M50 10 L51 13 M49 11.5 L53 11.5"/>`,

  druid:
    `<path d="M24 26 C16 10 8 8 6 10 M24 26 C10 14 6 20 6 22 M40 26 C48 10 56 8 58 10 M40 26 C54 14 58 20 58 22" opacity=".85"/>
          <path d="M28 30 C26 36 38 36 36 30 C38 24 26 24 28 30 Z"/>
          <path d="M32 30 L32 44"/>`,

  shaman:
    `<path d="M24 10 H40 V26 H24 Z M24 26 H40 V42 H24 Z M28 10 L26 4 M36 10 L38 4"/>
          <path d="M26 18 H38 M26 34 H38"/>
          <circle cx="28" cy="15" r="1.2"/><circle cx="36" cy="15" r="1.2"/>
          <path d="M28 31 L30 35 L28 33 M36 31 L34 35 L36 33"/>
          <path d="M44 30 L40 37 L44 37 L40 44" opacity=".8"/>`,

  void_knight:
    `<path d="M32 12 L36 26 L52 24 L38 34 L44 50 L30 38 L14 42 L28 32 L18 12 Z" opacity=".35"/>
          <path d="M32 8 L32 52"/>
          <path d="M27 14 L37 14 M27 20 L37 20 M24 26 H40" opacity=".7"/>`,

  blacksmith:
    `<path d="M22 32 H42 L46 40 H18 Z M18 40 H46 V46 H18 Z"/>
          <path d="M22 32 L13 32 L16 36 L21 36"/>
          <path d="M40 14 L32 22 M34 18 L44 28"/>
          <circle cx="44" cy="28" r="1.5"/>`,

  marksman:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  hunter:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  sniper:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  falconer:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  ballistae:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  slinger:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  arbalist:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  sharpshooter:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  beastmaster:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  trapper:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  miner:
    `<path d="M20 52 L38 34"/>
          <path d="M32 40 A16 16 0 0 1 38 22 L48 25 A11 11 0 0 0 36 45 Z"/>
          <path d="M46 14 L46 20 M43 17 L49 17"/>`,

  farmer:
    `<path d="M24 54 L37 41"/>
          <path d="M32 46 L46 40 L40 33 Z"/>
          <path d="M46 16 L46 44"/>
          <path d="M44 22 Q40 20 38 24 M44 28 Q39 26 37 31 M44 34 Q40 32 38 36"/>
          <path d="M48 22 Q52 20 54 24 M48 28 Q53 26 55 31 M48 34 Q52 32 54 36"/>`,

  gunslinger:
    `<path d="M12 36 L24 30 L26 22"/>
          <path d="M30 12 Q46 12 48 26"/>
          <path d="M30 12 L48 26"/>
          <path d="M48 26 L60 21"/>
          <path d="M58 19 L60 21 L57 23"/>`,

  samurai:
    `<path d="M20 34 C16 30 18 24 24 24 C30 24 30 30 26 34" opacity=".45"/>
          <path d="M46 6 C38 15 30 27 28 42 M28 42 L36 42 L38 46"/>
          <path d="M28 44 L42 38"/>
          <path d="M30 50 L52 56"/>
          <path d="M34 40 L30 49"/>`,

  ninja:
    `<rect x="12" y="22" width="22" height="4" rx="2" transform="rotate(45 23 24)"/>
          <rect x="30" y="38" width="22" height="4" rx="2" transform="rotate(45 41 40)"/>
          <circle cx="32" cy="32" r="3"/>`,

  bard:
    `<circle cx="32" cy="38" r="9"/>
          <circle cx="32" cy="38" r="3" opacity=".6"/>
          <path d="M32 47 L32 54"/>
          <path d="M41 40 L54 32"/>
          <path d="M38 16 L38 28"/>
          <path d="M38 20 C44 21 46 25 44 29 C43 31 40 31 38 30"/>`,

  warden:
    `<path d="M23 10 L41 10 L41 32 C41 43 33 51 32 52 C31 51 23 43 23 32 Z"/>
          <path d="M41 28 Q50 26 51 18 Q43 22 41 28 Z"/>`,

  terraformer:
    `<path d="M26 10 L26 30"/>
          <path d="M18 30 H34 L36 38 L40 44 H14 L16 38 Z"/>
          <path d="M8 48 Q20 40 32 48 M30 52 Q16 46 8 54"/>
          <path d="M22 24 L16 18 M16 18 L20 17"/>`,

  spellblade:
    `<path d="M36 56 L48 18"/>
          <path d="M28 50 L42 40 M36 56 L30 48"/>
          <path d="M48 18 L54 12 M44 22 L50 16"/>
          <path d="M20 26 A8 8 0 0 1 24 14 M14 30 A13 13 0 0 1 20 12" opacity=".5"/>
          <path d="M11 22 L8 18 M9 28 L5 30"/>`,

  sorcerer:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  elementalist:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  conjurer:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  illusionist:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  necromancer:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  witch:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  battle_mage:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  pyromancer:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  cryomancer:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  storm_caller:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  geomancer:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  sage:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  apothecary:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  battle_medic:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  oracle:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  chanter:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  priest:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  spirit_walker:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  life_binder:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  confessor:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  herbalist:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  warden_of_woods:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  sentinel:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  bulwark:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  guardian:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  fortress:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  aegis:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  stone_warden:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  ironclad:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  phalanx:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  colossus:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  shadow:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  infiltrator:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  nightblade:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  whisper:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  cutthroat:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  phantom:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  renegade:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  deadeye:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  scoundrel:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  trickster:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  shadow_blade:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  beast_tamer:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  undead_commander:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  golemancer:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  banneret:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  warlord:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  commander:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  ritualist:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  binder:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  spellthief:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  blade_mage:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  runic_warrior:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  hexblade:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  arcane_archer:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  battle_cleric:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  spirit_knight:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  runepriest:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  mystic:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  adept:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  artificer:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  jeweler:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  tinker:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  skinner:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  lumberjack:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  mason:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  weaver:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  brewer:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  cartographer:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  runesmith:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  fate_weaver:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  void_walker:
    `<path d="M32 8 C38 18 44 24 44 36 C44 47 38 54 32 54 C26 54 20 47 20 36 C20 29 26 24 32 18 Z"/>
          <path d="M32 24 C30 32 26 36 26 41 C26 46 29 49 32 49 C35 49 38 46 38 41 C38 38 35 34 32 28 Z" opacity=".55"/>`,

  time_mage:
    `<path d="M32 6 L42 14 L46 28 L40 44 L32 58 L24 44 L18 28 L22 14 Z"/>
          <path d="M32 14 L32 50 M22 30 L42 30 M25 42 L39 42 M24 20 L40 20"/>
          <circle cx="32" cy="32" r="6" opacity=".6"/>`,

  dreamwalker:
    `<circle cx="32" cy="32" r="22"/>
          <path d="M32 18 L32 46 M18 32 L46 32 M24 24 L40 40 M24 40 L40 24"/>`,

  soul_binder:
    `<path d="M32 10 L52 52 L12 52 Z"/>
          <path d="M32 22 L42 46 L22 46 Z" opacity=".5"/>
          <path d="M32 44 L32 36"/>`,

  starweaver:
    `<path d="M46 20 L52 32 L46 44 L32 50 L18 44 L12 32 L18 20 L32 14 Z"/>
          <circle cx="32" cy="32" r="10"/>
          <circle cx="32" cy="32" r="3"/>`,

  chaos_mage:
    `<path d="M22 12 L42 12 L42 32 C42 44 36 51 32 55 C28 51 22 44 22 32 Z"/>
          <path d="M27 30 L32 38 L38 26"/>`,

  blood_mage:
    `<path d="M18 18 L46 46 M46 18 L18 46"/>
          <circle cx="32" cy="32" r="6"/>
          <path d="M32 22 L32 42 M22 32 L42 32"/>`,

  thaumaturge:
    `<path d="M32 10 L36 24 L50 24 L39 33 L43 47 L32 39 L21 47 L25 33 L14 24 L28 24 Z"/>
          <circle cx="32" cy="32" r="5" opacity=".7"/>`,

  /* fallback sigil */
  _default:
    `<path d="M32 8 L36 22 L50 26 L38 32 L42 46 L32 38 L22 46 L26 32 L14 26 L28 22 Z"/>
     <circle cx="32" cy="32" r="6"/>`,

  /* Hand-drawn icons (these render as custom SVG). Any key NOT here falls
     back to an auto-generated monogram letter glyph in app.js. */
  _custom: [
    "dragonkin","kitsune","titanborn","drow","celestial","abyssal","naga","djinn",
    "satyr","treant","dryad","avian","tortle","golemkin","frostborne","wraith",
    "dwarf","human","elf","orc","undead","vampire","werewolf","beastkin","fairy",
    "brethren","hafis",
    "warrior","barbarian","ranger","alchemist","enchanter","blacksmith","miner",
    "farmer","terraformer","berserker","paladin","death_knight","spellbreaker",
    "assassin","monk","mage","warlock","cleric","druid","shaman","void_knight",
    "gunslinger","samurai","ninja","bard","warden","spellblade"
  ],
};

window.ICONS = ICONS;
