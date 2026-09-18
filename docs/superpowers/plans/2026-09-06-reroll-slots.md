# Reroll Points + Class Slots Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add per-player race reroll points, class reroll points, and an admin-set class slot cap to RandomRace, with spend-on-`/claim` rerolls, dedicated `/rerollrace` / `/rerollclass` commands, and join reminders.

**Architecture:** PlayerDataManager stores the three new per-player fields in `playerdata.yml`. A `RerollService` owns all spend/slot rules and is unit-tested. Player commands branch into "free claim/fill" vs "spend a reroll" paths; admin commands gain `give/set/setslots/check`. A `PlayerJoinListener` sends an intro on first join and reminders when spare rerolls exist. `ClassSpinAnimation` gains a `keep` map so partial fills merge with existing classes instead of replacing them.

**Tech Stack:** Java 21, Paper API 1.21.1, Maven, JUnit 5 (jupiter), ValhallaRaces compile-time stubs.

## Global Constraints

- Working directory for all builds: `D:\e\Projects\ValhallaRaces\RandomRace`
- Java source is comment-free (project convention). Mini YAML comments in `config.yml` are OK (existing style).
- Version bump to **1.2.0** in BOTH `pom.xml` and `src/main/resources/plugin.yml`.
- No git commits during implementation — the user commits/pushes when they choose. Do not stage or commit.
- Do not touch `target/` (git-ignored) or anything outside `D:\e\Projects\ValhallaRaces\RandomRace\` and the spec/plan docs.
- Keep existing public behavior of untouched subcommands (`listrace`, `setrace`, `setclass`, `setclasscount`, `listclass`, `reload`) working.
- `mvn` commands run from `D:\e\Projects\ValhallaRaces\RandomRace`.

---

### Task 1: PlayerDataManager — reroll/slot storage, `clearClaim`, File constructor

Adds storage for the three new fields, a test-friendly `File` constructor, and the `clearClaim` semantic (claim data wiped, granted points/slots/joined kept). Command paths that wipe a whole record (`reset`, `reroll` in `RandomRaceAdminCommand`) switch to `clearClaim` in the same task so the tree always compiles.

**Files:**
- Modify: `src/main/java/com/yourname/randomrace/managers/PlayerDataManager.java`
- Modify: `src/main/java/com/yourname/randomrace/commands/RandomRaceAdminCommand.java:78` and `:86` (two `clear(` calls → `clearClaim(`)
- Test: `src/test/java/com/yourname/randomrace/managers/PlayerDataManagerTest.java`

**Interfaces:**
- Produces (used by later tasks):
  - `int getRaceRerolls(UUID)` / `void addRaceRerolls(UUID,int)` / `void setRaceRerolls(UUID,int)`
  - `int getClassRerolls(UUID)` / `void addClassRerolls(UUID,int)` / `void setClassRerolls(UUID,int)`
  - `int getClassSlots(UUID)` (stored raw, default -1) / `void setClassSlots(UUID,int)`
  - `boolean hasRecord(UUID)` / `void markJoined(UUID)` / `void clearClaim(UUID)`
  - constructor `PlayerDataManager(File file)`
- Consumes: nothing new.

- [ ] **Step 1: Write the failing test**

Create `src/test/java/com/yourname/randomrace/managers/PlayerDataManagerTest.java`:

```java
package com.yourname.randomrace.managers;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.File;
import java.nio.file.Path;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

public class PlayerDataManagerTest {

    @TempDir
    Path tempDir;

    private PlayerDataManager manager() {
        return new PlayerDataManager(new File(tempDir.toFile(), "playerdata.yml"));
    }

    @Test
    void defaultRerollsAndSlots() {
        PlayerDataManager m = manager();
        UUID id = UUID.randomUUID();
        assertEquals(0, m.getRaceRerolls(id));
        assertEquals(0, m.getClassRerolls(id));
        assertEquals(-1, m.getClassSlots(id));
    }

    @Test
    void addAndSetRerollsPersist() {
        PlayerDataManager m = manager();
        UUID id = UUID.randomUUID();
        m.addRaceRerolls(id, 2);
        m.addClassRerolls(id, 3);
        assertEquals(2, m.getRaceRerolls(id));
        assertEquals(3, m.getClassRerolls(id));
        m.setRaceRerolls(id, 1);
        m.setClassRerolls(id, 0);
        assertEquals(1, m.getRaceRerolls(id));
        assertEquals(0, m.getClassRerolls(id));
    }

    @Test
    void setClassSlotsPersists() {
        PlayerDataManager m = manager();
        UUID id = UUID.randomUUID();
        m.setClassSlots(id, 5);
        assertEquals(5, m.getClassSlots(id));
    }

    @Test
    void clearClaimPreservesRerollsSlotsAndRecord() {
        PlayerDataManager m = manager();
        UUID id = UUID.randomUUID();
        m.markJoined(id);
        m.setRace(id, "dragonkin", "Steve");
        m.addRaceRerolls(id, 2);
        m.setClassSlots(id, 6);
        m.clearClaim(id);
        assertNull(m.getRace(id));
        assertEquals(2, m.getRaceRerolls(id));
        assertEquals(6, m.getClassSlots(id));
        assertTrue(m.hasRecord(id));
    }

    @Test
    void markJoinedCreatesRecord() {
        PlayerDataManager m = manager();
        UUID id = UUID.randomUUID();
        assertFalse(m.hasRecord(id));
        m.markJoined(id);
        assertTrue(m.hasRecord(id));
    }

    @Test
    void resolveOfflineFindsByName() {
        PlayerDataManager m = manager();
        UUID id = UUID.randomUUID();
        m.setRace(id, "elf", "Alex");
        assertEquals(id, m.resolveOffline("ALEX"));
    }
}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `mvn -q test -Dtest=PlayerDataManagerTest`
Expected: FAIL — `getRaceRerolls`, `getClassRerolls`, `getClassSlots`, `hasRecord`, `markJoined`, `clearClaim`, and the `File` constructor do not exist yet.

- [ ] **Step 3: Implement**

Replace the body of `PlayerDataManager.java` with:

```java
package com.yourname.randomrace.managers;

import com.yourname.randomrace.RandomRacePlugin;
import org.bukkit.configuration.file.YamlConfiguration;

import java.io.File;
import java.io.IOException;
import java.util.UUID;

public class PlayerDataManager {
    private final RandomRacePlugin plugin;
    private final File file;
    private YamlConfiguration data;

    public PlayerDataManager(RandomRacePlugin plugin) {
        this.plugin = plugin;
        this.file = new File(plugin.getDataFolder(), "playerdata.yml");
        if (!file.exists()) {
            plugin.saveResource("playerdata.yml", false);
        }
        this.data = YamlConfiguration.loadConfiguration(file);
    }

    public PlayerDataManager(File file) {
        this.plugin = null;
        this.file = file;
        this.data = (file.exists() && file.length() > 0L)
                ? YamlConfiguration.loadConfiguration(file)
                : new YamlConfiguration();
    }

    public boolean hasClaimed(UUID uuid) {
        return data.getLong(uuid + ".claimed", 0L) > 0L;
    }

    public void markClaimed(UUID uuid) {
        data.set(uuid + ".claimed", System.currentTimeMillis());
        save();
    }

    public void setRace(UUID uuid, String raceKey, String playerName) {
        data.set(uuid + ".race", raceKey);
        data.set(uuid + ".name", playerName);
        save();
    }

    public String getRace(UUID uuid) {
        return data.getString(uuid + ".race");
    }

    public void setClasses(UUID uuid, java.util.Collection<String> classKeys, String playerName) {
        data.set(uuid + ".classes", new java.util.ArrayList<>(classKeys));
        data.set(uuid + ".name", playerName);
        save();
    }

    public java.util.List<String> getClasses(UUID uuid) {
        java.util.List<String> list = data.getStringList(uuid + ".classes");
        return list == null ? new java.util.ArrayList<>() : list;
    }

    public int getRaceRerolls(UUID uuid) {
        return data.getInt(uuid + ".race-rerolls", 0);
    }

    public void addRaceRerolls(UUID uuid, int amount) {
        data.set(uuid + ".race-rerolls", getRaceRerolls(uuid) + amount);
        save();
    }

    public void setRaceRerolls(UUID uuid, int amount) {
        data.set(uuid + ".race-rerolls", amount);
        save();
    }

    public int getClassRerolls(UUID uuid) {
        return data.getInt(uuid + ".class-rerolls", 0);
    }

    public void addClassRerolls(UUID uuid, int amount) {
        data.set(uuid + ".class-rerolls", getClassRerolls(uuid) + amount);
        save();
    }

    public void setClassRerolls(UUID uuid, int amount) {
        data.set(uuid + ".class-rerolls", amount);
        save();
    }

    public int getClassSlots(UUID uuid) {
        return data.getInt(uuid + ".class-slots", -1);
    }

    public void setClassSlots(UUID uuid, int slots) {
        data.set(uuid + ".class-slots", slots);
        save();
    }

    public boolean hasRecord(UUID uuid) {
        return data.contains(uuid.toString());
    }

    public void markJoined(UUID uuid) {
        data.set(uuid + ".joined", System.currentTimeMillis());
        save();
    }

    public void clearClaim(UUID uuid) {
        data.set(uuid + ".claimed", null);
        data.set(uuid + ".race", null);
        data.set(uuid + ".classes", null);
        save();
    }

    public UUID resolveOffline(String name) {
        for (String key : data.getKeys(false)) {
            String stored = data.getString(key + ".name");
            if (stored != null && stored.equalsIgnoreCase(name)) {
                try {
                    return UUID.fromString(key);
                } catch (IllegalArgumentException ignored) {
                }
            }
        }
        return null;
    }

    private void save() {
        try {
            data.save(file);
        } catch (IOException e) {
            if (plugin != null) {
                plugin.getLogger().warning("Could not save playerdata.yml: " + e.getMessage());
            }
        }
    }
}
```

In `RandomRaceAdminCommand.java`, change the two `plugin.getPlayerDataManager().clear(` calls (in the `reset` and `reroll` cases) to `plugin.getPlayerDataManager().clearClaim(`.

- [ ] **Step 4: Run test to verify it passes**

Run: `mvn -q test -Dtest=PlayerDataManagerTest`
Expected: PASS (all 6 tests green). `@TempDir` auto-generates a throwaway temp file.

- [ ] **Step 5: Verify full tree still compiles**

Run: `mvn -q compile`
Expected: BUILD SUCCESS.

---

### Task 2: RerollService + plugin wiring + tests

The single owner of the reroll/slot rules. Tested with a temp-file `PlayerDataManager` (no server needed).

**Files:**
- Create: `src/main/java/com/yourname/randomrace/managers/RerollService.java`
- Modify: `src/main/java/com/yourname/randomrace/RandomRacePlugin.java` (field + getter)
- Test: `src/test/java/com/yourname/randomrace/managers/RerollServiceTest.java`

**Interfaces:**
- Consumes: Task 1 `PlayerDataManager` (`getRaceRerolls`, `setRaceRerolls`, `getClassRerolls`, `setClassRerolls`, `getClassSlots`, `setClassSlots`).
- Produces (used by Tasks 3–8):
  - `RerollService(RandomRacePlugin plugin)`
  - `RerollService(PlayerDataManager data, int defaultClassSlots)`
  - `boolean trySpendRaceReroll(UUID)` / `boolean trySpendClassReroll(UUID)`
  - `int raceRerolls(UUID)` / `int classRerolls(UUID)` / `boolean hasAnyRerolls(UUID)`
  - `int classSlots(UUID)` (falls back to the default when stored is -1)
  - `void addRaceRerolls(UUID,int)` / `setRaceRerolls(UUID,int)` (clamp ≥0) / `addClassRerolls(UUID,int)` / `setClassRerolls(UUID,int)` (clamp ≥0) / `setClassSlots(UUID,int)` (clamp 1–10)
  - `boolean isRaceClaimed(Player)` / `boolean areClassesFull(Player)`

- [ ] **Step 1: Write the failing test**

Create `src/test/java/com/yourname/randomrace/managers/RerollServiceTest.java`:

```java
package com.yourname.randomrace.managers;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.File;
import java.nio.file.Path;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

public class RerollServiceTest {

    @TempDir
    Path tempDir;

    private RerollService service(int defaultSlots) {
        File file = new File(tempDir.toFile(), "d" + System.nanoTime() + ".yml");
        return new RerollService(new PlayerDataManager(file), defaultSlots);
    }

    @Test
    void spendRaceRerollWithNoPointsFails() {
        RerollService s = service(3);
        UUID id = UUID.randomUUID();
        assertFalse(s.trySpendRaceReroll(id));
        assertEquals(0, s.raceRerolls(id));
    }

    @Test
    void spendRaceRerollWithPointsSucceedsAndDecrements() {
        RerollService s = service(3);
        UUID id = UUID.randomUUID();
        s.addRaceRerolls(id, 2);
        assertTrue(s.trySpendRaceReroll(id));
        assertEquals(1, s.raceRerolls(id));
        assertTrue(s.trySpendRaceReroll(id));
        assertEquals(0, s.raceRerolls(id));
        assertFalse(s.trySpendRaceReroll(id));
    }

    @Test
    void spendClassRerollUsesSeparatePool() {
        RerollService s = service(3);
        UUID id = UUID.randomUUID();
        s.addClassRerolls(id, 1);
        assertTrue(s.trySpendClassReroll(id));
        assertEquals(0, s.classRerolls(id));
        assertFalse(s.trySpendRaceReroll(id));
    }

    @Test
    void classSlotsFallBackToDefaultWhenUnset() {
        RerollService s = service(4);
        UUID id = UUID.randomUUID();
        assertEquals(4, s.classSlots(id));
        s.setClassSlots(id, 7);
        assertEquals(7, s.classSlots(id));
    }

    @Test
    void setterClampsRanges() {
        RerollService s = service(3);
        UUID id = UUID.randomUUID();
        s.setClassSlots(id, 99);
        assertEquals(10, s.classSlots(id));
        s.setClassSlots(id, 0);
        assertEquals(1, s.classSlots(id));
        s.setRaceRerolls(id, -5);
        assertEquals(0, s.raceRerolls(id));
    }

    @Test
    void hasAnyRerollsTracksBothTypes() {
        RerollService s = service(3);
        UUID id = UUID.randomUUID();
        assertFalse(s.hasAnyRerolls(id));
        s.addClassRerolls(id, 1);
        assertTrue(s.hasAnyRerolls(id));
        s.setClassRerolls(id, 0);
        assertFalse(s.hasAnyRerolls(id));
    }
}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `mvn -q test -Dtest=RerollServiceTest`
Expected: FAIL — `RerollService` does not exist.

- [ ] **Step 3: Implement**

Create `src/main/java/com/yourname/randomrace/managers/RerollService.java`:

```java
package com.yourname.randomrace.managers;

import com.yourname.randomrace.RandomRacePlugin;
import me.athlaeos.valhallaraces.ClassManager;
import me.athlaeos.valhallaraces.RaceManager;
import org.bukkit.entity.Player;

import java.util.UUID;

public class RerollService {
    private final PlayerDataManager data;
    private final int defaultClassSlots;

    public RerollService(PlayerDataManager data, int defaultClassSlots) {
        this.data = data;
        this.defaultClassSlots = defaultClassSlots;
    }

    public RerollService(RandomRacePlugin plugin) {
        this(plugin.getPlayerDataManager(), plugin.getConfig().getInt("classes-count", 3));
    }

    public boolean trySpendRaceReroll(UUID uuid) {
        if (data.getRaceRerolls(uuid) <= 0) return false;
        data.setRaceRerolls(uuid, data.getRaceRerolls(uuid) - 1);
        return true;
    }

    public boolean trySpendClassReroll(UUID uuid) {
        if (data.getClassRerolls(uuid) <= 0) return false;
        data.setClassRerolls(uuid, data.getClassRerolls(uuid) - 1);
        return true;
    }

    public int raceRerolls(UUID uuid) {
        return data.getRaceRerolls(uuid);
    }

    public int classRerolls(UUID uuid) {
        return data.getClassRerolls(uuid);
    }

    public boolean hasAnyRerolls(UUID uuid) {
        return raceRerolls(uuid) > 0 || classRerolls(uuid) > 0;
    }

    public int classSlots(UUID uuid) {
        int slots = data.getClassSlots(uuid);
        return slots < 0 ? defaultClassSlots : slots;
    }

    public void addRaceRerolls(UUID uuid, int amount) {
        data.setRaceRerolls(uuid, Math.max(0, data.getRaceRerolls(uuid) + amount));
    }

    public void setRaceRerolls(UUID uuid, int amount) {
        data.setRaceRerolls(uuid, Math.max(0, amount));
    }

    public void addClassRerolls(UUID uuid, int amount) {
        data.setClassRerolls(uuid, Math.max(0, data.getClassRerolls(uuid) + amount));
    }

    public void setClassRerolls(UUID uuid, int amount) {
        data.setClassRerolls(uuid, Math.max(0, amount));
    }

    public void setClassSlots(UUID uuid, int slots) {
        data.setClassSlots(uuid, Math.max(1, Math.min(10, slots)));
    }

    public boolean isRaceClaimed(Player p) {
        return RaceManager.getRace(p) != null;
    }

    public boolean areClassesFull(Player p) {
        return ClassManager.getClasses(p).size() >= classSlots(p.getUniqueId());
    }
}
```

In `RandomRacePlugin.java`:
- Add field `private RerollService rerollService;`
- In `onEnable`, after `playerDataManager = new PlayerDataManager(this);`, add `rerollService = new RerollService(this);`
- Add getter `public RerollService getRerollService() { return rerollService; }`

- [ ] **Step 4: Run test to verify it passes**

Run: `mvn -q test -Dtest=RerollServiceTest`
Expected: PASS (all 6 tests green).

---

### Task 3: RerollMessages helper + spin-animation rerolls-left lines + ClassSpinAnimation `keep`

Shared player-facing message builder, the rerolls-left line at the end of both spins, and the `keep` map so class fills merge instead of replace.

**Files:**
- Create: `src/main/java/com/yourname/randomrace/utils/RerollMessages.java`
- Modify: `src/main/java/com/yourname/randomrace/gui/SpinAnimation.java` (rerolls-left line in `finish()`)
- Modify: `src/main/java/com/yourname/randomrace/gui/ClassSpinAnimation.java` (`keep` constructor + merged assign + rerolls-left line)

**Interfaces:**
- Consumes: Task 2 `RerollService` (via `RandomRacePlugin.getRerollService()`), `MessageUtil`.
- Produces:
  - `static void RerollMessages.sendRerollsLeft(Player, RandomRacePlugin)`
  - `static void RerollMessages.sendReminder(Player, RandomRacePlugin)` (consumed by Task 6)
  - `static String RerollMessages.plural(int)`
  - `ClassSpinAnimation(RandomRacePlugin, Player, Map<Integer,Class>, Map<Integer,Class>)` — 4-arg constructor; 3-arg delegates with an empty keep map.

- [ ] **Step 1: Implement RerollMessages**

Create `src/main/java/com/yourname/randomrace/utils/RerollMessages.java`:

```java
package com.yourname.randomrace.utils;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.managers.RerollService;
import org.bukkit.entity.Player;

public final class RerollMessages {
    private RerollMessages() {
    }

    public static void sendRerollsLeft(Player p, RandomRacePlugin plugin) {
        RerollService s = plugin.getRerollService();
        int rr = s.raceRerolls(p.getUniqueId());
        int cr = s.classRerolls(p.getUniqueId());
        String msg = plugin.getConfig().getString("messages.rerolls-left",
                "&7You have &e{rrace}&7 race reroll{race_plural} and &e{cclass}&7 class reroll{class_plural} left.");
        msg = MessageUtil.replace("{rrace}", String.valueOf(rr), msg);
        msg = MessageUtil.replace("{race_plural}", plural(rr), msg);
        msg = MessageUtil.replace("{cclass}", String.valueOf(cr), msg);
        msg = MessageUtil.replace("{class_plural}", plural(cr), msg);
        p.sendMessage(MessageUtil.color(msg));
    }

    public static void sendReminder(Player p, RandomRacePlugin plugin) {
        RerollService s = plugin.getRerollService();
        int rr = s.raceRerolls(p.getUniqueId());
        int cr = s.classRerolls(p.getUniqueId());
        String msg = plugin.getConfig().getString("messages.reroll-reminder",
                "&6You have &e{rrace}&6 race reroll{race_plural} and &e{cclass}&6 class reroll{class_plural}. Re-roll with &c/rerollrace&e / &c/rerollclass&e.");
        msg = MessageUtil.replace("{rrace}", String.valueOf(rr), msg);
        msg = MessageUtil.replace("{race_plural}", plural(rr), msg);
        msg = MessageUtil.replace("{cclass}", String.valueOf(cr), msg);
        msg = MessageUtil.replace("{class_plural}", plural(cr), msg);
        p.sendMessage(MessageUtil.color(msg));
    }

    public static String plural(int n) {
        return n == 1 ? "" : "s";
    }
}
```

- [ ] **Step 2: Verify it compiles**

Run: `mvn -q compile`
Expected: BUILD SUCCESS (both methods are gravity wells for unused-warning only; no errors).

- [ ] **Step 3: Add rerolls-left line to SpinAnimation**

In `SpinAnimation.java`:
- Add import `import com.yourname.randomrace.utils.RerollMessages;`
- In `finish()`, immediately after the `sendStatsAndLink(name);` call, add `RerollMessages.sendRerollsLeft(player, plugin);`

- [ ] **Step 4: Add `keep` + rerolls-left line to ClassSpinAnimation**

In `ClassSpinAnimation.java`:
- Add imports `import com.yourname.randomrace.utils.RerollMessages;`
- Add field `private final Map<Integer, Class> keep;`
- Change the constructor to delegate:

```java
    public ClassSpinAnimation(RandomRacePlugin plugin, Player player, Map<Integer, Class> winners) {
        this(plugin, player, winners, java.util.Collections.emptyMap());
    }

    public ClassSpinAnimation(RandomRacePlugin plugin, Player player, Map<Integer, Class> winners, Map<Integer, Class> keep) {
        this.plugin = plugin;
        this.player = player;
        this.winners = winners;
        this.keep = keep == null ? java.util.Collections.emptyMap() : keep;
        this.assignmentManager = new ClassAssignmentManager(plugin);
        this.poolManager = plugin.getClassPoolManager();
        loadGroupNames();
    }
```

- Replace the `finish()` assignment block so it merges keep + winners:

```java
    private void finish() {
        completed = true;
        HandlerList.unregisterAll(this);
        Map<Integer, Class> all = new LinkedHashMap<>();
        all.putAll(keep);
        for (Map.Entry<Integer, Class> e : winners.entrySet()) {
            all.put(e.getKey(), e.getValue());
        }
        assignmentManager.assign(player, new ArrayList<>(all.values()));
```

- In `finish()`, after the existing `sendStatsAndLink(parts);` call, add `RerollMessages.sendRerollsLeft(player, plugin);`

- [ ] **Step 5: Verify it compiles**

Run: `mvn -q compile`
Expected: BUILD SUCCESS. (Existing 3-arg call sites — e.g. admin `rerollclass` — still work via the delegating constructor.)

---

### Task 4: Claim commands become rerolls

`/claimrace``/claimclass` now spend a point when the player is already claimed/full, and `/claimclass` fills free up to the slot cap.

**Files:**
- Modify: `src/main/java/com/yourname/randomrace/commands/ClaimRaceCommand.java`
- Modify: `src/main/java/com/yourname/randomrace/commands/ClaimClassCommand.java`
- Modify: `src/main/resources/config.yml` (messages block additions)

**Interfaces:**
- Consumes: Task 2 `RerollService` methods; Task 3 `RerollMessages.sendRerollsLeft`, `ClassSpinAnimation` 4-arg constructor.
- Produces: none new (behavior change only).

- [ ] **Step 1: Rewrite ClaimRaceCommand**

Replace the body of `ClaimRaceCommand.java` with:

```java
package com.yourname.randomrace.commands;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.gui.SpinAnimation;
import com.yourname.randomrace.managers.RacePoolManager;
import com.yourname.randomrace.managers.RerollService;
import com.yourname.randomrace.utils.MessageUtil;
import com.yourname.randomrace.utils.RerollMessages;
import com.yourname.randomrace.utils.SoundUtil;
import me.athlaeos.valhallaraces.Race;
import org.bukkit.Sound;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

import java.util.List;
import java.util.Random;

public class ClaimRaceCommand implements CommandExecutor {
    private final RandomRacePlugin plugin;
    private final RerollService rerollService;
    private final Random random = new Random();

    public ClaimRaceCommand(RandomRacePlugin plugin) {
        this.plugin = plugin;
        this.rerollService = plugin.getRerollService();
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!(sender instanceof Player)) {
            sender.sendMessage(MessageUtil.color("&cOnly players can claim a race."));
            return true;
        }
        Player p = (Player) sender;
        if (!p.hasPermission("randomrace.claim")) {
            p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.no-permission", "&cYou don't have permission to use this.")));
            return true;
        }
        if (rerollService.isRaceClaimed(p) && plugin.getConfig().getBoolean("one-time-only", true)) {
            return reroll(p);
        }
        spin(p);
        return true;
    }

    private boolean reroll(Player p) {
        if (!rerollService.trySpendRaceReroll(p.getUniqueId())) {
            p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.reroll-race-no-points", "&cYou have no race rerolls left. Ask an admin to give you some.")));
            SoundUtil.play(p, Sound.ENTITY_VILLAGER_NO);
            RerollMessages.sendRerollsLeft(p, plugin);
            return true;
        }
        plugin.getRacePoolManager().refresh();
        List<Race> available = plugin.getRacePoolManager().getAvailableRaces(p);
        if (available.isEmpty()) {
            p.sendMessage(MessageUtil.color("&cThere are no races available to you right now."));
            return true;
        }
        Race winner = plugin.getRacePoolManager().pickWeighted(random, available);
        p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.reroll-race-spin", "&eThe fates are rerolling your race...")));
        new SpinAnimation(plugin, p, winner).start();
        return true;
    }

    private void spin(Player p) {
        plugin.getRacePoolManager().refresh();
        RacePoolManager rpm = plugin.getRacePoolManager();
        List<Race> available = rpm.getAvailableRaces(p);
        if (available.isEmpty()) {
            p.sendMessage(MessageUtil.color("&cThere are no races available to you right now."));
            return;
        }
        Race winner = rpm.pickWeighted(random, available);
        p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.spin-start", "&eThe fates are deciding your race...")));
        new SpinAnimation(plugin, p, winner).start();
    }
}
```

- [ ] **Step 2: Rewrite ClaimClassCommand**

Replace the body of `ClaimClassCommand.java` with:

```java
package com.yourname.randomrace.commands;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.gui.ClassSpinAnimation;
import com.yourname.randomrace.managers.ClassAssignmentManager;
import com.yourname.randomrace.managers.RerollService;
import com.yourname.randomrace.utils.MessageUtil;
import com.yourname.randomrace.utils.RerollMessages;
import com.yourname.randomrace.utils.SoundUtil;
import me.athlaeos.valhallaraces.Class;
import me.athlaeos.valhallaraces.ClassManager;
import me.athlaeos.valhallaraces.Race;
import me.athlaeos.valhallaraces.RaceManager;
import org.bukkit.Sound;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public class ClaimClassCommand implements CommandExecutor {
    private final RandomRacePlugin plugin;
    private final ClassAssignmentManager assignmentManager;
    private final RerollService rerollService;
    private final Random random = new Random();

    public ClaimClassCommand(RandomRacePlugin plugin) {
        this.plugin = plugin;
        this.assignmentManager = new ClassAssignmentManager(plugin);
        this.rerollService = plugin.getRerollService();
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!(sender instanceof Player)) {
            sender.sendMessage(MessageUtil.color("&cOnly players can claim classes."));
            return true;
        }
        Player p = (Player) sender;
        if (!p.hasPermission("randomrace.class")) {
            p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.class-no-permission", "&cYou don't have permission to use this.")));
            return true;
        }
        int cap = rerollService.classSlots(p.getUniqueId());
        Map<Integer, Class> existing = ClassManager.getClasses(p);
        int have = existing == null ? 0 : existing.size();
        if (have >= cap) {
            return reroll(p, cap);
        }
        fill(p, cap, existing);
        return true;
    }

    private boolean reroll(Player p, int cap) {
        if (!rerollService.trySpendClassReroll(p.getUniqueId())) {
            p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.reroll-class-no-points", "&cYou have no class rerolls left. Ask an admin to give you some.")));
            SoundUtil.play(p, Sound.ENTITY_VILLAGER_NO);
            RerollMessages.sendRerollsLeft(p, plugin);
            return true;
        }
        assignmentManager.clear(p);
        plugin.getClassPoolManager().refresh();
        String race = raceName(p);
        List<Integer> groups = plugin.getClassPoolManager().pickRandomGroups(random, cap, p, race, null);
        Map<Integer, Class> winners = new LinkedHashMap<>();
        for (Integer g : groups) {
            Class c = plugin.getClassPoolManager().pickForGroup(random, g, p, race);
            if (c != null) winners.put(g, c);
        }
        if (winners.isEmpty()) {
            p.sendMessage(MessageUtil.color("&cNo classes are available to you right now."));
            return true;
        }
        p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.reroll-class-spin", "&eThe fates are rerolling your classes...")));
        new ClassSpinAnimation(plugin, p, winners).start();
        return true;
    }

    private void fill(Player p, int cap, Map<Integer, Class> existing) {
        Map<Integer, Class> live = existing == null ? new LinkedHashMap<>() : existing;
        plugin.getClassPoolManager().refresh();
        String race = raceName(p);
        Set<Integer> skip = live.keySet();
        List<Integer> groups = plugin.getClassPoolManager().pickRandomGroups(random, cap, p, race, skip);
        Map<Integer, Class> winners = new LinkedHashMap<>();
        for (Integer g : groups) {
            Class c = plugin.getClassPoolManager().pickForGroup(random, g, p, race);
            if (c != null) winners.put(g, c);
        }
        if (winners.isEmpty()) {
            p.sendMessage(MessageUtil.color("&cNo classes are available to you right now."));
            return;
        }
        p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.class-spin-start", "&eThe fates are choosing your classes...")));
        new ClassSpinAnimation(plugin, p, winners, live).start();
    }

    private String raceName(Player p) {
        Race r = RaceManager.getRace(p);
        return r == null ? null : r.getName();
    }
}
```

Note: `fill` passes `live` (the player's current classes) as the `keep` map so existing classes survive; `reroll` clears first, so no keep is needed.

- [ ] **Step 3: Add config messages**

In `src/main/resources/config.yml`, append to the `messages:` block (keep the existing keys):

```yaml
  reroll-race-no-points: "&cYou have no race rerolls left. Ask an admin to give you some."
  reroll-class-no-points: "&cYou have no class rerolls left. Ask an admin to give you some."
  reroll-race-spin: "&eThe fates are rerolling your race..."
  reroll-class-spin: "&eThe fates are rerolling your classes..."
  rerolls-left: "&7You have &e{rrace}&7 race reroll{race_plural} and &e{cclass}&7 class reroll{class_plural} left."
```

Also update the `class-one-time-only:` comment line (keep the key, it is now superseded — full players always need a class reroll):

```yaml
# class-one-time-only is superseded: full players now spend a class reroll point to re-roll.
class-one-time-only: true
```

- [ ] **Step 4: Verify compile + existing tests**

Run: `mvn -q compile` — BUILD SUCCESS.
Run: `mvn -q test` — all tests green.

---

### Task 5: `/rerollrace` + `/rerollclass` commands, plugin.yml, version bumps, README

Two new player commands that always spend a point and spin.

**Files:**
- Create: `src/main/java/com/yourname/randomrace/commands/RerollRaceCommand.java`
- Create: `src/main/java/com/yourname/randomrace/commands/RerollClassCommand.java`
- Modify: `src/main/resources/plugin.yml` (commands + version)
- Modify: `pom.xml` (version)
- Modify: `src/main/java/com/yourname/randomrace/RandomRacePlugin.java` (register executors)
- Modify: `README.md` (command table rows)

**Interfaces:**
- Consumes: Task 2 `RerollService`, Task 3 `RerollMessages`, existing `SpinAnimation` / `ClassSpinAnimation`.
- Produces: registered commands `rerollrace` / `rerollclass`.

- [ ] **Step 1: Create RerollRaceCommand**

Create `src/main/java/com/yourname/randomrace/commands/RerollRaceCommand.java`:

```java
package com.yourname.randomrace.commands;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.gui.SpinAnimation;
import com.yourname.randomrace.managers.RerollService;
import com.yourname.randomrace.utils.MessageUtil;
import com.yourname.randomrace.utils.RerollMessages;
import com.yourname.randomrace.utils.SoundUtil;
import me.athlaeos.valhallaraces.Race;
import org.bukkit.Sound;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

import java.util.List;
import java.util.Random;

public class RerollRaceCommand implements CommandExecutor {
    private final RandomRacePlugin plugin;
    private final RerollService rerollService;
    private final Random random = new Random();

    public RerollRaceCommand(RandomRacePlugin plugin) {
        this.plugin = plugin;
        this.rerollService = plugin.getRerollService();
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!(sender instanceof Player)) {
            sender.sendMessage(MessageUtil.color("&cOnly players can reroll a race."));
            return true;
        }
        Player p = (Player) sender;
        if (!p.hasPermission("randomrace.claim")) {
            p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.no-permission", "&cYou don't have permission to use this.")));
            return true;
        }
        if (!rerollService.trySpendRaceReroll(p.getUniqueId())) {
            p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.reroll-race-no-points", "&cYou have no race rerolls left. Ask an admin to give you some.")));
            SoundUtil.play(p, Sound.ENTITY_VILLAGER_NO);
            RerollMessages.sendRerollsLeft(p, plugin);
            return true;
        }
        plugin.getRacePoolManager().refresh();
        List<Race> available = plugin.getRacePoolManager().getAvailableRaces(p);
        if (available.isEmpty()) {
            p.sendMessage(MessageUtil.color("&cThere are no races available to you right now."));
            return true;
        }
        Race winner = plugin.getRacePoolManager().pickWeighted(random, available);
        p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.reroll-race-spin", "&eThe fates are rerolling your race...")));
        new SpinAnimation(plugin, p, winner).start();
        return true;
    }
}
```

- [ ] **Step 2: Create RerollClassCommand**

Create `src/main/java/com/yourname/randomrace/commands/RerollClassCommand.java`:

```java
package com.yourname.randomrace.commands;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.gui.ClassSpinAnimation;
import com.yourname.randomrace.managers.ClassAssignmentManager;
import com.yourname.randomrace.managers.RerollService;
import com.yourname.randomrace.utils.MessageUtil;
import com.yourname.randomrace.utils.RerollMessages;
import com.yourname.randomrace.utils.SoundUtil;
import me.athlaeos.valhallaraces.Class;
import me.athlaeos.valhallaraces.Race;
import me.athlaeos.valhallaraces.RaceManager;
import org.bukkit.Sound;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public class RerollClassCommand implements CommandExecutor {
    private final RandomRacePlugin plugin;
    private final ClassAssignmentManager assignmentManager;
    private final RerollService rerollService;
    private final Random random = new Random();

    public RerollClassCommand(RandomRacePlugin plugin) {
        this.plugin = plugin;
        this.assignmentManager = new ClassAssignmentManager(plugin);
        this.rerollService = plugin.getRerollService();
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!(sender instanceof Player)) {
            sender.sendMessage(MessageUtil.color("&cOnly players can reroll classes."));
            return true;
        }
        Player p = (Player) sender;
        if (!p.hasPermission("randomrace.class")) {
            p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.class-no-permission", "&cYou don't have permission to use this.")));
            return true;
        }
        if (!rerollService.trySpendClassReroll(p.getUniqueId())) {
            p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.reroll-class-no-points", "&cYou have no class rerolls left. Ask an admin to give you some.")));
            SoundUtil.play(p, Sound.ENTITY_VILLAGER_NO);
            RerollMessages.sendRerollsLeft(p, plugin);
            return true;
        }
        int cap = rerollService.classSlots(p.getUniqueId());
        assignmentManager.clear(p);
        plugin.getClassPoolManager().refresh();
        String race = raceName(p);
        List<Integer> groups = plugin.getClassPoolManager().pickRandomGroups(random, cap, p, race, null);
        Map<Integer, Class> winners = new LinkedHashMap<>();
        for (Integer g : groups) {
            Class c = plugin.getClassPoolManager().pickForGroup(random, g, p, race);
            if (c != null) winners.put(g, c);
        }
        if (winners.isEmpty()) {
            p.sendMessage(MessageUtil.color("&cNo classes are available to you right now."));
            return true;
        }
        p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.reroll-class-spin", "&eThe fates are rerolling your classes...")));
        new ClassSpinAnimation(plugin, p, winners).start();
        return true;
    }

    private String raceName(Player p) {
        Race r = RaceManager.getRace(p);
        return r == null ? null : r.getName();
    }
}
```

- [ ] **Step 3: plugin.yml — commands + version**

In `src/main/resources/plugin.yml`, change `version: 1.0.0` to `version: 1.2.0`, and add the two commands (after `claimclass`):

```yaml
  rerollrace:
    description: Spend a race reroll to spin a new race
    permission: randomrace.claim
  rerollclass:
    description: Spend a class reroll to re-roll all classes
    permission: randomrace.class
