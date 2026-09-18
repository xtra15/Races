# Race Save Slots Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `/raceslot` GUI system — a single listener-drive chest UI where each player can save their current race into one of 5 slots, replace a filled slot, or load a saved slot back as their active race (cooldown-gated), stored per-player in `playerdata.yml`.

**Architecture:** `PlayerDataManager` gains the 5 slot keys + a load-cooldown timestamp. One persisted `RaceSlotGui` listener owns all three screens (Main 5-slot row / Sub-menu / Confirm) and dispatches clicks off a per-player `Mode` state. Loading applies the race in-process via `AssignmentManager.assign` (buffs + stored race), marks the player claimed, and stamps the cooldown. Version bumps to 1.3.0.

**Tech Stack:** Java 21, Paper API 1.21.1, Maven, JUnit 5 (jupiter), Bukkit Inventory API.

## Global Constraints

- Working directory for all builds: `D:\e\Projects\ValhallaRaces\RandomRace`
- Java source is comment-free (project convention). Mini YAML comments in `config.yml` are OK (existing style).
- Version bump to **1.3.0** in BOTH `pom.xml` (currently 1.2.0) and `src/main/resources/plugin.yml` (currently 1.2.0).
- No git commits during implementation — the user commits/pushes when they choose. Do not stage or commit.
- Do not touch `target/` (git-ignored) or anything outside `D:\e\Projects\ValhallaRaces\RandomRace\` and the spec/plan docs.
- Chest inventory titles truncate at 32 chars — long prompts go in item lore, titles stay short.
- `mvn` commands run from `D:\e\Projects\ValhallaRaces\RandomRace`.

---

### Task 1: `PlayerDataManager` — 5 race slots + load cooldown storage

Adds the stored values the GUI reads/writes.

**Files:**
- Modify: `src/main/java/com/yourname/randomrace/managers/PlayerDataManager.java`
- Test: `src/test/java/com/yourname/randomrace/managers/PlayerDataManagerTest.java`

**Interfaces:**
- Consumes: existing `save()`, `data` (YamlConfiguration), `File` constructor.
- Produces (used by Tasks 2–3):
  - `String getRaceSlot(UUID, int)` — null when empty
  - `void setRaceSlot(UUID, int, String)` — null clears
  - `java.util.Map<Integer,String> getRaceSlots(UUID)`
  - `long getLoadCooldown(UUID)` — 0 means not cooling down
  - `void setLoadCooldown(UUID, long)` — epoch millis

- [ ] **Step 1: Write the failing tests**

Append to `src/test/java/com/yourname/randomrace/managers/PlayerDataManagerTest.java`:

```java
    @Test
    void raceSlotsDefaultEmpty() {
        PlayerDataManager m = manager();
        UUID id = UUID.randomUUID();
        assertNull(m.getRaceSlot(id, 1));
        assertTrue(m.getRaceSlots(id).isEmpty());
    }

    @Test
    void setRaceSlotPersists() {
        PlayerDataManager m = manager();
        UUID id = UUID.randomUUID();
        m.setRaceSlot(id, 3, "dragonkin");
        assertEquals("dragonkin", m.getRaceSlot(id, 3));
        assertEquals("dragonkin", m.getRaceSlots(id).get(3));
    }

    @Test
    void clearRaceSlotRemovesIt() {
        PlayerDataManager m = manager();
        UUID id = UUID.randomUUID();
        m.setRaceSlot(id, 2, "elf");
        m.setRaceSlot(id, 2, null);
        assertNull(m.getRaceSlot(id, 2));
        assertTrue(m.getRaceSlots(id).isEmpty());
    }

    @Test
    void loadCooldownDefaultZero() {
        PlayerDataManager m = manager();
        UUID id = UUID.randomUUID();
        assertEquals(0L, m.getLoadCooldown(id));
    }

    @Test
    void setLoadCooldownPersists() {
        PlayerDataManager m = manager();
        UUID id = UUID.randomUUID();
        m.setLoadCooldown(id, 123456789L);
        assertEquals(123456789L, m.getLoadCooldown(id));
    }
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `mvn -q test -Dtest=PlayerDataManagerTest`
Expected: FAIL — `getRaceSlot`, `setRaceSlot`, `getRaceSlots`, `getLoadCooldown`, `setLoadCooldown` do not exist.

