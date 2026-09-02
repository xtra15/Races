# RandomRace Class Support Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add class assignment to RandomRace: a `/claimclass` command that rolls one weighted-random class per group via a 3-slot chest strip, assigned in-process through ValhallaRaces' `ClassManager`.

**Architecture:** New `ClassPoolManager` mirrors `RacePoolManager` but adds per-group filtering (permission + `race_filter`) and per-group weighted picks. A shared `WeightedPicker` util replaces the duplicate weighting logic in races and classes. `ClassSpinAnimation` runs a 3-slot strip that advances group-by-group; everything is assigned at the end via `ClassManager.setClasses`. The class gate is `ClassManager.getClasses(player)`.

**Tech Stack:** Java 21, Maven, Paper API, JUnit 5 (test scope), `me.athlaeos.valhallaraces` stub (extended with `Class`/`ClassManager`).

## Global Constraints

- Java target **21**; Paper **1.21.2** (`api-version: 1.21`); `depend: [ ValhallaMMO, ValhallaRaces ]`.
- Package `com.yourname.randomrace`; project dir `RandomRace/`.
- Gate = `ClassManager.getClasses(player)` (live); never `playerdata.yml` for the gate.
- Stub lives under `src/main/stub/`, compile-only, excluded from jar.
- Reuse existing patterns/utilities (`MessageUtil`, `SoundUtil`) — do not duplicate.
- Do not add code comments unless asked.

---

### Task 1: Extend the ValhallaRaces stub with Class + ClassManager

**Files:**
- Create: `RandomRace/src/main/stub/me/athlaeos/valhallaraces/Class.java`
- Create: `RandomRace/src/main/stub/me/athlaeos/valhallaraces/ClassManager.java`

**Interfaces:**
- Produces:
  - `me.athlaeos.valhallaraces.Class` with `getName()`, `getDisplayName()`, `getIcon()`,
    `getGroup()`, `getPermissionRequired()`, `getLimitedToRaces()`.
  - `me.athlaeos.valhallaraces.ClassManager` with static
    `getRegisteredClasses()` → `Map<String, Class>`,
    `getClasses(Player)` → `Map<Integer, Class>`,
    `setClasses(Player, Collection<Class>)`.

- [ ] **Step 1: Create `Class.java` stub**

`RandomRace/src/main/stub/me/athlaeos/valhallaraces/Class.java`:
```java
package me.athlaeos.valhallaraces;

import org.bukkit.inventory.ItemStack;

import java.util.ArrayList;
import java.util.Collection;

public class Class {
    private final String name;
    private final String displayName;
    private final ItemStack icon;
    private final int group;
    private final String permissionRequired;
    private final Collection<String> limitedToRaces;

    public Class(String name, String displayName, ItemStack icon, int group, String permissionRequired, Collection<String> limitedToRaces) {
        this.name = name;
        this.displayName = displayName;
        this.icon = icon;
        this.group = group;
        this.permissionRequired = permissionRequired;
        this.limitedToRaces = limitedToRaces == null ? new ArrayList<>() : new ArrayList<>(limitedToRaces);
    }

    public String getName() { return name; }
    public String getDisplayName() { return displayName; }
    public ItemStack getIcon() { return icon; }
    public int getGroup() { return group; }
    public String getPermissionRequired() { return permissionRequired; }
    public Collection<String> getLimitedToRaces() { return limitedToRaces; }
}
```

- [ ] **Step 2: Create `ClassManager.java` stub**

`RandomRace/src/main/stub/me/athlaeos/valhallaraces/ClassManager.java`:
```java
package me.athlaeos.valhallaraces;

import org.bukkit.entity.Player;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

public class ClassManager {
    private static Map<String, Class> registeredClasses = new HashMap<>();

    public static Map<String, Class> getRegisteredClasses() { return registeredClasses; }
    public static Map<Integer, Class> getClasses(Player p) { return new HashMap<>(); }
    public static void setClasses(Player p, Collection<Class> classes) { }
}
```

- [ ] **Step 3: Build to verify stub compiles and is excluded from jar**

Run: `mvn -q -DskipTests package`
Expected: BUILD SUCCESS; `jar tf target/randomrace-1.0.0.jar | grep -c me/athlaeos` → `0`.

- [ ] **Step 4: Commit**

```bash
git add RandomRace
git commit -m "chore(randomrace): add Class + ClassManager compile stubs"
```

---

### Task 2: Extract shared WeightedPicker; refactor RacePoolManager to use it

**Files:**
- Create: `RandomRace/src/main/java/com/yourname/randomrace/managers/WeightedPicker.java`
- Modify: `RandomRace/src/main/java/com/yourname/randomrace/managers/RacePoolManager.java`
- Test: `RandomRace/src/test/java/com/yourname/randomrace/managers/WeightedPickerTest.java`