```

- [ ] **Step 4: pom.xml version**

In `pom.xml`, change `<version>1.1.0</version>` to `<version>1.2.0</version>`.

- [ ] **Step 5: Register executors in RandomRacePlugin**

In `RandomRacePlugin.onEnable`, after the `claimclass` registration, add:

```java
        Objects.requireNonNull(getCommand("rerollrace")).setExecutor(new RerollRaceCommand(this));
        Objects.requireNonNull(getCommand("rerollclass")).setExecutor(new RerollClassCommand(this));
```

- [ ] **Step 6: README command rows**

In `README.md`, add two rows to the command table (after `/claimclass`):

```
| `/rerollrace` | `randomrace.claim` | Spend 1 race reroll to spin a new race |
| `/rerollclass` | `randomrace.class` | Spend 1 class reroll to re-roll all classes up to your slot cap |
```

- [ ] **Step 7: Verify compile + tests**

Run: `mvn -q compile` — BUILD SUCCESS.
Run: `mvn -q test` — all tests green.

---

### Task 6: PlayerJoinListener — intro + reminders

Sends the first-join intro and the "you have spare rerolls" reminder.

**Files:**
- Create: `src/main/java/com/yourname/randomrace/listeners/PlayerJoinListener.java`
- Modify: `src/main/java/com/yourname/randomrace/RandomRacePlugin.java` (register listener)
- Modify: `src/main/resources/config.yml` (first-join + reroll-reminder messages)

**Interfaces:**
- Consumes: Task 1 `hasRecord`/`markJoined`, Task 2 `hasAnyRerolls`, Task 3 `RerollMessages.sendReminder`, `MessageUtil`.
- Produces: join-time behavior.

- [ ] **Step 1: Create PlayerJoinListener**

Create `src/main/java/com/yourname/randomrace/listeners/PlayerJoinListener.java`:

```java
package com.yourname.randomrace.listeners;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.utils.MessageUtil;
import com.yourname.randomrace.utils.RerollMessages;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;

