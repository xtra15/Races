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
