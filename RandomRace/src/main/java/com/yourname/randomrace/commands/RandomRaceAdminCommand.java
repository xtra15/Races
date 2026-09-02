package com.yourname.randomrace.commands;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.gui.SpinAnimation;
import com.yourname.randomrace.managers.AssignmentManager;
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
                sender.sendMessage(MessageUtil.color("&aReset " + rp.getName() + "'s race."));
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
