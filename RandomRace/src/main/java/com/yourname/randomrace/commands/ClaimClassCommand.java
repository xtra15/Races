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