**Interfaces:**
- Consumes: nothing (generic).
- Produces:
  - `WeightedPicker<T>` with
    `T pick(Random random, List<T> items, ToDoubleFunction<T> weight)` →
    `T` (or `null` if empty).
  - `RacePoolManager#pickWeighted(Random, List<Race>)` keeps its signature (delegates
    internally), so `ClaimRaceCommand` and admin command are unaffected.

- [ ] **Step 1: Write the failing test**

`RandomRace/src/test/java/com/yourname/randomrace/managers/WeightedPickerTest.java`:
```java
package com.yourname.randomrace.managers;

import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.function.ToDoubleFunction;

import static org.junit.jupiter.api.Assertions.*;

public class WeightedPickerTest {

    @Test
    void uniformPoolPicksAllWithinBounds() {
        List<String> items = Arrays.asList("a", "b", "c");
        ToDoubleFunction<String> w = s -> 1.0;
        int[] counts = new int[3];
        Random rnd = new Random(7L);
        for (int i = 0; i < 6000; i++) {
            counts[items.indexOf(WeightedPicker.pick(rnd, items, w))]++;
        }
        for (int c : counts) {
            assertTrue(c > 1500 && c < 2500, "unexpected count " + c);
        }
    }

    @Test
    void weightedPoolNeverReturnsNullWhenNonEmpty() {
        List<String> items = Arrays.asList("a", "b");
        ToDoubleFunction<String> w = s -> s.equals("a") ? 9.0 : 1.0;
        Random rnd = new Random(3L);
        int a = 0;
        for (int i = 0; i < 1000; i++) {
            if ("a".equals(WeightedPicker.pick(rnd, items, w))) a++;
        }
        assertTrue(a > 500, "weighted count " + a + " should favor 'a'");
    }

    @Test
    void emptyPoolReturnsNull() {
        assertNull(WeightedPicker.pick(new Random(), Arrays.asList(), s -> 1.0));
        assertNull(WeightedPicker.pick(new Random(), null, s -> 1.0));
    }
}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `mvn test`
Expected: FAIL — `WeightedPicker` not found.

- [ ] **Step 3: Implement `WeightedPicker`**

`RandomRace/src/main/java/com/yourname/randomrace/managers/WeightedPicker.java`:
```java
package com.yourname.randomrace.managers;

import java.util.List;
import java.util.Random;
import java.util.function.ToDoubleFunction;

public final class WeightedPicker {
    private WeightedPicker() {}