- [ ] **Step 3: Implement**

Add this import to `PlayerDataManager.java`:

```java
import org.bukkit.configuration.ConfigurationSection;
```

Add these methods after `markJoined` / before `migrateByName` (or anywhere after the `setClassSlots` block):

```java
    public String getRaceSlot(UUID uuid, int slot) {
        return data.getString(uuid + ".raceslots." + slot);
    }

    public void setRaceSlot(UUID uuid, int slot, String raceKey) {
        data.set(uuid + ".raceslots." + slot, raceKey);
        save();
    }

    public java.util.Map<Integer, String> getRaceSlots(UUID uuid) {
        java.util.Map<Integer, String> map = new java.util.LinkedHashMap<>();
        ConfigurationSection section = data.getConfigurationSection(uuid + ".raceslots");
        if (section != null) {
            for (String key : section.getKeys(false)) {
                try {
                    map.put(Integer.parseInt(key), section.getString(key));
                } catch (NumberFormatException ignored) {
                }
            }
        }
        return map;
    }

    public long getLoadCooldown(UUID uuid) {
        return data.getLong(uuid + ".race-slot-cooldown", 0L);
    }

    public void setLoadCooldown(UUID uuid, long endEpochMillis) {
        data.set(uuid + ".race-slot-cooldown", endEpochMillis);
        save();
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `mvn -q test -Dtest=PlayerDataManagerTest`
Expected: PASS (all existing + 5 new tests green).

- [ ] **Step 5: Verify full tree compiles**

Run: `mvn -q compile`
Expected: BUILD SUCCESS.

---

### Task 2: `RaceSlotGui` — three screens + click logic + cooldown helper

The whole UI: Main (5 slots in middle row), Sub-menu (save-new / load), Confirm (red/green + center item). One persisted listener with per-player state.

**Files:**
- Create: `src/main/java/com/yourname/randomrace/gui/RaceSlotGui.java`
- Test: `src/test/java/com/yourname/randomrace/gui/RaceSlotGuiTest.java`

**Interfaces:**
- Consumes: Task 1 `PlayerDataManager` slot/cooldown methods; existing `AssignmentManager.assign(Player, Race)`, `RaceManager.getRace(Player)` / `getRegisteredRaces()`, `RacePoolManager.materialFor(Race)`, `MessageUtil.color(String)`, config key `race-slot-cooldown-seconds`.
- Produces (used by Task 3):
  - `void openMain(Player)`
  - `static long secondsRemaining(long endEpochMillis, long nowMillis)` — ceiling seconds

- [ ] **Step 1: Write the failing cooldown-helper test**

Create `src/test/java/com/yourname/randomrace/gui/RaceSlotGuiTest.java`:

```java
package com.yourname.randomrace.gui;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class RaceSlotGuiTest {

    @Test
    void remainingSecondsIsCeiling() {
        assertEquals(3L, RaceSlotGui.secondsRemaining(5000L, 2000L));
        assertEquals(1L, RaceSlotGui.secondsRemaining(5000L, 4999L));
        assertEquals(0L, RaceSlotGui.secondsRemaining(5000L, 5000L));
        assertEquals(0L, RaceSlotGui.secondsRemaining(5000L, 6000L));
    }
}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `mvn -q test -Dtest=RaceSlotGuiTest`
Expected: FAIL — `RaceSlotGui` does not exist.

- [ ] **Step 3: Implement RaceSlotGui**

Create `src/main/java/com/yourname/randomrace/gui/RaceSlotGui.java`:

