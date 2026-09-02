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
        ClassPoolManager m = new ClassPoolManager(null);
        List<Class> all = Arrays.asList(
                cls("one", 1, null, Collections.emptyList()),
                cls("elf-only", 1, null, Arrays.asList("elf")),
                cls("other-group", 2, null, Collections.emptyList()),
                cls("locked", 1, "some.perm", Collections.emptyList()));
        m.poolForTest(all);
        List<Class> g1 = m.candidatesFor(1, null, "elf");
        List<String> ids = new java.util.ArrayList<>();
        for (Class c : g1) ids.add(c.getName());
        assertTrue(ids.contains("one"));
        assertTrue(ids.contains("elf-only"));
        assertFalse(ids.contains("other-group"));
        assertFalse(ids.contains("locked"));
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