import java.util.UUID;

public class PlayerJoinListener implements Listener {
    private final RandomRacePlugin plugin;

    public PlayerJoinListener(RandomRacePlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler
    public void onJoin(PlayerJoinEvent e) {
        Player p = e.getPlayer();
        UUID uuid = p.getUniqueId();
        boolean first = !plugin.getPlayerDataManager().hasRecord(uuid);
        if (first) {
            plugin.getPlayerDataManager().markJoined(uuid);
        }
        plugin.getServer().getScheduler().runTaskLater(plugin, () -> {
            if (!p.isOnline()) return;
            if (first) {
                String intro = MessageUtil.replace("{player}", p.getName(),
                        plugin.getConfig().getString("messages.first-join",
                                "&eWelcome, &6{player}&e! Claim your race with &c/claimrace&e and your classes with &c/claimclass&e."));
                p.sendMessage(MessageUtil.color(intro));
            }
            if (plugin.getRerollService().hasAnyRerolls(uuid)) {
                RerollMessages.sendReminder(p, plugin);
            }
        }, 20L);
    }
}
```

- [ ] **Step 2: Register the listener**

In `RandomRacePlugin.java`, add import `import com.yourname.randomrace.listeners.PlayerJoinListener;` and `import org.bukkit.Bukkit;` (if not already imported). In `onEnable`, at the end, add:

```java
        Bukkit.getPluginManager().registerEvents(new PlayerJoinListener(this), this);
```

- [ ] **Step 3: Add join messages to config.yml**

In the `messages:` block:

```yaml
  first-join: "&eWelcome, &6{player}&e! Claim your race with &c/claimrace&e and your classes with &c/claimclass&e."
  reroll-reminder: "&6You have &e{rrace}&6 race reroll{race_plural} and &e{cclass}&6 class reroll{class_plural}. Re-roll with &c/rerollrace&e / &c/rerollclass&e."
```

- [ ] **Step 4: Verify compile + tests**

Run: `mvn -q compile` — BUILD SUCCESS.
Run: `mvn -q test` — all tests green.

---

### Task 7: Admin `give` / `set` / `setslots` / `check` + tab completion

Adds the four admin subcommands (offline-capable) and extends tab completion.

**Files:**
- Modify: `src/main/java/com/yourname/randomrace/commands/RandomRaceAdminCommand.java`

**Interfaces:**
- Consumes: Task 2 `RerollService` setters/getters, Task 1 `resolveOffline`, `ClassManager.getClasses` (live), `ClassManager.getRegisteredClasses`, `RaceManager.getRegisteredRaces`.
- Produces: `give`, `set`, `setslots`, `check` subcommands for `/randomrace`.

- [ ] **Step 1: Extend SUBCOMMANDS + imports**

In `RandomRaceAdminCommand.java`:
- Add imports: `import com.yourname.randomrace.managers.PlayerDataManager;`, `import com.yourname.randomrace.managers.RerollService;`, `import java.util.UUID;` (check existing imports; `ClassManager` is already imported).
- Change the `SUBCOMMANDS` list to:

```java
    private static final List<String> SUBCOMMANDS = Arrays.asList(
        "reload", "listrace", "reset", "reroll", "setrace",
        "resetclass", "rerollclass", "setclass", "setclasscount", "listclass",
        "give", "set", "setslots", "check"
    );
```

- [ ] **Step 2: Add the four case blocks + helper**

Insert the four cases before the `default:` case in `onCommand`:

```java
            case "give":
                if (args.length < 4) { sender.sendMessage(MessageUtil.color("&cUsage: /randomrace give <player> <race|class> <amount>")); return true; }
                {
                    UUID tu = uuidFor(args[1]);
                    if (tu == null) { sender.sendMessage(MessageUtil.color("&cPlayer not found.")); return true; }
                    int n;
                    try {
                        n = Integer.parseInt(args[3]);
                    } catch (NumberFormatException ex) {
                        sender.sendMessage(MessageUtil.color("&cInvalid amount."));
                        return true;
                    }
                    if (n < 1) { sender.sendMessage(MessageUtil.color("&cAmount must be 1 or more.")); return true; }
                    if (args[2].equalsIgnoreCase("class")) {
                        plugin.getRerollService().addClassRerolls(tu, n);
                        sender.sendMessage(MessageUtil.color("&aGave &e" + n + "&a class reroll(s) to &e" + args[1] + "&a."));
                    } else if (args[2].equalsIgnoreCase("race")) {
                        plugin.getRerollService().addRaceRerolls(tu, n);
                        sender.sendMessage(MessageUtil.color("&aGave &e" + n + "&a race reroll(s) to &e" + args[1] + "&a."));
                    } else {
                        sender.sendMessage(MessageUtil.color("&cType must be 'race' or 'class'."));
                        return true;
                    }
                }
                return true;
            case "set":
                if (args.length < 4) { sender.sendMessage(MessageUtil.color("&cUsage: /randomrace set <player> <race|class> <amount>")); return true; }
                {
                    UUID tu = uuidFor(args[1]);
                    if (tu == null) { sender.sendMessage(MessageUtil.color("&cPlayer not found.")); return true; }
                    int n;
                    try {
                        n = Integer.parseInt(args[3]);
                    } catch (NumberFormatException ex) {
                        sender.sendMessage(MessageUtil.color("&cInvalid amount."));
                        return true;
                    }
                    if (n < 0) { sender.sendMessage(MessageUtil.color("&cAmount cannot be negative.")); return true; }
                    if (args[2].equalsIgnoreCase("class")) {
                        plugin.getRerollService().setClassRerolls(tu, n);
                    } else if (args[2].equalsIgnoreCase("race")) {
                        plugin.getRerollService().setRaceRerolls(tu, n);
                    } else {
                        sender.sendMessage(MessageUtil.color("&cType must be 'race' or 'class'."));
                        return true;
                    }
                    sender.sendMessage(MessageUtil.color("&aSet " + args[1] + "'s " + args[2].toLowerCase() + " rerolls to &e" + n + "&a."));
                }
                return true;
            case "setslots":
                if (args.length < 3) { sender.sendMessage(MessageUtil.color("&cUsage: /randomrace setslots <player> <1-10>")); return true; }
                {
                    UUID tu = uuidFor(args[1]);
                    if (tu == null) { sender.sendMessage(MessageUtil.color("&cPlayer not found.")); return true; }
                    int n;
                    try {
                        n = Integer.parseInt(args[2]);
                    } catch (NumberFormatException ex) {
                        sender.sendMessage(MessageUtil.color("&cInvalid number."));
                        return true;
                    }
                    if (n < 1 || n > 10) { sender.sendMessage(MessageUtil.color("&cSlots must be between 1 and 10.")); return true; }
                    plugin.getRerollService().setClassSlots(tu, n);
                    sender.sendMessage(MessageUtil.color("&aSet " + args[1] + "'s max class slots to &e" + n + "&a."));
                    Player online = Bukkit.getPlayerExact(args[1]);
                    if (online != null && ClassManager.getClasses(online).size() > n) {
                        sender.sendMessage(MessageUtil.color("&7(They currently have more classes; the next class re-roll will shrink to " + n + ".)"));
                    }
                }
                return true;
            case "check":
                if (args.length < 2) { sender.sendMessage(MessageUtil.color("&cUsage: /randomrace check <player>")); return true; }
                {
                    UUID tu = uuidFor(args[1]);
                    if (tu == null) { sender.sendMessage(MessageUtil.color("&cPlayer not found.")); return true; }
                    PlayerDataManager pdm = plugin.getPlayerDataManager();
                    RerollService rs = plugin.getRerollService();
                    String race = pdm.getRace(tu);
                    int have = pdm.getClasses(tu).size();
                    sender.sendMessage(MessageUtil.color("&8&m------------------------"));
                    sender.sendMessage(MessageUtil.color("&e&l" + args[1]));
                    sender.sendMessage(MessageUtil.color("&8Race: &f" + (race == null ? "&7None" : race)));
                    sender.sendMessage(MessageUtil.color("&8Classes: &f" + have + "&7/&f" + rs.classSlots(tu)));
                    sender.sendMessage(MessageUtil.color("&8Race rerolls: &f" + rs.raceRerolls(tu)));
                    sender.sendMessage(MessageUtil.color("&8Class rerolls: &f" + rs.classRerolls(tu)));
                    sender.sendMessage(MessageUtil.color("&8&m------------------------"));
                }
                return true;
```

Add the `uuidFor` helper method (near `playerNames`):

```java
    private UUID uuidFor(String name) {
        Player online = Bukkit.getPlayerExact(name);
        if (online != null) return online.getUniqueId();
        UUID stored = plugin.getPlayerDataManager().resolveOffline(name);
        if (stored != null) return stored;
        return Bukkit.getOfflinePlayer(name).getUniqueId();
    }
```

- [ ] **Step 3: Extend tab completion**

In `onTabComplete`, in the `args.length == 2` switch, add:

```java
                case "give":
                case "set":
                case "setslots":
                case "check":
                    return filter(playerNames(), args[1]);
```

In the `args.length == 3` switch, add:

```java
                case "give":
                case "set":
                    return filter(Arrays.asList("race", "class"), args[2]);
```

- [ ] **Step 4: Verify compile + tests**

Run: `mvn -q compile` — BUILD SUCCESS.
Run: `mvn -q test` — all tests green.

---

### Task 8: `/valracestats` reroll/slot line

Adds a line to the detail view showing rerolls and slots (works for online and offline targets).

**Files:**
- Modify: `src/main/java/com/yourname/randomrace/commands/ValhallaStatsCommand.java`

**Interfaces:**
- Consumes: Task 2 `RerollService` getters, Task 1 `resolveOffline`.
- Produces: extra detail line.

- [ ] **Step 1: Add the reroll/slot line**

In `ValhallaStatsCommand.java`:
- Add import `import com.yourname.randomrace.managers.RerollService;` and `import java.util.UUID;` (UUID is already imported).
- In `sendDetail`, after the `classesLive`/`classKeys` block and before the `StatInfo.formatCombinedStats` loop, insert:

```java
        UUID targetUuid = online != null ? online.getUniqueId() : plugin.getPlayerDataManager().resolveOffline(name);
        if (targetUuid != null) {
            RerollService rs = plugin.getRerollService();
            sender.sendMessage(MessageUtil.color("&8Rerolls: &f" + rs.raceRerolls(targetUuid) + " race / "
                    + rs.classRerolls(targetUuid) + " class &8- Slots: &f" + rs.classSlots(targetUuid)));
        }
```

- [ ] **Step 2: Verify compile + tests**

Run: `mvn -q compile` — BUILD SUCCESS.
Run: `mvn -q test` — all tests green.

---

### Task 9: Final verification

- [ ] **Step 1: Full test suite**

Run: `mvn test`
Expected: all tests pass (existing 4 test classes + the 2 new ones, no failures).

- [ ] **Step 2: Package the jar**

Run: `mvn -q package`
Expected: BUILD SUCCESS. Verify with `Get-ChildItem target\*.jar` that `target/randomrace-1.2.0.jar` exists.

- [ ] **Step 3: Sanity-check config keys**

Confirm `src/main/resources/config.yml` messages block now contains: `first-join`, `reroll-reminder`, `reroll-race-no-points`, `reroll-class-no-points`, `reroll-race-spin`, `reroll-class-spin`, `rerolls-left`.

- [ ] **Step 4: Report**

Summarize: files added/changed, jar path, and the manual server test script (join → rem: intro; `/claimrace` spin + rerolls-left line; `/claimclass` fill + rerolls-left line; admin `give 1 race`, `/rerollrace` spins + count drops; `setslots 5` then `/claimclass` fills 2 free; `check` shows all).

---

## Self-Review

- **Spec coverage:** Storage fields (Task 1) · RerollService rules (Task 2) · rerolls-left after claims (Tasks 3–4, animations) · `/claimrace`/`/claimclass` become rerolls (Task 4) · dedicated `/rerollrace`/`/rerollclass` (Task 5) · fill-vs-reroll both (Task 4) · slot fill free + full re-roll costs a point (Task 4) · first-join intro + reminder both (Task 6) · defaults 0/0/-1→3 (Tasks 1–2) · admin give/set/setslots/check (Task 7) · admin reroll stays free + points preserved via `clearClaim` (Tasks 1, 7) · valracestats line (Task 8) · version 1.2.0 (Task 5) · tests (Tasks 1–2, 9).
- **Placeholder scan:** All steps contain concrete code or exact commands; no TBDs.
- **Type consistency:** `RerollService` signatures identical across Tasks 2–8; `clearClaim`, `hasRecord`, `markJoined`, `classSlots`, `sendRerollsLeft`/`sendReminder` names match everywhere; `ClassSpinAnimation` 4-arg constructor (plugin, player, winners, keep) is the only new overload and matches its Task 4 usage.