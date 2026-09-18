# Offline Reroll Points Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make admin-granted reroll points (`give`/`set`/`setslots`) survive a player's first login by migrating phantom `OfflinePlayer:<name>` records into the player's real UUID record on join.

**Architecture:** `PlayerDataManager.migrateByName` copies rerolls/class-slots/joined from a phantom playerdata key (whose stored `.name` matches the joiner) into the joiner's real-UUID record, then deletes the phantom key. `PlayerJoinListener` computes `first` before migrating (so the intro still shows), runs the migration, then marks joined. Testable via a package-private `migrateByName(UUID, String)` overload using the existing `PlayerDataManager(File)` constructor.

**Tech Stack:** Java 21, Paper API 1.21.1, Maven, JUnit 5 (jupiter).

## Global Constraints

- Working directory for all builds: `D:\e\Projects\ValhallaRaces\RandomRace`
- Java source is comment-free (project convention). No `console.log`-style noise.
- No git commits during implementation — the user commits/pushes when they choose. Do not stage or commit.
- Do not touch `target/` (git-ignored) or anything outside `D:\e\Projects\ValhallaRaces\RandomRace\` and the spec/plan docs.
- No version bump — this is a bugfix, not a release.
- `mvn` commands run from `D:\e\Projects\ValhallaRaces\RandomRace`.

---

### Task 1: `PlayerDataManager.migrateByName` + tests

Migration logic that moves a phantom-key record's reroll/slot data under the player's real UUID and removes the phantom key.

**Files:**
- Modify: `src/main/java/com/yourname/randomrace/managers/PlayerDataManager.java`
- Test: `src/test/java/com/yourname/randomrace/managers/PlayerDataManagerTest.java`

**Interfaces:**
- Consumes: nothing new (existing `hasRecord`, `save`, `getKeys`, `data`).
- Produces (used by Task 2):
  - `public void migrateByName(Player p)` — delegates to the overload below.
  - `void migrateByName(UUID uuid, String name)` — package-private, unit-testable (same package as the tests).

- [ ] **Step 1: Write the failing tests**

Append these three tests to `src/test/java/com/yourname/randomrace/managers/PlayerDataManagerTest.java`:

```java
@Test
void migrateMovesPhantomRerollsToRealUuid() {
    PlayerDataManager m = manager();
    UUID phantom = UUID.randomUUID();
    UUID real = UUID.randomUUID();
    m.setRace(phantom, "elf", "Steve");
    m.addRaceRerolls(phantom, 2);
    m.addClassRerolls(phantom, 3);
    m.setClassSlots(phantom, 5);
    m.migrateByName(real, "Steve");
    assertEquals(2, m.getRaceRerolls(real));
    assertEquals(3, m.getClassRerolls(real));
    assertEquals(5, m.getClassSlots(real));
    assertFalse(m.hasRecord(phantom));
}

@Test
void migrateIsNoOpWhenRealRecordExists() {
    PlayerDataManager m = manager();
    UUID phantom = UUID.randomUUID();
    UUID real = UUID.randomUUID();
    m.setRace(phantom, "elf", "Steve");
    m.addRaceRerolls(phantom, 2);
    m.markJoined(real);
    m.addRaceRerolls(real, 1);
    m.migrateByName(real, "Steve");
    assertEquals(1, m.getRaceRerolls(real));
    assertTrue(m.hasRecord(phantom));
}

@Test
void migrateDoesNotCopyDefaultSlots() {
    PlayerDataManager m = manager();
    UUID phantom = UUID.randomUUID();
    UUID real = UUID.randomUUID();
    m.setRace(phantom, "elf", "Steve");
    m.addRaceRerolls(phantom, 2);
    m.setClassSlots(phantom, -1);
    m.migrateByName(real, "Steve");
    assertEquals(2, m.getRaceRerolls(real));
    assertEquals(-1, m.getClassSlots(real));
    assertFalse(m.hasRecord(phantom));
}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `mvn -q test -Dtest=PlayerDataManagerTest`
Expected: FAIL — `migrateByName(java.util.UUID, java.lang.String)` does not exist.

- [ ] **Step 3: Implement migrateByName**

Add imports and the two methods in `PlayerDataManager.java`:

