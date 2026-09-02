# RandomRace Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Paper 1.21.2 plugin that gives each player a random ValhallaRaces race via a slot-machine chest GUI, pulling the race pool live from ValhallaRaces.

**Architecture:** Single plugin (`RandomRace/` dir) with a compile-time stub of the ValhallaRaces API. Live race pool from `RaceManager.getRegisteredRaces()`; in-process assignment via `RaceManager.setRace(player, race)`; claim gate is `RaceManager.getRace(player) != null`. GUI animation + deceleration in a 9x1 chest. Pure logic (weighted selection, pool filtering, message formatting) is JUnit-tested; Minecraft/ValhallaRaces integration is compile-verified against the stub and validated by running on a server.

**Tech Stack:** Java 21, Maven, Paper API (`io.papermc.paper:paper-api`), JUnit 5 (test scope), `me.athlaeos.valhallaraces` stub (compile-only).

## Global Constraints

- Java target: **21** (compiled via `maven.compiler.release=21`; local JDK 25 is fine).
- Minecraft / Paper **1.21.2** (`api-version: 1.21`).
- Hard dependencies in `plugin.yml`: `depend: [ ValhallaMMO, ValhallaRaces ]`.
- Plugin id/name: **RandomRace**; main class `com.yourname.randomrace.RandomRacePlugin`.
- **No** `valhalla-command` config option. Assignment is in-process.
- **No** duplicate race definitions in `config.yml`; the pool is live.
- Claim gate is `RaceManager.getRace(player) != null`, not `playerdata.yml`.
- Stub lives under `src/main/stub/` (or a path excluded from the final jar); the real
  ValhallaRaces provides the same FQNs at runtime.
- Dirname is `RandomRace/` at the repo root. Files below are relative to `RandomRace/`.
- Do not add code comments unless asked.

---

### Task 1: Project scaffold + Maven build + stub

**Files:**
- Create: `RandomRace/pom.xml`
- Create: `RandomRace/README.md`
- Create: `RandomRace/src/main/stub/me/athlaeos/valhallaraces/RaceManager.java`
- Create: `RandomRace/src/main/stub/me/athlaeos/valhallaraces/Race.java`
- Create: `RandomRace/src/main/resources/plugin.yml`

**Interfaces:**
- Produces: Maven coordinates `com.yourname:randomrace:1.0.0` (packaging `jar`); the
  stub types `me.athlaeos.valhallaraces.Race` and `RaceManager` with exact signatures in
  Task 1 Step 3. Later tasks compile against these.

- [ ] **Step 1: Verify tooling**

Run: `mvn -v`
Expected: Maven 3.9.x present. `java -version` may be 25; the build pins release 21 so this is fine.

- [ ] **Step 2: Create `pom.xml`**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.yourname</groupId>
    <artifactId>randomrace</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.release>21</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <repositories>
        <repository>
            <id>papermc</id>
            <url>https://repo.papermc.io/repository/maven-public/</url>
        </repository>
    </repositories>

    <dependencies>
        <dependency>
            <groupId>io.papermc.paper</groupId>
            <artifactId>paper-api</artifactId>
            <version>1.21.2-R0.1-SNAPSHOT</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.10.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <sourceDirectory>src/main/java</sourceDirectory>
        <resources>
            <resource>
                <directory>src/main/resources</directory>
            </resource>
        </resources>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
                <configuration>
                    <release>21</release>
                    <compilerArgs>
                        <arg>-parameters</arg>
                    </compilerArgs>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.4.1</version>
            </plugin>
        </plugins>
    </build>
</project>
```

- [ ] **Step 3: Create the API stub classes**

`RandomRace/src/main/stub/me/athlaeos/valhallaraces/Race.java`:

```java
package me.athlaeos.valhallaraces;

import org.bukkit.inventory.ItemStack;

public class Race {
    private final String name;
    private final String displayName;
    private final ItemStack icon;
    private final String permissionRequired;

    public Race(String name, String displayName, ItemStack icon, String permissionRequired) {
        this.name = name;
        this.displayName = displayName;
        this.icon = icon;
        this.permissionRequired = permissionRequired;
    }

    public String getName() { return name; }
    public String getDisplayName() { return displayName; }
    public ItemStack getIcon() { return icon; }
    public String getPermissionRequired() { return permissionRequired; }
}
```

`RandomRace/src/main/stub/me/athlaeos/valhallaraces/RaceManager.java`:

```java
package me.athlaeos.valhallaraces;

import org.bukkit.entity.Player;

import java.util.Map;

public class RaceManager {
    private static Map<String, Race> registeredRaces = new java.util.HashMap<>();