```java
package com.yourname.randomrace.gui;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.managers.AssignmentManager;
import com.yourname.randomrace.managers.PlayerDataManager;
import com.yourname.randomrace.utils.MessageUtil;
import me.athlaeos.valhallaraces.Race;
import me.athlaeos.valhallaraces.RaceManager;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryCloseEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.ItemMeta;

import java.util.HashMap;
import java.util.Map;

public class RaceSlotGui implements Listener {
    private static final int[] MAIN_POSITIONS = {9, 11, 13, 15, 17};
    private static final int CONFIRM_RED = 11;
    private static final int CONFIRM_CENTER = 13;
    private static final int CONFIRM_GREEN = 15;
    private static final int SUBMENU_SAVE = 11;
    private static final int SUBMENU_LOAD = 15;

    private enum Mode { MAIN, SUBMENU, SAVE_CONFIRM, REPLACE_CONFIRM, LOAD_CONFIRM }

    private static final class State {
        final Mode mode;
        final int slot;

        State(Mode mode, int slot) {
            this.mode = mode;
            this.slot = slot;
        }
    }

    private final RandomRacePlugin plugin;
    private final AssignmentManager assignmentManager;
    private final Map<Player, State> states = new HashMap<>();

    public RaceSlotGui(RandomRacePlugin plugin) {
        this.plugin = plugin;
        this.assignmentManager = new AssignmentManager(plugin);
    }

    public void openMain(Player p) {
        Inventory inv = plugin.getServer().createInventory(null, 27, MessageUtil.color("&8Race Slots"));
        fillBackground(inv);
        String current = currentRaceName(p);
        inv.setItem(4, named(Material.BOOK, "&eCurrent race: &f" + (current == null ? "&7None" : current)));
        PlayerDataManager pdm = plugin.getPlayerDataManager();
        for (int i = 0; i < MAIN_POSITIONS.length; i++) {
            int slot = i + 1;
            String key = pdm.getRaceSlot(p.getUniqueId(), slot);
            if (key == null) {
                inv.setItem(MAIN_POSITIONS[i], named(Material.GREEN_STAINED_GLASS_PANE, "&aSlot &f#" + slot,
                        "&7Click to save your current race here"));
            } else {
                Race race = raceByKey(key);
                String name = race == null ? key : stripColor(race.getDisplayName());
                Material mat = race == null ? Material.PAPER : plugin.getRacePoolManager().materialFor(race);
                inv.setItem(MAIN_POSITIONS[i], named(mat, "&f" + name,
                        "&7Slot #" + slot, "&7Click to manage"));
            }
        }
        p.openInventory(inv);
        states.put(p, new State(Mode.MAIN, 0));
    }

    private void openSubmenu(Player p, int slot) {
        Inventory inv = plugin.getServer().createInventory(null, 27, MessageUtil.color("&8Slot #" + slot));
        fillBackground(inv);
        inv.setItem(SUBMENU_SAVE, named(Material.WRITABLE_BOOK, "&eSave new race here",
                "&7Overwrite slot #" + slot + " with your current race"));
        inv.setItem(SUBMENU_LOAD, named(Material.DIAMOND, "&bLoad this race",
                "&7Make this your active race (cooldown applies)"));
        p.openInventory(inv);
        states.put(p, new State(Mode.SUBMENU, slot));
    }

    private void openConfirm(Player p, Mode mode, int slot) {
        String title = mode == Mode.SAVE_CONFIRM ? "&aSave this race?"
                : mode == Mode.REPLACE_CONFIRM ? "&cReplace race?"
                : "&eLoad saved race?";
        Inventory inv = plugin.getServer().createInventory(null, 27, MessageUtil.color(title));
        fillBackground(inv);
        String centerKey = mode == Mode.SAVE_CONFIRM
                ? currentRaceKey(p)
                : plugin.getPlayerDataManager().getRaceSlot(p.getUniqueId(), slot);
        Race centerRace = raceByKey(centerKey);
        String centerName = centerRace == null ? stripColor(centerKey) : stripColor(centerRace.getDisplayName());
        String lore = mode == Mode.SAVE_CONFIRM ? "&7Save into slot #" + slot + "?"
                : mode == Mode.REPLACE_CONFIRM ? "&7This race will be overwritten"
                : "&7Switch to this race?";
        Material mat = centerRace == null ? Material.PAPER : plugin.getRacePoolManager().materialFor(centerRace);
        inv.setItem(CONFIRM_CENTER, named(mat, "&f" + centerName, lore));
        inv.setItem(CONFIRM_RED, named(Material.RED_STAINED_GLASS_PANE, "&cCancel"));
        inv.setItem(CONFIRM_GREEN, named(Material.GREEN_STAINED_GLASS_PANE, "&aConfirm"));
        p.openInventory(inv);
        states.put(p, new State(mode, slot));
    }

    @EventHandler
    public void onClick(InventoryClickEvent e) {
        Player p = (Player) e.getWhoClicked();
        State st = states.get(p);
        if (st == null) return;
        e.setCancelled(true);
        int slot = e.getSlot();
        switch (st.mode) {
            case MAIN:
                for (int i = 0; i < MAIN_POSITIONS.length; i++) {
                    if (slot != MAIN_POSITIONS[i]) continue;
                    int n = i + 1;
                    if (plugin.getPlayerDataManager().getRaceSlot(p.getUniqueId(), n) == null) {
                        if (currentRaceKey(p) == null) {
                            p.sendMessage(MessageUtil.color("&cYou have no race to save."));
                            return;
                        }
                        openConfirm(p, Mode.SAVE_CONFIRM, n);
                    } else {
                        openSubmenu(p, n);
                    }
                    return;
                }
                return;
            case SUBMENU:
                if (slot == SUBMENU_SAVE) {
                    if (currentRaceKey(p) == null) {
                        p.sendMessage(MessageUtil.color("&cYou have no race to save."));
                        return;
                    }
                    openConfirm(p, Mode.REPLACE_CONFIRM, st.slot);
                } else if (slot == SUBMENU_LOAD) {
                    long remaining = secondsRemaining(plugin.getPlayerDataManager().getLoadCooldown(p.getUniqueId()),
                            System.currentTimeMillis());
                    if (remaining > 0) {
                        p.sendMessage(MessageUtil.color("&cWait " + remaining + "s before switching races."));
                        openMain(p);
                    } else {
                        openConfirm(p, Mode.LOAD_CONFIRM, st.slot);
                    }
                }
                return;
            case SAVE_CONFIRM:
            case REPLACE_CONFIRM:
                if (slot == CONFIRM_GREEN) {
                    String key = currentRaceKey(p);
                    if (key == null) {
                        p.sendMessage(MessageUtil.color("&cYou have no race to save."));
                        return;
                    }
                    plugin.getPlayerDataManager().setRaceSlot(p.getUniqueId(), st.slot, key);
                    openMain(p);
                } else if (slot == CONFIRM_RED) {
                    openMain(p);
                }
                return;
            case LOAD_CONFIRM:
                if (slot == CONFIRM_GREEN) {
                    load(p, st.slot);
                    openMain(p);
                } else if (slot == CONFIRM_RED) {
                    openMain(p);
                }
                return;
        }
    }

    private void load(Player p, int slot) {
        String key = plugin.getPlayerDataManager().getRaceSlot(p.getUniqueId(), slot);
        Race race = raceByKey(key);
        if (race == null) return;
        long end = System.currentTimeMillis() + plugin.getConfig().getInt("race-slot-cooldown-seconds", 30) * 1000L;
        plugin.getPlayerDataManager().setLoadCooldown(p.getUniqueId(), end);
        assignmentManager.assign(p, race);
        plugin.getPlayerDataManager().markClaimed(p.getUniqueId());
        p.sendMessage(MessageUtil.color("&aLoaded saved race &e" + stripColor(race.getDisplayName()) + "&a."));
    }

    @EventHandler
    public void onClose(InventoryCloseEvent e) {
        states.remove((Player) e.getPlayer());
    }

    private String currentRaceKey(Player p) {
        Race r = RaceManager.getRace(p);
        return r == null ? null : r.getName();
    }

    private String currentRaceName(Player p) {
        Race r = RaceManager.getRace(p);
        return r == null ? null : stripColor(r.getDisplayName());
    }

    private Race raceByKey(String key) {
        if (key == null) return null;
        Map<String, Race> races = RaceManager.getRegisteredRaces();
        return races == null ? null : races.get(key);
    }

    public static long secondsRemaining(long endEpochMillis, long nowMillis) {
        long ms = endEpochMillis - nowMillis;
        if (ms <= 0) return 0;
        return (ms + 999L) / 1000L;
    }

    private void fillBackground(Inventory inv) {
        ItemStack black = named(Material.BLACK_STAINED_GLASS_PANE, " ");
        for (int slot = 0; slot < inv.getSize(); slot++) {
            inv.setItem(slot, black);
        }
    }

    private ItemStack named(Material material, String name, String... lore) {
        ItemStack item = new ItemStack(material, 1);
        ItemMeta meta = item.getItemMeta();
        if (meta != null) {
            meta.setDisplayName(MessageUtil.color(name));
            if (lore.length > 0) {
                java.util.List<String> lines = new java.util.ArrayList<>();
                for (String s : lore) lines.add(MessageUtil.color(s));
                meta.setLore(lines);
            }
            item.setItemMeta(meta);
        }
        return item;
    }

    private String stripColor(String s) {
        if (s == null) return "";
        return s.replaceAll("(?i)\\u00A7[0-9a-fk-or]", "");
    }
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `mvn -q test -Dtest=RaceSlotGuiTest`
Expected: PASS (helper test green; GUI logic compiles).

- [ ] **Step 5: Verify full tree compiles**

Run: `mvn -q compile`
Expected: BUILD SUCCESS.

---

### Task 3: `/raceslot` command + wiring + config + version + README

Registers the command, binds the GUI instance as a plugin listener, adds the cooldown config, bumps versions.

**Files:**
- Create: `src/main/java/com/yourname/randomrace/commands/RaceSlotCommand.java`
- Modify: `src/main/java/com/yourname/randomrace/RandomRacePlugin.java`
- Modify: `src/main/resources/plugin.yml`
- Modify: `src/main/resources/config.yml`
- Modify: `pom.xml`
- Modify: `README.md`

**Interfaces:**
- Consumes: Task 2 `RaceSlotGui.openMain(Player)`.
- Produces: registered command `raceslot` (permission `randomrace.claim`).

- [ ] **Step 1: Create RaceSlotCommand**

Create `src/main/java/com/yourname/randomrace/commands/RaceSlotCommand.java`:

```java
package com.yourname.randomrace.commands;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.utils.MessageUtil;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