    public static <T> T pick(Random random, List<T> items, ToDoubleFunction<T> weight) {
        if (items == null || items.isEmpty()) return null;
        double total = 0;
        for (T item : items) total += Math.max(0.0, weight.applyAsDouble(item));
        if (total <= 0) return items.get(0);
        double roll = random.nextDouble() * total;
        double cumulative = 0;
        for (T item : items) {
            cumulative += Math.max(0.0, weight.applyAsDouble(item));
            if (roll < cumulative) return item;
        }
        return items.get(items.size() - 1);
    }
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `mvn test`
Expected: PASS (3 WeightedPicker tests).

- [ ] **Step 5: Refactor `RacePoolManager` to delegate weighting**

Replace `pickWeighted` and `weightFor` bodies in
`RandomRace/src/main/java/com/yourname/randomrace/managers/RacePoolManager.java`:

```java
@Override-like methods unchanged signatures:
    public Race pickWeighted(Random random, List<Race> available) {
        return WeightedPicker.pick(random, available, this::weightFor);
    }

    public double weightFor(Race r) {
        if (plugin == null) return 1.0;
        double w = plugin.getConfig().getDouble("race-weights." + r.getName(), 1.0);
        return Math.max(1.0, w);
    }
```
(`RacePoolManager` already imports `java.util.Random`; add no new public surface.)

- [ ] **Step 6: Run full test suite to confirm refactor didn't break race tests**

Run: `mvn test`
Expected: PASS — `RacePoolManagerTest` (3) still green alongside `WeightedPickerTest` (3).

- [ ] **Step 7: Commit**

```bash
git add RandomRace
git commit -m "refactor(randomrace): extract WeightedPicker shared by races and classes"
```

---

### Task 3: ClassPoolManager + ClassAssignmentManager

**Files:**
- Create: `RandomRace/src/main/java/com/yourname/randomrace/managers/ClassPoolManager.java`
- Create: `RandomRace/src/main/java/com/yourname/randomrace/managers/ClassAssignmentManager.java`
- Test: `RandomRace/src/test/java/com/yourname/randomrace/managers/ClassPoolManagerTest.java`

**Interfaces:**
- Consumes: stub `Class`, `ClassManager`, `RandomRacePlugin`, `WeightedPicker`.
- Produces:
  - `ClassPoolManager(RandomRacePlugin)` with `refresh()`, and
    `List<Class> candidatesFor(int group, Player player, String playerRace)`,
    `Class pickForGroup(Random, int group, Player, String race)`.
  - `ClassAssignmentManager` with `assign(Player, Collection<Class>)`,
    `replaceAll(Player, Collection<Class>)`, `clear(Player)`,
    `hasAllClasses(Player, int totalGroups)`.
  - Static helper `ClassPoolManager.filterByRace(Collection<String> limitedTo, String race)`
    (package-visible for testing) and `permissionOk(Player, String)`.

- [ ] **Step 1: Write the failing tests**

`RandomRace/src/test/java/com/yourname/randomrace/managers/ClassPoolManagerTest.java`:
```java
package com.yourname.randomrace.managers;

import me.athlaeos.valhallaraces.Class;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

import static org.junit.jupiter.api.Assertions.*;

public class ClassPoolManagerTest {

    private Class cls(String id, int group, String perm, List<String> limited) {
        return new Class(id, "&c" + id, null, group, perm, limited);
    }

    @Test
    void emptyRaceFilterIncludesClass() {
        Class c = cls("a", 1, null, Collections.emptyList());
        assertTrue(ClassPoolManager.passRaceFilter(c.getLimitedToRaces(), "elf"));
        assertTrue(ClassPoolManager.passRaceFilter(c.getLimitedToRaces(), null));
    }

    @Test
    void nonEmptyRaceFilterExcludesUnlistedRace() {
        Class c = cls("a", 1, null, Arrays.asList("elf", "human"));
        assertTrue(ClassPoolManager.passRaceFilter(c.getLimitedToRaces(), "elf"));
        assertFalse(ClassPoolManager.passRaceFilter(c.getLimitedToRaces(), "dragon"));
    }

    @Test
    void nullRaceExcludedWhenFilterNonEmpty() {
        Class c = cls("a", 1, null, Arrays.asList("elf"));
        assertFalse(ClassPoolManager.passRaceFilter(c.getLimitedToRaces(), null));
    }

    @Test
    void candidatesFilteredByGroupPermAndRace() {
        // need a Player for permission check; use null player = no perms.
        // Build a pool in a fresh ClassPoolManager with a null plugin and a null player
        // and a race "elf". Classes 1a/1b group1, 2x group2.
        // Only systematic filtering is tested here; permission filtering needs a Player and
        // is covered implicitly (null player => null perm => included).
        ClassPoolManager m = new ClassPoolManager(null);
        List<Class> all = Arrays.asList(
                cls("one", 1, null, Collections.emptyList()),
                cls("elf-only", 1, null, Arrays.asList("elf")),
                cls("other-group", 2, null, Collections.emptyList()),
                cls("locked", 1, "some.perm", Collections.emptyList()));
        // candidate source normally comes from the registry; we simulate by adding to pool
        m.poolForTest(all);
        List<Class> g1 = m.candidatesFor(1, null, "elf");
        List<String> ids = new java.util.ArrayList<>();
        for (Class c : g1) ids.add(c.getName());
        assertTrue(ids.contains("one"));
        assertTrue(ids.contains("elf-only"));
        assertFalse(ids.contains("other-group"));
        assertFalse(ids.contains("locked")); // null player lacks "some.perm"
    }

    @Test
    void pickForGroupReturnsClassInThatGroup() {
        ClassPoolManager m = new ClassPoolManager(null);
        m.poolForTest(Arrays.asList(
                cls("one", 1, null, Collections.emptyList()),
                cls("two", 1, null, Collections.emptyList()),
                cls("three", 2, null, Collections.emptyList())));
        Class picked = m.pickForGroup(new Random(5L), 1, null, null);
        assertNotNull(picked);
        assertEquals(1, picked.getGroup());
    }
}
```

Add `ClassPoolManager.poolForTest(...)` and a package-visible `pool` field accessor used
only by tests. The test needs a way to inject the pool. Provide:

```java
public void poolForTest(List<Class> classes) { pool.clear(); pool.addAll(classes); }
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `mvn test`
Expected: FAIL — `ClassPoolManager` / `ClassAssignmentManager` not found.

- [ ] **Step 3: Implement `ClassPoolManager`**

`RandomRace/src/main/java/com/yourname/randomrace/managers/ClassPoolManager.java`:
```java
package com.yourname.randomrace.managers;

import com.yourname.randomrace.RandomRacePlugin;
import me.athlaeos.valhallaraces.Class;
import me.athlaeos.valhallaraces.ClassManager;
import org.bukkit.entity.Player;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Random;

public class ClassPoolManager {
    private final RandomRacePlugin plugin;
    private final List<Class> pool = new ArrayList<>();