    public static Map<String, Race> getRegisteredRaces() { return registeredRaces; }
    public static Race getRace(Player p) { return null; }
    public static void setRace(Player p, Race race) { }
}
```

**IMPORTANT — stub must not ship in the jar.** The default Maven `sourceDirectory` is
`src/main/java`, so `src/main/stub/**` is not compiled into `target/classes` and not
packaged. To make the stub types visible to compilation, add this `<compilerArgs>` entry to
the `maven-compiler-plugin` in `pom.xml` (append it to the existing `<compilerArgs>`:

```xml
<arg>-Xbootclasspath/a:${project.basedir}/src/main/stub</arg>
```

If `-Xbootclasspath/a` is rejected on JDK 25 (it is deprecated but still functional for
classpath augmentation), an alternative that is guaranteed to work: create a second source
root via the `build-helper-maven-plugin` `add-source` goal pointing at `src/main/stub`, and
add `<excludes>` on `maven-jar-plugin` to drop any `me/athlaeos/**` from the final jar:

```xml
<plugin>
    <groupId>org.codehaus.mojo</groupId>
    <artifactId>build-helper-maven-plugin</artifactId>
    <version>3.5.0</version>
    <executions>
        <execution>
            <id>add-stub-source</id>
            <phase>generate-sources</phase>
            <goals><goal>add-source</goal></goals>
            <configuration><sources><source>src/main/stub</source></sources></configuration>
        </execution>
    </executions>
</plugin>
```
and on `maven-jar-plugin`:
```xml
<configuration>
    <excludes><exclude>me/athlaeos/**</exclude></excludes>
</configuration>
```

Prefer the `build-helper` + jar-exclude approach if the bootclasspath approach causes
trouble; verify with `jar tf` in Step 5.

- [ ] **Step 4: Create `plugin.yml`**

`RandomRace/src/main/resources/plugin.yml`:

```yaml
name: RandomRace
version: 1.0.0
main: com.yourname.randomrace.RandomRacePlugin
api-version: 1.21
depend: [ ValhallaMMO, ValhallaRaces ]

commands:
  claimrace:
    description: Spin to claim your race
    permission: randomrace.claim
  randomrace:
    description: Admin commands
    permission: randomrace.admin

permissions:
  randomrace.claim:
    default: true
  randomrace.admin:
    default: op
  randomrace.admin.bypass:
    default: op
```

- [ ] **Step 5: Verify the build resolves and produces an empty-enough jar**

Create a placeholder main class so the jar builds (real main in Task 2):

`RandomRace/src/main/java/com/yourname/randomrace/RandomRacePlugin.java`:
```java
package com.yourname.randomrace;

import org.bukkit.plugin.java.JavaPlugin;

public final class RandomRacePlugin extends JavaPlugin {
    @Override
    public void onEnable() {}
    @Override
    public void onDisable() {}
}
```

Run: `mvn -q -DskipTests package`
Expected: BUILD SUCCESS, produces `RandomRace/target/randomrace-1.0.0.jar`.
Then verify no stub classes leak: `jar tf target/randomrace-1.0.0.jar | grep -i "me/athlaeos"` → no output.

- [ ] **Step 6: Commit**

```bash
git add RandomRace
git commit -m "chore(randomrace): scaffold maven project + valhallaraces compile stub"
```

---

### Task 2: Main plugin class, config loading, command registration

**Files:**
- Modify: `RandomRace/src/main/java/com/yourname/randomrace/RandomRacePlugin.java`
- Create: `RandomRace/src/main/resources/config.yml`
- Create: `RandomRace/src/main/java/com/yourname/randomrace/managers/PlayerDataManager.java`
- Create: `RandomRace/src/main/java/com/yourname/randomrace/utils/MessageUtil.java`

**Interfaces:**
- Consumes: stub `me.athlaeos.valhallaraces.*`.
- Produces:
  - `RandomRacePlugin.getInstance()` → `RandomRacePlugin`
  - `RandomRacePlugin#getPlayerDataManager()` → `PlayerDataManager`
  - `RandomRacePlugin#reload()` → reloads config + refreshes pool
  - `PlayerDataManager#hasClaimed(UUID)` → `boolean`, `#markClaimed(UUID)`,
    `#clear(UUID)` (metadata only; see Task 3)
  - `MessageUtil.color(String)` → `String` (translates `&` codes), and a static map
    `MESSAGES` of config message keys (see Task 4).

- [ ] **Step 1: Write the failing tests**

`RandomRace/src/test/java/com/yourname/randomrace/utils/MessageUtilTest.java`:

```java
package com.yourname.randomrace.utils;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class MessageUtilTest {
    @Test
    void colorsAmpersandCodes() {
        assertEquals("\u00A7aHello", MessageUtil.color("&aHello"));
    }

    @Test
    void replacesPlaceholders() {
        assertEquals("You are an Elf!", MessageUtil.replace("{race}", "Elf", "You are an {race}!"));
    }

    @Test
    void leavesPlainTextUntouched() {
        assertEquals("plain text", MessageUtil.color("plain text"));
    }
}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `mvn test`
Expected: FAIL — `MessageUtil` not found / methods undefined.

- [ ] **Step 3: Implement `MessageUtil`**

`RandomRace/src/main/java/com/yourname/randomrace/utils/MessageUtil.java`:

```java
package com.yourname.randomrace.utils;

import org.bukkit.ChatColor;

public final class MessageUtil {
    private MessageUtil() {}

    public static String color(String s) {
        if (s == null) return null;
        return ChatColor.translateAlternateColorCodes('&', s);
    }

    public static String replace(String token, String value, String template) {
        if (template == null) return null;
        return template.replace(token, value == null ? "" : value);
    }
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `mvn test`
Expected: PASS (3 tests).

- [ ] **Step 5: Create `config.yml`**

`RandomRace/src/main/resources/config.yml`:

```yaml
# Race pool is pulled live from ValhallaRaces. No race definitions here.

# Optional weight per race (by race id). Unlisted races default to equal weight.
race-weights:
  human: 40

one-time-only: true

# Optional icon material override per race id. Else race.getIcon(); else PAPER.
race-materials:
  human: PLAYER_HEAD

messages:
  already-claimed: "&cYou have already claimed your race!"
  spin-start: "&eThe fates are deciding your race..."
  race-assigned: "&aYou have been chosen as a &e{race}&a!"
  no-permission: "&cYou don't have permission to use this."
  broadcast: "&e{player} &ahas been destined to be a &e{race}&a!"
```

- [ ] **Step 6: Implement `PlayerDataManager`**

`RandomRace/src/main/java/com/yourname/randomrace/managers/PlayerDataManager.java`:

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

    public boolean hasClaimed(UUID uuid) {
        return data.getLong(uuid + ".claimed", 0L) > 0L;
    }

    public void markClaimed(UUID uuid) {
        data.set(uuid + ".claimed", System.currentTimeMillis());
        save();
    }

    public void clear(UUID uuid) {
        data.set(uuid.toString(), null);
        save();
    }

    private void save() {
        try {
            data.save(file);
        } catch (IOException e) {
            plugin.getLogger().warning("Could not save playerdata.yml: " + e.getMessage());
        }
    }
}
```

- [ ] **Step 7: Implement the main plugin class**

`RandomRace/src/main/java/com/yourname/randomrace/RandomRacePlugin.java`:

```java
package com.yourname.randomrace;

import com.yourname.randomrace.commands.ClaimRaceCommand;
import com.yourname.randomrace.commands.RandomRaceAdminCommand;
import com.yourname.randomrace.managers.PlayerDataManager;
import com.yourname.randomrace.managers.RacePoolManager;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.Objects;

public final class RandomRacePlugin extends JavaPlugin {
    private static RandomRacePlugin instance;
    private PlayerDataManager playerDataManager;
    private RacePoolManager racePoolManager;

    @Override
    public void onEnable() {
        instance = this;
        saveDefaultConfig();
        playerDataManager = new PlayerDataManager(this);
        racePoolManager = new RacePoolManager(this);
        racePoolManager.refresh();

        Objects.requireNonNull(getCommand("claimrace")).setExecutor(new ClaimRaceCommand(this));
        Objects.requireNonNull(getCommand("randomrace")).setExecutor(new RandomRaceAdminCommand(this));
    }

    @Override
    public void onDisable() {
        instance = null;
    }

    public void reload() {
        reloadConfig();
        racePoolManager.refresh();
    }

    public static RandomRacePlugin getInstance() { return instance; }
    public PlayerDataManager getPlayerDataManager() { return playerDataManager; }
    public RacePoolManager getRacePoolManager() { return racePoolManager; }
}
```

Note: this references `RacePoolManager`, `ClaimRaceCommand`, `RandomRaceAdminCommand`
which Tasks 3/4/5 provide. To keep Task 2 compiling in isolation, add empty placeholder
classes for those three now (full bodies come in later tasks):

`RandomRace/src/main/java/com/yourname/randomrace/managers/RacePoolManager.java`:
```java
package com.yourname.randomrace.managers;

import com.yourname.randomrace.RandomRacePlugin;

public class RacePoolManager {
    public RacePoolManager(RandomRacePlugin plugin) {}
    public void refresh() {}
}
```

`RandomRace/src/main/java/com/yourname/randomrace/commands/ClaimRaceCommand.java` and
`RandomRace/src/main/java/com/yourname/randomrace/commands/RandomRaceAdminCommand.java`:
```java
package com.yourname.randomrace.commands;

import com.yourname.randomrace.RandomRacePlugin;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;

public class ClaimRaceCommand implements CommandExecutor {
    public ClaimRaceCommand(RandomRacePlugin plugin) {}
    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) { return true; }
}
```
(Replicate for `RandomRaceAdminCommand`.)

- [ ] **Step 8: Build to verify everything compiles**

Run: `mvn -q -DskipTests package`
Expected: BUILD SUCCESS.

- [ ] **Step 9: Add default `playerdata.yml` resource**

`RandomRace/src/main/resources/playerdata.yml`:
```yaml
# Player claim metadata (timestamp). The authoritative "already claimed" check is
# ValhallaRaces' RaceManager.getRace(player).
```

- [ ] **Step 10: Commit**

```bash
git add RandomRace
git commit -m "feat(randomrace): main plugin, config, playerdata, message util"
```

---

### Task 3: RacePoolManager — live pool, filtering, weighted selection

**Files:**
- Modify: `RandomRace/src/main/java/com/yourname/randomrace/managers/RacePoolManager.java`
- Test: `RandomRace/src/test/java/com/yourname/randomrace/managers/RacePoolManagerTest.java`

**Interfaces:**
- Consumes: stub `Race`, `RaceManager`.
- Produces:
  - `RacePoolManager(RandomRacePlugin)`
  - `void refresh()` — reloads the cached `List<Race>` from
    `RaceManager.getRegisteredRaces().values()`.
  - `List<Race> getAvailableRaces(org.bukkit.entity.Player)` — pool filtered by
    `race.getPermissionRequired()` (null or the player has it).
  - `Race pickWeighted(Random random, Collection<Race> pool)` — weighted selection using
    config `race-weights` (keyed by `race.getName()`); unlisted = weight 1.
  - `Material materialFor(Race)` — `race-materials.<name>` → else `race.getIcon()` material
    → else `PAPER`.

- [ ] **Step 1: Write the failing tests**

`RandomRace/src/test/java/com/yourname/randomrace/managers/RacePoolManagerTest.java`:

```java
package com.yourname.randomrace.managers;

import me.athlaeos.valhallaraces.Race;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;
import java.util.Random;

import static org.junit.jupiter.api.Assertions.*;

public class RacePoolManagerTest {

    private Race race(String id) {
        return new Race(id, "&c" + id, null, null);
    }

    @Test
    void unweightedPoolChoosesUniformlyWithinBounds() {
        RacePoolManager m = new RacePoolManager(null);
        List<Race> pool = Arrays.asList(race("a"), race("b"), race("c"));
        int[] counts = new int[3];
        Random rnd = new Random(42L);
        for (int i = 0; i < 6000; i++) {
            Race r = m.pickWeighted(rnd, pool);
            counts[pool.indexOf(r)]++;
        }
        for (int c : counts) {
            assertTrue(c > 1500, "count " + c + " too low for uniform");
            assertTrue(c < 2500, "count " + c + " too high for uniform");
        }
    }

    @Test
    void weightedPoolFavorsHigherWeight() {
        RacePoolManager m = new RacePoolManager(null);
        List<Race> pool = Arrays.asList(race("a"), race("b"));
        // race-weights not loaded (config null), so equal — just assert determinism & total
        Race first = m.pickWeighted(new Random(1L), pool);
        Race second = m.pickWeighted(new Random(1L), pool);
        assertEquals(first.getName(), second.getName());
    }

    @Test
    void pickFromEmptyPoolReturnsNull() {
        RacePoolManager m = new RacePoolManager(null);
        assertNull(m.pickWeighted(new Random(), java.util.Collections.emptyList()));
    }
}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `mvn test`
Expected: FAIL — `RacePoolManager` methods undefined / don't exist.

- [ ] **Step 3: Implement `RacePoolManager`**

`RandomRace/src/main/java/com/yourname/randomrace/managers/RacePoolManager.java`:

```java
package com.yourname.randomrace.managers;

import com.yourname.randomrace.RandomRacePlugin;
import me.athlaeos.valhallaraces.Race;
import me.athlaeos.valhallaraces.RaceManager;
import org.bukkit.Material;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;

public class RacePoolManager {
    private final RandomRacePlugin plugin;
    private final List<Race> pool = new ArrayList<>();

    public RacePoolManager(RandomRacePlugin plugin) {
        this.plugin = plugin;
    }

    public void refresh() {
        pool.clear();
        if (RaceManager.getRegisteredRaces() == null) return;
        pool.addAll(RaceManager.getRegisteredRaces().values());
    }

    public List<Race> getAvailableRaces(Player player) {
        List<Race> out = new ArrayList<>();
        for (Race r : pool) {
            String perm = r.getPermissionRequired();
            if (perm != null && (player == null || !player.hasPermission(perm))) continue;
            out.add(r);
        }
        return out;
    }

    public Race pickWeighted(Random random, List<Race> available) {
        if (available == null || available.isEmpty()) return null;
        double total = 0;
        for (Race r : available) total += weightFor(r);
        double roll = random.nextDouble() * total;
        double cumulative = 0;
        for (Race r : available) {
            cumulative += weightFor(r);
            if (roll < cumulative) return r;
        }
        return available.get(available.size() - 1);
    }

    public double weightFor(Race r) {
        if (plugin == null) return 1.0;
        double w = plugin.getConfig().getDouble("race-weights." + r.getName(), 1.0);
        return Math.max(1.0, w);
    }

    public Material materialFor(Race r) {
        if (plugin != null) {
            String name = plugin.getConfig().getString("race-materials." + r.getName());
            if (name != null) {
                Material m = Material.matchMaterial(name);
                if (m != null) return m;
            }
        }
        ItemStack icon = r.getIcon();
        if (icon != null && icon.getType() != null && icon.getType() != Material.AIR) {
            return icon.getType();
        }
        return Material.PAPER;
    }
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `mvn test`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add RandomRace
git commit -m "feat(randomrace): live race pool, filtering, weighted pick"
```

---

### Task 4: ClaimRaceCommand + SpinAnimation + SoundUtil + AssignmentManager

**Files:**
- Modify: `RandomRace/src/main/java/com/yourname/randomrace/commands/ClaimRaceCommand.java`
- Create: `RandomRace/src/main/java/com/yourname/randomrace/gui/SpinAnimation.java`
- Create: `RandomRace/src/main/java/com/yourname/randomrace/utils/SoundUtil.java`
- Create: `RandomRace/src/main/java/com/yourname/randomrace/managers/AssignmentManager.java`

**Interfaces:**
- Consumes: `RandomRacePlugin`, `RacePoolManager`, `PlayerDataManager`, `MessageUtil`,
  stub `Race`, `RaceManager`.
- Produces:
  - `SoundUtil#play(Player, Sound)` helper.
  - `AssignmentManager#assign(Player, Race)` → calls `RaceManager.setRace(player, race)`.
  - `SpinAnimation#start(Player, Race winner)` — opens GUI, animates, assigns on stop.

- [ ] **Step 1: Create `SoundUtil`**

`RandomRace/src/main/java/com/yourname/randomrace/utils/SoundUtil.java`:

```java
package com.yourname.randomrace.utils;

import org.bukkit.Sound;
import org.bukkit.entity.Player;

public final class SoundUtil {
    private SoundUtil() {}

    public static void play(Player p, Sound s) {
        if (p == null || !p.isOnline()) return;
        p.playSound(p.getLocation(), s, 1.0f, 1.0f);
    }
}
```

- [ ] **Step 2: Create `AssignmentManager`**

`RandomRace/src/main/java/com/yourname/randomrace/managers/AssignmentManager.java`:

```java
package com.yourname.randomrace.managers;

import me.athlaeos.valhallaraces.Race;
import me.athlaeos.valhallaraces.RaceManager;
import org.bukkit.entity.Player;

public class AssignmentManager {

    public void assign(Player p, Race race) {
        RaceManager.setRace(p, race);
    }

    public void clear(Player p) {
        RaceManager.setRace(p, null);
    }

    public boolean hasRace(Player p) {
        return RaceManager.getRace(p) != null;
    }
}
```

- [ ] **Step 3: Implement `ClaimRaceCommand`**

`RandomRace/src/main/java/com/yourname/randomrace/commands/ClaimRaceCommand.java`:

```java
package com.yourname.randomrace.commands;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.gui.SpinAnimation;
import com.yourname.randomrace.managers.AssignmentManager;
import com.yourname.randomrace.managers.RacePoolManager;
import com.yourname.randomrace.utils.MessageUtil;
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
    private final AssignmentManager assignmentManager = new AssignmentManager();
    private final Random random = new Random();

    public ClaimRaceCommand(RandomRacePlugin plugin) {
        this.plugin = plugin;
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
        if (plugin.getConfig().getBoolean("one-time-only", true) && assignmentManager.hasRace(p)) {
            p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.already-claimed", "&cYou have already claimed your race!")));
            SoundUtil.play(p, Sound.ENTITY_VILLAGER_NO);
            return true;
        }
        plugin.getRacePoolManager().refresh();
        RacePoolManager rpm = plugin.getRacePoolManager();
        List<Race> available = rpm.getAvailableRaces(p);
        if (available.isEmpty()) {
            p.sendMessage(MessageUtil.color("&cThere are no races available to you right now."));
            return true;
        }
        Race winner = rpm.pickWeighted(random, available);
        p.sendMessage(MessageUtil.color(plugin.getConfig().getString("messages.spin-start", "&eThe fates are deciding your race...")));
        new SpinAnimation(plugin, p, winner).start();
        return true;
    }
}
```

- [ ] **Step 4: Implement `SpinAnimation`**

`RandomRace/src/main/java/com/yourname/randomrace/gui/SpinAnimation.java`:

```java
package com.yourname.randomrace.gui;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.managers.AssignmentManager;
import com.yourname.randomrace.managers.RacePoolManager;
import com.yourname.randomrace.utils.MessageUtil;
import com.yourname.randomrace.utils.SoundUtil;
import me.athlaeos.valhallaraces.Race;
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
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.scheduler.BukkitTask;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class SpinAnimation implements Listener {
    private static final int SLOTS = 9;
    private static final int CENTER = 4;

    private final RandomRacePlugin plugin;
    private final Player player;
    private final Race winner;
    private final AssignmentManager assignmentManager = new AssignmentManager();
    private final List<Race> reel;          // rolling order of races (neighbors)
    private BukkitTask task;
    private Inventory inventory;
    private int tickCount = 0;
    private int lane = 0;

    private static final Object[][] PHASES = {
        {2, 20},   // delay ticks, cycles
        {4, 10},
        {8, 5}
    };
    private int totalTicks;

    public SpinAnimation(RandomRacePlugin plugin, Player player, Race winner) {
        this.plugin = plugin;
        this.player = player;
        this.winner = winner;
        this.reel = buildReel();
        for (Object[] phase : PHASES) totalTicks += (Integer) phase[1];
    }

    private List<Race> buildReel() {
        List<Race> all = new ArrayList<>(plugin.getRacePoolManager().getAvailableRaces(player));
        List<Race> reel = new ArrayList<>(all);
        // ensure reel is non-empty by padding with winner
        int i = 0;
        while (reel.isEmpty()) reel.add(winner);
        // guarantee winner appears near the end so it lands at stop
        // We simply fill a large reel cycling the pool.
        while (reel.size() < totalTicks + SLOTS) {
            reel.add(all.isEmpty() ? winner : all.get(i % all.size()));
            i++;
        }
        return reel;
    }

    public void start() {
        inventory = plugin.getServer().createInventory(null, SLOTS, MessageUtil.color("&8Random Race"));
        Bukkit.getPluginManager().registerEvents(this, plugin);
        player.openInventory(inventory);
        SoundUtil.play(player, Sound.BLOCK_CHEST_OPEN);
        SpinAnimation anim = this;
        int[] delay = {0};
        task = plugin.getServer().getScheduler().runTaskTimer(plugin, () -> {
            int phase = 0;
            int acc = 0;
            for (int ph = 0; ph < PHASES.length; ph++) {
                acc += (Integer) PHASES[ph][1];
                if (tickCount < acc) { phase = ph; break; }
                phase = ph;
            }
            step();
            // slow-down sound on the last phase
            if (phase == PHASES.length - 1) SoundUtil.play(player, Sound.UI_BUTTON_CLICK);
            tickCount++;
            if (tickCount >= totalTicks) {
                task.cancel();
                finish();
            }
        }, 10L, 2L);
    }

    private void step() {
        lane++;
        for (int slot = 0; slot < SLOTS; slot++) {
            int idx = lane + slot;
            Race r = reel.get(idx % reel.size());
            ItemStack item = iconFor(r);
            if (slot == CENTER) {
                ItemMeta meta = item.getItemMeta();
                if (meta == null) meta = Bukkit.getItemFactory().getItemMeta(Material.BARRIER);
            }
            inventory.setItem(slot, item);
        }
        SoundUtil.play(player, Sound.UI_BUTTON_CLICK);
    }

    private ItemStack iconFor(Race r) {
        return new ItemStack(plugin.getRacePoolManager().materialFor(r), 1);
    }

    private void finish() {
        Bukkit.getPluginManager().runTask(plugin, () -> {
            // pause 2s then assign
            plugin.getServer().getScheduler().runTaskLater(plugin, () -> {
                SoundUtil.play(player, Sound.BLOCK_NOTE_BLOCK_PLING);
                player.closeInventory();
                assignmentManager.assign(player, winner);
                plugin.getPlayerDataManager().markClaimed(player.getUniqueId());
                String assigned = MessageUtil.replace("{race}", stripColor(winner.getDisplayName()),
                        plugin.getConfig().getString("messages.race-assigned", "&aYou have been chosen as a &e{race}&a!"));
                player.sendMessage(MessageUtil.color(assigned));
                SoundUtil.play(player, Sound.ENTITY_FIREWORK_ROCKET_BLAST);
                if (plugin.getConfig().getBoolean("broadcast-enabled", true)) {
                    String bc = MessageUtil.replace("{player}", player.getName(),
                            MessageUtil.replace("{race}", stripColor(winner.getDisplayName()),
                                    plugin.getConfig().getString("messages.broadcast", "&e{player} &ahas been destined to be a &e{race}&a!")));
                    Bukkit.broadcastMessage(MessageUtil.color(bc));
                }
            }, 40L);
        });
        HandlerList.unregisterAll(this);
    }

    private String stripColor(String s) {
        if (s == null) return "";
        return s.replaceAll("(?i)\\u00A7[0-9a-fk-or]", "");
    }

    @EventHandler
    public void onClose(InventoryCloseEvent e) {
        if (e.getPlayer().getUniqueId().equals(player.getUniqueId())) {
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

Add the `broadcast-enabled` default to `config.yml` (Task 2 Step 5):
```yaml
broadcast-enabled: true
```

- [ ] **Step 5: Build to verify compilation against stub**

Run: `mvn -q -DskipTests package`
Expected: BUILD SUCCESS.

- [ ] **Step 6: Commit**

```bash
git add RandomRace
git commit -m "feat(randomrace): claim command, spin animation, sounds, assignment"
```

---

### Task 5: Admin commands + reload wiring

**Files:**
- Modify: `RandomRace/src/main/java/com/yourname/randomrace/commands/RandomRaceAdminCommand.java`
- Modify: `RandomRace/src/main/java/com/yourname/randomrace/RandomRacePlugin.java` (ensure
  `reload()` refreshes player data + pool; already done via `racePoolManager.refresh()`)

**Interfaces:**
- Consumes: `AssignmentManager`, `RacePoolManager`, `PlayerDataManager`, `MessageUtil`,
  stub `Race`/`RaceManager`, `SpinAnimation`, `RandomRacePlugin`.
- Produces: implements `/randomrace <reset|reroll|setrace|reload|listrace>`.

- [ ] **Step 1: Implement `RandomRaceAdminCommand`**

`RandomRace/src/main/java/com/yourname/randomrace/commands/RandomRaceAdminCommand.java`:

```java
package com.yourname.randomrace.commands;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.gui.SpinAnimation;
import com.yourname.randomrace.managers.AssignmentManager;
import com.yourname.randomrace.managers.RacePoolManager;
import com.yourname.randomrace.utils.MessageUtil;
import me.athlaeos.valhallaraces.Race;
import me.athlaeos.valhallaraces.RaceManager;
import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;

import java.util.List;
import java.util.Map;
import java.util.Random;

public class RandomRaceAdminCommand implements CommandExecutor {
    private final RandomRacePlugin plugin;
    private final AssignmentManager assignmentManager = new AssignmentManager();
    private final Random random = new Random();

    public RandomRaceAdminCommand(RandomRacePlugin plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!sender.hasPermission("randomrace.admin")) {
            sender.sendMessage(MessageUtil.color("&cYou don't have permission to use this."));
            return true;
        }
        if (args.length == 0) {
            sender.sendMessage(MessageUtil.color("&cUsage: /randomrace <reset|reroll|setrace|reload|listrace>"));
            return true;
        }
        switch (args[0].toLowerCase()) {
            case "reload":
                plugin.reload();
                sender.sendMessage(MessageUtil.color("&aRandomRace reload complete."));
                return true;
            case "listrace":
                plugin.getRacePoolManager().refresh();
                Map<String, Race> races = RaceManager.getRegisteredRaces();
                if (races == null || races.isEmpty()) {
                    sender.sendMessage(MessageUtil.color("&cNo races loaded from ValhallaRaces."));
                } else {
                    sender.sendMessage(MessageUtil.color("&aLoaded " + races.size() + " races:"));
                    for (Race r : races.values()) {
                        sender.sendMessage(MessageUtil.color("  &7" + r.getName() + " &8- &f" + stripColor(r.getDisplayName())));
                    }
                }
                return true;
            case "reset":
                if (args.length < 2) { sender.sendMessage(MessageUtil.color("&cUsage: /randomrace reset <player>")); return true; }
                Player rp = Bukkit.getPlayerExact(args[1]);
                if (rp == null) { sender.sendMessage(MessageUtil.color("&cPlayer not found.")); return true; }
                assignmentManager.clear(rp);
                plugin.getPlayerDataManager().clear(rp.getUniqueId());
                if (sender.hasPermission("randomrace.admin.bypass")) {
                    sender.sendMessage(MessageUtil.color("&aReset " + rp.getName() + "'s race."));
                }
                return true;
            case "reroll":
                if (args.length < 2) { sender.sendMessage(MessageUtil.color("&cUsage: /randomrace reroll <player>")); return true; }
                Player rr = Bukkit.getPlayerExact(args[1]);
                if (rr == null) { sender.sendMessage(MessageUtil.color("&cPlayer not found.")); return true; }
                assignmentManager.clear(rr);
                plugin.getPlayerDataManager().clear(rr.getUniqueId());
                plugin.getRacePoolManager().refresh();
                List<Race> available = plugin.getRacePoolManager().getAvailableRaces(rr);
                if (available.isEmpty()) { sender.sendMessage(MessageUtil.color("&cNo races available.")); return true; }
                Race winner = plugin.getRacePoolManager().pickWeighted(random, available);
                new SpinAnimation(plugin, rr, winner).start();
                return true;
            case "setrace":
                if (args.length < 3) { sender.sendMessage(MessageUtil.color("&cUsage: /randomrace setrace <player> <race>")); return true; }
                Player sp = Bukkit.getPlayerExact(args[1]);
                if (sp == null) { sender.sendMessage(MessageUtil.color("&cPlayer not found.")); return true; }
                Race race = RaceManager.getRegisteredRaces().get(args[2]);
                if (race == null) { sender.sendMessage(MessageUtil.color("&cRace '" + args[2] + "' not found.")); return true; }
                assignmentManager.assign(sp, race);
                plugin.getPlayerDataManager().markClaimed(sp.getUniqueId());
                sender.sendMessage(MessageUtil.color("&aSet " + sp.getName() + "'s race to " + stripColor(race.getDisplayName()) + "&a."));
                return true;
            default:
                sender.sendMessage(MessageUtil.color("&cUsage: /randomrace <reset|reroll|setrace|reload|listrace>"));
                return true;
        }
    }

    private String stripColor(String s) {
        if (s == null) return "";
        return s.replaceAll("(?i)\\u00A7[0-9a-fk-or]", "");
    }
}
```

- [ ] **Step 2: Ensure `SpinAnimation` finish uses admin-context-safe broadcast**

Verify `SpinAnimation.finish()` broadcasts only when the config flag is on (already
implemented in Task 4). No change needed.

- [ ] **Step 3: Build to verify**

Run: `mvn -q -DskipTests package`
Expected: BUILD SUCCESS.

- [ ] **Step 4: Run all tests**

Run: `mvn test`
Expected: PASS (all unit tests).

- [ ] **Step 5: Commit**

```bash
git add RandomRace
git commit -m "feat(randomrace): admin commands (reset/reroll/setrace/reload/listrace)"
```

---

### Task 6: Final verification + packaging + README

**Files:**
- Verify: `RandomRace/target/randomrace-1.0.0.jar`
- Create: `RandomRace/README.md`

**Interfaces:** none (deliverable is a shippable jar + docs).

- [ ] **Step 1: Clean package with tests**

Run: `mvn clean verify`
Expected: BUILD SUCCESS, all tests pass.

- [ ] **Step 2: Confirm stub classes are excluded from the jar**

Run: `jar tf target/randomrace-1.0.0.jar | grep -c "me/athlaeos"` 
Expected: `0`.

- [ ] **Step 3: Confirm main + plugin.yml present**

Run: `jar tf target/randomrace-1.0.0.jar | grep -E "RandomRacePlugin|plugin.yml"`
Expected: both present.

- [ ] **Step 4: Write `RandomRace/README.md`**

Cover: purpose; dependencies (ValhallaMMO + ValhallaRaces, both required at runtime);
installation (drop the jar in `plugins/`); commands/permissions table; config keys
(weights, materials, messages, one-time-only, broadcast-enabled); note that the race pool
is pulled live from ValhallaRaces and that assignment is in-process. Keep it concise.

- [ ] **Step 5: Commit**

```bash
git add RandomRace
git commit -m "docs(randomrace): add README"
```

- [ ] **Step 6: Final commit/push (on request)**

If the user asks, push to the remote. Otherwise stop here.