public class RaceSlotCommand implements CommandExecutor {
    private final RandomRacePlugin plugin;

    public RaceSlotCommand(RandomRacePlugin plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!(sender instanceof Player)) {
            sender.sendMessage(MessageUtil.color("&cOnly players can use this."));
            return true;
        }
        Player p = (Player) sender;
        if (!p.hasPermission("randomrace.claim")) {
            p.sendMessage(MessageUtil.color("&cYou don't have permission to use this."));
            return true;
        }
        plugin.getRaceSlotGui().openMain(p);
        return true;
    }
}
```

- [ ] **Step 2: Wire into RandomRacePlugin**

In `RandomRacePlugin.java`:
- Add imports `import com.yourname.randomrace.commands.RaceSlotCommand;` and `import com.yourname.randomrace.gui.RaceSlotGui;`
- Add field `private RaceSlotGui raceSlotGui;`
- In `onEnable`, after the existing command registrations add:

```java
        raceSlotGui = new RaceSlotGui(this);
        Bukkit.getPluginManager().registerEvents(raceSlotGui, this);
        Objects.requireNonNull(getCommand("raceslot")).setExecutor(new RaceSlotCommand(this));
```

- Add getter:

```java
    public RaceSlotGui getRaceSlotGui() { return raceSlotGui; }
