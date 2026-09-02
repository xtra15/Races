package com.yourname.randomrace.managers;

import me.athlaeos.valhallaraces.Class;
import me.athlaeos.valhallaraces.ClassManager;
import org.bukkit.entity.Player;

import java.util.Collection;
import java.util.Collections;

public class ClassAssignmentManager {

    public void assign(Player p, Collection<Class> classes) {
        ClassManager.setClasses(p, classes);
    }

    public void replaceAll(Player p, Collection<Class> classes) {
        assign(p, classes);
    }

    public void clear(Player p) {
        ClassManager.setClasses(p, Collections.emptyList());
    }

    public int count(Player p) {
        return ClassManager.getClasses(p).size();
    }
}
