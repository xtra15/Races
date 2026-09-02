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