```

(`Bukkit` is already imported in `RandomRacePlugin` from Task 6 of the reroll-slots feature; if not, add `import org.bukkit.Bukkit;`.)

- [ ] **Step 3: plugin.yml — command + version**

In `src/main/resources/plugin.yml`:
- Change `version: 1.2.0` to `version: 1.3.0`
- Add after the `valracestats` block:

```yaml
  raceslot:
    description: Open your 5 saved-race slots (save / replace / load)
    permission: randomrace.claim
```

- [ ] **Step 4: pom.xml version**

In `pom.xml`, change `<version>1.2.0</version>` to `<version>1.3.0</version>`.

- [ ] **Step 5: config.yml cooldown key**

In `src/main/resources/config.yml`, add after `classes-count`:

```yaml
# Seconds between loading two saved races from /raceslot (saving is never throttled).
race-slot-cooldown-seconds: 30
```

- [ ] **Step 6: README**

In `README.md`:
- Change `# Result: target/randomrace-1.2.0.jar` to `# Result: target/randomrace-1.3.0.jar`
- Add a row after the `/rerollclass` row:

```
| `/raceslot` | `randomrace.claim` | Open your 5 saved-race slots (save, replace, load) |
```

- [ ] **Step 7: Verify compile + tests**

Run: `mvn -q compile` — BUILD SUCCESS.
Run: `mvn -q test` — all tests green.