```java
import org.bukkit.entity.Player;
```

Add this field is already present — no field needed. Add the two methods after `markJoined` and before `clearClaim`:

```java
    public void migrateByName(Player p) {
        migrateByName(p.getUniqueId(), p.getName());
    }

    void migrateByName(UUID uuid, String name) {
        if (hasRecord(uuid)) return;
        boolean migrated = false;
        for (String key : data.getKeys(false)) {
            if (key.equals(uuid.toString())) continue;
            String stored = data.getString(key + ".name");
            if (stored == null || !stored.equalsIgnoreCase(name)) continue;
            int rr = data.getInt(key + ".race-rerolls", 0);
            int cr = data.getInt(key + ".class-rerolls", 0);
            int slots = data.getInt(key + ".class-slots", -1);
            if (rr > 0) data.set(uuid + ".race-rerolls", rr);
            if (cr > 0) data.set(uuid + ".class-rerolls", cr);
            if (slots >= 1) data.set(uuid + ".class-slots", slots);
            data.set(uuid + ".joined", data.getLong(key + ".joined", System.currentTimeMillis()));
            data.set(key, null);
            migrated = true;
            break;
        }
        if (migrated) save();
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `mvn -q test -Dtest=PlayerDataManagerTest`
Expected: PASS (all existing + 3 new tests green).

- [ ] **Step 5: Verify full tree compiles**

Run: `mvn -q compile`
Expected: BUILD SUCCESS.

---

### Task 2: `PlayerJoinListener` migration wiring

Runs the migration on join, keeping the first-join intro + reminder flow intact.

**Files:**
- Modify: `src/main/java/com/yourname/randomrace/listeners/PlayerJoinListener.java`

**Interfaces:**
- Consumes: Task 1 `public void migrateByName(Player p)`.
- Produces: join-time behavior (no new interface).

- [ ] **Step 1: Reorder onJoin**

In `PlayerJoinListener.java`, change the top of `onJoin` from:

```java
        boolean first = !plugin.getPlayerDataManager().hasRecord(uuid);
        if (first) {
            plugin.getPlayerDataManager().markJoined(uuid);
        }
```

to:

```java
        boolean first = !plugin.getPlayerDataManager().hasRecord(uuid);
        plugin.getPlayerDataManager().migrateByName(p);
        if (first) {
            plugin.getPlayerDataManager().markJoined(uuid);
        }
```

Everything below (the `runTaskLater` intro/reminder block) stays unchanged.

- [ ] **Step 2: Verify compile + full test suite**

Run: `mvn -q compile` — BUILD SUCCESS.
Run: `mvn -q test` — all tests green.

---

### Task 3: Final verification

- [ ] **Step 1: Full test suite**

Run: `mvn test`
Expected: all tests pass (30 existing + 3 new, no failures).

- [ ] **Step 2: Rebuild the jar**

Run: `mvn -q package`
Expected: BUILD SUCCESS. Verify with `Get-ChildItem target\randomrace-1.2.0.jar` that the jar exists (unchanged version).

- [ ] **Step 3: Report**

Summarize: `migrateByName` added (Player + package-private UUID/String overloads), `PlayerJoinListener` reordered, jar path, and the manual test script: admin `/randomrace give <player> race 2` for a player who has never joined → target logs in → first-join intro + a "2 race rerolls" reminder appear; `/randomrace check <player>` shows 2.

---

## Self-Review

- **Spec coverage:** `migrateByName(Player)` present (Task 1) · no-op when real record exists (Task 1, test 2) · copy rerolls only when > 0 (Task 1) · copy `class-slots` only when >= 1 (Task 1, test 3) · copy `joined` with now fallback (Task 1) · delete phantom key after single match (Task 1, `break`) · `first` computed before migration; `markJoined` still on first join; reminder unchanged (Task 2) · testing via package-private overload matching spec's test section (Task 1).
- **Placeholder scan:** All steps contain concrete code or exact commands; no TBDs.
- **Type consistency:** `migrateByName(Player)` (Task 2) and package-private `migrateByName(UUID, String)` (Task 1, test-facing) share one name with documented overloads; existing accessor names (`getRaceRerolls`, `getClassRerolls`, `getClassSlots`, `hasRecord`) reused verbatim.