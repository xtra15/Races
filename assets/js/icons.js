/* Hand-drawn SVG sigil icons for every race and class.
   Each icon is the inner content of an <svg viewBox="0 0 64 64">
   with fill="none" stroke="currentColor" — one cohesive line-icon set. */

const ICONS = {

  /* ------------------------------- RACES ------------------------------ */

  dragonkin: /* dragon head, open jaw, swept horn */
    `<path d="M20 46 C14 44 12 38 14 32 C16 26 22 24 30 24 C38 24 42 26 46 30 C50 34 50 40 44 44 C40 48 32 50 26 50 C22 50 19 48 20 46 Z"/>
     <path d="M30 24 C28 16 22 12 16 12"/>
     <path d="M20 46 L14 56 L24 50"/>
     <circle cx="30" cy="31" r="2"/>
     <path d="M46 30 L52 27 M46 33 L52 31"/>`,

  kitsune: /* fox head with a sweep of tails */
    `<path d="M20 26 L16 10 L30 16 M44 26 L48 10 L34 16"/>
     <path d="M16 26 C16 40 22 46 32 46 C42 46 48 40 48 26 C44 32 40 30 32 30 C24 30 20 32 16 26 Z"/>
     <path d="M36 16 C44 6 56 8 58 18"/>
     <path d="M42 24 C50 16 58 20 56 30"/>
     <path d="M30 12 C40 2 54 4 56 16"/>
     <circle cx="26" cy="33" r="2"/><circle cx="38" cy="33" r="2"/>`,

  titanborn: /* twin mountain peaks, giant scale */
    `<path d="M10 46 L28 14 L38 30 L46 20 L56 46 Z"/>
     <path d="M28 14 L24 22 L32 24 Z" opacity=".55"/>
     <path d="M46 20 L42 28 L50 30 Z" opacity=".55"/>
     <path d="M8 52 L58 52"/>
     <path d="M14 52 L12 46 M52 52 L54 44"/>`,

  drow: /* spider with blade-legs, dark web */
    `<circle cx="32" cy="38" rx="9" ry="12"/>
     <circle cx="32" cy="22" r="4"/>
     <path d="M26 30 L16 14 M38 30 L48 14"/>
     <path d="M23 36 L10 26 M41 36 L54 26"/>
     <path d="M25 46 L16 56 M39 46 L48 56"/>
     <path d="M27 49 L20 58 M37 49 L44 58"/>`,

  celestial: /* halo, wings, mantle */
    `<circle cx="32" cy="18" r="6"/>
     <path d="M16 30 C6 24 6 12 16 10 C22 10 26 15 26 20 C26 26 22 28 16 30 Z"/>
     <path d="M48 30 C58 24 58 12 48 10 C42 10 38 15 38 20 C38 26 42 28 48 30 Z"/>
     <path d="M32 26 L22 50 L42 50 Z"/>
     <path d="M14 10 L18 6 M50 10 L46 6"/>`,

  abyssal: /* horned demon head, slanted eyes */
    `<path d="M20 26 C16 12 24 2 30 10"/>
     <path d="M44 26 C48 12 40 2 34 10"/>
     <path d="M20 26 C20 42 25 48 32 48 C39 48 44 42 44 26 C40 31 36 33 32 32 C28 31 24 31 20 26 Z"/>
     <path d="M24 36 L28 33 M40 36 L36 33"/>`,

  naga: /* coiled serpent with forked tongue */
    `<path d="M14 16 C14 40 20 54 32 54 C44 54 50 42 50 34 C50 26 44 22 38 24 C34 26 32 30 34 34 C36 38 42 38 43 34"/>
     <path d="M43 34 L54 26 M54 26 L58 22 M54 26 L60 30"/>
     <path d="M14 16 C10 16 8 20 10 24"/>`,

  djinn: /* genie lamp with rising smoke */
    `<path d="M20 40 C20 28 24 24 32 22 C40 20 44 26 42 32 C40 38 33 40 32 48 C31 54 40 54 44 54 Q24 56 20 40 Z"/>
     <path d="M44 54 L54 50 L50 45"/>
     <path d="M22 22 Q16 16 22 16"/>
     <path d="M44 22 C48 12 56 18 54 26"/>
     <path d="M54 18 C58 12 62 18 60 22"/>`,

  satyr: /* goat horns, beard, muzzle */
    `<path d="M18 22 C14 12 22 6 28 12 M46 22 C50 12 42 6 36 12"/>
     <path d="M20 26 C20 40 26 46 32 46 C38 46 44 40 44 26 C38 30 34 30 32 30 C28 30 24 30 20 26 Z"/>
     <path d="M28 46 L26 53 M32 46 L32 54 M36 46 L38 53"/>
     <path d="M24 46 L18 52 M40 46 L46 52"/>`,

  treant: /* crowned tree with a face */
    `<circle cx="24" cy="18" r="8"/><circle cx="40" cy="18" r="8"/><circle cx="32" cy="12" r="8"/>
     <path d="M30 24 L28 54 M34 24 L36 54"/>
     <path d="M20 32 L13 38 M44 32 L51 38"/>
     <circle cx="28" cy="34" r="2"/><circle cx="36" cy="34" r="2"/>
     <path d="M29 41 Q32 44 35 41"/>`,

  dryad: /* leaf-spirit with petal wings */
    `<circle cx="32" cy="16" r="4"/>
     <path d="M32 20 L32 38"/>
     <path d="M18 26 C10 22 10 14 18 12 C22 20 22 24 18 26 Z"/>
     <path d="M46 26 C54 22 54 14 46 12 C42 20 42 24 46 26 Z"/>
     <path d="M32 38 C24 46 40 46 32 38 Z"/>
     <path d="M32 10 L32 4 M29 7 L35 7"/>`,

  avian: /* bird in flight */
    `<path d="M21 22 C14 28 16 37 25 39 C33 41 41 37 44 31 C48 25 44 19 38 19 C36 13 25 13 21 22 Z"/>
     <path d="M26 24 C31 30 38 30 38 30"/>
     <path d="M44 27 L52 27 L44 31 Z"/>
     <path d="M21 36 L14 44 M21 36 L18 46"/>
     <circle cx="29" cy="26" r="1.4"/>`,

  tortle: /* turtle shell dome with plates */
    `<path d="M16 34 C16 50 48 50 48 34 Z"/>
     <path d="M20 34 L20 40 M28 34 L27 42 M36 34 L37 42 M44 34 L44 40 M32 34 L32 42 M32 24 L32 30"/>
     <path d="M16 34 L9 32 L10 38 Z M48 34 L55 32 L54 38 Z"/>
     <path d="M22 44 L18 52 M42 44 L46 52"/>`,

  golemkin: /* stone construct, riveted */
    `<rect x="20" y="14" width="24" height="26" rx="4"/>
     <path d="M20 24 H44 M26 14 V40 M38 14 V40"/>
     <circle cx="28" cy="30" r="2"/><circle cx="36" cy="30" r="2"/>
     <path d="M24 40 L22 52 M40 40 L42 52 M32 40 V48"/>`,

  frostborne: /* ice crystal shard */
    `<path d="M32 6 L42 22 L50 52 L32 40 L14 52 L22 22 Z"/>
     <path d="M32 14 L32 40 M22 34 L42 34 M26 45 L38 45"/>
     <path d="M32 40 L36 30 M32 40 L28 30"/>`,

  wraith: /* ghost with wispy hem */
    `<path d="M24 14 C14 14 12 24 12 32 L12 48 L18 42 L24 48 L30 42 L36 48 L42 42 L48 48 L52 32 C52 24 50 14 40 14 C36 19 28 19 24 14 Z"/>
     <circle cx="27" cy="28" r="2.2"/><circle cx="37" cy="28" r="2.2"/>
     <path d="M29 35 Q32 38 35 35"/>`,

  dwarf: /* bearded helmet with gem */
    `<path d="M22 26 L42 26 C43 34 39 40 32 40 C25 40 21 34 22 26 Z"/>
     <circle cx="32" cy="32" r="3"/>
     <path d="M24 40 L20 52 L28 47 L32 53 L36 47 L44 52 L40 40 Z"/>`,

  human: /* balanced figure, open stance */
    `<circle cx="32" cy="17" r="5"/>
     <path d="M32 24 L32 40"/>
     <path d="M32 30 L20 40 M32 30 L44 40"/>
     <path d="M32 40 L24 54 M32 40 L40 54"/>`,

  elf: /* archer's bow with arrow */
    `<path d="M16 20 Q6 32 16 44"/>
     <path d="M16 20 L16 44"/>
     <path d="M16 32 L52 32"/>
     <path d="M44 28 L52 32 L44 36 L44 32 Z"/>
     <path d="M54 30 L58 28 M54 34 L58 36"/>`,

  orc: /* tusked brute face */
    `<path d="M24 16 C20 16 15 22 17 31 C19 40 26 45 32 45 C38 45 45 40 47 31 C49 22 44 16 40 16 Z"/>
     <path d="M25 36 L20 46 M39 36 L44 46"/>
     <circle cx="27" cy="27" r="2.4"/><circle cx="37" cy="27" r="2.4"/>
     <path d="M27 27 L24 25 M37 27 L40 25 M24 21 L28 16 M44 21 L40 16"/>`,

  undead: /* skull */
    `<path d="M23 16 C17 16 15 22 16 29 L16 34 C20 38 24 40 32 40 C40 40 44 38 48 34 L48 29 C49 22 47 16 41 16 Z"/>
     <circle cx="26" cy="28" r="3"/><circle cx="38" cy="28" r="3"/>
     <path d="M29 32 L35 32"/>
     <path d="M30 36 L32 34 L34 36"/>
     <path d="M20 42 L22 46 M44 42 L42 46"/>`,

  vampire: /* bat with fanged base */
    `<path d="M32 24 C24 12 10 10 7 16 C13 20 16 27 14 33 C20 27 25 28 32 28 C39 28 44 27 50 33 C48 27 51 20 57 16 C54 10 40 12 32 24 Z"/>
     <path d="M27 28 L30 36 L27 31 Z M37 28 L34 36 L37 31 Z"/>
     <path d="M32 36 L32 42"/>`,

  werewolf: /* claws raking the moon */
    `<path d="M14 16 Q6 12 6 22 C12 18 14 20 14 26 Z"/>
     <path d="M22 12 Q16 8 17 18 C22 14 24 15 24 21 Z" opacity=".6"/>
     <path d="M48 16 C56 10 58 18 54 24 C50 20 48 24 48 28 Z" opacity=".6"/>
     <path d="M40 12 C48 6 50 16 46 22 C42 18 40 22 40 28 Z"/>`,

  beastkin: /* cat face, whiskers */
    `<path d="M24 22 L20 6 L32 14 M40 22 L44 6 L32 14"/>
     <path d="M15 25 C15 39 22 47 32 47 C42 47 49 39 49 25 C44 31 40 30 32 30 C24 30 20 31 15 25 Z"/>
     <path d="M15 33 L5 31 M15 37 L6 39 M49 33 L59 31 M49 37 L58 39"/>`,

  fairy: /* two wings, a spark */
    `<path d="M18 30 C9 21 11 12 19 12 C25 12 26 20 22 27 M46 30 C55 21 53 12 45 12 C39 12 38 20 42 27"/>
     <circle cx="32" cy="40" r="3"/>
     <path d="M32 14 L32 18 M30 16 L34 16 M26 22 L30 20 M38 22 L34 20"/>`,

  brethren: /* campfire of the clan */
    `<path d="M32 48 C21 41 20 27 28 22 C31 36 37 37 39 25 C45 30 45 41 32 48 Z"/>
     <path d="M17 50 L47 50 M21 54 L43 54"/>`,

  hafis: /* shattered shield */
    `<path d="M16 18 L16 36 C16 45 24 50 32 54 C40 50 48 45 48 36 L48 18 Z"/>
     <path d="M28 28 L32 35 L38 26 M30 34 L25 40 M34 40 L40 44"/>`,

  /* ------------------------------- CLASSES ----------------------------- */

  warrior: /* shield with blade */
    `<path d="M22 12 L42 12 L42 34 C42 44 37 51 32 55 C27 51 22 44 22 34 Z"/>
     <path d="M32 20 L32 40 M24 30 L40 30"/>
     <path d="M32 41 L32 49 M29 47 L32 53 L35 47"/>`,

  barbarian: /* great axe */
    `<path d="M32 10 L32 54"/>
     <path d="M32 18 C21 13 13 17 13 25 C13 31 19 33 29 30 L32 18 Z"/>
     <path d="M32 14 L28 6 M32 14 L36 6"/>
     <path d="M29 44 L35 44 L32 50 Z"/>`,

  ranger: /* drawn bow and nocked arrow */
    `<path d="M16 18 Q5 32 16 46"/>
     <path d="M17.5 19.5 L14.5 44.5"/>
     <path d="M16 32 L52 32"/>
     <path d="M44 28 L52 32 L44 36 Z"/>`,

  berserker: /* crossed twin axes */
    `<path d="M20 12 L40 52 M44 12 L24 52" opacity=".45"/>
     <path d="M24 14 C14 11 9 19 15 25 C20 22 24 18 24 14 Z"/>
     <path d="M40 50 C50 47 55 39 49 33 C44 36 40 42 40 50 Z"/>`,

  paladin: /* radiant cross */
    `<path d="M32 12 L32 52 M20 26 L44 26"/>
     <path d="M36 14 L40 10 M40 18 L44 14 M28 50 L24 54 M24 46 L20 50"/>`,

  death_knight: /* rune blade with a skull */
    `<path d="M36 52 L52 14 M36 52 L46 20"/>
     <path d="M48 18 L52 14 M44 22 L48 26"/>
     <path d="M40 26 L42 22 M36 32 L38 28 Z"/>
     <circle cx="21" cy="32" r="6"/>
     <circle cx="18.6" cy="31" r="1.4"/><circle cx="23.4" cy="31" r="1.4"/>`,

  spellbreaker: /* broken ward circle and rift */
    `<path d="M18 34 C18 22 26 16 34 19 C42 22 46 31 42 39"/>
     <path d="M34 19 L30 22 M38 32 L42 28 L37 24"/>
     <path d="M42 39 L47 44 M42 39 L47 36 M44 33 L48 31"/>`,

  assassin: /* dagger with a drop */
    `<path d="M32 8 L40 32 L34 40 L26 30 Z"/>
     <path d="M24 34 L38 40"/>
     <path d="M30 44 L34 43 M31 48 L35 47"/>
     <path d="M36 34 L44 36 L38 32 Z"/>
     <path d="M46 44 L46 48"/><circle cx="46" cy="51" r="1.4"/>`,

  monk: /* fist with circling chi */
    `<circle cx="32" cy="30" r="7"/>
     <path d="M28 34 L34 34 M30 37 L34 37 M29 40 L33 40"/>
     <path d="M22 26 L14 24 M42 24 L50 22"/>
     <path d="M24 22 C18 12 10 14 10 22 C14 24 20 24 24 22 Z" opacity=".5"/>
     <path d="M40 22 C46 12 54 14 54 22 C50 24 44 24 40 22 Z" opacity=".5"/>`,

  alchemist: /* bubbling flask */
    `<path d="M28 12 L36 12 M30 12 L32 20 M34 12 L32 20"/>
     <path d="M20 34 C18 46 22 54 32 54 C42 54 46 46 44 34 Z"/>
     <path d="M24 40 Q28 44 32 40 Q36 36 40 40"/>
     <circle cx="27" cy="47" r="1.3"/><circle cx="37" cy="47" r="1.3"/>`,

  mage: /* staff with an orb and arc */
    `<path d="M32 54 L32 18"/>
     <circle cx="32" cy="12" r="5"/>
     <path d="M30 12 L34 12 M32 10 L32 14"/>
     <path d="M22 32 A14 14 0 0 0 42 32" opacity=".6"/>
     <path d="M46 48 L44 45 M14 18 L16 22"/>`,

  warlock: /* seer's eye in a wisp */
    `<path d="M14 32 Q32 16 50 32 Q32 48 14 32 Z"/>
     <circle cx="32" cy="32" r="6"/>
     <path d="M32 25 L32 39"/>
     <path d="M12 22 Q4 20 8 12 M52 22 Q60 20 56 12"/>`,

  cleric: /* chalice with holy light */
    `<path d="M20 22 L20 31 C20 37 44 37 44 31 L44 22 Z"/>
     <path d="M32 31 L32 40 M26 40 L38 40 M26 48 L38 48 M32 40 L32 48"/>
     <path d="M26 22 L18 16 M38 22 L46 16 M38 22 L30 16 M26 22 L34 16"/>`,

  enchanter: /* open tome with a spark */
    `<path d="M12 22 C20 18 27 19 32 25 C37 19 44 18 52 22 L52 44 C44 40 37 41 32 47 C27 41 20 40 12 44 Z"/>
     <path d="M32 25 L32 47"/>
     <path d="M40 14 L42 18 M38 16 L44 16"/>
     <path d="M50 10 L51 13 M49 11.5 L53 11.5"/>`,

  druid: /* antlered leaf */
    `<path d="M24 26 C16 10 8 8 6 10 M24 26 C10 14 6 20 6 22 M40 26 C48 10 56 8 58 10 M40 26 C54 14 58 20 58 22" opacity=".85"/>
     <path d="M28 30 C26 36 38 36 36 30 C38 24 26 24 28 30 Z"/>
     <path d="M32 30 L32 44"/>`,

  shaman: /* totem pole with a storm mark */
    `<path d="M24 10 H40 V26 H24 Z M24 26 H40 V42 H24 Z M28 10 L26 4 M36 10 L38 4"/>
     <path d="M26 18 H38 M26 34 H38"/>
     <circle cx="28" cy="15" r="1.2"/><circle cx="36" cy="15" r="1.2"/>
     <path d="M28 31 L30 35 L28 33 M36 31 L34 35 L36 33"/>
     <path d="M44 30 L40 37 L44 37 L40 44" opacity=".8"/>`,

  void_knight: /* blade rising from a portal */
    `<path d="M32 12 L36 26 L52 24 L38 34 L44 50 L30 38 L14 42 L28 32 L18 12 Z" opacity=".35"/>
     <path d="M32 8 L32 52"/>
     <path d="M27 14 L37 14 M27 20 L37 20 M24 26 H40" opacity=".7"/>`,

  blacksmith: /* anvil and hammer */
    `<path d="M22 32 H42 L46 40 H18 Z M18 40 H46 V46 H18 Z"/>
     <path d="M22 32 L13 32 L16 36 L21 36"/>
     <path d="M40 14 L32 22 M34 18 L44 28"/>
     <circle cx="44" cy="28" r="1.5"/>`,

  miner: /* pick with a nugget */
    `<path d="M20 52 L38 34"/>
     <path d="M32 40 A16 16 0 0 1 38 22 L48 25 A11 11 0 0 0 36 45 Z"/>
     <path d="M46 14 L46 20 M43 17 L49 17"/>`,

  farmer: /* hoe and wheat sheaf */
    `<path d="M24 54 L37 41"/>
     <path d="M32 46 L46 40 L40 33 Z"/>
     <path d="M46 16 L46 44"/>
     <path d="M44 22 Q40 20 38 24 M44 28 Q39 26 37 31 M44 34 Q40 32 38 36"/>
     <path d="M48 22 Q52 20 54 24 M48 28 Q53 26 55 31 M48 34 Q52 32 54 36"/>`,

  gunslinger: /* crossbow, drawn */
    `<path d="M12 36 L24 30 L26 22"/>
     <path d="M30 12 Q46 12 48 26"/>
     <path d="M30 12 L48 26"/>
     <path d="M48 26 L60 21"/>
     <path d="M58 19 L60 21 L57 23"/>`,

  samurai: /* katana, enso circle */
    `<path d="M20 34 C16 30 18 24 24 24 C30 24 30 30 26 34" opacity=".45"/>
     <path d="M46 6 C38 15 30 27 28 42 M28 42 L36 42 L38 46"/>
     <path d="M28 44 L42 38"/>
     <path d="M30 50 L52 56"/>
     <path d="M34 40 L30 49"/>`,

  ninja: /* four-point shuriken */
    `<rect x="12" y="22" width="22" height="4" rx="2" transform="rotate(45 23 24)"/>
     <rect x="30" y="38" width="22" height="4" rx="2" transform="rotate(45 41 40)"/>
     <circle cx="32" cy="32" r="3"/>`,

  bard: /* lute and a note */
    `<circle cx="32" cy="38" r="9"/>
     <circle cx="32" cy="38" r="3" opacity=".6"/>
     <path d="M32 47 L32 54"/>
     <path d="M41 40 L54 32"/>
     <path d="M38 16 L38 28"/>
     <path d="M38 20 C44 21 46 25 44 29 C43 31 40 31 38 30"/>`,

  warden: /* shield with a leaf */
    `<path d="M23 10 L41 10 L41 32 C41 43 33 51 32 52 C31 51 23 43 23 32 Z"/>
     <path d="M41 28 Q50 26 51 18 Q43 22 41 28 Z"/>`,

  terraformer: /* shovel and rolling land */
    `<path d="M26 10 L26 30"/>
     <path d="M18 30 H34 L36 38 L40 44 H14 L16 38 Z"/>
     <path d="M8 48 Q20 40 32 48 M30 52 Q16 46 8 54"/>
     <path d="M22 24 L16 18 M16 18 L20 17"/>`,

  spellblade: /* blade sheathed in magic */
    `<path d="M36 56 L48 18"/>
     <path d="M28 50 L42 40 M36 56 L30 48"/>
     <path d="M48 18 L54 12 M44 22 L50 16"/>
     <path d="M20 26 A8 8 0 0 1 24 14 M14 30 A13 13 0 0 1 20 12" opacity=".5"/>
     <path d="M11 22 L8 18 M9 28 L5 30"/>`,

  /* fallback sigil */
  _default:
    `<path d="M32 8 L36 22 L50 26 L38 32 L42 46 L32 38 L22 46 L26 32 L14 26 L28 22 Z"/>
     <circle cx="32" cy="32" r="6"/>`,
};

window.ICONS = ICONS;