---

### Task 4: Final verification

- [ ] **Step 1: Full test suite**

Run: `mvn test`
Expected: all tests pass (33 existing + 6 new, no failures).

- [ ] **Step 2: Package the jar**

Run: `mvn -q package`
Expected: BUILD SUCCESS. Verify with `Get-ChildItem target\randomrace-1.3.0.jar`.

- [ ] **Step 3: Sanity-check config**

Confirm `src/main/resources/config.yml` contains `race-slot-cooldown-seconds: 30` and that `plugin.yml` version is `1.3.0`.

- [ ] **Step 4: Report**

Summarize: `PlayerDataManager` slot/cooldown methods, `RaceSlotGui`, `RaceSlotCommand`, version 1.3.0, jar path, and the manual server test script:
1. No race → `/raceslot` shows empty slots; clicking one → "&cYou have no race to save."
2. `/claimrace` → `/raceslot` → click empty slot 1 → confirm red/green + current race center → green → slot fills; refshes GUI.
3. Click filled slot → sub-menu (Save new / Load this) → Save new → replace confirm (shows stored race) → green overwrites.
4. Load this → load confirm → green → `&aLoaded saved race ...`; immediately loading again → `&cWait Ns ...`.
5. Verify `/valracestats` race changed; reroll counts untouched.

---

## Self-Review

- **Spec coverage:** `/raceslot` + `randomrace.claim` (Task 3) · Main GUI 5 slots at cols 0,2,4,6,8 with green empty panes + current-race info top-center (Task 2) · empty-slot confirm "save" with red left/green right + 2-side gaps (Task 2 `openConfirm`) · filled-slot sub-menu Save-new/Load (Task 2 `openSubmenu`) · replace confirm showing stored race (Task 2 `REPLACE_CONFIRM`) · load confirm + `AssignmentManager.assign` + claimed + cooldown (Task 2 `load`) · wait-Xs message (Task 2 SUBMENU branch) · short titles + full question in lore (Task 2 confirm titles/lore) · storage `raceslots.1..5` + `race-slot-cooldown` (Task 1) · cooldown config key (Task 3) · version 1.3.0 (Task 3) · tests for storage + helper (Tasks 1–2, 4).
- **Placeholder scan:** Every step has concrete code or exact commands; no TBDs.
- **Type consistency:** `openMain(Player)`, `secondsRemaining(long,long)` names match across Tasks 2–3; `getRaceSlot(UUID,int)`, `setRaceSlot(UUID,int,String)`, `getLoadCooldown(UUID)`, `setLoadCooldown(UUID,long)` identical in Tasks 1–2; `AssignmentManager.assign(Player,Race)` and `RacePoolManager.materialFor(Race)` match their existing definitions used in `SpinAnimation`/`ClassSpinAnimation`.