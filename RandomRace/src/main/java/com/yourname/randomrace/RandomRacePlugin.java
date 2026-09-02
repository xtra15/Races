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