    public ClassPoolManager(RandomRacePlugin plugin) {
        this.plugin = plugin;
    }

    public void refresh() {
        pool.clear();
        if (ClassManager.getRegisteredClasses() == null) return;
        pool.addAll(ClassManager.getRegisteredClasses().values());
    }

    public void poolForTest(List<Class> classes) {
        pool.clear();
        pool.addAll(classes);
    }

    public List<Class> candidatesFor(int group, Player player, String playerRace) {
        List<Class> out = new ArrayList<>();
        for (Class c : pool) {
            if (c.getGroup() != group) continue;
            if (!permissionOk(player, c.getPermissionRequired())) continue;
            if (!passRaceFilter(c.getLimitedToRaces(), playerRace)) continue;
            out.add(c);
        }
        return out;
    }

    public Class pickForGroup(Random random, int group, Player player, String playerRace) {
        List<Class> candidates = candidatesFor(group, player, playerRace);
        if (candidates.isEmpty()) return null;
        return WeightedPicker.pick(random, candidates, this::weightFor);
    }

    public double weightFor(Class c) {
        if (plugin == null) return 1.0;
        double w = plugin.getConfig().getDouble("class-weights." + c.getName(), 1.0);
        return Math.max(1.0, w);
    }

    static boolean permissionOk(Player player, String required) {
        if (required == null) return true;
        return player != null && player.hasPermission(required);
    }

    static boolean passRaceFilter(Collection<String> limitedTo, String playerRace) {
        if (limitedTo == null || limitedTo.isEmpty()) return true;
        if (playerRace == null) return false;
        return limitedTo.contains(playerRace);
    }
}
```

- [ ] **Step 4: Implement `ClassAssignmentManager`**

`RandomRace/src/main/java/com/yourname/randomrace/managers/ClassAssignmentManager.java`:
```java
package com.yourname.randomrace.managers;

import me.athlaeos.valhallaraces.Class;
import me.athlaeos.valhallaraces.ClassManager;
import org.bukkit.entity.Player;

import java.util.Collection;

public class ClassAssignmentManager {

    public void assign(Player p, Collection<Class> classes) {
        ClassManager.setClasses(p, classes);
    }

    public void clear(Player p) {
        ClassManager.setClasses(p, java.util.Collections.emptyList());
    }

    public int count(Player p) {
        return ClassManager.getClasses(p).size();
    }
}
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `mvn test`
Expected: PASS — ClassPoolManagerTest (5) green. Some tests skip permission filtering because
a real `Player` isn't available; that's acceptable and documented in the test comments.

- [ ] **Step 6: Commit**

```bash
git add RandomRace
git commit -m "feat(randomrace): class pool manager with group/race filtering"
```

---

### Task 4: ClassSpinAnimation (3-slot, group-by-group)

**Files:**
- Create: `RandomRace/src/main/java/com/yourname/randomrace/gui/ClassSpinAnimation.java`

**Interfaces:**
- Consumes: `RandomRacePlugin`, `ClassPoolManager`, `ClassAssignmentManager`, `MessageUtil`,
  `SoundUtil`, stub `Class`.
- Produces:
  - `ClassSpinAnimation(RandomRacePlugin, Player, Map<Integer,Class> winners)`
    where winners maps group → pre-picked class.
  - `void start()` — runs the 3-slot animation advancing group-by-group, assigns all at the
    end via ClassAssignmentManager, sends per-group + summary messages.

- [ ] **Step 1: Implement `ClassSpinAnimation`**

`RandomRace/src/main/java/com/yourname/randomrace/gui/ClassSpinAnimation.java`:
```java
package com.yourname.randomrace.gui;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.managers.ClassAssignmentManager;
import com.yourname.randomrace.managers.ClassPoolManager;
import com.yourname.randomrace.utils.MessageUtil;
import com.yourname.randomrace.utils.SoundUtil;
import me.athlaeos.valhallaraces.Class;
import me.athlaeos.valhallaraces.Race;
import me.athlaeos.valhallaraces.RaceManager;
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.Sound;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.HandlerList;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryCloseEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemStack;
import org.bukkit.scheduler.BukkitTask;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class ClassSpinAnimation implements Listener {
    private static final int SLOTS = 3;
    private static final int CENTER = 1;
    private static final int[][] PHASES = {{2, 5}, {4, 3}, {8, 2}};
    private static final int TOTAL_TICKS;
    static {
        int t = 0;
        for (int[] p : PHASES) t += p[1];
        TOTAL_TICKS = t;
    }

    private final RandomRacePlugin plugin;
    private final Player player;
    private final Map<Integer, Class> winners;   // group -> class (assignment order)
    private final ClassPoolManager poolManager;
    private final ClassAssignmentManager assignmentManager = new ClassAssignmentManager();
    private final Map<Integer, String> groupNames = new LinkedHashMap<>();
    private Inventory inventory;
    private BukkitTask task;
    private boolean completed = false;

    public ClassSpinAnimation(RandomRacePlugin plugin, Player player, Map<Integer, Class> winners) {
        this.plugin = plugin;
        this.player = player;
        this.winners = winners;
        this.poolManager = plugin.getClassPoolManager();
        loadGroupNames();
    }

    private void loadGroupNames() {
        for (int g = 1; g <= 10; g++) {
            groupNames.put(g, plugin.getConfig().getString("groups." + g, "Group " + g));
        }
    }

    public void start() {
        inventory = plugin.getServer().createInventory(null, SLOTS, MessageUtil.color("&8Random Classes"));
        Bukkit.getPluginManager().registerEvents(this, plugin);
        player.openInventory(inventory);
        SoundUtil.play(player, Sound.BLOCK_CHEST_OPEN);
        rollNext(winners.keySet().iterator());
    }

    private void rollNext(final java.util.Iterator<Integer> groups) {
        if (!groups.hasNext()) {
            finish();
            return;
        }
        final int group = groups.next();
        final Class winner = winners.get(group);
        SoundUtil.play(player, Sound.BLOCK_CHEST_OPEN);
        final int[] tick = {0};
        task = plugin.getServer().getScheduler().runTaskTimer(plugin, () -> {
            for (int slot = 0; slot < SLOTS; slot++) {
                int idx = tick[0] + slot;
                inventory.setItem(slot, new ItemStack(materialFor(winner, group, idx), 1));
            }
            SoundUtil.play(player, Sound.UI_BUTTON_CLICK);
            tick[0]++;
            if (tick[0] >= TOTAL_TICKS) {
                task.cancel();
                inventory.setItem(CENTER, new ItemStack(materialFor(winner, group, TOTAL_TICKS), 1));
                SoundUtil.play(player, Sound.BLOCK_NOTE_BLOCK_PLING);
                sendGroupMessage(group, winner);
                plugin.getServer().getScheduler().runTaskLater(plugin, () -> rollNext(groups), 12L);
            }
        }, 10L, 2L);
    }

    private ItemStack materialFor(Class winner, int group, int lane) {
        Material m = configuredMaterial(winner);
        // depth variation: neighbors cycle through the group's candidate classes if any
        ClassPoolManager rpm = poolManager;
        List<Class> cands = rpm.candidatesFor(group, player, playerRace());
        if (!cands.isEmpty()) {
            Class shown = cands.get(lane % cands.size());
            m = configuredMaterial(shown);
        }
        return new ItemStack(m, 1);
    }

    private String playerRace() {
        Race r = RaceManager.getRace(player);
        return r == null ? null : r.getName();
    }

    private Material configuredMaterial(Class c) {
        String name = c != null ? plugin.getConfig().getString("class-materials." + c.getName()) : null;
        if (name != null) {
            Material m = Material.matchMaterial(name);
            if (m != null) return m;
        }
        if (c != null && c.getIcon() != null && c.getIcon().getType() != Material.AIR) return c.getIcon().getType();
        return Material.PAPER;
    }

    private void sendGroupMessage(int group, Class winner) {
        String gn = groupNames.getOrDefault(group, "Group " + group);
        String msg = MessageUtil.replace("{class}", stripColor(winner.getDisplayName()),
                MessageUtil.replace("{group}", gn,
                        plugin.getConfig().getString("messages.class-assigned", "&eYou are now a &b{group} {class}&e!")));
        player.sendMessage(MessageUtil.color(msg));
    }

    private void finish() {
        completed = true;
        HandlerList.unregisterAll(this);
        assignmentManager.assign(player, new ArrayList<>(winners.values()));
        List<String> parts = new ArrayList<>();
        for (Map.Entry<Integer, Class> e : winners.entrySet()) {
            parts.add(groupNames.getOrDefault(e.getKey(), "Group " + e.getKey()) + " " + stripColor(e.getValue().getDisplayName()));
        }
        String summary = MessageUtil.replace("{classes}", String.join(", ", parts),
                plugin.getConfig().getString("messages.class-summary", "&aYour classes are now: &e{classes}&a!"));
        player.sendMessage(MessageUtil.color(summary));
        SoundUtil.play(player, Sound.ENTITY_FIREWORK_ROCKET_BLAST);
        if (plugin.getConfig().getBoolean("broadcast-class", true)) {
            String bc = MessageUtil.replace("{player}", player.getName(),
                    plugin.getConfig().getString("messages.class-broadcast", "&e{player} &ahas been destined with their classes!"));
            Bukkit.broadcastMessage(MessageUtil.color(bc));
        }
    }

    private String stripColor(String s) {
        if (s == null) return "";
        return s.replaceAll("(?i)\\u00A7[0-9a-fk-or]", "");
    }

    @EventHandler
    public void onClose(InventoryCloseEvent e) {
        if (e.getPlayer().getUniqueId().equals(player.getUniqueId()) && !completed) {
            if (task != null) task.cancel();
            HandlerList.unregisterAll(this);
        }
    }

    @EventHandler
    public void onClick(InventoryClickEvent e) {
        if (e.getWhoClicked().getUniqueId().equals(player.getUniqueId())) {
            e.setCancelled(true);
        }
    }
}
```

**Task ordering note:** `ClassSpinAnimation` calls `plugin.getClassPoolManager()`, which is
added in **Task 5**. Run Task 5 Step 1 (add the getter + wire the command) before running
this Task 4 Step 2 build check, or expect compilation to fail until then. Alternatively,
execute Task 5 Step 1 and Task 4 together and build once.

- [ ] **Step 2: Build to verify compilation against stub**

Run after Task 5 Step 1: `mvn -q -DskipTests package`
Expected: BUILD SUCCESS.

- [ ] **Step 3: Commit**

```bash
git add RandomRace
git commit -m "feat(randomrace): class 3-slot group-by-group animation"
```

---

### Task 5: ClaimClassCommand + wire into plugin

**Files:**
- Create: `RandomRace/src/main/java/com/yourname/randomrace/commands/ClaimClassCommand.java`
- Modify: `RandomRace/src/main/java/com/yourname/randomrace/RandomRacePlugin.java`

**Interfaces:**
- Consumes: `ClassPoolManager`, `ClassAssignmentManager`, `ClassSpinAnimation`, `MessageUtil`,
  `SoundUtil`, stub `Class`/`ClassManager`.
- Produces:
  - `RandomRacePlugin#getClassPoolManager()` → `ClassPoolManager`
  - `RandomRacePlugin.onEnable()` wires `/claimclass`.

- [ ] **Step 1: Add `Plugin#getClassPoolManager` and wire the command**

In `RandomRacePlugin.java`:
- Add field `private ClassPoolManager classPoolManager;`
- In `onEnable()` after `racePoolManager.refresh();`:
  ```java
  classPoolManager = new ClassPoolManager(this);
  classPoolManager.refresh();
  Objects.requireNonNull(getCommand("claimclass")).setExecutor(new ClaimClassCommand(this));
  ```
- In `reload()` add `classPoolManager.refresh();`
- Add getter `public ClassPoolManager getClassPoolManager() { return classPoolManager; }`
- Add imports `com.yourname.randomrace.commands.ClaimClassCommand` and
  `com.yourname.randomrace.managers.ClassPoolManager`.

- [ ] **Step 2: Implement `ClaimClassCommand`**

`RandomRace/src/main/java/com/yourname/randomrace/commands/ClaimClassCommand.java`:
```java
package com.yourname.randomrace.commands;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.gui.ClassSpinAnimation;
import com.yourname.randomrace.managers.ClassAssignmentManager;
import com.yourname.randomrace.utils.MessageUtil;
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
import java.util.Map;
import java.util.Random;

public class ClaimClassCommand implements CommandExecutor {
    private static final int TOTAL_GROUPS = 10;
    private final RandomRacePlugin plugin;
    private final ClassAssignmentManager assignmentManager = new ClassAssignmentManager();
    private final Random random = new Random();

    public ClaimClassCommand(RandomRacePlugin plugin) {
        this.plugin = plugin;
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
        if (plugin.getConfig().getBoolean("class-one-time-only", true)
                && assignmentManager.count(p) >= TOTAL_GROUPS) {
            p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.class-already-claimed", "&cYou already have all your classes!")));
            SoundUtil.play(p, Sound.ENTITY_VILLAGER_NO);
            return true;
        }
        plugin.getClassPoolManager().refresh();
        Map<Integer, Class> existing = ClassManager.getClasses(p);
        String race = raceName(p);
        Map<Integer, Class> winners = new LinkedHashMap<>();
        StringBuilder skipped = new StringBuilder();
        for (int g = 1; g <= TOTAL_GROUPS; g++) {
            if (existing.containsKey(g)) continue;
            Class c = plugin.getClassPoolManager().pickForGroup(random, g, p, race);
            if (c == null) {
                skipped.append(" ").append(g);
                continue;
            }
            winners.put(g, c);
        }
        if (winners.isEmpty()) {
            p.sendMessage(MessageUtil.color("&cNo classes are available to you right now."));
            return true;
        }
        p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.class-spin-start", "&eThe fates are choosing your classes...")));
        new ClassSpinAnimation(plugin, p, winners).start();
        if (skipped.length() > 0) {
            p.sendMessage(MessageUtil.color("&7Some groups had no available classes:&e" + skipped));
        }
        return true;
    }

    private String raceName(Player p) {
        Race r = RaceManager.getRace(p);
        return r == null ? null : r.getName();
    }
}
```

- [ ] **Step 3: Build to verify**

Run: `mvn -q -DskipTests package`
Expected: BUILD SUCCESS.

- [ ] **Step 4: Commit**

```bash
git add RandomRace
git commit -m "feat(randomrace): /claimclass command"
```

---

### Task 6: Config + plugin.yml + admin class subcommands

**Files:**
- Modify: `RandomRace/src/main/resources/config.yml`
- Modify: `RandomRace/src/main/resources/plugin.yml`
- Modify: `RandomRace/src/main/java/com/yourname/randomrace/commands/RandomRaceAdminCommand.java`

**Interfaces:**
- Consumes: `ClassPoolManager`, `ClassAssignmentManager`, `ClassSpinAnimation`, `MessageUtil`,
  stub `Class`/`ClassManager`.

- [ ] **Step 1: Add class config to `config.yml`**

Append to `RandomRace/src/main/resources/config.yml`:
```yaml
class-weights: {}
class-materials: {}

groups:
  1: "Warrior"
  2: "Specialist"
  3: "Adept"
  4: "Healer"
  5: "Guardian"
  6: "Shadow"
  7: "Warlord"
  8: "Mystic"
  9: "Artisan"
  10: "Weaver"

class-one-time-only: true
broadcast-class: true

messages:
  class-no-permission: "&cYou don't have permission to use this."
  class-already-claimed: "&cYou already have all your classes!"
  class-spin-start: "&eThe fates are choosing your classes..."
  class-assigned: "&eYou are now a &b{group} {class}&e!"
  class-summary: "&aYour classes are now: &e{classes}&a!"
  class-broadcast: "&e{player} &ahas been destined with their classes!"
```

- [ ] **Step 2: Add `/claimclass` to `plugin.yml`**

Add under `commands:`:
```yaml
  claimclass:
    description: Roll your classes (one per group)
    permission: randomrace.class
```
And under `permissions:`:
```yaml
  randomrace.class:
    default: true
```

- [ ] **Step 3: Add admin class subcommands to `RandomRaceAdminCommand`**

Add a `ClassAssignmentManager` field and helper `groupName(int)`. Add cases to the
existing `switch` (before the `default`):

```java
case "resetclass":
    if (args.length < 2) { sender.sendMessage(MessageUtil.color("&cUsage: /randomrace resetclass <player>")); return true; }
    Player cp = Bukkit.getPlayerExact(args[1]);
    if (cp == null) { sender.sendMessage(MessageUtil.color("&cPlayer not found.")); return true; }
    classAssignmentManager.clear(cp);
    sender.sendMessage(MessageUtil.color("&aReset " + cp.getName() + "'s classes."));
    return true;
case "rerollclass":
    if (args.length < 2) { sender.sendMessage(MessageUtil.color("&cUsage: /randomrace rerollclass <player>")); return true; }
    Player rrp = Bukkit.getPlayerExact(args[1]);
    if (rrp == null) { sender.sendMessage(MessageUtil.color("&cPlayer not found.")); return true; }
    classAssignmentManager.clear(rrp);
    plugin.getClassPoolManager().refresh();
    Map<Integer, me.athlaeos.valhallaraces.Class> winners = new LinkedHashMap<>();
    String race = raceName(rrp);
    for (int g = 1; g <= 10; g++) {
        me.athlaeos.valhallaraces.Class c = plugin.getClassPoolManager().pickForGroup(random, g, rrp, race);
        if (c != null) winners.put(g, c);
    }
    if (winners.isEmpty()) { sender.sendMessage(MessageUtil.color("&cNo classes available.")); return true; }
    new ClassSpinAnimation(plugin, rrp, winners).start();
    return true;
case "setclass":
    if (args.length < 4) { sender.sendMessage(MessageUtil.color("&cUsage: /randomrace setclass <player> <group> <class>")); return true; }
    Player scp = Bukkit.getPlayerExact(args[1]);
    if (scp == null) { sender.sendMessage(MessageUtil.color("&cPlayer not found.")); return true; }
    int group;
    try { group = Integer.parseInt(args[2]); } catch (NumberFormatException e) { sender.sendMessage(MessageUtil.color("&cInvalid group.")); return true; }
    me.athlaeos.valhallaraces.Class sc = me.athlaeos.valhallaraces.ClassManager.getRegisteredClasses().get(args[3]);
    if (sc == null || sc.getGroup() != group) { sender.sendMessage(MessageUtil.color("&cClass '" + args[3] + "' not found or not in that group.")); return true; }
    java.util.Map<Integer, me.athlaeos.valhallaraces.Class> cur = new LinkedHashMap<>(me.athlaeos.valhallaraces.ClassManager.getClasses(scp));
    cur.put(group, sc);
    classAssignmentManager.replaceAll(scp, new java.util.ArrayList<>(cur.values()));
    sender.sendMessage(MessageUtil.color("&aSet " + scp.getName() + "'s " + groupName(group) + " class to " + stripColor(sc.getDisplayName()) + "&a."));
    return true;
case "listclass":
    plugin.getClassPoolManager().refresh();
    Map<String, me.athlaeos.valhallaraces.Class> classes = me.athlaeos.valhallaraces.ClassManager.getRegisteredClasses();
    if (classes == null || classes.isEmpty()) {
        sender.sendMessage(MessageUtil.color("&cNo classes loaded from ValhallaRaces."));
    } else {
        sender.sendMessage(MessageUtil.color("&aLoaded " + classes.size() + " classes:"));
        for (me.athlaeos.valhallaraces.Class c : classes.values()) {
            sender.sendMessage(MessageUtil.color("  [&b" + c.getGroup() + "&f] &7" + c.getName() + " &8- &f" + stripColor(c.getDisplayName())));
        }
    }
    return true;
```

Add to `ClassAssignmentManager` a `replaceAll(Player, Collection<Class>)` alias for
`assign(Player, Collection<Class>)` (same behavior — `setClasses` merges by group):

```java
public void replaceAll(Player p, Collection<Class> classes) { assign(p, classes); }
```

Add helpers to `RandomRaceAdminCommand`:
```java
private String raceName(Player p) {
    me.athlaeos.valhallaraces.Race r = me.athlaeos.valhallaraces.RaceManager.getRace(p);
    return r == null ? null : r.getName();
}
private String groupName(int g) {
    return plugin.getConfig().getString("groups." + g, "Group " + g);
}
```
Add field `private final ClassAssignmentManager classAssignmentManager = new ClassAssignmentManager();`
and `private final java.util.Random random = new java.util.Random();` (already present as
`random`). Add imports for `ClassSpinAnimation`, `ClassAssignmentManager`, `LinkedHashMap`.

- [ ] **Step 4: Build + run all tests**

Run: `mvn test`
Expected: BUILD SUCCESS; all tests pass (MessageUtil 3, RacePoolManager 3, WeightedPicker 3,
ClassPoolManager 5).

- [ ] **Step 5: Verify jar excludes stub classes**

Run: `jar tf target/randomrace-1.0.0.jar | Select-String me/athlaeos | Measure-Object`
Expected: `0`.

- [ ] **Step 6: Commit**

```bash
git add RandomRace
git commit -m "feat(randomrace): config/plugin/permissions + admin class subcommands"
```

---

### Task 7: Update README

**Files:**
- Modify: `RandomRace/README.md`

**Interfaces:** none.

- [ ] **Step 1: Update README**

Add `/claimclass` to the commands/permissions table and a "Classes" section describing:
- one class per group (10 groups); `/claimclass` rolls each via a 3-slot strip.
- group names from `groups.<n>` config.
- `class-weights`, `class-materials` config keys.
- `race_filter` (a class limited to certain races is excluded unless the player's race is
  listed).
- admin class subcommands (`resetclass`, `rerollclass`, `setclass`, `listclass`).
- gate = all 10 groups filled.

- [ ] **Step 2: Commit**

```bash
git add RandomRace
git commit -m "docs(randomrace): document class support"
```

---

### Task 8: Final verification

**Files:** none (verification only).

- [ ] **Step 1: Clean build with tests**

Run: `mvn clean verify`
Expected: BUILD SUCCESS, all tests pass.

- [ ] **Step 2: Confirm jar integrity**

Run:
```
jar tf target/randomrace-1.0.0.jar | Select-String -Pattern "ClaimClassCommand|ClassSpinAnimation|ClassPoolManager|plugin.yml|config.yml"
```
and
```
jar tf target/randomrace-1.0.0.jar | Select-String -Pattern "me/athlaeos" | Measure-Object
```
Expected: new classes + resources present; stub count `0`.

- [ ] **Step 3: Confirm clean git state**

Run: `git status --short` from repo root
Expected: no uncommitted changes.
